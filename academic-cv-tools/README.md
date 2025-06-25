# `academic-cv-tools`

This is a small python module to parse `.tex` and `.bib` files
from the `academic-cv` LaTeX template and output the `json` data 
used to generate some of the pages in this GitHub Pages site. 

## Setup

```bash
cd academic-cv-tools
sudo apt-get update
sudo apt-get install python3-pip python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
chmod +x compile.sh
```

## Usage

```bash
./compile.sh
```