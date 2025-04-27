from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig
from xsdata.exceptions import ParserError

from .TwincatObjects import TcPlcObject
from .TwincatObjects.tc_plc_object import Pou, Dut, Itf, Get, Set, Method, Property

from typing import Optional, List, Dict
from pathlib import Path
from dataclasses import dataclass
import re
import logging





logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@dataclass
class TcDocumentation:
    details: Optional[str] = None
    usage: Optional[str] = None
    brief: Optional[str] = None
    returns: Optional[str] = None
    custom_tags: Optional[Dict[str, str]] = None
    
    def __post_init__(self):
        if self.custom_tags is None:
            self.custom_tags = {}

@dataclass
class TcVariable:
    name: str = ''
    type: str = ''
    initial_value: Optional[str] = None
    comment: Optional[str] = None
    attributes: Optional[Dict[str, str]] = None

@dataclass
class TcVariableSection:
    section_type: str = ''  # VAR, VAR_INPUT, VAR_OUTPUT, VAR_IN_OUT, VAR_STAT, VAR CONSTANT
    variables: List[TcVariable] = None
    
    def __post_init__(self):
        if self.variables is None:
            self.variables = []

def parse_documentation(declaration: str) -> Optional[TcDocumentation]:
    """
    Parse documentation comments from a declaration string.
    
    Args:
        declaration: The declaration string containing documentation comments.
        
    Returns:
        A TcDocumentation object or None if no documentation is found.
    """
    if not declaration:
        return None
    
    # Extract only the part before the first variable block
    var_pattern = re.compile(r'VAR(?:_INPUT|_OUTPUT|_IN_OUT|_INST|_STAT|[ ]CONSTANT)?', re.DOTALL)
    struct_pattern = re.compile(r'STRUCT', re.DOTALL)
    
    # Find the position of the first variable block
    var_match = var_pattern.search(declaration)
    struct_match = struct_pattern.search(declaration)
    
    # Determine the end position of the documentation block
    end_pos = len(declaration)
    if var_match:
        end_pos = min(end_pos, var_match.start())
    if struct_match:
        end_pos = min(end_pos, struct_match.start())
    
    # Extract only the part before the first variable block
    doc_part = declaration[:end_pos]
    
    # Define regex patterns for different comment styles
    # 1. Multi-line comment: (* ... *)
    # 2. Single-line comment: // ...
    # 3. Multi-line comment with stars: (*** ... ***)
    multiline_comment_pattern = re.compile(r'\(\*\s*(.*?)\s*\*\)', re.DOTALL)
    singleline_comment_pattern = re.compile(r'//\s*(.*?)$', re.MULTILINE)
    
    # Extract all comments
    comments = []
    
    # Check for multi-line comments
    for match in multiline_comment_pattern.finditer(doc_part):
        comments.append(match.group(1).strip())
    
    # Check for single-line comments
    single_line_comments = []
    for match in singleline_comment_pattern.finditer(doc_part):
        single_line_comments.append(match.group(1).strip())
    
    if single_line_comments:
        comments.append('\n'.join(single_line_comments))
    
    if not comments:
        return None
    
    # Join all comments
    comment_text = '\n'.join(comments)
    
    # Parse documentation tags
    doc = TcDocumentation()
    
    # Define regex patterns for documentation tags
    details_pattern = re.compile(r'@details\s*(.*?)(?=@\w+|\Z)', re.DOTALL)
    usage_pattern = re.compile(r'@usage\s*(.*?)(?=@\w+|\Z)', re.DOTALL)
    brief_pattern = re.compile(r'@brief\s*(.*?)(?=@\w+|\Z)', re.DOTALL)
    returns_pattern = re.compile(r'@return\s*(.*?)(?=@\w+|\Z)', re.DOTALL)
    custom_tag_pattern = re.compile(r'@(\w+)\s*(.*?)(?=@\w+|\Z)', re.DOTALL)
    
    # Helper function to clean up tag content
    def clean_tag_content(content):
        if content:
            # Remove lines that are just asterisks
            content = re.sub(r'^\s*\*+\s*$', '', content, flags=re.MULTILINE)
            # Remove trailing asterisks and whitespace
            content = re.sub(r'\s*\*+\s*$', '', content)
            # Remove leading asterisks and whitespace from each line
            content = re.sub(r'^\s*\*+\s*', '', content, flags=re.MULTILINE)
            # Remove leading and trailing whitespace
            content = content.strip()
            # Replace multiple whitespace with a single space
            content = re.sub(r'\s+', ' ', content)
        return content
    
    # Extract details
    details_match = details_pattern.search(comment_text)
    if details_match:
        doc.details = clean_tag_content(details_match.group(1))
    
    # Extract usage
    usage_match = usage_pattern.search(comment_text)
    if usage_match:
        doc.usage = clean_tag_content(usage_match.group(1))
    
    # Extract brief
    brief_match = brief_pattern.search(comment_text)
    if brief_match:
        doc.brief = clean_tag_content(brief_match.group(1))
    
    # Extract returns
    returns_match = returns_pattern.search(comment_text)
    if returns_match:
        doc.returns = clean_tag_content(returns_match.group(1))
    
    # Extract custom tags
    for match in custom_tag_pattern.finditer(comment_text):
        tag_name = match.group(1)
        tag_value = clean_tag_content(match.group(2))
        if tag_name not in ['details', 'usage', 'brief', 'return']:
            doc.custom_tags[tag_name] = tag_value
    
    return doc

def parse_variable_sections(declaration: str) -> List[TcVariableSection]:
    """
    Parse variable sections from a declaration string.
    
    Args:
        declaration: The declaration string containing variable sections.
        
    Returns:
        A list of TcVariableSection objects.
    """
    if not declaration:
        return []
    
    # Define regex patterns
    section_pattern = re.compile(r'(VAR(?:_INPUT|_OUTPUT|_IN_OUT|_INST|_STAT|[ ]CONSTANT)?)\s*(.*?)END_VAR', re.DOTALL)
    struct_pattern = re.compile(r'STRUCT\s*(.*?)END_STRUCT', re.DOTALL)
    attribute_pattern = re.compile(r'\{attribute\s+\'([^\']+)\'\s*(?:\:=\s*\'([^\']*)\')?\}')
    comment_pattern = re.compile(r'(?://(.*)$)|(?:\(\*\s*(.*?)\s*\*\))|(?:\(\*\*\*(.*?)\*\*\*\))', re.MULTILINE | re.DOTALL)
    
    # Find all variable sections
    sections = []
    
    # Process VAR sections
    for section_match in section_pattern.finditer(declaration):
        section_type = section_match.group(1).strip()
        section_content = section_match.group(2).strip()
        
        # Create a new section
        section = TcVariableSection(section_type=section_type)
        
        # Split the section content into lines
        lines = section_content.split('\n')
        
        # Process each line
        current_var = None
        current_attributes = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for attribute
            attr_match = attribute_pattern.search(line)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2) if attr_match.group(2) else ""
                current_attributes[attr_name] = attr_value
                continue
            
            # Check for variable declaration
            if ':' in line:
                # If we have a previous variable, add it to the section
                if current_var:
                    section.variables.append(current_var)
                
                # Parse the new variable
                var_parts = line.split(':', 1)
                var_name = var_parts[0].strip()
                
                # Extract comment if present
                var_comment = None
                comment_match = comment_pattern.search(line)
                if comment_match:
                    # Get the first non-None group
                    for group in comment_match.groups():
                        if group:
                            var_comment = group.strip()
                            break
                
                # Remove comment from line for further processing
                if comment_match:
                    line = line[:comment_match.start()].strip()
                
                # Parse type and initial value
                type_value_parts = var_parts[1].strip()
                if ';' in type_value_parts:
                    type_value_parts = type_value_parts.rstrip(';')
                
                var_type = type_value_parts
                var_initial_value = None
                
                # Check for initial value
                if ':=' in type_value_parts:
                    type_init_parts = type_value_parts.split(':=', 1)
                    var_type = type_init_parts[0].strip()
                    var_initial_value = type_init_parts[1].strip()
                
                # Create the variable
                current_var = TcVariable(
                    name=var_name,
                    type=var_type,
                    initial_value=var_initial_value,
                    comment=var_comment,
                    attributes=current_attributes if current_attributes else None
                )
                
                # Reset attributes for the next variable
                current_attributes = {}
            
        # Add the last variable if there is one
        if current_var:
            section.variables.append(current_var)
        
        # Add the section to the list
        sections.append(section)
    
    # Process STRUCT sections for DUTs
    for struct_match in struct_pattern.finditer(declaration):
        struct_content = struct_match.group(1).strip()
        
        # Create a new section for the struct
        section = TcVariableSection(section_type="STRUCT")
        
        # Split the struct content into lines
        lines = struct_content.split('\n')
        
        # Process each line
        current_var = None
        current_attributes = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Check for attribute
            attr_match = attribute_pattern.search(line)
            if attr_match:
                attr_name = attr_match.group(1)
                attr_value = attr_match.group(2) if attr_match.group(2) else ""
                current_attributes[attr_name] = attr_value
                continue
            
            # Check for variable declaration
            if ':' in line:
                # If we have a previous variable, add it to the section
                if current_var:
                    section.variables.append(current_var)
                
                # Parse the new variable
                var_parts = line.split(':', 1)
                var_name = var_parts[0].strip()
                
                # Extract comment if present
                var_comment = None
                comment_match = comment_pattern.search(line)
                if comment_match:
                    # Get the first non-None group
                    for group in comment_match.groups():
                        if group:
                            var_comment = group.strip()
                            break
                
                # Remove comment from line for further processing
                if comment_match:
                    line = line[:comment_match.start()].strip()
                
                # Parse type and initial value
                type_value_parts = var_parts[1].strip()
                if ';' in type_value_parts:
                    type_value_parts = type_value_parts.rstrip(';')
                
                var_type = type_value_parts
                var_initial_value = None
                
                # Check for initial value
                if ':=' in type_value_parts:
                    type_init_parts = type_value_parts.split(':=', 1)
                    var_type = type_init_parts[0].strip()
                    var_initial_value = type_init_parts[1].strip()
                
                # Create the variable
                current_var = TcVariable(
                    name=var_name,
                    type=var_type,
                    initial_value=var_initial_value,
                    comment=var_comment,
                    attributes=current_attributes if current_attributes else None
                )
                
                # Reset attributes for the next variable
                current_attributes = {}
            
        # Add the last variable if there is one
        if current_var:
            section.variables.append(current_var)
        
        # Add the section to the list if it has variables
        if section.variables:
            sections.append(section)
    
    return sections

@dataclass
class TcGet:
    name : str = ''
    declaration : str = ''
    implementation : str = ''    

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Get):
        if xml_import is None:
            return None
            
        return TcGet(name=xml_import.name, 
                     declaration=xml_import.declaration, 
                     implementation=xml_import.implementation)

@dataclass
class TcSet:
    name : str = ''
    declaration : str = ''
    implementation : str = ''   

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Set):
        if xml_import is None:
            return None
            
        return TcSet(name=xml_import.name, 
                     declaration=xml_import.declaration, 
                     implementation=xml_import.implementation) 

@dataclass
class TcMethod:
    name : str = ''
    accessModifier : Optional[str] = None
    returnType : Optional[str] = None
    declaration : str = ''
    implementation : str = ''
    variable_sections: Optional[List[TcVariableSection]] = None
    documentation: Optional[TcDocumentation] = None
    
    def __post_init__(self):
        if self.variable_sections is None:
            self.variable_sections = []

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Method):
        if xml_import is None:
            return None
            
        # Parse access modifier and return type from declaration
        accessModifier = None
        returnType = None
        variable_sections = []
        documentation = None
        
        if xml_import.declaration:
            declaration_lines = xml_import.declaration.strip().split('\n')
            if declaration_lines:
                first_line = declaration_lines[0].strip()
                # Look for METHOD [MODIFIER] name : return_type;
                if first_line.startswith('METHOD '):
                    # Check for return type after colon
                    if ':' in first_line:
                        # Split by colon and get the part after it
                        return_part = first_line.split(':', 1)[1].strip()
                        # Remove trailing semicolon if present
                        if return_part.endswith(';'):
                            return_part = return_part[:-1].strip()
                        returnType = return_part
                    
                    # Check for access modifier
                    parts = first_line.split(' ')
                    if len(parts) >= 3:
                        # Check if the second part is an access modifier
                        possible_modifier = parts[1].upper()
                        if possible_modifier in ['PROTECTED', 'PRIVATE', 'INTERNAL', 'PUBLIC']:
                            accessModifier = possible_modifier
            
            # Parse variable sections
            variable_sections = parse_variable_sections(xml_import.declaration)
            
            # Parse documentation
            documentation = parse_documentation(xml_import.declaration)

        return TcMethod(name=xml_import.name, 
                        accessModifier=accessModifier,
                        returnType=returnType,
                        declaration=xml_import.declaration, 
                        implementation=xml_import.implementation,
                        variable_sections=variable_sections,
                        documentation=documentation)

@dataclass
class TcProperty:
    name : str = ''
    returnType : Optional[str] = None
    get : Optional[TcGet] = None
    set : Optional[TcSet] = None

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Property):
        if xml_import is None:
            return None
        
        # Parse return type from declaration
        returnType = None
        if xml_import.declaration:
            declaration_lines = xml_import.declaration.strip().split('\n')
            if declaration_lines:
                first_line = declaration_lines[0].strip()
                # Look for PROPERTY name : return_type
                if first_line.startswith('PROPERTY '):
                    # Check for return type after colon
                    if ':' in first_line:
                        # Split by colon and get the part after it
                        return_part = first_line.split(':', 1)[1].strip()
                        returnType = return_part
            
        return TcProperty(name=xml_import.name,
                          returnType=returnType,
                          get=TcGet.from_xml_import(xml_import=xml_import.get),
                          set=TcSet.from_xml_import(xml_import=xml_import.set))

@dataclass
class TcPou:
    name : str = ''
    implements : Optional[list[str]] = None
    extends : Optional[str] = None
    declaration : str = ''
    implementation : str = ''

    methods : Optional[list[TcMethod]] = None
    properties : Optional[list[TcProperty]] = None
    variable_sections: Optional[List[TcVariableSection]] = None
    documentation: Optional[TcDocumentation] = None
    
    def __post_init__(self):
        if self.variable_sections is None:
            self.variable_sections = []

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Pou):
        if xml_import is None:
            return None
            
        properties = []
        if hasattr(xml_import, 'property') and xml_import.property:
            properties = [TcProperty.from_xml_import(xml_import=prop) for prop in xml_import.property]
            
        methods = []
        if hasattr(xml_import, 'method') and xml_import.method:
            methods = [TcMethod.from_xml_import(xml_import=meth) for meth in xml_import.method]
        
        # Parse extends and implements from declaration
        extends = None
        implements = None
        variable_sections = []
        
        if xml_import.declaration:
            declaration_lines = xml_import.declaration.strip().split('\n')
            if declaration_lines:
                first_line = declaration_lines[0].strip()
                
                # Check for EXTENDS
                if ' EXTENDS ' in first_line:
                    # Extract the part after EXTENDS
                    extends_part = first_line.split(' EXTENDS ')[1]
                    # If there's an IMPLEMENTS part, remove it
                    if ' IMPLEMENTS ' in extends_part:
                        extends_part = extends_part.split(' IMPLEMENTS ')[0]
                    extends = extends_part.strip()
                
                # Check for IMPLEMENTS
                if ' IMPLEMENTS ' in first_line:
                    # Extract the part after IMPLEMENTS
                    implements_part = first_line.split(' IMPLEMENTS ')[1]
                    # Split by comma to get multiple interfaces
                    implements = [interface.strip() for interface in implements_part.split(',')]
            
            # Parse variable sections
            variable_sections = parse_variable_sections(xml_import.declaration)
            
            # Parse documentation
            documentation = parse_documentation(xml_import.declaration)
            
        return TcPou(name=xml_import.name,
                    declaration=xml_import.declaration, 
                    implementation=xml_import.implementation,
                    properties=properties,
                    methods=methods,
                    extends=extends,
                    implements=implements,
                    variable_sections=variable_sections,
                    documentation=documentation)

@dataclass
class TcItf:
    name : str = ''
    extends : Optional[list[str]] = None

    methods : Optional[list[TcMethod]] = None
    properties : Optional[list[TcProperty]] = None

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Itf):
        if xml_import is None:
            return None
            
        properties = []
        if hasattr(xml_import, 'property') and xml_import.property:
            properties = [TcProperty.from_xml_import(xml_import=prop) for prop in xml_import.property]
            
        methods = []
        if hasattr(xml_import, 'method') and xml_import.method:
            methods = [TcMethod.from_xml_import(xml_import=meth) for meth in xml_import.method]
        
        # Parse extends from declaration
        extends = None
        
        if xml_import.declaration:
            declaration_lines = xml_import.declaration.strip().split('\n')
            if declaration_lines:
                first_line = declaration_lines[0].strip()
                
                # Check for EXTENDS
                if ' Extends ' in first_line or ' EXTENDS ' in first_line:
                    # Extract the part after EXTENDS (case insensitive)
                    if ' Extends ' in first_line:
                        extends_part = first_line.split(' Extends ')[1]
                    else:
                        extends_part = first_line.split(' EXTENDS ')[1]
                    
                    # Split by comma to get multiple interfaces
                    extends = [interface.strip() for interface in extends_part.split(',')]
            
        return TcItf(name=xml_import.name,
                    properties=properties,
                    methods=methods,
                    extends=extends)

@dataclass
class TcDut:
    name : str = ''
    declaration : str = ''
    variable_sections: Optional[List[TcVariableSection]] = None
    documentation: Optional[TcDocumentation] = None
    
    def __post_init__(self):
        if self.variable_sections is None:
            self.variable_sections = []

    @classmethod
    def from_xml_import(cls, 
                        xml_import: Dut):
        if xml_import is None:
            return None
        
        variable_sections = []
        documentation = None
        if xml_import.declaration:
            # Parse variable sections
            variable_sections = parse_variable_sections(xml_import.declaration)
            
            # Parse documentation
            documentation = parse_documentation(xml_import.declaration)
            
        return TcDut(name=xml_import.name,
                    declaration=xml_import.declaration,
                    variable_sections=variable_sections,
                    documentation=documentation)
    



class TwinCatLoader:

    def __init__(self, 
                 search_path: str | Path,
                 tcObjects: list[(str,object)] = [],
                 name_space: Optional[str] = ''):
        
        self.tcObjects : list[object] = tcObjects
        self.search_paths: list[Path] = []
        self.name_space: str = name_space
        self.found_tcPou: list[Path] = []
        self.found_tcDut: list[Path] = []
        self.found_tcIo: list[Path] = []
        config = ParserConfig(fail_on_unknown_properties=True)
        self.parser = XmlParser(config=config)

        
        self.append_search_path(Path(search_path))
        
        self.search_for_tc_files(found_tc_files=self.found_tcPou, file_ending='.TcPou')
        self.search_for_tc_files(found_tc_files=self.found_tcDut, file_ending='.TcDut')
        self.search_for_tc_files(found_tc_files=self.found_tcIo, file_ending='.TcIo')


    def append_search_path(self, path: Path) -> None:
        path = path.resolve()
        if path not in self.search_paths:
            logger.info('add path: %s to search paths', path)
            self.search_paths.append(path)


    def search_for_tc_files(self, 
                            found_tc_files:list[Path], 
                            file_ending:str, ):

        for paths in self.search_paths:
            for path in paths.rglob('*'+ file_ending):
                found_tc_files.append(path)


    def load(self):

        for obj in self.found_tcPou:
            try:
                self.tcObjects.append((obj.name, TcPou.from_xml_import(self.parser.parse(obj, TcPlcObject).pou)))
                logger.info('loaded: %s', obj.name)
            except ParserError:
                logger.error('error when loading: %s', obj, exc_info=True)

        for obj in self.found_tcDut:
            try:
                self.tcObjects.append((obj.name, TcDut.from_xml_import(self.parser.parse(obj, TcPlcObject).dut)))
                logger.info('loaded: %s',obj.name)
            except ParserError:
                logger.error('error when loading: %s', obj, exc_info=True)
            
        for obj in self.found_tcIo:
            try:
                self.tcObjects.append((obj.name, TcItf.from_xml_import(self.parser.parse(obj, TcPlcObject).itf)))     
                logger.info('loaded: %s', obj.name)
            except ParserError:
                logger.error('error when loading: %s', obj, exc_info=True)

    def getItemByName(self, name:str) -> object | None:
        for obj_name, obj in self.tcObjects:
            if str(obj_name) == name:
                return obj

    def getAllItems(self)->list[(str, object)]:
        return self.tcObjects
   


if __name__ == '__main__':
    search_path:Path = 'TwincatFiles'
    tcObjects: list[object] = list()

    loader = TwinCatLoader(
        search_path=search_path,
        tcObjects=tcObjects
    )
    loader.load()

    print(len(tcObjects))

    #print(loader.getItemByName('FB_Base.TcPOU'))

    #print(tcObjects[0])
