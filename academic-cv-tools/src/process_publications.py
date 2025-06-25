import os

from lib.args import parse_args
from lib.bibparser import json_bib_to_bibtex, parse_bibtex_file
from lib.config import read_bib_config
from lib.utils import process_name
from lib.files import output_dir

# Parse command line arguments and read the BibTeX config file
args = parse_args()
file_paths, categories = read_bib_config(args["config"])

# Process each BibTeX file
processed_files = []
for file_path, category in zip(file_paths, categories):
    json_bib: list[dict] = parse_bibtex_file(file_path).entries

    for entry in json_bib:
        if "article-doi" in entry and "doi" not in entry:
            entry["doi"] = entry["article-doi"]
            del entry["article-doi"]

        if entry["ENTRYTYPE"] == "patent":
            date = entry.get("date", "")
            if date:
                # Extract year from date if available
                entry["year"] = date.split("-")[0]
            else:
                # Default to arbitrary year if date is not available (should not happen)
                entry["year"] = "2023"

            entry["is_patent"] = "true"
            entry["ENTRYTYPE"] = "online"

            if "bibtex_show" in entry:
                del entry["bibtex_show"]

        else:
            entry["bibtex_show"] = "true"

        if "author" in entry and isinstance(entry["author"], str):
            # Convert author names to initials
            authors = entry["author"].split(" and ")
            entry["author"] = " and ".join(
                [process_name(name) for name in authors]
            )

        if "editor" in entry and isinstance(entry["editor"], str):
            # Convert editor names to initials
            editors = entry["editor"].split(" and ")
            entry["editor"] = " and ".join(
                [process_name(name) for name in editors]
            )

        entry["category"] = category

    bibtex_output = ".".join(file_path.split(".")[:-1:]) + "_processed.bib"

    processed_files.append(bibtex_output)

    with open(bibtex_output, "w") as bibtex_file:
        bibtex_file.write(json_bib_to_bibtex(json_bib))

joined_bibtex_path = f"{output_dir()}/publications.bib"

# Join all bibtex files into a single file
with open(joined_bibtex_path, "w") as all_bibtex_file:
    for processed_file in processed_files:
        with open(processed_file, "r") as f:
            all_bibtex_file.write(f.read())

# Delete individual processed files
for processed_file in processed_files:
    try:
        os.remove(processed_file)
    except OSError as e:
        print(f"Error deleting file {processed_file}: {e}")
