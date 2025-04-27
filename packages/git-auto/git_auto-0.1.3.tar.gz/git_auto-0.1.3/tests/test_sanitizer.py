import pytest
import re  # Import re for testing invalid patterns
from git_auto.src.sanitizer import (
    DataSanitizer,
    sanitization_mapping,
    reverse_mapping,
)


# --- Fixtures ---
@pytest.fixture
def sanitizer():
    # Reset mappings before each test to ensure isolation
    sanitization_mapping.clear()
    reverse_mapping.clear()
    return DataSanitizer()


@pytest.fixture
def default_sanitizer():
    # Reset mappings before each test to ensure isolation
    sanitization_mapping.clear()
    reverse_mapping.clear()
    return DataSanitizer()


# --- Basic Sanitization Tests ---


def test_sanitize_ip_address(default_sanitizer):
    """Test basic IP address sanitization."""
    text = "Connecting to server at 192.0.2.1 for data transfer."
    sanitized_text = default_sanitizer.sanitize_text(text)
    assert "192.0.2.1" not in sanitized_text
    assert "IP-1" in sanitized_text
    assert sanitized_text == "Connecting to server at IP-1 for data transfer."


def test_preserve_local_ip(sanitizer):
    """Test that local/private IPs are preserved."""
    text = "Local IP is 192.168.1.100 and loopback is 127.0.0.1."
    sanitized_text = sanitizer.sanitize_text(text)
    assert sanitized_text == text  # Should remain unchanged


def test_sanitize_email(sanitizer):
    """Test basic email sanitization."""
    text = "Contact support@example.com for help."
    sanitized_text = sanitizer.sanitize_text(text)
    assert "support@example.com" not in sanitized_text
    assert "user-1@example.com" in sanitized_text
    assert sanitized_text == "Contact user-1@example.com for help."


def test_sanitize_domain(sanitizer):
    """Test domain name sanitization."""
    text = "Deployed to internal.example-app.cloud and public.example.org."
    sanitized = sanitizer.sanitize_text(text)
    assert "internal.example-app.cloud" not in sanitized
    assert "public.example.org" not in sanitized
    assert "example-1.com" in sanitized  # First domain found
    assert "example-2.com" in sanitized  # Second domain found
    assert sanitized == "Deployed to example-1.com and example-2.com."


def test_preserve_common_domains(sanitizer):
    """Test that common public domains are preserved."""
    text = "Code is on github.com, image is on quay.io/repo."
    sanitized = sanitizer.sanitize_text(text)
    assert sanitized == text


def test_sanitize_api_key(sanitizer):
    """Test API key sanitization."""
    text = "API_KEY=a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"
    sanitized = sanitizer.sanitize_text(text)
    assert "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2" not in sanitized
    assert "API-KEY-" in sanitized


def test_preserve_git_hash(sanitizer):
    """Test that git hashes are not mistaken for API keys."""
    text = "Commit hash is abcdef1234567890abcdef1234567890abcdef12."
    sanitized = sanitizer.sanitize_text(text)
    assert sanitized == text


def test_sanitize_uuid(sanitizer):
    """Test UUID sanitization."""
    text = "Request ID: 123e4567-e89b-12d3-a456-426614174000"
    sanitized = sanitizer.sanitize_text(text)
    assert "123e4567-e89b-12d3-a456-426614174000" not in sanitized
    assert "uuid-1" in sanitized


def test_sanitize_url_with_path(sanitizer):
    """Test URL sanitization."""
    text = "Access https://api.example.net/v1/users for data."
    sanitized = sanitizer.sanitize_text(text)
    assert "api.example.net" not in sanitized
    assert "https://example-1.com/resource" in sanitized  # Domain part gets replaced


def test_sanitize_hostname(sanitizer):
    """Test hostname sanitization."""
    text = "Connect to db-server-01.prod.internal for database."
    sanitized = sanitizer.sanitize_text(text)
    assert "db-server-01.prod.internal" not in sanitized
    assert "hostname-1.internal" in sanitized


# --- Custom Pattern Tests ---


def test_custom_pattern_sanitization():
    """Test sanitization using a custom pattern."""
    custom_patterns = [
        r"project-id-\d{4}",  # Example: project-id-1234
        r"user-secret-[a-z]+",  # Example: user-secret-abc
    ]
    sanitizer = DataSanitizer(custom_patterns=custom_patterns)
    text = "Configured with project-id-5678 and user-secret-xyz."
    sanitized = sanitizer.sanitize_text(text)

    assert "project-id-5678" not in sanitized
    assert "user-secret-xyz" not in sanitized
    # Check for generic custom placeholders
    assert "CUSTOM-1-" in sanitized  # Placeholder for first custom pattern
    assert "CUSTOM-2-" in sanitized  # Placeholder for second custom pattern


def test_custom_pattern_desanitization():
    """Test desanitization with custom patterns."""
    custom_patterns = [r"session-\w+"]
    sanitizer = DataSanitizer(custom_patterns=custom_patterns)
    original = "User session-abc123 logged in."
    sanitized = sanitizer.sanitize_text(original)
    desanitized = sanitizer.desanitize_text(sanitized)

    assert "session-abc123" not in sanitized
    assert "CUSTOM-1-" in sanitized
    assert desanitized == original


def test_custom_pattern_invalid_regex():
    """Test that invalid custom regex patterns are skipped gracefully."""
    custom_patterns = [
        r"valid-pattern-\d+",
        r"invalid-pattern-(",  # Invalid regex
        r"another-valid-\w+",
    ]
    # Expect a warning log, but initialization should succeed
    sanitizer = DataSanitizer(custom_patterns=custom_patterns)

    # Check that the valid patterns were added
    assert "custom_1" in sanitizer.patterns
    assert (
        "custom_3" in sanitizer.patterns
    )  # Should be indexed based on valid patterns found
    # Check that the invalid pattern was skipped (no custom_2)
    assert "custom_2" not in sanitizer.patterns

    text = "Data: valid-pattern-123, invalid-pattern-(, another-valid-abc"
    sanitized = sanitizer.sanitize_text(text)

    # Check that valid patterns work
    assert "valid-pattern-123" not in sanitized
    assert "another-valid-abc" not in sanitized
    assert "CUSTOM-1-" in sanitized
    assert (
        "CUSTOM-2-" in sanitized
    )  # Corresponds to the *third* pattern (another-valid-abc)

    # Check that the text matching the invalid pattern remains unchanged
    assert "invalid-pattern-(" in sanitized


# --- Custom Literal Tests ---


def test_custom_literal_sanitization():
    """Test sanitization using custom literals."""
    custom_literals = [
        "ProjectX-Secret-Key",  # Longer
        "ProjectX",  # Shorter
        "prod.mycompany.internal",
    ]
    # Pass literals to constructor
    sanitizer = DataSanitizer(custom_literals=custom_literals)
    text = "Connect ProjectX to prod.mycompany.internal using ProjectX-Secret-Key."
    sanitized = sanitizer.sanitize_text(text)

    assert "ProjectX-Secret-Key" not in sanitized
    assert "ProjectX" not in sanitized
    assert "prod.mycompany.internal" not in sanitized
    # Check for literal placeholders (indices based on sorted list: Key, URL, ProjectX)
    assert "LITERAL-1-" in sanitized  # ProjectX-Secret-Key
    assert "LITERAL-2-" in sanitized  # prod.mycompany.internal
    assert "LITERAL-3-" in sanitized  # ProjectX
    # Verify longer match replaced first
    assert sanitized.count("LITERAL-3-") == 1  # ProjectX should only be replaced once


def test_custom_literal_desanitization():
    """Test desanitization with custom literals."""
    custom_literals = ["my-internal-app.local"]
    sanitizer = DataSanitizer(custom_literals=custom_literals)
    original = "Access my-internal-app.local for data."
    sanitized = sanitizer.sanitize_text(original)
    desanitized = sanitizer.desanitize_text(sanitized)

    assert "my-internal-app.local" not in sanitized
    assert "LITERAL-1-" in sanitized
    assert desanitized == original


def test_literal_and_regex_interaction():
    """Test that literals are replaced before regex patterns."""
    custom_literals = ["admin@mycompany.com"]  # Literal email
    # Default email regex pattern also exists
    sanitizer = DataSanitizer(custom_literals=custom_literals)
    text = "Login as admin@mycompany.com or user@example.com."
    sanitized = sanitizer.sanitize_text(text)

    assert "admin@mycompany.com" not in sanitized
    assert "user@example.com" not in sanitized
    # Check that the literal was replaced using the literal placeholder
    assert "LITERAL-1-" in sanitized
    # Check that the regex pattern replaced the other email
    assert "user-1@example.com" in sanitized


# --- Desanitization Tests ---


def test_desanitize_ip(sanitizer):
    original = "Server IP: 198.51.100.1"
    sanitized = sanitizer.sanitize_text(original)
    desanitized = sanitizer.desanitize_text(sanitized)
    assert sanitized != original
    assert "IP-1" in sanitized
    assert desanitized == original


def test_desanitize_multiple(sanitizer):
    original = "User admin@example.com accessed 198.51.100.1 via api.example.org"
    sanitized = sanitizer.sanitize_text(original)
    desanitized = sanitizer.desanitize_text(sanitized)

    assert "admin@example.com" not in sanitized
    assert "198.51.100.1" not in sanitized
    assert "api.example.org" not in sanitized
    assert "user-1@example.com" in sanitized
    assert "IP-1" in sanitized
    assert "example-1.com" in sanitized  # Domain gets sanitized

    assert desanitized == original


# --- Preservation Tests (Git Syntax etc.) ---


def test_preserve_git_diff_headers(sanitizer):
    """Ensure git diff headers are untouched."""
    text = (
        "diff --git a/file.txt b/file.txt\n"
        "index 1234567..abcdef0 100644\n"
        "--- a/file.txt\n"
        "+++ b/file.txt\n"
        "@@ -1,1 +1,1 @@\n"
        "-Hello 1.2.3.4\n"
        "+Hello IP-1"
    )
    sanitized = sanitizer.sanitize_text(text)
    # Only the IP within the content line should change
    expected = (
        "diff --git a/file.txt b/file.txt\n"
        "index 1234567..abcdef0 100644\n"
        "--- a/file.txt\n"
        "+++ b/file.txt\n"
        "@@ -1,1 +1,1 @@\n"
        "-Hello IP-1\n"
        "+Hello IP-1"
    )
    assert sanitized == expected


def test_preserve_known_settings(sanitizer):
    """Ensure known setting keys are not sanitized."""
    text = "Set targetPort: 8080 and interval: 30s"
    sanitized = sanitizer.sanitize_text(text)
    assert sanitized == text


def test_preserve_filepaths(sanitizer):
    """Ensure common file paths are not mistaken for domains/hostnames."""
    text = "Modified src/utils/helpers.py and tests/test_api.py"
    sanitized = sanitizer.sanitize_text(text)
    assert sanitized == text


# --- Edge Case Tests ---


def test_overlapping_matches(sanitizer):
    """Test scenario where matches might overlap (though regex usually handles this)."""
    # Example: URL containing an email-like pattern
    text = "Go to https://user-1@example.com/login for details."
    sanitized = sanitizer.sanitize_text(text)
    # Expect the URL pattern to take precedence or handle correctly
    assert (
        "user-1@example.com" not in sanitized
    )  # Should not be sanitized as email separately
    assert "https://example-1.com/resource" in sanitized  # URL replaced


def test_empty_input(sanitizer):
    assert sanitizer.sanitize_text("") == ""
    assert sanitizer.desanitize_text("") == ""


def test_no_sensitive_data(sanitizer):
    text = "This is a simple line of text."
    sanitized = sanitizer.sanitize_text(text)
    assert sanitized == text
    desanitized = sanitizer.desanitize_text(sanitized)
    assert desanitized == text
