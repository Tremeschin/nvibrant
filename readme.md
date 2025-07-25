<div align="center">
  <h1>nvibrant</h1>
  <p>Configure NVIDIA's Digital Vibrance on Wayland</p>
  <a href="https://pypi.org/project/nvibrant/"><img src="https://img.shields.io/pypi/v/nvibrant?label=PyPI&color=blue"></a>
  <a href="https://pypi.org/project/nvibrant/"><img src="https://img.shields.io/pypi/dw/nvibrant?label=Installs&color=blue"></a>
  <a href="https://github.com/Tremeschin/nvibrant/"><img src="https://img.shields.io/github/v/tag/Tremeschin/nvibrant?label=GitHub&color=orange"></a>
  <a href="https://github.com/Tremeschin/nvibrant/stargazers/"><img src="https://img.shields.io/github/stars/Tremeschin/nvibrant?label=Stars&style=flat&color=orange"></a>
  <a href="https://github.com/Tremeschin/nvibrant/releases/"><img src="https://img.shields.io/github/v/release/Tremeschin/nvibrant?label=Release&color=light-green"></a>
  <a href="https://github.com/Tremeschin/nvibrant/releases/"><img src="https://img.shields.io/github/downloads/Tremeschin/nvibrant/total?label=Downloads&color=light-green"></a>
  <a href="https://discord.gg/KjqvcYwRHm"><img src="https://img.shields.io/discord/1184696441298485370?label=Discord&style=flat&color=purple"></a>
  <br>
  <br>
</div>

## 🔥 Description

NVIDIA GPUs have a nice feature called *Digital Vibrance* that increases the colors saturation of the display. The option is readily available on [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/) in Linux, but is too coupled with `libxnvctrl`, making it softly "exclusive" to the X11 display server over wayland; but I paid for my pixels to glow :^)

An interesting observation is that the setting persists after modifying it on X11 and then switching to Wayland. I theorized [(1)](https://github.com/libvibrant/vibrantLinux/issues/27#issuecomment-2729822152) [(2)](https://www.reddit.com/r/archlinux/comments/1gx1hir/comment/mhpe2pk/?context=3) it was possible to call some shared library or interface to configure it directly in their driver, independently of the display server, and indeed, it is possible!

This repository uses `nvidia-modeset` and `nvkms` headers found at [nvidia/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules/) to make [ioctl](https://en.wikipedia.org/wiki/Ioctl) calls in the `/dev/nvidia-modeset` device for configuring display attributes. These headers are synced with the proprietary releases, should work fine if you're on any of `nvidia-dkms`, `nvidia-open` or `nvidia`.

**Note**: A future, and intended way, will be through [NVML](https://developer.nvidia.com/management-library-nvml), as evident by some [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/blob/6c755d9304bf4761f2b131f0687f0ebd1fcf7cd4/src/libXNVCtrlAttributes/NvCtrlAttributesNvml.c#L1235) comments

## 📦 Installation

There's multiple ways to get nvibrant, do check the [usage](#-usage) and [autostarting](#-autostarting) sections afterwards!

### 🔴 Python package

This utility [finds the best](https://github.com/Tremeschin/nvibrant/blob/4d9cc065f13c8110e5dd22368715ff07299b8192/nvibrant/__init__.py#L73-L95) nvibrant binary for your driver, already bundled in the package for all known [tags](https://github.com/NVIDIA/open-gpu-kernel-modules/tags) at release time. Simply install the [`pypi/nvibrant`](https://pypi.org/project/nvibrant/) package, where [`uvx`](https://docs.astral.sh/uv/) • [`tools`](https://docs.astral.sh/uv/concepts/tools/) usage is recommended:

```sh
# With standard python tooling
$ python3 -m pip install nvibrant
$ python3 -m nvibrant 512 512

# Always latest, simpler
$ uvx nvibrant 512 512
```

<sup><b>Note:</b> This package is an official release channel for nvibrant</sup>


### 🟡 Package manager

Install from your distro's package manager, it may use the python package at system level:

<table align="center">
  <tr>
    <th></th>
    <th>Distro</th>
    <th>Installation</th>
    <th>Maintainer</th>
  </tr>

  <!-- Arch Linux -->
  <tr>
    <td>
      <img src="https://raw.githubusercontent.com/edent/SuperTinyIcons/refs/heads/master/images/svg/arch_linux.svg" width="64">
    </td>
    <td>
      Arch Linux
    </td>
    <td>
      Install the <a href="https://aur.archlinux.org/packages/nvibrant-bin"><code>nvibrant-bin</code></a> AUR package:
      <ul>
        <li><code><a href="https://github.com/Morganamilo/paru">paru</a> -Syu nvibrant-bin</code></li>
        <li><code><a href="https://github.com/Jguer/yay">yay</a> -Syu nvibrant-bin</code></li>
      </ul>
    </td>
    <td>
      <a href="https://github.com/Incognitux">@Incognitux</a>
    </td>
  </tr>

  <!-- Add yours via PR -->
  <tr>
    <td>...</td>
    <td>...</td>
    <td>
      <div align="center">
        <i>Help me by packaging for your distro!</i>
        <br><sup>❤️ Thanks to all maintainers for your work! ❤️</sup>
      </div>
    </div>
    </td>
    <td>You 🙂</td>
  </tr>
</table>

<sup><b>Obligatory:</b> Third-party packages are often safe but not checked by me</sup>

### 🟢 Prebuilt binaries

You can download all latest builds made by GitHub Actions in the [Releases](https://github.com/Tremeschin/nvibrant/releases) page as a `.tar.gz` archive, just remember to run `chmod +x nvibrant*` to mark the files as executable after extracting!

- Run them directly as `./nvibrant-linux-amd64-<driver>-v<version>.bin (args)`

> [!NOTE]
> There is some level of compatibility across different nvibrant and driver versions, as the related code is mostly stable on nvidia's side. Always prefer using the closest, but not newer, version to your driver!
> - **Example**: Running `nvibrant-linux-amd64-575.51.03-v1.0.6.bin` on driver `v575.64.03` works
> - This is automatically handled by the python utility, hence the strong recommendation :)


### 🔵 Build it yourself

**Requirements**: Have `git`, `gcc` compilers; `meson` and `ninja` _(too)_ are already `python3` dependencies

```sh
# Clone the code alongside nvidia kernel headers
git clone https://github.com/Tremeschin/nvibrant && cd nvibrant
git submodule update --init --recursive
```

From here, you can either build only the C++ part for a target driver:

```sh
# Any tag from https://github.com/NVIDIA/open-gpu-kernel-modules/tags
$ cd open-gpu && git checkout 575.64.03 && cd ..

# Configure and compile project, final binary at 'build' directory
$ meson setup --buildtype release ./build && ninja -C ./build
$ ./build/nvibrant 512 512
```

Or build them all for the python utility to use:

```sh
# Installs dependencies on the user's site-packages
$ python3 -m pip install -r requirements.txt
$ python3 ./nvibrant/build.py

# Have it on path or run directly
$ ~/.local/bin/nvibrant 512 512
```


## 🚀 Usage

**Inputs**: Vibrance Levels are numbers from `-1024` to `1023` that determines the intensity of the effect. Zero being the "no effect" (default at boot), `-1024` grayscale, and `1023` max saturation (200%)

The values are passed as arguments to `nvibrant`'s binary, matching the _order of physical ports_ in your GPU (not the index of the video server). For example, I have two monitors on HDMI and DisplayPort in an RTX 3060 first two outputs, to set vibrance to `512` and `1023`, respectively, I would run:

```sh
$ nvibrant 512 1023

Display 0:
• (0, HDMI) • Set Vibrance (  512) • Success
• (1, DP  ) • Set Vibrance ( 1023) • Success
• (2, DP  ) • Set Vibrance (    0) • None
...
```

<sup><b>Note:</b> You might need to set `nvidia_drm.modeset=1` kernel parameter, but I think it's enabled by default on recent drivers.</sup>

If a value is not passed for the Nth physical output, nvibrant will default to zero. When no argument is passed, it will effectively clear the vibrance for all outputs. `None` means the output is disconnected.

✅ You might have a display at the later ports, in which case use as:

```sh
$ nvibrant 0 0 0 1023

Display 0:
• (0, HDMI) • Set Vibrance (    0) • None
• (1, DP  ) • Set Vibrance (    0) • None
• (2, DP  ) • Set Vibrance (    0) • None
• (3, DP  ) • Set Vibrance ( 1023) • Success
• (4, DP  ) • Set Vibrance (    0) • None
```

### 🔴 Multiple Displays on Multiple GPUs

If you have multiple devices, specify a `NVIDIA_GPU=N` index:

```sh
$ NVIDIA_GPU=1 nvibrant 0 100

Display 0:
• (0, HDMI) • Set Vibrance (    0) • Success
• (1, DP  ) • Set Vibrance (  100) • Success
```

### 🟡 Autostarting

For simplicity, a Systemd user service running either `uvx` for the latest releases (in case of driver updates), or a prebuilt binary directly should cover most users, plus it integrates well with [dotfiles](https://github.com/Tremeschin/DotFiles/blob/main/.config/systemd/user/nvibrant.service) repositories!

Create a file at `~/.config/systemd/user/nvibrant.service` with the content:

```ini
[Unit]
Description=Apply nvibrant
After=graphical.target

[Service]
Type=oneshot
ExecStart=uvx nvibrant 1023 1023

[Install]
WantedBy=default.target
```

Enable the service with `systemctl --user enable --now nvibrant.service`

- You can also pin it to a specific version with `uvx nvibrant==1.0.6 (args)` to have more control
- Can also have a `~/.local/bin/nvibrant` and use `ExecStart=%h/.local/bin/nvibrant (args)`

### 🟢 Common Issues

Please [report](https://github.com/Tremeschin/nvibrant/issues) unknown or unlisted issues to be added here!

- If you get a _"Driver version mismatch"_ or `ioctl` errors, maybe try rebooting (if you haven't) since the last driver update. Otherwise, you can force the version with `NVIDIA_DRIVER_VERSION=x.y.z`. It must match what `/dev/nvidia-modeset` expects and is currently loaded in the kernel.

- Ensure you have the `nvidia-modeset` kernel module loaded, as it is required for the ioctl calls to work. You can check this with `lsmod | grep nvidia`. Else, add it to your kernel boot parameters.

- It's possible that nvibrant may fail on future or older drivers due to differences between the internal structs and enums in the latest `nvkms` headers. Please report any issues you encounter!

<sup><b>❤️ Consider</b> [supporting](https://github.com/sponsors/Tremeschin/) my work, this took 16 hours to figure out and implement :)</sup>

## ⭐️ Future Work

Integrating this work directly in [libvibrant](https://github.com/libvibrant/) would be the ideal solution, although matching the nvidia driver version could be annoying for a generalized solution. Feel free to base off this code for an upstream solution and PR, in the meantime, here's some local improvements that could be made:

- Add support for other Display Attributes (Dithering et al.)
- Make an actual CLI interface with `--help`, `--version`, etc.
- I am _probably_ not doing safe-C code or mallocs right :^)

Contributions are welcome if you are more C/C++ savy than me! 🙂
