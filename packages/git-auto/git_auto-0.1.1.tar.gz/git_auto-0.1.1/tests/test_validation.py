import pytest
import subprocess
import logging  # Import logging for caplog
import toml  # Import toml for mocking errors
from unittest.mock import MagicMock, patch

from git_auto.src.validation import (
    check_syntax_errors,
    check_unsupported_chars,
    is_binary_file,
)

# --- Fixtures ---


@pytest.fixture
def mock_files_valid():
    return {
        "valid.py": {"content": "print('hello')", "extension": ".py"},
        "valid.json": {"content": '{"key": "value"}', "extension": ".json"},
        "valid.yaml": {"content": "key: value\nlist:\n  - item1", "extension": ".yaml"},
    }


@pytest.fixture
def mock_files_invalid():
    return {
        "invalid.py": {
            "content": "print 'hello'",
            "extension": ".py",
        },  # Python 2 syntax
        "invalid.json": {
            "content": '{"key": "value",}',
            "extension": ".json",
        },  # Trailing comma
        "invalid.yaml": {
            "content": "key: value\nlist: item1",
            "extension": ".yaml",
        },  # Indentation error
    }


@pytest.fixture
def mock_files_chars():
    return {
        "control_chars.txt": {"content": "Hello\x00World", "extension": ".txt"},
        "bom.py": {"content": "\ufeffprint('hello')", "extension": ".py"},
    }


@pytest.fixture
def mock_files_js():
    return {"script.js": {"content": "console.log('hello');", "extension": ".js"}}


@pytest.fixture
def mock_files_yaml():
    return {"config.yaml": {"content": "key: value", "extension": ".yaml"}}


@pytest.fixture
def mock_files_yaml_multi_doc():
    return {
        "multi.yaml": {
            "content": """
apiVersion: v1
kind: Service
metadata:
  name: service1
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment1
""",
            "extension": ".yaml",
        }
    }


@pytest.fixture
def mock_files_yaml_multi_doc_invalid():
    return {
        "multi_invalid.yaml": {
            "content": """
apiVersion: v1
kind: Service
---
apiVersion: apps/v1
kind: Deployment
  bad: indent
""",
            "extension": ".yaml",
        }
    }


@pytest.fixture
def mock_files_dockerfile_good():
    return {
        "Dockerfile": {
            "content": """
FROM python:3.9-slim
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
""",
            "extension": "",  # Test filename matching
        }
    }


@pytest.fixture
def mock_files_dockerfile_bad():
    return {
        "Dockerfile.prod": {
            "content": """
FROM ubuntu:latest
RUN apt-get update
ADD https://example.com/script.sh /tmp/
RUN chmod +x /tmp/script.sh && /tmp/script.sh
""",
            "extension": ".prod",  # Test extension matching
        }
    }


@pytest.fixture
def mock_files_shell_good():
    return {
        "script.sh": {
            "content": """
#!/bin/bash
set -euo pipefail

echo "Hello world"
RESULT=$(ls -l)
echo "$RESULT"
""",
            "extension": ".sh",
        }
    }


@pytest.fixture
def mock_files_shell_bad():
    return {
        "script.sh": {
            "content": """
#!/bin/sh
# Missing set -euo pipefail

echo "Processing..."
OUTPUT=`pwd` # Uses backticks
echo "Current dir: $OUTPUT"
""",
            "extension": ".sh",
        }
    }


@pytest.fixture
def mock_files_toml_good():
    return {
        "config.toml": {"content": '[section]\nkey = "value"\n', "extension": ".toml"}
    }


@pytest.fixture
def mock_files_toml_bad():
    return {"bad.toml": {"content": '[section\nkey = "value"\n', "extension": ".toml"}}


@pytest.fixture
def mock_files_pyproject_good():
    return {
        "pyproject.toml": {
            "content": """
[build-system]
requires = ["setuptools"]
build-backend = "setuptools.build_meta"

[project]
name = "my-package"
version = "0.1.0"
""",
            "extension": ".toml",
        }
    }


@pytest.fixture
def mock_files_pyproject_bad():
    return {
        "pyproject.toml": {
            "content": """
# Missing [project] table
[build-system]
requires = ["setuptools"]
""",
            "extension": ".toml",
        }
    }


@pytest.fixture
def mock_files_pyproject_missing_name():
    return {
        "pyproject.toml": {
            "content": """
[build-system]
requires = ["setuptools"]

[project]
# Missing name key
version = "0.1.0"
""",
            "extension": ".toml",
        }
    }


@pytest.fixture
def mock_files_req_good():
    return {
        "requirements.txt": {
            "content": """
# This is a comment
click==8.0.0
requests>=2.20
# another comment

-e git+https://github.com/user/repo.git#egg=editable
./local/package
""",
            "extension": ".txt",
        }
    }


@pytest.fixture
def mock_files_req_bad():
    return {
        "requirements-dev.txt": {
            "content": """
pytest # Unpinned
flake8==5.0
requests # Unpinned
""",
            "extension": ".txt",
        }
    }


@pytest.fixture
def mock_files_pkgjson_good():
    return {
        "package.json": {
            "content": '{"name": "my-app", "version": "1.0.0", "main": "index.js"}',
            "extension": ".json",
        }
    }


@pytest.fixture
def mock_files_pkgjson_missing_name():
    return {"package.json": {"content": '{"version": "1.0.0"}', "extension": ".json"}}


@pytest.fixture
def mock_files_pkgjson_missing_version():
    return {"package.json": {"content": '{"name": "my-app"}', "extension": ".json"}}


@pytest.fixture
def mock_files_pkgjson_not_object():
    return {
        "package.json": {
            "content": '["name", "version"]',  # JSON array, not object
            "extension": ".json",
        }
    }


@pytest.fixture
def mock_files_non_ascii():
    return {
        "cyrillic.yaml": {
            "content": "key: value\nrepo: pоdinfо # Cyrillic 'о'",
            "extension": ".yaml",
        },
        "mixed_chars.txt": {
            "content": "Hello © World™",  # Copyright and TM symbols
            "extension": ".txt",
        },
    }


# --- Tests for is_binary_file (Example) ---


def test_is_binary_file_true():
    assert is_binary_file("Hello\x00World") == True


def test_is_binary_file_false():
    assert is_binary_file("Hello World\nThis is text.") == False


# --- Tests for check_syntax_errors ---


@patch("git_auto.src.validation.subprocess.run")
@patch(
    "git_auto.src.validation.shutil.which", return_value="/usr/bin/node"
)  # Assume node exists
@patch("git_auto.src.validation.yaml", MagicMock())  # Assume PyYAML is installed
@patch(
    "git_auto.src.validation._YAMLLINT_AVAILABLE", False
)  # Assume yamllint is NOT installed initially
def test_check_syntax_errors_valid(mock_which, mock_run, mock_files_valid):
    """Test syntax check with valid files."""
    # Mock subprocess.run to always return success (returncode 0)
    mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
    issues = check_syntax_errors(mock_files_valid)
    assert not issues  # No issues should be found


@patch("git_auto.src.validation.subprocess.run")
@patch("git_auto.src.validation.shutil.which", return_value="/usr/bin/node")
@patch("git_auto.src.validation.yaml", MagicMock())
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_errors_invalid_py(mock_which, mock_run, mock_files_invalid):
    """Test syntax check with invalid Python."""
    # Mock subprocess.run for Python check to return an error
    mock_run.return_value = MagicMock(
        returncode=1, stdout="", stderr="SyntaxError: invalid syntax"
    )
    issues = check_syntax_errors({"invalid.py": mock_files_invalid["invalid.py"]})
    assert len(issues) == 1
    assert issues[0]["file"] == "invalid.py"
    assert "Python syntax error" in issues[0]["error"]


@patch("git_auto.src.validation.subprocess.run")
@patch("git_auto.src.validation.shutil.which", return_value="/usr/bin/node")
@patch("git_auto.src.validation.yaml", MagicMock())  # Mock PyYAML
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_errors_invalid_json(mock_which, mock_run, mock_files_invalid):
    """Test syntax check with invalid JSON."""
    issues = check_syntax_errors({"invalid.json": mock_files_invalid["invalid.json"]})
    assert len(issues) == 1
    assert issues[0]["file"] == "invalid.json"
    assert "JSON syntax error" in issues[0]["error"]


@patch("git_auto.src.validation.subprocess.run")
@patch("git_auto.src.validation.shutil.which", return_value="/usr/bin/node")
@patch("git_auto.src.validation.yaml")  # Mock PyYAML module
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_errors_invalid_yaml(
    mock_yaml, mock_which, mock_run, mock_files_invalid
):
    """Test syntax check with invalid YAML (using PyYAML mock)."""
    # Mock yaml.safe_load to raise an error
    mock_yaml.safe_load.side_effect = yaml.YAMLError(
        "mapping values are not allowed here"
    )
    mock_yaml.YAMLError = yaml.YAMLError  # Ensure the exception type is available

    issues = check_syntax_errors({"invalid.yaml": mock_files_invalid["invalid.yaml"]})

    assert len(issues) == 1
    assert issues[0]["file"] == "invalid.yaml"
    assert "YAML syntax error" in issues[0]["error"]
    assert "mapping values are not allowed here" in issues[0]["error"]


@patch("git_auto.src.validation.subprocess.run")
@patch(
    "git_auto.src.validation.shutil.which", return_value=None
)  # Mock node as NOT found
@patch("git_auto.src.validation.yaml", MagicMock())
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_skip_js_no_node(mock_which, mock_run, mock_files_js, caplog):
    """Test that JS check is skipped and logged if node is not found."""
    caplog.set_level(logging.DEBUG)  # Ensure debug messages are captured
    issues = check_syntax_errors(mock_files_js)
    assert not issues  # No syntax errors reported
    mock_run.assert_not_called()  # Subprocess should not be called for node check
    # Check for the specific debug log message
    assert (
        "Node.js not found in PATH, skipping syntax check for script.js" in caplog.text
    )


@patch("git_auto.src.validation.subprocess.run")
@patch("git_auto.src.validation.shutil.which")  # Mock which generally
@patch("git_auto.src.validation.yaml", MagicMock())
@patch(
    "git_auto.src.validation._YAMLLINT_AVAILABLE", False
)  # Mock yamllint as NOT available
def test_check_syntax_skip_yamllint_not_available(
    mock_available, mock_which, mock_run, mock_files_yaml, caplog
):
    """Test that yamllint check is skipped and logged if not available."""
    caplog.set_level(logging.DEBUG)
    # Mock PyYAML check passing
    mock_yaml.safe_load = MagicMock()

    issues = check_syntax_errors(mock_files_yaml)

    assert not issues  # No syntax errors reported (basic YAML check passes)
    # Ensure yamllint subprocess was not called
    assert not any(call.args[0][0] == "yamllint" for call in mock_run.call_args_list)
    # Check for the specific debug log message
    assert (
        "yamllint not found in PATH, skipping advanced YAML linting for config.yaml"
        in caplog.text
    )


@patch("git_auto.src.validation.subprocess.run")
@patch("git_auto.src.validation.shutil.which")
@patch("git_auto.src.validation.yaml", None)  # Mock PyYAML as NOT installed
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_skip_yaml_no_pyyaml(
    mock_available, mock_yaml, mock_which, mock_run, mock_files_yaml, caplog
):
    """Test that YAML check is skipped and logged if PyYAML is not installed."""
    caplog.set_level(logging.DEBUG)
    issues = check_syntax_errors(mock_files_yaml)
    assert not issues  # No errors reported
    # Check for the specific debug log message
    assert (
        "PyYAML not installed, skipping YAML syntax check for config.yaml"
        in caplog.text
    )


@patch("git_auto.src.validation.yaml", MagicMock())
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_yaml_multi_doc_good(
    mock_available, mock_yaml, mock_files_yaml_multi_doc
):
    """Test validation of a valid multi-document YAML file."""
    # Simulate safe_load_all yielding multiple documents
    mock_yaml.safe_load_all.return_value = [
        {"apiVersion": "v1"},
        {"apiVersion": "apps/v1"},
    ]
    issues = check_syntax_errors(mock_files_yaml_multi_doc)
    assert not issues
    mock_yaml.safe_load_all.assert_called_once()


@patch("git_auto.src.validation.yaml", MagicMock())
@patch("git_auto.src.validation._YAMLLINT_AVAILABLE", False)
def test_check_syntax_yaml_multi_doc_invalid(
    mock_available, mock_yaml, mock_files_yaml_multi_doc_invalid
):
    """Test validation of a multi-document YAML file with an error in one document."""
    # Simulate safe_load_all raising an error during iteration
    mock_yaml.safe_load_all.side_effect = yaml.YAMLError("parsing failed in second doc")
    mock_yaml.YAMLError = yaml.YAMLError

    issues = check_syntax_errors(mock_files_yaml_multi_doc_invalid)
    assert len(issues) == 1
    assert issues[0]["file"] == "multi_invalid.yaml"
    assert "YAML syntax error" in issues[0]["error"]
    assert "parsing failed in second doc" in issues[0]["error"]
    mock_yaml.safe_load_all.assert_called_once()


# --- Tests for Dockerfile Validation ---


def test_check_syntax_dockerfile_good(mock_files_dockerfile_good):
    """Test Dockerfile with no basic issues."""
    issues = check_syntax_errors(mock_files_dockerfile_good)
    assert not issues


def test_check_syntax_dockerfile_bad(mock_files_dockerfile_bad):
    """Test Dockerfile with multiple basic issues."""
    issues = check_syntax_errors(mock_files_dockerfile_bad)
    assert len(issues) == 3
    errors = [issue["error"] for issue in issues]
    assert any("apt-get update' without subsequent 'rm -rf" in e for e in errors)
    assert any("Base image uses 'latest' tag" in e for e in errors)
    assert any("Found 'ADD' with a URL" in e for e in errors)


def test_check_syntax_dockerfile_apt_ok(tmp_path):
    """Test Dockerfile with correct apt-get update/clean pattern."""
    content = "FROM debian\nRUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*"
    files = {"Dockerfile": {"content": content, "extension": ""}}
    issues = check_syntax_errors(files)
    assert not any("apt-get update" in issue["error"] for issue in issues)


def test_check_syntax_dockerfile_no_latest(tmp_path):
    """Test Dockerfile without latest tag."""
    content = "FROM ubuntu:22.04\nRUN echo hello"
    files = {"Dockerfile": {"content": content, "extension": ""}}
    issues = check_syntax_errors(files)
    assert not any("latest' tag" in issue["error"] for issue in issues)


def test_check_syntax_dockerfile_add_local(tmp_path):
    """Test Dockerfile with ADD for local files (should be ok)."""
    content = "FROM scratch\nADD ./local_file /app/"
    files = {"Dockerfile": {"content": content, "extension": ""}}
    issues = check_syntax_errors(files)
    assert not any("'ADD' with a URL" in issue["error"] for issue in issues)


# --- Tests for Shell Script Validation ---


def test_check_syntax_shell_good(mock_files_shell_good):
    """Test shell script with no basic issues."""
    issues = check_syntax_errors(mock_files_shell_good)
    assert not issues


def test_check_syntax_shell_bad(mock_files_shell_bad):
    """Test shell script with missing set options and backticks."""
    issues = check_syntax_errors(mock_files_shell_bad)
    assert len(issues) == 2
    errors = [issue["error"] for issue in issues]
    assert any(
        "Consider adding `set -e', `set -u', `set -o pipefail`" in e for e in errors
    )
    assert any("Found deprecated backticks ``" in e for e in errors)


def test_check_syntax_shell_missing_some_set(tmp_path):
    """Test shell script missing only some set options."""
    content = "#!/bin/bash\nset -e\nset -o pipefail\necho hello"
    files = {"script.sh": {"content": content, "extension": ".sh"}}
    issues = check_syntax_errors(files)
    assert len(issues) == 1
    assert "Consider adding `set -u`" in issues[0]["error"]


def test_check_syntax_shell_no_backticks(tmp_path):
    """Test shell script using $() instead of backticks."""
    content = "#!/bin/bash\nset -euo pipefail\nRESULT=$(pwd)\necho $RESULT"
    files = {"script.sh": {"content": content, "extension": ".sh"}}
    issues = check_syntax_errors(files)
    assert not any("backticks" in issue["error"] for issue in issues)


@patch(
    "git_auto.src.validation.shutil.which"
)  # Mock which to control tool availability
@patch("git_auto.src.validation.subprocess.run")  # Mock subprocess
def test_check_syntax_shell_with_shellcheck_issues(
    mock_run, mock_which, mock_files_shell_bad
):
    """Test shell script validation using shellcheck when it finds issues."""
    # Simulate shellcheck being available
    mock_which.side_effect = (
        lambda cmd: "/usr/bin/shellcheck" if cmd == "shellcheck" else None
    )
    # Simulate shellcheck JSON output with issues
    shellcheck_output = json.dumps(
        [
            {
                "file": "-",
                "line": 5,
                "column": 1,
                "level": "warning",
                "code": 2034,
                "message": "OUTPUT appears unused...",
            },
            {
                "file": "-",
                "line": 6,
                "column": 1,
                "level": "style",
                "code": 2006,
                "message": "Use $(...) instead...",
            },  # Style issue, should be ignored by current logic
        ]
    )
    mock_run.return_value = MagicMock(returncode=0, stdout=shellcheck_output, stderr="")

    issues = check_syntax_errors(mock_files_shell_bad)

    assert len(issues) == 1  # Only the warning should be reported
    assert (
        "Shellcheck (warning SC2034 L5:C1): OUTPUT appears unused..."
        in issues[0]["error"]
    )
    mock_run.assert_called_once_with(
        ["shellcheck", "-f", "json", mock.ANY],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("git_auto.src.validation.shutil.which")
@patch("git_auto.src.validation.subprocess.run")
def test_check_syntax_shell_with_shellcheck_no_issues(
    mock_run, mock_which, mock_files_shell_good
):
    """Test shell script validation using shellcheck when it finds no issues."""
    mock_which.side_effect = (
        lambda cmd: "/usr/bin/shellcheck" if cmd == "shellcheck" else None
    )
    # Simulate empty JSON output (no issues)
    mock_run.return_value = MagicMock(returncode=0, stdout="[]", stderr="")

    issues = check_syntax_errors(mock_files_shell_good)
    assert not issues
    mock_run.assert_called_once_with(
        ["shellcheck", "-f", "json", mock.ANY],
        capture_output=True,
        text=True,
        check=False,
    )


@patch("git_auto.src.validation.shutil.which")
@patch("git_auto.src.validation.subprocess.run")
def test_check_syntax_shell_shellcheck_execution_error(
    mock_run, mock_which, mock_files_shell_good
):
    """Test handling when shellcheck command itself fails."""
    mock_which.side_effect = (
        lambda cmd: "/usr/bin/shellcheck" if cmd == "shellcheck" else None
    )
    # Simulate shellcheck failing
    mock_run.return_value = MagicMock(
        returncode=1, stdout="", stderr="Internal shellcheck error"
    )

    issues = check_syntax_errors(mock_files_shell_good)
    assert len(issues) == 1
    assert "Shellcheck execution error: Internal shellcheck error" in issues[0]["error"]


@patch("git_auto.src.validation.shutil.which")  # Mock which
@patch("git_auto.src.validation.subprocess.run")  # Mock subprocess run
def test_check_syntax_shell_no_shellcheck_fallback(
    mock_run, mock_which, mock_files_shell_bad, caplog
):
    """Test fallback to regex checks when shellcheck is not available."""
    caplog.set_level(logging.DEBUG)
    # Simulate shellcheck NOT being available
    mock_which.side_effect = lambda cmd: None

    issues = check_syntax_errors(mock_files_shell_bad)

    # Check that subprocess.run was NOT called for shellcheck
    assert not any(call.args[0][0] == "shellcheck" for call in mock_run.call_args_list)
    # Check that the fallback regex issues are reported
    assert len(issues) == 2
    errors = [issue["error"] for issue in issues]
    assert any(
        "Consider adding `set -e', `set -u', `set -o pipefail`" in e for e in errors
    )
    assert any("Found deprecated backticks ``" in e for e in errors)
    # Check for the debug log message indicating fallback
    assert "shellcheck not found, performing basic checks for script.sh" in caplog.text


def test_check_syntax_shell_good_regex_only(mock_files_shell_good):
    """Test shell script with no basic issues using only regex (simulate no shellcheck)."""
    with patch("git_auto.src.validation._SHELLCHECK_AVAILABLE", False):
        issues = check_syntax_errors(mock_files_shell_good)
        assert not issues


def test_check_syntax_shell_bad_regex_only(mock_files_shell_bad):
    """Test shell script with issues using only regex (simulate no shellcheck)."""
    with patch("git_auto.src.validation._SHELLCHECK_AVAILABLE", False):
        issues = check_syntax_errors(mock_files_shell_bad)
        assert len(issues) == 2
        errors = [issue["error"] for issue in issues]
        assert any(
            "Consider adding `set -e', `set -u', `set -o pipefail`" in e for e in errors
        )
        assert any("Found deprecated backticks ``" in e for e in errors)


# --- Tests for TOML / pyproject.toml Validation ---


@patch("git_auto.src.validation.toml", MagicMock())  # Assume toml is installed
def test_check_syntax_toml_good(mock_toml, mock_files_toml_good):
    """Test validation of a syntactically correct TOML file."""
    mock_toml.loads.return_value = {
        "section": {"key": "value"}
    }  # Simulate successful parse
    issues = check_syntax_errors(mock_files_toml_good)
    assert not issues
    mock_toml.loads.assert_called_once()


@patch("git_auto.src.validation.toml", MagicMock())  # Assume toml is installed
def test_check_syntax_toml_bad(mock_toml, mock_files_toml_bad):
    """Test validation of a TOML file with syntax errors."""
    # Simulate TomlDecodeError during parsing
    mock_toml.loads.side_effect = toml.TomlDecodeError("Syntax error", "doc", 0)
    mock_toml.TomlDecodeError = toml.TomlDecodeError  # Make exception type available

    issues = check_syntax_errors(mock_files_toml_bad)
    assert len(issues) == 1
    assert issues[0]["file"] == "bad.toml"
    assert "TOML syntax error" in issues[0]["error"]


@patch("git_auto.src.validation.toml", MagicMock())
def test_check_syntax_pyproject_good(mock_toml, mock_files_pyproject_good):
    """Test validation of a valid pyproject.toml."""
    # Simulate successful parse with expected structure
    mock_toml.loads.return_value = {
        "build-system": {"requires": ["setuptools"], "build-backend": "..."},
        "project": {"name": "my-package", "version": "0.1.0"},
    }
    issues = check_syntax_errors(mock_files_pyproject_good)
    assert not issues
    mock_toml.loads.assert_called_once()


@patch("git_auto.src.validation.toml", MagicMock())
def test_check_syntax_pyproject_bad(mock_toml, mock_files_pyproject_bad):
    """Test validation of pyproject.toml missing [project] table."""
    # Simulate parse result missing the project table
    mock_toml.loads.return_value = {"build-system": {"requires": ["setuptools"]}}
    issues = check_syntax_errors(mock_files_pyproject_bad)
    assert len(issues) == 1
    assert issues[0]["file"] == "pyproject.toml"
    assert "Missing required [project] table" in issues[0]["error"]


@patch("git_auto.src.validation.toml", MagicMock())
def test_check_syntax_pyproject_missing_name(
    mock_toml, mock_files_pyproject_missing_name
):
    """Test validation of pyproject.toml missing project.name key."""
    # Simulate parse result missing the name key
    mock_toml.loads.return_value = {
        "build-system": {"requires": ["setuptools"]},
        "project": {"version": "0.1.0"},
    }
    issues = check_syntax_errors(mock_files_pyproject_missing_name)
    assert len(issues) == 1
    assert issues[0]["file"] == "pyproject.toml"
    assert "Missing required 'name' key in [project] table" in issues[0]["error"]


@patch("git_auto.src.validation.toml", None)  # Simulate toml library NOT installed
def test_check_syntax_toml_no_library(mock_files_toml_good, caplog):
    """Test that TOML check is skipped and logged if library is not installed."""
    caplog.set_level(logging.DEBUG)
    issues = check_syntax_errors(mock_files_toml_good)
    assert not issues  # No errors reported
    assert (
        "toml library not installed, skipping TOML validation for config.toml"
        in caplog.text
    )


# --- Tests for requirements.txt Validation ---


def test_check_syntax_requirements_good(mock_files_req_good):
    """Test requirements file with pinned, commented, or editable deps."""
    issues = check_syntax_errors(mock_files_req_good)
    assert not issues


def test_check_syntax_requirements_bad(mock_files_req_bad):
    """Test requirements file with unpinned dependencies."""
    issues = check_syntax_errors(mock_files_req_bad)
    assert len(issues) == 2
    errors = [issue["error"] for issue in issues]
    assert any("Potentially unpinned dependency 'pytest'" in e for e in errors)
    assert any("Potentially unpinned dependency 'requests'" in e for e in errors)
    assert not any("flake8" in e for e in errors)


def test_check_syntax_requirements_mixed(tmp_path):
    """Test requirements file with a mix of pinned and unpinned."""
    content = "click==8.0\nrequests\n# pytest==7.0\nflake8>=5"
    files = {"requirements.txt": {"content": content, "extension": ".txt"}}
    issues = check_syntax_errors(files)
    assert len(issues) == 1
    assert "Potentially unpinned dependency 'requests'" in issues[0]["error"]


# --- Tests for JSON / package.json Validation ---


def test_check_syntax_json_good(mock_files_valid):
    """Test validation of a generic valid JSON file."""
    issues = check_syntax_errors({"valid.json": mock_files_valid["valid.json"]})
    assert not issues


def test_check_syntax_json_bad(mock_files_invalid):
    """Test validation of a generic invalid JSON file."""
    issues = check_syntax_errors({"invalid.json": mock_files_invalid["invalid.json"]})
    assert len(issues) == 1
    assert issues[0]["file"] == "invalid.json"
    assert "JSON syntax error" in issues[0]["error"]


def test_check_syntax_pkgjson_good(mock_files_pkgjson_good):
    """Test validation of a valid package.json file."""
    issues = check_syntax_errors(mock_files_pkgjson_good)
    assert not issues


def test_check_syntax_pkgjson_missing_name(mock_files_pkgjson_missing_name):
    """Test package.json missing the name field."""
    issues = check_syntax_errors(mock_files_pkgjson_missing_name)
    assert len(issues) == 1
    assert issues[0]["file"] == "package.json"
    assert "Missing required 'name' field" in issues[0]["error"]


def test_check_syntax_pkgjson_missing_version(mock_files_pkgjson_missing_version):
    """Test package.json missing the version field."""
    issues = check_syntax_errors(mock_files_pkgjson_missing_version)
    assert len(issues) == 1
    assert issues[0]["file"] == "package.json"
    assert "Missing required 'version' field" in issues[0]["error"]


def test_check_syntax_pkgjson_not_object(mock_files_pkgjson_not_object):
    """Test package.json where the root is not a JSON object."""
    issues = check_syntax_errors(mock_files_pkgjson_not_object)
    # It should report the specific package.json error first
    assert len(issues) == 1
    assert issues[0]["file"] == "package.json"
    assert "Root element is not an object" in issues[0]["error"]


# --- Tests for check_unsupported_chars ---


def test_check_unsupported_chars_control(mock_files_chars):
    """Test detection of control characters."""
    issues = check_unsupported_chars(
        {"control_chars.txt": mock_files_chars["control_chars.txt"]}
    )
    assert len(issues) == 1
    assert issues[0]["file"] == "control_chars.txt"
    assert "U+0000" in issues[0]["error"]  # Null byte


def test_check_unsupported_chars_bom(mock_files_chars):
    """Test detection of UTF-8 BOM."""
    issues = check_unsupported_chars({"bom.py": mock_files_chars["bom.py"]})
    assert len(issues) == 1
    assert issues[0]["file"] == "bom.py"
    assert "UTF-8 BOM marker" in issues[0]["error"]


def test_check_unsupported_chars_clean(mock_files_valid):
    """Test clean files have no unsupported char issues."""
    issues = check_unsupported_chars(mock_files_valid)
    assert not issues


def test_check_unsupported_chars_non_ascii(mock_files_non_ascii):
    """Test detection of non-ASCII printable characters."""
    issues = check_unsupported_chars(mock_files_non_ascii)
    assert len(issues) == 2  # One for each file

    cyrillic_issue = next((i for i in issues if i["file"] == "cyrillic.yaml"), None)
    mixed_issue = next((i for i in issues if i["file"] == "mixed_chars.txt"), None)

    assert cyrillic_issue is not None
    assert "CRITICAL: Found non-ASCII characters" in cyrillic_issue["error"]
    assert "'о'" in cyrillic_issue["error"]  # Check the specific char
    assert "U+043E" in cyrillic_issue["error"]  # Check the code point

    assert mixed_issue is not None
    assert "CRITICAL: Found non-ASCII characters" in mixed_issue["error"]
    assert "'©™'" in mixed_issue["error"]  # Check specific chars
    assert "U+00A9" in mixed_issue["error"]
    assert "U+2122" in mixed_issue["error"]
