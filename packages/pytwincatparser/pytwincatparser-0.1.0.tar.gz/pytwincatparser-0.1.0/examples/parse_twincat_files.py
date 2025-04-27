#!/usr/bin/env python3
"""
Example script demonstrating how to use pytwincatparser to parse TwinCAT files.
"""

from pathlib import Path
from pytwincatparser import TwinCatLoader, TcPou

def main():
    # Path to TwinCAT files
    search_path = Path("TwincatFiles")
    
    # Initialize empty list to store TwinCAT objects
    tc_objects = []
    
    # Create loader instance
    loader = TwinCatLoader(
        search_path=search_path,
        tcObjects=tc_objects
    )
    
    # Load all TwinCAT files
    loader.load()
    
    print(f"Loaded {len(tc_objects)} TwinCAT objects")
    
    # Print names of all loaded objects
    print("\nLoaded objects:")
    for name, obj in tc_objects:
        print(f"- {name}")
    
    # Get a specific POU by name
    fb_base = loader.getItemByName("FB_Base.TcPOU")
    if fb_base:
        print("\nFound FB_Base.TcPOU:")
        print(f"Name: {fb_base.name}")
        
        # Print extends and implements information
        if fb_base.extends:
            print(f"Extends: {fb_base.extends}")
        if fb_base.implements:
            print(f"Implements: {', '.join(fb_base.implements)}")
        
        # Print documentation
        if fb_base.documentation:
            print("\nDocumentation:")
            if fb_base.documentation.details:
                print(f"Details: {fb_base.documentation.details}")
            if fb_base.documentation.usage:
                print(f"Usage: {fb_base.documentation.usage}")
            if fb_base.documentation.brief:
                print(f"Brief: {fb_base.documentation.brief}")
            if fb_base.documentation.returns:
                print(f"Returns: {fb_base.documentation.returns}")
            if fb_base.documentation.custom_tags:
                print("Custom Tags:")
                for tag, value in fb_base.documentation.custom_tags.items():
                    print(f"  {tag}: {value}")
        
        # Print variable sections
        if hasattr(fb_base, 'variable_sections') and fb_base.variable_sections:
            print("\nVariable Sections:")
            for section in fb_base.variable_sections:
                print(f"- Section Type: {section.section_type}")
                print(f"  Variables:")
                for var in section.variables:
                    var_info = f"    - {var.name} : {var.type}"
                    if var.initial_value:
                        var_info += f" := {var.initial_value}"
                    if var.comment:
                        var_info += f" // {var.comment}"
                    print(var_info)
        
        # Print methods with access modifiers and return types
        if hasattr(fb_base, 'methods') and fb_base.methods:
            print("\nMethods:")
            for method in fb_base.methods:
                access_modifier = method.accessModifier if method.accessModifier else ""
                return_type = method.returnType if method.returnType else ""
                print(f"- {method.name} (Access Modifier: {access_modifier}, Return Type: {return_type})")
                
                # Print method documentation
                if method.documentation:
                    print(f"  Documentation:")
                    if method.documentation.brief:
                        print(f"    Brief: {method.documentation.brief}")
                    if method.documentation.details:
                        print(f"    Details: {method.documentation.details}")
                    if method.documentation.usage:
                        print(f"    Usage: {method.documentation.usage}")
                    if method.documentation.returns:
                        print(f"    Returns: {method.documentation.returns}")
                    if method.documentation.custom_tags:
                        print("    Custom Tags:")
                        for tag, value in method.documentation.custom_tags.items():
                            print(f"      {tag}: {value}")
                
                # Print method variable sections
                if hasattr(method, 'variable_sections') and method.variable_sections:
                    print(f"  Variable Sections:")
                    for section in method.variable_sections:
                        print(f"  - Section Type: {section.section_type}")
                        print(f"    Variables:")
                        for var in section.variables:
                            var_info = f"      - {var.name} : {var.type}"
                            if var.initial_value:
                                var_info += f" := {var.initial_value}"
                            if var.comment:
                                var_info += f" // {var.comment}"
                            print(var_info)
        
        # Print properties with return types
        if hasattr(fb_base, 'properties') and fb_base.properties:
            print("\nProperties:")
            for prop in fb_base.properties:
                return_type = prop.returnType if prop.returnType else ""
                print(f"- {prop.name} (Return Type: {return_type})")
    
    # Get a specific DUT by name
    st_pml_command = loader.getItemByName("ST_PmlCommand.TcDUT")
    if st_pml_command:
        print("\nFound ST_PmlCommand.TcDUT:")
        print(f"Name: {st_pml_command.name}")
        
        # Print documentation
        if st_pml_command.documentation:
            print("\nDocumentation:")
            if st_pml_command.documentation.details:
                print(f"Details: {st_pml_command.documentation.details}")
            if st_pml_command.documentation.usage:
                print(f"Usage: {st_pml_command.documentation.usage}")
            if st_pml_command.documentation.brief:
                print(f"Brief: {st_pml_command.documentation.brief}")
            if st_pml_command.documentation.returns:
                print(f"Returns: {st_pml_command.documentation.returns}")
            if st_pml_command.documentation.custom_tags:
                print("Custom Tags:")
                for tag, value in st_pml_command.documentation.custom_tags.items():
                    print(f"  {tag}: {value}")
        
        # Print variable sections
        if hasattr(st_pml_command, 'variable_sections') and st_pml_command.variable_sections:
            print("\nVariable Sections:")
            for section in st_pml_command.variable_sections:
                print(f"- Section Type: {section.section_type}")
                print(f"  Variables:")
                for var in section.variables:
                    var_info = f"    - {var.name} : {var.type}"
                    if var.initial_value:
                        var_info += f" := {var.initial_value}"
                    if var.comment:
                        var_info += f" // {var.comment}"
                    print(var_info)
    
    # Get a specific interface by name
    i_data = loader.getItemByName("I_Data.TcIO")
    if i_data:
        print("\nFound I_Data.TcIO:")
        print(f"Name: {i_data.name}")
        
        # Print extends information
        if i_data.extends:
            print(f"Extends: {', '.join(i_data.extends)}")
        
        # Print properties
        if hasattr(i_data, 'properties') and i_data.properties:
            print("\nProperties:")
            for prop in i_data.properties:
                return_type = prop.returnType if prop.returnType else ""
                print(f"- {prop.name} (Return Type: {return_type})")
        
        # Print methods
        if hasattr(i_data, 'methods') and i_data.methods:
            print("\nMethods:")
            for method in i_data.methods:
                return_type = method.returnType if method.returnType else ""
                print(f"- {method.name} (Return Type: {return_type})")

if __name__ == "__main__":
    main()
