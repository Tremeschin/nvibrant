---
title: Changelog
icon: material/file-document-edit
description: Changelog page for the nvibrant project. Detailed history of software
  updates, feature improvements, infrastructure changes, and driver support milestones.
tags:
- About
- Changelog
- Versions
---

!!! success "This project is complete and stable, no actions are needed unless a driver update breaks it!"
    - Don't panic when it breaks, follow this [FAQ](./help.md#new-drivers) section for a workaround and asking a patch release.

### :package: v1.3.0 <small>Staging</small> {#v1.3.0}

!!! quote ""
    - Support setting the [Dithering Mode](./docs/dithering.md#mode) requested in [#18 (comment)](https://github.com/Tremeschin/nvibrant/issues/18#issuecomment-4654683807)
    - Support setting the [Dithering Depth](./docs/dithering.md#depth) requested in [#18 (comment)](https://github.com/Tremeschin/nvibrant/issues/18#issuecomment-4654683807)
    - Simplify website path `/about/changelog` to just `/changelog`
    - Change project license from GPL-3.0 to MIT[^mit]

[^mit]: I had chosen GPL in a hurry and by habit. Spiritually, nvibrant should be a small, simple project. :slight_smile:

### :package: v1.2.1 <small>May 28, 2026</small> {#v1.2.1}

!!! quote ""
    - Port readme contents into a website made with [Zensical](https://zensical.org/docs/get-started/)
    - Update GitHub Actions workflow to `ubuntu-24.04` for newer GCC versions [#37](https://github.com/Tremeschin/nvibrant/issues/37)
    - Update prebuilt binaries up to driver v610.43.02 (breaking changes) [#39](https://github.com/Tremeschin/nvibrant/issues/39)

### :package: v1.2.0 <small>Mar 06, 2026</small> {#v1.2.0}

!!! quote ""
    Maintenance release, support newer drivers, major packaging changes.

    After learning a few tricks writing [rustbin](https://github.com/BrokenSource/Rustbin), I'm backtracking into fixing some less than ideal decisions and designs in nvibrant - most notably using [`TemporaryDirectory`](https://docs.python.org/3/library/tempfile.html#tempfile.TemporaryDirectory) for compiling the meson project, including artifacts via hatchling [build hooks](https://hatch.pypa.io/latest/plugins/build-hook/reference/), and properly [tagging wheels](https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/) instead of using `py3-none-any` (which is wrong, binaries are for specific os+arch targets).

    **Changes**:

    - Update prebuilt binaries up to driver v595.45.04 (breaking changes)
    - Python runtime code is now minimal and doesn't include building infrastructure.
    - Add this `changelog.md` file and reference it on all past releases.
    - Enable [Immutable Releases](https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/) in the GitHub repository.

    **Breaking**:

    - Wheels are now [tagged](https://packaging.python.org/en/latest/specifications/platform-compatibility-tags/) for each platform, eg. `nvibrant-1.2.0-py3-none-manylinux_2_17_x86_64.whl`
        - After much thought, **yanking** all previous releases on PyPI is the best course of action, to prevent unsupported platforms from accidentally installing a wrong `py3-none-any` wheel. Users who use pinned versions will notice no changes, as it overrides yanks. _There are **no issues** with older versions_ and you can keep using them normally, pardon my mistakes.
        - Rename internal binaries from `nvibrant-linux-amd64-590-48-01-v1.1.0.bin` to `nvibrant-590.48.01`, as wheels contain version information, and package managers should vendor drivers separately.
    - Stop providing standalone `.tar.gz` releases, as [`.whl` are Zips](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) and can extract `/nvibrant/resources/*`
    - Downgrade the build script into regular build hook, always making a wheel for the current host (a step towards sdists). Should be buildable in Linux ARM now, feedback welcome.

    <small><b>Note</b> that source distributions are intentionally not supported for technical reasons (complex build steps), and that nvidia only has drivers for x86-64 glibc and aarch64 linux (the package is complete).</small>

### :package: v1.1.0 <small>Jul 29, 2025</small> {#v1.1.0}

!!! quote ""
    First release with significant changes and new features in a while. Should be fully compatible with the previous usage, recommendation to use pinned version still holds.

    - Add support to change dithering via environment variable `ATTRIBUTE=dithering uvx nvibrant`, as some users have flickering/artifacts with it enabled. Related issue [#18](https://github.com/Tremeschin/nvibrant/issues/18) and [readme](https://github.com/Tremeschin/nvibrant?tab=readme-ov-file#-dithering) section.
    - Safer code that reads a type directly from argv with inline limits instead of an auxiliary vector.
    - Reviewed and overhauled the readme, better visibility, build instructions.

    <small><b>Note:</b> The env var defaults to `vibrance` if unset, in case you use it elsewhere - wished it was a CLI, but it works and I have other priorities.</small>

### :package: v1.0.6 <small>May 25, 2025</small> {#v1.0.6}

!!! quote ""
    - Add proper Multi GPU support with `NVIDIA_GPU=index` (default: 0) environment variable [#8](https://github.com/Tremeschin/nvibrant/issues/8)
    - Shouldn't break compatibility, slight worry for `>= v575` drivers, feedback welcome!

### :package: v1.0.5 <small>Apr 22, 2025</small> {#v1.0.5}

!!! quote ""
    - Search for a closest match of a previous driver in the bundled files if an exact match is not found (Commit [`f22db7`](https://github.com/Tremeschin/nVibrant/commit/f22db7395545ac93332cf87b197ec80e4d5d1717), issue [#7](https://github.com/Tremeschin/nvibrant/issues/7)). This makes it so that patch or minor bumps don't need a build every time. Should work even across major releases, you can't win if you don't play, right?
    - Added `packaging` dependency on python for easily finding the best version

### :package: v1.0.4 <small>Apr 20, 2025</small> {#v1.0.4}

!!! quote ""
    - Releases are now also published on [PyPI](https://pypi.org/project/nvibrant/). All nvidia driver versions binaries are bundled with them, using the one matching your current driver at runtime.
    - Move `meson` and `ninja` from the regular dependencies to development dependencies of v1.0.3 on PyPI
    - Package the 143 files in a `.tar.gz` for GitHub releases, that's what a good night of sleep does to you.
