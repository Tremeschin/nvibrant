<div align="center">
  <h1>nVibrant</h1>
  <p>Configure NVIDIA's Digital Vibrance on Wayland</p>
</div>

## DOWNLOAD v1.0.6 NEW REDUCED EDITION 👇 https://github.com/JustLachin/nVibrant-gui/releases/download/v1.0.6-gui-new-reduced/nvibrant.zip

<img src="https://raw.githubusercontent.com/JustLachin/nVibrant-gui/refs/heads/main/main.png"  alt="Preview"/>

> [!IMPORTANT]
> This repository is a proof of concept that will be improved over time, e.g. proper CLI and distro packaging are WIP. Contributions are welcome, as I'm not primarily a C/C++ developer 🙂

## 🔥 Description

**NVIDIA GPUs** have a nice feature called **Digital Vibrance** that increases the colors saturation of the display. The option is readily available on [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/) in Linux, but is too coupled with `libxnvctrl`. Therefore, it's "exclusive" to the X11 display server and unavailable on Wayland; but I paid for my pixels to glow :^)

An interesting observation is that the setting persists after modifying it on X11 and then switching to Wayland. I theorized [[1]](https://github.com/libvibrant/vibrantLinux/issues/27#issuecomment-2729822152) [[2]](https://www.reddit.com/r/archlinux/comments/1gx1hir/comment/mhpe2pk/?context=3) it was possible to call some shared library or interface to configure it directly in their driver, independently of the display server. And indeed, it is possible!

This repository uses `nvidia-modeset` and `nvkms` headers found at [nvidia/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules/) to make [ioctl](https://en.wikipedia.org/wiki/Ioctl) calls in the `/dev/nvidia-modeset` device for configuring display attributes. These headers are synced with the proprietary releases, should work fine if you're on any of `nvidia-dkms`, `nvidia-open` or `nvidia`

**Note**: A future (and intended) way to will be through [NVML](https://developer.nvidia.com/management-library-nvml), as evident by some [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/blob/6c755d9304bf4761f2b131f0687f0ebd1fcf7cd4/src/libXNVCtrlAttributes/NvCtrlAttributesNvml.c#L1235) comments

## 📦 Installation

There's multiple ways to get nvibrant:

### 1. Package manager

You can install from your distro's package manager, if available:

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

  <!-- Add yours -->
  <tr>
    <td>...</td>
    <td>...</td>
    <td><i>Help me by packaging for your distro!</i></td>
    <td>You 🙂</td>
  </tr>
</table>

<div align="center">
  <sup>❤️ Thanks to all package maintainers for your work! ❤️</sup>
</div>


### 2. PyPI Package

This method automatically choses the right binary for your driver version, the most convenient.

Install the [nvibrant](https://pypi.org/project/nvibrant/) package with any `pip` compatible tool:

```sh
# Note: You might need to use 'pip3', or
# 'python -m pip', or 'python3 -m pip'.
pip install nvibrant
```

Then run it with::

```sh
nvibrant 512 1023
```

Alternatively, install [uv](https://docs.astral.sh/uv/) and use it as a [tool](https://docs.astral.sh/uv/concepts/tools/), or run directly with:

```sh
# Always uses latest version
uvx nvibrant (args)
```

<b>Note:</b> Using `uvx` is highly recommended, it installs at `~/.local/share/uv` and `~/.cache/uv`.


### 3. Prebuilt binaries

You can download the latest builds made by GitHub Actions in the [Releases](https://github.com/Tremeschin/nVibrant/releases) page

- Remember to run `chmod +x nvibrant*` to mark non tar.gz files as executable!


### 4. Build it yourself

**Pre-requisites**: Have [git](https://git-scm.com/), [uv](https://docs.astral.sh/uv) and GCC Compilers installed, then run:

- `git clone https://github.com/Tremeschin/nVibrant && cd nVibrant`
- `git submodule update --init --recursive`
- `uv run nvibrant-build`

You should have the executables for all driver versions located at `nvibrant/resources/*.bin`, then:

- Either run any compiled executable directly, ideally matching your driver version,
- Install with `pip install .` to have `nvibrant` available in the user site packages
- Directly run as `uv run nvibrant (args)` to handle all of that and python for you

## 🚀 Usage

> See the [Common Issues](#common-issues) section for any problems • And here for [Autostarting](#automatically-running-on-login) it on login!

**Inputs**: Vibrance Levels are numbers from `-1024` to `1023` that determines the intensity of the effect. Zero being the "no effect" (default at boot), `-1024` grayscale, and `1023` max saturation (200%)

The values are passed as arguments to `nvibrant`'s binary, matching the **order of physical ports** in your GPU (not the index of the video server). For example, I have two monitors on HDMI and DisplayPort in an RTX 3060 first two ports, to set vibrance to `512` and `1023`, respectively, I would run:

```sh
# Will be './nvibrant-linux-amd64-v1.0.2.bin' instead of 'nvibrant'
# if you're using the prebuilt binaries from the releases page!
$ nvibrant 512 1023

GPU 0:
• (0, HDMI) • Set Vibrance (  512) • Success
• (1, DP  ) • Set Vibrance ( 1023) • Success
• (2, DP  ) • Set Vibrance (    0) • None
• (3, DP  ) • Set Vibrance (    0) • None
• (4, DP  ) • Set Vibrance (    0) • None
• (5, DP  ) • Set Vibrance (    0) • None
• (6, DP  ) • Set Vibrance (    0) • None
```

<sup><b>Note:</b> You might need to set `nvidia_drm.modeset=1` kernel parameter, but I think it's enabled by default on recent drivers.</sup>

If a value is not passed for the Nth physical output, nvibrant will default to zero. When no argument is passed, it will effectively clear the vibrance for all outputs. `None` means the output is disconnected

✅ You might have a display at the later ports, in which case use as:

```sh
$ nvibrant 0 0 0 1023

GPU 0:
• (0, HDMI) • Set Vibrance (    0) • None
• (1, DP  ) • Set Vibrance (    0) • None
• (2, DP  ) • Set Vibrance (    0) • None
• (3, DP  ) • Set Vibrance ( 1023) • Success
• (4, DP  ) • Set Vibrance (    0) • None
```

### Multiple Displays on Multiple GPUs

If you have multiple displays on multiple GPUs, it _should_ work too:

```sh
# Fictional example, feedback welcome!
$ nvibrant 0 100 512 1023

GPU 0:
• (0, HDMI) • Set Vibrance (    0) • Success
• (1, DP  ) • Set Vibrance (  100) • Success

GPU 1:
• (0, HDMI) • Set Vibrance (  512) • Success
• (1, DP  ) • Set Vibrance ( 1023) • Success
```

### Automatically Running on Login

You can rename and place the binary at `~/.local/bin/nvibrant` (or find the distro's one by running `which nvibrant`) and write a quick Desktop Entry, Systemd Service or other methods to run it on login:

<b>1. Desktop Autostart</b>: Should work on GNOME, KDE, Xfce, etc, maybe not WMs

Create a file at `~/.config/autostart/nvibrant.desktop` with the content:

```ini
[Desktop Entry]
Type=Application
Name=nVibrant
Exec=/home/tremeschin/.local/bin/nvibrant 1023 1023
X-GNOME-Autostart-enabled=true
NoDisplay=true
```

Do replace `tremeschin` with your username!

Or you can also use [uv](https://docs.astral.sh/uv/) to always grab latest [PyPI](https://pypi.org/project/nvibrant/), in case of driver updates:

```ini
[Desktop Entry]
Type=Application
Name=nVibrant
Exec=uvx nvibrant 1023 1023
X-GNOME-Autostart-enabled=true
NoDisplay=true
```

Or pin it to a specific version as `uvx nvibrant==1.0.3 (args)`, so it's more secure.

<b>2. Systemd Service</b>: Works everywhere if you use systemd (very likely)

Create a file at `~/.config/systemd/user/nvibrant.service` with the content:

```ini
[Unit]
Description=Set NVIDIA Vibrance
After=graphical.target

[Service]
Type=oneshot
ExecStart=%h/.local/bin/nvibrant 1023 1023

[Install]
WantedBy=default.target
```

Then run `systemctl --user enable nvibrant.service` to enable it on login, add `--now` for immediate effect.

Using `uvx` could work too per last sections, not sure of the behavior.

<b>3. Window Manager</b>: Search for your WM's autostart method in the configs

### Common Issues

Please [report](https://github.com/Tremeschin/nVibrant/issues) unknown or unlisted issues to be added here!

- If you get a _"Driver version mismatch"_ or `ioctl` errors, maybe try rebooting (if you haven't) since the last driver update. Otherwise, you can force the version with `NVIDIA_DRIVER_VERSION=x.y.z`. It must match what `/dev/nvidia-modeset` expects and is currently loaded in the kernel.

- It's possible that nVibrant may fail on future or older drivers due to differences between the internal structs and enums in the latest `nvkms` headers. Please report any issues you encounter!

<sup><b>❤️ Consider</b> [supporting](https://github.com/sponsors/Tremeschin/) my work, this took 16 hours to figure out and implement :)</sup>

## ⭐️ Future Work

Integrating this work directly in [libvibrant](https://github.com/libvibrant/) would be the ideal solution, although matching the nvidia driver version could be annoying for a generalized solution. Feel free to base off this code for an upstream solution and PR, in the meantime, here's some local improvements that could be made:

- Package the binary in many linux distros (help needed!)
- Save the current values to restore it later
- Add support for other Display Attributes (Dithering et al.)
- Make an actual CLI interface with `--help`, `--version`, etc.
- I am _probably_ not doing safe-C code or mallocs right :^)

Contributions are welcome if you are more C/C++ savy than me! 🙂
