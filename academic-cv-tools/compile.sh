#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Get the directory of the current script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &>/dev/null && pwd)

# Info
echo "Running academic-cv-tools to compile your academic data!"
echo ""
echo "Processing resume data..."

# Process the cv data
echo " ├─ Processing education data..."
python3 "$SCRIPT_DIR/src/process_education.py" "$SCRIPT_DIR/input/config.json"
echo " ├─ Processing experience data..."
python3 "$SCRIPT_DIR/src/process_experience.py" "$SCRIPT_DIR/input/config.json"
echo " ├─ Processing honors and awards data..."
python3 "$SCRIPT_DIR/src/process_honors_awards.py" "$SCRIPT_DIR/input/config.json"
echo " └─ Processing scholarships and fellowships data..."
python3 "$SCRIPT_DIR/src/process_scholarships_fellowships.py" "$SCRIPT_DIR/input/config.json"

# Join the cv data
echo "Joining resume data..."
python3 "$SCRIPT_DIR/src/join.py" "$SCRIPT_DIR/input/basics.json" "$SCRIPT_DIR/output/experience.json" \
    "$SCRIPT_DIR/output/education.json" "$SCRIPT_DIR/output/fellowships.json" "$SCRIPT_DIR/output/honors.json"

# Process the funding data
echo "Processing funding data..."
python3 "$SCRIPT_DIR/src/process_funding.py" "$SCRIPT_DIR/input/config.json"

# Process the publications data
echo "Processing publications data..."
python3 "$SCRIPT_DIR/src/process_publications.py" "$SCRIPT_DIR/input/config.json"

# Process the alumni data
echo "Processing alumni data..."
python3 "$SCRIPT_DIR/src/process_alumni.py" "$SCRIPT_DIR/input/config.json"

# Clean up the output directory
echo "Cleaning up output directory..."
rm -rf "$SCRIPT_DIR/output/experience.json" \
    "$SCRIPT_DIR/output/education.json" \
    "$SCRIPT_DIR/output/fellowships.json" \
    "$SCRIPT_DIR/output/honors.json"

# Final message
echo ""
echo "Academic CV data processing complete!"
echo "Output files are located in the output directory: $SCRIPT_DIR/output/."
