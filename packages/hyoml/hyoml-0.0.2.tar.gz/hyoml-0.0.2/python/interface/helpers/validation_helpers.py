"""
ValidationHelpers - provides isValidX validators for Hyoml.
"""

from utils.validator import Validator

class ValidationHelper:
    def __init__(self, hyoml_instance):
        self.hyoml = hyoml_instance

    def isValidJSON(self, data): return Validator.isValidJSON(data)
    def isValidYAML(self, data): return Validator.isValidYAML(data)
    def isValidENV(self, data): return Validator.isValidENV(data)
    def isValidINI(self, data): return Validator.isValidINI(data)
    def isValidTOML(self, data): return Validator.isValidTOML(data)
    def isValidCSV(self, data): return Validator.isValidCSV(data)
    def isValidXML(self, data): return Validator.isValidXML(data)
    def isValidMarkdown(self, data): return Validator.isValidMarkdown(data)
    def isValidHTML(self, data): return Validator.isValidHTML(data)
    def isValidStrictYML(self, data): return Validator.isValidStrictYML(data)
    def isValidJavaProperties(self, data): return Validator.isValidJavaProperties(data)
    def isValidSQL(self, data): return Validator.isValidSQL(data)
    def isValidShellScript(self, data): return Validator.isValidShellScript(data)
    def isValidRSS(self, data): return Validator.isValidRSS(data)
    def isValidAtom(self, data): return Validator.isValidAtom(data)
    def isValidJSONLD(self, data): return Validator.isValidJSONLD(data)
    def isValidRDF(self, data): return Validator.isValidRDF(data)
    def isValidMicrodata(self, data): return Validator.isValidMicrodata(data)
    def isValidTurtleTTL(self, data): return Validator.isValidTurtleTTL(data)
    def isValidNTriples(self, data): return Validator.isValidNTriples(data)
    def isValidNotation3(self, data): return Validator.isValidNotation3(data)
    def isValidOWL(self, data): return Validator.isValidOWL(data)
    def isValidSPARQL(self, data): return Validator.isValidSPARQL(data)
