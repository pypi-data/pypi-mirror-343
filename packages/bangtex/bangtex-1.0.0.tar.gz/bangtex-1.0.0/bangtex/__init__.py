#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unicode UTF-8 Bangla to Bangtex converter

This program will convert a unicode utf8 encoded Bangla source text
file for TeX/LaTeX into bangtex format.

Copyright (C) 2006  Abhijit Dasgupta (takdoom@yahoo.com)
Python port: 2025

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

from .converter import convert_text, convert_file

__version__ = '1.0.0'
__all__ = ['convert_text', 'convert_file']