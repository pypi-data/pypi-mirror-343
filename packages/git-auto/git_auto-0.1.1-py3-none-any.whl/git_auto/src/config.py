import os
import yaml
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, Any, Optional, List, Set
import logging
from pydantic import BaseModel, Field, ValidationError, field_validator
import subprocess

logger = logging.getLogger(__name__)

# Load .env file first, if present
load_dotenv()

# --- Default Repo Context --- (Can be overridden)
DEFAULT_REPO_CONTEXT = """
Project Structure Overview:
- mycli/: Main package directory.
  - src/: Source code.
    - cli.py: Command-line interface (Click).
    - config.py: Configuration loading (Pydantic, .env, .mycli.yaml).
    - ai_interface.py: Interaction with Gemini API.
    - git_utils.py: Git command execution.
    - sanitizer.py: Data sanitization/infuscation.
    - validation.py: Local code validation checks.
  - prompt_presets/: Default AI prompt templates.
  - templates/: Default output templates.
- tests/: Unit tests (pytest).
- pyproject.toml: Project metadata, dependencies, build config.
- README.md: Project documentation.

Purpose: This tool assists developers by analyzing staged Git changes,
validating code, generating conventional commit messages using AI,
and providing an interactive commit approval process.
"""

# --- Dynamic Repo Context Generation ---

DEFAULT_IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    ".env",
    "node_modules",
    "build",
    "dist",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "mycli.egg-info",
    ".vscode",
    ".idea",
    ".roo",
}
KEY_FILES = {
    "pyproject.toml",
    "setup.py",
    "setup.cfg",
    "requirements.txt",
    "Pipfile",
    "package.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "package-lock.json",
    "Dockerfile",
    "docker-compose.yaml",
    "docker-compose.yml",
    "Makefile",
    "Taskfile.yml",
    "justfile",
    "README.md",
    "README.rst",
    "LICENSE",
    "CONTRIBUTING.md",
    ".env.example",
    ".env.template",
    "config.yaml",
    "config.yml",
    "settings.toml",
    "main.py",
    "app.py",
    "cli.py",
    "__main__.py",
    "manage.py",
    ".gitignore",
    ".dockerignore",
}


def generate_repo_context(
    root_dir: Path,
    max_depth: int = 3,
    max_files_per_dir: int = 10,  # Limit files shown per directory
    max_total_lines: int = 100,  # Limit total output lines
    ignore_dirs: Optional[Set[str]] = None,
    key_files: Optional[Set[str]] = None,
) -> str:
    """Generates a string representation of the directory structure, highlighting key files."""
    if ignore_dirs is None:
        ignore_dirs = DEFAULT_IGNORE_DIRS
    if key_files is None:
        key_files = KEY_FILES

    structure = []
    line_count = 0

    def add_line(line: str) -> bool:
        nonlocal line_count
        if line_count >= max_total_lines:
            if not structure[-1].endswith("..."):  # Add ellipsis only once
                structure.append("    ... (output truncated)")
                line_count += 1
            return False
        structure.append(line)
        line_count += 1
        return True

    if not add_line(f"Project Root: {root_dir.name}"):
        return "\n".join(structure)

    def walk_dir(current_dir: Path, depth: int, prefix: str):
        nonlocal line_count
        if depth > max_depth:
            add_line(f"{prefix}...")
            return

        dir_items = []
        file_items = []
        try:
            for item in sorted(current_dir.iterdir()):
                if item.name in ignore_dirs:
                    continue
                if item.is_dir():
                    dir_items.append(item)
                else:
                    file_items.append(item)
        except OSError as e:
            logger.warning("Could not read directory %s: %s", current_dir, e)
            return

        # Combine and prioritize key files
        sorted_files = sorted(file_items, key=lambda f: f.name not in key_files)
        all_items = dir_items + sorted_files

        files_shown_count = 0
        for i, item in enumerate(all_items):
            if line_count >= max_total_lines:
                add_line(f"{prefix}    ... (output truncated)")
                break  # Stop processing items in this directory

            is_last = i == len(all_items) - 1
            connector = "└── " if is_last else "├── "
            indicator = ""  # Default

            if item.is_file():
                if files_shown_count >= max_files_per_dir:
                    if i == len(all_items) - 1 or not any(
                        f.is_file() for f in all_items[i + 1 :]
                    ):
                        # Show ellipsis only if it's the last file or no more files follow
                        add_line(
                            f"{prefix}{connector}... ({len(file_items) - files_shown_count} more files)"
                        )
                    continue  # Skip remaining files in this dir if limit reached
                files_shown_count += 1
                if item.name in key_files:
                    indicator = "* "  # Mark key files

            line_to_add = f"{prefix}{connector}{indicator}{item.name}"
            if item.is_dir():
                try:
                    # Add file count for directories
                    num_children = sum(
                        1 for _ in item.iterdir() if _.name not in ignore_dirs
                    )
                    line_to_add += f"/ ({num_children} items)"
                except OSError:
                    line_to_add += "/ (error reading)"

            if not add_line(line_to_add):
                break  # Stop if total line limit reached

            if item.is_dir():
                new_prefix = prefix + ("    " if is_last else "│   ")
                walk_dir(item, depth + 1, new_prefix)

    try:
        walk_dir(root_dir, 1, "")
        return "\n".join(structure)
    except Exception as e:
        logger.error("Failed to generate repository context: %s", e, exc_info=True)
        return "Error: Could not generate repository structure."


# --- Pydantic Models ---


class GenerationConfig(BaseModel):
    temperature: float = Field(..., ge=0.0, le=1.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    top_k: Optional[int] = Field(None, ge=1)
    max_output_tokens: int = Field(..., ge=1)


class SafetySetting(BaseModel):
    category: str
    threshold: str


# Default cache directory (user's cache folder)
def get_default_cache_dir() -> Path:
    # Use the new package name
    return Path.home() / ".cache" / "git-auto-commit"


class AppConfig(BaseModel):
    # Required
    api_key: str = Field(..., alias="GEMINI_API_KEY")

    # Optional with defaults
    model: str = "gemini-1.5-flash"
    safety_settings: List[SafetySetting] = Field(
        default_factory=lambda: [
            SafetySetting(
                category="HARM_CATEGORY_HARASSMENT", threshold="BLOCK_ONLY_HIGH"
            ),
            SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH", threshold="BLOCK_ONLY_HIGH"
            ),
            SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT", threshold="BLOCK_ONLY_HIGH"
            ),
            SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT", threshold="BLOCK_ONLY_HIGH"
            ),
        ]
    )
    max_diff_size: int = Field(4000, ge=100)
    preset: str = "dev"
    validation_prompt_path: Optional[str] = None
    commit_prompt_path: Optional[str] = None
    infuscation_patterns_file: Optional[str] = None  # Path to custom patterns file
    custom_infuscation_patterns: List[str] = Field(
        default_factory=list
    )  # Loaded patterns
    infuscation_literals_file: Optional[str] = None  # Path to custom literals file
    custom_infuscation_literals: List[str] = Field(
        default_factory=list
    )  # Loaded literals
    # Output Template Paths
    standard_output_template_path: Optional[str] = None
    minimal_output_template_path: Optional[str] = None
    repo_context: Optional[str] = None  # Will be populated dynamically

    # Caching Configuration
    cache_enabled: bool = True
    cache_dir: Path = Field(default_factory=get_default_cache_dir)
    cache_ttl_seconds: int = Field(3600 * 24 * 7, ge=0)  # Default: 1 week

    # Nested generation configs
    generation_config_validation: GenerationConfig = GenerationConfig(
        temperature=0.2, top_p=0.95, top_k=40, max_output_tokens=1024
    )
    generation_config_commit: GenerationConfig = GenerationConfig(
        temperature=0.3, top_p=0.95, top_k=40, max_output_tokens=256
    )

    @field_validator("api_key")
    def api_key_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("API key cannot be empty")
        return v


# --- Configuration File Handling ---

# Use the new package name for consistency
DEFAULT_CONFIG_FILENAME = ".git_auto_commit.yaml"


def find_config_file() -> Optional[Path]:
    """Search for config file in current dir, then home dir."""
    # 1. Current directory
    current_dir_path = Path.cwd() / DEFAULT_CONFIG_FILENAME
    if current_dir_path.is_file():
        return current_dir_path

    # 2. Home directory
    home_dir_path = Path.home() / DEFAULT_CONFIG_FILENAME
    if home_dir_path.is_file():
        return home_dir_path

    # 3. ~/.config/git-auto-commit/config.yaml (Linux/macOS style)
    # Use hyphenated name for XDG standard convention
    xdg_config_path = Path.home() / ".config" / "git-auto-commit" / "config.yaml"
    if xdg_config_path.is_file():
        return xdg_config_path

    return None


def load_config_from_file(config_path: Path) -> Dict[str, Any]:
    """Load configuration from a YAML file."""
    if not yaml:
        logger.warning(
            "PyYAML is not installed. Cannot load config file %s.", config_path
        )
        return {}
    try:
        with open(config_path, "r") as f:
            config_data: Dict[str, Any] = yaml.safe_load(f) or {}
            logger.debug("Successfully loaded config from %s", config_path)
            return config_data
    except Exception as e:
        logger.warning(
            "Could not load or parse config file %s: %s", config_path, e, exc_info=False
        )
        return {}


# --- Helper to load custom literals ---


def load_custom_literals(file_path_str: Optional[str]) -> List[str]:
    if not file_path_str:
        return []

    literals_path = Path(file_path_str).resolve()
    if not literals_path.is_file():
        logger.warning("Custom infuscation literals file not found: %s", literals_path)
        return []

    literals: List[str] = []
    try:
        with open(literals_path, "r", encoding="utf-8") as f:
            for line in f:
                literal = line.strip()
                if literal and not literal.startswith(
                    "#"
                ):  # Ignore empty lines and comments
                    literals.append(literal)
        logger.info(
            "Loaded %d custom infuscation literals from %s",
            len(literals),
            literals_path,
        )
        # Sort by length descending to replace longer matches first
        return sorted(literals, key=len, reverse=True)
    except Exception as e:
        logger.error(
            "Failed to read custom infuscation literals file %s: %s",
            literals_path,
            e,
            exc_info=True,
        )
        return []


# --- Helper to load custom patterns ---


def load_custom_patterns(file_path_str: Optional[str]) -> List[str]:
    if not file_path_str:
        return []

    patterns_path = Path(file_path_str).resolve()
    if not patterns_path.is_file():
        logger.warning("Custom infuscation patterns file not found: %s", patterns_path)
        return []

    patterns: List[str] = []
    try:
        with open(patterns_path, "r", encoding="utf-8") as f:
            for line in f:
                pattern = line.strip()
                if pattern and not pattern.startswith(
                    "#"
                ):  # Ignore empty lines and comments
                    patterns.append(pattern)
        logger.info(
            "Loaded %d custom infuscation patterns from %s",
            len(patterns),
            patterns_path,
        )
        return patterns
    except Exception as e:
        logger.error(
            "Failed to read custom infuscation patterns file %s: %s",
            patterns_path,
            e,
            exc_info=True,
        )
        return []


# --- Main Configuration Loading ---


def load_config() -> AppConfig:
    """Load config from file, env vars, validate, load custom patterns."""
    config_file_path: Optional[Path] = find_config_file()
    file_config: Dict[str, Any] = (
        load_config_from_file(config_file_path) if config_file_path else {}
    )

    merged_config_data: Dict[str, Any] = {}

    # 1. Start with file config
    merged_config_data.update(file_config)

    # 2. Override with environment variables
    if "GEMINI_API_KEY" in os.environ:
        merged_config_data["GEMINI_API_KEY"] = os.environ["GEMINI_API_KEY"]
    if "MODEL" in os.environ:
        merged_config_data["model"] = os.environ["MODEL"]
    if "MAX_DIFF_SIZE" in os.environ:
        merged_config_data["max_diff_size"] = os.environ["MAX_DIFF_SIZE"]
    if "COMMIT_PRESET" in os.environ:
        merged_config_data["preset"] = os.environ["COMMIT_PRESET"]
    if "VALIDATION_PROMPT_PATH" in os.environ:
        merged_config_data["validation_prompt_path"] = os.environ[
            "VALIDATION_PROMPT_PATH"
        ]
    if "COMMIT_PROMPT_PATH" in os.environ:
        merged_config_data["commit_prompt_path"] = os.environ["COMMIT_PROMPT_PATH"]
    if "INFUSCATION_PATTERNS_FILE" in os.environ:
        merged_config_data["infuscation_patterns_file"] = os.environ[
            "INFUSCATION_PATTERNS_FILE"
        ]
    if "INFUSCATION_LITERALS_FILE" in os.environ:
        merged_config_data["infuscation_literals_file"] = os.environ[
            "INFUSCATION_LITERALS_FILE"
        ]
    if "STANDARD_OUTPUT_TEMPLATE_PATH" in os.environ:
        merged_config_data["standard_output_template_path"] = os.environ[
            "STANDARD_OUTPUT_TEMPLATE_PATH"
        ]
    if "MINIMAL_OUTPUT_TEMPLATE_PATH" in os.environ:
        merged_config_data["minimal_output_template_path"] = os.environ[
            "MINIMAL_OUTPUT_TEMPLATE_PATH"
        ]
    if "CACHE_ENABLED" in os.environ:
        merged_config_data["cache_enabled"] = os.environ["CACHE_ENABLED"].lower() in [
            "true",
            "1",
            "yes",
        ]
    if "CACHE_DIR" in os.environ:
        merged_config_data["cache_dir"] = os.environ["CACHE_DIR"]
    if "CACHE_TTL_SECONDS" in os.environ:
        merged_config_data["cache_ttl_seconds"] = os.environ["CACHE_TTL_SECONDS"]

    gen_val_overrides: Dict[str, Any] = {}
    if "VALIDATION_TEMP" in os.environ:
        gen_val_overrides["temperature"] = os.environ["VALIDATION_TEMP"]
    if "VALIDATION_TOP_P" in os.environ:
        gen_val_overrides["top_p"] = os.environ["VALIDATION_TOP_P"]
    if "VALIDATION_TOP_K" in os.environ:
        gen_val_overrides["top_k"] = os.environ["VALIDATION_TOP_K"]
    if "VALIDATION_MAX_TOKENS" in os.environ:
        gen_val_overrides["max_output_tokens"] = os.environ["VALIDATION_MAX_TOKENS"]
    if gen_val_overrides:
        merged_config_data["generation_config_validation"] = {
            **(merged_config_data.get("generation_config_validation") or {}),
            **gen_val_overrides,
        }

    gen_commit_overrides: Dict[str, Any] = {}
    if "COMMIT_TEMP" in os.environ:
        gen_commit_overrides["temperature"] = os.environ["COMMIT_TEMP"]
    if "COMMIT_TOP_P" in os.environ:
        gen_commit_overrides["top_p"] = os.environ["COMMIT_TOP_P"]
    if "COMMIT_TOP_K" in os.environ:
        gen_commit_overrides["top_k"] = os.environ["COMMIT_TOP_K"]
    if "COMMIT_MAX_TOKENS" in os.environ:
        gen_commit_overrides["max_output_tokens"] = os.environ["COMMIT_MAX_TOKENS"]
    if gen_commit_overrides:
        merged_config_data["generation_config_commit"] = {
            **(merged_config_data.get("generation_config_commit") or {}),
            **gen_commit_overrides,
        }

    try:
        # Instantiate config *without* repo_context first
        if "repo_context" in merged_config_data:
            del merged_config_data[
                "repo_context"
            ]  # Ensure it's not passed if present in file

        app_config = AppConfig(**merged_config_data)

        # Generate and add repo context
        try:
            # Assume the script runs from somewhere within the repo
            # Find the git root directory to use as the base for context generation
            git_root_proc = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True,
                text=True,
                check=False,
                cwd=Path.cwd(),
            )
            if git_root_proc.returncode == 0:
                repo_root = Path(git_root_proc.stdout.strip())
                logger.debug("Generating repo context from root: %s", repo_root)
                app_config.repo_context = generate_repo_context(repo_root)
            else:
                logger.warning(
                    "Could not determine git repository root. Repo context will be unavailable."
                )
                app_config.repo_context = "Repository structure context unavailable."
        except FileNotFoundError:
            logger.warning("'git' command not found. Repo context will be unavailable.")
            app_config.repo_context = (
                "Repository structure context unavailable (git not found)."
            )
        except Exception as e:
            logger.error(
                "Error determining git root or generating context: %s", e, exc_info=True
            )
            app_config.repo_context = "Error generating repository structure context."

        # Load custom patterns and literals based on the validated paths
        app_config.custom_infuscation_patterns = load_custom_patterns(
            app_config.infuscation_patterns_file
        )
        app_config.custom_infuscation_literals = load_custom_literals(
            app_config.infuscation_literals_file
        )

        # Ensure cache directory exists after validation
        try:
            app_config.cache_dir.mkdir(parents=True, exist_ok=True)
            logger.debug("Cache directory ensured at: %s", app_config.cache_dir)
        except OSError as e:
            logger.error(
                "Failed to create cache directory %s: %s. Caching might fail.",
                app_config.cache_dir,
                e,
            )

        if config_file_path:
            logger.info("Loaded configuration from: %s", config_file_path)

        # Log final config at debug level (excluding API key)
        try:
            # Use model_dump and exclude the api_key
            config_dict_safe = app_config.model_dump(exclude={"api_key"})
            logger.debug("Final configuration loaded: %s", config_dict_safe)
        except Exception as log_e:
            logger.warning("Could not serialize config for debug logging: %s", log_e)

        return app_config
    except ValidationError as e:
        logger.error("Configuration validation failed:", exc_info=False)
        for error in e.errors():
            field = ".".join(map(str, error["loc"]))
            logger.error(f"  Field '{field}': {error['msg']}")
        raise ValueError(f"Invalid configuration: {e}") from e
