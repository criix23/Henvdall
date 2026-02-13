"""Tests for parser module."""

import tempfile
from pathlib import Path

import pytest

from henvdall.parser import EnvFileParser


class TestEnvFileParser:
    """Tests for EnvFileParser class."""

    def test_parse_simple_file(self):
        """Test parsing a simple .env file."""
        content = """
DATABASE_URL=postgresql://localhost/db
API_KEY=secret123
PORT=3000
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            entries = EnvFileParser.parse_file(temp_path)

            assert len(entries) == 3
            assert "DATABASE_URL" in entries
            assert entries["DATABASE_URL"].value == "postgresql://localhost/db"
            assert entries["API_KEY"].value == "secret123"
            assert entries["PORT"].value == "3000"
        finally:
            temp_path.unlink()

    def test_parse_with_comments(self):
        """Test parsing .env file with comments."""
        content = """
# This is a comment
DATABASE_URL=postgresql://localhost/db
API_KEY=secret123  # (url)
PORT=3000  # (int)
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            entries = EnvFileParser.parse_file(temp_path)

            assert len(entries) == 3
            assert entries["API_KEY"].comment == "(url)"
            assert entries["PORT"].comment == "(int)"
        finally:
            temp_path.unlink()

    def test_parse_quoted_values(self):
        """Test parsing values with quotes."""
        content = """
SINGLE_QUOTED='value with spaces'
DOUBLE_QUOTED="another value"
NO_QUOTES=simple
"""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            f.write(content)
            temp_path = Path(f.name)

        try:
            entries = EnvFileParser.parse_file(temp_path)

            assert entries["SINGLE_QUOTED"].value == "value with spaces"
            assert entries["DOUBLE_QUOTED"].value == "another value"
            assert entries["NO_QUOTES"].value == "simple"
        finally:
            temp_path.unlink()

    def test_parse_empty_file(self):
        """Test parsing an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.env') as f:
            temp_path = Path(f.name)

        try:
            entries = EnvFileParser.parse_file(temp_path)
            assert len(entries) == 0
        finally:
            temp_path.unlink()

    def test_parse_nonexistent_file(self):
        """Test parsing a file that doesn't exist."""
        entries = EnvFileParser.parse_file(Path("/nonexistent/file.env"))
        assert len(entries) == 0

    def test_format_entry_simple(self):
        """Test formatting a simple entry."""
        result = EnvFileParser.format_entry("KEY", "value")
        assert result == "KEY=value"

    def test_format_entry_with_spaces(self):
        """Test formatting an entry with spaces."""
        result = EnvFileParser.format_entry("KEY", "value with spaces")
        assert result == 'KEY="value with spaces"'

    def test_format_entry_with_special_chars(self):
        """Test formatting an entry with special characters."""
        result = EnvFileParser.format_entry("KEY", "value#with#hash")
        assert result == 'KEY="value#with#hash"'
