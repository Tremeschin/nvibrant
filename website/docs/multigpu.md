---
title: Multi GPU
icon: material/inbox-multiple-outline
description: Configure Digital Vibrance on Wayland in systems with multiple GPUs
  by using environment variables to target an specific card in nvibrant.
tags:
- Documentation
- Quickstart
---

If you have multiple devices, specify a `NVIDIA_GPU=N` index:

```sh
$ NVIDIA_GPU=1 nvibrant 0 100

Display 0:
• (0, HDMI) • Set Vibrance (    0) • Success
• (1, DP  ) • Set Vibrance (  100) • Success
```
