#!/bin/bash

VENV_DIR="venv"

# Specify the libraries to install
REQUIRED_LIBS="numpy pandas Tk CTkTable customtkinter pillow matplotlib tabulate openpyxlu"

# Check if the virtual environment directory already exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment not found. Creating a new one..."
    python3 -m venv "$VENV_DIR"
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

pip install --upgrade pip

# Install the required libraries
pip install $REQUIRED_LIBS

echo "Libraries installed and virtual environment setup complete."