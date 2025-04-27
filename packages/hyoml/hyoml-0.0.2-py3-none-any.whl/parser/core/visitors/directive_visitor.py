class DirectiveVisitor:
    """
    Processes special directives embedded in Hyoml text.
    Directives like <strict=true> or <parse mode="json"> can alter or annotate output.
    """

    @staticmethod
    def visit(data):
        if not isinstance(data, dict):
            return data

        directives = data.get("_directives") or data.get("tagsDirectives", {}).get("directives", [])

        for directive in directives:
            if "=" in directive:
                try:
                    key, value = directive.strip("<>/ ").split("=", 1)
                    key = key.strip().lower()
                    value = value.strip().strip('"\'')
                    data[f"@{key}"] = value
                except Exception:
                    continue
                    continue
            elif directive.startswith("<parse") and "mode=" in directive:
                try:
                    match = directive.strip("<>").split("mode=")[1]
                    data["@parse_mode"] = match.strip('"\' ')
                except Exception:
                    pass
                    pass

        return data
