# Mintlify Changelog Generator 🚀

Generate beautiful, AI-powered changelogs directly from your git commits.

[![PyPI version](https://img.shields.io/pypi/v/mintlify-changelog.svg)](https://pypi.org/project/mintlify-changelog/)
[![Python Versions](https://img.shields.io/pypi/pyversions/mintlify-changelog.svg)](https://pypi.org/project/mintlify-changelog/)
[![License](https://img.shields.io/pypi/l/mintlify-changelog.svg)](https://github.com/mintlify/changelog/blob/main/LICENSE)

## Features

✨ **Smart Grouping** - Intelligently groups related changes under clear categories  
🔄 **Enhanced Context** - Uses repository data to provide richer context  
🐛 **Emoji Categories** - Visually appealing headings with emoji indicators  
📚 **Multiple Output Formats** - Export as Markdown, HTML, JSON, or plain text  
🧠 **AI-Powered** - Leverages Claude AI for natural language understanding  
🎨 **Theme Support** - Choose from different styles to match your preferences  
🔄 **Semantic Version Detection** - Automatically suggests version bumps  
🌐 **Zero Config** - Works immediately without complex setup  

## Installation

```bash
pip install mintlify-changelog
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/mintlify/changelog.git
```

## Quick Start

1. Navigate to any git repository
2. Set your API key (one-time setup):
   ```bash
   mintlify-changelog --set-api-key "your-api-key"
   ```
3. Generate a changelog:
   ```bash
   mintlify-changelog
   ```

## Usage

```
mintlify-changelog [options]
```

### Basic Options

- `-c, --count N` - Generate changelog for the last N commits (default: 20)
- `-o, --output FILE` - Save changelog to a file (e.g., CHANGELOG.md)
- `--title TITLE` - Custom title for the changelog
- `--dry-run` - Preview the prompt without calling the API
- `-q, --quiet` - Suppress progress output
- `-h, --help` - Show help message
- `--version` - Show version information

### Format Options

- `--format FORMAT` - Output format (markdown, html, json, text)
- `--theme THEME` - Theme style (standard, conventional, minimal, detailed)
- `--list-themes` - See available themes with descriptions

### Configuration

- `--set-api-key KEY` - Set your Claude API key securely
- `--set-config KEY=VALUE` - Set a configuration value (e.g., defaults.count=30)

### Examples

Generate for last 10 commits:
```bash
mintlify-changelog -c 10
```

Save to a file:
```bash
mintlify-changelog -o CHANGELOG.md
```

Generate HTML changelog:
```bash
mintlify-changelog --format html -o changelog.html
```

Use Conventional Commits style:
```bash
mintlify-changelog --theme conventional
```

## Example Output

```markdown
# My Project Changelog
### April 23, 2025

#### ✨ New Features
- Add user authentication system with OAuth support
- Implement dark mode across all components
- Add real-time notification system

#### 🐛 Bug Fixes
- Fix critical race condition in async data loading
- Address security vulnerability in input validation
- Resolve file upload issues on Safari browsers

#### 📚 Documentation
- Add comprehensive API documentation
- Create user onboarding guide with screenshots

---

This release introduces major new features including authentication, dark mode, and real-time notifications while addressing several critical bugs and improving documentation.
```

## Environment Variables

- `MINTLIFY_API_KEY` - Your Claude API key
- `MINTLIFY_BASE_URL` - API base URL
- `MINTLIFY_API_ENDPOINT` - API endpoint path
- `MINTLIFY_MODEL` - Claude model to use
- `MINTLIFY_MAX_TOKENS` - Maximum tokens for API response
- `MINTLIFY_TEMPERATURE` - Temperature setting for API

## Developing

Clone the repository and install in development mode:

```bash
git clone https://github.com/mintlify/changelog.git
cd changelog
pip install -e .
```

## License

MIT