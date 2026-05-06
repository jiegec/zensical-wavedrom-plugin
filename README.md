# Zensical WaveDrom Plugin

A Zensical extension for rendering [WaveDrom](https://wavedrom.com/) diagrams in Markdown.

This is a port of the [mkdocs-wavedrom-plugin](https://github.com/kuri65536/mkdocs-wavedrom-plugin) (or, my [maintained fork](https://github.com/jiegec/mkdocs-wavedrom-plugin)) for the Zensical static site generator.

## Features

- Transform fenced code blocks with language `wavedrom` into WaveDrom script tags or embedded SVG
- Support for `pymdownx.superfences` custom fences
- Optional SVG embedding at build time (no JavaScript required)

## Installation

```bash
pip install zensical-wavedrom-plugin
```

## Configuration

Add to your `zensical.toml`:

### Default mode (JavaScript rendering)

In default mode, WaveDrom code blocks are transformed into `<script type="WaveDrom">` tags and the WaveDrom JavaScript library processes them on page load.

```toml
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
```

### Embed SVG mode

When `embed_svg = true` is set, WaveDrom diagrams are rendered to SVG at build time. This means no JavaScript is required on the client side.

```toml
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
embed_svg = true
```

### Pymdownx Integration

This plugin integrates with `pymdownx.superfences` to provide custom fence support when `pymdownx` is used instead of `fenced_code`.

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "wavedrom", class = "wavedrom", format = "zensical_wavedrom_plugin.extension.fence_wavedrom_format" }
]
[project.markdown_extensions.wavedrom]
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

## License

This project is licensed under the MIT License.
