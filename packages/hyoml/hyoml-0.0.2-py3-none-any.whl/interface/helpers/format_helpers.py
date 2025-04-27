"""
FormatHelpers - provides asX formatting helpers for Hyoml.
"""

class FormatHelper:
    def __init__(self, hyoml_instance):
        self.hyoml = hyoml_instance

    def asJSON(self, data, path=None, **opts):
        return self.hyoml.format(data, "json", path=path, **opts)

    def asYAML(self, data, path=None, **opts):
        return self.hyoml.format(data, "yaml", path=path, **opts)

    def asTOML(self, data, path=None, **opts):
        return self.hyoml.format(data, "toml", path=path, **opts)

    def asINI(self, data, path=None, **opts):
        return self.hyoml.format(data, "ini", path=path, **opts)

    def asENV(self, data, path=None, **opts):
        return self.hyoml.format(data, "env", path=path, **opts)

    def asCSV(self, data, path=None, **opts):
        return self.hyoml.format(data, "csv", path=path, **opts)

    def asXML(self, data, path=None, **opts):
        return self.hyoml.format(data, "xml", path=path, **opts)

    def asMarkdown(self, data, path=None, **opts):
        return self.hyoml.format(data, "markdown", path=path, **opts)

    def asHTML(self, data, path=None, **opts):
        return self.hyoml.format(data, "html", path=path, **opts)

    def asStrictYML(self, data, path=None, **opts):
        return self.hyoml.format(data, "strictyml", path=path, **opts)

    def toTXT(self, data, path=None, **opts):
        return self.hyoml.format(data, "txt", path=path, **opts)

    def asJavaProperties(self, data, path=None, **opts):
        return self.hyoml.format(data, "java_properties", path=path, **opts)

    def asSQL(self, data, path=None, **opts):
        return self.hyoml.format(data, "sql", path=path, **opts)

    def asShellScript(self, data, path=None, **opts):
        return self.hyoml.format(data, "shell_script", path=path, **opts)

    def asRSS(self, data, path=None, **opts):
        return self.hyoml.format(data, "rss", path=path, **opts)

    def asAtom(self, data, path=None, **opts):
        return self.hyoml.format(data, "atom", path=path, **opts)

    def asJSONLD(self, data, path=None, **opts):
        return self.hyoml.format(data, "jsonld", path=path, **opts)

    def asRDF(self, data, path=None, **opts):
        return self.hyoml.format(data, "rdf", path=path, **opts)

    def asMicrodata(self, data, path=None, **opts):
        return self.hyoml.format(data, "microdata", path=path, **opts)

    def asTurtleTTL(self, data, path=None, **opts):
        return self.hyoml.format(data, "turtle_ttl", path=path, **opts)

    def asNTriples(self, data, path=None, **opts):
        return self.hyoml.format(data, "ntriples", path=path, **opts)

    def asNotation3(self, data, path=None, **opts):
        return self.hyoml.format(data, "notation3", path=path, **opts)

    def asOWL(self, data, path=None, **opts):
        return self.hyoml.format(data, "owl", path=path, **opts)

    def asSPARQL(self, data, path=None, **opts):
        return self.hyoml.format(data, "sparql", path=path, **opts)
