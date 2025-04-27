import subprocess
import os
import logging
from typing import Dict, Any

from .validation import is_binary_file

logger = logging.getLogger(__name__)


def get_git_diff() -> str:
    """Get staged changes diff."""
    try:
        result: subprocess.CompletedProcess = subprocess.run(
            ["git", "diff", "--staged"],
            capture_output=True,
            text=True,
            check=True,  # Raise error on failure
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error("Failed to get git diff: %s", e.stderr or e)
        raise RuntimeError("Failed to get git diff") from e
    except FileNotFoundError:
        logger.error("'git' command not found. Is Git installed and in PATH?")
        raise RuntimeError("'git' command not found")


def get_modified_files() -> Dict[str, Any]:
    """Get staged files with their content and metadata."""
    modified_files_data: Dict[str, Any] = {}
    try:
        # Get file statuses and names
        name_status_result: subprocess.CompletedProcess = subprocess.run(
            ["git", "diff", "--staged", "--name-status"],
            capture_output=True,
            text=True,
            check=True,
        )

        for line in name_status_result.stdout.strip().splitlines():
            if not line:
                continue

            parts = line.split("\t")
            status: str = parts[0].strip()
            # Handle potential renames (R status has source and destination)
            file_path: str = parts[-1].strip()

            if status.startswith("D"):
                logger.debug("Skipping deleted file: %s", file_path)
                continue

            # Get the staged content of the file
            try:
                content_result: subprocess.CompletedProcess = subprocess.run(
                    ["git", "show", f":{file_path}"],
                    capture_output=True,
                    check=True,
                )
                content_bytes: bytes = content_result.stdout

                try:
                    content: str = content_bytes.decode("utf-8")
                    binary: bool = is_binary_file(content)
                except UnicodeDecodeError:
                    logger.warning(
                        "Could not decode %s as UTF-8, treating as binary.", file_path
                    )
                    content = "[Binary File]"  # Placeholder for binary
                    binary = True

                extension: str = os.path.splitext(file_path)[1].lower()

                modified_files_data[file_path] = {
                    "content": "[Binary File]" if binary else content,
                    "extension": extension,
                    "status": status,
                }

            except subprocess.CalledProcessError as e:
                logger.warning(
                    "Could not get staged content for %s. Error: %s",
                    file_path,
                    e.stderr or e,
                )
                modified_files_data[file_path] = {
                    "content": "[Error retrieving content]",
                    "extension": os.path.splitext(file_path)[1].lower(),
                    "status": status,
                }
            except Exception as e:
                logger.error(
                    "An unexpected error occurred processing %s: %s",
                    file_path,
                    e,
                    exc_info=True,
                )
                modified_files_data[file_path] = {
                    "content": "[Error processing file]",
                    "extension": os.path.splitext(file_path)[1].lower(),
                    "status": status,
                }

    except subprocess.CalledProcessError as e:
        logger.error("Failed to get modified file list: %s", e.stderr or e)
        raise RuntimeError("Failed to get modified file list") from e
    except FileNotFoundError:
        logger.error("'git' command not found. Is Git installed and in PATH?")
        raise RuntimeError("'git' command not found")

    return modified_files_data


def check_git_repo() -> None:
    """Check if the current directory is a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            check=True,
            capture_output=True,  # Suppress output
        )
        logger.debug("Current directory is a git repository.")
    except subprocess.CalledProcessError as e:
        logger.error("Not inside a git repository.")
        raise RuntimeError("Not a git repository.") from e
    except FileNotFoundError:
        logger.error("'git' command not found. Is Git installed and in PATH?")
        raise RuntimeError("'git' command not found")
