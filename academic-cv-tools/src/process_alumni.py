import json

from lib.args import parse_args
from lib.bibparser import parse_bibtex_file
from lib.config import read_cv_config
from lib.utils import normalize_date

# Parse command line arguments and read the BibTeX config file
args = parse_args()
input_path, output_path = read_cv_config(args["config"], "alumni")

# Convert BibTeX to JSON format
json_bib: list[dict] = parse_bibtex_file(input_path).entries

# Process each entry in the JSON BibTeX data
for entry in json_bib:
    month = "" if "month" not in entry else entry["month"].strip()
    year = "" if "year" not in entry else entry["year"].strip()
    day = "" if "day" not in entry else entry["day"].strip()

    date = f"{day} {month} {year}"
    date = normalize_date(date)

    entry["date"] = date

    if "address" in entry:
        if "location" not in entry:
            entry["location"] = entry["address"]
        del entry["address"]


# Save the JSON data to a file
with open(output_path, "w") as file:

    json.dump(json_bib, file, indent=4)
