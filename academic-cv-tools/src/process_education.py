import json

from lib.args import parse_args
from lib.config import read_cv_config
from lib.cventry import process_cventries

# Parse command line arguments
args = parse_args()

entries_title = "education"
input_path, output_path = read_cv_config(args["config"], entries_title)

with open(input_path, "r") as file:
    lines = file.readlines()

cv_entries = process_cventries(lines)
json_entries = []

for entry in cv_entries:
    education_title = entry[0]
    education_institution = entry[1]
    education_location = entry[2]
    education_year = entry[3]
    education_description = entry[4]

    education_logo = ""
    education_image = ""  # Not used
    education_url = ""  # Not used

    if len(entry) > 5:
        education_logo = entry[5]
    if len(entry) > 6:
        education_image = entry[6]
    if len(entry) > 7:
        education_url = entry[7]

    json_entry = {
        "institution": education_institution,
        "url": education_url,
        "location": education_location,
        "name": education_title,
        "startDate": education_year,
        "endDate": education_year,
        "notes": education_description,
    }

    json_entries.append(json_entry)


with open(output_path, "w") as json_file:
    json.dump({entries_title: json_entries},
              json_file, indent=4, ensure_ascii=False)
