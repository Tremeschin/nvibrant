---
title: Laptops
icon: material/laptop
description: Laptops documentation, technical issues and solutions for multiple
  manufacturers in changing vibrance and dithering on wayland for hybrid systems.
tags:
- Documentation
- Quickstart
- Laptop
---

!!! tip "Main GitHub tracker and issues: [Tremeschin/nvibrant#22](https://github.com/Tremeschin/nvibrant/issues/22)"

## Problem

nvibrant makes calls to the nvidia driver, which is then responsible for the color transformation matrix in the outputs. For power efficiency reasons, laptops only uses the dedicated GPU on intensive tasks, dynamically switching with any of [Optimus](https://wiki.archlinux.org/title/NVIDIA_Optimus), [Bumblebee](https://wiki.archlinux.org/title/Bumblebee), or [PRIME](https://wiki.archlinux.org/title/PRIME) on Linux.

As such, the Integrated GPU (iGPU) "owns" the displays at all times, being the middle man to transfer rendered frames from the Discrete GPU (dGPU) to the display.

> _**Notice the problem**: the nvidia driver isn't controlling the outputs!_

Other tools like [vibrantLinux](https://github.com/libvibrant/vibrantLinux) uses existing [Color Transformation Matrix](https://unix.stackexchange.com/a/730078) protocols in X11 and/or Linux Direct Rendering Manager (DRM) to achieve the effect.

## Solution

You must ensure only the nvidia card and driver is active on the system, by disabling the integrated graphics in your BIOS/UEFI settings - assuming it is even supported or possible.

!!! danger "Expect much worse battery life with such!"

!!! info "**Advocate** for a vendor-agnostic wayland [saturation-protocol](../help.md#saturation-protocol) today!"

Seek help in manuals, forums for your model, send pull requests for information below:

### :simple-acer: Acer

:hash: Unknown

### :simple-alienware: Alienware

:hash: Unknown

### :simple-asus: Asus

:hash: Unknown

### :simple-dell: Dell

:hash: Unknown

### :simple-framework: Framework

:hash: Unknown

### :simple-hp: HP

:hash: Unknown

### :simple-lenovo: Lenovo

:hash: Unknown

### :material-microsoft: Microsoft

:hash: Unknown

### :simple-system76: System76

:hash: Unknown

### :simple-samsung: Samsung

:hash: Unknown
