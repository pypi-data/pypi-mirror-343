"""
.. module:: find_obj
    :platform: Unix, Windows
    :synopsis: Find file object
"""

# Python Standard Libraries
import logging
import os

# 3rd Party Libraries


# Project Specific Libraries


LOGGER = logging.getLogger(__name__)


def find(path: str, file_name: str, search_dirs: int = 4) -> str:
    """Find a file by traversing the parent

    Args:
        file_path (str): Starting path

        file_name (str): Name of file to find

        search_dirs (int, Optional): Number of parent directories to traverse,
        defaults to 4

    Returns:
        str: Path of file found, None if file is not found
    """
    LOGGER.debug(
        "Searching for %(file_name)s in %(path)s",
        {"file_name": file_name, "path": path},
    )

    file_path = path

    for _ in range(0, search_dirs):
        if os.path.exists(os.path.join(file_path, file_name)):
            return file_path

        file_path = os.path.join(file_path, "..")

    LOGGER.info(
        "%(file_name)s not found within %(search_dirs)s directories of "
        "%(path)s",
        {"file_name": file_name, "path": path, "search_dirs": search_dirs},
    )

    return None


def check(path: str, file_name: str) -> bool:
    """Function to check if a file exists

    Args:
        path (str): Directory path of the file to load

        file_name (str): Name of the file (with extension)

    Returns:
        bool: True/False if file exists
    """
    path = os.path.expanduser(path)

    if os.path.isfile(os.path.join(path, file_name)):
        return True

    LOGGER.warning(
        "File does not exist at %(path)s/%(file_name)s",
        {"file_name": file_name, "path": path},
    )
    return False
