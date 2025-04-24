#!/bin/bash

# Clean previous builds
rm -rf dist

# Build the package
python -m build

# Upload to PyPI using API key
python -m twine upload dist/* -u __token__ -p pypi-AgEIcHlwaS5vcmcCJDkwMTlkNmE2LWFkZmYtNGU2ZC1hYzUwLWFiYmRjYTg4YTNkYgACIlsxLFsiY29tcHV0ZXItdXNlLW9vdGItaW50ZXJuYWwiXV0AAixbMixbIjllNmQ5NTRjLTgxZGEtNGRkNy05Yjk5LWVjYzMzOGUwN2NlZSJdXQAABiBFIKbytGELyFb1-i20Cu4tSo8cAUlX1DCLmUALq0mcPA
