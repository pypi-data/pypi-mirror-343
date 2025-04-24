#!/usr/bin/env python3
"""
Core functionality for the Mintlify Changelog Generator.
"""
import os
import sys
import json
import textwrap
import time
import subprocess
from typing import Dict, Any, List, Optional
import requests

from mintlify_changelog.config import (
    get_api_key, 
    get_api_config, 
    get_default_count,
    get_template,
    load_config
)
from mintlify_changelog.analyzer import CommitAnalyzer
from mintlify_changelog.formatters import get_formatter
from mintlify_changelog.prompts import get_prompt_template


def ensure_git_repo() -> None:
    """Ensure the current directory is a git repository."""
    try:
        subprocess.check_output(["git", "rev-parse", "--is-inside-work-tree"], stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        sys.exit("Error: Not a git repository.")


def get_repo_info() -> Dict[str, Any]:
    """Get repository information to enrich the changelog context."""
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
                info["name"] = repo_match.group(1)
            else:
                info["name"] = os.path.basename(os.getcwd())
        except subprocess.CalledProcessError:
            # No remote or other issue
            info["name"] = os.path.basename(os.getcwd())
        
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
            
        # Get repo path
        try:
            repo_path = subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip()
            info["path"] = repo_path
        except subprocess.CalledProcessError:
            info["path"] = os.getcwd()
        
    except Exception as e:
        print(f"Warning: Error getting repo info: {e}", file=sys.stderr)
    
    return info


def call_claude(
    prompt: str,
    system_prompt: str,
    api_config: Optional[Dict[str, Any]] = None
) -> str:
    """Call the Claude API to generate a changelog.
    
    Handles retries and various API response formats gracefully.
    """
    if api_config is None:
        api_config = get_api_config()
        
    # Get API settings
    base_url = api_config.get("base_url", "https://mintlify-take-home.com")
    endpoint = api_config.get("endpoint", "/api/message")
    model = api_config.get("model", "claude-3-5-sonnet-latest")
    max_tokens = api_config.get("max_tokens", 4096)
    temperature = api_config.get("temperature", 0.5)
    timeout = api_config.get("timeout", 60)
    
    # Get API key
    api_key = get_api_key()
    if not api_key:
        sys.exit("Error: No API key found. Set one with --set-api-key or the MINTLIFY_API_KEY environment variable.")
    
    # Prepare request
    url = base_url.rstrip('/') + endpoint
    headers = {"X-API-Key": api_key, "Content-Type": "application/json"}
    payload = {
        "model": model,
        "system": system_prompt,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    
    # Add retry logic for better reliability
    max_retries = 2
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries + 1):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
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
      mintlify-changelog --theme conventional # Use conventional commit theme
      mintlify-changelog --format html       # Output as HTML
    
    For more options:
      mintlify-changelog --help
    """))


def generate_changelog(
    count: int = None,
    dry_run: bool = False,
    output_file: Optional[str] = None,
    title: str = "📋 CHANGELOG",
    theme: str = "standard",
    output_format: str = "markdown",
    release_cycle: str = None,
    show_progress: bool = True
) -> str:
    """
    Main function to generate a changelog.
    
    Args:
        count: Number of commits to analyze
        dry_run: If True, only show the prompt without calling the API
        output_file: Path to save the changelog to
        title: Custom title for the changelog
        theme: Theme name for prompt style
        output_format: Output format (markdown, html, json, text)
        release_cycle: Time-based grouping for entries ("auto", "daily", "weekly", "monthly", "none")
        show_progress: Whether to show progress indicators
        
    Returns:
        The generated changelog text
    """
    if count is None:
        count = get_default_count()
        
    if count < 1:
        raise ValueError("Count must be >= 1")
        
    if release_cycle is None:
        config = load_config()
        release_cycle = config.get("defaults", {}).get("release_cycle", "auto")

    # Show progress indicator
    if show_progress:
        print("🔍 Analyzing git repository...", end="\r")
    
    try:
        ensure_git_repo()
        
        # Set up analyzer with chosen template
        analyzer = CommitAnalyzer()
        
        # Get repository information
        repo_info = get_repo_info()
        
        # Fetch and analyze commits
        commits = analyzer.fetch_commits(count)
        if not commits:
            raise ValueError("No commits found.")
            
        # Get commit summary lines
        commit_lines = analyzer.get_commit_summary_lines(commits)
        
        # Analyze commit patterns
        analysis = analyzer.analyze_commit_patterns(commits)
        
    except Exception as e:
        raise RuntimeError(f"Error analyzing repository: {e}")
        
    if show_progress:
        print(" " * 80, end="\r")  # Clear progress line
        print(f"📊 Found {len(commits)} commits to process")

    # Prepare prompt context
    context = {
        "repository": repo_info,
        "commit_lines": commit_lines,
        "analysis": analysis,
        "release_cycle": release_cycle
    }
    
    # Get appropriate prompt template
    prompt_template = get_prompt_template(theme)
    system_prompt = prompt_template.get_system_prompt()
    user_prompt = prompt_template.get_user_prompt(context)
    
    if dry_run:
        if show_progress:
            print("\n" + "═" * 80)
            print("🔍 PROMPT PREVIEW (--dry-run)")
            print("═" * 80)
            print(f"System Prompt:\n{system_prompt}")
            print("\nUser Prompt:\n{user_prompt}")
        return user_prompt

    if show_progress:
        print("🤖 Generating changelog with Claude AI...", end="\r")
        if release_cycle != "none":
            print(f"Using {release_cycle} release cycle grouping...", end="\r")
        
    try:
        # Call API to generate changelog
        changelog = call_claude(user_prompt, system_prompt)
    except Exception as e:
        raise RuntimeError(f"Failed to generate changelog: {e}")
    
    # Format output
    formatter = get_formatter(output_format, repo_info.get("name", ""))
    formatted_output = formatter.format(changelog)
    
    # Print results
    if show_progress:
        print(" " * 80, end="\r")  # Clear progress line
        
        # For non-plain text formats, print in console-friendly format
        if output_format not in ["json", "html"]:
            print("\n" + "═" * 80)
            print(title)
            print("═" * 80)
            print(formatted_output)
            print("═" * 80)
    
    # Save to file if requested
    if output_file:
        try:
            with open(output_file, "w") as f:
                if output_format == "markdown":
                    # Add a header with timestamp for markdown
                    from datetime import datetime
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"# {title}\n\n")
                    f.write(f"_Generated on {now}_\n\n")
                
                f.write(formatted_output)
                
            if show_progress:
                print(f"\n✅ Changelog saved to {output_file}")
            
            # Offer to copy to clipboard on macOS
            if show_progress and sys.platform == "darwin" and output_format != "html":
                try:
                    clipboard_cmd = ["pbcopy"]
                    clipboard_proc = subprocess.Popen(clipboard_cmd, stdin=subprocess.PIPE)
                    clipboard_proc.communicate(input=formatted_output.encode())
                    print("📋 Changelog copied to clipboard")
                except:
                    pass
        except Exception as e:
            if show_progress:
                print(f"\n❌ Error saving changelog: {e}")
    
    return formatted_output