# Build and Resource Metadata

This is a repository that contains the list of FiveM builds and installable resources for LambentLight.

# Guidelines

## Builds

To update the list of FiveM builds, follow this steps:

1. Install Python 3.5 or higher and lxml (use `python -m pip install lxml`)
2. Go to https://runtime.fivem.net/artifacts/fivem/build_server_windows/master/ for Windows or https://runtime.fivem.net/artifacts/fivem/build_proot_linux/master/ for Linux and complete the captcha
3. Save the page from your browser as `windows.html` for Windows or `linux.html` for Linux on the root of this repository
4. Open a Terminal from the root of the repo and run `convert.bat`
5. `builds.json` and `builds.linux.json` should now be updated and ready to be commited or used

## Resources

To add new resources, first make sure that:

* Is being used (sending your new resources to promote them is a no-no)
  * Please corroborate this with a GitHub repo, FiveM thread or 5mods page
* Is able to run without random crashes (in other words, the resource can have bugs but is useable)
* Is public (no "Join my Discord/Patreon type of downloads")
* Is either a script, gamemode or loading screen
  * Please note that we do not allow cars, maps or textures
  * If you belive that we should accept a specific mod that is not allowed, open an issue and we can discuss it

Once the resource complies with the already mentioned prerequisites, do the following to add it into the list:

1. Pick either a Resource per Commit or Resource per Pull Request
2. Add a new object **at the top** of `resources.json` with the resource information
3. Wait for the team to aprove the new Resource(s)

# JSON formats

Every resource and version object has a specific format that you need to follow.

## Resource

* `name`: The readable name (please do not use initials like ELS unless required)
* `author`: Name(s) of the authors or developers
* `folder`: The desired destination folder of the resource
* `path`: The path of the resource inside of the compressed file
  * If this and the version path is present, the version path takes presedence
* `type`: Type of resource, where:
  * 0 is script
  * 1 is gamemode
  * 2 is loading screen
* `license`: The URL of the resource License
* `requires`: A list of resource names that this one depends to
* `instructions`: If the resource requires aditional configuration, a web page that shows the user how to configure it
* `versions`: An array of resource version objects

## Version

* `version`: The version (2.5.1) or Git SHA hash (008e46b420c44b0c62cb9375f7883f445c4d2592)
* `download`: The download URL for the version
* `path`: The path of the resource inside of the compressed file
  * If this and the version path is present, the version path takes presedence
* `compression`: The compression type of the resource, where:
  * 0 is Zip
  * 1 is 7zip
  * 2 is Rar/WinRAR
