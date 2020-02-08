import os
import sys

from .builds import generate_builds
from .newrepo import create_new_repo
from .parsing import parse_game, ensure_input, COMMON
from .resources import update_lists, update_version, create_new, update_versions


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
    if mode == "newrepo":
        create_new_repo()
    if mode == "all" or mode == "builds":
        generate_builds()
    if mode == "all" or mode == "versions":
        if "GITHUB_TOKEN" not in os.environ:
            sys.exit("A GitHub Token is required for updating all of the versions at the same time..")
        update_versions()
    if mode == "all" or mode == "versionmanual":
        game = parse_game(ensure_input("Name of the game that you want to update (gtav, rdr2, common) > ", COMMON[0]))
        name = ensure_input("Name of the file that you want to update > ")
        update_version(f"resources/{game}/{name}")
    if mode == "all" or mode == "new":
        create_new()
    if mode == "all" or mode == "list":
        update_lists()


if __name__ == "__main__":
    main()
