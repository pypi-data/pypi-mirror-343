# x4util

This repository contains a version controlled and packaged version of the NRDC [forexy](https://pypi.org/project/forexy/) script collection, previously also released also via the NRDC as _[x4util code](https://nds.iaea.org/nrdc/nrdc_sft/)_ and supplementary codes.

The main advantage of x4util is

- the systematic version control via the [source repository](https://git.oecd-nea.org/exfor/tools/x4util), which is automatically patched with forexy changes
- the implementation of a (so far minimal) test suite
- the wrapping of the scripts into an python package while still exposing command line scripts

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

### ... latest release

```console
pip install x4util
```

### ... development version

this requires python, pip and git to be installed on the system

```console
pip install git+https://git.oecd-nea.org/exfor/tools/x4util.git
```

## Contribute

To contribute to the project, clone the repository, implement changes and propose to include them via a Merge Request.
Test are managed using hatch. To run test locally use `hatch test`.

## License

`x4util` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

## Developer notes

This package is developed and managed using [hatch](https://hatch.pypa.io/latest).

Releases are managed by gitlab pipelines triggered by version tags. To include a commit in the changelog of a release use the `Changelog: <added/changed/removed>` [pattern as commit trailer](https://about.gitlab.com/blog/2023/11/01/tutorial-automated-release-and-release-notes-with-gitlab/).
