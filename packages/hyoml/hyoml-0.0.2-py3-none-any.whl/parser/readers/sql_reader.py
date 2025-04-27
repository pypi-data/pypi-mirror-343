"""
SqlReader - Parses basic SQL DDL and INSERT statements into structured data.
"""

from python.parser.readers.base_reader import BaseReader

class SqlReader(BaseReader):
    """
    Reader for simple SQL blocks.
    Supports strict parsing and relaxed tolerant parsing.
    """

    def can_parse(self, input_text: str) -> bool:
        """
        Detect if the input looks like SQL.

        Args:
            input_text (str): Text to inspect.

        Returns:
            bool: True if it looks like SQL.
        """
        stripped = input_text.strip().lower()
        return stripped.startswith("create table") or stripped.startswith("insert into")

    def parse(self, input_text: str):
        """
        Parse the input SQL text.

        Args:
            input_text (str): SQL text.

        Returns:
            dict: Parsed SQL structure.
        """
        try:
            return self._parse_sql(input_text)
        except Exception as e:
            print(f"Error: {e}")
            if self.strict_mode:
                raise ValueError(f"[SqlReader] Strict SQL parsing failed: {e}")
            else:
                relaxed_text = self._relax_sql(input_text)
                try:
                    return self._parse_sql(relaxed_text)
                except Exception as e2:
                    raise ValueError(f"[SqlReader] Relaxed SQL parsing failed after attempting fixes: {e2}")

    def _parse_sql(self, text):
        """
        Very simple internal SQL parser for basic CREATE TABLE and INSERT.
        """
        lines = text.strip().splitlines()
        result = {}

        if lines[0].strip().lower().startswith("create table"):
            result["operation"] = "create_table"
            table_name = lines[0].strip().split()[2]
            result["table"] = table_name
            columns = []
            for line in lines[1:]:
                line = line.strip().strip(",").strip()
                if line.endswith(")"):
                    line = line[:-1].strip()
                if line and " " in line:
                    colname, coltype = line.split(None, 1)
                    columns.append({"name": colname, "type": coltype})
            result["columns"] = columns

        elif lines[0].strip().lower().startswith("insert into"):
            result["operation"] = "insert"
            parts = lines[0].strip().split()
            table_name = parts[2]
            result["table"] = table_name
            values = []
            for line in lines:
                if "values" in line.lower():
                    values_text = line.split("values", 1)[1]
                    values_text = values_text.strip(" ();")
                    entries = [v.strip().strip("'\"") for v in values_text.split(",")]
                    values.append(entries)
            result["values"] = values

        else:
            raise ValueError("Unsupported SQL format.")

        return result

    def _relax_sql(self, text):
        """
        Try to auto-fix simple relaxed SQL issues.

        Args:
            text (str): Raw SQL text.

        Returns:
            str: Modified text.
        """
        relaxed = text

        # Example: Normalize spaces, remove extra line breaks (future enhancements)

        return relaxed
