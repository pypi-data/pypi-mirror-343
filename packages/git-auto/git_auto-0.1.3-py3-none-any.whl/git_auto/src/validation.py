import os
import re
import subprocess
import sys
import tempfile
import shutil
import json
import string
import logging
from typing import Dict, Any, List, Pattern

logger = logging.getLogger(__name__)

# Try importing YAML, required for basic YAML check
try:
    import yaml
except ImportError:
    yaml = None  # Flag that PyYAML is not installed

# Try importing TOML library
try:
    import toml
except ImportError:
    toml = None  # Flag that toml is not installed

# Check if yamllint is available (optional dependency)
_YAMLLINT_AVAILABLE: bool = shutil.which("yamllint") is not None

# Check if shellcheck is available
_SHELLCHECK_AVAILABLE: bool = shutil.which("shellcheck") is not None

# Regex to find unpinned dependencies (excluding comments/empty lines)
# Looks for lines that don't start with #, contain text, but lack ==
UNPINNED_REQ_REGEX = re.compile(r"^\s*[^#\s].*[^=]==.*", re.IGNORECASE)


# Check if a file is likely binary
def is_binary_file(content: str) -> bool:
    """Check if file content appears to be binary."""
    # Simple heuristic: Check for null bytes or high proportion of non-printable chars
    if "\x00" in content:
        return True

    # Count non-printable characters
    non_printable = sum(1 for c in content if c not in (string.printable + "\t\n\r"))
    if non_printable > len(content) * 0.3:  # If >30% non-printable
        return True

    return False


# Check for syntax errors in modified files
def check_syntax_errors(modified_files: Dict[str, Any]) -> List[Dict[str, str]]:
    """Check syntax for various file types (Python, JS/TS, JSON, YAML, Dockerfile, Shell Script, TOML, requirements.txt)."""
    syntax_issues: List[Dict[str, str]] = []

    for file_path, file_info in modified_files.items():
        filename = os.path.basename(file_path)
        extension: str = file_info.get("extension", "").lower()
        content: str = file_info.get("content", "")

        # Determine if it's a Dockerfile
        is_dockerfile = filename.lower() == "dockerfile" or extension == ".dockerfile"

        # Skip binary files, files without content, or without extensions
        if not content or content == "[Binary File]" or is_binary_file(content):
            continue
        # Skip if no extension AND not a Dockerfile by name
        if not extension and not is_dockerfile:
            continue

        temp_path: str = ""
        try:
            # Create a temporary file for syntax checking
            with tempfile.NamedTemporaryFile(
                suffix=extension, delete=False, mode="w", encoding="utf-8"
            ) as temp_file:
                temp_path = temp_file.name
                temp_file.write(content)
        except Exception as e:
            logger.error(
                "Could not create temp file for validation of %s: %s",
                file_path,
                e,
                exc_info=True,
            )
            syntax_issues.append(
                {
                    "file": file_path,
                    "error": f"Could not create temp file for validation: {e}",
                }
            )
            continue

        try:
            # --- Python ---
            if extension == ".py":
                result: subprocess.CompletedProcess = subprocess.run(
                    [sys.executable, "-m", "py_compile", temp_path],
                    capture_output=True,
                    text=True,
                )
                if result.returncode != 0:
                    error_msg = result.stderr.strip()
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": f"Python syntax error: {error_msg}",
                        }
                    )

            # --- JavaScript/TypeScript ---
            elif extension in [".js", ".ts"]:
                node_path = shutil.which("node")
                if node_path:
                    result = subprocess.run(
                        [node_path, "--check", temp_path],
                        capture_output=True,
                        text=True,
                    )
                    if result.returncode != 0:
                        error_msg = result.stderr.strip()
                        syntax_issues.append(
                            {
                                "file": file_path,
                                "error": f"JS/TS syntax error: {error_msg}",
                            }
                        )
                else:
                    logger.debug(
                        "Node.js not found in PATH, skipping syntax check for %s",
                        file_path,
                    )

            # --- JSON / package.json Checks ---
            elif extension == ".json":
                try:
                    parsed_json = json.loads(content)
                    # Specific checks if it's package.json
                    if filename.lower() == "package.json":
                        logger.debug("Performing package.json checks for %s", file_path)
                        if not isinstance(parsed_json, dict):
                            syntax_issues.append(
                                {
                                    "file": file_path,
                                    "error": "package.json: Root element is not an object.",
                                }
                            )
                        else:
                            if "name" not in parsed_json:
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "package.json: Missing required 'name' field.",
                                    }
                                )
                            if "version" not in parsed_json:
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "package.json: Missing required 'version' field.",
                                    }
                                )
                            # Add more checks? e.g., presence of scripts, main, license?
                except json.JSONDecodeError as e:
                    syntax_issues.append(
                        {"file": file_path, "error": f"JSON syntax error: {e}"}
                    )
                except Exception as e:
                    logger.error(
                        "Error during package.json specific checks for %s: %s",
                        file_path,
                        e,
                        exc_info=True,
                    )
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": f"Error checking package.json: {e}",
                        }
                    )

            # --- YAML ---
            elif extension in [".yaml", ".yml"]:
                if yaml:
                    try:
                        # Use safe_load_all for multi-document support
                        # Iterate through the generator to force parsing of all documents
                        documents = list(yaml.safe_load_all(content))
                        logger.debug(
                            "YAML syntax check passed for %d documents in %s",
                            len(documents),
                            file_path,
                        )

                        # Basic check passed, now try yamllint if available
                        if _YAMLLINT_AVAILABLE:
                            result = subprocess.run(
                                ["yamllint", "-s", temp_path],
                                capture_output=True,
                                text=True,
                            )
                            if result.returncode != 0:
                                error_msg = (
                                    result.stdout.strip() + "\n" + result.stderr.strip()
                                ).strip()
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": f"yamllint issues:\n{error_msg}",
                                    }
                                )
                        else:
                            logger.debug(
                                "yamllint not found in PATH, skipping advanced YAML linting for %s",
                                file_path,
                            )
                    except yaml.YAMLError as e:
                        syntax_issues.append(
                            {"file": file_path, "error": f"YAML syntax error: {e}"}
                        )
                else:
                    logger.debug(
                        "PyYAML not installed, skipping YAML syntax check for %s",
                        file_path,
                    )

            # --- Dockerfile Checks --- (Basic Regex)
            elif is_dockerfile:
                logger.debug("Performing basic Dockerfile checks for %s", file_path)
                # Check 1: apt-get update without cleaning lists
                if re.search(r"apt-get update", content) and not re.search(
                    r"rm -rf /var/lib/apt/lists/\*", content
                ):
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": "Dockerfile: Found 'apt-get update' without subsequent 'rm -rf /var/lib/apt/lists/*' (potential layer bloat).",
                        }
                    )
                # Check 2: Using 'latest' tag for base image
                if re.search(r"^FROM\s+[^:]+:latest", content, re.MULTILINE):
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": "Dockerfile: Base image uses 'latest' tag, which is not recommended for reproducible builds.",
                        }
                    )
                # Check 3: ADD command with URL (prefer curl/wget for better layer caching)
                if re.search(r"^ADD\s+(https?://\S+)", content, re.MULTILINE):
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": "Dockerfile: Found 'ADD' with a URL. Consider using curl or wget instead for better layer caching.",
                        }
                    )

            # --- Shell Script Checks ---
            elif extension == ".sh":
                if _SHELLCHECK_AVAILABLE:
                    logger.debug("Running shellcheck for %s", file_path)
                    try:
                        # Run shellcheck with JSON output format
                        result = subprocess.run(
                            ["shellcheck", "-f", "json", temp_path],
                            capture_output=True,
                            text=True,
                            check=False,
                        )
                        if result.stdout:
                            try:
                                shellcheck_issues = json.loads(result.stdout)
                                if isinstance(shellcheck_issues, list):
                                    for issue in shellcheck_issues:
                                        line = issue.get("line", "?")
                                        col = issue.get("column", "?")
                                        level = issue.get("level", "info")
                                        code = issue.get("code", "SC?")
                                        message = issue.get("message", "Unknown issue")
                                        if level in ["warning", "error"]:
                                            syntax_issues.append(
                                                {
                                                    "file": file_path,
                                                    "error": f"Shellcheck ({level} SC{code} L{line}:C{col}): {message}",
                                                }
                                            )
                            except json.JSONDecodeError:
                                logger.warning(
                                    "Failed to parse shellcheck JSON output for %s",
                                    file_path,
                                )
                                if result.stderr:
                                    syntax_issues.append(
                                        {
                                            "file": file_path,
                                            "error": f"Shellcheck error: {result.stderr.strip()}",
                                        }
                                    )
                        elif result.returncode != 0:
                            syntax_issues.append(
                                {
                                    "file": file_path,
                                    "error": f"Shellcheck execution error: {result.stderr.strip()}",
                                }
                            )
                    except Exception as e:
                        logger.error(
                            "Failed to execute shellcheck for %s: %s",
                            file_path,
                            e,
                            exc_info=True,
                        )
                        syntax_issues.append(
                            {
                                "file": file_path,
                                "error": f"Failed to run shellcheck: {e}",
                            }
                        )
                else:
                    logger.debug(
                        "shellcheck not found, performing basic checks for %s",
                        file_path,
                    )
                    has_set_e = re.search(
                        r"^\s*set\s+.*-[^\s]*e", content, re.MULTILINE
                    )
                    has_set_u = re.search(
                        r"^\s*set\s+.*-[^\s]*u", content, re.MULTILINE
                    )
                    has_pipefail = re.search(
                        r"^\s*set\s+.*-o\s+pipefail", content, re.MULTILINE
                    )

                    if not (has_set_e and has_set_u and has_pipefail):
                        missing = []
                        if not has_set_e:
                            missing.append("set -e")
                        if not has_set_u:
                            missing.append("set -u")
                        if not has_pipefail:
                            missing.append("set -o pipefail")
                        syntax_issues.append(
                            {
                                "file": file_path,
                                "error": f"Shell script: Consider adding `{'`, `'.join(missing)}` near the top for stricter error handling.",
                            }
                        )

                    if re.search(r"`.*`", content):
                        syntax_issues.append(
                            {
                                "file": file_path,
                                "error": "Shell script: Found deprecated backticks ``. Consider using `$()` instead.",
                            }
                        )

            # --- TOML / pyproject.toml Checks ---
            elif extension == ".toml":
                if toml:
                    logger.debug("Performing TOML validation for %s", file_path)
                    try:
                        # Basic TOML syntax check
                        parsed_toml = toml.loads(content)

                        # Specific checks if it's pyproject.toml
                        if filename.lower() == "pyproject.toml":
                            if "project" not in parsed_toml:
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "pyproject.toml: Missing required [project] table.",
                                    }
                                )
                            elif "name" not in parsed_toml.get("project", {}):
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "pyproject.toml: Missing required 'name' key in [project] table.",
                                    }
                                )

                            if "build-system" not in parsed_toml:
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "pyproject.toml: Missing recommended [build-system] table.",
                                    }
                                )
                            elif "requires" not in parsed_toml.get("build-system", {}):
                                syntax_issues.append(
                                    {
                                        "file": file_path,
                                        "error": "pyproject.toml: Missing recommended 'requires' key in [build-system] table.",
                                    }
                                )

                    except toml.TomlDecodeError as e:
                        syntax_issues.append(
                            {"file": file_path, "error": f"TOML syntax error: {e}"}
                        )
                    except Exception as e:
                        # Catch other potential errors during checks
                        logger.error(
                            "Error during pyproject.toml specific checks for %s: %s",
                            file_path,
                            e,
                            exc_info=True,
                        )
                        syntax_issues.append(
                            {
                                "file": file_path,
                                "error": f"Error checking pyproject.toml: {e}",
                            }
                        )
                else:
                    logger.debug(
                        "toml library not installed, skipping TOML validation for %s",
                        file_path,
                    )

            # --- requirements.txt Checks ---
            # Check common requirement file names
            elif filename.lower().startswith(
                "requirements"
            ) and filename.lower().endswith(".txt"):
                logger.debug("Performing requirements.txt checks for %s", file_path)
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    line_num = i + 1
                    stripped_line = line.strip()
                    # Skip comments and empty lines
                    if not stripped_line or stripped_line.startswith("#"):
                        continue
                    # Skip editable installs or local paths
                    if (
                        stripped_line.startswith("-e")
                        or stripped_line.startswith(".")
                        or stripped_line.startswith("/")
                    ):
                        continue
                    # Skip lines with version specifiers (==, >=, <=, ~=, <, >)
                    if re.search(r"(==|>=|<=|~=|!=|<|>)", stripped_line):
                        continue

                    # If we reach here, it's likely an unpinned dependency
                    syntax_issues.append(
                        {
                            "file": file_path,
                            "error": f"requirements.txt (L{line_num}): Potentially unpinned dependency '{stripped_line}'. Consider pinning versions with '=='.",
                        }
                    )

        finally:
            # Clean up the temporary file
            if temp_path:
                try:
                    os.unlink(temp_path)
                except OSError as e:
                    logger.warning(
                        "Could not remove temporary validation file %s: %s",
                        temp_path,
                        e,
                    )

    return syntax_issues


# Check for unsupported characters
def check_unsupported_chars(modified_files: Dict[str, Any]) -> List[Dict[str, str]]:
    """Check for control characters, BOM, and potentially problematic non-ASCII chars."""
    unsupported_char_issues: List[Dict[str, str]] = []
    # Regex for control characters (excluding tab, newline, carriage return)
    control_chars_regex: Pattern[str] = re.compile(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]")
    # Regex for potentially problematic non-ASCII characters (anything outside printable ASCII 32-126)
    # We exclude common whitespace like newline, tab, carriage return which are handled separately if needed.
    # This will catch Cyrillic, Greek, etc.
    non_ascii_printable_regex: Pattern[str] = re.compile(r"[^\x20-\x7E\n\r\t]")

    for file_path, file_info in modified_files.items():
        content: str = file_info.get("content", "")
        extension: str = file_info.get("extension", "").lower()

        # Skip binary files or files without content
        if not content or is_binary_file(content):
            continue

        # Check 1: Control Characters
        control_matches: List[str] = control_chars_regex.findall(content)
        if control_matches:
            unique_chars: List[str] = sorted(list(set(control_matches)))
            char_codes: List[str] = [f"U+{ord(c):04X}" for c in unique_chars]
            unsupported_char_issues.append(
                {
                    "file": file_path,
                    "error": f"Contains control character(s): {', '.join(char_codes)}",
                }
            )

        # Check 2: UTF-8 BOM
        if content.startswith("\ufeff") and extension in [
            ".py",
            ".js",
            ".sh",
            ".json",
            ".yaml",
            ".yml",
        ]:
            unsupported_char_issues.append(
                {
                    "file": file_path,
                    "error": "Contains UTF-8 BOM marker which may cause issues.",
                }
            )

        # Check 3: Non-Standard Printable Characters (potential typos/homographs)
        # We check this *after* BOM check
        content_no_bom = content[1:] if content.startswith("\ufeff") else content
        non_ascii_matches: List[str] = non_ascii_printable_regex.findall(content_no_bom)
        if non_ascii_matches:
            unique_chars = sorted(list(set(non_ascii_matches)))
            # Limit the number of reported chars to avoid huge messages
            limit = 10
            reported_chars = unique_chars[:limit]
            ellipsis = "..." if len(unique_chars) > limit else ""
            # Report with high severity suggestion
            unsupported_char_issues.append(
                {
                    "file": file_path,
                    "error": f"CRITICAL: Found non-ASCII characters (potential typos/homographs): '{''.join(reported_chars)}{ellipsis}' (Codes: {[f'U+{ord(c):04X}' for c in reported_chars]})",
                }
            )

    return unsupported_char_issues
