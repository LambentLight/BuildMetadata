# The libraries that we need for parsing the page
import json
import os
import re
import sys

import lxml.html

# For more information, see https://regexr.com/4nl34
REGEX = "\\.\\/([0-9]{3,4}-[0-9a-z]{40})\\/(server\\.zip|fx\\.tar\\.xz)"


def main():
    """
    The function that parses the FiveM page into
    JSON that LambentLight/ServerManager can read.
    """
    # If the number of argument is not three
    if len(sys.argv) != 3:
        print(f"Wrong number of arguments. Expected 3, got {len(sys.argv)}")
        sys.exit(2)

    # First we need to check that the file with the HTML exists
    if not os.path.isfile(sys.argv[1]):
        # Print a message and exit with a code 2
        print("The file with the builds does not exists!")
        sys.exit(3)

    # Load the contents into the lxml parser
    html = lxml.html.parse(sys.argv[1])
    # Get the a nodes
    a_nodes = html.xpath("//a[@class='panel-block ']")

    # Create a list for storing our builds
    builds = []

    # For each a node that we have
    for node in a_nodes:
        # Try to search the respective regex on the href
        regex = re.search(REGEX, node.attrib.get("href", ""))

        # If the regex was able to find the group
        if regex is not None and regex.group(1):
            # Add the item into our list
            builds.append(regex.group(1))

    # Open a file for writing the builds
    with open(sys.argv[2], "w") as output:
        # Dump the list of builds
        json.dump(builds, output, indent=4)
        # And finally and a line at the end
        output.write("\n")


# If we are running the script as standalone (aka no importing)
if __name__ == "__main__":
    main()
