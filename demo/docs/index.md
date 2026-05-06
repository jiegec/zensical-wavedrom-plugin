# WaveDrom Plugin Demo

Welcome to the **zensical-wavedrom-plugin** demo project! This project demonstrates how to render [WaveDrom](https://wavedrom.com/) digital timing diagrams in your Zensical documentation.

## What is WaveDrom?

WaveDrom is a digital timing diagram rendering engine that uses a simple JSON-based format to describe waveforms, bitfields, and registers.

## Default Mode

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


## Embed SVG Mode

When `embed_svg = true` is set, WaveDrom diagrams are rendered to SVG at build time. This means no JavaScript is required on the client side.

!!! note

    To enable embed SVG mode, set `embed_svg = true` in your `zensical.toml`:

    ```toml
    [project.markdown_extensions.wavedrom]
    embed_svg = true
    ```

## Pymdownx Integration

This plugin integrates with `pymdownx.superfences` to provide custom fence support. The integration is already configured in this demo's `zensical.toml`:

```toml
[project.markdown_extensions.pymdownx.superfences]
custom_fences = [
  { name = "wavedrom", class = "wavedrom", format = "zensical_wavedrom_plugin.extension.fence_wavedrom_format" }
]
[project.markdown_extensions.wavedrom]
```

## Learn More

- [WaveDrom Tutorial](https://wavedrom.com/tutorial.html)
- [WaveDrom GitHub](https://github.com/wavedrom/wavedrom)
- [zensical-wavedrom-plugin on GitHub](https://github.com/jiegec/zensical-wavedrom-plugin)
