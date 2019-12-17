# The libraries that we need for parsing the page
import json
import re

import lxml.html
import requests

# For more information, see https://regexr.com/4nl34
REGEX = "\\.\\/([0-9]{3,4}-[0-9a-z]{40})\\/(server\\.zip|fx\\.tar\\.xz)"


def generate_builds():
    """
    Downloads and Parses the FiveM and RedM builds into JSON lists.
    """
    # Make the web request for the URL
    req = requests.get("https://runtime.fivem.net/artifacts/fivem/build_server_windows/master/")
    # If we got a non 200, continue to the next iteration
    if req.status_code != 200:
        print(f"Got code {req.status_code} while updating builds!")
        return

    # Try to get the parsed list of builds
    builds = parse_builds(req.text)
    # Then, open a file with the correct name
    with open("builds.json", "w") as file:
        # Dump the list as a JSON
        json.dump(builds, file, indent=4)
        # And write a new line at the end
        file.write("\n")


def parse_builds(text):
    """
    Gets the list of builds from the HTML page in a string.
    """
    # Load the contents into the lxml parser
    html = lxml.html.fromstring(text)
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

    # Finally, return the list of builds
    return builds
