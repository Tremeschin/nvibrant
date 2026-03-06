
## 📦 v1.2.0

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
    - Rename internal binaries from `nvibrant-linux-amd64-590-48-01-v1.1.0.bin` to `nvibrant-590.48.01`, as wheels already contain version information, and package managers should vendor target drivers separately.
- Stop providing standalone `.tar.gz` releases, as [`.whl` are Zips](https://packaging.python.org/en/latest/specifications/binary-distribution-format/) and can easily extract `/nvibrant/resources/*`
- Downgrade the build script into regular build hook, always making a wheel for the current host (a step towards sdists). Should be buildable in Linux ARM now, feedback welcome.

<small><b>Note</b> that source distributions are intentionally not supported for technical reasons (complex build steps), and that nvidia only has drivers for x86-64 glibc and aarch64 linux (the package is complete).</small>

## 📦 v1.1.0

First release with significant changes and new features in a while. Should be fully compatible with the previous usage, recommendation to use pinned version still holds.

- Add support to change dithering via environment variable `ATTRIBUTE=dithering uvx nvibrant`, as some users have flickering/artifacts with it enabled. Related issue [#18](https://github.com/Tremeschin/nvibrant/issues/18) and [readme](https://github.com/Tremeschin/nvibrant?tab=readme-ov-file#-dithering) section.
- Safer code that reads a type directly from argv with inline limits instead of an auxiliary vector.
- Reviewed and overhauled the readme, better visibility, build instructions.

<small><b>Note:</b> The env var defaults to `vibrance` if unset, in case you use it elsewhere - wished it was a CLI, but it works and I have other priorities.</small>


## 📦 v1.0.6

- Add proper Multi GPU support with `NVIDIA_GPU=index` (default: 0) environment variable [#8](https://github.com/Tremeschin/nvibrant/issues/8)
- Shouldn't break compatibility, slight worry for `>= v575` drivers, feedback welcome!


## 📦 v1.0.5

- Search for a closest match of a previous driver in the bundled files if an exact match is not found (Commit [`f22db7`](https://github.com/Tremeschin/nVibrant/commit/f22db7395545ac93332cf87b197ec80e4d5d1717), issue [#7](https://github.com/Tremeschin/nvibrant/issues/7)). This makes it so that patch or minor bumps don't need a build every time. Should work even across major releases, you can't win if you don't play, right?
- Added `packaging` dependency on python for easily finding the best version


## 📦 v1.0.4

- Releases are now also published on [PyPI](https://pypi.org/project/nvibrant/). All nvidia driver versions binaries are bundled with them, using the one matching your current driver at runtime.
- Move `meson` and `ninja` from the regular dependencies to development dependencies of v1.0.3 on PyPI
- Package the 143 files in a `.tar.gz` for GitHub releases, that's what a good night of sleep does to you.
