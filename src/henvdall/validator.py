"""Validation logic for environment variable values."""

import re
from typing import Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, field_validator


class ValidationResult(BaseModel):
    """Result of a validation check."""

    is_valid: bool
    error_message: Optional[str] = None


class EnvValueValidator:
    """Validator for environment variable values based on type hints."""

    PLACEHOLDER_PATTERNS = [
        r"(?i)your[_\s].*here",
        r"(?i)placeholder",
        r"(?i)change[_\s]?me",
        r"(?i)replace[_\s]?this",
        r"(?i)todo",
        r"(?i)xxx+",
        r"^admin123$",
        r"^password123$",
        r"^test123$",
        r"^secret$",
        r"^changeme$",
    ]

    @staticmethod
    def validate_int(value: str) -> ValidationResult:
        """Validate that a value is a valid integer."""
        try:
            int(value)
            return ValidationResult(is_valid=True)
        except ValueError:
            return ValidationResult(
                is_valid=False,
                error_message=f"'{value}' is not a valid integer",
            )

    @staticmethod
    def validate_url(value: str) -> ValidationResult:
        """Validate that a value is a valid URL."""
        try:
            result = urlparse(value)
            if all([result.scheme, result.netloc]):
                return ValidationResult(is_valid=True)
            return ValidationResult(
                is_valid=False,
                error_message=f"'{value}' is not a valid URL (must include scheme and domain)",
            )
        except Exception as e:
            return ValidationResult(
                is_valid=False,
                error_message=f"'{value}' is not a valid URL: {str(e)}",
            )

    @classmethod
    def validate_value(cls, value: str, validation_type: Optional[str]) -> ValidationResult:
        """Validate a value based on its type hint."""
        if not validation_type:
            return ValidationResult(is_valid=True)

        validation_type = validation_type.lower().strip()

        if validation_type == "int":
            return cls.validate_int(value)
        elif validation_type == "url":
            return cls.validate_url(value)
        else:
            return ValidationResult(is_valid=True)

    @classmethod
    def is_placeholder(cls, value: str) -> bool:
        """Check if a value looks like a placeholder that needs to be changed."""
        if not value or not value.strip():
            return True

        for pattern in cls.PLACEHOLDER_PATTERNS:
            if re.search(pattern, value):
                return True

        return False

    @classmethod
    def extract_validation_type(cls, comment: str) -> Optional[str]:
        """Extract validation type from a comment string."""
        if not comment:
            return None

        match = re.search(r'\((\w+)\)', comment)
        if match:
            return match.group(1)

        return None
