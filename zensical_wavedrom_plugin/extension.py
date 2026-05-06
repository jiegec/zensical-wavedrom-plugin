from __future__ import annotations

from typing import TYPE_CHECKING

import wavedrom
from bs4 import BeautifulSoup
from markdown import Extension
from markdown.postprocessors import Postprocessor

if TYPE_CHECKING:
    from markdown import Markdown

_WAVEDROM_INIT_SCRIPT = (
    "<script>"
    'window.addEventListener("load", function() '
    "{WaveDrom.ProcessAll();});"
    "</script>"
)


def _escape(txt: str) -> str:
    """Basic html escaping."""
    txt = txt.replace("&", "&amp;")
    txt = txt.replace("<", "&lt;")
    txt = txt.replace(">", "&gt;")
    return txt


def fence_wavedrom_format(
    source: str,
    language: str,
    class_name: str,
    options: dict,
    md: Markdown,
    **kwargs: object,
) -> str:
    """Format wavedrom fence for pymdownx.superfences."""
    return '<script type="WaveDrom">%s</script>' % (_escape(source))


class WavedromPostprocessor(Postprocessor):
    """Transform wavedrom blocks and append initialization script."""

    def __init__(self, md: Markdown, embed_svg: bool) -> None:
        super().__init__(md)
        self.embed_svg = embed_svg
        self.found_wavedrom = False
        self._script_appended = False

    def run(self, text: str) -> str:
        for i, raw in enumerate(self.md.htmlStash.rawHtmlBlocks):
            self.md.htmlStash.rawHtmlBlocks[i] = self._process_html(raw)

        if self.found_wavedrom and not self.embed_svg and not self._script_appended:
            # Append init script to the last stashed block to avoid
            # corrupting heading text when TOC's render_inner_html
            # runs postprocessors on fragments.
            if self.md.htmlStash.rawHtmlBlocks:
                last = self.md.htmlStash.rawHtmlBlocks[-1]
                self.md.htmlStash.rawHtmlBlocks[-1] = (
                    last + "\n" + _WAVEDROM_INIT_SCRIPT
                )
                self._script_appended = True
            else:
                text = text + "\n" + _WAVEDROM_INIT_SCRIPT
                self._script_appended = True
        return text

    def _process_html(self, html: str) -> str:
        # for pymdownx,
        # handle <script type="WaveDrom"></script> form
        html = self._process_scripts(html)
        # handle <code class="language-wavedrom"></code> form
        return self._process_code_blocks(html)

    def _process_code_blocks(self, html: str) -> str:
        if "language-wavedrom" not in html:
            return html

        soup = BeautifulSoup(html, "html.parser")
        modified = False

        for pre in soup.find_all("pre"):
            code = pre.find("code")
            if code is None:
                continue
            classes = code.get("class", [])
            if isinstance(classes, str):
                classes = classes.split()
            if "language-wavedrom" not in classes:
                continue

            self.found_wavedrom = True
            text = code.get_text()

            if self.embed_svg:
                try:
                    svg = wavedrom.render(text).tostring()
                except Exception:
                    continue
                svg_soup = BeautifulSoup(svg, "html.parser")
                svg_element = svg_soup.find()
                if svg_element:
                    pre.replace_with(svg_element)
            else:
                script = soup.new_tag("script")
                script["type"] = "WaveDrom"
                script.string = text
                pre.replace_with(script)
            modified = True

        return str(soup) if modified else html

    def _process_scripts(self, html: str) -> str:
        if "WaveDrom" not in html:
            return html

        soup = BeautifulSoup(html, "html.parser")
        modified = False

        for script in soup.find_all("script", type="WaveDrom"):
            self.found_wavedrom = True
            if self.embed_svg:
                text = script.get_text()
                try:
                    svg = wavedrom.render(text).tostring()
                except Exception:
                    continue
                svg_soup = BeautifulSoup(svg, "html.parser")
                svg_element = svg_soup.find()
                if svg_element:
                    script.replace_with(svg_element)
                    modified = True

        return str(soup) if modified else html


class WavedromExtension(Extension):
    """Markdown extension for WaveDrom diagrams.

    This extension transforms wavedrom code blocks into either embedded SVG
    or WaveDrom script tags, and appends the initialization script when
    needed.
    """

    def __init__(self, **kwargs: object) -> None:
        self.config = {
            "embed_svg": [
                False,
                "Embed SVG inline instead of using JavaScript",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md: Markdown) -> None:
        md.registerExtension(self)

        embed_svg = bool(self.getConfig("embed_svg", False))

        postprocessor = WavedromPostprocessor(md, embed_svg)
        md.postprocessors.register(postprocessor, "wavedrom", 31)
