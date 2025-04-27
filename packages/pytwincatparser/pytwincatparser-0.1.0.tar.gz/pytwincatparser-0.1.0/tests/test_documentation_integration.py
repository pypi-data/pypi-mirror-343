import unittest
import os
import tempfile
from pathlib import Path
from pytwincatparser_xsdata import TwinCatLoader, TcPou, TcDut, TcMethod, TcDocumentation

class TestDocumentationIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up temporary files for testing."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_files_dir = Path(self.temp_dir.name)
        
        # Create a test POU file
        self.pou_file_path = self.test_files_dir / "FB_Test.TcPOU"
        with open(self.pou_file_path, 'w') as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.12">
  <POU Name="FB_Test" Id="{12345678-1234-1234-1234-123456789012}" SpecialFunc="None">
    <Declaration><![CDATA[FUNCTION_BLOCK FB_Test
(*
 @details
 This is a test function block.
 @usage
 Use this function block for testing.
*)
VAR
    _test : BOOL;
END_VAR
]]></Declaration>
    <Implementation>
      <ST><![CDATA[]]></ST>
    </Implementation>
    <Method Name="TestMethod" Id="{12345678-1234-1234-1234-123456789013}">
      <Declaration><![CDATA[METHOD TestMethod : BOOL
(***********************************************************************************
* @brief Description : This is a test method.
* @return Returns TRUE if successful.
************************************************************************************)
VAR_INPUT
    input : BOOL;
END_VAR
]]></Declaration>
      <Implementation>
        <ST><![CDATA[]]></ST>
      </Implementation>
    </Method>
  </POU>
</TcPlcObject>''')
        
        # Create a test DUT file
        self.dut_file_path = self.test_files_dir / "ST_Test.TcDUT"
        with open(self.dut_file_path, 'w') as f:
            f.write('''<?xml version="1.0" encoding="utf-8"?>
<TcPlcObject Version="1.1.0.1" ProductVersion="3.1.4024.9">
  <DUT Name="ST_Test" Id="{12345678-1234-1234-1234-123456789014}">
    <Declaration><![CDATA[TYPE ST_Test :

//@details
//This is a test structure.
//@usage
//Use this structure for testing.

STRUCT
    field1 : BOOL;
    field2 : INT;
    field3 : STRING;
END_STRUCT
END_TYPE
]]></Declaration>
  </DUT>
</TcPlcObject>''')
    
    def tearDown(self):
        """Clean up temporary files."""
        self.temp_dir.cleanup()
    
    def test_pou_documentation(self):
        """Test that documentation is correctly parsed and attached to POUs."""
        # Create loader and load files
        tc_objects = []
        loader = TwinCatLoader(
            search_path=self.test_files_dir,
            tcObjects=tc_objects
        )
        loader.load()
        
        # Get the test POU
        fb_test = loader.getItemByName("FB_Test.TcPOU")
        
        # Check that the POU has documentation
        self.assertIsNotNone(fb_test)
        self.assertIsNotNone(fb_test.documentation)
        self.assertEqual(fb_test.documentation.details, "This is a test function block.")
        self.assertEqual(fb_test.documentation.usage, "Use this function block for testing.")
        self.assertIsNone(fb_test.documentation.brief)
        self.assertIsNone(fb_test.documentation.returns)
        self.assertEqual(fb_test.documentation.custom_tags, {})
    
    def test_method_documentation(self):
        """Test that documentation is correctly parsed and attached to methods."""
        # Create loader and load files
        tc_objects = []
        loader = TwinCatLoader(
            search_path=self.test_files_dir,
            tcObjects=tc_objects
        )
        loader.load()
        
        # Get the test POU
        fb_test = loader.getItemByName("FB_Test.TcPOU")
        
        # Check that the method has documentation
        self.assertIsNotNone(fb_test)
        self.assertIsNotNone(fb_test.methods)
        self.assertEqual(len(fb_test.methods), 1)
        
        test_method = fb_test.methods[0]
        self.assertEqual(test_method.name, "TestMethod")
        self.assertIsNotNone(test_method.documentation)
        self.assertIsNone(test_method.documentation.details)
        self.assertIsNone(test_method.documentation.usage)
        self.assertEqual(test_method.documentation.brief, "Description : This is a test method.")
        self.assertEqual(test_method.documentation.returns, "Returns TRUE if successful.")
        self.assertEqual(test_method.documentation.custom_tags, {})
    
    def test_dut_documentation(self):
        """Test that documentation is correctly parsed and attached to DUTs."""
        # Create loader and load files
        tc_objects = []
        loader = TwinCatLoader(
            search_path=self.test_files_dir,
            tcObjects=tc_objects
        )
        loader.load()
        
        # Get the test DUT
        st_test = loader.getItemByName("ST_Test.TcDUT")
        
        # Check that the DUT has documentation
        self.assertIsNotNone(st_test)
        self.assertIsNotNone(st_test.documentation)
        self.assertEqual(st_test.documentation.details, "This is a test structure.")
        self.assertEqual(st_test.documentation.usage, "Use this structure for testing.")
        self.assertIsNone(st_test.documentation.brief)
        self.assertIsNone(st_test.documentation.returns)
        self.assertEqual(st_test.documentation.custom_tags, {})

if __name__ == '__main__':
    unittest.main()
