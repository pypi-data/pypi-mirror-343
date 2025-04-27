import re
from typing import Any, Dict


class RelaxedYML:
    """
    Relaxed YML parser with support for:
    - Nested indentation
    - Unquoted keys
    - Reserved keywords
    - Smart type casting
    - Lists with "- "
    - Inline key-value fallback
    - <tag>, <directive=>, </tag> recognition
    """

    def __init__(self, tag_key="_tags", directive_key="_directives", merge_tags=False):
        """
        Args:
            tag_key (str): Where to store parsed tags.
            directive_key (str): Where to store parsed directives.
            merge_tags (bool): If True, store both under 'tagsDirectives'.
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
        Parses relaxed YML into a dictionary structure.

        Args:
            text (str): Relaxed YML input

        Returns:
            dict: Parsed output with optional tags/directives
        """
        lines = text.replace('\t', '  ').split('\n')
        result = {}
        stack = [(0, result)]
        tags = []
        directives = []

        for line in lines:
            raw = line.strip()
            if not raw or raw.startswith('#'):
                continue

            try:
                if re.match(r'^<.*?/? *?>$', raw):
                    if '=' in raw:
                        directives.append(raw)
                    else:
                        tags.append(raw)
                    continue

                indent = len(line) - len(raw)
                while indent < stack[-1][0]:
                    stack.pop()

                parent = stack[-1][1]

                if ':' in raw:
                    key, value = raw.split(':', 1)
                    key = self._clean_key(key.strip())
                    value = value.strip()

                    if not value:
                        new_dict = {}
                        parent[key] = new_dict
                        stack.append((indent + 2, new_dict))
                    else:
                        parent[key] = self._finalize_value(value)

                elif raw.startswith('- '):
                    item = raw[2:].strip()
                    if not isinstance(parent, list):
                        last_key = list(parent.keys())[-1]
                        parent[last_key] = []
                        parent = parent[last_key]
                    parent.append(self._finalize_value(item))

                else:
                    parts = raw.split()
                    if len(parts) == 2:
                        parent[self._clean_key(parts[0])] = self._finalize_value(parts[1])
                    else:
                        parent[raw] = True

            except Exception as e:
                print(f"Error: {e}")
                raise ValueError(f"[RelaxedYML] Failed parsing line: `{line}`\n{e}")

        if self.merge_tags:
            result["tagsDirectives"] = {"tags": tags, "directives": directives}
        else:
            result[self.tag_key] = tags
            result[self.directive_key] = directives

        return result

    def _clean_key(self, key: str) -> str:
        return key.strip('"\' ')

    def _finalize_value(self, value: str) -> Any:
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
