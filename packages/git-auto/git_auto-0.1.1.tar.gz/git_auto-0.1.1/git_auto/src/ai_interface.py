import google.generativeai as genai
from typing import Dict, Any, List, Optional, Tuple  # Add Tuple
import os
import importlib.resources as pkg_resources
import click
from pathlib import Path  # Need Path for custom file loading
import logging  # Import logging
import hashlib  # For cache keys
import time  # For cache TTL
import json  # For storing cache data

# Setup logger
logger = logging.getLogger(__name__)

# Attempt to import common Google API errors
try:
    import google.api_core.exceptions
except ImportError:
    google = None  # Indicate google.api_core is not available

from .config import load_config, AppConfig  # Import AppConfig type hint
from .sanitizer import DataSanitizer
from .. import prompt_presets


# Helper function to load prompt from file (package data or custom path)
def _load_prompt(filename: str, custom_path: Optional[str] = None) -> str:
    prompt_content = "Error: Could not load prompt."
    source = "package data"

    if custom_path:
        source = f"custom path ({custom_path})"
        try:
            prompt_path = Path(custom_path).resolve()
            if prompt_path.is_file():
                with open(prompt_path, "r", encoding="utf-8") as f:
                    prompt_content = f.read()
                logger.debug(
                    "Loaded prompt '%s' from custom path: %s", filename, custom_path
                )
            else:
                error_msg = f"Custom prompt file not found at {custom_path}"
                logger.error(error_msg)
                prompt_content = f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Error reading custom prompt file {custom_path}: {e}"
            logger.error(error_msg, exc_info=True)
            prompt_content = f"Error: {error_msg}"
    else:
        # Load from package data if no custom path
        try:
            prompt_content = pkg_resources.read_text(prompt_presets, filename)
            logger.debug("Loaded default prompt '%s' from package data.", filename)
        except FileNotFoundError:
            error_msg = (
                f"Default prompt file '{filename}' not found within package data."
            )
            logger.error(error_msg)
            prompt_content = f"Error: {error_msg}"
        except Exception as e:
            error_msg = (
                f"Error reading default prompt file '{filename}' from package data: {e}"
            )
            logger.error(error_msg, exc_info=True)
            prompt_content = f"Error: {error_msg}"

    if prompt_content.startswith("Error:"):
        # Log the error again before returning the error string
        logger.warning(
            "Prompt loading failed for '%s'. Returning error string.", filename
        )

    return prompt_content


# Helper function to configure GenAI
def _configure_genai() -> AppConfig:  # Return type is now AppConfig
    config = load_config()
    # Access api_key via attribute
    genai.configure(api_key=config.api_key)
    return config


# Helper function to handle truncation and sanitization
def _prepare_diff_for_ai(
    diff: str, config: AppConfig, infuscate: bool, verbose: bool
) -> Tuple[str, Optional[DataSanitizer]]:
    max_size = config.max_diff_size
    truncated = False
    processed_diff = diff
    sanitizer: Optional[DataSanitizer] = None  # Initialize sanitizer as None

    if len(processed_diff) > max_size:
        processed_diff = processed_diff[:max_size]
        truncated = True
        if verbose:
            click.echo(
                click.style(
                    f"\n--- Diff truncated to {max_size} characters --- ", fg="yellow"
                )
            )

    # Handle sanitization on the potentially truncated diff
    if infuscate:
        if verbose:
            click.echo(
                click.style(
                    "\n--- Original Text (Before Sanitization) ---", fg="yellow"
                )
            )
            click.echo(
                text[:1000] + ("... (truncated)" if len(text) > 1000 else "")
            )  # Show truncated original
            click.echo(click.style("--- End Original Text ---", fg="yellow"))

        # Pass custom patterns AND literals from config to sanitizer
        sanitizer = DataSanitizer(
            custom_patterns=config.custom_infuscation_patterns,
            custom_literals=config.custom_infuscation_literals,
        )
        processed_diff = sanitizer.sanitize_text(processed_diff)

        if verbose:
            click.echo(
                click.style("\n--- Sanitized Text (Sent to AI) ---", fg="yellow")
            )
            click.echo(
                processed_diff[:1000]
                + ("... (truncated)" if len(processed_diff) > 1000 else "")
            )
            click.echo(click.style(sanitizer.get_sanitization_summary(), dim=True))
            click.echo(click.style("--- End Sanitized Text ---", fg="yellow"))

    # Add truncation note *after* sanitization if needed
    if truncated:
        truncation_note = (
            "\n\n[Note: The provided diff was truncated due to length limitations.]"
        )
        processed_diff += truncation_note

    return processed_diff, sanitizer


# Helper function to handle sanitization
def _handle_sanitization(
    text: str, infuscate: bool, verbose: bool
) -> Tuple[str, Optional[DataSanitizer]]:
    sanitizer = None
    processed_text = text
    if infuscate:
        if verbose:
            click.echo(
                click.style(
                    "\n--- Original Text (Before Sanitization) ---", fg="yellow"
                )
            )
            click.echo(
                text[:1000] + ("... (truncated)" if len(text) > 1000 else "")
            )  # Show truncated original
            click.echo(click.style("--- End Original Text ---", fg="yellow"))

        sanitizer = DataSanitizer()
        processed_text = sanitizer.sanitize_text(text)

        if verbose:
            click.echo(
                click.style("\n--- Sanitized Text (Sent to AI) ---", fg="yellow")
            )
            click.echo(
                processed_text[:1000]
                + ("... (truncated)" if len(processed_text) > 1000 else "")
            )
            click.echo(click.style(sanitizer.get_sanitization_summary(), dim=True))
            click.echo(click.style("--- End Sanitized Text ---", fg="yellow"))

    return processed_text, sanitizer


# Helper function to handle desanitization
def _handle_desanitization(
    text: str, sanitizer: Optional[DataSanitizer], verbose: bool
) -> str:
    original_text = text
    desanitized_text = text
    if sanitizer:
        desanitized_text = sanitizer.desanitize_text(text)
        if verbose and original_text != desanitized_text:
            click.echo(
                click.style(
                    "\n--- AI Response (Before Desanitization) ---", fg="yellow"
                )
            )
            click.echo(original_text)
            click.echo(
                click.style(
                    "--- End AI Response (Before Desanitization) ---", fg="yellow"
                )
            )
            click.echo(
                click.style("\n--- AI Response (After Desanitization) ---", fg="green")
            )
            click.echo(desanitized_text)
            click.echo(
                click.style(
                    "--- End AI Response (After Desanitization) ---", fg="green"
                )
            )
    elif verbose:
        # Still show the raw response if verbose, even if no desanitization happened
        click.echo(click.style("\n--- Raw AI Response ---", fg="cyan"))
        click.echo(text)
        click.echo(click.style("--- End Raw AI Response ---", fg="cyan"))

    return desanitized_text


# --- Cache Helper Functions ---


def _generate_cache_key(prompt: str, model_name: str) -> str:
    """Generate a unique cache key based on prompt and model."""
    hasher = hashlib.sha256()
    hasher.update(model_name.encode("utf-8"))
    hasher.update(prompt.encode("utf-8"))
    return hasher.hexdigest()


def _read_from_cache(cache_dir: Path, key: str, ttl_seconds: int) -> Optional[str]:
    """Read response from cache if valid and not expired."""
    cache_file = cache_dir / f"{key}.json"
    if not cache_file.is_file():
        logger.debug("Cache miss (file not found): %s", key)
        return None

    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache_data = json.load(f)
        timestamp = cache_data.get("timestamp", 0)
        response = cache_data.get("response")

        if not response:
            logger.warning("Cache invalid (no response): %s", key)
            return None

        if time.time() - timestamp > ttl_seconds:
            logger.debug("Cache expired: %s", key)
            return None

        logger.debug("Cache hit: %s", key)
        return response
    except (json.JSONDecodeError, OSError, Exception) as e:
        logger.warning("Failed to read cache file %s: %s", cache_file, e)
        return None


def _write_to_cache(cache_dir: Path, key: str, response: str) -> None:
    """Write AI response to the cache."""
    cache_file = cache_dir / f"{key}.json"
    cache_data = {"timestamp": time.time(), "response": response}
    try:
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(cache_data, f)
        logger.debug("Wrote to cache: %s", key)
    except OSError as e:
        logger.error("Failed to write cache file %s: %s", cache_file, e)


def validate_code_changes(
    diff: str,
    files: Dict[str, Any],
    infuscate: bool = False,
    verbose: bool = False,
    no_cache: bool = False,  # Add no_cache flag
) -> str:
    """Analyze git diff with Gemini API for validation, optionally sanitizing and truncating."""
    config = _configure_genai()
    processed_diff, sanitizer = _prepare_diff_for_ai(diff, config, infuscate, verbose)

    safety_settings_dict = [s.model_dump() for s in config.safety_settings]
    generation_config_dict = config.generation_config_validation.model_dump(
        exclude_none=True
    )

    model = genai.GenerativeModel(
        config.model,  # Attribute access
        safety_settings=safety_settings_dict,
        generation_config=generation_config_dict,
    )

    file_list = [f"- {fp}" for fp in files.keys()]
    file_context = (
        "MODIFIED FILES:\n" + "\n".join(file_list)
        if file_list
        else "MODIFIED FILES: None"
    )

    prompt_template = _load_prompt(
        "validation_prompt.txt",
        custom_path=config.validation_prompt_path,  # Attribute access for prompt path
    )
    prompt = prompt_template.format(
        repo_context=config.repo_context,  # Add repo context
        file_context=file_context,
        processed_diff=processed_diff,
    )

    # --- Caching Logic ---
    cache_key = None
    if config.cache_enabled and not no_cache:
        cache_key = _generate_cache_key(prompt, config.model)
        cached_response = _read_from_cache(
            config.cache_dir, cache_key, config.cache_ttl_seconds
        )
        if cached_response is not None:
            logger.info("Using cached validation response.")
            return _handle_desanitization(cached_response, sanitizer, verbose)
    # --- End Caching Logic ---

    if verbose:
        click.echo(
            click.style("\n--- Validation Prompt (Sent to AI) ---", fg="magenta")
        )
        click.echo(prompt)
        click.echo(click.style("--- End Validation Prompt ---", fg="magenta"))

    try:
        response: Any = model.generate_content(
            prompt
        )  # Type hint for response if possible
        ai_response_text: str = response.text

        # --- Caching Logic ---
        if config.cache_enabled and not no_cache and cache_key:
            _write_to_cache(config.cache_dir, cache_key, ai_response_text)
        # --- End Caching Logic ---

        return _handle_desanitization(ai_response_text, sanitizer, verbose)
    except google.api_core.exceptions.GoogleAPIError as e:
        error_msg = f"Gemini API Error during validation: {e}"
        logger.error(error_msg, exc_info=verbose)
        return f"VALIDATION: ERROR - {error_msg}"
    except Exception as e:
        error_msg = f"Unexpected error during AI validation: {e}"
        logger.error(error_msg, exc_info=True)
        return f"VALIDATION: ERROR - {error_msg}"


def generate_commit_message(
    diff: str,
    files: Dict[str, Any],
    infuscate: bool = False,
    verbose: bool = False,
    no_cache: bool = False,  # Add no_cache flag
) -> str:
    """Generate commit message with Gemini API, optionally sanitizing and truncating."""
    config = _configure_genai()
    processed_diff, sanitizer = _prepare_diff_for_ai(diff, config, infuscate, verbose)

    safety_settings_dict = [s.model_dump() for s in config.safety_settings]
    generation_config_dict = config.generation_config_commit.model_dump(
        exclude_none=True
    )

    model = genai.GenerativeModel(
        config.model,  # Attribute access
        safety_settings=safety_settings_dict,
        generation_config=generation_config_dict,
    )

    file_list = [f"- {fp}" for fp in files.keys()]
    file_context = (
        "MODIFIED FILES:\n" + "\n".join(file_list)
        if file_list
        else "MODIFIED FILES: None"
    )

    prompt_template = _load_prompt(
        "commit_prompt.txt",
        custom_path=config.commit_prompt_path,  # Attribute access for prompt path
    )
    prompt = prompt_template.format(
        repo_context=config.repo_context,  # Add repo context
        file_context=file_context,
        processed_diff=processed_diff,
    )

    # --- Caching Logic ---
    cache_key = None
    if config.cache_enabled and not no_cache:
        cache_key = _generate_cache_key(prompt, config.model)
        cached_response = _read_from_cache(
            config.cache_dir, cache_key, config.cache_ttl_seconds
        )
        if cached_response is not None:
            logger.info("Using cached commit message response.")
            return _handle_desanitization(cached_response, sanitizer, verbose)
    # --- End Caching Logic ---

    if verbose:
        click.echo(
            click.style("\n--- Commit Message Prompt (Sent to AI) ---", fg="magenta")
        )
        click.echo(prompt)
        click.echo(click.style("--- End Commit Message Prompt ---", fg="magenta"))

    try:
        response: Any = model.generate_content(prompt)
        ai_response_text: str = response.text.strip()
        if ai_response_text.startswith("```") and ai_response_text.endswith("```"):
            ai_response_text = ai_response_text[3:-3].strip()

        # --- Caching Logic ---
        if config.cache_enabled and not no_cache and cache_key:
            _write_to_cache(config.cache_dir, cache_key, ai_response_text)
        # --- End Caching Logic ---

        return _handle_desanitization(ai_response_text, sanitizer, verbose)
    except google.api_core.exceptions.GoogleAPIError as e:
        error_msg = f"Gemini API Error during commit generation: {e}"
        logger.error(error_msg, exc_info=verbose)
        return f"Error: Could not generate commit message due to API error."
    except Exception as e:
        error_msg = f"Unexpected error during commit message generation: {e}"
        logger.error(error_msg, exc_info=True)
        return f"Error: Could not generate commit message due to unexpected error."


# Generate a fallback message based on changed files and their status
def generate_fallback_message(files: Dict[str, Any]) -> str:
    """Generates a fallback commit message considering file status and type."""
    if not files:
        return "chore: automated commit"

    file_paths = list(files.keys())
    statuses = [
        info.get("status", "M")[0].upper() for info in files.values()
    ]  # Get first letter of status
    extensions = [info.get("extension", "").lower() for info in files.values()]

    # --- Determine Commit Type Prefix ---
    # Prioritize based on status and then extension
    prefix = "chore:"  # Default
    if "A" in statuses:
        prefix = "feat:"  # Adding files often means new features
    elif "R" in statuses:
        prefix = "refactor:"  # Renaming is often part of refactoring
    elif (
        "D" in statuses
    ):  # Although get_modified_files filters these, handle if logic changes
        prefix = "fix:"  # Or chore, depending on context
    elif "M" in statuses:
        # If only modifications, use extension type
        common_ext = (
            max(set(e for e in extensions if e), key=extensions.count)
            if any(extensions)
            else ""
        )
        if any("test" in f.lower() for f in file_paths):
            prefix = "test:"
        elif any(
            f.lower().endswith(("readme.md", "readme", ".md")) for f in file_paths
        ):
            prefix = "docs:"
        elif common_ext in [".css", ".scss", ".less", ".style"]:
            prefix = "style:"
        elif common_ext in [".py", ".js", ".ts", ".java", ".go", ".rb", ".cs", ".php"]:
            prefix = "refactor:"  # Modifying code is often refactoring or fixing
        elif common_ext in [".json", ".yml", ".yaml", ".toml", ".ini", ".xml", ".conf"]:
            prefix = "config:"
        elif common_ext in [".sh", ".bash", ".ps1"]:
            prefix = "chore:"
        else:
            prefix = "chore:"  # Fallback for modifications
    else:
        prefix = "chore:"  # Default if only other statuses exist

    # --- Determine Summary ---
    if len(file_paths) == 1:
        filename = os.path.basename(file_paths[0])
        status_verb = {"A": "add", "M": "modify", "D": "delete", "R": "rename"}.get(
            statuses[0], "update"
        )
        summary = f"{status_verb} {filename}"
    else:
        # Simple summary for multiple files
        status_desc = []
        if "A" in statuses:
            status_desc.append("add new")
        if "M" in statuses:
            status_desc.append("modify existing")
        if "R" in statuses:
            status_desc.append("rename/move")
        if "D" in statuses:
            status_desc.append("delete")
        # Count file types
        ext_counts = {}
        for ext in extensions:
            if ext:
                ext_counts[ext] = ext_counts.get(ext, 0) + 1
        most_common_ext = max(ext_counts, key=ext_counts.get) if ext_counts else ""

        if status_desc:
            summary = f"{', '.join(status_desc)} files"
            if most_common_ext:
                summary += f" (mostly {most_common_ext})"
        elif most_common_ext:
            summary = f"update {most_common_ext} files"
        else:
            summary = "update multiple files"

    # Ensure summary fits within ~50 chars
    full_prefix = f"{prefix} "
    max_summary_len = 50 - len(full_prefix)
    if len(summary) > max_summary_len:
        summary = summary[: max_summary_len - 3] + "..."

    return f"{full_prefix}{summary}"
