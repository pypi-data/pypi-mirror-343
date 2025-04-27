import unittest
from middleware.tag_visitor import TagVisitor
from middleware.directive_visitor import DirectiveVisitor

class TestVisitors(unittest.TestCase):
    """
    Tests for middleware visitors that process tags and directives.
    """

    def test_tag_visitor_extracts_tags(self):
        data = {
            "@author": "Ahmed",
            "title": "Hyoml",
            "meta": {
                "@version": "1.0"
            }
        }
        result = TagVisitor().visit(data)
        self.assertIn("_tags", result)
        self.assertIn("author", result["_tags"])
        self.assertEqual(result["_tags"]["author"], "Ahmed")
        self.assertIn("version", result["meta"].get("_tags", {}))

    def test_directive_visitor_extracts_directives(self):
        data = {
            "%strict": True,
            "content": "data",
            "nested": {
                "%type": "json"
            }
        }
        result = DirectiveVisitor().visit(data)
        self.assertIn("_directives", result)
        self.assertTrue(result["_directives"]["strict"])
        self.assertEqual(result["nested"].get("_directives", {}).get("type"), "json")

if __name__ == "__main__":
    unittest.main()
