import re
from typing import Any, Dict


class RelaxedJSON:
    """
    Relaxed JSON parser with support for:
    - Single/double quotes
    - Unquoted keys
    - Reserved keywords (true, null, etc.)
    - Type casting (float, int, 1/2, 80%)
    - Trailing commas
    - Multiline values
    - <tag>, </tag>, <directive=...> recognition
    """

    def __init__(self, tag_key="_tags", directive_key="_directives", merge_tags=False):
        """
        Args:
            tag_key (str): Key name to store collected tags.
            directive_key (str): Key name to store collected directives.
            merge_tags (bool): If True, store both under a single key "tagsDirectives".
        """
        self.tag_key = tag_key
        self.directive_key = directive_key
        self.merge_tags = merge_tags

        self.reserved = {
            'true': True, 'false': False,
            'null': None, 'none': None,
            'undefined': None, 'NaN': None,
            'TRUE': True, 'FALSE': False, 'NULL': None, 'NONE': None,
            'NIL': None, 'nil': None,
            'yes': True, 'no': False,
            'maybe': 'maybe',
            'void': None, 'VOID': None,
            'unknown': None, 'UNKNOWN': None
        }

    def parse(self, text: str) -> Dict[str, Any]:
        """
        Parse relaxed JSON input text into a dictionary.

        Args:
            text (str): Relaxed JSON string

        Returns:
            dict: Parsed data with optional _tags/_directives
        """
        result = {}
        tags = []
        directives = []
        multiline_key = None
        multiline_val = []

        for line in text.strip().splitlines():
            stripped = line.strip()

            if not stripped or stripped.startswith('#'):
                continue

            try:
                # Handle tags/directives
                if re.match(r'^<.*?/? *?>$', stripped):
                    if '=' in stripped:
                        directives.append(stripped)
                    else:
                        tags.append(stripped)
                    continue

                if ':' in stripped:
                    if multiline_key:
                        result[multiline_key] = self._finalize_value(' '.join(multiline_val))
                        multiline_key = None
                        multiline_val = []

                    key, value = stripped.split(':', 1)
                    key = self._clean_key(key)
                    value = value.strip()

                    if self._is_unbalanced_string(value):
                        multiline_key = key
                        multiline_val = [value]
                    else:
                        result[key] = self._finalize_value(value)

                elif multiline_key:
                    multiline_val.append(stripped)

            except Exception as e:
                print(f"Error: {e}")
                raise ValueError(f"[RelaxedJSON] Failed to parse line: `{line}`\n{e}")

        if multiline_key:
            result[multiline_key] = self._finalize_value(' '.join(multiline_val))

        if self.merge_tags:
            result["tagsDirectives"] = {"tags": tags, "directives": directives}
        else:
            result[self.tag_key] = tags
            result[self.directive_key] = directives

        return result

    def _clean_key(self, key: str) -> str:
        """Remove surrounding quotes from key"""
        return key.strip(' "\'')

    def _is_unbalanced_string(self, value: str) -> bool:
        """Check if a string has unbalanced quotes"""
        return (value.count('"') % 2 == 1) or (value.count("'") % 2 == 1)

    def _finalize_value(self, value: str) -> Any:
        """Convert string into its actual type (reserved, number, string)"""
        val = value.strip().strip(',')

        if val in self.reserved:
            return self.reserved[val]

        try:
            if re.match(r'^-?\\d+\\.\\d*e[+-]?\\d+$', val, re.IGNORECASE):
                return float(val)
            elif '.' in val and re.match(r'^-?\\d+\\.\\d+$', val):
                return float(val)
            elif val.isdigit():
                return int(val)
        except Exception:
            pass
            pass

        if re.match(r'^\\d+/\\d+$', val) or '%' in val or '\\\\' in val:
            return val

        return val.strip('"\'')
