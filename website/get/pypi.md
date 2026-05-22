---
title: Python Registry
icon: material/language-python
tags:
- Install
- Python
- uv
---

!!! success "This is an official release channel for nvibrant"

## :simple-astral: With uv {#uv}

Following the concepts of [uv/tools](https://docs.astral.sh/uv/concepts/tools/), you can run nvibrant from an ephemeral environment:

```linenums="1"
uvx nvibrant (args)
```

For more stability and/or safety, pin to a specific [version](../about/changelog.md):

```linenums="1"
uvx nvibrant==1.2.1 (args)
```

## :material-language-python: With pip {#pip}

Simply install the [`pypi/nvibrant`](https://pypi.org/project/nvibrant/) package and run its main and only entry point:

```linenums="1"
python3 -m pip install nvibrant
python3 -m nvibrant (args)
```
