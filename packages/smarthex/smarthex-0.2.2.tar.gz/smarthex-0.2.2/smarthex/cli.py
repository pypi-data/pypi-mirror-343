#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SmartHex16 CLI - Command-line interface for SmartHex operations.
"""
import argparse
import sys
from typing import Optional

from smarthex import SmartHex, __version__

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="SmartHex16 - Generate and validate hexadecimal identifiers"
    )
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"SmartHex16 v{__version__}"
    )
    parser.add_argument(
        "-g", 
        "--generate",
        action="store_true",
        help="Generate a new SmartHex16 identifier"
    )
    parser.add_argument(
        "-v", 
        "--validate",
        metavar="ID",
        help="Validate a SmartHex16 identifier"
    )
    return parser

def main(args: Optional[list[str]] = None) -> int:
    """Main entry point for the CLI."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    smarthex = SmartHex()
    
    if parsed_args.generate:
        print(smarthex.generate())
        return 0
        
    if parsed_args.validate:
        is_valid = smarthex.validate(parsed_args.validate)
        print(f"'{parsed_args.validate}' is {'valid' if is_valid else 'invalid'}")
        return 0 if is_valid else 1
        
    parser.print_help()
    return 0

if __name__ == "__main__":
    sys.exit(main()) 