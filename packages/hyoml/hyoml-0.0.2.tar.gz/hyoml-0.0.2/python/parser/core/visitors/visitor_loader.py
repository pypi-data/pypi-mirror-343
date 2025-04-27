import importlib

class VisitorPipeline:
    """
    Dynamically loads and applies a pipeline of visitors to parsed data.
    """

    @staticmethod
    def apply(data, visitor_paths=None):
        """
        Apply a list of visitors in order to the parsed data.

        Args:
            data (dict): Parsed data to transform.
            visitor_paths (list): List of full import paths (e.g., core.visitors.date_visitor.DateVisitor)

        Returns:
            dict: Transformed data after visitor pipeline
        """
        if not visitor_paths:
            return data

        for path in visitor_paths:
            try:
                module_path, class_name = path.rsplit(".", 1)
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name)
                data = cls.visit(data)
            except Exception as e:
                print(f"Error: {e}")
                print(f"[warn] Failed to apply visitor {path}: {e}")

        return data
