import os


def root_dir() -> str:
    """
    Return the absolute path to the root academic cv tools
    project directory, which is the parent of the current 
    directory file.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))


def input_dir() -> str:
    """
    Return the full path to the input directory of the 
    academic cv tools project.
    """
    return root_dir() + "/input"


def output_dir() -> str:
    """
    Return the full path to the output directory of the
    academic cv tools project.
    """
    return root_dir() + "/output"
