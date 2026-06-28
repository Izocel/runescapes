#!/bin/bash
set -e

# -----------------------------------------
# Create virtual environment only if missing
# -----------------------------------------
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
else
    echo "Virtual environment already exists."
fi

# -----------------------------------------
# Try activation in Git Bash / Linux / macOS
# -----------------------------------------
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
else
    echo "Could not activate venv. Activate manually and rerun."
    exit 1
fi

# -----------------------------------------
# Verify activation
# -----------------------------------------
if [[ "$VIRTUAL_ENV" == "" ]]; then
    echo "Virtual environment is not activated."
    exit 1
fi

# -----------------------------------------
# Check for pip
# -----------------------------------------
python -m pip install --upgrade pip

# -----------------------------------------
# Install dependencies
# -----------------------------------------
rm -f deps-lock.txt
pip install -r deps.txt --upgrade
pip freeze > deps-lock.txt

echo "Environment ready."
