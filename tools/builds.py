# The libraries that we need for parsing the page
import json
import lxml.html
import os
import sys


def main():
    """
    The function that parses the FiveM page into
    JSON that LambentLight/ServerManager can read.
    """
    # If the number of argument is not three
    if len(sys.argv) != 3:
        print("Wrong number of arguments. Expected 3, got " + len(sys.argv))
        sys.exit(2)

    # First we need to check that the file with the HTML exists
    if not os.path.isfile(sys.argv[1]):
        # Print a message and exit with a code 2
        print("The file with the builds does not exists!")
        sys.exit(3)

    # Load the contents into the lxml parser
    html = lxml.html.parse(sys.argv[1])
    # Get the a nodes
    a_nodes = html.xpath("//a")

    # Create a list for storing our builds
    builds = []

    # For each a node that we have
    for node in a_nodes:
        # If it has a title attribute and is not "revoked"
        if "title" in node.attrib and node.attrib["title"] != "revoked":
            # Add the item into our list
            builds.append(node.attrib["title"])

    # Open a file for writing the builds
    with open(sys.argv[2], "w") as output:
        # Dump the list of builds
        json.dump(builds, output, indent=4)
        # And finally and a line at the end
        output.write("\n")


# If we are running the script as standalone (aka no importing)
if __name__ == "__main__":
    main()
