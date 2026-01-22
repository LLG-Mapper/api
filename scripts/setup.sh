#!/bin/bash
# Setup script for Unix-like systems
# Run from the project root directory
python -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
echo "Virtual environment activated."
./scripts/dbCreate.sh
echo "Database created."
python -m app.seeds.seed
echo "Database seeded."
echo "Setup complete."