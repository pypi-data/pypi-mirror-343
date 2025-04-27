"""
DirectiveVisitor: Extracts or applies directives from parsed Hyoml structures.
"""

class DirectiveVisitor:
    def __init__(self, config=None):
        self.config = config or {}

    def visit(self, node):
        if isinstance(node, dict):
            directives = {}
            for k, v in list(node.items()):
                if isinstance(k, str) and k.startswith('%'):
                    directives[k[1:]] = v
                    del node[k]
                elif isinstance(v, (dict, list)):
                    node[k] = self.visit(v)
            if directives:
                node['_directives'] = directives
        elif isinstance(node, list):
            for i, item in enumerate(node):
                node[i] = self.visit(item)
        return node
