from .builds import generate_builds


def main():
    """
    Runs all of the Metadata generation logic.
    """
    # Generate the list of builds
    generate_builds()


if __name__ == "__main__":
    main()
