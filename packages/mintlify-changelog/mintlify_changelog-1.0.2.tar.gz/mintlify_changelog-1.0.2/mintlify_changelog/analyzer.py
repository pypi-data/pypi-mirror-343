#!/usr/bin/env python3
"""
Commit analyzer for processing git history.

Provides tools for analyzing, categorizing, and structuring git commits
to prepare them for changelog generation.
"""
import re
import os
from collections import defaultdict, Counter
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import subprocess
from mintlify_changelog.config import get_template


@dataclass
class CommitInfo:
    """Information about a single commit."""
    sha: str
    author: str
    date: datetime
    subject: str
    body: str
    files_changed: List[str]
    stats: Dict[str, int]
    
    @property
    def short_sha(self) -> str:
        """Return shortened commit SHA."""
        return self.sha[:7]
    
    @property
    def pr_references(self) -> List[str]:
        """Extract PR references from commit message."""
        all_text = f"{self.subject} {self.body}"
        return re.findall(r'(?:PR\s*)?#(\d+)', all_text)
    
    @property
    def file_extensions(self) -> List[str]:
        """Get list of file extensions affected by this commit."""
        extensions = []
        for file in self.files_changed:
            _, ext = os.path.splitext(file)
            if ext and ext not in extensions:
                extensions.append(ext)
        return extensions
    
    def categorize(self, categories: List[Dict[str, Any]]) -> str:
        """Categorize commit based on patterns."""
        subject_lower = self.subject.lower()
        
        # Try to match conventional commit format first
        conventional_match = re.match(r'^(\w+)(\([^)]+\))?:', self.subject)
        if conventional_match:
            commit_type = conventional_match.group(1)
            for category in categories:
                if commit_type in category["patterns"]:
                    return category["name"]
        
        # Otherwise, look for patterns in the subject
        for category in categories:
            for pattern in category["patterns"]:
                if pattern.lower() in subject_lower:
                    return category["name"]
        
        # Default to "Other" or the last category
        return categories[-1]["name"]
    
    def is_merge_commit(self) -> bool:
        """Check if this is a merge commit."""
        return self.subject.startswith("Merge")
    
    def is_dependency_update(self) -> bool:
        """Check if this is a dependency update commit."""
        dep_keywords = ["dependency", "dependencies", "deps", "bump", "upgrade", "update"]
        package_refs = ["package.json", "requirements.txt", "Gemfile", "go.mod", "pom.xml"]
        
        # Check subject
        subject_lower = self.subject.lower()
        if any(kw in subject_lower for kw in dep_keywords):
            return True
        
        # Check files changed
        for file in self.files_changed:
            if any(dep_file in file for dep_file in package_refs):
                return True
                
        return False
    
    def __str__(self) -> str:
        """String representation for human readability."""
        files_str = f"{len(self.files_changed)} files" if self.files_changed else "Unknown files"
        date_str = self.date.strftime("%Y-%m-%d %H:%M")
        pr_refs = f" [PR #{', #'.join(self.pr_references)}]" if self.pr_references else ""
        
        return f"`{self.short_sha}` {self.subject}{pr_refs} _(by {self.author} on {date_str}, {files_str})_"


class CommitAnalyzer:
    """Analyzes git commits to prepare for changelog generation."""
    
    def __init__(self, template_name: str = "default"):
        """Initialize analyzer with template."""
        self.template = get_template(template_name)
        
    def fetch_commits(self, count: int) -> List[CommitInfo]:
        """Fetch detailed information about git commits."""
        # Get basic commit data
        fmt = "%H%x1f%an%x1f%aI%x1f%s%x1f%b%x1e"
        raw = subprocess.check_output(
            ["git", "log", f"-n{count}", f"--pretty=format:{fmt}"], 
            text=True
        )
        
        # Parse commit data
        commits = []
        records = [r for r in raw.split("\x1e") if r.strip()]
        
        for record in records:
            # Parse each commit
            parts = record.strip().split("\x1f")
            if len(parts) < 4:
                continue
                
            sha, author, iso_date, subject = parts[:4]
            body = parts[4] if len(parts) >= 5 else ""
            
            # Get files changed and stats
            files_changed, stats = self._get_commit_stats(sha)
            
            # Create commit info
            commit = CommitInfo(
                sha=sha,
                author=author,
                date=datetime.fromisoformat(iso_date),
                subject=subject,
                body=body.strip(),
                files_changed=files_changed,
                stats=stats
            )
            
            commits.append(commit)
            
        return commits
    
    def _get_commit_stats(self, sha: str) -> Tuple[List[str], Dict[str, int]]:
        """Get files changed and stats for a commit."""
        files_changed = []
        stats = {"additions": 0, "deletions": 0, "total": 0}
        
        try:
            # Get files changed
            files_output = subprocess.check_output(
                ["git", "show", "--name-only", "--pretty=format:", sha],
                text=True
            )
            files_changed = [f for f in files_output.strip().split("\n") if f]
            
            # Get stats
            stats_output = subprocess.check_output(
                ["git", "show", "--stat", "--pretty=format:", sha],
                text=True
            )
            
            # Parse stats
            additions_match = re.search(r'(\d+) insertion', stats_output)
            deletions_match = re.search(r'(\d+) deletion', stats_output)
            
            if additions_match:
                stats["additions"] = int(additions_match.group(1))
            if deletions_match:
                stats["deletions"] = int(deletions_match.group(1))
                
            stats["total"] = stats["additions"] + stats["deletions"]
            
        except Exception:
            # Just continue if we can't get stats
            pass
            
        return files_changed, stats
    
    def categorize_commits(self, commits: List[CommitInfo]) -> Dict[str, List[CommitInfo]]:
        """Categorize commits into sections."""
        categories = self.template.get("categories", [])
        categorized = defaultdict(list)
        
        for commit in commits:
            # Skip merge commits if desired
            if commit.is_merge_commit():
                continue
                
            category = commit.categorize(categories)
            categorized[category].append(commit)
            
        return dict(categorized)
    
    def analyze_commit_patterns(self, commits: List[CommitInfo]) -> Dict[str, Any]:
        """Analyze commits for patterns and insights."""
        # Initialize stats
        stats = {
            "total_commits": len(commits),
            "date_range": None,
            "top_authors": {},
            "top_file_types": {},
            "category_distribution": {},
            "large_changes": [],
            "dependency_updates": [],
            "estimated_scope": "minor",  # default
            "commit_dates": []  # Store commit dates for time-based grouping
        }
        
        if not commits:
            return stats
        
        # Calculate date range and collect all commit dates
        newest_date = commits[0].date
        oldest_date = commits[-1].date
        stats["date_range"] = (oldest_date, newest_date)
        
        # Store all commit dates for time-based grouping
        stats["commit_dates"] = [commit.date for commit in commits]
        
        # Count authors
        author_counts = Counter([commit.author for commit in commits])
        stats["top_authors"] = dict(author_counts.most_common(3))
        
        # Count file types
        extensions = []
        for commit in commits:
            extensions.extend(commit.file_extensions)
        stats["top_file_types"] = dict(Counter(extensions).most_common(5))
        
        # Categorize commits
        categorized = self.categorize_commits(commits)
        stats["category_distribution"] = {k: len(v) for k, v in categorized.items()}
        
        # Find large changes
        large_changes = [c for c in commits if c.stats.get("total", 0) > 100]
        stats["large_changes"] = large_changes
        
        # Find dependency updates
        stats["dependency_updates"] = [c for c in commits if c.is_dependency_update()]
        
        # Guess semantic version change
        stats["estimated_scope"] = self._estimate_version_scope(commits, categorized)
        
        return stats
    
    def _estimate_version_scope(self, 
                               commits: List[CommitInfo], 
                               categorized: Dict[str, List[CommitInfo]]) -> str:
        """Estimate the scope of changes (major, minor, patch)."""
        # Simple heuristic based on conventional commits
        breaking_changes = sum(1 for c in commits if "BREAKING CHANGE" in c.body)
        
        # Count new features
        feature_categories = ["Features", "New Features", "Added"]
        feature_count = sum(len(categorized.get(cat, [])) for cat in feature_categories)
        
        # Count bug fixes
        fix_categories = ["Bug Fixes", "Fixed"]
        fix_count = sum(len(categorized.get(cat, [])) for cat in fix_categories)
        
        if breaking_changes > 0:
            return "major"
        elif feature_count > 0:
            return "minor"
        else:
            return "patch"
    
    def build_prompt_context(self, 
                            commits: List[CommitInfo], 
                            repo_info: Dict[str, Any] = None) -> Dict[str, Any]:
        """Build enhanced context for the AI prompt."""
        # Analyze commits
        analysis = self.analyze_commit_patterns(commits)
        
        # Create context
        context = {
            "repository": repo_info or {},
            "commits": [
                {
                    "sha": c.short_sha,
                    "subject": c.subject,
                    "author": c.author,
                    "date": c.date.isoformat(),
                    "category": c.categorize(self.template.get("categories", [])),
                    "pr_references": c.pr_references,
                    "is_dependency_update": c.is_dependency_update(),
                    "is_merge_commit": c.is_merge_commit(),
                    "files_changed_count": len(c.files_changed),
                }
                for c in commits
            ],
            "analysis": {
                "total_commits": analysis["total_commits"],
                "date_range": (
                    analysis["date_range"][0].strftime("%Y-%m-%d"),
                    analysis["date_range"][1].strftime("%Y-%m-%d")
                ) if analysis["date_range"] else None,
                "category_distribution": analysis["category_distribution"],
                "estimated_scope": analysis["estimated_scope"],
                "has_dependency_updates": len(analysis["dependency_updates"]) > 0,
                "has_large_changes": len(analysis["large_changes"]) > 0,
            },
            "categories": self.template.get("categories", [])
        }
        
        return context
    
    def get_commit_summary_lines(self, commits: List[CommitInfo]) -> List[str]:
        """Get formatted commit summary lines for each commit."""
        return [str(commit) for commit in commits]