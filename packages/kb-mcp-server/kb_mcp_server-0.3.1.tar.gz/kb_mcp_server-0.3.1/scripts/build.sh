#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Change to the project root directory
cd "$(dirname "$0")/.."

# Ensure we have the latest version of uv
pip install -U uv

# Clean up any previous build artifacts
rm -rf dist build *.egg-info

# Ensure build and twine are installed
uv pip install build twine

# Build the package using standard Python build tool
echo "Building kb-mcp-server package..."
python -m build

# Upload to PyPI using twine
echo "Uploading to PyPI..."
twine upload dist/*

echo "Build and publish complete!"
echo "Package is now available at: https://pypi.org/project/kb-mcp-server/"
