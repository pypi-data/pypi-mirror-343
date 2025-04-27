import re

class HyomlConfigValidator:
    """
    Validator to check the validity of Hyoml configuration rules.
    """

    def __init__(self, config: dict):
        """
        Initialize the validator with Hyoml configuration.

        Args:
            config (dict): The Hyoml configuration loaded from .hyoml file.
        """
        self.config = config

    def validate(self):
        """
        Validate the Hyoml configuration against the defined rules.

        Raises:
            ValueError: If any rule violation is detected.
        """
        self._validate_structure()
        self._validate_strict_mode()
        self._validate_embedded_content()
        self._validate_tags_and_directives()
        self._validate_multiline_strings()

    def _validate_structure(self):
        """Ensure the overall structure of the Hyoml file is valid."""
        structure = self.config.get("structure", [])
        if not isinstance(structure, list):
            raise ValueError("[HyomlConfigValidator] 'structure' must be a list.")
        # Validate individual structure rules
        for rule in structure:
            if not isinstance(rule, str):
                raise ValueError(f"[HyomlConfigValidator] Invalid structure rule: {rule}")

    def _validate_strict_mode(self):
        """Ensure strict mode rules are properly applied."""
        if self.config.get("strict_mode", False):
            # Enforce strict syntax rules
            if not self.config.get("json", {}).get("strict-booleans", False):
                raise ValueError("[HyomlConfigValidator] In strict mode, 'strict-booleans' must be enabled.")
            if not self.config.get("yaml", {}).get("indentation-sensitive", False):
                raise ValueError("[HyomlConfigValidator] In strict mode, 'indentation-sensitive' must be enabled for YAML.")

    def _validate_embedded_content(self):
        """Ensure that embedded content (e.g., <hyoml_json>, <hyoml_yaml>) is properly defined."""
        embedded_content = self.config.get("embedded_content", [])
        if not isinstance(embedded_content, list):
            raise ValueError("[HyomlConfigValidator] 'embedded_content' must be a list.")
        for rule in embedded_content:
            if not isinstance(rule, str) or not re.match(r"<hyoml_\w+>.*</hyoml_\w+>", rule):
                raise ValueError(f"[HyomlConfigValidator] Invalid embedded content rule: {rule}")

    def _validate_tags_and_directives(self):
        """Validate custom tags and directives."""
        tags_and_directives = self.config.get("directives_and_tags", [])
        if not isinstance(tags_and_directives, list):
            raise ValueError("[HyomlConfigValidator] 'directives_and_tags' must be a list.")
        for rule in tags_and_directives:
            if not isinstance(rule, str):
                raise ValueError(f"[HyomlConfigValidator] Invalid directive or tag rule: {rule}")
            if not re.match(r"^[@%]\w+", rule):
                raise ValueError(f"[HyomlConfigValidator] Invalid tag or directive format: {rule}")

    def _validate_multiline_strings(self):
        """Ensure that multiline strings are handled correctly."""
        multiline_support = self.config.get("multiline_support", [])
        if not isinstance(multiline_support, list):
            raise ValueError("[HyomlConfigValidator] 'multiline_support' must be a list.")
        for rule in multiline_support:
            if not isinstance(rule, str):
                raise ValueError(f"[HyomlConfigValidator] Invalid multiline string rule: {rule}")
            if "JSON" in rule and "triple quotes" not in rule:
                raise ValueError("[HyomlConfigValidator] JSON multiline strings must be enclosed in triple quotes (''' or \""").")
            if "YAML" in rule and "literal blocks" not in rule:
                raise ValueError("[HyomlConfigValidator] YAML multiline strings must use the '|' character.")
