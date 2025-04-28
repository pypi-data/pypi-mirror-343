# Bangtex

Unicode UTF-8 Bangla to Bangtex converter

This program will convert a unicode utf8 encoded Bangla source text file for TeX/LaTeX into bangtex format.

## Installation

```bash
pip install bangtex
```

## Usage

```bash
from bangtex import convert_text

bangla_text = "বাংলা টেক্সট"
bangtex_text = convert_text(bangla_text)
print(bangtex_text)
```