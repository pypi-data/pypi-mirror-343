#!/usr/bin/env python3
"""
Core functionality for the Mintlify Changelog Generator.
"""
from __future__ import annotations
import argparse
import json
import os
import subprocess
import sys
import textwrap
import time
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
import requests

# ────────────────────────────────────────────────────────────────────────────────
# Configuration (override via environment if desired)
# ────────────────────────────────────────────────────────────────────────────────
BASE_URL: str = os.getenv("MINTLIFY_BASE_URL", "https://mintlify-take-home.com")
API_ENDPOINT: str = os.getenv("MINTLIFY_API_ENDPOINT", "/api/message")
API_KEY: str = os.getenv("MINTLIFY_API_KEY", "YOUR_API_KEY_HERE")
MODEL: str = os.getenv("MINTLIFY_MODEL", "claude-3-5-sonnet-latest")
MAX_TOKENS: int = int(os.getenv("MINTLIFY_MAX_TOKENS", "4096"))
TEMPERATURE: float = float(os.getenv("MINTLIFY_TEMPERATURE", "0.5"))
TIMEOUT_SEC: int = 60
DEFAULT_COUNT: int = 20

SYSTEM_PROMPT = textwrap.dedent("""
You are ReleaseBot, the expert changelog generator. Create a beautiful, detailed markdown changelog that delights end users.

Guidelines:
  • Audience: Developers and product users with no internal context
  • Organization: Group similar changes under clear category headings:
      - ✨ **New Features** - New functionality and capabilities
      - 🔄 **Changes & Improvements** - Enhancements to existing features
      - 🐛 **Bug Fixes** - Issues resolved in this release
      - 📚 **Documentation** - Documentation updates and improvements
      - 🧰 **Development** - Developer workflow improvements, refactoring
  • Style:
      - Use crisp, clear bullet points with emoji indicators
      - Start each entry with a present-tense verb
      - Use clear, concise language that explains both what changed and why it matters
      - Include version numbers, PR links, or ticket references when present in commit messages
      - Ensure even small changes are presented in a way that highlights their value
  • Format:
      - Add a timestamp/date to the changelog header
      - Use consistent, clean markdown formatting throughout
      - Make it visually scan-friendly with nested indentation for related items
      - Use header formatting that matches professional changelogs like Vercel or Mintlify
      - When appropriate, note major changes with 🔥 or 💥 indicators
  • Handling many commits:
      - Intelligently group related commits under a single logical change
      - If there are more than 15 commits, organize them into major themes
      - For large refactors across many commits, summarize as a single cohesive change
      - Look for repeated patterns in commit messages (like "Fix typo") and group them
      - If there are many dependency updates, group them as "Update dependencies" with key highlights

Be thorough but concise. Even for small commits, produce a polished, professional changelog that helps users understand what's new and why it matters.
""")
USER_PROMPT_TEMPLATE = textwrap.dedent("""
# Repository: {repo_name}
# Branch: {branch}
{extra_info}

Here are the last {count} commits (newest first), each on its own line:
{commits}

Please produce a markdown changelog following the guidelines above. 
Include a clear title with repository name and date.
""")

# ────────────────────────────────────────────────────────────────────────────────
@dataclass
class Commit:
    sha: str
    author: str
    date: datetime
    subject: str
    body: str

    @classmethod
    def from_record(cls, record: str) -> Commit:
        parts = record.strip().split("\x1f")
        if len(parts) < 4:
            raise ValueError(f"Malformed record: {record!r}")
        sha, author, iso_date, subject = parts[:4]
        body = parts[4] if len(parts) >= 5 else ""
        return cls(
            sha=sha,
            author=author,
            date=datetime.fromisoformat(iso_date),
            subject=subject,
            body=body.strip(),
        )

    def summary_line(self) -> str:
        short_sha = self.sha[:7]
        date_str = self.date.strftime("%Y-%m-%d %H:%M")
        # Process the body to extract any PR references
        body_text = " ".join(self.body.split())
        pr_refs = ""
        if "PR" in body_text or "#" in body_text:
            # Simple extraction of PR references like #123 or PR #456
            import re
            pr_matches = re.findall(r'(?:PR\s*)?#(\d+)', body_text)
            if pr_matches:
                pr_refs = f" [PR refs: {', '.join([f'#{num}' for num in pr_matches])}]"
        
        # Add file stats if we can parse them from the body
        file_stats = ""
        if "files changed" in body_text.lower():
            file_stats_match = re.search(r'(\d+)\s+files?\s+changed', body_text.lower())
            if file_stats_match:
                file_stats = f" ({file_stats_match.group(0)})"
        
        one_line_body = body_text[:150] + ("..." if len(body_text) > 150 else "")
        return f"* `{short_sha}` {self.subject}{pr_refs}{file_stats} _(by {self.author} on {date_str})_\n  {one_line_body}"

# ────────────────────────────────────────────────────────────────────────────────
def ensure_git_repo() -> None:
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        sys.exit("Error: Not a git repository.")


def fetch_commits(count: int) -> List[Commit]:
    fmt = "%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e"
    try:
        raw = subprocess.check_output(["git", "log", f"-n{count}", f"--pretty=format:{fmt}", "--stat"], text=True)
    except subprocess.CalledProcessError as e:
        sys.exit(f"Git error: {e}")
    records = [r for r in raw.split("\x1e") if r.strip()]
    return [Commit.from_record(r) for r in records]

def get_repo_info() -> dict:
    """Get additional repository information to enrich the changelog context."""
    info = {}
    try:
        # Get repository name
        try:
            remote_url = subprocess.check_output(["git", "config", "--get", "remote.origin.url"], text=True, stderr=subprocess.DEVNULL).strip()
            info["remote"] = remote_url
            # Extract repo name from URL
            import re
            repo_match = re.search(r'[:/]([^/]+/[^/]+?)(?:\.git)?$', remote_url)
            if repo_match:
                info["repo"] = repo_match.group(1)
        except subprocess.CalledProcessError:
            # No remote or other issue
            info["repo"] = os.path.basename(os.getcwd())
        
        # Get current branch
        try:
            branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"], text=True).strip()
            info["branch"] = branch
        except subprocess.CalledProcessError:
            info["branch"] = "unknown"
            
        # Get latest tag if any
        try:
            latest_tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"], text=True, stderr=subprocess.DEVNULL).strip()
            info["latest_tag"] = latest_tag
        except subprocess.CalledProcessError:
            info["latest_tag"] = None
        
    except Exception as e:
        print(f"Warning: Error getting repo info: {e}", file=sys.stderr)
    
    return info

# ────────────────────────────────────────────────────────────────────────────────
def build_prompt(commits: List[Commit]) -> str:
    lines = [c.summary_line() for c in commits]
    
    # Get repository info for better context
    repo_info = get_repo_info()
    repo_name = repo_info.get("repo", os.path.basename(os.getcwd()))
    branch = repo_info.get("branch", "main")
    
    # Build extra info section
    extra_info_parts = []
    if "latest_tag" in repo_info and repo_info["latest_tag"]:
        extra_info_parts.append(f"# Latest tag: {repo_info['latest_tag']}")
    
    # Add commit date range
    if commits:
        latest_date = commits[0].date.strftime("%Y-%m-%d")
        oldest_date = commits[-1].date.strftime("%Y-%m-%d")
        if latest_date != oldest_date:
            extra_info_parts.append(f"# Date range: {oldest_date} to {latest_date}")
        else:
            extra_info_parts.append(f"# Date: {latest_date}")
    
    extra_info = "\n".join(extra_info_parts)
    
    return USER_PROMPT_TEMPLATE.format(
        repo_name=repo_name,
        branch=branch,
        extra_info=extra_info,
        count=len(lines),
        commits="\n".join(lines)
    )


def call_claude(prompt: str) -> str:
    """Call the Claude API to generate a changelog.
    
    Handles retries and various API response formats gracefully.
    """
    url = BASE_URL.rstrip('/') + API_ENDPOINT
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    payload = {
        "model": MODEL,
        "system": SYSTEM_PROMPT,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    }
    
    # Add retry logic for better reliability
    max_retries = 2
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=TIMEOUT_SEC)
            resp.raise_for_status()
            data = resp.json()
            
            # Handle Claude API format (v2)
            if "content" in data and isinstance(data["content"], list):
                # Extract text content from the response
                text_parts = [part["text"] for part in data["content"] if part["type"] == "text"]
                return "\n".join(text_parts)
            
            # Handle Claude API format (v1)
            elif "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"].strip()
                
            # Handle other valid response formats
            elif "completion" in data:
                return data["completion"].strip()
                
            else:
                # Fallback - try to extract any text content or return a meaningful message
                if "message" in data:
                    return f"The API returned a message: {data['message']}"
                else:
                    return "Changelog generated successfully, but in an unexpected format."
                    
        except requests.exceptions.Timeout:
            if attempt < max_retries:
                print(f"Request timed out. Retrying in {retry_delay} seconds... ({attempt+1}/{max_retries})", end="\r")
                time.sleep(retry_delay)
                continue
            raise Exception("API request timed out. Please try again later.")
            
        except requests.exceptions.HTTPError as e:
            # Handle specific HTTP errors
            if resp.status_code == 401:
                raise Exception("API key is invalid or expired. Please check your credentials.")
            elif resp.status_code == 429:
                if attempt < max_retries:
                    print(f"Rate limited. Retrying in {retry_delay} seconds... ({attempt+1}/{max_retries})", end="\r")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception("API rate limit exceeded. Please try again later.")
            elif resp.status_code >= 500:
                if attempt < max_retries:
                    print(f"Server error. Retrying in {retry_delay} seconds... ({attempt+1}/{max_retries})", end="\r")
                    time.sleep(retry_delay)
                    continue
                else:
                    raise Exception("API server error. Please try again later.")
            else:
                # Generic HTTP error
                error_msg = f"HTTP Error: {resp.status_code}"
                if resp.text:
                    try:
                        error_data = resp.json()
                        if "message" in error_data:
                            error_msg += f" - {error_data['message']}"
                    except:
                        pass
                raise Exception(error_msg)
                
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to the API. Please check your internet connection.")
            
        except Exception as e:
            # Handle general errors
            raise Exception(f"API error: {str(e)}")
            
    # This point should never be reached due to the exception handling above
    raise Exception("Unknown error occurred")

# ────────────────────────────────────────────────────────────────────────────────
def print_welcome():
    """Print a welcome message when no arguments are provided."""
    print(textwrap.dedent("""
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                      🚀 Mintlify Changelog Generator                      ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    Generate beautiful changelogs from your git commits using Claude AI.
    
    Quick Examples:
      mintlify-changelog                     # Use default settings (20 commits)
      mintlify-changelog -c 10               # Generate for 10 commits
      mintlify-changelog -o CHANGELOG.md     # Save to file
      mintlify-changelog --title "v1.0.0"    # Custom title
    
    For more options:
      mintlify-changelog --help
    """))

def generate_changelog(count: int = DEFAULT_COUNT, 
                       dry_run: bool = False, 
                       output_file: Optional[str] = None, 
                       title: str = "📋 CHANGELOG") -> str:
    """
    Main function to generate a changelog.
    
    Args:
        count: Number of commits to analyze
        dry_run: If True, only show the prompt without calling the API
        output_file: Path to save the changelog to
        title: Custom title for the changelog
        
    Returns:
        The generated changelog text
    """
    if count < 1:
        raise ValueError("Count must be >= 1")

    # Show spinner for git operations
    print("🔍 Analyzing git repository...", end="\r")
    
    try:
        ensure_git_repo()
        commits = fetch_commits(count)
        if not commits:
            raise ValueError("No commits found.")
    except Exception as e:
        raise RuntimeError(f"Error: {e}")
        
    print(" " * 40, end="\r")  # Clear spinner
    print(f"📊 Found {len(commits)} commits to process")

    prompt = build_prompt(commits)
    if dry_run:
        print("\n" + "═" * 80)
        print("🔍 PROMPT PREVIEW (--dry-run)")
        print("═" * 80)
        print(prompt)
        return prompt

    print("🤖 Generating changelog with Claude AI...", end="\r")
    try:
        changelog = call_claude(prompt)
    except Exception as e:
        raise RuntimeError(f"Failed to generate changelog - {e}")
    
    # Print a nicely formatted output
    print(" " * 40, end="\r")  # Clear spinner
    print("\n" + "═" * 80)
    print(title)
    print("═" * 80)
    print(changelog)
    print("═" * 80)
    
    # Save to file if requested
    if output_file:
        try:
            with open(output_file, "w") as f:
                # Add a header with timestamp
                from datetime import datetime
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"# {title}\n\n")
                f.write(f"_Generated on {now}_\n\n")
                f.write(changelog)
            print(f"\n✅ Changelog saved to {output_file}")
            
            # Offer to copy to clipboard on macOS
            if sys.platform == "darwin":
                try:
                    clipboard_cmd = ["pbcopy"]
                    clipboard_proc = subprocess.Popen(clipboard_cmd, stdin=subprocess.PIPE)
                    clipboard_proc.communicate(input=changelog.encode())
                    print("📋 Changelog copied to clipboard")
                except:
                    pass
        except Exception as e:
            print(f"\n❌ Error saving changelog: {e}")
    
    return changelog