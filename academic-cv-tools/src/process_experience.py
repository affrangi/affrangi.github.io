import json

from lib.args import parse_args
from lib.config import read_cv_config
from lib.cventry import process_cventries
from lib.utils import process_date_range

# Parse command line arguments
args = parse_args()

entries_title = "experience"
input_path, output_path = read_cv_config(args["config"], entries_title)

current_entries = "current_positions"
past_entries = "past_positions"

with open(input_path, "r") as file:
    content = file.read()

parts = content.split("% PAST POSITIONS")
current_lines = parts[0].strip().splitlines()
past_lines = parts[1].strip().splitlines() if len(parts) > 1 else []

current_cv_entries = process_cventries(current_lines)
past_cv_entries = process_cventries(past_lines)


def process_experience(cv_entries: list[list[str]]) -> list[dict]:
    json_entries = []

    for entry in cv_entries:
        position = entry[0]
        institution = entry[1]
        location = entry[2]
        date_range = entry[3]
        highlights = entry[4]

        logo = ""  # Not used at the moment
        image = ""  # Not used at the moment
        url = ""

        if len(entry) > 5:
            logo = entry[5]
        if len(entry) > 6:
            image = entry[6]
        if len(entry) > 7:
            url = entry[7]

        start_date, end_date = process_date_range(date_range)

        json_entry = {
            "position": position,
            "institution": institution,
            "location": location,
            "startDate": start_date,
            "highlights": highlights,
            "url": url,
        }

        if end_date is not None:
            json_entry["endDate"] = end_date

        json_entries.append(json_entry)

    return json_entries


# Process current positions
json_current = process_experience(current_cv_entries)

# Process past positions
json_past = process_experience(past_cv_entries)

# Join current and past entries
json_entries = {
    current_entries: json_current,
    past_entries: json_past
}


with open(output_path, "w") as json_file:
    json.dump(json_entries, json_file, indent=4, ensure_ascii=False)
