#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Command-line interface for the Bangla to Bangtex converter
"""

import argparse
import sys
from .converter import convert_file

def main():
    """Entry point for the command-line interface"""
    parser = argparse.ArgumentParser(description='Convert utf8 Bangla to bangtex format')
    parser.add_argument('-d', action='store_true', help='Show unicode tokens')
    parser.add_argument('infile', nargs='?', type=str, help='Input file (default: stdin)')
    parser.add_argument('-o', '--output', type=str, help='Output file (default: stdout)')
    
    args = parser.parse_args()
    
    convert_file(args.infile, args.output, args.d)

if __name__ == "__main__":
    main()