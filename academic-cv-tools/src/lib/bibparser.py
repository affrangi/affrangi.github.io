from typing import TYPE_CHECKING

import bibtexparser
from bibtexparser.bparser import BibTexParser

if TYPE_CHECKING:
    from bibtexparser.bibdatabase import BibDatabase


def json_entry_to_bibtex_entry(entry: str) -> str:
    bibtex = f"@{entry['ENTRYTYPE']}{{{entry['ID']},\n"
    for key, value in entry.items():
        if key not in ["ENTRYTYPE", "ID"]:
            bibtex += f"    {key} = {{{value}}},\n"
    bibtex = bibtex.rstrip(",\n") + "\n}\n\n"
    return bibtex


def parse_bibtex_file(file_name: str) -> "BibDatabase":
    parser = BibTexParser(
        ignore_nonstandard_types=False,
        homogenize_fields=True,
    )

    with open(file_name, "r") as bibtex_input:
        bib_database = bibtexparser.load(bibtex_input, parser=parser)

    return bib_database


def json_bib_to_bibtex(json_bib: list[dict]) -> str:
    bibtex = ""
    for entry in json_bib:
        bibtex += json_entry_to_bibtex_entry(entry)
    return bibtex
