import json

from lib.args import parse_args
from lib.config import read_cv_config
from lib.cventry import process_cventries
from lib.utils import process_date_range

# Parse command line arguments
args = parse_args()

entries_title = "funding"
input_path, output_path = read_cv_config(args["config"], entries_title)

with open(input_path, "r") as file:
    lines = file.readlines()

cv_entries = process_cventries(lines)
json_entries = []

for entry in cv_entries:
    # Mandatory fields
    subtitle = entry[0]
    title = entry[1]
    institution = entry[2]
    date = entry[3]
    description = entry[4]

    start_date, end_date = process_date_range(date)

    # Optional fields
    logo = ""
    image = ""
    url = ""

    if len(entry) > 5:
        logo = entry[5]
    if len(entry) > 6:
        image = entry[6]
    if len(entry) > 7:
        url = entry[7]

    json_entry = {
        "subtitle": subtitle,
        "title": title,
        "institution": institution,
        "startDate": start_date,
        "endDate":  end_date or start_date,
        "description": description,
        "img": image,
        "logo": logo,
        "url": url,
    }

    json_entries.append(json_entry)


with open(output_path, "w") as json_file:
    json.dump({entries_title: json_entries},
              json_file, indent=4, ensure_ascii=False)
