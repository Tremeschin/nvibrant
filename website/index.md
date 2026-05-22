<div align="center">
  <h1>nvibrant</h1>
  <p>Configure Nvidia's Digital Vibrance on Wayland</p>
  <a href="https://pypi.org/project/nvibrant/"><img src="https://img.shields.io/pypi/v/nvibrant?label=PyPI&color=blue"></a>
  <a href="https://pypi.org/project/nvibrant/"><img src="https://img.shields.io/pypi/dw/nvibrant?label=Installs&color=blue"></a>
  <a href="https://github.com/Tremeschin/nvibrant/releases/"><img src="https://img.shields.io/github/v/release/Tremeschin/nvibrant?label=Release&color=light-green"></a>
  <a href="https://github.com/Tremeschin/nvibrant/releases/"><img src="https://img.shields.io/github/downloads/Tremeschin/nvibrant/total?label=Downloads&color=light-green"></a>
  <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
</div>

<img src="https://github.com/user-attachments/assets/962a3f4d-6022-402f-a47b-27aeba595a19"/>

## 🔥 Description

NVIDIA GPUs have a nice feature called *Digital Vibrance* that increases the colors saturation of the display. The option is readily available on [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/), but is too coupled with libxnvctrl, making it softly "exclusive" to the X11 display server over wayland; but I paid for my pixels to glow :^)

An interesting observation is that the setting persists after modifying it on X11 and then switching to Wayland. I theorized [(1)](https://github.com/libvibrant/vibrantLinux/issues/27#issuecomment-2729822152) [(2)](https://www.reddit.com/r/archlinux/comments/1gx1hir/comment/mhpe2pk/?context=3) it was possible to call some shared library or interface to configure it directly in their driver, independently of the display server, and indeed, it is possible!

This project uses `nvidia-modeset` and `nvkms` headers found at [nvidia/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules/) to make [ioctl](https://en.wikipedia.org/wiki/Ioctl) calls in the `/dev/nvidia-modeset` device for configuring display attributes.

**Note**: A future intended way will be through [NVML](https://developer.nvidia.com/management-library-nvml), as evident by some [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/blob/6c755d9304bf4761f2b131f0687f0ebd1fcf7cd4/src/libXNVCtrlAttributes/NvCtrlAttributesNvml.c#L1235) comments

<sup><b>❤️ Consider</b> [supporting](https://github.com/sponsors/Tremeschin/) my work, this took 30 hours to figure out, implement, write a website, make it convenient 🫠</sup>

## 📦 Getting Started

<div align="center">
  <a href="https://nvibrant.tremeschin.com/">
    <img src="https://github.com/user-attachments/assets/f74653a0-a62d-4911-b23b-f5d0ea03007e"/>
  </a>
  <i>
    Visit the documentation at
    <a href="https://nvibrant.tremeschin.com/">https://nvibrant.tremeschin.com/</a>
  </i>
</div>
