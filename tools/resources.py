import glob
import json

from .github import get_commits, get_releases


def update_list():
    """
    Updates the basic list of Resources (list.json) from the extended metadata.
    """
    # Create a list to store the metadata temporarily
    resources = []

    # Iterate over the files in the metadata folder
    for file in get_files():
        # Open it up and load the contents
        with open(file, "r+") as opened:
            # Get the information of the resource
            data = json.load(opened)
            # And append the basic information
            resources.append(data["info"])

    # Then, open the list of resources and extract them
    with open("resources/list.json", "w") as opened:
        # Dump the contents of the list
        json.dump(resources, opened, indent=4)
        # And write a new line at the end
        opened.write("\n")


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

            # Create some shortcuts for the objects
            params = data["update"].get("parameters", {})

            # If the file uses GitHub Releases for the updates
            if data["update"]["type"] == 1:
                # Create a new list of versions
                data["versions"] = []

                # If we need to fetch a specific number of commits
                if "commits" in params:
                    # Add those versions from the commits
                    data["versions"].extend(get_commits(**params))

                # If we don't have the update from releases disabled
                if not ("skip_releases" in params and params["skip_releases"]):
                    # Request the list of releases to GitHub and save them
                    data["versions"] = get_releases(**params)

            # Remove everything and go back to the start of the file
            opened.seek(0)
            opened.truncate()
            # And dump the new file contents
            json.dump(data, opened, indent=4)
            # And finally add a new line at the end
            opened.write("\n")


def get_files():
    """
    Gets a file iterator for the resources/metadata directory.
    """
    return glob.iglob("resources/metadata/*.json")
