---
title: Dithering
icon: material/grain
tags:
- Documentation
- Quickstart
- Dithering
---

Some users have issues with dithering causing flickering or artifacts on their displays [(1)](https://github.com/Tremeschin/nvibrant/issues/18) [(2)](https://www.reddit.com/r/linux_gaming/comments/1jmsva0/comment/mkehyuk/), or may prefer it enabled - which also lacks a Wayland option to disable in `nvidia-settings`.

Since nvibrant already sets up most of the work, I also included options for it :slight_smile:

## State

For enabling or disabling dithering in monitors, use the following numbers in args:

```sh
$ ATTRIBUTE=dithering nvibrant (...)
```

```cpp linenums="1"
enum NvKmsDpyAttributeRequestedDitheringValue {
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_AUTO = 0,
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_ENABLED = 1,
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_DISABLED = 2,
};
```

Default value is (2), disabling on all monitors without input arguments.

For enabling in certain or all monitors, similar to vibrance levels, adapt to your setup:

```sh
$ ATTRIBUTE=dithering nvibrant 0 2 2 1
$ ATTRIBUTE=dithering nvibrant 1 1 1 1
```

## Mode

!!! warning "Only in [git main](../get/source.md) builds, next patch release will include this option."

For setting the dithering mode when enabled, use the following numbers in args:

```sh
$ ATTRIBUTE=dithering-mode nvibrant (...)
```

```cpp linenums="1"
enum NvKmsDpyAttributeCurrentDitheringModeValue {
    NV_KMS_DPY_ATTRIBUTE_CURRENT_DITHERING_MODE_NONE = 0,
    NV_KMS_DPY_ATTRIBUTE_CURRENT_DITHERING_MODE_DYNAMIC_2X2 = 1,
    NV_KMS_DPY_ATTRIBUTE_CURRENT_DITHERING_MODE_STATIC_2X2 = 2,
    NV_KMS_DPY_ATTRIBUTE_CURRENT_DITHERING_MODE_TEMPORAL = 3,
};
```

Default value in nvibrant is (0), unsure about the driver.

## Depth

!!! warning "Only in [git main](../get/source.md) builds, next patch release will include this option."

For setting the dithering depth when enabled, use the following numbers in args:

```sh
$ ATTRIBUTE=dithering-depth nvibrant (...)
```

```cpp linenums="1"
enum NvKmsDpyAttributeRequestedDitheringDepthValue {
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_DEPTH_AUTO = 0,
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_DEPTH_6_BITS = 1,
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_DEPTH_8_BITS = 2,
    NV_KMS_DPY_ATTRIBUTE_REQUESTED_DITHERING_DEPTH_10_BITS = 3,
};
```

Default value in nvibrant is (0), likely in the driver too.
