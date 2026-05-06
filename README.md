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

```toml
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
```

### Embed SVG mode

```toml
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
embed_svg = true
```

### Pymdownx Integration

```yaml
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
