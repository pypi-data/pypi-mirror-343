"""
TagVisitor: Extracts and processes tags in Hyoml-parsed data.
"""

class TagVisitor:
    def __init__(self, config=None):
        self.config = config or {}

    def visit(self, node):
        if isinstance(node, dict):
            tags = {}
            for k, v in list(node.items()):
                if isinstance(k, str) and k.startswith('@'):
                    tags[k[1:]] = v
                    del node[k]
                elif isinstance(v, (dict, list)):
                    node[k] = self.visit(v)
            if tags:
                node['_tags'] = tags
        elif isinstance(node, list):
            for i, item in enumerate(node):
                node[i] = self.visit(item)
        return node
