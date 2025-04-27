"""
HyomlParser - Parses Hyoml hybrid files (relaxed JSON, YAML, TOML, etc.).
Supports embedded format detection via ReaderFactory.
"""

import re
from python.parser.reader_factory import ReaderFactory
from python.parser.core.relaxedjson_with_tags import RelaxedJSON
from python.parser.core.relaxedyml_with_tags import RelaxedYML

from python.parser.core.middleware.autofixer import AutoFixer
from python.parser.core.middleware.reviver import Reviver
from python.parser.core.middleware.config_validator import HyomlConfigValidator  # Importing the validator
from utils.conversion_utils import dict_to_list, list_to_dict, tuple_to_dict  # Importing conversion utilities

from python.parser.core.visitors.date_visitor import DateVisitor
from python.parser.core.visitors.tag_visitor import TagVisitor
from python.parser.core.visitors.directive_visitor import DirectiveVisitor
from python.parser.core.visitors.visitor_loader import VisitorPipeline

class HyomlParser:
    """
    Main orchestrator that handles RelaxedJSON, RelaxedYML parsing,
    smart block-based embedded format detection, tag/directive extraction,
    visitor pipeline transformations, and reviver application.
    """

    def __init__(self, options: dict = None):
        """
        Initialize the parser.

        Args:
            options (dict): Parser options and behavior settings.
        """
        self.options = options or {}
        self.strict_mode = self.options.get("strict_mode", False)

        self.reader_factory = ReaderFactory(strict_mode=self.strict_mode)
        self.json = RelaxedJSON(
            tag_key=self.options.get("tag_key", "_tags"),
            directive_key=self.options.get("directive_key", "_directives"),
            merge_tags=self.options.get("merge_tags", False)
        )
        self.yml = RelaxedYML(
            tag_key=self.options.get("tag_key", "_tags"),
            directive_key=self.options.get("directive_key", "_directives"),
            merge_tags=self.options.get("merge_tags", False)
        )

        # Validate Hyoml configuration before proceeding with parsing
        self._validate_configuration()

    def _validate_configuration(self):
        """
        Validates the Hyoml configuration rules using HyomlConfigValidator.

        Raises:
            ValueError: If the configuration is invalid.
        """
        validator = HyomlConfigValidator(self.options)
        validator.validate()

    def parse(self, text: str) -> dict:
        """
        Parse Hyoml text.

        Applies:
        - Autofix and typo correction
        - Block-wise format detection and delegation
        - Visitor pipeline
        - Reviver transformation

        Args:
            text (str): Raw Hyoml input.

        Returns:
            dict: Structured parsed result.
        """
        try:
            if 'strict' not in self.options:
                if self._detect_strict_mode(text):
                    self.options['strict'] = True

            log_autofix = self.options.get("log_autofix", False)
            fixed = AutoFixer.apply(text, level="smart", log_fixes=log_autofix)

            blocks = self._split_blocks(fixed)
            raw_result = {}

            for block in blocks:
                key, value = self._parse_block(block)
                if key is not None:
                    raw_result[key] = value
                elif isinstance(value, dict):
                    # Convert dict to list if needed
                    if self.options.get("convert_dict_to_list", False):
                        raw_result[key] = dict_to_list(value)
                    else:
                        raw_result.update(value)  # if block returns a dict, merge it
                elif isinstance(value, list):
                    # Convert list to dict if needed
                    if self.options.get("convert_list_to_dict", False):
                        raw_result[key] = list_to_dict(value)
                    else:
                        raw_result[key] = value
                elif isinstance(value, tuple):
                    # Convert tuple to dict if needed
                    if self.options.get("convert_tuple_to_dict", False):
                        raw_result[key] = tuple_to_dict(value)
                    else:
                        raw_result[key] = value

            # Apply built-in and custom visitors
            visited = VisitorPipeline.apply(
                DirectiveVisitor.visit(
                    TagVisitor.visit(
                        DateVisitor.visit(raw_result)
                    )
                ),
                self.options.get("visitors")
            )

            # Apply optional reviver
            return Reviver.apply(visited, self.options.get("reviver"), self.options)

        except Exception as e:
            print(f"Error: {e}")
            print(f"Error: {e}")
            raise ValueError(f"[HyomlParser] Parse failed: {e}")

    def _detect_strict_mode(self, text: str) -> bool:
        """
        Detect if strict mode should be activated based on input content.
        """
        strict_keywords = [
            "use strict", "strict", "strict-mode", "restricted", "restrictions",
            "enforce", "enforced", "lock", "locked", "mode=locked", "secure",
            "harden", "hardening"
        ]
        lines = text.strip().splitlines()[:5]
        for line in lines:
            normalized = line.strip().strip("'\"<>").lower()
            for keyword in strict_keywords:
                if keyword in normalized:
                    return True
        return False

    def _split_blocks(self, text: str):
        """
        Split input text into logical parsing blocks.
        """
        lines = text.strip().splitlines()
        blocks = []
        current_block = []

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if current_block:
                    blocks.append("\n".join(current_block))
                    current_block = []
            elif re.match(r"^[\\w\\-]+:", stripped):
                if current_block:
                    blocks.append("\n".join(current_block))
                current_block = [line]
            else:
                current_block.append(line)

        if current_block:
            blocks.append("\n".join(current_block))

        return blocks

    def _parse_block(self, block: str):
        """
        Parse a single block.

        Args:
            block (str): Raw block text.

        Returns:
            (key, value) tuple or (None, dict) if full block result.
        """
        block = block.strip()
        if not block:
            return {}, {}

        if ":" in block.splitlines()[0]:
            first_line = block.splitlines()[0]
            key, value_part = first_line.split(":", 1)
            key = key.strip()
            value_part = value_part.strip()

            if value_part:
                parsed_value = self._parse_inline_value(value_part)
            else:
                content = "\n".join(block.splitlines()[1:])
                parsed_value = self._try_delegate_to_readers(content)

            return key, parsed_value

        else:
            parsed_value = self._try_delegate_to_readers(block)
            return {}, parsed_value

    def _parse_inline_value(self, value_text: str):
        """
        Parse simple inline values (numbers, booleans, strings).
        """
        if value_text.lower() in ("true", "false"):
            return value_text.lower() == "true"
        try:
            if "." in value_text:
                return float(value_text)
            else:
                return int(value_text)
        except ValueError:
            return value_text.strip('"').strip("'")
            return value_text.strip('"').strip("'")

    def _try_delegate_to_readers(self, block_text: str):
        """
        Try to detect and parse using specialized Readers first,
        fallback to RelaxedJSON or RelaxedYML.
        """
        try:
            return self.reader_factory.detect_and_parse(block_text)
        except Exception:
            try:
                if "{" in block_text:
                    return self.json.parse(block_text)
                else:
                    return self.yml.parse(block_text)
            except Exception:
                return block_text.strip()
                return block_text.strip()

    def is_strict(self, rule: str) -> bool:
        """
        Check if a specific strict rule is enabled.

        Args:
            rule (str): Strict rule name.

        Returns:
            bool: True if strictly enforced.
        """
        value = self.options.get(rule)
        return value is True or value == "error"
