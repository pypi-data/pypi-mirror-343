#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Installation of the markdown2app package.
"""

import os
from setuptools import setup, find_packages

# Long description from README.md
try:
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.md"), encoding="utf-8") as f:
        LONG_DESCRIPTION = '\n' + f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ''

# Get version from _version.py
version = {}
with open("src/markdown2app/_version.py") as f:
    exec(f.read(), version)

# Configuration setup
setup(
    name="markdown2app",
    version=version["__version__"],
    description="libs to run markdown as an app in a python3 environment",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Tom Sapletta",
    author_email="tom@sapletta.com",
    maintainer="markdown2app developers",
    maintainer_email="info@softreck.dev",
    python_requires=">=3.7",
    url="https://markdown2app.plainmark.com",
    project_urls={
        "Repository": "https://github.com/plain-mark/markdown2app",
        "Changelog": "https://github.com/plain-mark/markdown2app/releases",
        "Wiki": "https://github.com/plain-mark/markdown2app/wiki",
        "Issue Tracker": "https://github.com/plain-mark/markdown2app/issues/new",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="Apache-2.0",
    license_files=("LICENSE",),
    keywords=["python", "markdown2app", "markdown", "app", "plainmark"],
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)