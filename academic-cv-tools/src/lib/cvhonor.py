import re

from lib.cvhelpers import clean_cv, clean_cv_items

nr_optional_args = 2
nr_mandatory_args = 4


def process_cvhonors(content: str | list[str]) -> list[list[str]]:
    """
    Process cvhonors from a string or a list of strings. Chonors
    are expected to be in the format:

        \cvhonor%
            [<skip>]%
            {<position>}{<title>}{<location>}{<date>}%

    Each cventry can have up to 2 optional arguments and must have
    4 mandatory arguments.

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

    cv_honors = re.findall(
        r"\\cvhonor[^\n]+(?=\n|$)", content)

    clean_honors = clean_cv_items(
        cv_honors, nr_mandatory_args, nr_optional_args)

    return clean_honors
