import re


def unwrap_braces(text: str) -> str:
    """Remove outer braces from a string if they exist."""
    text = text.strip()
    if text.startswith("{") and text.endswith("}"):
        text = text[1:-1]
        return unwrap_braces(text)  # Recursively unwrap
    return text.strip()


def tex_to_html(text: str) -> str:
    """Convert LaTeX text string to a HTML string."""
    text = re.sub(r"\\textbf\{(.*?)\}", r"<strong>\1</strong>", text)
    text = re.sub(r"\\textit\{(.*?)\}", r"<em>\1</em>", text)
    text = re.sub(r"\\texttt\{(.*?)\}", r"<code>\1</code>", text)
    text = re.sub(r"\\emph\{(.*?)\}", r"<em>\1</em>", text)
    text = re.sub(r"\\href\{(.*?)\}\{(.*?)\}", r"<a href='\1'>\2</a>", text)
    text = re.sub(r"\\&", r"&amp;", text)  # Escape ampersand
    text = re.sub(r"\\%", r"%", text)  # Escape percent sign
    text = re.sub(r"\\_", r"_", text)  # Escape underscore
    text = re.sub(r"\\textbackslash\s*", r"\\", text)  # Escape backslash
    text = re.sub(r"\-\-", "—", text)  # Escape backslash
    return text


def remove_comments(text: str | list[str]) -> str | list[str]:
    """Remove comments from a string or a list of strings."""
    comment_pattern = r"(?<!\\)%.*"
    if isinstance(text, str):
        return re.sub(comment_pattern, "", text)
    elif isinstance(text, list):
        return [re.sub(comment_pattern, "", line) for line in text]
    raise TypeError("Input must be a string or a list of strings.")


MONTHS = {
    "jan": "01", "feb": "02", "mar": "03", "apr": "04",
    "may": "05", "jun": "06", "jul": "07", "aug": "08",
    "sep": "09", "oct": "10", "nov": "11", "dec": "12"
}


def normalize_date(date: str) -> str:
    """Normalize date string like '[[1 ]Jan ]2023' to 'YYYY[-MM[-DD]]' format."""
    date = date.strip().lower()
    date_parts = date.split()
    if len(date_parts) == 1:
        # Single year: e.g., "2023"
        return date_parts[0].strip()
    elif len(date_parts) == 2:
        # Month and year: e.g., "Jan 2023"
        year = date_parts[1].strip()
        month = MONTHS.get(date_parts[0][:3], "01")
        return f"{year}-{month}"
    elif len(date_parts) == 3:
        # Day, month and year: e.g., "1 Jan 2023"
        year = date_parts[2].strip()
        month = MONTHS.get(date_parts[1][:3], "01")
        day = date_parts[0].strip()
        return f"{year}-{month}-{day}"
    raise ValueError(
        f"Invalid date format: {date}. Expected format: '[[1 ]Jan ]2023'")


def process_date_range(date_range: str) -> tuple[str, str]:
    """Process a date range string and return start and end dates."""
    date_range = date_range.strip()

    if date_range.count('—') == 1:
        # The date is in format '2023—24'
        start_date, end_date = [d.strip() for d in date_range.split('—')]

        if len(start_date) == 4 and len(end_date) == 2:
            end_date = int(start_date[:2] + end_date)
            start_date = int(start_date)

            if start_date > end_date:
                end_date += 100  # Adjust for century if needed

            return str(start_date), str(end_date)

        else:
            date_range = date_range.replace('—', '-')

    if '-' not in date_range:
        # If no end date is provided, use the start date as both
        start_date = normalize_date(date_range)
        return start_date, start_date

    elif date_range.count('-') == 1:
        start_date, end_date = [d.strip().lower()
                                for d in date_range.split('-')]
        if end_date in ["today", "present", "now", ""]:
            return normalize_date(start_date.strip()), None
        return normalize_date(start_date.strip()), normalize_date(end_date.strip())

    raise ValueError(
        f"Invalid date format: {date_range}. Expected formats: " +
        "'[[1 ]Jan ]2023 - [[1 ]Jan ]2024', '[[1 ]Jan ]2023', " +
        "'[[1 ]Jan ]2023 - [Present | Now | Today]', ], " +
        "2023—24'.")


def add_dot(text: str) -> str:
    """Add a dot at the end of the text if it doesn't already end with one."""
    text = text.strip()
    if not text.endswith("."):
        return text + "."
    return text


def shorten_word(word: str) -> str:
    """Shorten a word to its first letter followed by a dot.
    Word can start with a brace and this will be preserved."""
    new_word = ""
    if word.startswith("{"):
        new_word += "{"
        word = word[1:].strip()
    new_word += word[0] + "."
    if word.endswith("}"):
        new_word += "}"
    return new_word


def shorten_words(text: str) -> str:
    """Shorten words in the text to their first letter followed by a dot.
    Words are separated by spaces or dashes (-)."""
    words = text.split()
    shortened_words = []
    for word in words:
        if '-' in word:
            subwords = word.split('-')
            shortened_subwords = [shorten_word(sub) for sub in subwords]
            shortened_words.append('-'.join(shortened_subwords))
        else:
            shortened_words.append(shorten_word(word))
    return ' '.join(shortened_words).strip()


def process_name(name: str, verbose: bool = False) -> str:
    """
    Convert full name to initials.

    Parameters
    ----------
    name : str
        Full name to be processed.
    verbose : bool, optional
        If True, print debug information. Default is False.

    Returns
    -------
    str
        Processed name with initials.
    """
    name = name.strip()

    # Skip processing if name is wrapped in braces
    if name.startswith("{") and name.endswith("}"):
        if verbose:
            print(f"Name '{name}' is wrapped in braces. Returning as is.")
        return name

    # Split name by comma
    parts = name.split(',')

    # If the name is in format "Surname, Given Name", return it as "Surname, G. N."
    if len(parts) == 2:
        new_name = parts[0] + ", " + shorten_words(parts[1])
        return new_name

    # If the name is in format "Given Name Surname", return it as "Surname, G. N."
    elif len(parts) == 1:
        if verbose:
            print(f"Name '{name}' does not have a comma. " +
                  "Assuming it is in format 'Given Name Surname'.")

        # Split "Given Name Surname" into "Given" "Name" and "Surname"
        parts = parts[0].split()

        # If there's only one part, return it as is
        if len(parts) == 1:
            if verbose:
                print(f"Name '{name}' is only one word. " +
                      "Returning as is.")
            return parts[0]

        # If there are multiple parts, assume the last part is the surname
        surname = parts[-1]

        # If the surname is a single letter, warn the user
        # It is probably a mistake
        if len(surname) == 1:
            if verbose:
                print(f"Surname '{surname}' is a single letter. " +
                      "Please, check whether this is a mistake.")

        # Build the new name with surname and initials
        initials = shorten_words("".join(parts[:-1]))
        new_name = f"{surname}, {initials}"

        if verbose:
            print(f"Processed name '{name}' to '{new_name}'")
        return new_name

    # If the name has more than one comma, it is not in the expected format
    if verbose:
        print(f"Name '{name}' is not in the expected format. Returning as is.")
    return name


def parse_surrounded_text(text: str, op: str = "{", cl: str = "}") -> list[str]:
    """
    Parse text surrounded by specified open and close characters.

    Parameters
    ----------
    text : str
        The input text to parse.
    op : str, optional
        The opening character, by default "{".
    cl : str, optional
        The closing character, by default "}".

    Returns
    -------
    list[str]
        A list of strings found between the open and close characters.
    """

    # Find all occurrences of the opening and closing characters
    opening_chars = re.finditer(rf"{re.escape(op)}", text)
    closing_chars = re.finditer(rf"{re.escape(cl)}", text)

    # Store the indices and values of the opening and closing characters
    matches = [
        {"index": m.span()[0], "value": op} for m in opening_chars
    ] + [
        {"index": m.span()[0], "value": cl} for m in closing_chars
    ]

    # If no opening or closing characters are found, return an empty list
    if not matches:
        return []

    # Sort the list by index to maintain the order of characters
    matches.sort(key=lambda x: x["index"])

    # Extract indices and values from the sorted matches
    idxs = [item["index"] for item in matches]
    vals = [item["value"] for item in matches]

    # Assign a cumulative sum to each opening and closing character.
    # The sum represents the nesting level of the braces
    op_cumsum = []
    buffer = 0
    for char in vals:
        if char == op:
            buffer += 1
        elif char == cl:
            buffer = max(0, buffer - 1)
        op_cumsum.append(buffer)

    # Identify the external opening and closing characters.
    # External opening characters should have a cumulative sum of 1,
    # and external closing characters should have a cumulative sum
    # of 0.
    i = 0
    openclose = 0
    done = False
    ranges = []
    while not done:
        if openclose == 1:
            if 0 not in op_cumsum[i:]:
                done = True
            else:
                i_close = op_cumsum[i:].index(0) + i
                openclose = 0
                ranges.append((idxs[i], idxs[i_close]))
                i = i_close
        elif openclose == 0:
            if 1 not in op_cumsum[i:]:
                done = True
            else:
                i_open = op_cumsum[i:].index(1) + i
                openclose = 1
                i = i_open

    # If no ranges were found, return an empty list
    if not ranges:
        return []

    # Extract the text between the ranges
    return [text[start+1:end] for start, end in ranges]
