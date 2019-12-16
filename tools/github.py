import requests
from packaging.specifiers import SpecifierSet, InvalidSpecifier
from packaging.version import Version, InvalidVersion

DL_ZIPBALL = "https://github.com/{0}/{1}/archive/{2}.zip"
API_RELEASES = "https://api.github.com/repos/{0}/{1}/releases"
COMMIT_RELEASES = "https://api.github.com/repos/{0}/{1}/commits"


def get_commits(**kwargs):
    """
    Gets the specified number of commits from a GitHub repository.
    """
    # Get the parts that we need
    owner = kwargs.get("owner")
    repo = kwargs.get("repo")
    count = kwargs.get("commits")
    patch = kwargs.get("patches")["*"]

    # Create a place for storing the releases
    releases = []
    # Make the GET request
    get = requests.get(COMMIT_RELEASES.format(owner, repo))

    # If the request is not 200, return the empty list
    if get.status_code != 200:
        return releases

    # If is 200, iterate over the commits
    for commit in get.json():
        # Create the object with the information
        data = {
            "version": "{0} ({1})".format(commit["sha"], commit["commit"]["message"]),
            "download": DL_ZIPBALL.format(owner, repo, commit["sha"]),
            "path": patch["path"].format(commit["sha"])
        }
        # And add the new version into the list
        releases.append(data)

    # Finally, return the list with the releases
    return releases


def get_releases(**kwargs):
    """
    Gets a list of releases from a GitHub Repository.
    """
    # Get the parts that we need
    owner = kwargs.get("owner")
    repo = kwargs.get("repo")
    patches = kwargs.get("patches", {})
    skip = kwargs.get("skip", [])

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

        # Create a temporary set of patches
        patch = {}
        # Try to parse the version on the tag without the trailing V
        try:
            version = Version(release["tag_name"].strip("v"))
        except InvalidVersion:
            version = None

        # Select the correct set of manual patches
        for key, item in patches.items():
            # Try to parse the specifier
            try:
                specifier = SpecifierSet(key)
            except InvalidSpecifier:
                specifier = None

            # If the specifier and version are valids and the later is compatible with the specifier
            if specifier and version and version in specifier:
                patch = item
                break

        # If there is no patches set, let's use the generic set of patches if is available
        if not patch and "*" in patches:
            patch = patches["*"]

        # If assets is empty or this resource requires the zip, set it as the file
        if not release["assets"] or ("zip_only" in patch and patch["zip_only"]):
            download = DL_ZIPBALL.format(owner, repo, release["tag_name"])
        # If there is a released file, save the first one it
        else:
            download = release["assets"][0]["browser_download_url"]

        # Create the object with the version information
        data = {
            "version": release["tag_name"].strip("v"),
            "download": download
        }
        # If there is a path to format, use it
        if "path" in patch:
            data["path"] = patch["path"].format(data["version"])

        # And add the release onto the list
        releases.append(data)

    # Finally, return the new list of releases
    return releases
