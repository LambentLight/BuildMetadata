import sys

from .builds import generate_builds


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

    # IF the mode is set to all or builds, generate the list of builds
    if mode == "all" or mode == "builds":
        generate_builds()


if __name__ == "__main__":
    main()
