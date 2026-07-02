---
title: General
icon: octicons/package-16
tags:
- Questions
- Issues
---

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

There is some level of compatibility across different nvibrant and driver versions, as the related code is mostly stable on nvidia's side. However, internal struct layout changes[^struct-changes] breaks the ioctl communications every so often in new major releases, as seen in:

[^struct-changes]: For example, the removal of SLI options in 590.xx as Pascal (GTX 10xx) support was dropped happened to be a field in the GPU querying structures nvibrant uses [#31](https://github.com/Tremeschin/nvibrant/issues/31#issuecomment-4012908896), or random changes [#5](https://github.com/Tremeschin/nvibrant/issues/5#issuecomment-2814513826)

```sh
$ unzip nvibrant-*-py3-none-manylinux_2_17_x86_64.whl
$ md5sum nvibrant/resources/* | /bin/uniq -w32
```

```
6b9ec215720784c4c054825d9ece0bc1  nvibrant/resources/nvibrant-515.43.04
eadac0e0a9561622e99bda44c270902b  nvibrant/resources/nvibrant-525.47.04
9d5db7eba4830c967ea09682ac4b664d  nvibrant/resources/nvibrant-530.30.02
4d1392be4ec7dcb58e046b0336cde5ff  nvibrant/resources/nvibrant-535.43.02
041bfdaaeda4ea9b861e647b4ce62f09  nvibrant/resources/nvibrant-545.23.06
91bc7cbb12ca31156ccaca5d5e32e6a7  nvibrant/resources/nvibrant-560.28.03
4c3d16ff6094a85d9d6a16c97d810c6d  nvibrant/resources/nvibrant-565.57.01
5f5ac2875d3535cd3bfcf2e7a96c813d  nvibrant/resources/nvibrant-570.86.15
2ff5ff75acd9d2775db6d06eef4f437b  nvibrant/resources/nvibrant-570.207
b33bc562dc8c67f924cea9bb12b18fc4  nvibrant/resources/nvibrant-575.51.02
b0d592a68e4e22a843318074b960b9c1  nvibrant/resources/nvibrant-595.45.04
```

Any driver version between two versions _should_ work using the lowest of the two - this choice is automatically made by the [Python utility](./get/pypi.md), manual usage should follow the same logic!

<hr>

## **Q:** Common Issues {#common-issues}

- If you get a _"Driver version mismatch"_ or `ioctl` errors, maybe try rebooting (if you haven't) since the last driver update, it must match what `/dev/nvidia-modeset` expects and is currently loaded in the kernel. Otherwise, force it with `NVIDIA_DRIVER_VERSION=x.y.z`.

- Ensure you have the `nvidia-modeset` kernel module loaded, as it is required for the ioctl calls to work, you can check this with `lsmod | grep nvidia`. Should be enabled by default on any sufficiently recent (2025-) driver,else add it to your kernel boot parameters.
