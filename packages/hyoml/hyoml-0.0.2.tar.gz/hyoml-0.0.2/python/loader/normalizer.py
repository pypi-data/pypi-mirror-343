"""
ResourceNormalizer - Normalizes mixed resource input formats.
"""

class ResourceNormalizer:
    """
    Normalizes raw resources (string, tuple, dict) into a unified structure.
    """

    def __init__(self, resource_agent=None):
        """
        Initialize normalizer.

        Args:
            resource_agent (dict): Optional cloud clients mapping.
        """
        self.resource_agent = resource_agent or {}

    def normalize(self, raw_resources):
        """
        Normalize mixed raw inputs into a clean list of resource dicts.

        Args:
            raw_resources (list): Raw resource entries.

        Returns:
            list: List of normalized dicts.
        """
        normalized = []

        for entry in raw_resources:
            if isinstance(entry, str):
                normalized.append({"resource": entry, "agent": None, "agent_object": None})

            elif isinstance(entry, (list, tuple)) and len(entry) == 2:
                resource, agent_or_object = entry
                if isinstance(agent_or_object, str):
                    normalized.append({"resource": resource, "agent": agent_or_object, "agent_object": None})
                else:
                    normalized.append({"resource": resource, "agent": None, "agent_object": agent_or_object})

            elif isinstance(entry, dict):
                resource = entry.get("resource") or entry.get("uri_source") or entry.get("source")
                agent = entry.get("agent") or entry.get("agent_name")
                agent_object = entry.get("agent_object")  # Optional explicit
                if resource:
                    normalized.append({"resource": resource, "agent": agent, "agent_object": agent_object})
                else:
                    raise ValueError(f"[ResourceNormalizer] Invalid dict resource entry: {entry}")

            else:
                raise ValueError(f"[ResourceNormalizer] Unsupported resource entry type: {type(entry)}")

        return normalized
