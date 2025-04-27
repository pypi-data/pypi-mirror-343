import click
import sys
import subprocess
import os
import logging
import re
import shutil
import stat  # Import stat for chmod
import time  # Import time module
from typing import Optional, Dict, Any, List, Tuple
import importlib.metadata
from jinja2 import Environment, TemplateNotFound, TemplateSyntaxError
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from pathlib import Path  # Import Path

from .git_utils import check_git_repo, get_git_diff, get_modified_files
from .ai_interface import (
    validate_code_changes,
    generate_commit_message,
    generate_fallback_message,
)
from .validation import check_syntax_errors, check_unsupported_chars
from .config import load_config, AppConfig
from .. import templates

# Special return value for revert action
REVERT_ACTION = "__REVERT__"

# --- Logging Setup ---
log_format = "%(levelname)s: %(message)s"
logging.basicConfig(level=logging.INFO, format=log_format)
logger = logging.getLogger(__name__)

# Instantiate a global console object
console = Console()

# --- Hook Script Content (Updated Command) ---
HookScriptContent = """#!/bin/sh
# git-auto pre-commit hook

# Ensure git-auto is available
if ! command -v git-auto > /dev/null 2>&1; then
    echo "[git-auto hook] Error: git-auto command not found." >&2
    exit 1
fi

echo "[git-auto hook] Running git-auto helper..."

# Execute git-auto commit
git-auto commit
exit_code=$?

if [ $exit_code -ne 0 ]; then
    echo "[git-auto hook] Check failed or was cancelled. Aborting commit." >&2
    exit 1
fi

exit 0
"""


# --- Template Loading Helper ---
def _load_output_template(filename: str, custom_path: Optional[str] = None) -> str:
    """Load output template from file or fallback to basic Jinja template."""
    try:
        if custom_path and os.path.exists(custom_path):
            with open(custom_path, "r") as file:
                return file.read()
        else:
            template_path = os.path.join(
                os.path.dirname(__file__), "templates", filename
            )
            with open(template_path, "r") as file:
                return file.read()
    except FileNotFoundError:
        logger.warning(
            "Template file '%s' not found. Using fallback template.", filename
        )
        if "minimal" in filename:
            return "Validation: {{ validation_status_colored }}\n\nCommit Message:\n{{ commit_message }}"
        else:
            return "Validation Report:\n{{ validation_status_colored }}\n{% if issues %}{{ issues_table }}{% endif %}\n\nCommit Message:\n{{ commit_message }}"
    except Exception as e:
        logger.error("Error loading template '%s': %s", filename, e)
        return "Error: Template loading failed."


# --- Helper to Parse Validation Report --- (Updated Status Logic)
def parse_validation_report(report: str) -> Tuple[str, Dict[str, List[str]]]:
    """Parses the validation report into status and categorized issues."""
    lines = report.strip().split("\n")
    original_status_line = lines[0] if lines else "VALIDATION: UNKNOWN"
    issues: Dict[str, List[str]] = {
        "CRITICAL": [],
        "HIGH": [],
        "MEDIUM": [],
        "LOW": [],
        "PRACTICAL": [],
    }
    current_category = None

    category_map = {
        "CRITICAL ISSUES:": "CRITICAL",
        "HIGH ISSUES:": "HIGH",
        "MEDIUM ISSUES:": "MEDIUM",
        "LOW ISSUES:": "LOW",
        "PRACTICAL PROBLEMS:": "PRACTICAL",
    }

    for line in lines[1:]:
        line_stripped = line.strip()
        if not line_stripped or line_stripped == "None":
            continue

        is_category_header = False
        for header, key in category_map.items():
            if line_stripped.startswith(header):
                current_category = key
                is_category_header = True
                break

        if (
            not is_category_header
            and current_category
            and line_stripped.startswith("-")
        ):
            issues[current_category].append(line_stripped[1:].strip())
        elif (
            not is_category_header
            and not line_stripped.startswith("-")
            and not line_stripped.startswith("SUMMARY:")
        ):
            pass

    # Filter out empty categories
    issues = {k: v for k, v in issues.items() if v}

    # Determine new status based on highest severity
    final_status_line = "VALIDATION: PASSED"
    highest_severity = "NONE"
    if issues.get("CRITICAL"):
        final_status_line = "VALIDATION: NEEDS REVISION (CRITICAL)"
        highest_severity = "CRITICAL"
    elif issues.get("HIGH"):
        final_status_line = "VALIDATION: NEEDS REVISION (HIGH)"
        highest_severity = "HIGH"
    elif issues.get("MEDIUM"):
        final_status_line = "VALIDATION: PASSED WITH WARNINGS (MEDIUM)"
        highest_severity = "MEDIUM"
    elif issues.get("LOW"):
        final_status_line = "VALIDATION: PASSED WITH WARNINGS (LOW)"
        highest_severity = "LOW"
    elif issues.get("PRACTICAL"):
        final_status_line = "VALIDATION: PASSED WITH WARNINGS (PRACTICAL)"
        highest_severity = "PRACTICAL"
    elif "ERROR" in original_status_line:
        # Preserve original error status if parsing failed or AI reported error
        final_status_line = original_status_line
        highest_severity = "ERROR"

    logger.debug(
        "Parsed validation report. Highest severity: %s. Final Status: %s",
        highest_severity,
        final_status_line,
    )
    return final_status_line, issues


# --- Helper to Format Issues Table using Rich ---
def create_issues_table(issues: Dict[str, List[str]]) -> Optional[Table]:
    """Creates a rich Table object for validation issues."""
    if not issues:
        return None

    table = Table(
        title="[bold yellow]Validation Issues[/]",
        show_header=True,
        header_style="bold magenta",
        border_style="dim",
    )
    table.add_column("Severity", style="dim", width=10)
    table.add_column("Description", style="none", min_width=40, max_width=80)

    severity_order = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "PRACTICAL"]
    severity_styles = {
        "CRITICAL": "bold red",
        "HIGH": "red",
        "MEDIUM": "yellow",
        "LOW": "cyan",
        "PRACTICAL": "blue",
    }

    for severity in severity_order:
        if severity in issues:
            style = severity_styles.get(severity, "none")
            for issue_desc in issues[severity]:
                table.add_row(f"[{style}]{severity}[/]", issue_desc)

    return table


# --- User Approval Logic (Handling No Diff for Revert) ---
def get_user_approval(
    message: Optional[str],  # Message can be None if no diff
    validation_report: Optional[str],  # Report can be None if no diff
    diff_output: Optional[str],
    config: AppConfig,
    minimal: bool = False,
    can_revert: bool = False,
    # Add original args needed for regeneration
    modified_files: Dict[str, Any] = {},
    infuscate: bool = False,
    verbose: bool = False,
    no_cache: bool = False,
) -> Optional[str]:  # Return type can be str (message), None (cancel), or REVERT_ACTION
    """Parse report, show summary/message, prompt user (with details, regenerate, revert)."""

    status_line, issues = (
        parse_validation_report(validation_report)
        if validation_report
        else ("No changes to validate.", {})
    )
    needs_attention = (
        "NEEDS REVISION" in status_line
        or "WARNINGS" in status_line
        or "ERROR" in status_line
        or bool(issues)
    )

    # **Define display_output helper function here, before the loop**
    def display_output(current_message: str):
        """Helper to display the current status and message."""
        status_text = Text(status_line)
        if "PASSED" in status_line and "WARNINGS" not in status_line:
            status_text.stylize("green")
        elif "WARNINGS" in status_line:
            status_text.stylize("yellow")
        elif "NEEDS REVISION" in status_line or "ERROR" in status_line:
            status_text.stylize("bold red")
        console.print(
            Panel(
                status_text,
                title="[bold blue]Validation Status[/]",
                border_style="blue",
                expand=False,
            )
        )

        if not minimal and bool(issues):
            issues_table = create_issues_table(issues)
            if issues_table:
                console.print(issues_table)

        if current_message:  # Only print message panel if message exists
            console.print(
                Panel(
                    current_message,
                    title="[bold blue]Proposed Commit Message[/]",
                    border_style="blue",
                    expand=False,
                )
            )
        # else: Do nothing if no message (e.g., initial state with no diff)

    # Display initial message (if it exists)
    current_commit_message = message or ""  # Ensure it's a string
    display_output(current_commit_message)

    # --- Prompt Loop ---
    while True:
        prompt_options = ["n"]  # Always allow cancelling
        prompt_choices_display_parts = ["[N]o"]
        prompt_msg = "\nAction? "

        if message:  # Options requiring a message/diff
            prompt_options.extend(["y", "e", "v", "r"])
            prompt_choices_display_parts.extend(
                ["[Y]es", "[E]dit", "[V]iew diff", "[R]egenerate"]
            )  # Add Regenerate
            prompt_msg = "\nCommit with this message? "

        if bool(issues) and not minimal:
            prompt_options.append("d")
            prompt_choices_display_parts.append("[D]etails")

        if can_revert:
            prompt_options.append("z")
            prompt_choices_display_parts.append("[Z]Revert last & retry")

        prompt_choices_display = "/".join(prompt_choices_display_parts)

        if (
            needs_attention and message
        ):  # Add warning prefix only if there are issues AND a message to approve
            prompt_msg = (
                click.style("\n⚠️ Validation issues found! Proceed anyway?", fg="yellow")
                + " "
            )

        prompt_msg += f"{prompt_choices_display}: "

        # Ensure only valid options are presented based on state
        valid_choices = click.Choice(prompt_options, case_sensitive=False)
        response = click.prompt(
            prompt_msg, type=valid_choices, show_choices=False, err=False
        )

        if response == "y" and message:  # Can only say yes if there's a message
            return current_commit_message
        elif response == "n":
            return None
        elif response == "z" and can_revert:
            # Confirm revert action
            if click.confirm(
                f"Are you sure you want to revert the last commit (git reset --soft HEAD~1)?",
                default=False,
            ):
                return REVERT_ACTION  # Signal revert to the main command loop
            else:
                console.print("[yellow]Revert cancelled.[/]")
                if message:
                    display_output(current_commit_message)  # Re-display
                continue  # Re-prompt
        elif response == "e" and message:
            edited_message: Optional[str] = click.edit(current_commit_message)
            if edited_message is not None:
                edited_message = "\n".join(
                    line
                    for line in edited_message.splitlines()
                    if not line.strip().startswith("#")
                )
                final_edited_message: str = edited_message.strip()
                console.print(
                    Panel(
                        final_edited_message,
                        title="[bold blue]Edited Commit Message[/]",
                        border_style="blue",
                        expand=False,
                    )
                )
                if click.confirm("Use this edited message?"):
                    return final_edited_message
                else:
                    logger.info("User discarded edited message.")
                    # Re-show the current message before edit attempt
                    display_output(current_commit_message)
            else:
                logger.info("User cancelled edit.")
                # Re-show the current message
                display_output(current_commit_message)
        elif response == "v" and diff_output:
            console.print(diff_output)
            # Re-show the current message after viewing diff
            display_output(current_commit_message)
        elif response == "d" and bool(issues) and not minimal:
            # ... existing details logic ...
            # Re-show the current message after viewing details
            display_output(current_commit_message)
        elif response == "r" and message:
            logger.info("Regenerating commit message...")
            console.print("[cyan]🔄 Regenerating commit message...[/]")
            # Call generate_commit_message again (force no_cache for regeneration)
            new_commit_msg = generate_commit_message(
                diff_output,
                modified_files,
                infuscate,
                verbose,
                no_cache=True,  # Force regeneration, ignore cache
            )
            if new_commit_msg.startswith("Error:"):
                logger.warning(
                    "AI commit message regeneration failed (%s).", new_commit_msg
                )
                console.print(f"[yellow]⚠️ Regeneration failed: {new_commit_msg}[/]")
                # Keep the previous message and re-prompt
                display_output(current_commit_message)
            else:
                logger.info("Successfully regenerated commit message.")
                current_commit_message = new_commit_msg  # Update the message
                # Display the *new* message before re-prompting
                display_output(current_commit_message)
            continue  # Loop back to prompt again
        else:
            logger.warning(
                "Invalid input received or action not applicable: %s", response
            )
            # Re-display might be needed here if state allows
            if message:
                display_output(current_commit_message)


# --- CLI Definition ---
def get_package_version() -> str:
    try:
        # Use the new package name here
        return importlib.metadata.version("git-auto")
    except importlib.metadata.PackageNotFoundError:
        # Fallback if package not installed (e.g., during development)
        # Try reading from pyproject.toml as a fallback?
        # For now, return unknown
        return "unknown"


@click.group()
# Update package_name for version option
@click.version_option(
    version=get_package_version(),
    package_name="git-auto",
    message="%(package)s version %(version)s",
)
def cli() -> None:
    """AI-powered Git commit helper"""
    pass


@cli.command()
@click.option(
    "--verbose", "-v", is_flag=True, help="Enable verbose (DEBUG) logging output."
)
@click.option(
    "--infuscate",
    "-i",
    is_flag=True,
    help="Sanitize sensitive data before sending to AI.",
)
@click.option(
    "--minimal", "-m", is_flag=True, help="Show minimal output and suppress INFO logs."
)  # Updated help
@click.option(
    "--no-cache", is_flag=True, help="Force AI calls, bypassing any cached responses."
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Run analysis and generate message, but do not commit.",
)  # Add dry-run flag
def commit(
    verbose: bool, infuscate: bool, minimal: bool, no_cache: bool, dry_run: bool
) -> None:  # Add dry_run parameter
    # Set log level based on flags (verbose takes precedence over minimal)
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose logging enabled.")
    elif minimal:
        logging.getLogger().setLevel(logging.WARNING)  # Suppress INFO and DEBUG
        # No need to log here as INFO is suppressed
    else:
        logging.getLogger().setLevel(logging.INFO)

    # Use console print for user-facing start message, unaffected by log level
    console.print("[cyan]🚀 Starting Git AI Commit Helper...[/]")
    if dry_run:
        console.print("[yellow]-- Dry Run Mode Enabled --[/]")

    # --- Main Commit Loop (Handles Revert) ---
    while True:
        try:
            config = load_config()

            # Check if inside a git repo (do this inside loop in case revert fails initially?)
            logger.info("Checking Git repository status...")
            check_git_repo()

            # Check if a previous commit exists (HEAD is valid)
            can_revert = False
            try:
                head_check = subprocess.run(
                    ["git", "rev-parse", "--verify", "HEAD"],
                    check=True,
                    capture_output=True,
                )
                if head_check.returncode == 0:
                    can_revert = True
                    logger.debug(
                        "Previous commit found, revert option will be available."
                    )
            except (subprocess.CalledProcessError, FileNotFoundError):
                logger.debug(
                    "No previous commit found (or git error), revert option disabled."
                )
                can_revert = False

            logger.info("Checking staged changes...")
            diff_output: str = get_git_diff()

            # --- Allow proceeding if revert is possible, even with no diff ---
            if not diff_output and not can_revert:
                console.print(
                    "[yellow]No staged changes found and no previous commit to revert. Nothing to do.[/]"
                )
                sys.exit(0)

            # --- Perform analysis only if there are changes ---
            if diff_output:
                logger.info("Analyzing modified files...")
                modified_files: Dict[str, Any] = get_modified_files()
                if not modified_files:
                    console.print(
                        "[yellow]No modified files detected in staging area.[/]"
                    )
                    pass  # Allow proceeding if diff exists (e.g., mode change)

                logger.info("Running local validation checks...")
                syntax_issues = check_syntax_errors(modified_files)
                char_issues = check_unsupported_chars(modified_files)
                all_issues = syntax_issues + char_issues

                if all_issues:
                    local_issues_table = Table(
                        title="[bold yellow]Local Validation Issues Found[/]",
                        show_header=True,
                        header_style="bold magenta",
                        border_style="dim",
                    )
                    local_issues_table.add_column("File", style="cyan", no_wrap=True)
                    local_issues_table.add_column("Issue", style="yellow")
                    for issue in all_issues:
                        logger.warning(
                            f"Local validation issue - {issue['file']}: {issue['error']}"
                        )
                        local_issues_table.add_row(issue["file"], issue["error"])
                    console.print(local_issues_table)

                    if not click.confirm(
                        click.style(
                            "\n❓ Proceed with AI analysis despite local validation issues?",
                            fg="yellow",
                        ),
                        default=False,
                    ):
                        logger.info("Commit cancelled due to local validation issues.")
                        sys.exit(0)
                else:
                    logger.info("Local validation passed.")
                    console.print("[green]✅ Local validation passed.[/]")

                if infuscate:
                    logger.info("Data infuscation ENABLED")

                logger.info("Analyzing code with AI (Validation)...")
                validation_report: str = validate_code_changes(
                    diff_output, modified_files, infuscate, verbose, no_cache=no_cache
                )

                logger.info("Generating commit message with AI...")
                commit_msg: str = generate_commit_message(
                    diff_output, modified_files, infuscate, verbose, no_cache=no_cache
                )

                if commit_msg.startswith("Error:"):
                    logger.warning(
                        f"AI commit message generation failed ({commit_msg})."
                    )
                    logger.info("Generating fallback commit message...")
                    commit_msg = generate_fallback_message(modified_files)
                    logger.info(f'Using fallback: "{commit_msg}"')
            else:
                # No diff, so no analysis needed
                modified_files = {}
                validation_report = None
                commit_msg = None
                all_issues = []  # No local issues if no diff
                console.print(
                    "[cyan]No staged changes detected. Options available: Revert / No.[/]"
                )

            # 4. User Approval - Pass can_revert flag and potentially None for message/report
            approval_result: Optional[str] = get_user_approval(
                commit_msg,  # Can be None
                validation_report,  # Can be None
                diff_output,  # Can be empty string
                config,
                minimal,
                can_revert=can_revert,  # Pass the flag
                modified_files=modified_files,  # Pass modified_files
                infuscate=infuscate,  # Pass infuscate
                verbose=verbose,  # Pass verbose
                no_cache=no_cache,  # Pass no_cache
            )

            # 5. Handle Approval Result
            if approval_result == REVERT_ACTION:
                logger.info("User requested revert.")
                if dry_run:
                    console.print(
                        "[yellow]-- Dry Run: Skipping actual git reset --soft HEAD~1 --[/]"
                    )
                    console.print("[cyan]Restarting analysis process...[/]")
                    time.sleep(1)  # Brief pause for user to see message
                    continue  # Restart the loop
                else:
                    try:
                        console.print(
                            "[yellow]Reverting last commit (git reset --soft HEAD~1)...[/]"
                        )
                        reset_result = subprocess.run(
                            ["git", "reset", "--soft", "HEAD~1"],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        logger.info("Successfully reverted last commit.")
                        logger.debug("Git reset output: %s", reset_result.stdout)
                        console.print(
                            "[green]✅ Last commit reverted. Re-analyzing staged changes...[/]"
                        )
                        time.sleep(1)
                        continue  # Restart the loop
                    except subprocess.CalledProcessError as e:
                        logger.error("Failed to revert last commit:", exc_info=False)
                        logger.error(f"Git stderr:\n{e.stderr}")
                        console.print(f"[bold red]❌ Error reverting last commit:[/]")
                        console.print(Text(e.stderr or str(e)))
                        sys.exit(1)
                    except FileNotFoundError:
                        logger.error("'git' command not found during revert.")
                        console.print("[bold red]❌ Error: 'git' command not found.[/]")
                        sys.exit(1)

            elif approval_result:
                # Commit approved (or edited)
                approved_msg = approval_result
                if dry_run:
                    logger.info("Dry run: Skipping actual git commit.")
                    console.print("[yellow]-- Dry Run: Commit Skipped --[/]")
                    console.print("Commit message that would be used:")
                    console.print(
                        Panel(
                            approved_msg,
                            title="[blue]Final Commit Message[/]",
                            border_style="blue",
                        )
                    )
                    sys.exit(0)
                else:
                    logger.info("Executing git commit...")
                    try:
                        result: subprocess.CompletedProcess = subprocess.run(
                            ["git", "commit", "-m", approved_msg],
                            check=True,
                            capture_output=True,
                            text=True,
                        )
                        logger.debug(f"Git commit stdout:\n{result.stdout}")
                        logger.info("Committed successfully.")
                        console.print("[green]✅ Committed successfully.[/]")
                        sys.exit(0)
                    except subprocess.CalledProcessError as e:
                        logger.error(f"Git commit command failed:", exc_info=False)
                        logger.error(f"Git stderr:\n{e.stderr}")
                        console.print(f"[bold red]❌ Error during git commit:[/]")
                        console.print(Text(e.stderr or str(e)))
                        sys.exit(1)
            else:
                # User cancelled (N)
                logger.info("Commit cancelled by user.")
                console.print("[yellow]Commit cancelled by user.[/]")
                sys.exit(0)

            break  # Exit loop if commit happened or was cancelled

        # ... Error Handling for the loop iteration ...
        except ValueError as e:
            logger.error(f"Configuration Error: {str(e)}", exc_info=verbose)
            console.print(f"[bold red]❌ Configuration Error:[/]")
            console.print(Text(str(e)))
            sys.exit(1)
        except RuntimeError as e:
            logger.error(f"Runtime Error: {str(e)}", exc_info=verbose)
            console.print(f"[bold red]❌ Runtime Error:[/]")
            console.print(Text(str(e)))
            sys.exit(1)
        except subprocess.CalledProcessError as e:
            logger.error(f"Git command failed unexpectedly:", exc_info=verbose)
            logger.error(f"Git stderr:\n{e.stderr}")
            console.print(f"[bold red]❌ Git command failed unexpectedly:[/]")
            console.print(Text(e.stderr or str(e)))
            sys.exit(1)
        except Exception as e:
            logger.critical(f"An unexpected error occurred: {str(e)}", exc_info=True)
            console.print(f"[bold red]❌ An unexpected error occurred:[/]")
            console.print(Text(str(e)))
            sys.exit(1)


@cli.command(name="clear-cache")
def clear_cache() -> None:
    """Removes all cached AI responses."""
    logger = logging.getLogger(__name__)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        config = load_config()
        cache_dir = config.cache_dir
        if not cache_dir.exists():
            logger.info(
                "Cache directory does not exist (or is not configured): %s", cache_dir
            )
            console.print(f"[yellow]Cache directory not found: {cache_dir}[/]")
            sys.exit(0)

        if not cache_dir.is_dir():
            logger.error("Configured cache path is not a directory: %s", cache_dir)
            console.print(
                f"[bold red]❌ Error: Cache path is not a directory: {cache_dir}[/]"
            )
            sys.exit(1)

        logger.info("Attempting to clear cache directory: %s", cache_dir)
        if click.confirm(
            f"Are you sure you want to delete all contents of {cache_dir}?",
            default=False,
        ):
            try:
                items_deleted = 0
                items_failed = 0
                for item in cache_dir.iterdir():
                    try:
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                        items_deleted += 1
                        logger.debug("Removed cache item: %s", item.name)
                    except OSError as e:
                        items_failed += 1
                        logger.warning(
                            "Failed to remove cache item %s: %s", item.name, e
                        )

                if items_failed == 0:
                    msg = f"Successfully cleared {items_deleted} items from cache: {cache_dir}"
                    logger.info(msg)
                    console.print(f"[green]✅ {msg}[/]")
                else:
                    msg = f"Cleared {items_deleted} items, but failed to remove {items_failed} items from cache: {cache_dir}"
                    logger.warning(msg)
                    console.print(f"[yellow]⚠️ {msg}[/]")
                sys.exit(0)

            except Exception as e:
                logger.error(
                    "Failed to clear cache directory %s: %s",
                    cache_dir,
                    e,
                    exc_info=True,
                )
                console.print(f"[bold red]❌ Error clearing cache: {e}[/]")
                sys.exit(1)
        else:
            logger.info("Cache clear cancelled by user.")
            console.print("[yellow]Cache clear cancelled.[/]")
            sys.exit(0)

    except ValueError as e:
        logger.error(
            f"Configuration Error loading cache path: {str(e)}", exc_info=False
        )
        console.print(f"[bold red]❌ Configuration Error:[/]")
        console.print(Text(str(e)))
        sys.exit(1)
    except Exception as e:
        logger.critical(
            f"An unexpected error occurred during cache clear: {str(e)}", exc_info=True
        )
        console.print(f"[bold red]❌ An unexpected error occurred:[/]")
        console.print(Text(str(e)))
        sys.exit(1)


@cli.command(name="install-hook")
def install_hook() -> None:
    """Installs the mycli pre-commit hook into the current Git repository."""
    logger = logging.getLogger(__name__)
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    try:
        # 1. Check if inside a git repo and find root
        logger.debug("Checking for Git repository root.")
        git_root_proc = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            cwd=Path.cwd(),
        )
        if git_root_proc.returncode != 0:
            logger.error("Not inside a Git repository.")
            console.print("[bold red]❌ Error: Not inside a Git repository.[/]")
            sys.exit(1)
        repo_root = Path(git_root_proc.stdout.strip())
        hooks_dir = repo_root / ".git" / "hooks"
        hook_file = hooks_dir / "pre-commit"
        logger.info("Git repository found at: %s", repo_root)
        logger.info("Target hook file: %s", hook_file)

        # 2. Ensure hooks directory exists (it should, but check)
        if not hooks_dir.is_dir():
            logger.warning(".git/hooks directory not found. Attempting to create.")
            try:
                hooks_dir.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                logger.error(
                    "Failed to create .git/hooks directory: %s", e, exc_info=True
                )
                console.print(
                    f"[bold red]❌ Error: Could not create hooks directory: {hooks_dir}[/]"
                )
                console.print(f"[red]   {e}[/]")
                sys.exit(1)

        # 3. Check if hook file already exists
        overwrite = False
        if hook_file.exists():
            logger.warning("Pre-commit hook already exists: %s", hook_file)
            console.print(f"[yellow]⚠️ Pre-commit hook already exists: {hook_file}[/]")
            if not click.confirm("Overwrite existing pre-commit hook?", default=False):
                logger.info("Hook installation cancelled by user.")
                console.print("[yellow]Hook installation cancelled.[/]")
                sys.exit(0)
            overwrite = True
            logger.info("User confirmed overwrite.")

        # 4. Write the hook script
        try:
            with open(hook_file, "w", encoding="utf-8") as f:
                f.write(HookScriptContent)
            logger.info("Successfully wrote pre-commit hook script.")
        except OSError as e:
            logger.error("Failed to write pre-commit hook file: %s", e, exc_info=True)
            console.print(
                f"[bold red]❌ Error: Could not write hook file: {hook_file}[/]"
            )
            console.print(f"[red]   {e}[/]")
            sys.exit(1)

        # 5. Make the hook executable
        try:
            # Get current permissions and add execute bits
            current_stat = os.stat(hook_file)
            os.chmod(
                hook_file,
                current_stat.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH,
            )
            logger.info("Made pre-commit hook executable.")
        except OSError as e:
            logger.error("Failed to make hook executable: %s", e, exc_info=True)
            console.print(
                f"[bold red]❌ Error: Could not make hook executable: {hook_file}[/]"
            )
            console.print(
                f"[red]   You may need to run 'chmod +x {hook_file}' manually.[/]"
            )
            # Don't exit, as the hook is written, just warn

        action = "Overwrote" if overwrite else "Installed"
        console.print(
            f"[green]✅ {action} mycli pre-commit hook successfully to {hook_file}[/]"
        )
        sys.exit(0)

    except FileNotFoundError:
        logger.error("'git' command not found. Is Git installed and in PATH?")
        console.print(
            "[bold red]❌ Error: 'git' command not found. Is Git installed and in PATH?[/]"
        )
        sys.exit(1)
    except Exception as e:
        logger.critical(
            f"An unexpected error occurred during hook installation: {str(e)}",
            exc_info=True,
        )
        console.print(f"[bold red]❌ An unexpected error occurred: {str(e)}[/]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
