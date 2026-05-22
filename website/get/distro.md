---
title: Package Manager
icon: octicons/package-16
tags:
- Install
- Package Manager
---

!!! info "Community packages are often safe, but not always checked by me!"

## :material-arch: Arch Linux

Install the [`nvibrant-bin`](https://aur.archlinux.org/packages/nvibrant-bin) AUR package using [helpers](https://wiki.archlinux.org/title/AUR_helpers) or manually:

=== ":octicons-package-16: yay"
    ```sh linenums="1"
    yay -S nvibrant-bin
    ```

=== ":octicons-package-16: paru"
    ```sh linenums="1"
    paru -S nvibrant-bin
    ```

=== ":octicons-gear-16: Manual"
    ```sh linenums="1"
    git clone https://aur.archlinux.org/nvibrant-bin.git
    cd nvibrant-bin && makepkg -si
    ```

<small><b>Maintainer: <a href="https://github.com/Incognitux">@Incognitux</a></b></small>

<hr>

## :material-fedora: Fedora

Install the [`nvibrant`](https://copr.fedorainfracloud.org/coprs/starfish/nvibrant) rpm from the starfish COPR repository, generally speaking:

Enable the repository and install the package:

```sh linenums="1"
sudo dnf copr enable starfish/nvibrant
```

=== "Normal Fedora"
    ```sh linenums="1"
    sudo dnf install nvibrant
    ```

=== "Fedora Silverblue"
    ```sh linenums="1"
    rpm-ostree install nvibrant
    ```

<small><b>Maintainer: <a href="https://github.com/ykshek">@ykshek</a></b></small>

<hr>

## :material-nix: Nix Flakes

Use the [`nix-nvibrant`](https://github.com/mikaeladev/nix-nvibrant) flake, see repo for instructions.

<small><b>Maintainer: <a href="https://github.com/mikaeladev">@mikaeladev</a></b></small>

## :octicons-three-bars-16: Others

Consider packaging it for your distro and send pull requests here!
