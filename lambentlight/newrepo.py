import json
import logging
import os

LOGGER = logging.getLogger("lambentlight")


def create_new_repo():
    """
    Creates a new repository on the current working directory.
    """
    # Create all of the resources directory
    create_dir("resources")
    create_dir("resources/common")
    create_dir("resources/gtav")
    create_dir("resources/rdr2")
    dump_to_file("builds.json", [])
    dump_to_file("resources/common.json", [])
    dump_to_file("resources/gtav.json", [])
    dump_to_file("resources/rdr2.json", [])


def create_dir(directory: str):
    """
    Creates a directory and logs what happened.
    """
    # If the directory does not exists, create it and log it
    if not os.path.isdir(directory):
        os.mkdir(directory)
        LOGGER.info(f"{directory} has been created")
    # Otherwise, log that it already exists
    else:
        LOGGER.info(f"{directory} already exists")


def dump_to_file(file: str, contents: object):
    """
    Dumps the specified dictionary into the file.
    """
    # With the file opened, dump the object
    with open(file, "w") as opened:
        json.dump(contents, opened)
