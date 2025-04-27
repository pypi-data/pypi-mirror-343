import pytest
from click.testing import CliRunner
from unittest.mock import patch, MagicMock, ANY
import subprocess
import importlib.metadata
import shutil
from pathlib import Path

from git_auto.src.cli import cli
from git_auto.src.config import AppConfig

# --- Constants for Mocks ---
MOCK_DIFF = "diff --git a/file.py b/file.py..."
MOCK_FILES = {"file.py": {"status": "M", "extension": ".py", "content": "print(1)"}}
MOCK_VALIDATION_REPORT_PASS = "VALIDATION: PASSED\nSUMMARY: OK"
MOCK_VALIDATION_REPORT_FAIL = """
VALIDATION: NEEDS REVISION
CRITICAL ISSUES:
- Critical issue 1 - file.py
MEDIUM ISSUES:
- Medium issue A - file.py
- Medium issue B - other.py
LOW ISSUES:
- Low issue X - file.py
PRACTICAL PROBLEMS:
- Practical problem Y - file.py
SUMMARY: Needs work
""".strip()
MOCK_COMMIT_MSG = "fix: update file.py"
MOCK_EDITED_COMMIT_MSG = "feat: improve file.py"
MOCK_REGENERATED_COMMIT_MSG = "feat: enhance file.py significantly"
MOCK_STD_TEMPLATE_JINJA = """
STD REPORT:
{{ validation_status_colored }}
{% if issues %}
--- Validation Issues ---
{{ '{:<10}'.format('Severity') }} | {{ '{:<60}'.format('Description') }}
{{ '-' * 73 }}
{% for severity in severity_order %}
{%   if severity in issues %}
{%     for issue_desc in issues[severity] %}
{{ '{:<10}'.format(severity) }} | {{ '{:<60}'.format(issue_desc if issue_desc|length <= 60 else issue_desc[:57] + '...') }}
{%     endfor %}
{%   endif %}
{% endfor %}
{{ '-' * 73 }}
{% endif %}
COMMIT:
{{ commit_message }}
"""
MOCK_MIN_TEMPLATE_JINJA = (
    "MIN REPORT: {{ validation_status_colored }}\nCOMMIT:\n{{ commit_message }}"
)

# --- Fixtures ---


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mock_config_instance(mocker):
    """Provides a mock AppConfig instance."""
    mock_cfg = AppConfig(GEMINI_API_KEY="test_key")
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    return mock_cfg


@pytest.fixture
def mock_dependencies(mocker, mock_config_instance):
    """Mocks external dependencies for cli.commit."""
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())
    mock_check_git_repo = mocker.patch("git_auto.src.cli.check_git_repo")
    mock_get_git_diff = mocker.patch(
        "git_auto.src.cli.get_git_diff", return_value=MOCK_DIFF
    )
    mock_get_modified_files = mocker.patch(
        "git_auto.src.cli.get_modified_files", return_value=MOCK_FILES
    )
    mock_check_syntax = mocker.patch(
        "git_auto.src.cli.check_syntax_errors", return_value=[]
    )
    mock_check_chars = mocker.patch(
        "git_auto.src.cli.check_unsupported_chars", return_value=[]
    )
    mock_validate_ai = mocker.patch(
        "git_auto.src.cli.validate_code_changes",
        return_value=MOCK_VALIDATION_REPORT_PASS,
    )
    mock_generate_ai = mocker.patch(
        "git_auto.src.cli.generate_commit_message", return_value=MOCK_COMMIT_MSG
    )
    mock_subprocess_run = mocker.patch("git_auto.src.cli.subprocess.run")
    mock_click_edit = mocker.patch(
        "git_auto.src.cli.click.edit", return_value=MOCK_EDITED_COMMIT_MSG
    )
    mock_load_template = mocker.patch("git_auto.src.cli._load_output_template")
    mock_load_template.side_effect = (
        lambda filename, custom_path=None: MOCK_STD_TEMPLATE_JINJA
        if filename == "standard_output.txt"
        else MOCK_MIN_TEMPLATE_JINJA
        if filename == "minimal_output.txt"
        else "ERROR_LOADING_TEMPLATE"
    )
    mock_pager = mocker.patch("git_auto.src.cli.click.echo_via_pager")
    # Add mock for the HEAD check subprocess call
    mock_head_check = mocker.patch("git_auto.src.cli.subprocess.run")
    # Default behavior: assume HEAD exists, allow revert
    mock_head_check.return_value = MagicMock(returncode=0)

    return {
        "check_git_repo": mock_check_git_repo,
        "get_git_diff": mock_get_git_diff,
        "get_modified_files": mock_get_modified_files,
        "check_syntax": mock_check_syntax,
        "check_chars": mock_check_chars,
        "validate_ai": mock_validate_ai,
        "generate_ai": mock_generate_ai,
        "subprocess_run": mock_subprocess_run,
        "click_edit": mock_click_edit,
        "load_template": mock_load_template,
        "pager": mock_pager,
        "config_instance": mock_config_instance,
        "console": mock_console,
        "head_check": mock_head_check,  # Mock for the initial HEAD check
    }


# --- CLI Tests ---


def test_cli_version_flag(runner):
    """Test the --version flag."""
    with patch(
        "git_auto.src.cli.importlib.metadata.version", return_value="0.1.0-test"
    ):
        result = runner.invoke(cli, ["--version"])
    assert result.exit_code == 0
    assert "git-auto-commit version 0.1.0-test" in result.output


def test_commit_successful_run(runner, mock_dependencies):
    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["subprocess_run"].assert_called_once_with(
        ["git", "commit", "-m", MOCK_COMMIT_MSG],
        check=True,
        capture_output=True,
        text=True,
    )


def test_commit_command_no_changes(runner, mock_dependencies):
    """Test the command when git diff returns empty."""
    mock_dependencies["get_git_diff"].return_value = ""

    result = runner.invoke(cli, ["commit"])

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(
        "[yellow]No staged changes found. Use 'git add' first.[/]"
    )
    mock_dependencies["validate_ai"].assert_not_called()


def test_commit_command_local_validation_fail_proceed(
    runner, mock_dependencies, mocker
):
    """Test when local validation fails but user proceeds."""
    mock_dependencies["check_syntax"].return_value = [
        {"file": "bad.py", "error": "Syntax Error!"}
    ]
    mocker.patch("git_auto.src.cli.click.confirm", return_value=True)

    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    assert "Proceed with AI analysis despite local validation issues?" in result.output
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_command_local_validation_fail_cancel(runner, mock_dependencies, mocker):
    """Test when local validation fails and user cancels."""
    mock_dependencies["check_syntax"].return_value = [
        {"file": "bad.py", "error": "Syntax Error!"}
    ]
    mocker.patch("git_auto.src.cli.click.confirm", return_value=False)

    result = runner.invoke(cli, ["commit"], input="n\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    assert "Proceed with AI analysis despite local validation issues?" in result.output
    mock_dependencies["validate_ai"].assert_not_called()
    mock_dependencies["subprocess_run"].assert_not_called()


def test_commit_command_user_cancel_commit(runner, mock_dependencies):
    """Test when user cancels at the final commit confirmation."""
    result = runner.invoke(cli, ["commit"], input="n\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    assert "Commit with this message?" in result.output
    mock_dependencies["console"].print.assert_any_call(
        "[yellow]Commit cancelled by user.[/]"
    )
    mock_dependencies["subprocess_run"].assert_not_called()


def test_commit_successful_run_uses_standard_template(runner, mock_dependencies):
    """Test successful run uses the standard output template."""
    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["load_template"].assert_called_once_with(
        "standard_output.txt", None
    )
    assert "STD REPORT:" in result.output
    assert "MIN REPORT:" not in result.output
    assert MOCK_COMMIT_MSG in result.output
    assert "--- Validation Issues ---" not in result.output
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_minimal_output_uses_minimal_template(runner, mock_dependencies):
    """Test --minimal flag uses the minimal output template."""
    result = runner.invoke(cli, ["commit", "--minimal"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["load_template"].assert_called_once_with(
        "minimal_output.txt", None
    )
    assert "MIN REPORT:" in result.output
    assert "STD REPORT:" not in result.output
    assert MOCK_COMMIT_MSG in result.output
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_uses_custom_standard_template_path(runner, mock_dependencies):
    """Test that a custom standard template path from config is used."""
    custom_path = "/custom/standard.txt"
    mock_dependencies["config_instance"].standard_output_template_path = custom_path

    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["load_template"].assert_called_once_with(
        "standard_output.txt", custom_path
    )
    assert "STD REPORT:" in result.output
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_uses_custom_minimal_template_path(runner, mock_dependencies):
    """Test that a custom minimal template path from config is used."""
    custom_path = "/custom/minimal.txt"
    mock_dependencies["config_instance"].minimal_output_template_path = custom_path

    result = runner.invoke(cli, ["commit", "--minimal"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["load_template"].assert_called_once_with(
        "minimal_output.txt", custom_path
    )
    assert "MIN REPORT:" in result.output
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_template_load_error_fallback(runner, mock_dependencies):
    """Test fallback output when template loading fails."""
    fallback_template = "Validation: {{ validation_status_colored }}\n{% if issues %}{{ issues_table }}{% endif %}\n\nCommit Message:\n{{ commit_message }}"
    mock_dependencies["load_template"].return_value = fallback_template

    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    assert "Validation Report:" in result.output
    assert "Commit Message:" in result.output
    assert "STD REPORT:" not in result.output
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_final_git_commit_fails(runner, mock_dependencies):
    """Test when the actual 'git commit' subprocess call fails."""
    mock_dependencies["subprocess_run"].side_effect = subprocess.CalledProcessError(
        1, ["git", "commit"], stderr="commit hook failed"
    )

    result = runner.invoke(cli, ["commit"])

    assert result.exit_code == 1
    mock_dependencies["console"].print.assert_any_call(
        "[red]❌ Error during git commit: commit hook failed[/]"
    )


def test_commit_with_infuscate(runner, mock_dependencies):
    """Test that the infuscate flag is passed down."""
    result = runner.invoke(cli, ["commit", "--infuscate"])

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(
        "[blue]Data infuscation ENABLED[/]"
    )
    mock_dependencies["validate_ai"].assert_called_once_with(
        MOCK_DIFF, MOCK_FILES, True, False
    )
    mock_dependencies["generate_ai"].assert_called_once_with(
        MOCK_DIFF, MOCK_FILES, True, False
    )


def test_commit_with_verbose(runner, mock_dependencies):
    """Test that the verbose flag is passed down."""
    result = runner.invoke(cli, ["commit", "--verbose"])

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call("[blue]Verbose mode ENABLED[/]")
    mock_dependencies["validate_ai"].assert_called_once_with(
        MOCK_DIFF, MOCK_FILES, False, True
    )
    mock_dependencies["generate_ai"].assert_called_once_with(
        MOCK_DIFF, MOCK_FILES, False, True
    )


def test_commit_ai_commit_gen_fails_uses_fallback(runner, mock_dependencies):
    """Test when AI commit generation fails, CLI uses fallback and proceeds."""
    ai_error_msg = "Error: Could not generate commit message due to API error."
    fallback_msg = "refactor: modify file.py"
    mock_dependencies["generate_ai"].return_value = ai_error_msg

    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(
        "[yellow]AI commit message generation failed: Error: Could not generate commit message due to API error.[/]"
    )
    mock_dependencies["console"].print.assert_any_call(
        "[blue]Generating fallback commit message...[/]"
    )
    mock_dependencies["console"].print.assert_any_call(
        f'[green]Using fallback: "{fallback_msg}"[/]'
    )
    mock_dependencies["subprocess_run"].assert_called_once_with(
        ["git", "commit", "-m", fallback_msg],
        check=True,
        capture_output=True,
        text=True,
    )


def test_commit_user_views_diff(runner, mock_dependencies):
    """Test user viewing diff ('v') then confirming ('y')."""
    result = runner.invoke(cli, ["commit"], input="v\ny\n")

    assert result.exit_code == 0
    mock_dependencies["pager"].assert_called_once_with(MOCK_DIFF)
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_user_edits_message(runner, mock_dependencies, mocker):
    """Test user editing the commit message."""
    mocker.patch("git_auto.src.cli.click.confirm", return_value=True)
    result = runner.invoke(cli, ["commit"], input="e\ny\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    assert "Use this edited message?" in result.output
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["click_edit"].assert_called_once()
    mock_dependencies["subprocess_run"].assert_called_once_with(
        ["git", "commit", "-m", MOCK_EDITED_COMMIT_MSG],
        check=True,
        capture_output=True,
        text=True,
    )


def test_commit_ai_validation_fails_proceed(runner, mock_dependencies):
    """Test when AI validation fails but user proceeds."""
    mock_dependencies["validate_ai"].return_value = MOCK_VALIDATION_REPORT_FAIL
    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    assert "Issues detected! Proceed anyway?" in result.output
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_ai_validation_fails_view_details_then_proceed(
    runner, mock_dependencies
):
    """Test user viewing details ('d') when validation fails, then proceeding ('y')."""
    mock_dependencies["validate_ai"].return_value = MOCK_VALIDATION_REPORT_FAIL
    result = runner.invoke(cli, ["commit"], input="d\ny\n")

    assert result.exit_code == 0
    print_calls = mock_dependencies["console"].print.call_args_list
    table_print_count = sum(
        1 for call in print_calls if isinstance(call.args[0], Table)
    )
    assert table_print_count >= 2
    assert "/[D]etails" in result.output
    assert result.output.count("Issues detected! Proceed anyway?") >= 1
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_minimal_output_with_issues(runner, mock_dependencies):
    """Test --minimal flag still shows only status line even with issues."""
    mock_dependencies["validate_ai"].return_value = MOCK_VALIDATION_REPORT_FAIL
    result = runner.invoke(cli, ["commit", "--minimal"], input="y\n")

    assert result.exit_code == 0
    print_calls = mock_dependencies["console"].print.call_args_list
    table_print_count = sum(
        1 for call in print_calls if isinstance(call.args[0], Table)
    )
    assert table_print_count == 0
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(ANY)
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_user_regenerates_message(runner, mock_dependencies):
    """Test user regenerating the commit message ('r') then accepting ('y')."""
    # Mock generate_ai to return different messages on subsequent calls
    mock_dependencies["generate_ai"].side_effect = [
        MOCK_COMMIT_MSG,  # First call
        MOCK_REGENERATED_COMMIT_MSG,  # Second call (regeneration)
    ]

    # Simulate user typing 'r', then 'y'
    result = runner.invoke(cli, ["commit"], input="r\ny\n")

    assert result.exit_code == 0
    # Check that generate_ai was called twice
    assert mock_dependencies["generate_ai"].call_count == 2
    # Check the second call forced no_cache=True
    second_call_args = mock_dependencies["generate_ai"].call_args_list[1]
    assert second_call_args.kwargs.get("no_cache") is True

    # Check console output for regeneration indication
    mock_dependencies["console"].print.assert_any_call(
        "[cyan]🔄 Regenerating commit message...[/]"
    )
    # Check that the regenerated message was displayed in a panel
    # We check if print was called with a Panel containing the regenerated message
    found_regenerated_panel = False
    for call in mock_dependencies["console"].print.call_args_list:
        args = call.args
        if (
            args
            and isinstance(args[0], Panel)
            and args[0].renderable == MOCK_REGENERATED_COMMIT_MSG
        ):
            found_regenerated_panel = True
            break
    assert found_regenerated_panel, (
        "Regenerated commit message panel not found in console output"
    )

    # Check final success message
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )
    # Check that the *regenerated* message was used for the final commit
    mock_dependencies["subprocess_run"].assert_called_once_with(
        ["git", "commit", "-m", MOCK_REGENERATED_COMMIT_MSG],
        check=True,
        capture_output=True,
        text=True,
    )


def test_commit_user_regenerate_fails(runner, mock_dependencies):
    """Test handling when regeneration fails."""
    regenerate_error_msg = "Error: Regeneration failed."
    # Mock generate_ai: first call ok, second call returns error
    mock_dependencies["generate_ai"].side_effect = [
        MOCK_COMMIT_MSG,
        regenerate_error_msg,
    ]

    # Simulate user typing 'r', then 'y' (to accept the *original* message after failure)
    result = runner.invoke(cli, ["commit"], input="r\ny\n")

    assert result.exit_code == 0
    assert mock_dependencies["generate_ai"].call_count == 2
    # Check warning message was printed
    mock_dependencies["console"].print.assert_any_call(
        f"[yellow]⚠️ Regeneration failed: {regenerate_error_msg}[/]"
    )
    # Check that the *original* message was used for the final commit
    mock_dependencies["subprocess_run"].assert_called_once_with(
        ["git", "commit", "-m", MOCK_COMMIT_MSG],
        check=True,
        capture_output=True,
        text=True,
    )


def test_commit_revert_and_retry_success(runner, mock_dependencies):
    """Test user choosing revert [z], then accepting [y] on retry."""
    # Mock generate_ai to return different messages
    mock_dependencies["generate_ai"].side_effect = [
        "commit msg before revert",
        "commit msg after revert",
    ]
    # Mock subprocess.run: first call is HEAD check (mocked by head_check),
    # second call is git reset, third call is final git commit
    final_commit_mock = MagicMock(returncode=0)
    reset_mock = MagicMock(returncode=0)
    mock_dependencies["subprocess_run"].side_effect = [reset_mock, final_commit_mock]

    # Simulate user typing 'z', then 'y' for confirmation, then 'y' for final commit
    result = runner.invoke(cli, ["commit"], input="z\ny\ny\n")

    assert result.exit_code == 0
    # Check revert prompt and confirmation
    assert "/[Z]Revert last & retry" in result.output
    assert "Are you sure you want to revert the last commit" in result.output
    # Check messages indicating revert and restart
    mock_dependencies["console"].print.assert_any_call(
        "[yellow]Reverting last commit (git reset --soft HEAD~1)...[/]"
    )
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Last commit reverted. Re-analyzing staged changes...[/]"
    )
    # Check that analysis runs twice
    assert mock_dependencies["get_git_diff"].call_count == 2
    assert mock_dependencies["validate_ai"].call_count == 2
    assert mock_dependencies["generate_ai"].call_count == 2
    # Check git reset was called
    reset_mock.assert_called_once_with(
        ["git", "reset", "--soft", "HEAD~1"], check=True, capture_output=True, text=True
    )
    # Check final commit used the *second* generated message
    final_commit_mock.assert_called_once_with(
        ["git", "commit", "-m", "commit msg after revert"],
        check=True,
        capture_output=True,
        text=True,
    )
    mock_dependencies["console"].print.assert_any_call(
        "[green]✅ Committed successfully.[/]"
    )


def test_commit_revert_option_not_shown_no_head(runner, mock_dependencies):
    """Test that revert option [z] is not shown if no previous commit exists."""
    # Mock HEAD check to fail
    mock_dependencies["head_check"].side_effect = subprocess.CalledProcessError(
        1, "cmd"
    )

    # Run invoke and capture output to check prompts (user accepts immediately)
    result = runner.invoke(cli, ["commit"], input="y\n")

    assert result.exit_code == 0
    # Check that the revert option is NOT in the prompt string
    assert "/[Z]Revert last & retry" not in result.output
    assert (
        "Commit with this message? [Y]es/[N]o/[E]dit/[V]iew diff/[R]egenerate:"
        in result.output
    )
    # Check commit still happens
    mock_dependencies["subprocess_run"].assert_called_once()


def test_commit_revert_cancelled_by_user(runner, mock_dependencies):
    """Test user choosing revert [z], but cancelling the confirmation."""
    # Simulate user typing 'z', then 'n' for confirmation
    result = runner.invoke(
        cli, ["commit"], input="z\nn\n"
    )  # Need final \n if it re-prompts

    assert result.exit_code == 0  # Should exit gracefully after cancellation
    assert "Are you sure you want to revert the last commit" in result.output
    mock_dependencies["console"].print.assert_any_call("[yellow]Revert cancelled.[/]")
    # Check that git reset was NOT called
    assert not any(
        call.args[0][1] == "reset"
        for call in mock_dependencies["subprocess_run"].call_args_list
    )
    # Check that the final commit was NOT called
    assert not any(
        call.args[0][1] == "commit"
        for call in mock_dependencies["subprocess_run"].call_args_list
    )
    # Check that analysis only ran once
    assert mock_dependencies["get_git_diff"].call_count == 1


def test_commit_revert_fails(runner, mock_dependencies):
    """Test scenario where the git reset command fails."""
    # Mock subprocess.run: first call is HEAD check, second call (git reset) fails
    reset_fail_mock = MagicMock()
    reset_fail_mock.side_effect = subprocess.CalledProcessError(
        1, "git reset", stderr="Cannot reset"
    )
    mock_dependencies["subprocess_run"].side_effect = [reset_fail_mock]

    # Simulate user typing 'z', then 'y' for confirmation
    result = runner.invoke(cli, ["commit"], input="z\ny\n")

    assert result.exit_code == 1  # Should exit with error
    assert "Are you sure you want to revert the last commit" in result.output
    mock_dependencies["console"].print.assert_any_call(
        "[yellow]Reverting last commit (git reset --soft HEAD~1)...[/]"
    )
    mock_dependencies["console"].print.assert_any_call(
        "[bold red]❌ Error reverting last commit:[/]"
    )
    mock_dependencies["console"].print.assert_any_call(ANY)  # Should print the stderr
    # Check analysis only ran once
    assert mock_dependencies["get_git_diff"].call_count == 1


# --- Tests for clear-cache command ---


def test_cli_clear_cache_confirm_yes(runner, mocker, tmp_path):
    """Test 'clear-cache' command with user confirming yes."""
    cache_dir = tmp_path / "mycli_cache_test"
    cache_dir.mkdir()
    (cache_dir / "file1.json").touch()
    (cache_dir / "subdir").mkdir()
    (cache_dir / "subdir" / "file2.json").touch()

    mock_cfg = AppConfig(GEMINI_API_KEY="test_key", cache_dir=cache_dir)
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())

    result = runner.invoke(cli, ["clear-cache"], input="y\n")

    assert result.exit_code == 0
    assert (
        f"Are you sure you want to delete all contents of {cache_dir}?" in result.output
    )
    mock_console.print.assert_any_call(
        f"[green]✅ Successfully cleared 2 items from cache: {cache_dir}[/]"
    )
    assert cache_dir.exists()
    assert not list(cache_dir.iterdir())


def test_cli_clear_cache_confirm_no(runner, mocker, tmp_path):
    """Test 'clear-cache' command with user confirming no."""
    cache_dir = tmp_path / "mycli_cache_test_no"
    cache_dir.mkdir()
    cache_file = cache_dir / "file1.json"
    cache_file.touch()

    mock_cfg = AppConfig(GEMINI_API_KEY="test_key", cache_dir=cache_dir)
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())

    result = runner.invoke(cli, ["clear-cache"], input="n\n")

    assert result.exit_code == 0
    mock_console.print.assert_any_call("[yellow]Cache clear cancelled.[/]")
    assert cache_file.exists()


def test_cli_clear_cache_dir_not_exist(runner, mocker, tmp_path):
    """Test 'clear-cache' when the configured cache directory doesn't exist."""
    cache_dir = tmp_path / "non_existent_cache"
    mock_cfg = AppConfig(GEMINI_API_KEY="test_key", cache_dir=cache_dir)
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())

    result = runner.invoke(cli, ["clear-cache"])

    assert result.exit_code == 0
    mock_console.print.assert_any_call(
        f"[yellow]Cache directory not found: {cache_dir}[/]"
    )


def test_cli_clear_cache_path_is_file(runner, mocker, tmp_path):
    """Test 'clear-cache' when the configured cache path is a file, not a directory."""
    cache_file_path = tmp_path / "cache_is_a_file"
    cache_file_path.touch()
    mock_cfg = AppConfig(GEMINI_API_KEY="test_key", cache_dir=cache_file_path)
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())

    result = runner.invoke(cli, ["clear-cache"])

    assert result.exit_code == 1
    mock_console.print.assert_any_call(
        f"[red]❌ Error: Cache path is not a directory: {cache_file_path}[/]"
    )


@patch("git_auto.src.cli.shutil.rmtree")
def test_cli_clear_cache_permission_error(mock_rmtree, runner, mocker, tmp_path):
    """Test 'clear-cache' handling errors during deletion."""
    cache_dir = tmp_path / "mycli_cache_perm_err"
    cache_dir.mkdir()
    (cache_dir / "file1.json").touch()
    (cache_dir / "subdir").mkdir()

    mock_cfg = AppConfig(GEMINI_API_KEY="test_key", cache_dir=cache_dir)
    mocker.patch("git_auto.src.cli.load_config", return_value=mock_cfg)
    mock_console = mocker.patch("git_auto.src.cli.console", MagicMock())
    mock_rmtree.side_effect = OSError("Permission denied")

    result = runner.invoke(cli, ["clear-cache"], input="y\n")

    assert result.exit_code == 0
    mock_console.print.assert_any_call(
        "[yellow]Cleared 1 items, but failed to remove 1 items[/]"
    )
    assert not (cache_dir / "file1.json").exists()
    assert (cache_dir / "subdir").exists()
