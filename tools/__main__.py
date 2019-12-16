import sys

from .builds import generate_builds
from .resources import update_list, update_version, update_versions


def main():
    """
    Runs all of the Metadata generation logic.
    """
    # If the number of arguments is lower than two (script name + mode)
    if len(sys.argv) < 2:
        # Set the mode to all
        mode = "all"
    # Otherwise
    else:
        # Set the mode to the one specified by the user
        mode = sys.argv[1]

    # Now, run the correct function for the selected mode
    if mode == "all" or mode == "builds":
        generate_builds()
    if mode == "all" or mode == "versions":
        update_versions()
    if mode == "all" or mode == "versionmanual":
        name = input("Name of the file that you want to update > ")
        update_version(f"resources/metadata/{name}")
    if mode == "all" or mode == "list":
        update_list()


if __name__ == "__main__":
    main()
