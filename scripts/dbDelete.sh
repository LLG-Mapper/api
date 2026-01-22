#!/bin/bash
# Get the folder where this script is located
SCRIPT_DIR=$(dirname "$0")

# Delete migrations and instance folders relative to the script
rm -rf "$SCRIPT_DIR/../migrations"
rm -rf "$SCRIPT_DIR/../instance"

echo "Deleted migrations and instance folders."