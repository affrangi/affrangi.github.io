from lib.files import input_dir, output_dir


def read_bib_config(config_path: str) -> tuple[list[str], list[str]]:
    """Read the BibTeX config file and return the sources and categories."""
    import json

    with open(config_path, "r") as file:
        config = json.load(file)

    input_directory = input_dir()
    data = {
        f"{input_directory}/{source['file']}": source["category"]
        for source in config["bibliography"]
        if "file" in source and "category" in source
    }

    return list(data.keys()), list(data.values())


def read_cv_config(config_path: str, section: str) -> tuple[str, str]:
    """Read the CV config file and return the input and output paths."""
    import json

    with open(config_path, "r") as file:
        config = json.load(file)

    input_file = config[section]
    output_file = input_file.replace(".tex", ".json")

    input_path = f"{input_dir()}/{input_file}"

    if section == "alumni":
        output_path = f"{output_dir()}/alumni.json"
    else:
        output_path = f"{output_dir()}/{output_file}"

    return input_path, output_path
