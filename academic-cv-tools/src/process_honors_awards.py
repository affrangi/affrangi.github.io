import json

from lib.args import parse_args
from lib.config import read_cv_config
from lib.cvhonor import process_cvhonors
from lib.utils import process_date_range

# Parse command line arguments
args = parse_args()

entries_title = "awards"
input_path, output_path = read_cv_config(args["config"], entries_title)

international = "international_awards"
domestic = "domestic_awards"

with open(input_path, "r") as file:
    content = file.read()

parts = content.split("% DOMESTIC HONORS")
international_lines = parts[0].strip()
domestic_lines = parts[1].strip() if len(parts) > 1 else []

international_cv_honors = process_cvhonors(international_lines)
domestic_cv_entries = process_cvhonors(domestic_lines)


def process_honors(cv_honors: list[list[str]]) -> list[dict]:
    json_honors = []

    for honor in cv_honors:
        # Mandatory arguments
        award = honor[0]
        description = honor[1]
        location = honor[2]
        date = honor[3]

        # Optional arguments
        url = None

        if len(honor) > 4:
            url = honor[4]

        json_honor = {
            "award": award,
            "description": description,
            "location": location,
            "date": date,
        }

        if url:
            json_honor["url"] = url

        json_honors.append(json_honor)

    return json_honors


international_json_honors = process_honors(international_cv_honors)
domestic_json_honors = process_honors(domestic_cv_entries)

json_honors = {
    international: international_json_honors,
    domestic: domestic_json_honors
}

with open(output_path, "w") as json_file:
    json.dump(json_honors,
              json_file, indent=4, ensure_ascii=False)
