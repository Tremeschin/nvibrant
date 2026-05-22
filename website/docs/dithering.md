---
title: Dithering
icon: material/grain
tags:
- Documentation
- Quickstart
- Dithering
---

Some users have issues with dithering causing flickering or artifacts on their displays [(1)](https://github.com/Tremeschin/nvibrant/issues/18) [(2)](https://www.reddit.com/r/linux_gaming/comments/1jmsva0/comment/mkehyuk/), which also lacks a Wayland option to disable in `nvidia-settings`. Fear not, nvibrant has you covered!

```sh linenums="1"
ATTRIBUTE=dithering nvibrant (args)
```

Minor quirk, here's the values meanings, default is 2 disabling on all monitors without arguments:

```cpp
enum NvKmsDpyAttributeRequestedDitheringValue {
    ...AUTO = 0,
    ...ENABLED = 1,
    ...DISABLED = 2,
};
```
