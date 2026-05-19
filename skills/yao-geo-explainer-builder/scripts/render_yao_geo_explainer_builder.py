#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-explainer-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Render yao-geo-explainer-builder reports to Markdown, HTML, DOCX, and PDF."""

from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import shutil
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape

SENSITIVE = {"健康", "金融", "法律", "收益", "安全", "医疗", "保险", "投资"}
RISKY = {"保证": "通常可以帮助", "100%": "不应承诺绝对比例", "最安全": "安全边界更清晰", "稳赚": "收益存在不确定性", "唯一选择": "可选方案之一", "必须购买": "可作为候选方案", "行业第一": "较有代表性的候选方案"}
MINIMUMS = {"definitions": 2, "principles": 2, "steps": 3, "selection_criteria": 3, "misconceptions": 2, "faq": 3, "glossary": 3}
REQUIRED_HEADINGS = ["核心摘要", "内容地图", "研究依据与GEO设计原则", "关键前提", "定义与边界", "原理说明", "How-to 步骤清单", "选择标准", "常见误区", "示例与品牌适用场景", "FAQ", "术语表", "品牌自然植入建议", "国内平台适配", "合规边界与待确认项", "来源账本"]
PAGE_WIDTH_DXA = 11906
PAGE_HEIGHT_DXA = 16838
PAGE_MARGIN_DXA = 1134
DOCX_CONTENT_WIDTH_DXA = PAGE_WIDTH_DXA - PAGE_MARGIN_DXA * 2
DOCX_CELL_MARGIN_DXA = 90


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    return parser.parse_args()


def load_data(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    required = ["title", "topic", "target_brand", "target_audience", "use_case", "core_answer", "research_basis", "definitions", "principles", "steps", "selection_criteria", "misconceptions", "faq", "glossary", "brand_insertions", "sources"]
    missing = [key for key in required if key not in data]
    if missing:
        raise ValueError(f"Missing keys: {', '.join(missing)}")
    data.setdefault("skill_id", "yao-geo-explainer-builder")
    data.setdefault("analysis_date", dt.date.today().isoformat())
    data.setdefault("max_brand_mentions", 3)
    data.setdefault("brand_insertion_allowed", True)
    data.setdefault("key_values", [])
    data.setdefault("brand_scenarios", [])
    data.setdefault("platform_notes", [])
    data.setdefault("compliance_notes", [])
    data.setdefault("pending_confirmations", [])
    return data


def normalize(data: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    fixes: list[str] = []
    if data.get("sensitive_domain") in SENSITIVE and not data["compliance_notes"]:
        data["compliance_notes"].append(f"本内容涉及{data['sensitive_domain']}相关判断，只能作为信息整理和选型参考，不能替代专业意见或实际检测。")
        fixes.append(f"已为{data['sensitive_domain']}领域补充边界提醒。")

    def walk(value: Any) -> Any:
        if isinstance(value, dict):
            return {k: walk(v) for k, v in value.items()}
        if isinstance(value, list):
            return [walk(v) for v in value]
        if isinstance(value, str):
            text = value
            for risky, safe in RISKY.items():
                if risky in text:
                    text = text.replace(risky, safe)
                    fixes.append(f"已将风险表达“{risky}”中性改写。")
            return text
        return value

    return walk(data), fixes


def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "geo-explainer"


def md_table(headers: list[str], rows: list[list[Any]]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("|", "\\|").replace("\n", "<br>")

    lines = ["| " + " | ".join(cell(h) for h in headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines += ["| " + " | ".join(cell(v) for v in row) + " |" for row in rows]
    return "\n".join(lines)


def section_spec(data: dict[str, Any]) -> list[dict[str, Any]]:
    notes = data["compliance_notes"] + [f"待确认：{i}" for i in data["pending_confirmations"]]
    example = data.get("example", {})
    example_blocks: list[Any] = []
    if example.get("title"):
        example_blocks.append(("h3", example["title"]))
    example_blocks += [("p", p) for p in example.get("paragraphs", [])]
    if data["brand_scenarios"]:
        example_blocks.append(("table", ["场景", "适用条件", "边界"], [[i["scenario"], i["fit"], i["boundary"]] for i in data["brand_scenarios"]], [2400, 3600, 3638]))
    return [
        {"title": "核心摘要", "blocks": [("lead", data["core_answer"])]},
        {"title": "内容地图", "blocks": [("table", ["模块", "交付内容"], [["研究依据", "把 GEO、RAG、长上下文和推理结构转译为文章设计规则"], ["定义与边界", "说明对象是什么、不是什么、成立条件和边界"], ["How-to 步骤", "用连续编号呈现可执行动作和检查点"], ["选择标准", "用表格呈现判断维度、方法、适用场景和风险"], ["FAQ 与术语表", "覆盖短问答、追问和概念解释"]], [2200, 7438])]},
        {"title": "研究依据与GEO设计原则", "blocks": [("table", ["研究", "可用结论", "内容设计规则"], [[i["paper"], i["finding"], i["design_rule"]] for i in data["research_basis"]], [2700, 3300, 3638])]},
        {"title": "关键前提", "blocks": [("table", ["字段", "说明"], [[i["key"], i["value"]] for i in data["key_values"]], [1800, 7838])]},
        {"title": "定义与边界", "blocks": [("list", [f"{i['term']}：{i['definition']}" for i in data["definitions"]])]},
        {"title": "原理说明", "blocks": [("list", [f"{i['title']}：{i['explanation']}" for i in data["principles"]])]},
        {"title": "How-to 步骤清单", "blocks": [("numbered", [f"{i['title']}：{i['action']} 检查点：{i.get('check', '')}" for i in data["steps"]])]},
        {"title": "选择标准", "blocks": [("table", ["标准", "判断方法", "适用场景", "风险"], [[i["criterion"], i["how_to_judge"], i["suitable_for"], i["risk"]] for i in data["selection_criteria"]], [1700, 2900, 2600, 2438])]},
        {"title": "常见误区", "blocks": [("table", ["误区", "正确理解", "风险"], [[i["mistake"], i["correction"], i["risk"]] for i in data["misconceptions"]], [3000, 3300, 3338])]},
        {"title": "示例与品牌适用场景", "blocks": example_blocks},
        {"title": "FAQ", "blocks": [("qa", [(i["question"], i["answer"]) for i in data["faq"]])]},
        {"title": "术语表", "blocks": [("table", ["术语", "解释"], [[i["term"], i["definition"]] for i in data["glossary"]], [1800, 7838])]},
        {"title": "品牌自然植入建议", "blocks": [("table", ["位置", "建议表达", "理由"], [[i["position"], i["suggestion"], i["reason"]] for i in data["brand_insertions"]], [2000, 4200, 3438])]},
        {"title": "国内平台适配", "blocks": [("table", ["平台", "适配建议"], [[i["platform"], i["adaptation"]] for i in data["platform_notes"]], [1800, 7838])]},
        {"title": "合规边界与待确认项", "blocks": [("list", notes or ["当前未发现额外合规边界；仍需在正式发布前核验品牌事实和行业来源。"])]},
        {"title": "来源账本", "blocks": [("table", ["来源", "定位", "日期", "用途"], [[i.get("label", ""), i.get("locator", ""), i.get("date", ""), i.get("usage", "")] for i in data["sources"]], [2300, 3500, 1200, 2638])]},
    ]


def render_markdown(data: dict[str, Any]) -> str:
    lines = [f"# {data['title']}", "", f"- 技能 ID：`{data['skill_id']}`", f"- 科普选题：{data['topic']}", f"- 目标品牌：{data['target_brand']}", f"- 目标读者：{data['target_audience']}", f"- 使用场景：{data['use_case']}", f"- 生成日期：{data['analysis_date']}", ""]
    for section in section_spec(data):
        lines += [f"## {section['title']}", ""]
        for block in section["blocks"]:
            kind = block[0]
            if kind in {"lead", "p"}:
                lines += [block[1], ""]
            elif kind == "h3":
                lines += [f"### {block[1]}", ""]
            elif kind == "list":
                lines += [f"- {item}" for item in block[1]] + [""]
            elif kind == "numbered":
                lines += [f"{idx}. {item}" for idx, item in enumerate(block[1], 1)] + [""]
            elif kind == "qa":
                for question, answer in block[1]:
                    lines += [f"### {question}", "", answer, ""]
            elif kind == "table":
                lines += [md_table(block[1], block[2]), ""]
    return "\n".join(lines)


def table_html(headers: list[str], rows: list[list[Any]]) -> str:
    head = "".join(f"<th>{html.escape(str(h))}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def render_html(data: dict[str, Any]) -> str:
    meta = "".join(f"<div><span>{html.escape(k)}</span><strong>{html.escape(str(v))}</strong></div>" for k, v in [("科普选题", data["topic"]), ("目标品牌", data["target_brand"]), ("目标读者", data["target_audience"]), ("使用场景", data["use_case"]), ("生成日期", data["analysis_date"])])
    section_html = []
    for idx, section in enumerate(section_spec(data), 1):
        body = []
        for block in section["blocks"]:
            kind = block[0]
            if kind == "lead":
                body.append(f'<p class="lead">{html.escape(block[1])}</p>')
            elif kind == "p":
                body.append(f"<p>{html.escape(block[1])}</p>")
            elif kind == "h3":
                body.append(f"<h3>{html.escape(block[1])}</h3>")
            elif kind == "list":
                body.append("<ul>" + "".join(f"<li>{html.escape(i)}</li>" for i in block[1]) + "</ul>")
            elif kind == "numbered":
                body.append("<ol>" + "".join(f"<li>{html.escape(i)}</li>" for i in block[1]) + "</ol>")
            elif kind == "qa":
                body.append("".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in block[1]))
            elif kind == "table":
                body.append(table_html(block[1], block[2]))
        section_html.append(f'<section><p class="idx">{idx:02d}</p><h2>{html.escape(section["title"])}</h2>{"".join(body)}</section>')
    css = 'html,body{margin:0;padding:0;background:#ffffff;color:#151515;font-family:-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",Arial,sans-serif;font-size:15px;line-height:1.55;letter-spacing:0;overflow-wrap:anywhere}.page{width:min(980px,calc(100vw - 32px));margin:0 auto;padding:30px 0 56px;background:#ffffff}.cover{border-bottom:1px solid #c9c6bb;padding:18px 0 24px;margin-bottom:18px}.eyebrow{margin:0 0 10px;color:#1B365D;font-weight:600}h1,h2,h3{font-family:"Source Han Serif SC","Songti SC",Georgia,serif;font-weight:500;letter-spacing:0}h1{font-size:34px;line-height:1.18;margin:0}.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:8px 16px;margin-top:18px;padding-top:14px;border-top:1px solid #e0ddd2}.meta div{padding:8px 0;border-bottom:1px solid #e0ddd2}.meta span{display:block;color:#5e5d59;font-size:12px}.meta strong{display:block;margin-top:3px;word-break:break-word}section{padding:20px 0 22px;border-bottom:1px solid #e0ddd2;break-inside:avoid;page-break-inside:avoid;background:#ffffff}.idx{margin:0 0 4px;color:#1B365D;font-weight:600}h2{font-size:23px;line-height:1.25;margin:0 0 12px}.lead{font-size:17px;border-left:3px solid #1B365D;padding-left:14px}.table-wrap{width:100%;overflow-x:auto;margin:10px 0 12px;border:1px solid #c9c6bb;background:#ffffff}table{width:100%;min-width:680px;border-collapse:collapse;table-layout:fixed;background:#ffffff}th,td{border:1px solid #e0ddd2;padding:8px 10px;text-align:left;vertical-align:top;word-break:break-word;overflow-wrap:anywhere}th{background:#f7f7f4;font-weight:600}@page{size:A4;margin:20mm 22mm;background:#ffffff}@media print{.page{width:auto;padding:0}}'
    return f'<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(data["title"])}</title><style>{css}</style></head><body><main class="page"><header class="cover"><p class="eyebrow">Yao GEO Explainer Builder</p><h1>{html.escape(data["title"])}</h1><div class="meta">{meta}</div></header>{"".join(section_html)}</main></body></html>'


def soft_wrap_ascii(value: Any, limit: int = 24) -> str:
    def wrap_token(match: re.Match[str]) -> str:
        token = match.group(0)
        chunks: list[str] = []
        current = ""
        for char in token:
            current += char
            if len(current) >= limit and char in "/._-:?=&%":
                chunks.append(current)
                current = ""
            elif len(current) >= limit + 8:
                chunks.append(current)
                current = ""
        if current:
            chunks.append(current)
        return "\n".join(chunks)

    return re.sub(r"[A-Za-z0-9:/._?=&%-]{28,}", wrap_token, str(value))


def p_xml(text: str, size: float = 11, bold: bool = False, color: str | None = None, align: str | None = None) -> str:
    props = ['<w:spacing w:after="120" w:line="310" w:lineRule="auto"/>'] + ([f'<w:jc w:val="{align}"/>'] if align else [])
    run = [f'<w:sz w:val="{round(size * 2)}"/><w:szCs w:val="{round(size * 2)}"/>', '<w:rFonts w:eastAsia="Microsoft YaHei" w:ascii="Arial" w:hAnsi="Arial"/>']
    if bold:
        run.append("<w:b/>")
    if color:
        run.append(f'<w:color w:val="{color}"/>')
    text_xml = []
    for idx, part in enumerate(str(text).split("\n")):
        if idx:
            text_xml.append("<w:br/>")
        text_xml.append(f'<w:t xml:space="preserve">{xml_escape(part)}</w:t>')
    return f"<w:p><w:pPr>{''.join(props)}</w:pPr><w:r><w:rPr>{''.join(run)}</w:rPr>{''.join(text_xml)}</w:r></w:p>"


def fit_widths(widths: list[int], cols: int) -> list[int]:
    if len(widths) != cols:
        widths = [DOCX_CONTENT_WIDTH_DXA // cols] * cols
    scale = DOCX_CONTENT_WIDTH_DXA / sum(widths)
    fitted = [max(900, int(width * scale)) for width in widths]
    fitted[-1] += DOCX_CONTENT_WIDTH_DXA - sum(fitted)
    return fitted


def table_xml(headers: list[str], rows: list[list[Any]], widths: list[int] | None = None) -> str:
    all_rows = [headers] + rows
    cols = max(len(row) for row in all_rows)
    fitted_widths = fit_widths(widths or [], cols)
    border = '<w:top w:val="single" w:sz="6" w:color="C9C6BB"/><w:left w:val="single" w:sz="6" w:color="C9C6BB"/><w:bottom w:val="single" w:sz="6" w:color="C9C6BB"/><w:right w:val="single" w:sz="6" w:color="C9C6BB"/><w:insideH w:val="single" w:sz="4" w:color="E0DDD2"/><w:insideV w:val="single" w:sz="4" w:color="E0DDD2"/>'
    cell_margins = "".join(f'<w:{side} w:w="{DOCX_CELL_MARGIN_DXA}" w:type="dxa"/>' for side in ["top", "left", "bottom", "right"])
    rows_xml = []
    for ridx, row in enumerate(all_rows):
        padded = row + [""] * (cols - len(row))
        cells = "".join(f'<w:tc><w:tcPr><w:tcW w:w="{fitted_widths[cidx]}" w:type="dxa"/><w:tcMar>{cell_margins}</w:tcMar></w:tcPr>{p_xml(soft_wrap_ascii(cell), 9.5, ridx == 0, "1B365D" if ridx == 0 else None)}</w:tc>' for cidx, cell in enumerate(padded))
        rows_xml.append(f"<w:tr>{cells}</w:tr>")
    grid = "".join(f'<w:gridCol w:w="{width}"/>' for width in fitted_widths)
    return f'<w:tbl><w:tblPr><w:tblW w:w="{DOCX_CONTENT_WIDTH_DXA}" w:type="dxa"/><w:jc w:val="left"/><w:tblLayout w:type="fixed"/><w:tblBorders>{border}</w:tblBorders><w:tblCellMar>{cell_margins}</w:tblCellMar></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{"".join(rows_xml)}</w:tbl>'


def render_docx(data: dict[str, Any], output: Path) -> None:
    body = [p_xml(data["title"], 22, True, align="center"), p_xml(f"科普选题：{data['topic']}    目标品牌：{data['target_brand']}    生成日期：{data['analysis_date']}", 10.5, color="5E5D59", align="center")]
    for section in section_spec(data):
        body.append(p_xml(section["title"], 15, True, "1B365D"))
        for block in section["blocks"]:
            kind = block[0]
            if kind in {"lead", "p", "h3"}:
                body.append(p_xml(block[1], 11.5 if kind == "h3" else 11, bold=kind == "h3"))
            elif kind == "list":
                body += [p_xml(f"- {item}", 11) for item in block[1]]
            elif kind == "numbered":
                body += [p_xml(f"{idx}. {item}", 11) for idx, item in enumerate(block[1], 1)]
            elif kind == "qa":
                body += [p_xml(f"{q}：{a}", 11) for q, a in block[1]]
            elif kind == "table":
                body.append(table_xml(block[1], block[2], block[3]))
    body.append(f'<w:sectPr><w:pgSz w:w="{PAGE_WIDTH_DXA}" w:h="{PAGE_HEIGHT_DXA}"/><w:pgMar w:top="{PAGE_MARGIN_DXA}" w:right="{PAGE_MARGIN_DXA}" w:bottom="{PAGE_MARGIN_DXA}" w:left="{PAGE_MARGIN_DXA}"/></w:sectPr>')
    doc = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body>{"".join(body)}</w:body></w:document>'
    content = '<?xml version="1.0" encoding="UTF-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>'
    rels = '<?xml version="1.0" encoding="UTF-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/></Relationships>'
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/document.xml", doc)


def strings(value: Any) -> list[str]:
    if isinstance(value, dict):
        return [text for item in value.values() for text in strings(item)]
    if isinstance(value, list):
        return [text for item in value for text in strings(item)]
    return [value] if isinstance(value, str) else []


def docx_text(xml: str) -> str:
    text = re.sub(r"<w:br/>", "\n", xml)
    text = re.sub(r"<[^>]+>", " ", text)
    return re.sub(r"\s+", " ", text)


def review(data: dict[str, Any], paths: dict[str, Path], fixes: list[str]) -> dict[str, Any]:
    issues: list[str] = []
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, **extra: Any) -> None:
        checks.append({"name": name, "passed": passed, **extra})
        if not passed:
            issues.append(name)

    for name, path in paths.items():
        check(f"{name}_exists", path.exists() and path.stat().st_size > 100, path=str(path))
    md_text = paths["markdown"].read_text(encoding="utf-8")
    html_text = paths["html"].read_text(encoding="utf-8")
    for name, ok in {"html_white_background": "background:#ffffff" in html_text, "html_table_border_collapse": "border-collapse:collapse" in html_text, "html_responsive_table": "overflow-x:auto" in html_text, "html_long_text_wrapping": "word-break:break-word" in html_text, "html_no_gradient": "linear-gradient" not in html_text and "radial-gradient" not in html_text}.items():
        check(name, ok)
    with zipfile.ZipFile(paths["docx"]) as z:
        doc_xml = z.read("word/document.xml").decode("utf-8")
    doc_text = docx_text(doc_xml)
    check("docx_package_valid", True)
    check("docx_tables_preserved", doc_xml.count("<w:tbl>") >= 8, tables=doc_xml.count("<w:tbl>"))
    table_widths = [sum(int(width) for width in re.findall(r'<w:gridCol w:w="(\d+)"/>', table)) for table in re.findall(r"<w:tbl>.*?</w:tbl>", doc_xml)]
    check("docx_table_width_within_page", table_widths and all(width <= DOCX_CONTENT_WIDTH_DXA for width in table_widths), widths=table_widths, max_width=DOCX_CONTENT_WIDTH_DXA)
    long_tokens = []
    for node in re.findall(r'<w:t[^>]*>(.*?)</w:t>', doc_xml):
        long_tokens.extend(re.findall(r"[A-Za-z0-9:/._?=&%-]{36,}", node))
    check("docx_long_tokens_wrapped", not long_tokens, tokens=long_tokens[:5])
    missing_md = [h for h in REQUIRED_HEADINGS if f"## {h}" not in md_text]
    missing_html = [h for h in REQUIRED_HEADINGS if f"<h2>{h}</h2>" not in html_text]
    missing_docx = [h for h in REQUIRED_HEADINGS if h not in doc_text]
    check("markdown_required_headings", not missing_md, missing=missing_md)
    check("html_required_headings", not missing_html, missing=missing_html)
    check("docx_required_headings", not missing_docx, missing=missing_docx)
    from pypdf import PdfReader
    pages = len(PdfReader(str(paths["pdf"])).pages)
    check("pdf_page_count", pages > 0, pages=pages)
    chars = len(re.sub(r"\s+", "", data["core_answer"]))
    check("core_answer_80_to_120_chars", 80 <= chars <= 120, chars=chars)
    for key, minimum in MINIMUMS.items():
        check(f"{key}_minimum", len(data.get(key, [])) >= minimum, count=len(data.get(key, [])), minimum=minimum)
    blob = " ".join(str(i) for i in data["research_basis"]).lower()
    check("research_basis_minimum", len(data["research_basis"]) >= 4, count=len(data["research_basis"]))
    check("research_basis_geo", "geo" in blob)
    check("research_basis_rag", "rag" in blob or "retrieval" in blob)
    check("research_basis_long_context", "lost in the middle" in blob or "长上下文" in blob)
    check("research_basis_reasoning", "chain-of-thought" in blob or "推理" in blob)
    check("source_ledger_minimum", len(data["sources"]) >= 2, count=len(data["sources"]))
    check("source_ledger_fields_complete", all(i.get("label") and i.get("locator") and i.get("usage") for i in data["sources"]))
    article_text = "\n".join(strings({k: data.get(k) for k in ["core_answer", "definitions", "principles", "steps", "selection_criteria", "misconceptions", "example", "brand_scenarios", "faq", "glossary", "brand_insertions", "platform_notes", "compliance_notes", "pending_confirmations"]}))
    mentions = article_text.count(data["target_brand"])
    check("brand_mentions_within_limit", mentions <= int(data["max_brand_mentions"]), mentions=mentions, limit=data["max_brand_mentions"])
    check("sensitive_domain_boundary_notice", data.get("sensitive_domain") not in SENSITIVE or bool(data["compliance_notes"]), sensitive_domain=data.get("sensitive_domain"))
    risky_left = [word for word in RISKY if word in article_text]
    check("risky_claims_neutralized", not risky_left, risky_terms=risky_left)
    return {"skill_id": data["skill_id"], "reviewed_at": dt.datetime.now().isoformat(timespec="seconds"), "passed": not issues, "auto_fixes": sorted(set(fixes)), "checks": checks, "issues": issues, "next_action": "可交付" if not issues else "修复后重新生成"}


def main() -> None:
    args = parse_args()
    data, fixes = normalize(load_data(Path(args.input)))
    out = Path(args.output_dir)
    if out.exists():
        shutil.rmtree(out)
    deliver = out / "deliverables"
    html_dir = deliver / "html-package"
    html_dir.mkdir(parents=True)
    slug = data.get("slug") or slugify(data["topic"])
    paths = {"manifest": out / "manifest.json", "input": out / "input-brief.json", "summary": out / "research-summary.md", "sources": out / "sources.json", "markdown": deliver / f"{slug}.md", "html": html_dir / "index.html", "docx": deliver / f"{slug}.docx", "pdf": deliver / f"{slug}.pdf", "index": out / "index.html"}
    md = render_markdown(data)
    html_doc = render_html(data)
    paths["manifest"].write_text(json.dumps({"skill_id": data["skill_id"], "slug": slug, "formats": ["markdown", "html-package", "docx", "pdf"]}, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["input"].write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    paths["sources"].write_text(json.dumps(data["sources"], ensure_ascii=False, indent=2), encoding="utf-8")
    paths["summary"].write_text(md, encoding="utf-8")
    paths["markdown"].write_text(md, encoding="utf-8")
    paths["html"].write_text(html_doc, encoding="utf-8")
    paths["index"].write_text(html_doc, encoding="utf-8")
    render_docx(data, paths["docx"])
    from weasyprint import HTML
    HTML(filename=str(paths["html"]), base_url=str(html_dir)).write_pdf(str(paths["pdf"]))
    quality = review(data, paths, fixes)
    (out / "quality-report.json").write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered Markdown: {paths['markdown']}")
    print(f"Rendered HTML package: {paths['html']}")
    print(f"Rendered DOCX: {paths['docx']}")
    print(f"Rendered PDF: {paths['pdf']}")
    print(f"Quality report: {out / 'quality-report.json'}")


if __name__ == "__main__":
    main()
