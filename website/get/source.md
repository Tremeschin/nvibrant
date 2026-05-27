---
title: Source Build
icon: material/git
tags:
- Install
- Source
---

!!! success "This is an official release channel for nvibrant"

Clone the repository with latest `open-gpu` submodule changes:

```sh linenums="1"
git clone https://github.com/Tremeschin/nvibrant && cd nvibrant
git submodule update --init --remote
```

## Pure C++ {#cpp}

From here, you can either build only the C++ part for a target driver:

```sh linenums="1" title="Chose a target driver"
# Any tag from https://github.com/NVIDIA/open-gpu-kernel-modules/tags
cd open-gpu && git checkout 575.64.03 && cd ..
```

```sh linenums="1" title="Configure and compile"
meson setup --buildtype release ./build
ninja -C ./build
```

```sh linenums="1" title="Run the program"
./build/nvibrant 512 512
```

## Wheel {#wheel}

Or make a wheel for all drivers at `dist/*` for your host platform:

```sh linenums="1"
uv build --wheel
```