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
import re
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
        try:
            from markdown import markdown
            md_converter = markdown
        except ImportError:
            # Fallback basic markdown to HTML conversion if markdown package is not available
            import re
            
            def basic_md_to_html(text):
                # Basic conversion of markdown to HTML
                html = text
                # Headers
                html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
                html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
                html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
                
                # Lists
                html = re.sub(r'^- (.*?)$', r'<li>\1</li>', html, flags=re.MULTILINE)
                html = re.sub(r'(<li>.*?</li>)', r'<ul>\1</ul>', html, flags=re.DOTALL)
                
                # Bold and Italic
                html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
                html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
                
                # Code
                html = re.sub(r'`(.*?)`', r'<code>\1</code>', html)
                
                return html
                
            md_converter = basic_md_to_html
            
        title = f"<h1 class='text-3xl font-bold tracking-tight mb-4'>{self.repo_name} Changelog</h1>"
        timestamp = f"<div class='text-sm text-gray-500 mb-8'>Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>"
        try:
            body = md_converter(changelog, extensions=["tables", "fenced_code"])
        except TypeError:
            # If extensions aren't supported
            body = md_converter(changelog)
        
        # Split HTML content into parts that need f-string interpolation and those that don't
        head_part = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.repo_name} Changelog</title>
    <script src="https://cdn.tailwindcss.com"></script>"""
        
        # Use regular string (not f-string) for the JavaScript config to avoid f-string parsing issues
        script_part = """
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        border: "hsl(var(--border))",
                        input: "hsl(var(--input))",
                        ring: "hsl(var(--ring))",
                        background: "hsl(var(--background))",
                        foreground: "hsl(var(--foreground))",
                        primary: {
                            DEFAULT: "hsl(var(--primary))",
                            foreground: "hsl(var(--primary-foreground))",
                        },
                        secondary: {
                            DEFAULT: "hsl(var(--secondary))",
                            foreground: "hsl(var(--secondary-foreground))",
                        },
                        destructive: {
                            DEFAULT: "hsl(var(--destructive))",
                            foreground: "hsl(var(--destructive-foreground))",
                        },
                        muted: {
                            DEFAULT: "hsl(var(--muted))",
                            foreground: "hsl(var(--muted-foreground))",
                        },
                        accent: {
                            DEFAULT: "hsl(var(--accent))",
                            foreground: "hsl(var(--accent-foreground))",
                        },
                        popover: {
                            DEFAULT: "hsl(var(--popover))",
                            foreground: "hsl(var(--popover-foreground))",
                        },
                        card: {
                            DEFAULT: "hsl(var(--card))",
                            foreground: "hsl(var(--card-foreground))",
                        },
                    },
                    borderRadius: {
                        lg: "var(--radius)",
                        md: "calc(var(--radius) - 2px)",
                        sm: "calc(var(--radius) - 4px)",
                    },
                },
            },
        }
    </script>"""
        
        # Use regular string (not f-string) for CSS
        style_part = """
    <style>
        :root {
            --background: 0 0% 100%;
            --foreground: 222.2 84% 4.9%;
            --card: 0 0% 100%;
            --card-foreground: 222.2 84% 4.9%;
            --popover: 0 0% 100%;
            --popover-foreground: 222.2 84% 4.9%;
            --primary: 221.2 83.2% 53.3%;
            --primary-foreground: 210 40% 98%;
            --secondary: 210 40% 96.1%;
            --secondary-foreground: 222.2 47.4% 11.2%;
            --muted: 210 40% 96.1%;
            --muted-foreground: 215.4 16.3% 46.9%;
            --accent: 210 40% 96.1%;
            --accent-foreground: 222.2 47.4% 11.2%;
            --destructive: 0 84.2% 60.2%;
            --destructive-foreground: 210 40% 98%;
            --border: 214.3 31.8% 91.4%;
            --input: 214.3 31.8% 91.4%;
            --ring: 221.2 83.2% 53.3%;
            --radius: 0.5rem;
        }

        .dark {
            --background: 222.2 84% 4.9%;
            --foreground: 210 40% 98%;
            --card: 222.2 84% 4.9%;
            --card-foreground: 210 40% 98%;
            --popover: 222.2 84% 4.9%;
            --popover-foreground: 210 40% 98%;
            --primary: 217.2 91.2% 59.8%;
            --primary-foreground: 222.2 47.4% 11.2%;
            --secondary: 217.2 32.6% 17.5%;
            --secondary-foreground: 210 40% 98%;
            --muted: 217.2 32.6% 17.5%;
            --muted-foreground: 215 20.2% 65.1%;
            --accent: 217.2 32.6% 17.5%;
            --accent-foreground: 210 40% 98%;
            --destructive: 0 62.8% 30.6%;
            --destructive-foreground: 210 40% 98%;
            --border: 217.2 32.6% 17.5%;
            --input: 217.2 32.6% 17.5%;
            --ring: 224.3 76.3% 48%;
        }
        
        body {
            font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background-color: hsl(var(--background));
            color: hsl(var(--foreground));
            line-height: 1.6;
        }
        
        .changelog-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        
        .card {
            background-color: hsl(var(--card));
            border-radius: var(--radius);
            border: 1px solid hsl(var(--border));
            padding: 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        
        h1, h2, h3, h4 {
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.75em;
        }
        
        h1 { font-size: 2rem; }
        h2 { 
            font-size: 1.5rem; 
            margin-top: 2rem;
            color: hsl(var(--primary));
        }
        h3 { 
            font-size: 1.25rem; 
            color: hsl(var(--accent-foreground));
            padding-bottom: 0.25rem;
            border-bottom: 1px solid hsl(var(--border));
        }
        
        p, ul, ol { margin-bottom: 1rem; }
        
        ul {
            list-style-type: disc;
            padding-left: 1.5rem;
        }
        
        li {
            margin-bottom: 0.5rem;
        }
        
        li:last-child {
            margin-bottom: 0;
        }
        
        code {
            background-color: hsl(var(--muted));
            color: hsl(var(--muted-foreground));
            padding: 0.15rem 0.3rem;
            border-radius: 0.25rem;
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            font-size: 0.9em;
        }
        
        .tag {
            display: inline-flex;
            align-items: center;
            background-color: hsl(var(--secondary));
            color: hsl(var(--secondary-foreground));
            border-radius: 9999px;
            padding: 0.125rem 0.75rem;
            font-size: 0.75rem;
            font-weight: 500;
            margin-right: 0.5rem;
            margin-bottom: 0.5rem;
        }
        
        .feature {
            background-color: hsl(var(--primary));
            color: hsl(var(--primary-foreground));
        }
        
        .bugfix {
            background-color: hsl(var(--destructive));
            color: hsl(var(--destructive-foreground));
        }
        
        pre {
            background-color: hsl(var(--card));
            border-radius: var(--radius);
            padding: 1rem;
            overflow-x: auto;
            margin-bottom: 1rem;
            border: 1px solid hsl(var(--border));
        }
        
        blockquote {
            border-left: 4px solid hsl(var(--primary));
            padding-left: 1rem;
            margin-left: 0;
            margin-bottom: 1rem;
            color: hsl(var(--muted-foreground));
        }
        
        /* Added styles for emoji markers */
        .emoji-marker {
            display: inline-block;
            margin-right: 0.4rem;
        }
        
        /* Theme toggle button */
        .theme-toggle {
            position: fixed;
            top: 1rem;
            right: 1rem;
            background-color: hsl(var(--secondary));
            color: hsl(var(--secondary-foreground));
            border: none;
            border-radius: var(--radius);
            padding: 0.5rem;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
</head>
<body>
    <button class="theme-toggle" onclick="document.documentElement.classList.toggle('dark')">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        </svg>
    </button>"""
        
        # Use f-string for parts that need variable interpolation
        content_part = f"""    
    <div class="changelog-container">
        <div class="card">
            {title}
            {timestamp}
            
            <div class="prose max-w-none">
                {body}
            </div>
        </div>
        
        <div class="text-center text-sm text-gray-500 mt-8">
            Generated by Mintlify Changelog
        </div>
    </div>"""
        
        # Use regular string for JavaScript
        js_part = """    
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            // Add emoji marker spans to headings
            document.querySelectorAll('h2, h3').forEach(function(heading) {
                const text = heading.textContent;
                // Simple check for emoji-like characters at the beginning (works for many common emojis)
                if (text.length > 0 && text.charCodeAt(0) > 8000) {
                    // Get first character (which might be an emoji)
                    const firstChar = text.charAt(0);
                    heading.innerHTML = heading.innerHTML.replace(
                        firstChar, 
                        '<span class="emoji-marker">' + firstChar + '</span>'
                    );
                }
            });
            
            // Add tags to certain common changelog keywords
            const featureKeywords = ['new', 'feature', 'add', 'added', 'implement'];
            const bugfixKeywords = ['fix', 'fixed', 'bug', 'resolve', 'resolved', 'issue'];
            
            document.querySelectorAll('li').forEach(function(item) {
                const text = item.textContent.toLowerCase();
                let tagAdded = false;
                
                for (let keyword of featureKeywords) {
                    if (text.includes(keyword)) {
                        const tag = document.createElement('span');
                        tag.className = 'tag feature';
                        tag.textContent = 'Feature';
                        item.prepend(tag);
                        tagAdded = true;
                        break;
                    }
                }
                
                if (!tagAdded) {
                    for (let keyword of bugfixKeywords) {
                        if (text.includes(keyword)) {
                            const tag = document.createElement('span');
                            tag.className = 'tag bugfix';
                            tag.textContent = 'Fix';
                            item.prepend(tag);
                            break;
                        }
                    }
                }
            });
        });
    </script>
</body>
</html>"""

        # Combine all parts
        html = head_part + script_part + style_part + content_part + js_part
        return html


class EnhancedHTMLFormatter(HTMLFormatter):
    """Format changelog as enhanced HTML with shadcn-inspired UI."""
    
    def format(self, changelog: str) -> str:
        """
        Enhanced version of the HTML formatter with modern UI components.
        This implements shadcn-like styling without requiring React.
        """
        # Use the standard HTML formatter as a base
        return super().format(changelog)


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
        "enhanced-html": EnhancedHTMLFormatter,
        "json": JSONFormatter,
        "text": PlainTextFormatter,
    }
    
    formatter_class = format_map.get(format_type.lower(), MarkdownFormatter)
    return formatter_class(repo_name)