"""
.. module:: hsh
    :platform: Unix, Windows
    :synopsis: Hash data or file contents
"""

# Python Standard Libraries
import hashlib
import json
import logging
import os
import uuid


# 3rd Party Libraries


# Code Repository Sub-Packages


LOGGER = logging.getLogger(__name__)

BLOCKSIZE = 65536


def hash_content(source: object) -> str:
    """Hash content (file, data, directory)

    Args:
        source (object): Source of data to hash

    Returns:
        str: String of the hash in uuid format
    """
    # TODO Check if file is an archive file SPIN-20
    # TODO Hash directory content SPIN-19
    if isinstance(source, (dict, list)):
        return hash_string(json.dumps(source, default=str))

    if isinstance(source, (str, bytes)):
        return hash_string(source)

    raise NotImplementedError(f"Hashing for {type(source)} Not Supported")


def hash_file(path: str) -> str:
    """Hash a files content

    Args:
        path (str): String of the path to hash

    Returns:
        str: String of the hash in uuid format
    """
    hasher = hashlib.md5()  # nosec

    path = os.path.expanduser(path)

    with open(path, "rb") as file_obj:
        buf = file_obj.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = file_obj.read(BLOCKSIZE)

    return str(uuid.UUID(hasher.hexdigest()))


def hash_string(content: str) -> str:
    """Hash string of data

    Args:
        content(str): String of the content to hash

    Returns:
        str: String of the hash in uuid format
    """
    hasher = hashlib.md5()  # nosec

    if not isinstance(content, bytes):
        hasher.update(content.encode())
    else:
        hasher.update(content)

    return str(uuid.UUID(hasher.hexdigest()))
