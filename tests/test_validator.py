"""Tests for validator module."""

import pytest

from henvdall.validator import EnvValueValidator


class TestEnvValueValidator:
    """Tests for EnvValueValidator class."""

    def test_validate_int_valid(self):
        """Test integer validation with valid input."""
        result = EnvValueValidator.validate_int("42")
        assert result.is_valid is True
        assert result.error_message is None

    def test_validate_int_negative(self):
        """Test integer validation with negative number."""
        result = EnvValueValidator.validate_int("-10")
        assert result.is_valid is True

    def test_validate_int_invalid(self):
        """Test integer validation with invalid input."""
        result = EnvValueValidator.validate_int("not_a_number")
        assert result.is_valid is False
        assert result.error_message is not None

    def test_validate_url_valid(self):
        """Test URL validation with valid input."""
        result = EnvValueValidator.validate_url("https://example.com")
        assert result.is_valid is True
        assert result.error_message is None

    def test_validate_url_with_path(self):
        """Test URL validation with path."""
        result = EnvValueValidator.validate_url("https://api.example.com/v1/users")
        assert result.is_valid is True

    def test_validate_url_invalid(self):
        """Test URL validation with invalid input."""
        result = EnvValueValidator.validate_url("not_a_url")
        assert result.is_valid is False
        assert result.error_message is not None

    def test_validate_url_missing_scheme(self):
        """Test URL validation without scheme."""
        result = EnvValueValidator.validate_url("example.com")
        assert result.is_valid is False

    def test_is_placeholder_common_patterns(self):
        """Test placeholder detection with common patterns."""
        assert EnvValueValidator.is_placeholder("YOUR_API_KEY_HERE") is True
        assert EnvValueValidator.is_placeholder("your_key_here") is True
        assert EnvValueValidator.is_placeholder("PLACEHOLDER") is True
        assert EnvValueValidator.is_placeholder("change_me") is True
        assert EnvValueValidator.is_placeholder("admin123") is True
        assert EnvValueValidator.is_placeholder("password123") is True

    def test_is_placeholder_valid_values(self):
        """Test placeholder detection with valid values."""
        assert EnvValueValidator.is_placeholder("sk-1234567890abcdef") is False
        assert EnvValueValidator.is_placeholder("postgresql://localhost/db") is False
        assert EnvValueValidator.is_placeholder("production_key_abc123") is False

    def test_is_placeholder_empty(self):
        """Test placeholder detection with empty values."""
        assert EnvValueValidator.is_placeholder("") is True
        assert EnvValueValidator.is_placeholder("   ") is True

    def test_extract_validation_type(self):
        """Test extraction of validation type from comments."""
        assert EnvValueValidator.extract_validation_type("(int)") == "int"
        assert EnvValueValidator.extract_validation_type("some text (url) more text") == "url"
        assert EnvValueValidator.extract_validation_type("no validation") is None
        assert EnvValueValidator.extract_validation_type("") is None
