"""Utility functions for Dora."""

import logging
from typing import Iterator, Tuple
from os import environ, walk, path

def logger(name: str = None, fmt: str = None) -> logging.Logger:
    """Create logger
    :param name: Log name. Use the module name. Default is '__name__'
    :param fmt: Log format. See https://docs.python.org/3/library/logging.html#logrecord-attributes
    :return: Logger
    """
    if fmt is None:
        fmt = "%(levelname)s:%(name)s:%(funcName)s:%(message)s"
    logging.basicConfig(format=fmt)
    if name is None:
        name = __name__
    log = logging.getLogger(name)
    log.setLevel(getattr(logging, environ.get('LOG_LEVEL', 'DEBUG')))
    return log

def find_files(directory: str, file_type:str='sql') -> Iterator[Tuple[str, str]]:
    """
    Finds all `.sql` files in a directory, including subdirectories.

    Args:
        directory (str): The directory to search for files.
        file_type (str): The file extension to search for. Defaults to `sql`.

    Returns:
        list: A list of full paths to `.sql` files.
    """
    for root, _, files in walk(directory):
        for file in files:
            if file.endswith(f".{file_type}"):
                _dir = path.relpath(root, directory)
                if _dir == '.':
                    _dir = ''
                yield (path.join(_dir, file), file.split('.',maxsplit=1)[0])
