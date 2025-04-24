#!/bin/bash

# Clean previous builds
rm -rf dist

# Build the package
python -m build

# Upload to PyPI using API key
python -m twine upload dist/* -u __token__ -p 
