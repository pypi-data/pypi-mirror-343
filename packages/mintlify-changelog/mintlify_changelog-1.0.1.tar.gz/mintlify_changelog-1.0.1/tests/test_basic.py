#!/usr/bin/env python3
"""
Basic tests for the mintlify-changelog package.
"""
import os
import sys
import tempfile
import unittest
from unittest.mock import patch, MagicMock

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from mintlify_changelog.config import DEFAULT_CONFIG, _merge_config
from mintlify_changelog.formatters import get_formatter, MarkdownFormatter, HTMLFormatter
from mintlify_changelog.prompts import get_prompt_template


class TestConfig(unittest.TestCase):
    """Test configuration handling."""
    
    def test_merge_config(self):
        """Test config merging."""
        default = {"a": 1, "b": {"c": 2, "d": 3}}
        user = {"b": {"c": 4}, "e": 5}
        expected = {"a": 1, "b": {"c": 4, "d": 3}, "e": 5}
        
        result = _merge_config(default, user)
        self.assertEqual(result, expected)
    
    def test_default_config(self):
        """Test default config structure."""
        # Just validate that the default config has the expected sections
        sections = ["api", "defaults", "templates"]
        for section in sections:
            self.assertIn(section, DEFAULT_CONFIG)


class TestFormatters(unittest.TestCase):
    """Test output formatters."""
    
    def test_get_formatter(self):
        """Test formatter factory function."""
        markdown_formatter = get_formatter("markdown")
        self.assertIsInstance(markdown_formatter, MarkdownFormatter)
        
        html_formatter = get_formatter("html")
        self.assertIsInstance(html_formatter, HTMLFormatter)
        
        # Test fallback
        default_formatter = get_formatter("invalid")
        self.assertIsInstance(default_formatter, MarkdownFormatter)
    
    def test_markdown_formatter(self):
        """Test markdown formatter."""
        formatter = MarkdownFormatter()
        input_md = "# Test\n\nThis is a test."
        output = formatter.format(input_md)
        
        # Markdown formatter should return input as-is
        self.assertEqual(output, input_md)
    
    def test_html_formatter(self):
        """Test HTML formatter."""
        formatter = HTMLFormatter("Test Repo")
        input_md = "# Test\n\nThis is a test."
        output = formatter.format(input_md)
        
        # HTML formatter should convert to HTML
        self.assertIn("<html", output)
        self.assertIn("<h1>Test</h1>", output)
        self.assertIn("<p>This is a test.</p>", output)


class TestPrompts(unittest.TestCase):
    """Test prompt templates."""
    
    def test_get_prompt_template(self):
        """Test getting prompt templates."""
        # Test valid templates
        standard = get_prompt_template("standard")
        self.assertEqual(standard.name, "standard")
        
        conventional = get_prompt_template("conventional")
        self.assertEqual(conventional.name, "conventional")
        
        minimal = get_prompt_template("minimal")
        self.assertEqual(minimal.name, "minimal")
        
        detailed = get_prompt_template("detailed")
        self.assertEqual(detailed.name, "detailed")
        
        # Test fallback
        default = get_prompt_template("invalid")
        self.assertEqual(default.name, "standard")
    
    def test_prompt_content(self):
        """Test prompt generation with context."""
        template = get_prompt_template("standard")
        
        # Test with minimal context
        context = {
            "repository": {"name": "test-repo", "branch": "main"},
            "commit_lines": ["line1", "line2"],
            "analysis": {"total_commits": 2}
        }
        
        user_prompt = template.get_user_prompt(context)
        system_prompt = template.get_system_prompt()
        
        # Check that context variables are included
        self.assertIn("test-repo", user_prompt)
        self.assertIn("main", user_prompt)
        self.assertIn("line1", user_prompt)
        self.assertIn("line2", user_prompt)
        
        # Check system prompt has instructions
        self.assertIn("ReleaseBot", system_prompt)
        self.assertIn("Guidelines", system_prompt)


if __name__ == '__main__':
    unittest.main()