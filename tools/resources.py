import glob
import json
from os.path import isfile

from .github import get_commits, get_releases
from .parsing import ensure_input, parse_bool, parse_game, parse_int


def update_lists():
    """
    Updates the resource list of Red Dead Redemption 2 and Grand Theft Auto V.
    """
    update_list("gtav")
    update_list("rdr2")


def update_list(game):
    """
    Updates the basic list of Resources (list.json) from the extended metadata.
    """
    # Create a list to store the metadata temporarily
    resources = []

    # Iterate over the files in the metadata folder
    for file in get_files(game):
        # Open it up and load the contents
        with open(file, "r+") as opened:
            # Get the information of the resource
            data = json.load(opened)
            # And append the basic information
            resources.append(data["info"])

    # Then, open the list of resources and extract them
    with open(f"resources\\{game}.json", "w") as opened:
        # Dump the contents of the list
        json.dump(resources, opened, indent=4)
        # And write a new line at the end
        opened.write("\n")


def update_version(file):
    """
    Updates the selected versions from the file.
    """
    # If the file does not exists, notify the user and return
    if not isfile(file):
        print(f"The file {file} does not exists!")
        return

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


def update_versions():
    """
    Generates the list.json file with the names of the resources.
    """
    # Iterate over the files in the metadata folder
    for file in get_files("gtav"):
        # And update every single one of them
        update_version(file)
    # Repeat the same for the other folder
    for file in get_files("rdr2"):
        update_version(file)


def create_new():
    """
    Creates a new resource file step by step.
    """
    # Ask the user for basic input
    game = parse_game(ensure_input("With what game does this resource works? [gtav,rdr2] > "))
    name = ensure_input("What is the name of the resource? [] > ")
    author = ensure_input("Who is the author of the resource? [] > ")
    destination = ensure_input("What is the destination folder of the resource? [] > ")
    requires = ensure_input("What other resources does this one requires? (separate them with comas) [] > ", "")
    update = parse_bool(ensure_input("Should this resource be updated automatically via GitHub? [y/n] > ", False))

    # Create the new object with the data
    data = {
        "info": {
            "name": name,
            "author": author
        },
        "update": {
            "type": 0,
        },
        "install": {
            "destination": destination
        },
        "requires": [],
        "versions": []
    }

    # If there are requirements to be parsed
    if requires:
        data["requires"] = requires.split(",")

    # If the user wants to use GitHub for updating
    if update:
        # Ask the information that we need
        owner = ensure_input("Who is the owner of the GitHub repository? [] > ")
        repo = ensure_input("What is the name of the GitHub repository? [] > ")
        releases = parse_bool(ensure_input("Should GitHub Releases be included? [y/n] > ", True))
        commits = parse_int(ensure_input("How many commits should be included? (zero to disable) [0] > "), 0)
        path = ensure_input("What is the path of the resource folder inside of the compressed file? [] > ", "")

        # And add those values
        data["update"] = {
            "type": 1,
            "parameters": {
                "owner": owner,
                "repo": repo,
                "patches": {
                    "*": {
                        "path": path
                    }
                }
            }
        }

        # If the user doesn't want releases
        if not releases:
            data["update"]["parameters"]["skip_releases"] = True
        # If the user wants commits to be included
        if commits:
            data["update"]["parameters"]["commits"] = commits

    # If there are no requirements to add, remove the item
    if not data["requires"]:
        del data["requires"]

    # Create the destination path of the file
    file_path = f"resources\\{game}\\{name}.json"
    # Open the file for writing
    with open(file_path, "w") as opened:
        # Dump the new resource information
        json.dump(data, opened, indent=4)
        # And add a new line
        opened.write("\n")

    # If there is a way to update the versions
    if data["update"]["type"]:
        # Ask the user if he wants to refresh the versions right now
        after = parse_bool(ensure_input("Do you want to refresh the versions after finishing? [y/n] > ", True))

        # If he does, just call the respective function
        if after:
            update_version(file_path)

    # Finally, update the list of resources to add the new one
    update_list(game)


def get_files(game):
    """
    Gets a file iterator for the resources/metadata directory.
    """
    return glob.iglob(f"resources\\{game}\\*.json")
