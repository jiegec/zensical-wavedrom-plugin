from __future__ import annotations

import pytest
from markdown import Markdown

from zensical_wavedrom_plugin.extension import (
    WavedromExtension,
    WavedromPostprocessor,
    _escape,
    fence_wavedrom_format,
)


class TestEscape:
    def test_ampersand(self) -> None:
        assert _escape("a&b") == "a&amp;b"

    def test_lt(self) -> None:
        assert _escape("a<b") == "a&lt;b"

    def test_gt(self) -> None:
        assert _escape("a>b") == "a&gt;b"

    def test_combined(self) -> None:
        assert _escape("a&b<c>d") == "a&amp;b&lt;c&gt;d"

    def test_no_special(self) -> None:
        assert _escape("abc") == "abc"

    def test_empty(self) -> None:
        assert _escape("") == ""


class TestFenceWavedromFormat:
    def test_basic(self) -> None:
        source = '{ signal: [{ name: "A", wave: "01" }] }'
        result = fence_wavedrom_format(source, "wavedrom", "", {}, None)
        assert (
            result
            == '<script type="WaveDrom">{ signal: [{ name: "A", wave: "01" }] }</script>'
        )

    def test_escapes_special_chars(self) -> None:
        source = '{ signal: [{ name: "A<B", wave: "01" }] }'
        result = fence_wavedrom_format(source, "wavedrom", "", {}, None)
        assert "A&lt;B" in result


class TestDefaultMode:
    """Default mode: code blocks are replaced with <script type="WaveDrom">
    and ProcessAll() is appended."""

    @pytest.fixture
    def md(self) -> Markdown:
        return Markdown(extensions=["fenced_code", WavedromExtension()])

    def test_code_replaced_with_script(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert 'type="WaveDrom"' in result
        assert "<code" not in result

    def test_pre_removed(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<pre>" not in result

    def test_process_all_appended(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "WaveDrom.ProcessAll()" in result

    def test_content_preserved(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert '{ signal: [{ name: "A", wave: "01" }] }' in result

    def test_no_wavedrom_no_script(self, md: Markdown) -> None:
        source = "# Hello\n\nThis is plain text."
        result = md.convert(source)
        assert "WaveDrom.ProcessAll()" not in result


class TestEmbedSvgMode:
    """Embed SVG mode: wavedrom JSON is rendered to SVG at build time,
    no JavaScript required."""

    @pytest.fixture
    def md(self) -> Markdown:
        return Markdown(
            extensions=[
                "fenced_code",
                WavedromExtension(embed_svg=True),
            ]
        )

    def test_renders_svg(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<svg" in result
        assert '<script type="WaveDrom">' not in result

    def test_no_process_all(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "WaveDrom.ProcessAll()" not in result

    def test_svg_has_signal_name(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "Alfa", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<svg" in result
        assert "Alfa" in result


class TestPymdownxMode:
    """Pymdownx mode: script tags inserted by superfences are kept,
    ProcessAll() is appended."""

    @pytest.fixture
    def md(self) -> Markdown:
        return Markdown(
            extensions=[
                "pymdownx.superfences",
                WavedromExtension(),
            ],
            extension_configs={
                "pymdownx.superfences": {
                    "custom_fences": [
                        {
                            "name": "wavedrom",
                            "class": "wavedrom",
                            "format": fence_wavedrom_format,
                        }
                    ]
                }
            },
        )

    def test_wavedrom_script_preserved(self, md: Markdown) -> None:
        source = (
            '```wavedrom\n{ signal: [{ name: "Alfa", wave: "01.zx=ud.23.45" }] }\n```'
        )
        result = md.convert(source)
        assert 'type="WaveDrom"' in result
        assert '{ signal: [{ name: "Alfa", wave: "01.zx=ud.23.45" }] }' in result

    def test_no_svg_embedded(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<svg" not in result

    def test_process_all_present(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "WaveDrom.ProcessAll()" in result


class TestPymdownxEmbedSvgMode:
    """Pymdownx + embed SVG: superfences script tags are rendered to SVG."""

    @pytest.fixture
    def md(self) -> Markdown:
        return Markdown(
            extensions=[
                "pymdownx.superfences",
                WavedromExtension(embed_svg=True),
            ],
            extension_configs={
                "pymdownx.superfences": {
                    "custom_fences": [
                        {
                            "name": "wavedrom",
                            "class": "wavedrom",
                            "format": fence_wavedrom_format,
                        }
                    ]
                }
            },
        )

    def test_svg_embedded(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<svg" in result

    def test_no_wavedrom_script(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert 'type="WaveDrom"' not in result

    def test_no_process_all(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "A", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "WaveDrom.ProcessAll()" not in result

    def test_svg_has_signal_name(self, md: Markdown) -> None:
        source = '```wavedrom\n{ signal: [{ name: "Alfa", wave: "01" }] }\n```'
        result = md.convert(source)
        assert "<svg" in result
        assert "Alfa" in result


class TestPostprocessorUnit:
    """Unit tests for WavedromPostprocessor."""

    def test_processes_code_block(self) -> None:
        md = Markdown(extensions=["fenced_code"])
        post = WavedromPostprocessor(md, embed_svg=False)
        md.htmlStash.rawHtmlBlocks = [
            '<pre><code class="language-wavedrom">'
            '{ signal: [{ name: "A", wave: "01" }] }'
            "</code></pre>"
        ]
        result = post.run("<p>Hello</p>")
        assert 'type="WaveDrom"' in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" not in result
        assert post.found_wavedrom is True

    def test_no_code_block_no_change(self) -> None:
        md = Markdown(extensions=["fenced_code"])
        post = WavedromPostprocessor(md, embed_svg=False)
        md.htmlStash.rawHtmlBlocks = [
            '<pre><code class="language-python">' "print('hello')" "</code></pre>"
        ]
        result = post.run("<p>Hello</p>")
        assert md.htmlStash.rawHtmlBlocks[0] == (
            '<pre><code class="language-python">' "print('hello')" "</code></pre>"
        )
        assert "WaveDrom.ProcessAll()" not in result
        assert post.found_wavedrom is False

    def test_embed_svg_no_script(self) -> None:
        md = Markdown(extensions=["fenced_code"])
        post = WavedromPostprocessor(md, embed_svg=True)
        md.htmlStash.rawHtmlBlocks = [
            '<pre><code class="language-wavedrom">'
            '{ signal: [{ name: "A", wave: "01" }] }'
            "</code></pre>"
        ]
        result = post.run("<p>Hello</p>")
        assert "<svg" in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" not in result
        assert post.found_wavedrom is True

    def test_processes_script_tag(self) -> None:
        md = Markdown()
        post = WavedromPostprocessor(md, embed_svg=False)
        md.htmlStash.rawHtmlBlocks = [
            '<script type="WaveDrom">'
            '{ signal: [{ name: "A", wave: "01" }] }'
            "</script>"
        ]
        result = post.run("<p>Hello</p>")
        assert 'type="WaveDrom"' in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" not in result
        assert post.found_wavedrom is True

    def test_embed_svg_replaces_script(self) -> None:
        md = Markdown()
        post = WavedromPostprocessor(md, embed_svg=True)
        md.htmlStash.rawHtmlBlocks = [
            '<script type="WaveDrom">'
            '{ signal: [{ name: "A", wave: "01" }] }'
            "</script>"
        ]
        result = post.run("<p>Hello</p>")
        assert "<svg" in md.htmlStash.rawHtmlBlocks[0]
        assert 'type="WaveDrom"' not in md.htmlStash.rawHtmlBlocks[0]
        assert "WaveDrom.ProcessAll()" not in result
        assert post.found_wavedrom is True
