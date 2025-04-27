import re

class AutoFixer:
    """
    A smart, modular autofixer for RelaxedJSON/YML/Hyoml input.
    Cleans, normalizes, and corrects common syntax issues and structural irregularities.
    """

    @staticmethod
    def apply(text, level="smart", log_fixes=False):
        """
        Apply all autofix steps to the given text.

        Args:
            text (str): Original raw input string
            level (str): Fixing level (reserved for future use)
            log_fixes (bool): If True, will print diff of changes

        Returns:
            str: Cleaned and fixed string
        """
        try:
            original = text
            text = AutoFixer.fix_mixed_indents(text)
            text = AutoFixer.fix_mismatched_quotes(text)
            text = AutoFixer.fix_missing_commas(text)
            text = AutoFixer.fix_colons(text)
            text = AutoFixer.fix_backslashes(text)
            text = AutoFixer.fix_hyoml_keywords(text)
            text = AutoFixer.fix_floating_numbers(text)
            text = AutoFixer.fix_trailing_commas(text)
            text = AutoFixer.fix_brackets(text)

            if log_fixes:
                print("💡 AutoFix applied changes:")
                for line in AutoFixer.diff(original, text):
                    print(line)

            return text
        except Exception as e:
            print(f"Error: {e}")
            raise RuntimeError(f"[AutoFixer] Failed to apply autofix: {e}")

    @staticmethod
    def fix_mixed_indents(text):
        """Replace all tabs with 2 spaces."""
        return text.replace('\t', '  ')

    @staticmethod
    def fix_mismatched_quotes(text):
        """Replace incorrect inline single quotes with double quotes."""
        return re.sub(r"(['\"])(.*?)\1(?=\S)", r'"\2"', text)

    @staticmethod
    def fix_missing_commas(text):
        """Add missing commas between key-value lines."""
        try:
            lines = text.splitlines()
            for i in range(1, len(lines)):
                prev = lines[i - 1].strip()
                if ':' in prev and ':' in lines[i] and not prev.endswith((',', '{', '[')):
                    lines[i - 1] += ','
            return '\n'.join(lines)
        except Exception as e:
            print(f"Error: {e}")
            raise RuntimeError(f"[AutoFixer.fix_missing_commas] Failed: {e}")

    @staticmethod
    def fix_colons(text):
        """Add missing colons between key-value lines (key value → key: value)."""
        return re.sub(r'^(\s*[^:#\-]+)\s+([^\s#]+)', r'\1: \2', text, flags=re.MULTILINE)

    @staticmethod
    def fix_backslashes(text):
        """Fix over-escaped Windows-style backslashes."""
        return text.replace('\\\\', '/')

    @staticmethod
    def fix_trailing_commas(text):
        """Remove trailing commas before } or ]."""
        return re.sub(r',\s*([}\]])', r'\1', text)

    @staticmethod
    def fix_floating_numbers(text):
        """Fix invalid numbers like 12..3 or 0.4.5 → best guess."""
        return re.sub(r'(\d+)\.([\d\.]+)', lambda m: m.group(0) if re.fullmatch(r'\d+\.\d+', m.group(0)) else m.group(1) + '.' + m.group(2).split('.')[0], text)

    @staticmethod
    def fix_brackets(text):
        """Balance curly braces if open count exceeds close count."""
        if text.count('{') > text.count('}'):
            text += '}' * (text.count('{') - text.count('}'))
        return text

    @staticmethod
    def fix_hyoml_keywords(text):
        """Correct common typos in embedded hyoml language keywords."""
        patterns = {
            'hyoml_jasn': 'hyoml_json',
            'json-hyoml': 'hyoml_json',
            'jsn_hyoml': 'hyoml_json',
            'homl': 'hyoml',
            'hoyml': 'hyoml',
            'hyml': 'hyoml',
        }
        for wrong, right in patterns.items():
            text = re.sub(rf"<{wrong}>", f"<{right}>", text, flags=re.IGNORECASE)
        return text

    @staticmethod
    def diff(before, after):
        """
        Generate simple line-by-line diff.

        Returns:
            list[str]: Formatted diff lines
        """
        b_lines = before.splitlines()
        a_lines = after.splitlines()
        return [f"- {b}" if b != a else f"  {a}" for b, a in zip(b_lines, a_lines)] + [
            f"+ {a}" for a in a_lines[len(b_lines):]
        ]
