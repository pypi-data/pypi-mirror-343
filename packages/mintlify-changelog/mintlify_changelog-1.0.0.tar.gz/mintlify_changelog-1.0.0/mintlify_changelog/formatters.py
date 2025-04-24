#!/usr/bin/env python3
"""
Output formatters for different changelog formats.

Supports multiple output formats including:
- Markdown (default)
- HTML
- JSON
- Plain text
"""
import json
from typing import Dict, Any
import xml.etree.ElementTree as ET
from datetime import datetime


class ChangelogFormatter:
    """Base formatter class for changelogs."""
    
    def __init__(self, repo_name: str = ""):
        self.repo_name = repo_name
        
    def format(self, changelog: str) -> str:
        """Format the changelog output."""
        raise NotImplementedError("Formatters must implement format()")


class MarkdownFormatter(ChangelogFormatter):
    """Format changelog as Markdown."""
    
    def format(self, changelog: str) -> str:
        """Return markdown as-is."""
        return changelog


class HTMLFormatter(ChangelogFormatter):
    """Format changelog as HTML."""
    
    def format(self, changelog: str) -> str:
        """Convert markdown to HTML."""
        from markdown import markdown
        title = f"<h1>{self.repo_name} Changelog</h1>"
        timestamp = f"<p class='timestamp'>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>"
        body = markdown(changelog, extensions=["tables", "fenced_code"])
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.repo_name} Changelog</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }}
        h1, h2, h3, h4 {{
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            font-weight: 600;
        }}
        h1 {{ 
            font-size: 2.2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        h2 {{ font-size: 1.8em; }}
        h3 {{ font-size: 1.5em; }}
        h4 {{ font-size: 1.25em; }}
        p, ul, ol {{ margin-bottom: 1em; }}
        code {{
            background-color: rgba(27,31,35,.05);
            border-radius: 3px;
            font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
            font-size: 85%;
            padding: 0.2em 0.4em;
        }}
        hr {{ 
            height: 0.25em;
            border: 0;
            background-color: #e1e4e8;
            margin: 2rem 0;
        }}
        .timestamp {{
            color: #6a737d;
            font-style: italic;
        }}
    </style>
</head>
<body>
    {title}
    {timestamp}
    {body}
</body>
</html>
"""
        return html


class JSONFormatter(ChangelogFormatter):
    """Format changelog as JSON."""
    
    def format(self, changelog: str) -> str:
        """Convert markdown to structured JSON."""
        sections = self._parse_sections(changelog)
        result = {
            "title": f"{self.repo_name} Changelog",
            "generated_at": datetime.now().isoformat(),
            "sections": sections
        }
        return json.dumps(result, indent=2)
    
    def _parse_sections(self, changelog: str) -> Dict[str, Any]:
        """Parse the changelog into structured sections."""
        import re
        
        # Extract main title
        title = ""
        title_match = re.search(r'^#\s+(.+)$', changelog, re.MULTILINE)
        if title_match:
            title = title_match.group(1)
        
        # Extract date
        date = ""
        date_match = re.search(r'^###\s+(.+)$', changelog, re.MULTILINE)
        if date_match:
            date = date_match.group(1)
        
        # Extract sections
        section_pattern = r'(#{3,4}\s+.*?(?:New Features|Features|Changes|Improvements|Bug Fixes|Fixed|Documentation|Security|Other).*?)(?=#{3,4}|\Z)'
        sections = {}
        
        for section_match in re.finditer(section_pattern, changelog, re.DOTALL):
            section_text = section_match.group(1).strip()
            
            # Get section name
            section_name_match = re.search(r'^#{3,4}\s+(.*?)$', section_text, re.MULTILINE)
            if not section_name_match:
                continue
                
            section_name = section_name_match.group(1).strip()
            
            # Extract items
            items = []
            section_content = section_text.split('\n', 1)[1] if '\n' in section_text else ""
            
            for line in section_content.strip().split('\n'):
                if line.strip().startswith('-'):
                    items.append(line.strip()[1:].strip())
            
            sections[section_name] = items
            
        return {
            "title": title,
            "date": date,
            "categories": sections
        }


class PlainTextFormatter(ChangelogFormatter):
    """Format changelog as plain text."""
    
    def format(self, changelog: str) -> str:
        """Convert markdown to plain text."""
        import re
        
        # Replace headings
        text = re.sub(r'^#+\s+(.+)$', r'\1', changelog, flags=re.MULTILINE)
        
        # Replace bold and italic
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
        text = re.sub(r'_(.+?)_', r'\1', text)
        
        # Replace emoji markers (optional)
        text = re.sub(r'[🐛✨🔄📚🛠️🔒]', '', text)
        
        # Add proper spacing
        text = f"{self.repo_name.upper()} CHANGELOG\n{'=' * 50}\n\n{text}"
        
        return text


def get_formatter(format_type: str, repo_name: str = "") -> ChangelogFormatter:
    """Factory function to get the appropriate formatter."""
    format_map = {
        "markdown": MarkdownFormatter,
        "html": HTMLFormatter,
        "json": JSONFormatter,
        "text": PlainTextFormatter,
    }
    
    formatter_class = format_map.get(format_type.lower(), MarkdownFormatter)
    return formatter_class(repo_name)