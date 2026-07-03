---
title: Python Registry
icon: material/language-python
description: Official Python release channel for nvibrant, providing the PyPI package
  with bundled files for all nvidia drivers, installation using uv or pip.
tags:
- Install
- Python
- uv
---

!!! success "This is an official release channel for nvibrant"

## :simple-astral: With uv {#uv}

Have [astral-sh/uv](https://docs.astral.sh/uv/) installed - a modern python manager and runner.

Following the concepts of [uv/tools](https://docs.astral.sh/uv/concepts/tools/), you can run nvibrant from an ephemeral environment:

```linenums="1"
uvx nvibrant (args)
```

For more stability and/or safety, pin to a specific [version](../changelog.md):

```linenums="1"
uvx nvibrant==1.2.1 (args)
```

## :material-language-python: With pip {#pip}

Simply install the [`pypi/nvibrant`](https://pypi.org/project/nvibrant/) package and run its main and only entry point:

```linenums="1"
python3 -m pip install nvibrant
python3 -m nvibrant (args)
```
