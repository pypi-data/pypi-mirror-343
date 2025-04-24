#!/usr/bin/env python3
"""
AI prompt templates for changelog generation.

Provides different prompt templates for various changelog styles.
"""
import textwrap
from typing import Dict, Any, List


class PromptTemplate:
    """Base class for prompt templates."""
    
    name = "base"
    description = "Base prompt template"
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the AI."""
        raise NotImplementedError("Subclasses must implement get_system_prompt()")
    
    def get_user_prompt(self, context: Dict[str, Any]) -> str:
        """Get the user prompt with context variables."""
        raise NotImplementedError("Subclasses must implement get_user_prompt()")


class StandardPrompt(PromptTemplate):
    """Standard prompt for general-purpose changelogs."""
    
    name = "standard"
    description = "Detailed, professional changelog with rich formatting"
    
    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return textwrap.dedent("""
        You are ReleaseBot, the expert changelog generator. Create a beautiful, detailed markdown changelog that delights end users.

        Guidelines:
          • Audience: Developers and product users with no internal context
          • Organization: Group similar changes under clear category headings:
              - ✨ **New Features** - New functionality and capabilities
              - 🔄 **Changes & Improvements** - Enhancements to existing features
              - 🐛 **Bug Fixes** - Issues resolved in this release
              - 📚 **Documentation** - Documentation updates and improvements
              - 🧰 **Development** - Developer workflow improvements, refactoring
              - 🔒 **Security** - Security improvements and vulnerability fixes
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
              - For large refactors across many commits, summarize as a single cohesive change
              - Look for repeated patterns in commit messages (like "Fix typo") and group them
              - If there are many dependency updates, group them as "Update dependencies" with key highlights

        Be thorough but concise. Even for small commits, produce a polished, professional changelog that helps users understand what's new and why it matters.
        """)
    
    def get_user_prompt(self, context: Dict[str, Any]) -> str:
        """Get user prompt with context."""
        # Extract repository information
        repo_name = context.get("repository", {}).get("name", "Project")
        branch = context.get("repository", {}).get("branch", "main")
        
        # Get date information
        date_range = context.get("analysis", {}).get("date_range")
        date_info = f"Date range: {date_range[0]} to {date_range[1]}" if date_range else ""
        
        # Get release cycle preference
        release_cycle = context.get("release_cycle", "auto")
        
        # Get commit dates for time-based grouping
        commit_dates = context.get("analysis", {}).get("commit_dates", [])
        
        # Get commit information
        commit_count = context.get("analysis", {}).get("total_commits", 0)
        commit_lines = [f"* {c}" for c in context.get("commit_lines", [])]
        commits_text = "\n".join(commit_lines)
        
        # Build the prompt
        prompt = textwrap.dedent(f"""
        # Repository: {repo_name}
        # Branch: {branch}
        # {date_info}
        # Estimated version change: {context.get("analysis", {}).get("estimated_scope", "Unknown")}
        # Release cycle: {release_cycle}
        
        Here are the last {commit_count} commits (newest first), each on its own line:
        {commits_text}
        
        Please produce a markdown changelog following the guidelines above.
        Include a clear title with repository name and date.
        
        Important: For time-based organization of the changelog entries:
        - Use release cycle: "{release_cycle}"
        - If "auto": Intelligently determine if entries should be grouped by day, week, or all together
        - If "daily": Group entries by day with clear date headers
        - If "weekly": Group entries by week with clear week headers
        - If "monthly": Group entries by month with clear month headers
        - If "none": Do not use time-based grouping, focus only on categorizing by type
        """)
        
        return prompt


class ConventionalPrompt(PromptTemplate):
    """Prompt for conventional commit formatted repositories."""
    
    name = "conventional"
    description = "Follows Conventional Commits standard with semantic versioning"
    
    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return textwrap.dedent("""
        You are ReleaseBot, a changelog generator specializing in Conventional Commits. Create a standards-compliant changelog that follows conventional commit and semantic versioning best practices.

        Guidelines:
          • Audience: Developers and users who understand semantic versioning
          • Organization: Group changes under standard conventional commit types:
              - ✨ **Features** (feat) - New functionality
              - 🐛 **Bug Fixes** (fix) - Bug fixes
              - 💎 **Styles** (style) - Changes that don't affect code functionality
              - ♻️ **Refactoring** (refactor) - Code changes that neither fix bugs nor add features
              - ⚡ **Performance** (perf) - Performance improvements
              - 🧪 **Tests** (test) - Adding or correcting tests
              - 📚 **Documentation** (docs) - Documentation only changes
              - 🔧 **Build** (build) - Changes to build system or dependencies
              - 🤖 **CI** (ci) - Changes to CI configuration
              - 🔨 **Chore** (chore) - Other changes not modifying source or test files
              - ⏪ **Revert** (revert) - Reverts a previous commit
          • Style:
              - Follow keep-a-changelog format (keepachangelog.com)
              - Use brief, clear language focused on the technical change
              - Highlight scope in parentheses when available
              - Include ticket/issue references
              - Use proper semantic versioning sections
          • Format:
              - Start with a version header (based on semantic versioning)
              - Group changes under their respective type headings
              - List each change with its scope if available
              - Mark breaking changes with BREAKING CHANGE: prefix
              - Use GitHub issue/PR reference format (#123)

        Be comprehensive and precise, focusing on technical accuracy over marketing language.
        """)
    
    def get_user_prompt(self, context: Dict[str, Any]) -> str:
        """Get user prompt with context."""
        # Extract repository information
        repo_name = context.get("repository", {}).get("name", "Project")
        
        # Get semantic version info
        scope = context.get("analysis", {}).get("estimated_scope", "minor")
        
        # Get release cycle preference
        release_cycle = context.get("release_cycle", "auto")
        
        # Get commit information
        commit_count = context.get("analysis", {}).get("total_commits", 0)
        commit_lines = [f"* {c}" for c in context.get("commit_lines", [])]
        commits_text = "\n".join(commit_lines)
        
        # Build the prompt
        prompt = textwrap.dedent(f"""
        # Repository: {repo_name}
        # Commits: {commit_count}
        # Estimated version bump: {scope}
        # Release cycle: {release_cycle}
        
        Here are the last {commit_count} commits (newest first):
        {commits_text}
        
        Please generate a changelog following the Conventional Commits standard.
        Include a semantic version header (based on {scope} changes) and group changes by commit type.
        
        Important: For time-based organization of the changelog entries:
        - Use release cycle: "{release_cycle}"
        - If "auto": Intelligently determine if entries should be grouped by day, week, or all together
        - If "daily": Group entries by day with clear date headers
        - If "weekly": Group entries by week with clear week headers
        - If "monthly": Group entries by month with clear month headers
        - If "none": Do not use time-based grouping, focus only on categorizing by type
        """)
        
        return prompt


class MinimalPrompt(PromptTemplate):
    """Simple, minimal prompt for concise changelogs."""
    
    name = "minimal"
    description = "Concise, clean changelog with minimal formatting"
    
    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return textwrap.dedent("""
        You are ReleaseBot, generating minimal, clean changelogs. Create a concise, no-frills changelog that focuses on essential information.

        Guidelines:
          • Audience: Technical users who need quick, clear information
          • Organization: Use simple categories:
              - Added - New functionality added
              - Changed - Existing functionality that was changed/updated
              - Fixed - Bugs or issues that were fixed
              - Other - Everything else worth noting
          • Style:
              - Use short, direct sentences
              - Avoid marketing language or elaborate descriptions
              - Focus on what changed, not how it was implemented
              - Use plain language without emoji or elaborate formatting
          • Format:
              - Keep it simple with basic markdown headings
              - Group similar changes together
              - Favor brevity and clarity over comprehensiveness
              - Use dashes for list items

        Be concise and to-the-point. Prioritize clear communication over exhaustive detail.
        """)
    
    def get_user_prompt(self, context: Dict[str, Any]) -> str:
        """Get user prompt with context."""
        # Extract repository information
        repo_name = context.get("repository", {}).get("name", "Project")
        
        # Get release cycle preference
        release_cycle = context.get("release_cycle", "auto")
        
        # Get commit information
        commit_count = context.get("analysis", {}).get("total_commits", 0)
        commit_lines = [f"* {c}" for c in context.get("commit_lines", [])]
        commits_text = "\n".join(commit_lines)
        
        # Build the prompt
        prompt = textwrap.dedent(f"""
        # Repository: {repo_name}
        # Release cycle: {release_cycle}
        
        Here are the last {commit_count} commits (newest first):
        {commits_text}
        
        Please generate a minimal, clean changelog that groups changes into simple categories.
        Focus on clarity and brevity. Use minimal formatting.
        
        Important: For time-based organization of the changelog entries:
        - Use release cycle: "{release_cycle}"
        - If "auto": Intelligently determine if entries should be grouped by day, week, or all together
        - If "daily": Group entries by day with clear date headers
        - If "weekly": Group entries by week with clear week headers
        - If "monthly": Group entries by month with clear month headers
        - If "none": Do not use time-based grouping, focus only on categorizing by type
        """)
        
        return prompt


class DetailedPrompt(PromptTemplate):
    """Highly detailed prompt with extensive context."""
    
    name = "detailed"
    description = "Comprehensive changelog with rich context and analysis"
    
    def get_system_prompt(self) -> str:
        """Get system prompt."""
        return textwrap.dedent("""
        You are ReleaseBot, a sophisticated changelog expert specializing in comprehensive, context-rich release notes. Create an in-depth, well-structured changelog that provides both technical and business context.

        Guidelines:
          • Audience: Both technical users and product stakeholders
          • Organization: Use a hierarchical structure:
              - 🚀 **Major Features** - Significant new functionality (detail sub-features)
              - ✨ **Enhancements** - Improvements to existing features
              - 🐛 **Bug Fixes** - Issues that were resolved
              - 📚 **Documentation** - Documentation improvements
              - 🧰 **Development** - Technical improvements, refactoring, testing
              - 🔒 **Security** - Security fixes and improvements
              - 🔄 **Dependencies** - Updated libraries and dependencies
          • Style:
              - Start with an executive summary of key changes
              - Include both technical implementation and user impact
              - Use nested bullet points to show relationships between changes
              - Highlight breaking changes prominently
              - Include metrics where possible (e.g., "30% faster load times")
          • Format:
              - Use rich markdown formatting with clear hierarchy
              - Include a table of contents for longer changelogs
              - Group related changes under sub-headings
              - Include code examples for significant API changes
              - Add references to documentation, if available

        Create a comprehensive changelog that serves both as documentation and communication tool. Focus on context and impact while maintaining technical accuracy.
        """)
    
    def get_user_prompt(self, context: Dict[str, Any]) -> str:
        """Get user prompt with context including rich analysis."""
        # Extract repository information
        repo_name = context.get("repository", {}).get("name", "Project")
        
        # Get detailed analysis
        analysis = context.get("analysis", {})
        category_dist = analysis.get("category_distribution", {})
        category_text = "\n".join([f"- {k}: {v} commit(s)" for k, v in category_dist.items()])
        
        # Get release cycle preference
        release_cycle = context.get("release_cycle", "auto")
        
        # Get commit information
        commit_count = analysis.get("total_commits", 0)
        commit_lines = [f"* {c}" for c in context.get("commit_lines", [])]
        commits_text = "\n".join(commit_lines)
        
        # Build the prompt
        prompt = textwrap.dedent(f"""
        # Repository: {repo_name}
        
        ## Analysis Summary
        - Total commits: {commit_count}
        - Estimated version change: {analysis.get("estimated_scope", "Unknown")}
        - Date range: {analysis.get("date_range", ["Unknown", "Unknown"])[0]} to {analysis.get("date_range", ["Unknown", "Unknown"])[1]}
        - Release cycle: {release_cycle}
        
        ## Category Distribution
        {category_text}
        
        ## Special Notes
        - Contains dependency updates: {"Yes" if analysis.get("has_dependency_updates") else "No"}
        - Contains large changes: {"Yes" if analysis.get("has_large_changes") else "No"}
        
        ## Commits
        {commits_text}
        
        Please generate a comprehensive, detailed changelog that includes:
        1. An executive summary of key changes
        2. Detailed grouping of changes by category
        3. Special attention to breaking changes, if any
        4. Context about the impact of changes where possible
        
        Use rich markdown formatting and hierarchical structure.
        
        Important: For time-based organization of the changelog entries:
        - Use release cycle: "{release_cycle}"
        - If "auto": Intelligently determine if entries should be grouped by day, week, or all together
        - If "daily": Group entries by day with clear date headers
        - If "weekly": Group entries by week with clear week headers
        - If "monthly": Group entries by month with clear month headers
        - If "none": Do not use time-based grouping, focus only on categorizing by type
        """)
        
        return prompt


def get_prompt_template(name: str = "standard") -> PromptTemplate:
    """Get a prompt template by name."""
    templates = {
        "standard": StandardPrompt(),
        "conventional": ConventionalPrompt(),
        "minimal": MinimalPrompt(),
        "detailed": DetailedPrompt(),
    }
    
    return templates.get(name, StandardPrompt())