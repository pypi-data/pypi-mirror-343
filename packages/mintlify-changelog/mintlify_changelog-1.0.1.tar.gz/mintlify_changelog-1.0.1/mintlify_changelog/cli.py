#!/usr/bin/env python3
"""
Command-line interface for the Mintlify Changelog Generator.
"""
import argparse
import sys
import textwrap
import os
from typing import List, Dict, Any, Optional

from mintlify_changelog.core import (
    generate_changelog,
    print_welcome
)
from mintlify_changelog.config import (
    set_api_key,
    get_default_count,
    update_config_value
)
from mintlify_changelog import __version__


def main() -> None:
    """Entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Generate a markdown changelog for git commits using Claude AI.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""
        Examples:
          %(prog)s                           # Use default settings
          %(prog)s -c 15                     # Last 15 commits
          %(prog)s -o CHANGELOG.md           # Save to file
          %(prog)s --title "Release v1.0.0"  # Custom title
          %(prog)s --theme conventional      # Use conventional commits style
          %(prog)s --format html             # Generate HTML output
          %(prog)s --dry-run                 # Preview only
          
        Configuration:
          Configure with environment variables or ~/.config/mintlify/config.json
          
        Documentation:
          https://github.com/mintlify/changelog
        """)
    )
    
    # Basic options
    parser.add_argument("-c", "--count", type=int, 
                        help=f"Number of commits to summarize (default: {get_default_count()})")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Print prompt without calling the API")
    parser.add_argument("-o", "--output", metavar="FILE",
                        help="Save changelog to this file (e.g., CHANGELOG.md)")
    parser.add_argument("--title", default="", 
                        help="Custom title for the changelog")
    
    # Advanced options
    format_group = parser.add_argument_group("Format Options")
    format_group.add_argument("--format", choices=["markdown", "html", "enhanced-html", "json", "text"], default="markdown",
                         help="Output format (default: markdown)")
    format_group.add_argument("--theme", choices=["standard", "conventional", "minimal", "detailed"], default="standard",
                         help="Theme style for changelog (default: standard)")
    
    # Config management
    config_group = parser.add_argument_group("Configuration Options")
    config_group.add_argument("--set-api-key", metavar="KEY",
                       help="Set your Claude API key")
    config_group.add_argument("--set-config", metavar="KEY=VALUE",
                       help="Set a configuration value (e.g. defaults.count=30)")
    config_group.add_argument("--list-themes", action="store_true",
                       help="List available changelog themes")
    
    # Miscellaneous
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress progress output")
    parser.add_argument("--version", action="version", 
                        version=f"mintlify-changelog {__version__}")
    parser.add_argument("--single-file-cli", metavar="FILE",
                        help="Generate a standalone single-file CLI script")
    
    # Show welcome message if no args provided
    if len(sys.argv) == 1:
        print_welcome()
        return
        
    args = parser.parse_args()
    
    # Handle listing themes
    if args.list_themes:
        _list_themes()
        return
    
    # Handle single-file CLI generation
    if args.single_file_cli:
        try:
            _generate_single_file_cli(args.single_file_cli)
            print(f"✅ Single-file CLI generated at {args.single_file_cli}")
            return
        except Exception as e:
            sys.exit(f"❌ Error generating single-file CLI: {e}")
    
    # Handle API key setting
    if args.set_api_key:
        try:
            set_api_key(args.set_api_key)
            print("✅ API key saved successfully")
            return
        except Exception as e:
            sys.exit(f"❌ Error saving API key: {e}")
    
    # Handle config updates
    if args.set_config:
        try:
            key, value = args.set_config.split('=', 1)
            # Convert value to appropriate type
            if value.lower() in ['true', 'yes', 'y']:
                value = True
            elif value.lower() in ['false', 'no', 'n']:
                value = False
            elif value.isdigit():
                value = int(value)
            elif value.replace('.', '', 1).isdigit() and value.count('.') == 1:
                value = float(value)
                
            update_config_value(key, value)
            print(f"✅ Configuration updated: {key} = {value}")
            return
        except Exception as e:
            sys.exit(f"❌ Error updating configuration: {e}")

    # Generate the changelog
    try:
        title = args.title if args.title else "📋 CHANGELOG"
        generate_changelog(
            count=args.count,
            dry_run=args.dry_run,
            output_file=args.output,
            title=title,
            theme=args.theme,
            output_format=args.format,
            show_progress=not args.quiet
        )
    except Exception as e:
        sys.exit(f"Error: {e}")


def _list_themes() -> None:
    """List available themes with descriptions."""
    from mintlify_changelog.prompts import get_prompt_template
    
    themes = [
        ("standard", "Detailed, professional changelog with rich formatting"),
        ("conventional", "Follows Conventional Commits standard with semantic versioning"),
        ("minimal", "Concise, clean changelog with minimal formatting"),
        ("detailed", "Comprehensive changelog with rich context and analysis")
    ]
    
    print("\n📋 Available Changelog Themes\n")
    
    for name, description in themes:
        print(f"  • {name:12} - {description}")
        
    print("\nSet a theme with --theme <n>, for example: --theme conventional")


def _generate_single_file_cli(output_path: str) -> None:
    """Generate a standalone single-file CLI script.
    
    Args:
        output_path: Path where the single-file CLI will be saved
    """
    import os
    import shutil
    from pathlib import Path
    from mintlify_changelog import __version__
    
    # Source file is cli_complete_suite.py in the project root
    template_path = Path(__file__).parents[1] / "cli_complete_suite.py"
    
    if not template_path.exists():
        template_path = Path(__file__).parents[1] / "mintlify-changelog"
        if not template_path.exists():
            raise FileNotFoundError(f"Template file not found at {template_path}")
    
    # Simply copy the file and update the version
    shutil.copy2(template_path, output_path)
    
    # Update version
    with open(output_path, 'r') as f:
        content = f.read()
    
    # Rename the output file to the requested name
    output_name = Path(output_path).name
    content = content.replace('#!/usr/bin/env python3', 
                     f'#!/usr/bin/env python3\n# {output_name} - Generated by mintlify-changelog v{__version__}')
    
    content = content.replace('version="%(prog)s 1.0.0"', 
                     f'version="%(prog)s {__version__}"')
    
    # Write to the output file
    with open(output_path, 'w') as f:
        f.write(content)
    
    # Make the output file executable
    try:
        os.chmod(output_path, 0o755)
    except Exception:
        print(f"Warning: Could not make file executable. You may need to run: chmod +x {output_path}")


if __name__ == "__main__":
    main()