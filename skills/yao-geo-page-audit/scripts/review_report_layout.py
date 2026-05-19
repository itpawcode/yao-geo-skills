#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-page-audit
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Review yao-geo-page-audit report artifacts for Word/PDF right-overflow risk."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


WORD_NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def check_markdown(path: Path) -> dict:
    wide_tables = []
    if path.exists():
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if line.startswith("|"):
                columns = line.count("|") - 1
                if columns > 5:
                    wide_tables.append({"line": line_no, "columns": columns})
    return {"exists": path.exists(), "wide_table_lines_gt5": wide_tables}


def check_docx(path: Path) -> dict:
    result = {
        "exists": path.exists(),
        "max_table_columns": 0,
        "visible_url_tokens_gt40": [],
        "zip_ok": False,
    }
    if not path.exists():
        return result

    with ZipFile(path) as archive:
        bad_file = archive.testzip()
        result["zip_ok"] = bad_file is None
        root = ET.fromstring(archive.read("word/document.xml"))

    for table in root.findall(".//w:tbl", WORD_NS):
        rows = table.findall(".//w:tr", WORD_NS)
        table_columns = max((len(row.findall("./w:tc", WORD_NS)) for row in rows), default=0)
        result["max_table_columns"] = max(result["max_table_columns"], table_columns)

    for text_node in root.findall(".//w:t", WORD_NS):
        text = text_node.text or ""
        result["visible_url_tokens_gt40"].extend(re.findall(r"https?://\S{41,}", text))

    return result


def check_pdf(path: Path, render_dir: Path | None) -> dict:
    result = {
        "exists": path.exists(),
        "rendered_pages": 0,
        "right_edge_issues": [],
        "pdftoppm_available": shutil.which("pdftoppm") is not None,
    }
    if not path.exists() or render_dir is None or not result["pdftoppm_available"]:
        return result

    render_dir.mkdir(parents=True, exist_ok=True)
    prefix = render_dir / "page"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "110", str(path), str(prefix)],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        from PIL import Image
    except Exception:
        return result

    pages = sorted(render_dir.glob("page-*.png"))
    result["rendered_pages"] = len(pages)
    for image_path in pages:
        image = Image.open(image_path).convert("L")
        width, height = image.size
        strip = image.crop((width - 18, 0, width, height))
        histogram = strip.histogram()
        dark_ratio = sum(histogram[:245]) / (18 * height)
        if dark_ratio > 0.002:
            result["right_edge_issues"].append({"page": image_path.name, "dark_ratio": dark_ratio})
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--md", required=True)
    parser.add_argument("--docx", required=True)
    parser.add_argument("--pdf", required=True)
    parser.add_argument("--render-dir")
    parser.add_argument("--output")
    args = parser.parse_args()

    render_dir = Path(args.render_dir) if args.render_dir else None
    report = {
        "markdown": check_markdown(Path(args.md)),
        "docx": check_docx(Path(args.docx)),
        "pdf": check_pdf(Path(args.pdf), render_dir),
    }
    report["open_issues"] = []
    if report["markdown"]["wide_table_lines_gt5"]:
        report["open_issues"].append("markdown_table_too_wide")
    if report["docx"]["max_table_columns"] > 5:
        report["open_issues"].append("docx_table_too_wide")
    if report["docx"]["visible_url_tokens_gt40"]:
        report["open_issues"].append("docx_visible_url_too_long")
    if report["pdf"]["right_edge_issues"]:
        report["open_issues"].append("pdf_right_edge_content")
    if not report["docx"]["zip_ok"]:
        report["open_issues"].append("docx_zip_invalid")

    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 1 if report["open_issues"] else 0


if __name__ == "__main__":
    sys.exit(main())
