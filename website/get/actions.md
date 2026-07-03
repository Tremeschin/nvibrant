---
title: Workflow Builds
icon: octicons/workflow-16
description: Download nvibrant python wheels from GitHub Actions releases, or optionally
  extract the pre-compiled C++ binaries for running them manually.
tags:
- Install
- Prebuilt
- Binaries
---

!!! success "This is an official release channel for nvibrant"

You can download all builds made by GitHub Actions in the repository [releases](https://github.com/Tremeschin/nvibrant/releases) page, which are uploaded via Trusted Publishing to PyPI, and uses Immutable Releases.

## Python utility

The only dependency is [`pypi/packaging`](https://pypi.org/project/packaging/) for semver comparisons, run directly with:

```sh linenums="1"
uvx --with nvibrant-1.2.0-py3-none-manylinux_2_17_x86_64.whl nvibrant (...)
```

And/or install into a venv with standard pip or uv, same usage as [Python Registry](pypi.md) install.

## Extracting binaries

Since Python [wheels are zips](https://packaging.python.org/en/latest/specifications/binary-distribution-format/), you can glob or selectively unzip files from it:

```sh
# Extracts all nvibrant-$driver binaries into ./bin/
unzip -j "nvibrant-*.whl" "nvibrant/resources/*" -d ./bin
chmod +x "./bin/*"
```

And then copy somewhere else (like `~/.local/bin`) or run files directly:

```sh
./bin/nvibrant-575.64.03 (args)
```

<small><b>Note:</b> Always chose the closest, but not newer driver version file!</small>
