def parse_args_cv() -> dict:
    """Parse command line arguments."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Academic CV Tools CLI")

    parser.add_argument(
        "input",
        type=str,
        help="Path to the BibTeX or LaTeX file to process.",
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Path to the output JSON file. By default, it will be the same as the input file with a .json extension.",
    )

    variables = vars(parser.parse_args(sys.argv[1:]))

    if not variables["output"]:
        # Default output file is the input file with .json extension
        variables["output"] = variables["input"].rsplit(".", 1)[0] + ".json"

    if not variables["input"].endswith((".bib", ".tex")):
        raise ValueError("Input file must be a .bib or .tex file.")

    if variables["output"] and not variables["output"].endswith(".json"):
        raise ValueError("Output file must be a .json file.")

    return variables


def parse_args() -> dict:
    """Parse command line arguments."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Academic CV Tools CLI")

    parser.add_argument(
        "config",
        type=str,
        help="Path to the JSON config file specifying the sources to parse.",
    )

    variables = vars(parser.parse_args(sys.argv[1:]))

    if not variables["config"].endswith(".json"):
        raise ValueError("Config file must be a .json file.")

    return variables
