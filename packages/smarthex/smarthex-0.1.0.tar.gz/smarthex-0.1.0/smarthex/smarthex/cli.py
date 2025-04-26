#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SmartHex16 CLI - Command-line interface for SmartHex operations.
#
# Author: Victor Matos (@spacemany2k38, @vvrmatos)
# Email: contact@byteram.co
# Date: 2025-04-25
# Title: Applied Mathematician
#

import sys
import argparse
from smarthex import SmartHex

def main():
    """Command-line interface for SmartHex operations."""
    parser = argparse.ArgumentParser(description='SmartHex identifier operations')
    parser.add_argument('-e', '--validate', metavar='VALUE', 
                       help='Validate if the given value is a SmartHex identifier')
    
    args = parser.parse_args()
    smart_hex = SmartHex()
    
    if args.validate:
        is_valid = smart_hex.validate(args.validate)
        print(f"{args.validate} is {'valid' if is_valid else 'invalid'} SmartHex identifier")
        sys.exit(0 if is_valid else 1)
    
    print(smart_hex.generate())

if __name__ == "__main__":
    main() 