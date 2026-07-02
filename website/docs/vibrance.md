---
title: Vibrance
icon: octicons/sun-16
tags:
- Documentation
- Quickstart
- Vibrance
---

## Intensity

Vibrance levels are numbers from -1024 to 1023 that determines the intensity of the effect - zero being the default at boot, -1024 grayscale, and 1023 max saturation (200%).

## Usage

Values are passed as arguments to the `nvibrant` binary, matching the _order of physical ports_ the nvidia driver reports (may differ from the video server):

```sh
$ nvibrant 512 1023

Display 0:
• (0, HDMI) • Set Vibrance (  512) • Success
• (1, DP  ) • Set Vibrance ( 1023) • Success
• (2, DP  ) • Set Vibrance (    0) • None
...
```

You may only have monitors at the later ports[^disconnected], in which case use as:

[^disconnected]: `None` means the port has no outputs, it can never 'fail' and is skipped.

```sh
$ nvibrant 0 0 0 1023

Display 0:
• (0, HDMI) • Set Vibrance (    0) • None
• (1, DP  ) • Set Vibrance (    0) • None
• (2, DP  ) • Set Vibrance (    0) • None
• (3, DP  ) • Set Vibrance ( 1023) • Success
• (4, DP  ) • Set Vibrance (    0) • None
```

If a value is not passed for the Nth output, nvibrant defaults to zero, even if connected.

!!! tip "Tip"
    When no arguments are passed, it will effectively clear the vibrance for all outputs.
