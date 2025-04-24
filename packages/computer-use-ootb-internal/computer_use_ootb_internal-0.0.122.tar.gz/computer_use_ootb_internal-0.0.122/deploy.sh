#!/bin/bash

# Clean previous builds
rm -rf dist

# Build the package
python -m build

# Upload to PyPI using API key
python -m twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJGNiMDY2MzY0LWU0YWItNGNkZi1iNmJiLWViOTVjYTQ1NDA3NgACKlszLCIyNjgwNjg2Yy1lZDk2LTQxZGYtYjE2MC02ZGRmYWM4YjBlMWQiXQAABiC8l1-r93zvUfQ4W-aqfGCKady5e-94jEFbPA1SFyDgCw
