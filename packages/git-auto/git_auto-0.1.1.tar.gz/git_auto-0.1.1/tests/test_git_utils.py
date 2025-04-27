import pytest
import subprocess
from unittest.mock import patch, MagicMock

# Update import paths
from git_auto.src.git_utils import (
    get_git_diff,
    get_modified_files,
    check_git_repo,
)
from git_auto.src.validation import is_binary_file

# --- Mocks for subprocess ---


@pytest.fixture
def mock_subprocess_run():
    # Update patch path
    with patch("git_auto.src.git_utils.subprocess.run") as mock_run:
        yield mock_run


# --- Tests for check_git_repo ---


def test_check_git_repo_success(mock_subprocess_run):
    """Test check_git_repo when inside a git repository."""
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout="true\n", stderr=""
    )
    # check_git_repo doesn't return anything, just shouldn't raise
    try:
        check_git_repo()
    except RuntimeError:
        pytest.fail("check_git_repo raised RuntimeError unexpectedly")


def test_check_git_repo_failure(mock_subprocess_run):
    """Test check_git_repo when not inside a git repository."""
    # Simulate CalledProcessError by raising it when the mock is called
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        1, ["git", "rev-parse"]
    )
    with pytest.raises(RuntimeError, match="Not a git repository."):
        check_git_repo()


# --- Tests for get_git_diff ---


def test_get_git_diff_success(mock_subprocess_run):
    """Test get_git_diff with successful git diff command."""
    diff_content = "diff --git a/file.txt b/file.txt\n--- a/file.txt\n+++ b/file.txt\n@@ -1 +1 @@\n-old\n+new"
    mock_subprocess_run.return_value = MagicMock(
        returncode=0, stdout=diff_content, stderr=""
    )
    result = get_git_diff()
    assert result == diff_content
    mock_subprocess_run.assert_called_once_with(
        ["git", "diff", "--staged"], capture_output=True, text=True
    )


def test_get_git_diff_failure(mock_subprocess_run):
    """Test get_git_diff when git diff command fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, ["git", "diff"])
    with pytest.raises(RuntimeError, match="Failed to get git diff"):
        get_git_diff()


# --- Tests for get_modified_files ---


# Update patch path
@patch(
    "git_auto.src.git_utils.is_binary_file", return_value=False
)  # Assume text files unless specified
def test_get_modified_files_success(mock_is_binary, mock_subprocess_run):
    """Test get_modified_files with various file statuses."""
    name_status_output = (
        "M\tfile1.py\n"
        "A\tnew_file.txt\n"
        "R\trenamed_file.js\toriginal_name.js\n"  # Handle rename status
        "D\tdeleted_file.css\n"  # Should be skipped
    )
    file1_content = "print('modified')"
    new_file_content = "Hello there"
    renamed_content = "console.log('renamed');"

    # Configure mock responses for different calls
    def subprocess_side_effect(*args, **kwargs):
        cmd = args[0]
        if cmd == ["git", "diff", "--staged", "--name-status"]:
            return MagicMock(
                returncode=0, stdout=name_status_output, stderr="", check=True
            )
        elif cmd == ["git", "show", ":file1.py"]:
            return MagicMock(
                returncode=0, stdout=file1_content.encode("utf-8"), check=True
            )
        elif cmd == ["git", "show", ":new_file.txt"]:
            return MagicMock(
                returncode=0, stdout=new_file_content.encode("utf-8"), check=True
            )
        elif cmd == ["git", "show", ":renamed_file.js"]:
            return MagicMock(
                returncode=0, stdout=renamed_content.encode("utf-8"), check=True
            )
        else:
            # Raise an error for unexpected calls
            raise subprocess.CalledProcessError(
                1, cmd, output=b"Unexpected command", stderr=b"Error"
            )

    mock_subprocess_run.side_effect = subprocess_side_effect

    result = get_modified_files()

    assert "file1.py" in result
    assert result["file1.py"]["content"] == file1_content
    assert result["file1.py"]["extension"] == ".py"
    assert result["file1.py"]["status"] == "M"

    assert "new_file.txt" in result
    assert result["new_file.txt"]["content"] == new_file_content
    assert result["new_file.txt"]["extension"] == ".txt"
    assert result["new_file.txt"]["status"] == "A"

    assert "renamed_file.js" in result
    assert result["renamed_file.js"]["content"] == renamed_content
    assert result["renamed_file.js"]["extension"] == ".js"
    assert result["renamed_file.js"]["status"] == "R"

    assert "deleted_file.css" not in result  # Deleted files are skipped
    assert (
        "original_name.js" not in result
    )  # Original name of renamed file shouldn't be a key


# Update patch path
@patch(
    "git_auto.src.git_utils.is_binary_file", return_value=True
)  # Simulate binary file
def test_get_modified_files_binary(mock_is_binary, mock_subprocess_run):
    """Test get_modified_files with a binary file."""
    name_status_output = "A\timage.png"
    binary_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01"  # Sample PNG header

    def subprocess_side_effect(*args, **kwargs):
        cmd = args[0]
        if cmd == ["git", "diff", "--staged", "--name-status"]:
            return MagicMock(
                returncode=0, stdout=name_status_output, stderr="", check=True
            )
        elif cmd == ["git", "show", ":image.png"]:
            return MagicMock(returncode=0, stdout=binary_content, check=True)
        else:
            raise subprocess.CalledProcessError(1, cmd)

    mock_subprocess_run.side_effect = subprocess_side_effect

    result = get_modified_files()

    assert "image.png" in result
    assert result["image.png"]["content"] == "[Binary File]"
    assert result["image.png"]["extension"] == ".png"
    assert result["image.png"]["status"] == "A"


def test_get_modified_files_name_status_fail(mock_subprocess_run):
    """Test get_modified_files when 'git diff --name-status' fails."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, ["git", "diff"])
    with pytest.raises(subprocess.CalledProcessError):
        get_modified_files()


# Update patch path
@patch("git_auto.src.git_utils.is_binary_file", return_value=False)
def test_get_modified_files_show_fail(mock_is_binary, mock_subprocess_run):
    """Test get_modified_files when 'git show' fails for a file."""
    name_status_output = "M\tfile1.py"

    def subprocess_side_effect(*args, **kwargs):
        cmd = args[0]
        if cmd == ["git", "diff", "--staged", "--name-status"]:
            return MagicMock(
                returncode=0, stdout=name_status_output, stderr="", check=True
            )
        elif cmd == ["git", "show", ":file1.py"]:
            # Simulate failure for git show
            raise subprocess.CalledProcessError(
                1, cmd, stderr=b"fatal: unable to read file1.py"
            )
        else:
            raise subprocess.CalledProcessError(1, cmd)

    mock_subprocess_run.side_effect = subprocess_side_effect

    # Should still return a result, but with an error marker for the content
    result = get_modified_files()
    assert "file1.py" in result
    assert result["file1.py"]["content"] == "[Error retrieving content]"
    assert result["file1.py"]["extension"] == ".py"
    assert result["file1.py"]["status"] == "M"
