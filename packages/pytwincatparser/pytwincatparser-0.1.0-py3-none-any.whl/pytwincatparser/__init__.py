"""
pytwincatparser - A Python package for parsing TwinCAT PLC files using xsdata.
"""

from .TwincatParser import (
    TwinCatLoader,
    TcPou,
    TcDut,
    TcItf,
    TcMethod,
    TcProperty,
    TcGet,
    TcSet,
    TcVariable,
    TcVariableSection,
    TcDocumentation,
)

__version__ = "0.1.0"
__all__ = [
    "TwinCatLoader",
    "TcPou",
    "TcDut",
    "TcItf",
    "TcMethod",
    "TcProperty",
    "TcGet",
    "TcSet",
    "TcVariable",
    "TcVariableSection",
    "TcDocumentation",
]
