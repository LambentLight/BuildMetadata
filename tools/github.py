import requests

DL_ZIPBALL = "https://github.com/{0}/{1}/archive/{2}.zip"
API_RELEASES = "https://api.github.com/repos/{0}/{1}/releases"


def get_releases(owner, repo, skip=[], zip_only=False):
    """
    Gets a list of releases from a GitHub Repository.
    """
    # Create a place for storing the releases
    releases = []
    # Make the GET request
    get = requests.get(API_RELEASES.format(owner, repo))

    # If the request is not 200, return the empty list
    if get.status_code != 200:
        return releases

    # If is 200, iterate over the releases
    for release in get.json():
        # If this tag is on the excluded list, skip this iteration
        if release["tag_name"] in skip:
            continue

        # If assets is empty or this resource requires the zip, set it as the file
        if not release["assets"] or zip_only:
            download = DL_ZIPBALL.format(owner, repo, release["tag_name"])
        # If there is a released file, save the first one it
        else:
            download = release["assets"][0]["browser_download_url"]

        # Then, get the version of the release with the v stripped
        version = release["tag_name"].strip("v")

        # And add the release onto the list
        releases.append({"version": version, "download": download})

    # Finally, return the new list of releases
    return releases
