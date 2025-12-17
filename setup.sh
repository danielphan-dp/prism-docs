#!/bin/bash
set -e

uv venv --python 3.12
uv pip install -e ".[all]"

echo "Run: source .venv/bin/activate"
