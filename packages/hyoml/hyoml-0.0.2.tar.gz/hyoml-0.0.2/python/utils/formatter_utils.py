def clean_output(data, omit_keys=None):
    """
    Removes metadata keys like _tags, _directives, or any user-defined keys from a dictionary.

    Args:
        data (dict): Input parsed object
        omit_keys (list): List of keys to remove (default: [_tags, _directives, tagsDirectives, @tags, @directives])

    Returns:
        dict: Cleaned output
    """
    if not isinstance(data, dict):
        return data

    omit_keys = omit_keys or ["_tags", "_directives", "tagsDirectives", "@tags", "@directives"]
    return {k: v for k, v in data.items() if k not in omit_keys}
