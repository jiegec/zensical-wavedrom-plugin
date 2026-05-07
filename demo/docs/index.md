# WaveDrom Plugin Demo

Welcome to the **zensical-wavedrom-plugin** demo project! This project demonstrates how to render [WaveDrom](https://wavedrom.com/) digital timing diagrams in your documentation. Source code of this demo can be found in [the repo](https://github.com/jiegec/zensical-wavedrom-plugin/tree/master/demo).

Since this plugin is registered as a `markdown.extensions` entry point, it works with any [Python-Markdown](https://github.com/Python-Markdown/markdown)-based static site generator, including [Zensical](https://github.com/jiegec/zensical) and [MkDocs](https://www.mkdocs.org/).

## What is WaveDrom?

WaveDrom is a digital timing diagram rendering engine that uses a simple JSON-based format to describe waveforms, bitfields, and registers.

## Usage

Write fenced code blocks with language `wavedrom`:

### Simple Clock and Data

````markdown
```wavedrom
{ signal: [
  { name: "clk",  wave: "p....." },
  { name: "data", wave: "x.345x" }
] }
```
````

```wavedrom
{ signal: [
  { name: "clk",  wave: "p....." },
  { name: "data", wave: "x.345x" }
] }
```

### Multiple Signals

````markdown
```wavedrom
{ signal: [
  { name: "Alfa", wave: "01.zx=ud.23.45" },
  { name: "Bravo", wave: "lh.lh.lh.lh.lh" },
  { name: "Charlie", wave: "x3.=.x3.=.x3.=" },
  { name: "Delta", wave: "z..0.1.z.=z..0" }
] }
```
````

```wavedrom
{ signal: [
  { name: "Alfa", wave: "01.zx=ud.23.45" },
  { name: "Bravo", wave: "lh.lh.lh.lh.lh" },
  { name: "Charlie", wave: "x3.=.x3.=.x3.=" },
  { name: "Delta", wave: "z..0.1.z.=z..0" }
] }
```

## Zensical Configuration

### Default Mode

In default mode, WaveDrom code blocks are transformed into `<script type="WaveDrom">` tags and the WaveDrom JavaScript library processes them on page load. Add to your `zensical.toml`:

```toml
[project]
extra_javascript = [
  "https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/skins/default.js",
  "https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/wavedrom.min.js"
]
[project.markdown_extensions.fenced_code]
[project.markdown_extensions.wavedrom]
```

### Embed SVG Mode

When `embed_svg = true` is set, WaveDrom diagrams are rendered to SVG at build time. This means no JavaScript is required on the client side.

!!! note

    To enable embed SVG mode, set `embed_svg = true` in your `zensical.toml`:

    ```toml
    [project.markdown_extensions.wavedrom]
    embed_svg = true
    ```

### Pymdownx Integration

This plugin integrates with `pymdownx.superfences` to provide custom fence support. The integration is already configured in this demo's `zensical.toml`:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "wavedrom", class = "wavedrom", format = "zensical_wavedrom_plugin.extension.fence_wavedrom_format" }
]
[project.markdown_extensions.wavedrom]
```

## MkDocs Configuration

Since this plugin is registered as a `markdown.extensions` entry point, it also works with [MkDocs](https://www.mkdocs.org/). Here is the equivalent `mkdocs.yml` for each mode shown above.

### Default Mode (MkDocs)

```yaml
markdown_extensions:
  - wavedrom:
      embed_svg: false

extra_javascript:
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/skins/default.js
  - https://cdnjs.cloudflare.com/ajax/libs/wavedrom/3.5.0/wavedrom.min.js
```

### Embed SVG Mode (MkDocs)

```yaml
markdown_extensions:
  - wavedrom:
      embed_svg: true
```

### Pymdownx Integration (MkDocs)

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

## Learn More

- [WaveDrom Tutorial](https://wavedrom.com/tutorial.html)
- [WaveDrom GitHub](https://github.com/wavedrom/wavedrom)
- [zensical-wavedrom-plugin on GitHub](https://github.com/jiegec/zensical-wavedrom-plugin)
