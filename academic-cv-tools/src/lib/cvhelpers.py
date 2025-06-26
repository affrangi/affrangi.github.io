import re

from lib.utils import add_dot, remove_comments, tex_to_html, unwrap_braces, parse_surrounded_text


def clean_cv(content: str | list[str]) -> str:
    """
    Clean a cv file to make it ready for parsing.

    Parameters
    ----------
    content : str | list[str]
        The content to process, either as a single string or a list of strings.

    Returns
    -------
    str
        A cleaned string with comments removed, newlines adjusted, and
        cventries/cvhonors ready for parsing.
    """
    if isinstance(content, str):
        content = content.splitlines()
    elif not isinstance(content, list):
        raise TypeError("Input must be a string or a list of strings.")

    lines = remove_comments(content)  # Remove comments from each line
    lines = [line.strip()
             for line in lines if line.strip()]  # Remove empty lines

    content = "\n".join(lines)  # Join lines into a single string

    content = re.sub(r"\n", " ", content)
    content = re.sub(r"\\begin\{cvitems\}", "", content)
    content = re.sub(r"\\end\{cvitems\}", "", content)
    content = re.sub(r"\\cv", r"\n\\cv", content)
    content = re.sub(r"\\end", r"\n\\end", content)
    content = re.sub(r"\\begin", r"\n\\begin", content)

    return content


def clean_cv_items(
    cv_items: list[str],
    nr_mandatory_args: int,
    nr_optional_args: int,
) -> list[list[str]]:
    """
    Clean and process cventries or cvhonors from a CV file.
    Each cventry/cvhonor can have a variable number of optional arguments
    and must have a fixed number of mandatory arguments.

    Parameters
    ----------
    cv_items : list[str]
        A list of cvitem/cvhonor strings to clean.
    nr_mandatory_args : int
        The number of mandatory arguments each cventry/cvhonor must have.
    nr_optional_args : int
        The maximum number of optional arguments each cventry/cvhonor can have.

    Returns
    -------
    list[list[str]]
        A list of lists, where each inner list contains the valid processed data.
    """
    clean_items = []

    for item in cv_items:
        optional_args = find_optional_args(item)

        # Verify the number of optional arguments
        if len(optional_args) > nr_optional_args:
            raise ValueError(
                f"Invalid cv item format: {item}. Expected at most " +
                f"{nr_optional_args} optional arguments."
            )

        # The last optional argument is always a boolean flag
        # indicating whether to include the item or not.
        if (len(optional_args) == nr_optional_args
                and optional_args[nr_optional_args-1].lower() == "true"):
            continue

        mandatory_args = find_mandatory_args(item)

        # Verify the number of mandatory arguments
        if len(mandatory_args) != nr_mandatory_args:
            raise ValueError(
                f"Invalid cv item format: {item}. Expected " +
                f"{nr_mandatory_args} mandatory arguments."
            )

        cleaned_data = []

        for datum in mandatory_args + optional_args:
            datum = unwrap_braces(datum)
            datum = tex_to_html(datum)

            if "\\item" in datum:
                datum = [
                    add_dot(unwrap_braces(item))
                    for item in datum.split("\\item")
                    if item.strip()
                ]

            cleaned_data.append(datum)

        clean_items.append(cleaned_data)

    return clean_items


def find_optional_args(entry: str) -> list[str]:
    """
    Find optional arguments in a cventry or cvhonor entry.

    Parameters
    ----------
    entry: str
        The entry string to process.

    Returns
    -------
    list[str]
        A list of optional arguments found in the entry.
    """
    optional_args = re.findall(r"\\cv[^\[]*((?:\[.*?\]\s*)+)", entry)

    if not optional_args:
        return []

    return re.findall(r"\[(.*?)\]", optional_args[0])


def find_mandatory_args(entry: str) -> list[str]:
    """
    Find mandatory arguments in a cventry or cvhonor entry.

    Parameters
    ----------
    entry: str
        The entry string to process.

    Returns
    -------
    list[str]
        A list of mandatory arguments found in the entry.
    """
    return parse_surrounded_text(entry, "{", "}")
