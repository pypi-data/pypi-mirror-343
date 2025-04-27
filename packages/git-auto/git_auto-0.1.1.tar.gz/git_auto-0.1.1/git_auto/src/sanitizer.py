import re
import hashlib
import logging
from typing import Dict, Any, Optional, List, Pattern

logger = logging.getLogger(__name__)

# Dictionary to store original values and their sanitized replacements for later reference
sanitization_mapping: Dict[str, str] = {}
reverse_mapping: Dict[str, str] = {}


# Class to handle data sanitization with consistent replacements
class DataSanitizer:
    mappings: Dict[str, Dict[str, str]]
    known_settings: List[str]
    common_domains: List[str]
    patterns: Dict[str, Pattern[str]]
    git_syntax: List[str]
    placeholder_templates: Dict[str, str]
    custom_literals: List[str]  # Add hint for literals

    def __init__(
        self,
        custom_patterns: Optional[List[str]] = None,
        custom_literals: Optional[List[str]] = None,
    ) -> None:
        """Initialize sanitizer with optional custom regex patterns and literal strings."""
        # Store mappings for consistent replacements
        self.mappings = {
            "ip": {},  # IP addresses
            "domain": {},  # Domain names
            "email": {},  # Email addresses
            "api_key": {},  # API keys
            "password": {},  # Passwords
            "token": {},  # Tokens
            "secret": {},  # Secret keys
            "uuid": {},  # UUIDs
            "url": {},  # URLs
            "hostname": {},  # Hostnames
            "username": {},  # Usernames
            "private_key": {},  # Private keys
        }

        # Store custom literals (sorted by length descending in config loading)
        self.custom_literals = custom_literals or []

        # List of known settings that shouldn't be classified as sensitive
        self.known_settings = [
            "dns01-recursive-nameservers",
            "dns01-recursive-nameservers-only",
            "scrapeTimeout",
            "targetPort",
            "logging-format",
            "interval",
            "path",
            "metrics",
            "release",
            "enabled",
            "kube-prometheus-stack",
        ]

        # Common public domains that shouldn't be obfuscated
        self.common_domains = [
            "github.com",
            "gitlab.com",
            "bitbucket.org",
            "docker.io",
            "k8s.io",
            "kubernetes.io",
            "helm.sh",
            "charts.jetstack.io",
            "quay.io",
            "gcr.io",
            "amazonaws.com",
            "azure.com",
            "googleapis.com",
        ]

        # Define comprehensive patterns for sensitive data
        self.patterns: Dict[str, Pattern[str]] = {
            # IP address (IPv4) - only obfuscate non-standard IPs
            "ip": re.compile(
                r"\b(?!127\.0\.0\.1)(?!0\.0\.0\.0)(?!255\.255\.255\.255)(?!192\.168\.[0-9]{1,3}\.[0-9]{1,3})(?!10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})(?!172\.(?:1[6-9]|2[0-9]|3[0-1])\.[0-9]{1,3}\.[0-9]{1,3})(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
            ),
            # Domain names - more specific to avoid sanitizing common file extensions and git syntax
            "domain": re.compile(
                r"\b(?!localhost)(?!example\.com)(?!test\.com)(?!internal)(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+(?:com|net|org|io|dev|app|cloud|biz|co|ai|tech)\b"
            ),
            # Email addresses
            "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            # API keys (common formats) - excluding git hash-like patterns
            "api_key": re.compile(
                r"\b(?!(?:[0-9a-f]{7,40}))([A-Za-z0-9_\-\.]{32,64})\b"
            ),
            # Passwords in config
            "password": re.compile(
                r'(?:password|pwd|passwd|pass)(?:"\s*:\s*"|\s*=\s*"|\s*=\s*\')([^"\'\s]{8,})'
            ),
            # Auth tokens
            "token": re.compile(
                r'(?:token|access_token|auth_token|jwt|bearer)(?:"\s*:\s*"|\s*=\s*"|\s*=\s*\')([^"\'\s]{8,})'
            ),
            # Secret keys
            "secret": re.compile(
                r'(?:secret|secret_key|client_secret)(?:"\s*:\s*"|\s*=\s*"|\s*=\s*\')([^"\'\s]{8,})'
            ),
            # UUIDs
            "uuid": re.compile(
                r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b",
                re.IGNORECASE,
            ),
            # URLs with credentials - more specific to avoid replacing git command output
            "url": re.compile(
                r"\bhttps?://(?:[^:@/\s]+:[^:@/\s]+@)?(?:[^:@/\s]+)(?::[0-9]+)?(?:/[^?#\s]*)?(?:\?[^#\s]*)?(?:#[^\s]*)?"
            ),
            # Hostnames - excluding common git terms and file paths and common domains
            "hostname": re.compile(
                r"\b(?!(?:git|diff|index|file|mode|new|deleted|modified|rename|copy|HEAD|master|main|dev|stage|prod)$)(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+(?!(?:com|org|io|net|gov|edu)$)[a-zA-Z]{2,}\b"
            ),
            # Private key data (Base64 encoded)
            "private_key": re.compile(
                r"-----BEGIN (?:RSA )?PRIVATE KEY-----.+?-----END (?:RSA )?PRIVATE KEY-----",
                re.DOTALL,
            ),
        }

        # Add custom patterns
        if custom_patterns:
            for i, pattern_str in enumerate(custom_patterns):
                try:
                    # Compile the custom pattern
                    custom_regex = re.compile(pattern_str)
                    # Add it with a unique key
                    pattern_key = f"custom_{i + 1}"
                    self.patterns[pattern_key] = custom_regex
                    logger.debug(
                        "Added custom infuscation pattern %s: %s",
                        pattern_key,
                        pattern_str,
                    )
                except re.error as e:
                    logger.warning(
                        "Invalid custom infuscation regex pattern skipped: '%s'. Error: %s",
                        pattern_str,
                        e,
                    )

        # Git-specific elements to never sanitize
        self.git_syntax = [
            "diff",
            "index",
            "new file",
            "deleted file",
            "mode",
            "--- a/",
            "+++ b/",
            "@@ ",
            " @@",
            "+++",
            "---",
            "diff --git",
            "index ",
            "blob",
            "file",
            "mode",
            ".yaml",
            ".yml",
            ".json",
            ".xml",
            ".md",
            ".txt",
            "/dev/null",
            "crds:",
            "extraArgs:",
            "webhook:",
            "prometheus:",
            "servicemonitor:",
            "helmCharts:",
            "namespace:",
            "releaseName:",
            "version:",
            "valuesFile:",
            "enabled:",
            "repo:",
        ]

        # Generate placeholders for different sensitive data types
        self.generate_placeholder_templates()

    def generate_placeholder_templates(self) -> None:
        """Create templates for different types of placeholders"""
        self.placeholder_templates = {
            "ip": "IP-{index}",
            "domain": "example-{index}.com",
            "email": "user-{index}@example.com",
            "api_key": "API-KEY-{hash}",
            "password": "PASSWORD-{hash}",
            "token": "TOKEN-{hash}",
            "secret": "SECRET-{hash}",
            "uuid": "uuid-{index}",
            "url": "https://example-{index}.com/resource",
            "hostname": "hostname-{index}.internal",
            "username": "user-{index}",
            "private_key": "[PRIVATE-KEY-DATA]",
            "literal": "LITERAL-{index}-{hash}",  # Placeholder for custom literals
        }
        # Add generic placeholder for custom patterns
        num_built_in = len(self.placeholder_templates)
        for i in range(1, 51):  # Assume max 50 custom patterns for placeholders
            pattern_key = f"custom_{i}"
            self.placeholder_templates[pattern_key] = (
                f"CUSTOM-{i}-{hash}"  # Use hash for uniqueness
            )

    def generate_placeholder(
        self, data_type: str, original_value: str, index: Optional[int] = None
    ) -> str:
        """Generate a consistent placeholder for a given sensitive value."""
        # Ensure the placeholder template exists
        template = self.placeholder_templates.get(data_type, "UNKNOWN-{index}-{hash}")
        if index is None:
            short_hash = hashlib.md5(original_value.encode()).hexdigest()[:8]
            # Use length of specific mapping type or a generic counter if needed
            current_index = len(self.mappings.get(data_type, {})) + 1
            placeholder = template.format(hash=short_hash, index=current_index)
        else:
            placeholder = template.format(
                index=index, hash=index
            )  # Hash might not be relevant here
        return placeholder

    def should_preserve(self, text: str, match_type: Optional[str] = None) -> bool:
        """Check if the text should be preserved (not sanitized)"""
        # Check if text is a known setting keyword
        if any(setting in text for setting in self.known_settings):
            return True

        # Check if text is a common domain that shouldn't be obfuscated
        if match_type == "domain" and any(
            domain in text for domain in self.common_domains
        ):
            return True

        # Preserve Git syntax elements
        for syntax in self.git_syntax:
            if syntax in text:
                return True

        # Preserve common file paths and patterns
        if re.search(r"^(?:\.{1,2})?/(?:[^/]+/)*[^/]+\.[a-zA-Z0-9]{1,4}$", text):
            return True

        return False

    def is_setting_key(self, text: str) -> bool:
        """Check if the text is a setting key rather than a value"""
        setting_patterns = [
            r"--[a-zA-Z0-9_-]+",  # Command line flags
            r"[a-zA-Z0-9_-]+:",  # YAML keys
        ]

        for pattern in setting_patterns:
            if re.match(pattern, text):
                return True
        return False

    def sanitize_text(self, text: str) -> str:
        """Sanitize text by replacing literals first, then regex patterns."""
        if not text:
            return text

        sanitized_text = text
        literal_type = "literal"  # Placeholder type for literals

        # --- 1. Replace Custom Literals ---
        # Ensure the mapping type exists
        if literal_type not in self.mappings:
            self.mappings[literal_type] = {}

        if self.custom_literals:
            logger.debug(
                "Applying %d custom literal replacements...", len(self.custom_literals)
            )
            # Iterate through literals (already sorted by length descending)
            for i, literal in enumerate(self.custom_literals):
                if literal in sanitized_text:
                    if literal not in self.mappings[literal_type]:
                        # Use index `i` for consistent placeholder generation
                        placeholder = self.generate_placeholder(
                            literal_type, literal, index=i + 1
                        )
                        self.mappings[literal_type][literal] = placeholder
                        sanitization_mapping[placeholder] = literal
                        reverse_mapping[literal] = placeholder
                        logger.debug("Mapping literal '%s' to %s", literal, placeholder)
                    else:
                        # Literal already mapped, get existing placeholder
                        placeholder = self.mappings[literal_type][literal]

                    # Replace all occurrences of the literal
                    # Use simple string replace, might need refinement for word boundaries if required
                    sanitized_text = sanitized_text.replace(literal, placeholder)

        # --- 2. Replace Regex Patterns ---
        lines: List[str] = sanitized_text.split(
            "\n"
        )  # Process line by line after literal replacement
        sanitized_lines: List[str] = []

        for line in lines:
            # If this is a git header or metadata line, preserve it exactly
            if any(
                syntax in line
                for syntax in [
                    "diff --git",
                    "index ",
                    "--- ",
                    "+++ ",
                    "new file",
                    "deleted file",
                ]
            ):
                sanitized_lines.append(line)
                continue

            # Otherwise, process the line for sensitive data
            sanitized_line: str = line

            # Process each pattern type
            for data_type, pattern in self.patterns.items():
                # Ensure mapping type exists
                if data_type not in self.mappings:
                    self.mappings[data_type] = {}

                # Skip if the line contains git syntax that should be preserved entirely
                if self.should_preserve(line):
                    continue

                # For other patterns, use regex find and replace
                matches = list(pattern.finditer(sanitized_line))

                # Process matches in reverse order to avoid offset issues when replacing
                for match in reversed(matches):
                    # Get the matched text
                    match_text: str = match.group(0)

                    # Skip if this is a setting key, not a value to be sanitized
                    if self.is_setting_key(match_text):
                        continue

                    # Skip if this match should be preserved
                    if self.should_preserve(match_text, data_type):
                        continue

                    # For patterns that capture groups, use the first group if it exists
                    if match.groups():
                        # Password, tokens, etc. patterns capture the value after the key
                        original_value: str = match.group(1)
                        full_match: str = match.group(0)

                        # Skip short values and common defaults that don't need sanitization
                        if len(original_value) < 8 or original_value in [
                            "localhost",
                            "example.com",
                            "test",
                            "username",
                        ]:
                            continue

                        if original_value not in self.mappings[data_type]:
                            placeholder: str = self.generate_placeholder(
                                data_type, original_value
                            )
                            self.mappings[data_type][original_value] = placeholder
                            sanitization_mapping[placeholder] = original_value
                            reverse_mapping[original_value] = placeholder

                        # Replace just the sensitive part, keep the key/identifier
                        replacement: str = full_match.replace(
                            original_value, self.mappings[data_type][original_value]
                        )
                        sanitized_line = sanitized_line.replace(full_match, replacement)
                    else:
                        # IP addresses, domains, emails, etc.
                        original_value: str = match.group(0)

                        # Skip common defaults and localhost values
                        if (
                            original_value
                            in [
                                "127.0.0.1",
                                "localhost",
                                "example.com",
                                "test.com",
                                "0.0.0.0",
                                "user@example.com",
                            ]
                            or original_value.startswith("192.168.")
                            or original_value.startswith("10.")
                            or (
                                data_type == "ip"
                                and not all(
                                    0 <= int(octet) <= 255
                                    for octet in original_value.split(".")
                                )
                            )
                        ):
                            continue

                        # Special handling for IPs in DNS settings to preserve the port part
                        if data_type == "ip" and ":" in original_value:
                            ip_part, port_part = original_value.split(":", 1)

                            if ip_part not in self.mappings[data_type]:
                                placeholder: str = self.generate_placeholder(
                                    data_type, ip_part
                                )
                                self.mappings[data_type][ip_part] = placeholder
                                sanitization_mapping[placeholder] = ip_part
                                reverse_mapping[ip_part] = placeholder

                            sanitized_line = sanitized_line.replace(
                                original_value,
                                f"{self.mappings[data_type][ip_part]}:{port_part}",
                            )
                        else:
                            if original_value not in self.mappings[data_type]:
                                placeholder: str = self.generate_placeholder(
                                    data_type, original_value
                                )
                                self.mappings[data_type][original_value] = placeholder
                                sanitization_mapping[placeholder] = original_value
                                reverse_mapping[original_value] = placeholder

                            sanitized_line = sanitized_line.replace(
                                original_value, self.mappings[data_type][original_value]
                            )

            sanitized_lines.append(sanitized_line)

        return "\n".join(sanitized_lines)

    def desanitize_text(self, text: str) -> str:
        """Restore original values from placeholders in the sanitized text"""
        if not text:
            return text

        desanitized_text: str = text

        # Replace all placeholders with their original values
        for placeholder, original in sanitization_mapping.items():
            desanitized_text = desanitized_text.replace(placeholder, original)

        return desanitized_text

    def get_sanitization_summary(self) -> str:
        """Return a summary of sanitized data for verbose output"""
        summary: List[str] = []
        total_sanitized: int = 0

        for data_type, mappings in self.mappings.items():
            if mappings:
                count: int = len(mappings)
                total_sanitized += count
                examples: List[Any] = list(mappings.items())[
                    :3
                ]  # Show up to 3 examples

                example_strs: List[str] = []
                for original, sanitized in examples:
                    # Truncate long values
                    orig_display: str = (
                        original[:40] + "..." if len(original) > 40 else original
                    )
                    example_strs.append(f"    {orig_display} → {sanitized}")

                # Add entry to summary
                summary.append(f"{data_type}: {count} items sanitized")
                if example_strs:
                    summary.append("  Examples:")
                    for example in example_strs:
                        summary.append(example)

        if not summary:
            return "No sensitive data detected or sanitized"

        return f"Sanitized {total_sanitized} sensitive items:\n" + "\n".join(summary)
