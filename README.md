# Zensical WaveDrom Plugin

[![PyPI](https://badge.fury.io/py/zensical-wavedrom-plugin.svg)](https://pypi.org/project/zensical-wavedrom-plugin/)

A Markdown extension for rendering [WaveDrom](https://wavedrom.com/) digital timing diagrams, ported from [mkdocs-wavedrom-plugin](https://github.com/kuri65536/mkdocs-wavedrom-plugin) (or, my [maintained fork](https://github.com/jiegec/mkdocs-wavedrom-plugin)). Visit the [demo site](https://jia.je/zensical-wavedrom-plugin).

This plugin is registered as a `markdown.extensions` entry point, so it works with any [Python-Markdown](https://github.com/Python-Markdown/markdown)-based static site generator, including [Zensical](https://github.com/zensical/zensical) and [MkDocs](https://www.mkdocs.org/).

## Features

- Transform fenced code blocks with language `wavedrom` into WaveDrom script tags or embedded SVG
- Support for `pymdownx.superfences` custom fences
- Optional SVG embedding at build time (no JavaScript required)

## Installation

```bash
pip install zensical-wavedrom-plugin
```

## Usage

In your Markdown files:

````markdown
```wavedrom
{ signal: [
  { name: "clk",  wave: "p....." },
  { name: "data", wave: "x.345x" }
] }
```
````

## Configuration

### Zensical

Add to your `zensical.toml`:

#### Default mode (JavaScript rendering)

In default mode, WaveDrom code blocks are transformed into `<script type="WaveDrom">` tags and the WaveDrom JavaScript library processes them on page load.

```toml
[project]
extra_javascript = [
  "https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/skins/default.js",
  "https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/wavedrom.min.js"
]
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
```

#### Embed SVG mode

When `embed_svg = true` is set, WaveDrom diagrams are rendered to SVG at build time. This means no JavaScript is required on the client side.

```toml
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
embed_svg = true
```

#### Pymdownx Integration

This plugin integrates with `pymdownx.superfences` to provide custom fence support when `pymdownx` is used instead of `fenced_code`.

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "wavedrom", class = "wavedrom", format = "zensical_wavedrom_plugin.extension.fence_wavedrom_format" }
]
[project.markdown_extensions.wavedrom]
```

### MkDocs

Since this plugin is registered as a `markdown.extensions` entry point, it also works with [MkDocs](https://www.mkdocs.org/).

#### Default mode (MkDocs)

```yaml
markdown_extensions:
  - wavedrom:
      embed_svg: false

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/skins/default.js
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/wavedrom.min.js
```

#### Embed SVG mode (MkDocs)

```yaml
markdown_extensions:
  - wavedrom:
      embed_svg: true
```

#### Pymdownx Integration (MkDocs)

```yaml
markdown_extensions:
  - pymdownx.superfences:
      custom_fences:
        - name: wavedrom
          class: wavedrom
          format: !!python/name:zensical_wavedrom_plugin.extension.fence_wavedrom_format
  - wavedrom:
      embed_svg: false

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/skins/default.js
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/wavedrom.min.js
```

## License

This project is licensed under the MIT License.
