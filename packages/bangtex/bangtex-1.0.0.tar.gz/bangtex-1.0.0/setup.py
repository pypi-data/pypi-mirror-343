#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bangtex",
    version="1.0.0",
    author="Rakib Mollah",
    author_email="rakib1703115@gmail.com",
    description="Unicode UTF-8 Bangla to Bangtex converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/username/bangtex",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "bangtex=bangtex.cli:main",
        ],
    },
)