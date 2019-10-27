# bumpit
A small command line tool to bump tracked versions in your repository.

It is designed to integrate well with your CI/CD pipeline. Simply install and run `bumpit` as part of your pipeline. Let the robots do the boring work!

# Installation
You can download and install `bumpit` from PyPI by running:

```
pip install bumpit
```

# Usage

At a high level, you need to
1. setup the configuration file `.bumpconfig.yaml` in your target folder.
2. run `bumpit`.
3. and when you are ready, push the changes to your `remote`
    ```shell
    git push origin master --tags
    ```

## Usage
```shell
Usage: bumpit [OPTIONS]

Options:
  -d, --dry-run      Run the tool in dry run mode
  -c, --config TEXT  Configuration settings
  --help             Show this message and exit.
```

## Configuration
`bumpit` relies heavily on a configuration file capture all runtime context of `bumpit`. This config file is named `.bumpconfig.yaml` by default. You can override this using the `--config` option in the command line.

The config file looks like:

```yaml
current_version: "0.0.1"
strategy: "semver-patch"
tag: True
tag_format: "{version}"
tracked_files:
- setup.py
```

where:
* `current_version` - the current version of your files. It needs to be wrapped in quotes to force parsing to be string (e.g. avoid calver current_version to be parsed as float)
* strategy - supported values `semver-major`, `semver-minor`, `semver-patch`, `calver`
* `tag` - bool value to instruct the tool to tag the repository after the version update
* `tag_format` - format of the tag. Some people prefer to add prefix to their tag versions (e.g. `release/1.0.1`). As long as the `{version}` is present, then it is a valid `tag_format`
* tracked_files - a list of relative filenames to update version to. If the current_version is not found, the tool simply skips this file

# Examples
Check out the following repositories for examples:
* [CalVer](https://github.com/mobiusbyte/bumpit-calver-fixtures) example
* [SemVer](https://github.com/mobiusbyte/bumpit-semver-fixtures) example
* [bumpit](https://github.com/mobiusbyte/bumpit/blob/master/.bumpit.yaml) - yep! `bumpit` uses `bumpit`.

# Version Strategies
The tool currently supports the following versioning strategies
* [Semantic Version](https://semver.org/)
* [Calendar Version](https://calver.org/)

## Semantic Version
`buildit` implements a very basic semver scheme. It validates the right format using the [proposed format](https://semver.org/#is-there-a-suggested-regular-expression-regex-to-check-a-semver-string).

Notice that semantic version has optional `meta` tokens after the usual `major.minor.patch` tokens. When `meta` token is present and `bumpit` runs, `bumpit` naively updates the `major.minor.patch` version based on the strategy and leave the `meta` token as is. If this is not your expected behaviour, please help me understand how it should be handled. You can create an issue and perhaps a PR of your proposed solution.

## Calendar Version
`buildit` implements a very basic calver scheme. It assumes that the version follows the format `YYYYmm.variant` where
* `YYYY` - year
* `mm` - month zero padded
* `variant` - incrementing integer to distinguish different version for the same month

When the month rolls over to the next, `YYYYmm` will be the new month, and `variant` resets to `1`.

The format is quite concrete. This was sufficient enough for my use case. However, if you feel that this is too simplistic, please feel free to create an issue and perhaps a PR of your proposed solution.


# Development
## Contribution
Code and documentation improvements are all welcome. You can also file bug reports or feature suggestions.

The feature set is meant to handle different versioning strategies. Currently, the strategies I know are applied in the wilds are implemented, but it is by no means complete!

## Publishing
To publish `bumpit`, run the following

```shell
git checkout master
git pull
bumpit
git push origin master --tags
python setup.py bdist_wheel sdist
twine upload dist/*
```


# License
`bumpit` is released under the [MIT License](https://opensource.org/licenses/MIT).

