# Git Auto: AI-Powered Commit Assistant

`git-auto` is a command-line tool designed to streamline your Git workflow. It leverages AI (Google Gemini) to analyze your staged code changes, perform local validation checks, generate informative Conventional Commit messages, and provide an interactive review process before committing.

## ✨ Features

*   **AI-Powered Commit Messages:** Generates commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) specification based on your staged changes.
*   **AI Code Validation:** Analyzes your diff using AI to identify potential issues, security concerns, and deviations from best practices *within the changed lines*.
*   **Local Validation:** Performs pre-commit checks for common file types:
    *   Python (`py_compile`)
    *   JavaScript/TypeScript (`node --check`, if Node.js is available)
    *   JSON (Syntax validation, basic `package.json` checks)
    *   YAML (Syntax validation via PyYAML, multi-document support, optional `yamllint` integration)
    *   Dockerfile (Basic best practice checks)
    *   Shell Scripts (`shellcheck` integration if available, basic fallback checks)
    *   TOML (Syntax validation via `toml`, basic `pyproject.toml` checks)
    *   `requirements.txt` (Checks for unpinned dependencies)
    *   Character Checks (Detects control characters, BOMs, and potentially problematic non-ASCII characters)
*   **Data Infuscation (Sanitization):** Protects sensitive data by replacing it with placeholders before sending code diffs to the AI. Supports:
    *   Built-in rules for common patterns (IPs, emails, keys, etc.).
    *   Custom regex patterns defined in an external file.
    *   Custom literal strings defined in an external file.
*   **Interactive Workflow:** Provides a prompt to review AI suggestions, edit messages, view diffs, regenerate messages, or even revert the last commit before finalizing.
*   **Configurable:** Customize behavior via a `.git_auto.yaml` file (project-specific or user-global) and environment variables.
*   **Caching:** Caches AI responses to speed up analysis of unchanged diffs and reduce API usage.
*   **Dynamic Context:** Provides the AI with an overview of your repository structure for better context.
*   **Enhanced Output:** Uses `rich` for clear, formatted terminal output and Jinja2 for customizable output templates.
*   **Git Hook Integration:** Includes a command to easily install a pre-commit hook.

## 🚀 Installation

1.  **Prerequisites:**
    *   Python 3.8+
    *   Git
    *   (Optional but Recommended) `pipx` for isolated CLI tool installation, or a Python virtual environment (`venv`).
    *   (Optional) `yamllint` and `shellcheck` installed and in your PATH for enhanced local validation.

2.  **Install via `pipx` (Recommended for CLI tools):**
    ```bash
    # Replace with the actual Git repository URL or PyPI name after publishing
    pipx install git+https://github.com/yourusername/git-auto.git 
    # Or after publishing: pipx install git-auto

    # To include optional yamllint dependency (if you have it installed):
    # pipx inject git-auto yamllint 
    ```

3.  **Install via `pip` (in a Virtual Environment):**
    *   Clone the repository:
        ```bash
        # Replace with your actual repository URL
        git clone https://github.com/yourusername/git-auto.git
        cd git-auto
        ```
    *   Create and activate a virtual environment:
        ```bash
        python -m venv .venv
        source .venv/bin/activate # Linux/macOS
        # .\.venv\Scripts\activate # Windows
        ```
    *   Install the package:
        *   **Basic:**
            ```bash
            pip install .
            ```
        *   **With optional YAML linter:**
            ```bash
            pip install ".[linter]" 
            ```
        *   **For development:**
            ```bash
            pip install -e ".[dev,linter]"
            ```

## ⚙️ Configuration

Configuration is loaded from multiple sources with the following precedence (highest first):

1.  **Environment Variables**
2.  **Configuration File (`.git_auto.yaml`)** in the current Git repository root.
3.  **Configuration File (`.git_auto.yaml`)** in the user's home directory (`~`).
4.  **Configuration File (`config.yaml`)** in `~/.config/git-auto/` (XDG standard).
5.  **Default values** defined in the tool.

**1. API Key (Required)**

You need a Google Gemini API key.

*   Get one from [Google AI Studio](https://aistudio.google.com/app/apikey).
*   **Set via Environment Variable (Recommended):**
    ```bash
    export GEMINI_API_KEY='your-api-key' 
    ```
    (Add this to your `.bashrc`, `.zshrc`, `.profile`, or equivalent)
*   **Set via Configuration File:**
    Add `api_key: your-api-key` to your `.git_auto.yaml` file.

**2. Configuration File (`.git_auto.yaml`)**

Create this YAML file in your project root or home directory to customize settings.

**Example `.git_auto.yaml`:**

```yaml
# AI Model Configuration
model: gemini-1.5-flash # Or gemini-1.5-pro, etc.

# API Key (Alternative to environment variable)
# api_key: your-api-key 

# Diff Processing
max_diff_size: 4000 # Max characters of diff sent to AI (default: 4000)

# Custom Prompt Paths (Optional)
# validation_prompt_path: /path/to/my/validation_prompt.txt
# commit_prompt_path: /path/to/my/commit_prompt.txt

# Infuscation / Sanitization (Optional)
infuscation_patterns_file: .git_auto_secrets.txt # File with custom regex patterns
infuscation_literals_file: .git_auto_literals.txt # File with custom literal strings

# Output Templating (Optional)
# standard_output_template_path: /path/to/standard_output.j2
# minimal_output_template_path: /path/to/minimal_output.j2

# Caching Configuration
cache_enabled: true             # Default: true
cache_dir: ~/.cache/git-auto # Default: User cache directory
cache_ttl_seconds: 604800       # Default: 604800 (1 week)

# AI Generation Parameters (Optional Fine-tuning)
generation_config_validation:
  temperature: 0.2            # Default: 0.2 (Lower for more deterministic validation)
  top_p: 0.95                 # Default: 0.95
  top_k: 40                   # Default: 40
  max_output_tokens: 1024     # Default: 1024

generation_config_commit:
  temperature: 0.4            # Default: 0.4 (Slightly higher for commit message creativity)
  top_p: 0.95                 # Default: 0.95
  top_k: 40                   # Default: 40
  max_output_tokens: 256      # Default: 256 (Shorter for commit messages)

# Repository Context (Optional Override - Usually generated automatically)
# repo_context: "Custom description of this project..." 
```

**3. Environment Variables**

You can override any configuration file setting using environment variables:

*   `GEMINI_API_KEY`: Your API key.
*   `MODEL`: AI model name (e.g., `gemini-1.5-pro`).
*   `MAX_DIFF_SIZE`: Max diff size in characters.
*   `VALIDATION_PROMPT_PATH`: Path to custom validation prompt file.
*   `COMMIT_PROMPT_PATH`: Path to custom commit prompt file.
*   `INFUSCATION_PATTERNS_FILE`: Path to custom infuscation regex patterns file.
*   `INFUSCATION_LITERALS_FILE`: Path to custom infuscation literal strings file.
*   `STANDARD_OUTPUT_TEMPLATE_PATH`: Path to custom standard output Jinja2 template.
*   `MINIMAL_OUTPUT_TEMPLATE_PATH`: Path to custom minimal output Jinja2 template.
*   `CACHE_ENABLED`: Set to `false` or `0` to disable caching.
*   `CACHE_DIR`: Path to the cache directory.
*   `CACHE_TTL_SECONDS`: Cache time-to-live in seconds.
*   `VALIDATION_TEMP`, `VALIDATION_TOP_P`, `VALIDATION_TOP_K`, `VALIDATION_MAX_TOKENS`: Validation generation parameters.
*   `COMMIT_TEMP`, `COMMIT_TOP_P`, `COMMIT_TOP_K`, `COMMIT_MAX_TOKENS`: Commit generation parameters.
*   `REPO_CONTEXT`: Override the automatically generated repository context string.

## 🚀 Usage

**Core Workflow (`commit` command):**

1.  **Make changes** to your code.
2.  **Stage the changes** you want to include in the commit:
    ```bash
    git add <file1> <file2>... 
    # or
    git add -A 
    ```
3.  **Run `git-auto` instead of `git commit`:**
    ```bash
    git-auto commit 
    ```
    *(You can add options like `--infuscate`, `--minimal`, etc.)*
4.  **Review Output:** The tool will display:
    *   Local validation results (if any issues are found).
    *   AI Validation Status (`PASSED`, `PASSED WITH WARNINGS`, `NEEDS REVISION`).
    *   AI Proposed Commit Message.
5.  **Interactive Prompt:** Choose your next action:
    *   `[Y]es`: Accepts the proposed (or edited) commit message and performs `git commit`.
    *   `[N]o`: Cancels the operation without committing.
    *   `[E]dit`: Opens your default Git editor (`$EDITOR` or `vim`/`nano`) to modify the proposed commit message. After saving and closing, you'll be asked to confirm the edited message.
    *   `[V]iew diff`: Displays the full staged diff using your system's pager.
    *   `[R]egenerate`: Asks the AI to generate a new commit message based on the same diff (bypasses cache).
    *   `[D]etails`: (Only shown if AI validation found issues and `--minimal` is not used) Displays a detailed table of the issues identified by the AI.
    *   `[Z]Revert last & retry`: (Only shown if a previous commit exists) Performs `git reset --soft HEAD~1` to undo the last commit (keeping changes staged) and restarts the `git-auto` analysis process. Use this if you accidentally committed too early or want to refine the previous commit with the current changes.

**Command-Line Options (`commit` command):**

*   `--infuscate`, `-i`: Enables data sanitization (built-in rules + custom patterns/literals) before sending the diff to the AI.
*   `--minimal`, `-m`: Reduces output during the approval step, showing only the validation status line and the proposed commit message. Also suppresses `INFO` level log messages.
*   `--verbose`, `-v`: Enables detailed `DEBUG` level logging, showing internal steps, full prompts sent to AI, raw AI responses, etc.
*   `--no-cache`: Forces new calls to the AI, ignoring any previously cached responses for the current diff.
*   `--dry-run`: Performs all analysis and generation steps but skips the final `git commit` execution. Shows the commit message that *would* have been used.

**Other Commands:**

*   `git-auto clear-cache`: Finds the configured cache directory and interactively prompts to remove all cached AI responses.
*   `git-auto install-hook`: Attempts to install the Git pre-commit hook script into the current repository's `.git/hooks/pre-commit` file. Will prompt before overwriting an existing hook.
*   `git-auto --version`: Displays the installed version of the tool.

## ✨ Features Deep Dive

**AI Validation:**
The AI analyzes *only the changed lines* in your diff against general programming best practices, potential security concerns, and common configuration pitfalls. It assigns severity levels (CRITICAL, HIGH, MEDIUM, LOW) based on the potential impact of the *changes*. The goal is to catch significant issues before committing.

**Commit Message Generation:**
The AI generates messages following the Conventional Commits standard. It attempts to infer the appropriate type (`feat`, `fix`, `chore`, etc.) and scope based on the diff content and file paths. The subject line summarizes the primary action, and the body provides context based *only* on the diff.

**Infuscation/Sanitization (`--infuscate`):**
When enabled, this feature protects potentially sensitive information before it leaves your machine.
*   **Built-in Rules:** Automatically detect and replace common patterns like IP addresses (excluding private ranges), email addresses, UUIDs, API keys, secrets/passwords/tokens found in common config formats, and hostnames.
*   **Custom Regex Patterns:** Define your own regular expressions (one per line) in the file specified by `infuscation_patterns_file` (e.g., `.git_auto_secrets.txt`) to catch project-specific sensitive data formats.
*   **Custom Literal Strings:** Define exact strings (one per line) in the file specified by `infuscation_literals_file` (e.g., `.git_auto_literals.txt`) that should always be replaced. Longer literals are replaced before shorter ones to handle overlaps correctly.
*   **Placeholders:** Replaced data uses placeholders like `IP-1`, `API-KEY-abcdef12`, `LITERAL-1-1234abcd`, etc. The original values are restored in the AI's response before it's displayed to you.

**Local Validation:**
Before calling the AI, the tool runs quick local checks on modified files:
*   **Python:** Checks syntax using `py_compile`.
*   **JS/TS:** Checks syntax using `node --check` (requires Node.js).
*   **JSON:** Validates JSON syntax. Checks for required `name` and `version` in `package.json`.
*   **YAML:** Validates YAML syntax using PyYAML (handles multi-document files). Optionally uses `yamllint` for stricter checks if installed.
*   **Dockerfile:** Basic checks (e.g., `apt-get update` without `rm`, using `latest` tag, `ADD` with URL).
*   **Shell:** Uses `shellcheck` for detailed linting if installed. Falls back to basic checks (missing `set -euo pipefail`, deprecated backticks ``).
*   **TOML:** Validates TOML syntax using `toml`. Checks for required sections/keys in `pyproject.toml`.
*   **requirements.txt:** Warns about potentially unpinned dependencies (lines without version specifiers like `==`, `>=`, etc.).
*   **Characters:** Detects non-ASCII printable characters (potential typos/homographs), control characters, and UTF-8 BOMs.

**Caching:**
AI responses are cached locally based on the AI model and the exact prompt sent (including the diff, context, etc.). This avoids repeated API calls for the same analysis. Configure via `cache_enabled`, `cache_dir`, `cache_ttl_seconds`, or bypass with `--no-cache`. Use `git-auto clear-cache` to empty the cache.

**Dynamic Repo Context:**
The tool automatically scans your repository's directory structure (up to a certain depth, ignoring common temporary/build directories) and includes this overview in the prompt sent to the AI. This helps the AI understand the context of the changes better.

**Output Formatting (Rich & Jinja2):**
Terminal output uses the `rich` library for better readability (panels, tables, colors). The final approval screen is rendered using Jinja2 templates. You can customize the standard and minimal output formats by providing your own Jinja2 template files via the `standard_output_template_path` and `minimal_output_template_path` configuration options. The following variables are available in the template context:
*   `validation_status`: Raw status line (e.g., "VALIDATION: PASSED").
*   `validation_status_colored`: Status line with ANSI colors.
*   `issues`: Dictionary of issues keyed by severity (`{'CRITICAL': [...], 'HIGH': [...]}`).
*   `commit_message`: Proposed commit message string.
*   `has_issues`: Boolean indicating if validation found issues.
*   `minimal_mode`: Boolean indicating if `--minimal` was used.
*   `severity_order`: List of severities for ordered iteration: `["CRITICAL", "HIGH", "MEDIUM", "LOW", "PRACTICAL"]`.

## ↩️ Integrating with Git Hooks

Use `git-auto install-hook` to automatically add a `pre-commit` script to your current repository's `.git/hooks/` directory. This script will run `git-auto commit` every time you execute `git commit`. If the tool cancels the commit (e.g., you select 'n' or an error occurs), the `git commit` process will be aborted.

Alternatively, configure it manually or using a framework like [pre-commit](https://pre-commit.com/).

## 🛠️ Development

1.  **Install:** `pip install -e ".[dev,linter]"`
2.  **Run Tests:** `pytest`
3.  **Format & Lint:** `ruff format . && ruff check --fix .`
4.  **Type Check:** `mypy git_auto/src`

## ⚠️ Troubleshooting

*   **`ModuleNotFoundError: No module named 'git_auto'`:** This usually means the package wasn't installed correctly after cloning or renaming. Ensure you have renamed the source directory to `git_auto` (with an underscore) and run `pip uninstall git-auto git-auto-commit mycli -y` followed by `pip install .` (or `pip install -e .`) from the project root.
*   **API Key Errors:** Ensure your `GEMINI_API_KEY` is correctly set either as an environment variable or in your `.git_auto.yaml` file and that the key is valid.
*   **Configuration Not Loading:** Check the search paths mentioned in the Configuration section. Ensure your file is named correctly (`.git_auto.yaml` or `config.yaml` in the XDG path) and has valid YAML syntax. Environment variables always override file settings.

## 🤝 Contributing

(Placeholder - Add contribution guidelines if desired)

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
