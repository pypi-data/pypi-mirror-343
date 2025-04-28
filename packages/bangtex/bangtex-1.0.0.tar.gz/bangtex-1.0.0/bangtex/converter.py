#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Unicode UTF-8 Bangla to Bangtex converter - Core functionality

This module contains the core conversion functionality for transforming
Unicode UTF-8 Bangla text to Bangtex format.
"""

import re
import sys
from io import StringIO

# Character constants as hex values
ZWNJ = "\u200c"
ZWJ = "\u200d"
Aw = "\u0985"
Aaa = "\u0986"
CNBND = "\u0981"
DNARI = "\u0964"
DDNARI = "\u0965"
HSNT = "\u09cd"
Yjaw = "\u09af"
Akar = "\u09be"
Raw = "\u09b0"

# Bangla Unicode to Bangtex mapping
bangtex = {
    # Devnagari DANDA and DOUBLE DANDA
    0x964: ".", 0x965: "..",
    # Chandrabindu, Anuswar, and Bisorgo
    0x981: "NN", 0x982: "NNG", 0x983: "{h}",
    # Swarabarna
    0x985: "A", 0x986: "Aa", 0x987: "{I}", 0x988: "II",
    0x989: "U", 0x98a: "UU", 0x98b: "RR", 0x98f: "E", 0x990: "OI",
    0x993: "{O}", 0x994: "OU",
    # Main Banjonbarna
    0x995: "k", 0x996: "kh", 0x997: "g", 0x998: "gh", 0x999: "NG",
    0x99a: "c", 0x99b: "ch", 0x99c: "j", 0x99d: "jh", 0x99e: "NJ",
    0x99f: "T", 0x9a0: "Th", 0x9a1: "D", 0x9a2: "Dh", 0x9a3: "N",
    0x9a4: "t", 0x9a5: "th", 0x9a6: "d", 0x9a7: "dh", 0x9a8: "n",
    0x9aa: "p", 0x9ab: "ph", 0x9ac: "b", 0x9ad: "bh", 0x9ae: "m",
    0x9af: "J", 0x9b0: "r", 0x9b2: "l", 0x9b6: "sh", 0x9b7: "Sh",
    0x9b8: "s", 0x9b9: "H",
    # Kars
    0x9be: "a", 0x9bf: "i", 0x9c0: "ii", 0x9c1: "u", 0x9c2: "uu",
    0x9c3: "rR", 0x9c7: "e", 0x9c8: "{oi}", 0x9cb: "ea", 0x9cc: "eou",
    # HASANTA, Khandatta, and right-ou-kar
    0x9cd: ":/", 0x9ce: "t//", 0x9d7: "ou",
    # Doy-shuno-rha, DDHHoy-shunyo-rrha, and Yaw
    0x9dc: "rh", 0x9dd: "rhh", 0x9df: "y",
    # Numerals
    0x9e6: "0", 0x9e7: "1", 0x9e8: "2", 0x9e9: "3", 0x9ea: "4",
    0x9eb: "5", 0x9ec: "6", 0x9ed: "7", 0x9ee: "8", 0x9ef: "9",
    # Special punctuation bar, ZWNJ, and ZWJ:
    0x9f7: ".", 0x200c: "", 0x200d: ""
}

bangtexphola = {
    0x9a3: "/N", 0x9a8: "/n",
    0x9ac: "W", 0x9ae: "M", 0x9af: "Y", 0x9b0: "R", 0x9b2: "L",
    0x9df: "Y"
}

# Character class ranges as regex patterns
def build_unicode_range_pattern(ranges_str):
    """Convert a string of hex ranges to a regex pattern"""
    pattern_parts = []
    for line in ranges_str.strip().split('\n'):
        if not line or line.startswith('#'):
            continue
        if line.startswith('+main::'):
            # Include another defined range
            range_name = line[7:]
            pattern_parts.append(globals()[range_name]())
        elif line.startswith('-main::'):
            # Exclude another defined range
            # This requires negation within the character class
            # In Python regex, we would handle this differently
            continue
        else:
            start, end = line.split('\t')
            pattern_parts.append(f"\\u{start}-\\u{end}")
    
    return "[" + "".join(pattern_parts) + "]"

def InSwarabarna():
    return build_unicode_range_pattern("""
0985\t098c
098f\t0990
0993\t0994
""")

def InKars():
    return build_unicode_range_pattern("""
09bc\t09bc
09be\t09c4
09c7\t09c8
09cb\t09cc
09d7\t09d7
""")

def InAtoms():
    return build_unicode_range_pattern("""
0981\t0983
09ce\t09ce
09e6\t09ef
""")

def InPostSticky():
    return build_unicode_range_pattern("""
09bc\t09bc
09be\t09c4
09c7\t09c8
09cb\t09cc
09d7\t09d7
0981\t0981
09cd\t09cd
200c\t200c
""")

def InBinaryJoiner():
    return build_unicode_range_pattern("""
09cd\t09cd
""")

def InByanjon():
    return build_unicode_range_pattern("""
0995\t09a8
09aa\t09b0
09b2\t09b2
09b6\t09b9
09dc\t09dd
09df\t09df
""")

def InYaPhola():
    return build_unicode_range_pattern("""
09af\t09af
09df\t09df
""")

def InNaPhola():
    return build_unicode_range_pattern("""
09a3\t09a3
09a8\t09a8
""")

def InBaMaRaLaPhola():
    return build_unicode_range_pattern("""
09ac\t09ac
09ae\t09ae
09b0\t09b0
09b2\t09b2
""")

def InPholaNotYa():
    return build_unicode_range_pattern("""
09a3\t09a3
09a8\t09a8
09ac\t09ac
09ae\t09ae
09b0\t09b0
09b2\t09b2
""")

def InPholaNotNa():
    return build_unicode_range_pattern("""
09af\t09af
09df\t09df
09ac\t09ac
09ae\t09ae
09b0\t09b0
09b2\t09b2
""")

def InPhola():
    return build_unicode_range_pattern("""
09af\t09af
09df\t09df
09a3\t09a3
09a8\t09a8
09ac\t09ac
09ae\t09ae
09b0\t09b0
09b2\t09b2
""")

def InByajonNotPhola():
    # This is more complex due to the exclusion pattern
    # Creating a pattern that includes Byanjon but excludes PholaNotNa
    # For simplicity, explicitly defining the range
    return build_unicode_range_pattern("""
0995\t09a2
09a4\t09a7
09aa\t09ad
09b6\t09b9
09dc\t09dd
""")

def _get_token_pattern():
    """Build the main regex pattern that matches tokens"""
    return re.compile(
        fr'('
        fr'[^\u0980-\u09ff]|'  # non-Bengali characters
        fr'{Aw}{CNBND}?{HSNT}(?:{InYaPhola()}){CNBND}?{Akar}|'  # special pattern
        fr'{Aw}{Akar}{CNBND}?|'  # Aa with chandrabindu
        fr'{Aw}{CNBND}?{Akar}|'  # Aa with chandrabindu (alternate)
        fr'(?:{InSwarabarna()}){CNBND}?|'  # Swarabarna
        fr'(?:{InAtoms()})|'  # Atoms
        fr'(?:{InKars()})|'  # Kars
        fr'(?:{InByanjon()})(?!(?:{InPostSticky()}))|'  # Byanjon without post-sticky
        fr'(?:{Raw}(?:{InBinaryJoiner()})(?=(?:{InByanjon()})))?'  # optional reph
        fr'(?:{InByanjon()}){CNBND}?'  # main character
        fr'(?:(?:{InBinaryJoiner()})(?:{InByajonNotPhola()}))?'  # juktakkhor
        fr'{CNBND}?'
        fr'(?:{ZWNJ}?(?:{InBinaryJoiner()})(?:{InPholaNotYa()}))?'  # Phola but non-Ya-Phola
        fr'{CNBND}?'
        fr'(?:{HSNT}(?!(?:{InByanjon()})))?'  # real Hasanta
        fr'(?:{ZWNJ}?(?:{InBinaryJoiner()})(?:{InYaPhola()}))?'  # Ya-Phola
        fr'{CNBND}?'
        fr'(?:{HSNT}(?!(?:{InByanjon()})))?'  # real Hasanta
        fr'{CNBND}?'
        fr'(?:(?:{InKars()}))?'  # optional Kar
        fr'{CNBND}?|'
        fr'.(?={ZWNJ})|'  # character followed by ZWNJ
        fr'.'  # Any other character (cannot parse)
        fr')',
        re.DOTALL
    )

def convert_text(text, show_tokens=False):
    """
    Convert a string of Bangla text to Bangtex format
    
    Args:
        text (str): The Bangla text to convert
        show_tokens (bool): Whether to show unicode tokens
        
    Returns:
        str: The converted text in Bangtex format
    """
    pattern = _get_token_pattern()
    result = StringIO()
    
    for line in text.splitlines(True):  # keepends=True to preserve line endings
        pos = 0
        while pos < len(line):
            match = pattern.search(line, pos)
            if not match:
                break
            
            tok = match.group(1)
            ulist = [ord(c) for c in tok]
            
            if show_tokens:
                result.write("\n")
                result.write(" ".join([f"{c:04x}" for c in ulist]) + " : ")
            
            # Check if token contains chandrabindu
            if_cnbnd = "NN" if CNBND in tok else ""
            
            jotil = ""
            
            # Single character token
            if len(ulist) == 1 or (len(ulist) == 2 and (ulist[1] == 0x981 or ulist[1] == 0x9cd)):
                for c in ulist:
                    if c <= 0xff:
                        jotil += chr(c)
                    elif c in bangtex:
                        jotil += bangtex[c]
                    else:
                        jotil += f"\\Ucx{{{c:04x}}}"
            
            # Special case: Aw + HSNT + YaPhola + Akar
            elif re.match(fr'^{Aw}{CNBND}?{HSNT}(?:{InYaPhola()}){CNBND}?{Akar}$', tok):
                jotil += f"A{if_cnbnd}Ya"
            
            # Special case: Aw + Akar (with optional chandrabindu)
            elif re.match(fr'^{Aw}{Akar}{CNBND}?$', tok) or re.match(fr'^{Aw}{CNBND}?{Akar}$', tok):
                jotil += f"Aa{if_cnbnd}"
            
            # Complex token with juktakhors, pholas, etc.
            elif re.match(
                fr'^({Raw}{InBinaryJoiner()})?'
                fr'({InByanjon()})'
                fr'{CNBND}?'
                fr'({InBinaryJoiner()}{InByajonNotPhola()})?'
                fr'{CNBND}?'
                fr'({ZWNJ}?{InBinaryJoiner()}{InPholaNotYa()})?'
                fr'{CNBND}?'
                fr'({HSNT}(?!{InByanjon()}))?'
                fr'({ZWNJ}?{InBinaryJoiner()}{InYaPhola()})?'
                fr'{CNBND}?'
                fr'({HSNT}(?!{InByanjon()}))?'
                fr'{CNBND}?'
                fr'({InKars()})?'
                fr'{CNBND}?$',
                tok
            ):
                # Extract components using regex
                m = re.match(
                    fr'^({Raw}{InBinaryJoiner()})?'
                    fr'({InByanjon()})'
                    fr'{CNBND}?'
                    fr'({InBinaryJoiner()}{InByajonNotPhola()})?'
                    fr'{CNBND}?'
                    fr'({ZWNJ}?{InBinaryJoiner()}{InPholaNotYa()})?'
                    fr'{CNBND}?'
                    fr'({HSNT}(?!{InByanjon()}))?'
                    fr'({ZWNJ}?{InBinaryJoiner()}{InYaPhola()})?'
                    fr'{CNBND}?'
                    fr'({HSNT}(?!{InByanjon()}))?'
                    fr'{CNBND}?'
                    fr'({InKars()})?'
                    fr'{CNBND}?$',
                    tok
                )
                
                # Check for reph
                if m.group(1):
                    jotil += "r/"
                
                # Get main byanjon
                main_banj = ord(m.group(2))
                main_bang = bangtex[main_banj]
                post_bang = ""
                
                # Check for juktakkhor
                if m.group(3):
                    jukt_banj = ord(m.group(3)[-1])  # Get the last character (the consonant)
                    
                    # Special cases for bangtex
                    if main_banj == 0x995 and jukt_banj == 0x9b7:
                        main_bang = "kK"
                        post_bang = ""
                    elif main_banj == 0x9b9 and jukt_banj == 0x9a8:
                        main_bang = "n"
                        post_bang = "/H"
                    elif main_banj == 0x9b9 and jukt_banj == 0x9a3:
                        main_bang = "N"
                        post_bang = "/H"
                    elif main_banj == 0x99c and jukt_banj == 0x99e:
                        main_bang = "g"
                        post_bang = "/Y"
                    else:
                        post_bang = "/" + bangtex[jukt_banj]
                
                jotil += main_bang + post_bang
                
                # Check for phola
                if m.group(4):
                    phola_str = m.group(4)
                    phola_char = phola_str[-1]  # Last character is the phola
                    if ord(phola_char) in bangtexphola:
                        jotil += bangtexphola[ord(phola_char)]
                
                jotil += if_cnbnd
                
                # Check for real hasanta
                if m.group(5):
                    jotil += ":/"
                
                # Check for Ya-phola
                if m.group(6):
                    jotil += "Y"
                
                # Check for another real hasanta
                if m.group(7):
                    jotil += ":/"
                
                # Check for kar
                if m.group(8):
                    k = ord(m.group(8))
                    if k == 0x9bf:  # hrashwa-i-kar
                        jotil = "i" + jotil
                    elif k == 0x9c7:  # e-kar
                        jotil = "e" + jotil
                    elif k == 0x9c8:  # oi-kar
                        jotil = "{oi}" + jotil
                    elif k == 0x9cb:  # o-kar
                        jotil = "e" + jotil + "a"
                    elif k == 0x9cc:  # ou-kar
                        jotil = "e" + jotil + "ou"
                    else:
                        jotil += bangtex[k]
            
            else:
                sys.stderr.write("PARSE ERROR 3!!!\n")
            
            if show_tokens:
                jotil = f"(\"{jotil}\")"
            
            result.write(jotil)
            pos = match.end()
        
        if show_tokens:
            result.write("\n")
    
    return result.getvalue()

def convert_file(input_file=None, output_file=None, show_tokens=False):
    """
    Convert a file of Bangla text to Bangtex format
    
    Args:
        input_file (str, optional): Path to input file. If None, uses stdin.
        output_file (str, optional): Path to output file. If None, uses stdout.
        show_tokens (bool): Whether to show unicode tokens
        
    Returns:
        None
    """
    # Set up input file
    if input_file and input_file != "-":
        try:
            infile = open(input_file, 'r', encoding='utf-8')
        except:
            sys.stderr.write(f"Could not open \"{input_file}\" for reading\n")
            sys.exit(1)
    else:
        infile = sys.stdin
    
    # Set up output file
    if output_file:
        try:
            outfile = open(output_file, 'w', encoding='utf-8')
        except:
            sys.stderr.write(f"Could not open \"{output_file}\" for writing\n")
            sys.exit(1)
    else:
        outfile = sys.stdout
    
    # Read the entire file
    text = infile.read()
    
    # Convert and write
    result = convert_text(text, show_tokens)
    outfile.write(result)
    
    # Close files if they're not stdin/stdout
    if input_file and input_file != "-":
        infile.close()
    if output_file:
        outfile.close()