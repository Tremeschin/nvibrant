---
title: General
icon: octicons/package-16
description: Troubleshoot nvibrant issues including driver version mismatches, ioctl errors, and
  compatibility with new NVIDIA drivers using diagnostic checklists and common fixes.
tags:
- Questions
- Issues
---

## **Q:** Native Wayland Protocol {#wayland-protocol}

A standardized wayland colors protocol would eliminate the current nvidia-exclusive setting, by providing a common interface for display control for all compositors (brightness, contrast, etc).

> _Whether you're knowledgeable or know someone involved in wayland development, please try to submit a protocol for it, so Intel/AMD cards becomes an option for everyone._

Strong arguments:

- **:octicons-accessibility-16: Accessibility**: [Daltonic people](https://github.com/Tremeschin/nvibrant/issues/39#issue-4535578528) use it to help mitigate their health condition.
- **:octicons-issue-opened-16: Open issues** on [nvidia-settings](https://github.com/NVIDIA/nvidia-settings/issues/104), [vibrantLinux](https://github.com/libvibrant/vibrantLinux/issues/27) active for many years.
- **:material-star: nvibrant's** statistics on star counts, downloads, pypi package.

<small>:white_check_mark: <b>Get in touch</b> when it exists, so I can link it here and participate.</small>

<hr>

## **Q:** Intel and AMD cards {#intel-amd}

See the [:material-laptop: Laptops](./docs/laptop.md) page for insights, and join forces for a native [saturation-protocol](#wayland-protocol).

Apart from that, you can test how your display would look like with stronger colors by using the [mpv](https://github.com/mpv-player/mpv) video player and pressing the <kbd>8</kbd> key in a playback to increase saturation in the shader.

<hr>

## **Q:** Not working in newer drivers {#new-drivers}

> **Don't panic!** this is inevitable, learn about why in [#driver-compatibility](#driver-compatibility)

Follow these steps for a checklist in asking a new patch release and troubleshooting:

- [x] 1. Are you using the latest nvibrant release? Check the [:material-file-document-edit: Changelog](./changelog.md), update it, etc.

<p/>

- [x] 2. Has it been reported on GitHub? [Check here](https://github.com/Tremeschin/nvibrant/issues?q=is:issue), add a :thumbs_up: to confirm, read the messages.

<p/>

- [x] 3. Has your current driver been recently released (~2 weeks) and is a new major version?
    - Check drivers in [nvidia/open-gpu-kernel-modules](https://github.com/NVIDIA/open-gpu-kernel-modules/tags) repository tags.
    - Check current driver with `cat /sys/module/nvidia/version`
    - The first number is the major version (590.xx, 595.xx, etc).

    <small><b>Whether</b> that's not the case, follow [#common-issues](#common-issues)</small>

<p/>

- [x] 4. Make a [:material-git: Source Build](../get/source.md#wheel) using `uv build --wheel`, the hatchling build script automatically checkouts open-gpu to main and prints file hashes cutoffs for all drivers.
    - Compilation errors regarding open-gpu structs are a strong sign for breaking changes.
    - Does any new hash values shows up for a driver `<=` than yours?

<p/>

- [x] 5. Shall it compile without errors, test whether it works with the new driver without any code changes (simple recompilation), or would need further investigation:
    ```
    uvx --with dist/nvibrant-*.whl nvibrant (...)
    ```

-> Whether all of the above checks out, specially a new hash is seen, [Open an Issue](https://github.com/Tremeschin/nvibrant/issues/) in the repository using this [template](https://github.com/Tremeschin/nvibrant/issues/new?template=new-drivers.yml) for a patch release and add relevant outputs!

<small><b>Note:</b> Arch may take a while for new drivers to be packaged, your proactive help is essential for testing!</small>

<hr>

## **Q:** Driver compatibility {#driver-compatibility}

!!! tip "Always chose the closest, but not newer driver version file!"

There is some level of compatibility across different nvibrant and driver versions, as the related code is mostly stable on nvidia's side. However, internal struct layout changes[^struct-changes] breaks the ioctl communications every so often in new major releases, as seen in [`hatch_build.py`](https://github.com/Tremeschin/nvibrant/blob/9bafd52d0ab3202cdf76a49cb703e25c03a0d8af/hatch_build.py#L107-L121):

[^struct-changes]: For example, the removal of SLI options in 590.xx as Pascal (GTX 10xx) support was dropped happened to be a field in the GPU querying structures nvibrant uses [#31](https://github.com/Tremeschin/nvibrant/issues/31#issuecomment-4012908896), or random changes [#5](https://github.com/Tremeschin/nvibrant/issues/5#issuecomment-2814513826)

```
$ uv build --wheel
(...)

Breaking changes across driver versions:
• 863d221c62e2d33b4a6c8ca339aa226f  515.105.01
• 5fd8156069652d0b391e47e3e8829727  525.105.17
• d5886d1078ac5ee2ea534c7656574932  530.30.02
• e8c75422e1bcb3bce6814d7fe80bb8e1  535.104.05
• f34ce840fe61d912f8ca0dee98582e7d  545.23.06
• 66ca6dd1bf1b970d76d22025189ea520  560.28.03
• f5d81922f56fa19c315cd337f82158dd  565.57.01
• 9501cbd2421dcbc744ffbf96df6b8264  570.123.01
• 99c81b5cecdada319d14c20f7ec7a869  570.207
• 24dbdec0f91de3670fdf35c830c8ad4d  575.51.02
• 5bbeda89c90e81a5dac8a19b2a4657a3  595.104.02
• 3177754bdea0f33d08e19b2a218920a9  610.43.02
• 69e206a262263d607c8aceb9ed4378e5  615.71.09
• aa28f96477d9af03e819fb52ff884b9f  620.70.06

Successfully built dist/nvibrant-1.3.1-py3-none-manylinux_2_17_x86_64.whl

```

Any driver version between two versions _should_ work using the lowest of the two - this choice is automatically made by the [Python utility](./get/pypi.md), manual usage should follow the same logic!

<hr>

## **Q:** Common Issues {#common-issues}

- If you get a _"Driver version mismatch"_ or `ioctl` errors, maybe try rebooting (if you haven't) since the last driver update, it must match what `/dev/nvidia-modeset` expects and is currently loaded in the kernel. Otherwise, force it with `NVIDIA_DRIVER_VERSION=x.y.z`.

- Ensure you have the `nvidia-modeset` kernel module loaded, as it is required for the ioctl calls to work, you can check this with `lsmod | grep nvidia`. Should be enabled by default on any sufficiently recent (2025-) driver,else add it to your kernel boot parameters.
