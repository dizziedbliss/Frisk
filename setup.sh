#!/bin/bash

if [ ! -d "venv" ]; then
    echo "No virtual environment found. Creating one..."
    python -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate || { echo "Failed to activate venv"; exit 1; }

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install --upgrade -r requirements.txt

echo "All set!"


#!USELESSSSSS
#TODO:COMPLETE THIS