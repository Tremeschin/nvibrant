---
title: Installation
tags:
- Installation
- Quickstart
---

!!! info "Before you start"

    Core nvibrant is a pure a C++ binary targeting a specific nvidia driver, which _may work_ across future major versions (590.xx, 595.xx, etc), but _**will**_ eventually break on nvidia's open-gpu changes.

    - For supporting transitional periods, older drivers (LTS, distros) and [GPUs](https://archlinux.org/news/nvidia-590-driver-drops-pascal-support-main-packages-switch-to-open-kernel-modules/), a solution is to make and bundle files for all [known drivers](https://github.com/NVIDIA/open-gpu-kernel-modules/tags) at release time, and chose a best one [dynamically](https://github.com/Tremeschin/nvibrant/blob/21da533faa675f90d2ee92bc4b472fc54220c1a7/nvibrant/__init__.py#L26-L47) at runtime.

    - **Don't panic** when it breaks, follow this [FAQ](../faq.md#new-drivers) section for a workaround and asking a patch release.

There's multiple ways to get nvibrant, pick your choice:

- [**:material-language-python: Python Registry**](pypi.md): Main release channel, small utility to find a best binary for the current driver from bundled wheel resources. <small>(Recommended, official release channel)</small>

- [**:octicons-package-16: Package Manager**](distro.md): Community packaging effort for native management in your distro, may use the same python utility or alternative 'wrappers' such as a bash script instead.

- [**:octicons-workflow-16: Workflow Builds**](actions.md): Download prebuilt assets from the GitHub Actions release Workflow, same files uploaded on PyPI via Trusted Publishing, with Immutable Releases.

- [**:material-git: Source Build**](source.md): Make it yourself from the source code, pure C++ or Python utility.

- [**:material-recycle: Community**](community.md): Derivative work, such as TUIs, GUIs, Integrations, etc.

After installing, go for the Documentation section above for usage, autostarting, etc!
