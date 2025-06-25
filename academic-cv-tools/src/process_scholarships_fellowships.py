import json

from lib.cvhonor import process_cvhonors
from lib.utils import process_date_range
from lib.args import parse_args
from lib.config import read_cv_config

# Parse command line arguments
args = parse_args()

fellowships = "scholarships_and_fellowships"
input_path, output_path = read_cv_config(args["config"], fellowships)

with open(input_path, "r") as file:
    lines = file.readlines()

cv_honors = process_cvhonors(lines)
json_honors = []

for honor in cv_honors:
    # Mandatory arguments
    award = honor[0]
    institution = honor[1]
    location = honor[2]
    date = honor[3]

    start_date, end_date = process_date_range(date)

    # Optional arguments
    url = None

    if len(honor) > 4:
        url = honor[4]

    json_honor = {
        "award": award,
        "institution": institution,
        "location": location,
        "startDate": start_date,
        "endDate": end_date,
    }

    if url:
        json_honor["url"] = url

    json_honors.append(json_honor)


with open(output_path, "w") as json_file:
    json.dump({fellowships: json_honors},
              json_file, indent=4, ensure_ascii=False)
