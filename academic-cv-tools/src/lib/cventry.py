import re

from lib.cvhelpers import clean_cv, clean_cv_items

nr_optional_args = 4
nr_mandatory_args = 5


def process_cventries(content: str | list[str]) -> list[list[str]]:
    """
    Process cventries from a string or a list of strings. Cventries
    are expected to be in the format:

        \cventry%
            [<logo>][<image>][<url>][<skip>]%
            {<position>}{<title>}{<location>}{<date>}{<description>}%

    Each cventry can have up to 4 optional arguments and must have
    5 mandatory arguments.

    Parameters
    ----------
    content : str | list[str]
        The content to process, either as a single string or a list of strings.

    Returns
    -------
    list[list[str]]
        A list of lists, where each inner list contains the valid processed data.
    """
    content = clean_cv(content)  # Clean the content before processing

    cv_entries = re.findall(
        r"\\cventry[^\n]+(?=\n|$)", content)

    clean_entries = clean_cv_items(
        cv_entries, nr_mandatory_args, nr_optional_args)

    return clean_entries
