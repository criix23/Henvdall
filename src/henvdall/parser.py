"""Parser for .env and .env.example files."""

import re
from pathlib import Path
from typing import Dict, Optional, Tuple


class EnvEntry:
    """Represents a single environment variable entry."""

    def __init__(self, key: str, value: str, comment: Optional[str] = None):
        self.key = key
        self.value = value
        self.comment = comment

    def __repr__(self):
        return f"EnvEntry(key={self.key}, value={self.value}, comment={self.comment})"


class EnvFileParser:
    """Parser for .env files."""

    ENV_LINE_PATTERN = re.compile(
        r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*([^#]*?)(?:\s*#\s*(.*))?$'
    )

    @classmethod
    def parse_file(cls, file_path: Path) -> Dict[str, EnvEntry]:
        """Parse an .env file and return a dictionary of entries."""
        if not file_path.exists():
            return {}

        entries = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.rstrip('\n')

                if not line.strip() or line.strip().startswith('#'):
                    continue

                match = cls.ENV_LINE_PATTERN.match(line)
                if match:
                    key = match.group(1)
                    value = match.group(2).strip()
                    comment = match.group(3).strip() if match.group(3) else None

                    value = cls._unquote_value(value)

                    entries[key] = EnvEntry(key=key, value=value, comment=comment)

        return entries

    @staticmethod
    def _unquote_value(value: str) -> str:
        """Remove surrounding quotes from a value if present."""
        if len(value) >= 2:
            if (value[0] == '"' and value[-1] == '"') or (value[0] == "'" and value[-1] == "'"):
                return value[1:-1]
        return value

    @staticmethod
    def format_entry(key: str, value: str) -> str:
        """Format a key-value pair for writing to .env file."""
        if ' ' in value or any(char in value for char in ['#', '$', '\\']):
            value = f'"{value}"'
        return f"{key}={value}"
