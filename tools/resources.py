import glob
import json

from .github import get_releases


def update_versions():
    """
    Generates the list.json file with the names of the resources.
    """
    # Iterate over the files in the metadata folder
    for file in get_files():
        # Open it up and load the contents
        with open(file, "r+") as opened:
            # Get the information of the resource
            data = json.load(opened)

            # If the file uses GitHub Releases for the updates
            if data["update"]["type"] == 1:
                # Request the list of releases to GitHub and save them
                data["versions"] = get_releases(*data["update"]["parameters"])

            # Seek back to the start of the file
            opened.seek(0)
            # And dump the new file contents
            json.dump(data, opened, indent=4)
            # And finally add a new line at the end
            opened.write("\n")


def get_files():
    """
    Gets a file iterator for the resources/metadata directory.
    """
    return glob.iglob("resources/metadata/*.json")
