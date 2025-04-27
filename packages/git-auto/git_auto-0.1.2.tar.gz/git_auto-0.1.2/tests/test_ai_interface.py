import pytest
from unittest.mock import patch, MagicMock, mock_open  # Add mock_open
import time  # Import time for mocking
import json  # Import json for mocking
import hashlib  # Import hashlib for testing keys
from pathlib import Path  # Import Path for testing cache dir

# Modules to test
from git_auto.src.ai_interface import (
    validate_code_changes,
    generate_commit_message,
    generate_fallback_message,
    _load_prompt,
    _generate_cache_key,  # Import cache helpers for testing
    _read_from_cache,
    _write_to_cache,
)
from git_auto.src.config import AppConfig  # Import AppConfig for mocking
from git_auto.src.sanitizer import DataSanitizer

# --- Constants for Mocks ---

MOCK_DIFF = "diff --git a/file.py b/file.py\n--- a/file.py\n+++ b/file.py\n@@ -1 +1 @@\n-print('old')\n+print('new')"
MOCK_FILES = {"file.py": {"content": "print('new')", "extension": ".py"}}
MOCK_VALIDATION_RESPONSE = "VALIDATION: PASSED\nSUMMARY: Updated print statement."
MOCK_COMMIT_RESPONSE = (
    "fix: update print statement in file.py\n\nCorrect the output message."
)
MOCK_SANITIZED_DIFF = "diff --git a/file.py b/file.py\n--- a/file.py\n+++ b/file.py\n@@ -1 +1 @@\n-print('old')\n+print('new')"  # Assume no sanitization needed for this simple diff
MOCK_SANITIZED_COMMIT_RESPONSE = (
    MOCK_COMMIT_RESPONSE  # Assume no sensitive data in response
)
MOCK_REPO_CONTEXT = "Project Structure Overview:..."
MOCK_MODEL = "gemini-test-model"
MOCK_PROMPT_VALIDATION = (
    f"Validation Prompt:\nMODIFIED FILES:\n- file.py\nGIT DIFF:\n{MOCK_DIFF}"
)
MOCK_PROMPT_COMMIT = (
    f"Commit Prompt:\nMODIFIED FILES:\n- file.py\nGIT DIFF:\n{MOCK_DIFF}"
)

# --- Fixtures ---


@pytest.fixture
def mock_genai():
    # Mock the entire genai module used in ai_interface
    with patch("git_auto.src.ai_interface.genai") as mock_genai_module:
        # Mock the configure call
        mock_genai_module.configure = MagicMock()
        # Mock the GenerativeModel class
        mock_model_instance = MagicMock()
        mock_genai_module.GenerativeModel.return_value = mock_model_instance
        yield mock_genai_module, mock_model_instance


@pytest.fixture
def mock_config(max_diff_size=100):  # Add parameter for easy testing
    # Mock load_config to return predictable values including repo_context
    with patch("git_auto.src.ai_interface.load_config") as mock_load:
        # Simulate the AppConfig object being returned
        mock_app_config = MagicMock()
        mock_app_config.api_key = "TEST_API_KEY"
        mock_app_config.model = "gemini-test-model"
        mock_app_config.safety_settings = []  # Keep it simple for mock
        mock_app_config.generation_config_validation.model_dump.return_value = {
            "temperature": 0.1
        }
        mock_app_config.generation_config_commit.model_dump.return_value = {
            "temperature": 0.2
        }
        mock_app_config.max_diff_size = max_diff_size
        mock_app_config.validation_prompt_path = None
        mock_app_config.commit_prompt_path = None
        mock_app_config.custom_infuscation_patterns = []
        mock_app_config.repo_context = MOCK_REPO_CONTEXT  # Add mock context

        mock_load.return_value = mock_app_config
        yield mock_load


@pytest.fixture
def mock_sanitizer():
    # Mock the DataSanitizer class and its methods
    with patch(
        "git_auto.src.ai_interface.DataSanitizer"
    ) as mock_sanitizer_class:
        mock_instance = MagicMock()
        mock_sanitizer_class.return_value = mock_instance
        mock_instance.sanitize_text.return_value = MOCK_SANITIZED_DIFF
        mock_instance.desanitize_text.side_effect = (
            lambda text: text
        )  # Simple pass-through for testing
        mock_instance.get_sanitization_summary.return_value = "Sanitized 1 item."
        yield mock_instance


@pytest.fixture
def mock_load_prompt():
    # Mock _load_prompt to include repo_context placeholder
    with patch("git_auto.src.ai_interface._load_prompt") as mock_load:

        def side_effect(filename, custom_path=None):
            if filename == "validation_prompt.txt":
                return "Validation Prompt:\n{repo_context}\n{file_context}\nGIT DIFF:\n{processed_diff}"
            elif filename == "commit_prompt.txt":
                return "Commit Prompt:\n{repo_context}\n{file_context}\nGIT DIFF:\n{processed_diff}"
            return "Unknown prompt"

        mock_load.side_effect = side_effect
        yield mock_load


@pytest.fixture
def mock_config_cache(mocker, tmp_path):
    """Fixture for AppConfig with caching enabled and temp cache dir."""
    mock_cfg = AppConfig(
        GEMINI_API_KEY="test_key_cache",
        cache_enabled=True,
        cache_dir=tmp_path / "test_cache",
        cache_ttl_seconds=3600,  # 1 hour TTL for tests
        model=MOCK_MODEL,
    )
    # Ensure cache dir exists for the test
    mock_cfg.cache_dir.mkdir(parents=True, exist_ok=True)
    mocker.patch("git_auto.src.ai_interface.load_config", return_value=mock_cfg)
    return mock_cfg


# --- Tests for validate_code_changes ---


def test_validate_code_changes_success(mock_genai, mock_config, mock_load_prompt):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_VALIDATION_RESPONSE
    )

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES)

    assert result == MOCK_VALIDATION_RESPONSE
    mock_genai_module.configure.assert_called_once()
    mock_genai_module.GenerativeModel.assert_called_once()
    mock_model_instance.generate_content.assert_called_once()
    # Check structure: Repo context, File context before diff
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]
    assert "Validation Prompt:" in prompt_arg
    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + MOCK_DIFF in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


def test_validate_code_changes_infuscate(
    mock_genai, mock_config, mock_sanitizer, mock_load_prompt
):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_VALIDATION_RESPONSE
    )

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES, infuscate=True)

    assert result == MOCK_VALIDATION_RESPONSE
    mock_sanitizer.sanitize_text.assert_called_once_with(MOCK_DIFF)
    mock_sanitizer.desanitize_text.assert_called_once_with(MOCK_VALIDATION_RESPONSE)
    # Check structure with sanitized diff
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]
    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + MOCK_SANITIZED_DIFF in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


def test_validate_code_changes_api_error(mock_genai, mock_config, mock_load_prompt):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.side_effect = Exception("API Error")

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES)

    assert "VALIDATION: ERROR" in result


@pytest.mark.parametrize(
    "mock_config", [(20)], indirect=True
)  # Set max_diff_size via fixture
def test_validate_code_changes_truncation(mock_genai, mock_config, mock_load_prompt):
    """Test that the diff is truncated and a note is added."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_VALIDATION_RESPONSE
    )

    long_diff = "a" * 50  # Diff longer than max_diff_size (20)
    expected_truncated_diff = "a" * 20
    expected_note = "[Note: The provided diff was truncated due to length limitations.]"

    result = validate_code_changes(long_diff, MOCK_FILES)

    assert result == MOCK_VALIDATION_RESPONSE
    mock_model_instance.generate_content.assert_called_once()
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]

    # Check structure with truncated diff and note
    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + expected_truncated_diff in prompt_arg
    assert expected_note in prompt_arg
    assert long_diff not in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


# --- Tests for generate_commit_message ---


def test_generate_commit_message_success(mock_genai, mock_config, mock_load_prompt):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_COMMIT_RESPONSE
    )

    result = generate_commit_message(MOCK_DIFF, MOCK_FILES)

    assert result == MOCK_COMMIT_RESPONSE
    mock_model_instance.generate_content.assert_called_once()
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]
    # Check structure: Repo context, File context before diff
    assert "Commit Prompt:" in prompt_arg
    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + MOCK_DIFF in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


def test_generate_commit_message_infuscate(
    mock_genai, mock_config, mock_sanitizer, mock_load_prompt
):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_SANITIZED_COMMIT_RESPONSE
    )

    result = generate_commit_message(MOCK_DIFF, MOCK_FILES, infuscate=True)

    assert result == MOCK_SANITIZED_COMMIT_RESPONSE
    mock_sanitizer.sanitize_text.assert_called_once_with(MOCK_DIFF)
    mock_sanitizer.desanitize_text.assert_called_once_with(
        MOCK_SANITIZED_COMMIT_RESPONSE
    )
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]
    # Check structure with sanitized diff
    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + MOCK_SANITIZED_DIFF in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


def test_generate_commit_message_api_error_fallback(
    mock_genai, mock_config, mock_load_prompt
):
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.side_effect = Exception("API Error")

    # Patch the fallback function within the same module
    with patch(
        "git_auto.src.ai_interface.generate_fallback_message",
        return_value="fallback: commit",
    ) as mock_fallback:
        result = generate_commit_message(MOCK_DIFF, MOCK_FILES)
        assert result == "fallback: commit"
        mock_fallback.assert_called_once_with(["file.py"])


@pytest.mark.parametrize("mock_config", [(30)], indirect=True)  # Set max_diff_size
def test_generate_commit_message_truncation(mock_genai, mock_config, mock_load_prompt):
    """Test diff truncation for commit message generation."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_COMMIT_RESPONSE
    )

    long_diff = "b" * 60  # Diff longer than max_diff_size (30)
    expected_truncated_diff = "b" * 30
    expected_note = "[Note: The provided diff was truncated due to length limitations.]"

    result = generate_commit_message(long_diff, MOCK_FILES)

    assert result == MOCK_COMMIT_RESPONSE
    mock_model_instance.generate_content.assert_called_once()
    prompt_arg = mock_model_instance.generate_content.call_args[0][0]

    assert MOCK_REPO_CONTEXT in prompt_arg
    assert "MODIFIED FILES:\n- file.py" in prompt_arg
    assert "GIT DIFF:\n" + expected_truncated_diff in prompt_arg
    assert expected_note in prompt_arg
    assert long_diff not in prompt_arg
    assert prompt_arg.find(MOCK_REPO_CONTEXT) < prompt_arg.find("MODIFIED FILES:")
    assert prompt_arg.find("MODIFIED FILES:") < prompt_arg.find("GIT DIFF:")


# --- Tests for generate_fallback_message ---


def test_generate_fallback_message_add_py():
    files = {"src/component.py": {"status": "A", "extension": ".py"}}
    result = generate_fallback_message(files)
    assert result == "feat: add component.py"


def test_generate_fallback_message_modify_py():
    files = {"src/component.py": {"status": "M", "extension": ".py"}}
    result = generate_fallback_message(files)
    assert result == "refactor: modify component.py"


def test_generate_fallback_message_rename_py():
    files = {"src/new_component.py": {"status": "R", "extension": ".py"}}
    result = generate_fallback_message(files)
    assert result == "refactor: rename new_component.py"


def test_generate_fallback_message_multiple_yaml_modify():
    files = {
        "config/prod.yaml": {"status": "M", "extension": ".yaml"},
        "config/dev.yml": {"status": "M", "extension": ".yml"},
    }
    result = generate_fallback_message(files)
    # Prefix determined by extension for 'M' status
    assert (
        result == "config: modify existing files (mostly .yaml)"
    )  # .yaml might appear first


def test_generate_fallback_message_add_and_modify():
    files = {
        "new_feature.py": {"status": "A", "extension": ".py"},
        "existing_util.py": {"status": "M", "extension": ".py"},
    }
    result = generate_fallback_message(files)
    # 'A' status takes precedence for prefix 'feat'
    assert result == "feat: add new, modify existing files (mostly .py)"


def test_generate_fallback_message_test_file_modify():
    files = {"tests/test_component.py": {"status": "M", "extension": ".py"}}
    result = generate_fallback_message(files)
    # Filename check for 'test' takes precedence for 'M' status
    assert result == "test: modify test_component.py"


def test_generate_fallback_message_readme_modify():
    files = {"README.md": {"status": "M", "extension": ".md"}}
    result = generate_fallback_message(files)
    # Filename check for 'README' takes precedence for 'M' status
    assert result == "docs: modify README.md"


def test_generate_fallback_message_no_files():
    result = generate_fallback_message({})
    assert result == "chore: automated commit"


def test_generate_fallback_message_long_summary_truncation():
    files = {
        "a_very_very_very_long_filename_that_needs_truncation.py": {
            "status": "A",
            "extension": ".py",
        }
    }
    result = generate_fallback_message(files)
    assert result.startswith("feat: add a_very_very_very_long_filename_that_nee...")
    assert len(result) <= 50


# --- Tests for Cache Helpers ---


def test_generate_cache_key():
    key1 = _generate_cache_key("prompt1", "model1")
    key2 = _generate_cache_key("prompt2", "model1")
    key3 = _generate_cache_key("prompt1", "model2")
    key4 = _generate_cache_key("prompt1", "model1")
    assert isinstance(key1, str)
    assert len(key1) == 64  # SHA256 hex digest length
    assert key1 != key2
    assert key1 != key3
    assert key1 == key4


def test_read_from_cache_hit(tmp_path):
    cache_dir = tmp_path
    key = "testkey_hit"
    ttl = 3600
    response = "cached response data"
    cache_data = {
        "timestamp": time.time() - 100,
        "response": response,
    }  # Recent timestamp
    cache_file = cache_dir / f"{key}.json"
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    result = _read_from_cache(cache_dir, key, ttl)
    assert result == response


def test_read_from_cache_miss_no_file(tmp_path):
    result = _read_from_cache(tmp_path, "testkey_miss", 3600)
    assert result is None


def test_read_from_cache_miss_expired(tmp_path):
    cache_dir = tmp_path
    key = "testkey_expired"
    ttl = 100  # Short TTL
    response = "expired data"
    cache_data = {
        "timestamp": time.time() - 200,
        "response": response,
    }  # Expired timestamp
    cache_file = cache_dir / f"{key}.json"
    with open(cache_file, "w") as f:
        json.dump(cache_data, f)

    result = _read_from_cache(cache_dir, key, ttl)
    assert result is None


def test_read_from_cache_invalid_json(tmp_path):
    cache_dir = tmp_path
    key = "testkey_invalid"
    ttl = 3600
    cache_file = cache_dir / f"{key}.json"
    cache_file.write_text("this is not json")

    result = _read_from_cache(cache_dir, key, ttl)
    assert result is None


def test_write_to_cache(tmp_path):
    cache_dir = tmp_path
    key = "testkey_write"
    response = "data to write"
    _write_to_cache(cache_dir, key, response)

    cache_file = cache_dir / f"{key}.json"
    assert cache_file.is_file()
    with open(cache_file, "r") as f:
        data = json.load(f)
    assert data["response"] == response
    assert "timestamp" in data
    assert time.time() - data["timestamp"] < 5  # Should be very recent


# --- Tests for AI Functions with Caching ---


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_validate_cache_hit(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test cache hit for validation."""
    mock_genai_module, mock_model_instance = mock_genai
    cached_response = "cached validation result"
    mock_read.return_value = cached_response

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES)

    assert result == cached_response
    # Verify cache read was attempted with correct key
    expected_key = _generate_cache_key(MOCK_PROMPT_VALIDATION, MOCK_MODEL)
    mock_read.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, mock_config_cache.cache_ttl_seconds
    )
    # Verify AI was NOT called and cache was NOT written
    mock_model_instance.generate_content.assert_not_called()
    mock_write.assert_not_called()


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_validate_cache_miss(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test cache miss for validation (AI called, cache written)."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_VALIDATION_RESPONSE
    )
    mock_read.return_value = None  # Simulate cache miss

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES)

    assert result == MOCK_VALIDATION_RESPONSE
    expected_key = _generate_cache_key(MOCK_PROMPT_VALIDATION, MOCK_MODEL)
    mock_read.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, mock_config_cache.cache_ttl_seconds
    )
    # Verify AI WAS called and cache WAS written
    mock_model_instance.generate_content.assert_called_once()
    mock_write.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, MOCK_VALIDATION_RESPONSE
    )


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_validate_no_cache_flag(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test that --no-cache flag bypasses cache read/write."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_VALIDATION_RESPONSE
    )

    result = validate_code_changes(MOCK_DIFF, MOCK_FILES, no_cache=True)

    assert result == MOCK_VALIDATION_RESPONSE
    # Verify cache was NOT read or written
    mock_read.assert_not_called()
    mock_write.assert_not_called()
    # Verify AI WAS called
    mock_model_instance.generate_content.assert_called_once()


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_commit_cache_hit(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test cache hit for commit message generation."""
    mock_genai_module, mock_model_instance = mock_genai
    cached_response = "cached commit msg"
    mock_read.return_value = cached_response

    result = generate_commit_message(MOCK_DIFF, MOCK_FILES)

    assert result == cached_response
    expected_key = _generate_cache_key(MOCK_PROMPT_COMMIT, MOCK_MODEL)
    mock_read.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, mock_config_cache.cache_ttl_seconds
    )
    mock_model_instance.generate_content.assert_not_called()
    mock_write.assert_not_called()


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_commit_cache_miss(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test cache miss for commit message generation."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_COMMIT_RESPONSE
    )
    mock_read.return_value = None

    result = generate_commit_message(MOCK_DIFF, MOCK_FILES)

    assert result == MOCK_COMMIT_RESPONSE
    expected_key = _generate_cache_key(MOCK_PROMPT_COMMIT, MOCK_MODEL)
    mock_read.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, mock_config_cache.cache_ttl_seconds
    )
    mock_model_instance.generate_content.assert_called_once()
    mock_write.assert_called_once_with(
        mock_config_cache.cache_dir, expected_key, MOCK_COMMIT_RESPONSE
    )


@patch("git_auto.src.ai_interface._read_from_cache")
@patch("git_auto.src.ai_interface._write_to_cache")
def test_commit_no_cache_flag(
    mock_write, mock_read, mock_genai, mock_config_cache, mock_load_prompt
):
    """Test --no-cache flag for commit message generation."""
    mock_genai_module, mock_model_instance = mock_genai
    mock_model_instance.generate_content.return_value = MagicMock(
        text=MOCK_COMMIT_RESPONSE
    )

    result = generate_commit_message(MOCK_DIFF, MOCK_FILES, no_cache=True)

    assert result == MOCK_COMMIT_RESPONSE
    mock_read.assert_not_called()
    mock_write.assert_not_called()
    mock_model_instance.generate_content.assert_called_once()
