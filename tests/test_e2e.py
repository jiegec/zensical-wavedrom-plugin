from __future__ import annotations

import os
import shutil
import subprocess

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))


def _build_project(project_name: str) -> str:
    project_dir = os.path.join(TESTS_DIR, project_name)
    site_dir = os.path.join(project_dir, "site")
    if os.path.exists(site_dir):
        shutil.rmtree(site_dir)
    subprocess.run(
        ["zensical", "build"],
        cwd=project_dir,
        check=True,
        capture_output=True,
        text=True,
    )
    return os.path.join(site_dir, "index.html")


def _read_file(path: str) -> str:
    with open(path, encoding="utf-8") as f:
        return f.read()


class TestDefaultMode:
    """Default mode: fenced code blocks replaced with script tags."""

    def test_html_contains_wavedrom_script(self) -> None:
        f = _build_project("e2e_default")
        content = _read_file(f)
        assert 'type="WaveDrom"' in content

    def test_no_wavedrom_svg(self) -> None:
        f = _build_project("e2e_default")
        content = _read_file(f)
        # WaveDrom content should be in script tags, not SVG
        assert 'type="WaveDrom"' in content

    def test_process_all_present(self) -> None:
        f = _build_project("e2e_default")
        content = _read_file(f)
        assert "WaveDrom.ProcessAll()" in content

    def test_no_code_block_remains(self) -> None:
        f = _build_project("e2e_default")
        content = _read_file(f)
        assert "<code" not in content
        assert "<pre>" not in content


class TestEmbedSvgMode:
    """Embed SVG mode: diagrams rendered to inline SVG."""

    def test_svg_embedded(self) -> None:
        f = _build_project("e2e_embed_svg")
        content = _read_file(f)
        assert "<svg" in content

    def test_no_wavedrom_script(self) -> None:
        f = _build_project("e2e_embed_svg")
        content = _read_file(f)
        assert 'type="WaveDrom"' not in content

    def test_no_process_all(self) -> None:
        f = _build_project("e2e_embed_svg")
        content = _read_file(f)
        assert "WaveDrom.ProcessAll()" not in content

    def test_svg_has_signal_name(self) -> None:
        f = _build_project("e2e_embed_svg")
        content = _read_file(f)
        assert "Alfa" in content


class TestPymdownxMode:
    """Pymdownx mode: superfences script tags preserved."""

    def test_wavedrom_script_preserved(self) -> None:
        f = _build_project("e2e_pymdownx")
        content = _read_file(f)
        assert 'type="WaveDrom"' in content
        assert '{ signal: [{ name: "Alfa", wave: "01.zx=ud.23.45" }] }' in content

    def test_no_wavedrom_svg(self) -> None:
        f = _build_project("e2e_pymdownx")
        content = _read_file(f)
        # WaveDrom content should be in script tags, not SVG
        assert 'type="WaveDrom"' in content

    def test_process_all_present(self) -> None:
        f = _build_project("e2e_pymdownx")
        content = _read_file(f)
        assert "WaveDrom.ProcessAll()" in content


class TestPymdownxEmbedSvgMode:
    """Pymdownx + embed SVG: script tags rendered to SVG."""

    def test_svg_embedded(self) -> None:
        f = _build_project("e2e_pymdownx_embed_svg")
        content = _read_file(f)
        assert "<svg" in content

    def test_no_wavedrom_script(self) -> None:
        f = _build_project("e2e_pymdownx_embed_svg")
        content = _read_file(f)
        assert 'type="WaveDrom"' not in content

    def test_no_process_all(self) -> None:
        f = _build_project("e2e_pymdownx_embed_svg")
        content = _read_file(f)
        assert "WaveDrom.ProcessAll()" not in content

    def test_svg_has_signal_name(self) -> None:
        f = _build_project("e2e_pymdownx_embed_svg")
        content = _read_file(f)
        assert "Alfa" in content
