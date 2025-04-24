#!/usr/bin/env python3
"""
Command-line interface for the Mintlify Changelog Generator.
"""
import argparse
import sys
import textwrap

from mintlify_changelog.core import (
    DEFAULT_COUNT,
    generate_changelog,
    print_welcome
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
          %(prog)s --dry-run                 # Preview only
          
        Documentation and updates:
          https://github.com/mintlify/changelog
        """)
    )
    parser.add_argument("-c", "--count", type=int, default=DEFAULT_COUNT, 
                        help=f"Number of commits to summarize (default: {DEFAULT_COUNT})")
    parser.add_argument("--dry-run", action="store_true", 
                        help="Print prompt without calling the API")
    parser.add_argument("-o", "--output", 
                        help="Save changelog to this file (e.g., CHANGELOG.md)")
    parser.add_argument("--title", default="", 
                        help="Custom title for the changelog")
    parser.add_argument("--version", action="version", 
                        version=f"mintlify-changelog {__version__}")
    parser.add_argument("--set-api-key", 
                        help="Set your Claude API key")
    
    # Show welcome message if no args provided
    if len(sys.argv) == 1:
        print_welcome()
        return
        
    args = parser.parse_args()
    
    # Handle API key setting
    if args.set_api_key:
        try:
            import os
            home = os.path.expanduser("~")
            config_dir = os.path.join(home, ".config", "mintlify")
            os.makedirs(config_dir, exist_ok=True)
            with open(os.path.join(config_dir, "api_key"), "w") as f:
                f.write(args.set_api_key)
            print("✅ API key saved successfully")
            return
        except Exception as e:
            sys.exit(f"❌ Error saving API key: {e}")

    try:
        title = args.title if args.title else "📋 CHANGELOG"
        generate_changelog(
            count=args.count,
            dry_run=args.dry_run,
            output_file=args.output,
            title=title
        )
    except Exception as e:
        sys.exit(f"Error: {e}")

if __name__ == "__main__":
    main()