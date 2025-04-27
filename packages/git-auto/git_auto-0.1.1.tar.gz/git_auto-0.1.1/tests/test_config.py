import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml  # Import yaml for dumping in tests
from pydantic import ValidationError
import subprocess  # Import subprocess for mocking
import logging  # Import logging for caplog

# Module to test
from git_auto.src.config import (
    load_config,
    find_config_file,
    AppConfig,
    load_custom_patterns,
    generate_repo_context,
    load_custom_literals,
)  # Import load_custom_literals

# --- Fixtures ---


@pytest.fixture
def mock_env(monkeypatch):
    """Fixture to temporarily set environment variables."""
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.delenv("MODEL", raising=False)
    monkeypatch.delenv("MAX_DIFF_SIZE", raising=False)
    monkeypatch.delenv("VALIDATION_PROMPT_PATH", raising=False)
    monkeypatch.delenv("COMMIT_TEMP", raising=False)
    monkeypatch.delenv("INFUSCATION_PATTERNS_FILE", raising=False)
    monkeypatch.delenv(
        "INFUSCATION_LITERALS_FILE", raising=False
    )  # Clear literals file
    monkeypatch.delenv(
        "STANDARD_OUTPUT_TEMPLATE_PATH", raising=False
    )  # Clear template paths
    monkeypatch.delenv("MINIMAL_OUTPUT_TEMPLATE_PATH", raising=False)
    yield monkeypatch


@pytest.fixture
def mock_yaml(mocker):
    """Fixture to mock the yaml module."""
    mock_yaml_module = MagicMock()
    mock_yaml_module.safe_load.return_value = {}
    mocker.patch("git_auto.src.config.yaml", mock_yaml_module)
    yield mock_yaml_module


@pytest.fixture
def temp_config_file(tmp_path, content):
    """Fixture to create a temporary config file."""
    config_path = tmp_path / ".mycli.yaml"
    config_path.write_text(content)
    return config_path


@pytest.fixture
def temp_patterns_file(tmp_path, content):
    """Fixture to create a temporary patterns file."""
    patterns_path = tmp_path / "custom_patterns.txt"
    patterns_path.write_text(content)
    return patterns_path


@pytest.fixture
def temp_literals_file(tmp_path, content):
    """Fixture to create a temporary literals file."""
    literals_path = tmp_path / "custom_literals.txt"
    literals_path.write_text(content)
    return literals_path


# --- Tests for find_config_file ---


def test_find_config_file_current_dir(tmp_path, monkeypatch):
    """Test finding config in current directory."""
    monkeypatch.chdir(tmp_path)
    config_file = tmp_path / ".mycli.yaml"
    config_file.touch()
    found_path = find_config_file()
    assert found_path == config_file


def test_find_config_file_home_dir(tmp_path, monkeypatch):
    """Test finding config in home directory."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    config_file = tmp_path / ".mycli.yaml"
    config_file.touch()
    found_path = find_config_file()
    assert found_path == config_file


def test_find_config_file_xdg_dir(tmp_path, monkeypatch):
    """Test finding config in XDG config directory."""
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    xdg_config_dir = tmp_path / ".config" / "mycli"
    xdg_config_dir.mkdir(parents=True)
    config_file = xdg_config_dir / "config.yaml"
    config_file.touch()
    found_path = find_config_file()
    assert found_path == config_file


def test_find_config_file_priority(tmp_path, monkeypatch):
    """Test priority: CWD > Home > XDG."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    cwd_file = tmp_path / ".mycli.yaml"
    home_file = tmp_path / "home_config.yaml"
    xdg_dir = tmp_path / ".config" / "mycli"
    xdg_dir.mkdir(parents=True)
    xdg_file = xdg_dir / "config.yaml"

    cwd_file.touch()
    home_file.touch()
    xdg_file.touch()

    monkeypatch.setattr(Path, "home", lambda: home_file.parent)
    (tmp_path / ".mycli.yaml").rename(cwd_file)
    (tmp_path / ".mycli.yaml").touch()

    found_path = find_config_file()
    assert found_path == cwd_file

    cwd_file.unlink()
    found_path = find_config_file()
    assert found_path == (tmp_path / ".mycli.yaml")

    (tmp_path / ".mycli.yaml").unlink()
    found_path = find_config_file()
    assert found_path == xdg_file


def test_find_config_file_not_found(tmp_path, monkeypatch):
    """Test when no config file is found."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "nonexistent_home")
    found_path = find_config_file()
    assert found_path is None


# --- Tests for load_custom_patterns ---


def test_load_custom_patterns_success(temp_patterns_file):
    patterns_content = r"""
    [commit_patterns]
    # Example pattern - matches digits
    example = "\d+"
    """
    patterns_path = temp_patterns_file(patterns_content)
    patterns = load_custom_patterns(str(patterns_path))
    assert patterns == [r"SECRET_KEY_\d+", r"project-\w+-id"]


def test_load_custom_patterns_file_not_found():
    patterns = load_custom_patterns("non_existent_file.txt")
    assert patterns == []


def test_load_custom_patterns_empty_file(temp_patterns_file):
    patterns_path = temp_patterns_file("")
    patterns = load_custom_patterns(str(patterns_path))
    assert patterns == []


def test_load_custom_patterns_none_path():
    patterns = load_custom_patterns(None)
    assert patterns == []


# --- Tests for load_custom_literals ---


def test_load_custom_literals_success(temp_literals_file):
    literals_content = """
    # Comment
    LongerLiteralString
    ShortLiteral

    Another Literal
    """
    literals_path = temp_literals_file(literals_content)
    literals = load_custom_literals(str(literals_path))
    # Check sorting by length descending
    assert literals == ["LongerLiteralString", "Another Literal", "ShortLiteral"]


def test_load_custom_literals_file_not_found():
    literals = load_custom_literals("non_existent_literals.txt")
    assert literals == []


def test_load_custom_literals_empty_file(temp_literals_file):
    literals_path = temp_literals_file("")
    literals = load_custom_literals(str(literals_path))
    assert literals == []


def test_load_custom_literals_none_path():
    literals = load_custom_literals(None)
    assert literals == []


# --- Tests for generate_repo_context ---


@pytest.fixture
def mock_repo_structure(tmp_path):
    """Creates a mock directory structure for testing context generation."""
    root = tmp_path / "test_repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "src" / "main.py").touch()
    (root / "src" / "utils.py").touch()
    (root / "tests").mkdir()
    (root / "tests" / "test_main.py").touch()
    (root / ".git").mkdir()  # Should be ignored
    (root / "README.md").touch()
    (root / "requirements.txt").touch()
    (root / "subdir1").mkdir()
    (root / "subdir1" / "subsubdir").mkdir()
    (root / "subdir1" / "subsubdir" / "deep_file.txt").touch()
    (root / "subdir2").mkdir()
    (root / "subdir2" / "another_file.yaml").touch()
    return root


@pytest.fixture
def mock_repo_structure_detailed(tmp_path):
    """Creates a more detailed mock structure for context testing."""
    root = tmp_path / "test_repo_detailed"
    root.mkdir()
    (root / "src").mkdir()
    (root / "src" / "main.py").touch()  # Key file
    (root / "src" / "utils.py").touch()
    (root / "src" / "__init__.py").touch()
    (root / "tests").mkdir()
    (root / "tests" / "test_main.py").touch()
    (root / "tests" / "conftest.py").touch()
    (root / ".git").mkdir()  # Ignored
    (root / "node_modules").mkdir()  # Ignored
    (root / "README.md").touch()  # Key file
    (root / "pyproject.toml").touch()  # Key file
    (root / "data").mkdir()
    # Add more files than max_files_per_dir default (10)
    for i in range(15):
        (root / "data" / f"file_{i}.csv").touch()
    return root


def test_generate_repo_context_basic(mock_repo_structure):
    context = generate_repo_context(mock_repo_structure, max_depth=2)
    expected = """
Project Root: test_repo
├── README.md
├── requirements.txt
├── src
│   ├── main.py
│   └── utils.py
├── subdir1
│   └── subsubdir
│       └── ...
├── subdir2
│   └── another_file.yaml
└── tests
    └── test_main.py
""".strip()
    # Normalize line endings and spacing for comparison
    assert "\n".join(line.strip() for line in context.splitlines()) == "\n".join(
        line.strip() for line in expected.splitlines()
    )
    assert ".git" not in context


def test_generate_repo_context_max_depth(mock_repo_structure):
    context_d1 = generate_repo_context(mock_repo_structure, max_depth=1)
    context_d3 = generate_repo_context(mock_repo_structure, max_depth=3)

    assert "subsubdir" not in context_d1
    assert "subdir1" in context_d1
    assert "..." in context_d1  # Ellipsis should appear at depth 1 directories

    assert "subsubdir" in context_d3
    assert "deep_file.txt" in context_d3
    assert "..." not in context_d3  # Should reach the deep file within max_depth 3


def test_generate_repo_context_ignore_dirs(tmp_path):
    root = tmp_path / "ignore_test"
    root.mkdir()
    (root / "src").mkdir()
    (root / "node_modules").mkdir()
    (root / "node_modules" / "some_lib").touch()
    (root / "src" / "app.js").touch()
    context = generate_repo_context(root)
    assert "node_modules" not in context
    assert "app.js" in context


def test_generate_repo_context_detailed(mock_repo_structure_detailed):
    """Test context generation with file counts, key files, and limits."""
    context = generate_repo_context(
        mock_repo_structure_detailed, max_depth=3, max_files_per_dir=5
    )
    expected_lines = [
        "Project Root: test_repo_detailed",
        "├── * README.md",  # Key file marked
        "├── * pyproject.toml",  # Key file marked
        "├── data/ (15 items)",  # Directory with item count
        "│   ├── file_0.csv",
        "│   ├── file_1.csv",
        "│   ├── file_2.csv",
        "│   ├── file_3.csv",
        "│   └── file_4.csv",
        "│   ... (10 more files)",  # File limit ellipsis
        "├── src/ (3 items)",
        "│   ├── * __init__.py",  # Key file marked
        "│   ├── * main.py",  # Key file marked
        "│   └── utils.py",
        "└── tests/ (2 items)",
        "    ├── conftest.py",
        "    └── test_main.py",
    ]
    # Normalize and compare
    actual_lines = [line.strip() for line in context.splitlines()]
    expected_normalized = [line.strip() for line in expected_lines]
    assert actual_lines == expected_normalized
    assert ".git" not in context
    assert "node_modules" not in context


def test_generate_repo_context_total_line_limit(mock_repo_structure_detailed):
    """Test that the total line limit truncates the output."""
    context = generate_repo_context(
        mock_repo_structure_detailed,
        max_depth=5,
        max_files_per_dir=20,
        max_total_lines=10,
    )
    actual_lines = context.splitlines()
    assert len(actual_lines) <= 11  # Max lines + potential final ellipsis
    assert "... (output truncated)" in actual_lines[-1]
    # Check that some initial structure is present
    assert "Project Root: test_repo_detailed" in actual_lines[0]
    assert "* README.md" in context
    assert "data/" in context
    # Check that later parts are missing
    assert "tests/" not in context


# --- Tests for load_config ---


@patch("git_auto.src.config.subprocess.run")  # Mock subprocess globally for load_config tests
def test_load_config_dynamic_repo_context(mock_subproc_run, tmp_path, mock_env):
    """Test that repo context is generated dynamically."""
    mock_env.setenv("GEMINI_API_KEY", "api_key_ctx")
    # Mock git rev-parse returning the temp path as the repo root
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))

    # Create a dummy file structure within tmp_path
    (tmp_path / "file1.py").touch()
    (tmp_path / "subdir").mkdir()
    (tmp_path / "subdir" / "file2.txt").touch()

    config = load_config()

    assert isinstance(config, AppConfig)
    assert config.repo_context is not None
    assert f"Project Root: {tmp_path.name}" in config.repo_context
    assert "file1.py" in config.repo_context
    assert "subdir" in config.repo_context
    assert "file2.txt" in config.repo_context
    mock_subproc_run.assert_called_once_with(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=False,
        cwd=Path.cwd(),
    )


@patch("git_auto.src.config.subprocess.run")
def test_load_config_git_rev_parse_fails(mock_subproc_run, mock_env):
    """Test fallback when git rev-parse fails."""
    mock_env.setenv("GEMINI_API_KEY", "api_key_ctx_fail")
    mock_subproc_run.return_value = MagicMock(
        returncode=1, stdout="", stderr="not a git repo"
    )

    config = load_config()
    assert isinstance(config, AppConfig)
    assert "Repository structure context unavailable." in config.repo_context


@patch("git_auto.src.config.subprocess.run")
def test_load_config_git_not_found(mock_subproc_run, mock_env):
    """Test fallback when git command is not found."""
    mock_env.setenv("GEMINI_API_KEY", "api_key_ctx_nogit")
    mock_subproc_run.side_effect = FileNotFoundError

    config = load_config()
    assert isinstance(config, AppConfig)
    assert "git not found" in config.repo_context


@patch("git_auto.src.config.subprocess.run")  # Add mock
def test_load_config_api_key_from_env(mock_subproc_run, mock_env, caplog):
    """Test loading API key from environment and check debug log."""
    caplog.set_level(logging.DEBUG)  # Capture debug messages
    api_key = "env_api_key_123"
    mock_env.setenv("GEMINI_API_KEY", api_key)
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(Path.cwd()))

    config = load_config()

    assert isinstance(config, AppConfig)
    assert config.api_key == api_key
    assert config.model == "gemini-1.5-flash"
    assert config.repo_context is not None

    # Check for the debug log message
    assert "Final configuration loaded:" in caplog.text
    # Ensure API key is NOT in the logged config dictionary string
    assert f"'api_key': '{api_key}'" not in caplog.text
    assert "'model': 'gemini-1.5-flash'" in caplog.text  # Check other field is present


@patch("git_auto.src.config.find_config_file")  # Patch within the module
@patch("git_auto.src.config.subprocess.run")
def test_load_config_from_file(
    mock_subproc_run, mock_find_config, tmp_path, mock_env, mock_yaml, caplog
):
    """Test loading configuration purely from a file and check debug log."""
    caplog.set_level(logging.DEBUG)
    api_key = "file_api_key_456"
    file_data = {
        "GEMINI_API_KEY": api_key,
        "model": "file_model",
        "max_diff_size": 5000,
        "validation_prompt_path": "/file/val.txt",
        "generation_config_commit": {"temperature": 0.99, "max_output_tokens": 100},
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_find_config.return_value = config_file

    config = load_config()

    assert isinstance(config, AppConfig)
    assert config.api_key == api_key
    assert config.model == "file_model"
    assert config.max_diff_size == 5000
    assert config.validation_prompt_path == "/file/val.txt"
    assert config.commit_prompt_path is None
    assert config.generation_config_commit.temperature == 0.99
    assert config.generation_config_commit.max_output_tokens == 100
    assert config.generation_config_commit.top_p == 0.95
    assert config.generation_config_validation.temperature == 0.2

    # Check for the debug log message
    assert "Final configuration loaded:" in caplog.text
    assert f"'api_key': '{api_key}'" not in caplog.text
    assert "'model': 'file_model'" in caplog.text


@patch("git_auto.src.config.subprocess.run")
def test_load_config_env_overrides_file(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "env_api_key_789")
    mock_env.setenv("MODEL", "env_model")
    mock_env.setenv("COMMIT_TEMP", "0.11")

    file_data = {
        "GEMINI_API_KEY": "file_api_key",
        "model": "file_model",
        "generation_config_commit": {"temperature": 0.99, "max_output_tokens": 50},
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.api_key == "env_api_key_789"
    assert config.model == "env_model"
    assert config.generation_config_commit.temperature == 0.11
    assert config.generation_config_commit.max_output_tokens == 50


@patch("git_auto.src.config.subprocess.run")
def test_load_config_invalid_yaml_file(mock_subproc_run, tmp_path, mock_env, mock_yaml):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "env_api_key_abc")
    file_content = "model: model1\ninvalid_yaml: ["
    config_file = temp_config_file(tmp_path, file_content)
    mock_yaml.safe_load.side_effect = yaml.YAMLError("parsing failed")
    mock_yaml.YAMLError = yaml.YAMLError

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.api_key == "env_api_key_abc"
    assert config.model == "gemini-1.5-flash"
    mock_yaml.safe_load.assert_called_once()


@patch("git_auto.src.config.subprocess.run")
def test_load_config_pydantic_validation_error(mock_subproc_run, mock_env):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(Path.cwd()))
    mock_env.setenv("GEMINI_API_KEY", "env_api_key_def")
    mock_env.setenv("MAX_DIFF_SIZE", "not_an_integer")

    with pytest.raises(ValidationError) as excinfo:
        load_config()
    assert "max_diff_size" in str(excinfo.value)
    assert "Input should be a valid integer" in str(excinfo.value)


@patch("git_auto.src.config.subprocess.run")
def test_load_config_pydantic_validation_error_nested(mock_subproc_run, mock_env):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(Path.cwd()))
    mock_env.setenv("GEMINI_API_KEY", "env_api_key_ghi")
    mock_env.setenv("COMMIT_TEMP", "2.5")

    with pytest.raises(ValidationError) as excinfo:
        load_config()
    assert "generation_config_commit.temperature" in str(excinfo.value)
    assert "less than or equal to 1.0" in str(excinfo.value)


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_custom_patterns_file(
    mock_subproc_run, tmp_path, mock_env, mock_yaml, temp_patterns_file
):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_123")
    patterns_content = r"USER_TOKEN_\w+"
    patterns_path = temp_patterns_file(patterns_content)

    file_data = {"infuscation_patterns_file": str(patterns_path)}
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.infuscation_patterns_file == str(patterns_path)
    assert config.custom_infuscation_patterns == [r"USER_TOKEN_\w+"]


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_custom_patterns_env_override(
    mock_subproc_run, tmp_path, mock_env, mock_yaml, temp_patterns_file
):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_456")
    patterns_content_env = "ENV_PATTERN"
    patterns_path_env = temp_patterns_file(patterns_content_env)
    mock_env.setenv("INFUSCATION_PATTERNS_FILE", str(patterns_path_env))

    # Config file points to a different (or non-existent) file
    file_data = {"infuscation_patterns_file": "/path/to/ignored_patterns.txt"}
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.infuscation_patterns_file == str(patterns_path_env)  # Env var wins
    assert config.custom_infuscation_patterns == ["ENV_PATTERN"]


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_template_paths_file(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_t1")
    file_data = {
        "standard_output_template_path": "/path/std.txt",
        "minimal_output_template_path": "./rel/min.txt",
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.standard_output_template_path == "/path/std.txt"
    assert config.minimal_output_template_path == "./rel/min.txt"


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_template_paths_env(mock_subproc_run, mock_env):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(Path.cwd()))
    mock_env.setenv("GEMINI_API_KEY", "api_key_t2")
    mock_env.setenv("STANDARD_OUTPUT_TEMPLATE_PATH", "/env/std.txt")
    mock_env.setenv("MINIMAL_OUTPUT_TEMPLATE_PATH", "/env/min.txt")

    config = load_config()

    assert isinstance(config, AppConfig)
    assert config.standard_output_template_path == "/env/std.txt"
    assert config.minimal_output_template_path == "/env/min.txt"


@patch("git_auto.src.config.subprocess.run")
def test_load_config_template_paths_env_override(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_t3")
    mock_env.setenv("STANDARD_OUTPUT_TEMPLATE_PATH", "/env/override.txt")

    file_data = {
        "standard_output_template_path": "/file/ignored.txt",
        "minimal_output_template_path": "/file/min.txt",
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.standard_output_template_path == "/env/override.txt"  # Env wins
    assert config.minimal_output_template_path == "/file/min.txt"  # From file


@patch("git_auto.src.config.subprocess.run")
def test_load_config_gen_params_from_file(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    """Test loading generation params (temp, top_p, top_k, max_tokens) from file."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_gen1")
    file_data = {
        "generation_config_validation": {
            "temperature": 0.11,
            "top_p": 0.88,
            "max_output_tokens": 1111,
        },
        "generation_config_commit": {
            "temperature": 0.22,
            "top_k": 22,
            "max_output_tokens": 222,
        },
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    # Validation config
    assert config.generation_config_validation.temperature == 0.11
    assert config.generation_config_validation.top_p == 0.88
    assert config.generation_config_validation.top_k == 40  # Default
    assert config.generation_config_validation.max_output_tokens == 1111
    # Commit config
    assert config.generation_config_commit.temperature == 0.22
    assert config.generation_config_commit.top_p == 0.95  # Default
    assert config.generation_config_commit.top_k == 22
    assert config.generation_config_commit.max_output_tokens == 222


@patch("git_auto.src.config.subprocess.run")
def test_load_config_gen_params_env_override(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    """Test environment variables override file settings for generation params."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_gen2")
    # Env overrides for validation
    mock_env.setenv("VALIDATION_TEMP", "0.15")
    mock_env.setenv("VALIDATION_TOP_K", "35")
    # Env overrides for commit
    mock_env.setenv("COMMIT_TOP_P", "0.77")
    mock_env.setenv("COMMIT_MAX_TOKENS", "333")

    file_data = {
        "generation_config_validation": {
            "temperature": 0.11,  # Overridden by env
            "top_p": 0.88,  # Not overridden
            "top_k": 99,  # Overridden by env
            "max_output_tokens": 1111,  # Not overridden
        },
        "generation_config_commit": {
            "temperature": 0.22,  # Not overridden
            "top_p": 0.66,  # Overridden by env
            "top_k": 22,  # Not overridden
            "max_output_tokens": 222,  # Overridden by env
        },
    }
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    # Validation config
    assert config.generation_config_validation.temperature == 0.15  # Env
    assert config.generation_config_validation.top_p == 0.88  # File
    assert config.generation_config_validation.top_k == 35  # Env
    assert config.generation_config_validation.max_output_tokens == 1111  # File
    # Commit config
    assert config.generation_config_commit.temperature == 0.22  # File
    assert config.generation_config_commit.top_p == 0.77  # Env
    assert config.generation_config_commit.top_k == 22  # File
    assert config.generation_config_commit.max_output_tokens == 333  # Env


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_custom_literals_file(
    mock_subproc_run, tmp_path, mock_env, mock_yaml, temp_literals_file
):
    """Test loading custom literals file path from config."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_lit1")
    literals_content = "MyProjectName\nInternalURL"
    literals_path = temp_literals_file(literals_content)

    file_data = {"infuscation_literals_file": str(literals_path)}
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.infuscation_literals_file == str(literals_path)
    assert config.custom_infuscation_literals == [
        "MyProjectName",
        "InternalURL",
    ]  # Check loaded literals


@patch("git_auto.src.config.subprocess.run")
def test_load_config_with_custom_literals_env_override(
    mock_subproc_run, tmp_path, mock_env, mock_yaml, temp_literals_file
):
    """Test env var override for custom literals file path."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_lit2")
    literals_content_env = "EnvLiteral"
    literals_path_env = temp_literals_file(literals_content_env)
    mock_env.setenv("INFUSCATION_LITERALS_FILE", str(literals_path_env))

    file_data = {"infuscation_literals_file": "/ignored/path.txt"}
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.infuscation_literals_file == str(literals_path_env)
    assert config.custom_infuscation_literals == ["EnvLiteral"]


@patch("git_auto.src.config.subprocess.run")
def test_load_config_model_from_file(mock_subproc_run, tmp_path, mock_env, mock_yaml):
    """Test loading the AI model name from the config file."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_model1")
    file_data = {"model": "gemini-1.5-pro-latest"}
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.model == "gemini-1.5-pro-latest"


@patch("git_auto.src.config.subprocess.run")
def test_load_config_model_env_override(
    mock_subproc_run, tmp_path, mock_env, mock_yaml
):
    """Test that the MODEL environment variable overrides the config file."""
    mock_subproc_run.return_value = MagicMock(returncode=0, stdout=str(tmp_path))
    mock_env.setenv("GEMINI_API_KEY", "api_key_model2")
    mock_env.setenv("MODEL", "gemini-ultra-latest")  # Env var override

    file_data = {"model": "gemini-1.5-pro-latest"}  # From file
    config_file = temp_config_file(tmp_path, yaml.dump(file_data))
    mock_yaml.safe_load.return_value = file_data

    with patch("git_auto.src.config.find_config_file", return_value=config_file):
        config = load_config()

    assert isinstance(config, AppConfig)
    assert config.model == "gemini-ultra-latest"  # Env var should win
