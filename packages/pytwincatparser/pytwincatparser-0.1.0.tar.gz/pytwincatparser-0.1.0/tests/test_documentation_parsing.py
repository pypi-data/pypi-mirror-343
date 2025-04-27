import unittest
from pytwincatparser_xsdata.TwincatParser import parse_documentation, TcDocumentation

class TestDocumentationParsing(unittest.TestCase):
    
    def test_parse_multiline_comment(self):
        """Test parsing documentation from multi-line comments."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        (*
         @details
         This is a test function block.
         @usage
         Use this function block for testing.
        *)
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc.details, "This is a test function block.")
        self.assertEqual(doc.usage, "Use this function block for testing.")
        self.assertIsNone(doc.brief)
        self.assertIsNone(doc.returns)
        self.assertEqual(doc.custom_tags, {})
    
    def test_parse_singleline_comment(self):
        """Test parsing documentation from single-line comments."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        //@details
        //This is a test function block.
        //@usage
        //Use this function block for testing.
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc.details, "This is a test function block.")
        self.assertEqual(doc.usage, "Use this function block for testing.")
        self.assertIsNone(doc.brief)
        self.assertIsNone(doc.returns)
        self.assertEqual(doc.custom_tags, {})
    
    def test_parse_starred_comment(self):
        """Test parsing documentation from starred comments."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        (***********************************************************************************
        * @brief Description : This is a test function block.
        * @return None
        ************************************************************************************)
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNotNone(doc)
        self.assertIsNone(doc.details)
        self.assertIsNone(doc.usage)
        self.assertEqual(doc.brief, "Description : This is a test function block.")
        self.assertEqual(doc.returns, "None")
        self.assertEqual(doc.custom_tags, {})
    
    def test_parse_custom_tags(self):
        """Test parsing custom documentation tags."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        (*
         @details
         This is a test function block.
         @author John Doe
         @version 1.0.0
         @date 2025-04-26
        *)
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc.details, "This is a test function block.")
        self.assertIsNone(doc.usage)
        self.assertIsNone(doc.brief)
        self.assertIsNone(doc.returns)
        self.assertEqual(doc.custom_tags, {
            "author": "John Doe",
            "version": "1.0.0",
            "date": "2025-04-26"
        })
    
    def test_parse_mixed_comments(self):
        """Test parsing documentation from mixed comment styles."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        (*
         @details
         This is a test function block.
        *)
        // @usage
        // Use this function block for testing.
        (***********************************************************************************
        * @brief Description : This is a test function block.
        * @return None
        ************************************************************************************)
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNotNone(doc)
        self.assertEqual(doc.details, "This is a test function block.")
        self.assertEqual(doc.usage, "Use this function block for testing.")
        self.assertEqual(doc.brief, "Description : This is a test function block.")
        self.assertEqual(doc.returns, "None")
        self.assertEqual(doc.custom_tags, {})
    
    def test_no_documentation(self):
        """Test parsing when no documentation is present."""
        declaration = """
        FUNCTION_BLOCK FB_Test
        VAR
            _test : BOOL;
        END_VAR
        """
        
        doc = parse_documentation(declaration)
        
        self.assertIsNone(doc)
    
    def test_empty_declaration(self):
        """Test parsing when declaration is empty."""
        declaration = ""
        
        doc = parse_documentation(declaration)
        
        self.assertIsNone(doc)
    
    def test_none_declaration(self):
        """Test parsing when declaration is None."""
        declaration = None
        
        doc = parse_documentation(declaration)
        
        self.assertIsNone(doc)

if __name__ == '__main__':
    unittest.main()
