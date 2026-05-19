#!/usr/bin/env python3
"""Generate four-format GEO execution roadmap reports."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as xml_escape

import markdown
from weasyprint import HTML


REQUIRED_SECTIONS = [
    "执行摘要",
    "诊断承接",
    "北极星指标",
    "六个项目包",
    "90 天执行路线图",
    "国内平台差异化动作",
    "角色分工与验收指标",
    "监测闭环计划",
    "风险预案",
    "来源台账",
    "自检记录",
]

REQUIRED_PACKAGES = ["页面技术", "内容矩阵", "标题体系", "知识库", "外部证据", "监测闭环"]
REQUIRED_PLATFORMS = ["DeepSeek", "豆包", "千问", "Kimi", "元宝"]


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def clean(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return "；".join(clean(item) for item in value if clean(item))
    return str(value).strip()


def md_cell(value: Any) -> str:
    return clean(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: list[str], rows: list[list[Any]]) -> str:
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        padded = row + [""] * (len(headers) - len(row))
        output.append("| " + " | ".join(md_cell(item) for item in padded[: len(headers)]) + " |")
    return "\n".join(output)


def rows(items: Any, fields: list[tuple[str, str]]) -> list[list[str]]:
    return [[clean(item.get(key, "")) for key, _ in fields] for item in as_list(items) if isinstance(item, dict)]


def heads(fields: list[tuple[str, str]]) -> list[str]:
    return [label for _, label in fields]


def task_rows(project: dict[str, Any]) -> list[list[str]]:
    result = []
    for task in as_list(project.get("tasks")):
        if not isinstance(task, dict):
            continue
        result.append(
            [
                clean(task.get("task")),
                clean(task.get("steps")),
                clean(task.get("owner")),
                clean(task.get("deliverable")),
                clean(task.get("acceptance")),
                clean(task.get("dependency")),
            ]
        )
    return result


def role_rows(data: dict[str, Any]) -> list[list[str]]:
    result = []
    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        for task in as_list(project.get("tasks")):
            if not isinstance(task, dict):
                continue
            result.append(
                [
                    clean(project.get("name")),
                    clean(task.get("owner")),
                    clean(task.get("task")),
                    clean(task.get("deliverable")),
                    clean(task.get("acceptance")),
                ]
            )
    return result


def render_markdown(data: dict[str, Any]) -> str:
    report = data.get("report", {})
    lines = [f"# {clean(report.get('title', 'GEO 综合实施方案'))}", ""]
    lines += [
        table(
            ["字段", "内容"],
            [
                ["测试对象", report.get("company", "")],
                ["官网", report.get("website", "")],
                ["测试场景", report.get("scenario", "")],
                ["目标平台", data.get("target_platforms", REQUIRED_PLATFORMS)],
                ["生成日期", report.get("date", datetime.now().strftime("%Y-%m-%d"))],
                ["输出语言", report.get("language", "中文简体")],
            ],
        ),
        "",
        "## 执行摘要",
    ]
    lines += [f"- {clean(item)}" for item in as_list(data.get("executive_summary"))]
    lines += ["", "## 诊断承接"]
    lines += [
        table(
            ["诊断发现", "实施转译"],
            rows(data.get("diagnosis_bridge", {}).get("items"), [("finding", "诊断发现"), ("translation", "实施转译")]),
        ),
        "",
        "## 北极星指标",
    ]
    metric_fields = [("metric", "指标"), ("baseline", "基线"), ("target_30d", "30 天目标"), ("target_60d", "60 天目标"), ("target_90d", "90 天目标"), ("owner", "负责人")]
    lines += [table(heads(metric_fields), rows(data.get("north_star_metrics"), metric_fields)), "", "## 六个项目包"]

    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        lines += [
            "",
            f"### {clean(project.get('name'))}",
            "",
            table(
                ["字段", "内容"],
                [
                    ["目标", project.get("goal", "")],
                    ["输入", project.get("inputs", "")],
                    ["负责人", project.get("owner", "")],
                    ["交付物", project.get("deliverables", "")],
                    ["验收指标", project.get("acceptance_metrics", "")],
                    ["依赖关系", project.get("dependencies", "")],
                ],
            ),
            "",
            table(["任务", "步骤", "负责人", "交付物", "验收指标", "依赖"], task_rows(project)),
        ]

    roadmap_fields = [("phase", "阶段"), ("objective", "目标"), ("key_actions", "关键动作"), ("deliverables", "交付物"), ("acceptance", "验收口径")]
    platform_fields = [("platform", "平台"), ("focus", "执行重点"), ("question_clusters", "目标问题簇"), ("actions", "具体动作"), ("assets", "资产要求"), ("acceptance", "验收指标"), ("risk", "风险提示")]
    monitoring_fields = [("item", "监测项"), ("method", "方法"), ("cadence", "频率"), ("owner", "负责人"), ("acceptance", "验收指标")]
    risk_fields = [("risk", "风险"), ("trigger", "触发信号"), ("mitigation", "预案"), ("owner", "负责人"), ("acceptance", "验收指标")]
    source_fields = [("id", "编号"), ("claim", "支持断言"), ("source", "来源"), ("url", "URL")]

    lines += [
        "",
        "## 90 天执行路线图",
        table(heads(roadmap_fields), rows(data.get("roadmap"), roadmap_fields)),
        "",
        "## 国内平台差异化动作",
        table(heads(platform_fields), rows(data.get("platform_actions"), platform_fields)),
        "",
        "## 角色分工与验收指标",
        table(["项目包", "责任角色", "任务", "交付物", "验收指标"], role_rows(data)),
        "",
        "## 监测闭环计划",
        table(heads(monitoring_fields), rows(data.get("monitoring_plan"), monitoring_fields)),
        "",
        "## 风险预案",
        table(heads(risk_fields), rows(data.get("risk_plan"), risk_fields)),
        "",
        "## 来源台账",
        table(heads(source_fields), rows(data.get("source_basis"), source_fields)),
        "",
        "## 自检记录",
        table(
            ["检查项", "结果"],
            [
                ["四格式文件", "生成后由 quality-report.json 复核"],
                ["平台覆盖", "DeepSeek、豆包、千问、Kimi、元宝均有差异动作"],
                ["项目包覆盖", "页面技术、内容矩阵、标题体系、知识库、外部证据、监测闭环均有任务和验收指标"],
                ["承诺边界", "不承诺平台必定引用，只提升可发现性、可验证性和可抽取性"],
            ],
        ),
        "",
    ]
    return "\n".join(lines)


def render_html(markdown_text: str, title: str) -> str:
    body = markdown.markdown(markdown_text, extensions=["tables", "toc"])
    css = """
    :root {
      --paper: #ffffff;
      --ink: #172033;
      --muted: #647084;
      --line: #d9dee8;
      --soft: #f6f8fb;
      --accent: #1d4f91;
    }
    * { box-sizing: border-box; }
    html, body { margin: 0; padding: 0; background: #ffffff; color: var(--ink); }
    body {
      font-family: "Source Han Serif SC", "Noto Serif CJK SC", "Songti SC", "PingFang SC", "Microsoft YaHei", serif;
      font-size: 15px;
      line-height: 1.72;
    }
    .page { max-width: 1120px; margin: 0 auto; padding: 42px 42px 64px; background: #ffffff; }
    h1 { margin: 0 0 18px; padding-bottom: 16px; border-bottom: 2px solid var(--ink); font-size: 30px; line-height: 1.22; letter-spacing: 0; }
    h2 { margin: 34px 0 14px; padding-top: 4px; border-top: 1px solid var(--line); font-size: 21px; line-height: 1.35; letter-spacing: 0; }
    h3 { margin: 24px 0 10px; font-size: 17px; line-height: 1.42; letter-spacing: 0; }
    p { margin: 0 0 10px; }
    ul { margin: 8px 0 16px 1.2em; padding: 0; }
    li { margin: 4px 0; }
    table {
      width: 100%;
      border-collapse: collapse;
      table-layout: fixed;
      margin: 10px 0 22px;
      break-inside: avoid;
      background: #ffffff;
    }
    th, td {
      border: 1px solid var(--line);
      padding: 8px 9px;
      vertical-align: top;
      word-break: break-word;
      overflow-wrap: anywhere;
    }
    th { background: var(--soft); color: var(--ink); font-weight: 700; text-align: left; }
    code { white-space: pre-wrap; word-break: break-word; }
    @page { size: A4; margin: 16mm 14mm; }
    @media print {
      body { font-size: 11px; background: #ffffff; }
      .page { max-width: none; padding: 0; }
      h1 { font-size: 23px; }
      h2 { font-size: 16px; margin-top: 22px; }
      h3 { font-size: 13px; }
      th, td { padding: 5px 6px; }
      table { page-break-inside: avoid; }
    }
    """
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<style>{css}</style>
</head>
<body><main class="page">{body}</main></body>
</html>
"""


DOCX_PAGE_WIDTH = 11906
DOCX_PAGE_HEIGHT = 16838
DOCX_MARGIN = 1134
DOCX_CONTENT_WIDTH = DOCX_PAGE_WIDTH - (DOCX_MARGIN * 2)


def word_breaks(text: str) -> str:
    value = clean(text)
    for token in ["/", ".", "-", "_", "?", "&", "=", "#", ":"]:
        value = value.replace(token, token + "\u200b")
    return value


def w_text(text: str) -> str:
    lines = word_breaks(text).splitlines() or [""]
    chunks = []
    for index, line in enumerate(lines):
        if index:
            chunks.append("<w:br/>")
        chunks.append(f'<w:t xml:space="preserve">{xml_escape(line)}</w:t>')
    return "".join(chunks)


def w_p(
    text: str,
    style: str | None = None,
    *,
    font_size: int | None = None,
    before: int = 0,
    after: int = 120,
    keep_next: bool = False,
) -> str:
    p_props = []
    if style:
        p_props.append(f'<w:pStyle w:val="{style}"/>')
    if keep_next:
        p_props.append("<w:keepNext/>")
    p_props.append(f'<w:spacing w:before="{before}" w:after="{after}" w:line="300" w:lineRule="auto"/>')
    r_props = []
    if font_size:
        r_props.append(f'<w:sz w:val="{font_size}"/><w:szCs w:val="{font_size}"/>')
    rpr = f"<w:rPr>{''.join(r_props)}</w:rPr>" if r_props else ""
    return f"<w:p><w:pPr>{''.join(p_props)}</w:pPr><w:r>{rpr}{w_text(text)}</w:r></w:p>"


def normalize_widths(widths: list[int]) -> list[int]:
    if not widths:
        return []
    total = sum(widths)
    scaled = [max(420, round(width * DOCX_CONTENT_WIDTH / total)) for width in widths]
    diff = DOCX_CONTENT_WIDTH - sum(scaled)
    scaled[-1] += diff
    return scaled


def w_table(headers: list[str], body: list[list[str]], widths: list[int] | None = None, *, font_size: int = 17) -> str:
    if widths is None:
        widths = [DOCX_CONTENT_WIDTH // len(headers)] * len(headers)
    widths = normalize_widths(widths)

    def cell(text: str, width: int, header: bool = False) -> str:
        shade = '<w:shd w:fill="F6F8FB"/>' if header else ""
        bold = "<w:b/>" if header else ""
        size = max(font_size, 16)
        return (
            "<w:tc>"
            f'<w:tcPr><w:tcW w:w="{width}" w:type="dxa"/>{shade}<w:vAlign w:val="center"/></w:tcPr>'
            '<w:p><w:pPr><w:spacing w:before="0" w:after="60" w:line="280" w:lineRule="auto"/></w:pPr>'
            f'<w:r><w:rPr>{bold}<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>{w_text(clean(text))}</w:r>'
            "</w:p></w:tc>"
        )

    rows_xml = ["<w:tr>" + "".join(cell(item, widths[i], True) for i, item in enumerate(headers)) + "</w:tr>"]
    for row in body:
        padded = row + [""] * (len(headers) - len(row))
        rows_xml.append("<w:tr>" + "".join(cell(clean(item), widths[i]) for i, item in enumerate(padded[: len(headers)])) + "</w:tr>")
    grid = "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{width}"/>' for width in widths) + "</w:tblGrid>"
    borders = (
        f'<w:tblPr><w:tblW w:w="{DOCX_CONTENT_WIDTH}" w:type="dxa"/>'
        '<w:tblLayout w:type="fixed"/>'
        '<w:tblCellMar><w:top w:w="90" w:type="dxa"/><w:left w:w="120" w:type="dxa"/><w:bottom w:w="90" w:type="dxa"/><w:right w:w="120" w:type="dxa"/></w:tblCellMar>'
        '<w:tblBorders>'
        '<w:top w:val="single" w:sz="4" w:color="D9DEE8"/>'
        '<w:left w:val="single" w:sz="4" w:color="D9DEE8"/>'
        '<w:bottom w:val="single" w:sz="4" w:color="D9DEE8"/>'
        '<w:right w:val="single" w:sz="4" w:color="D9DEE8"/>'
        '<w:insideH w:val="single" w:sz="4" w:color="D9DEE8"/>'
        '<w:insideV w:val="single" w:sz="4" w:color="D9DEE8"/>'
        "</w:tblBorders></w:tblPr>"
    )
    return "<w:tbl>" + borders + grid + "".join(rows_xml) + "</w:tbl>"


def kv_table(items: list[list[Any]], label_width: int = 1850) -> str:
    return w_table(["字段", "内容"], [[clean(a), clean(b)] for a, b in items], [label_width, DOCX_CONTENT_WIDTH - label_width])


def write_docx(data: dict[str, Any], output_path: Path) -> None:
    report = data.get("report", {})
    parts: list[str] = []
    parts.append(w_p(clean(report.get("title", "GEO 综合实施方案")), "Title", after=220, keep_next=True))
    parts.append(
        kv_table(
            [
                ["测试对象", report.get("company", "")],
                ["官网", report.get("website", "")],
                ["测试场景", report.get("scenario", "")],
                ["目标平台", data.get("target_platforms", REQUIRED_PLATFORMS)],
                ["生成日期", report.get("date", datetime.now().strftime("%Y-%m-%d"))],
                ["输出语言", report.get("language", "中文简体")],
            ],
            1650,
        )
    )

    parts.append(w_p("执行摘要", "Heading1", before=260, keep_next=True))
    for index, item in enumerate(as_list(data.get("executive_summary")), start=1):
        parts.append(w_p(f"{index}. {clean(item)}", after=90))

    parts.append(w_p("诊断承接", "Heading1", before=260, keep_next=True))
    parts.append(w_table(["诊断发现", "实施转译"], rows(data.get("diagnosis_bridge", {}).get("items"), [("finding", "诊断发现"), ("translation", "实施转译")]), [4550, 5088]))

    parts.append(w_p("北极星指标", "Heading1", before=260, keep_next=True))
    for metric in as_list(data.get("north_star_metrics")):
        if not isinstance(metric, dict):
            continue
        parts.append(w_p(clean(metric.get("metric")), "Heading2", before=120, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["基线", metric.get("baseline", "")],
                    ["30 天目标", metric.get("target_30d", "")],
                    ["60 天目标", metric.get("target_60d", "")],
                    ["90 天目标", metric.get("target_90d", "")],
                    ["负责人", metric.get("owner", "")],
                ],
                1700,
            )
        )

    parts.append(w_p("六个项目包", "Heading1", before=260, keep_next=True))
    for project in as_list(data.get("project_packages")):
        if not isinstance(project, dict):
            continue
        parts.append(w_p(clean(project.get("name")), "Heading2", before=160, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["目标", project.get("goal", "")],
                    ["输入", project.get("inputs", "")],
                    ["负责人", project.get("owner", "")],
                    ["交付物", project.get("deliverables", "")],
                    ["验收指标", project.get("acceptance_metrics", "")],
                    ["依赖关系", project.get("dependencies", "")],
                ],
                1650,
            )
        )
        compact_tasks = []
        for task in as_list(project.get("tasks")):
            if not isinstance(task, dict):
                continue
            task_text = clean(task.get("task"))
            steps = clean(task.get("steps"))
            if steps:
                task_text = f"{task_text}\n步骤：{steps}"
            compact_tasks.append([task_text, clean(task.get("owner")), clean(task.get("deliverable")), clean(task.get("acceptance"))])
        parts.append(w_table(["任务与步骤", "负责人", "交付物", "验收指标"], compact_tasks, [3250, 1600, 2050, 2738], font_size=16))

    roadmap_fields = [("phase", "阶段"), ("objective", "目标"), ("key_actions", "关键动作"), ("deliverables", "交付物"), ("acceptance", "验收口径")]
    parts.append(w_p("90 天执行路线图", "Heading1", before=260, keep_next=True))
    parts.append(w_table(heads(roadmap_fields), rows(data.get("roadmap"), roadmap_fields), [1200, 1800, 2900, 1800, 1938], font_size=16))

    parts.append(w_p("国内平台差异化动作", "Heading1", before=260, keep_next=True))
    for platform in as_list(data.get("platform_actions")):
        if not isinstance(platform, dict):
            continue
        parts.append(w_p(clean(platform.get("platform")), "Heading2", before=120, keep_next=True))
        parts.append(
            kv_table(
                [
                    ["执行重点", platform.get("focus", "")],
                    ["目标问题簇", platform.get("question_clusters", "")],
                    ["具体动作", platform.get("actions", "")],
                    ["资产要求", platform.get("assets", "")],
                    ["验收指标", platform.get("acceptance", "")],
                    ["风险提示", platform.get("risk", "")],
                ],
                1650,
            )
        )

    parts.append(w_p("角色分工与验收指标", "Heading1", before=260, keep_next=True))
    parts.append(w_table(["项目包", "责任角色", "任务", "交付物", "验收指标"], role_rows(data), [1300, 1700, 2200, 2100, 2338], font_size=16))

    monitoring_fields = [("item", "监测项"), ("method", "方法"), ("cadence", "频率"), ("owner", "负责人"), ("acceptance", "验收指标")]
    parts.append(w_p("监测闭环计划", "Heading1", before=260, keep_next=True))
    monitoring_rows = [[r[0], f"{r[1]}\n频率：{r[2]}", r[3], r[4]] for r in rows(data.get("monitoring_plan"), monitoring_fields)]
    parts.append(w_table(["监测项", "方法与频率", "负责人", "验收指标"], monitoring_rows, [1450, 4200, 1450, 2538], font_size=16))

    risk_fields = [("risk", "风险"), ("trigger", "触发信号"), ("mitigation", "预案"), ("owner", "负责人"), ("acceptance", "验收指标")]
    parts.append(w_p("风险预案", "Heading1", before=260, keep_next=True))
    risk_rows = [[f"{r[0]}\n触发：{r[1]}", r[2], r[3], r[4]] for r in rows(data.get("risk_plan"), risk_fields)]
    parts.append(w_table(["风险与触发", "预案", "负责人", "验收指标"], risk_rows, [2500, 3700, 1350, 2088], font_size=16))

    parts.append(w_p("来源台账", "Heading1", before=260, keep_next=True))
    for source in as_list(data.get("source_basis")):
        if not isinstance(source, dict):
            continue
        parts.append(w_p(clean(source.get("id", "来源")), "Heading2", before=120, keep_next=True))
        parts.append(kv_table([["支持断言", source.get("claim", "")], ["来源", source.get("source", "")], ["URL", source.get("url", "")]], 1650))

    parts.append(w_p("自检记录", "Heading1", before=260, keep_next=True))
    parts.append(
        kv_table(
            [
                ["四格式文件", "生成后由 quality-report.json 复核"],
                ["平台覆盖", "DeepSeek、豆包、千问、Kimi、元宝均有差异动作"],
                ["项目包覆盖", "页面技术、内容矩阵、标题体系、知识库、外部证据、监测闭环均有任务和验收指标"],
                ["承诺边界", "不承诺平台必定引用，只提升可发现性、可验证性和可抽取性"],
                ["Word 排版", "使用固定页宽、固定列宽、固定表格布局和分组窄表，避免宽表向右溢出"],
            ],
            1650,
        )
    )

    document_xml = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>{''.join(parts)}<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1134" w:right="1134" w:bottom="1134" w:left="1134"/></w:sectPr></w:body>
</w:document>"""
    styles_xml = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:style w:type="paragraph" w:styleId="Normal"><w:name w:val="Normal"/><w:rPr><w:rFonts w:ascii="Times New Roman" w:eastAsia="宋体"/><w:sz w:val="21"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Title"><w:name w:val="Title"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="36"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:rPr><w:b/><w:rFonts w:ascii="Times New Roman" w:eastAsia="黑体"/><w:sz w:val="24"/></w:rPr></w:style>
</w:styles>"""
    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>"""
    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>"""
    word_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as docx:
        docx.writestr("[Content_Types].xml", content_types)
        docx.writestr("_rels/.rels", rels)
        docx.writestr("word/_rels/document.xml.rels", word_rels)
        docx.writestr("word/document.xml", document_xml)
        docx.writestr("word/styles.xml", styles_xml)


def check_docx(path: Path) -> tuple[bool, list[str]]:
    try:
        with zipfile.ZipFile(path, "r") as docx:
            text = docx.read("word/document.xml").decode("utf-8")
    except Exception as exc:
        return False, [str(exc)]
    missing = [section for section in REQUIRED_SECTIONS if section not in text]
    return not missing, missing


def check_docx_table_geometry(path: Path) -> tuple[bool, dict[str, Any]]:
    with zipfile.ZipFile(path, "r") as docx:
        text = docx.read("word/document.xml").decode("utf-8")
    tables = re.findall(r"<w:tbl>.*?</w:tbl>", text, flags=re.DOTALL)
    oversized: list[int] = []
    missing_grid: list[int] = []
    for index, table_xml in enumerate(tables, start=1):
        grid_cols = [int(value) for value in re.findall(r'<w:gridCol w:w="(\d+)"', table_xml)]
        if not grid_cols:
            missing_grid.append(index)
            continue
        if sum(grid_cols) > DOCX_CONTENT_WIDTH:
            oversized.append(index)
    detail = {
        "table_count": len(tables),
        "auto_table_width_count": text.count('w:type="auto"'),
        "tbl_grid_count": text.count("<w:tblGrid>"),
        "tc_width_count": text.count("<w:tcW"),
        "content_width_dxa": DOCX_CONTENT_WIDTH,
        "missing_grid_tables": missing_grid,
        "oversized_tables": oversized,
    }
    passed = bool(tables) and detail["auto_table_width_count"] == 0 and not missing_grid and not oversized
    return passed, detail


def review(data: dict[str, Any], paths: dict[str, Path], md: str, html_text: str) -> dict[str, Any]:
    checks = []

    def add(name: str, passed: bool, detail: Any) -> None:
        checks.append({"name": name, "pass": bool(passed), "detail": detail})

    add(
        "four_format_files_exist",
        all(paths[key].exists() and paths[key].stat().st_size > 1024 for key in ["markdown", "html", "docx", "pdf"]),
        {key: {"exists": paths[key].exists(), "size": paths[key].stat().st_size if paths[key].exists() else 0} for key in ["markdown", "html", "docx", "pdf"]},
    )
    add("markdown_required_sections", all(f"## {section}" in md for section in REQUIRED_SECTIONS), REQUIRED_SECTIONS)
    package_names = [clean(item.get("name")) for item in as_list(data.get("project_packages")) if isinstance(item, dict)]
    add("six_project_packages_present", len(package_names) >= 6 and all(name in "".join(package_names) for name in REQUIRED_PACKAGES), package_names)
    platforms = [clean(item.get("platform")) for item in as_list(data.get("platform_actions")) if isinstance(item, dict)]
    add("cn_platforms_present", all(name in platforms for name in REQUIRED_PLATFORMS), platforms)
    rr = role_rows(data)
    add("role_and_acceptance_metrics_present", len(rr) >= 12 and all(row[1] and row[4] for row in rr), {"role_rows": len(rr)})
    lower_html = html_text.lower()
    add("html_no_dark_or_gradient_tokens", "gradient" not in lower_html and "rgba(" not in lower_html and "background: #0" not in lower_html, "white editorial layout")
    add("html_layout_guards", all(token in html_text for token in ["background: #ffffff", "border-collapse: collapse", "table-layout: fixed", "overflow-wrap: anywhere"]), "table and overflow guards")
    docx_ok, docx_missing = check_docx(paths["docx"])
    add("docx_valid_and_contains_sections", docx_ok, {"missing": docx_missing})
    geometry_ok, geometry_detail = check_docx_table_geometry(paths["docx"])
    add("docx_fixed_table_geometry", geometry_ok, geometry_detail)
    pdf_header = b""
    if paths["pdf"].exists():
        pdf_header = paths["pdf"].read_bytes()[:4]
    add("pdf_valid", pdf_header == b"%PDF" and paths["pdf"].stat().st_size > 10000, {"header": pdf_header.decode("latin1"), "size": paths["pdf"].stat().st_size if paths["pdf"].exists() else 0})
    add("no_platform_citation_guarantee", "不承诺平台必定引用" in md, "explicit guarantee boundary present")
    return {"overall_pass": all(item["pass"] for item in checks), "generated_at": datetime.now().isoformat(timespec="seconds"), "checks": checks}


def render(input_path: Path, output_dir: Path) -> dict[str, Any]:
    data = json.loads(input_path.read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    basename = data.get("report", {}).get("output_basename", input_path.stem)
    title = data.get("report", {}).get("title", "GEO 综合实施方案")
    paths = {
        "markdown": output_dir / f"{basename}.md",
        "html": output_dir / f"{basename}.html",
        "docx": output_dir / f"{basename}.docx",
        "pdf": output_dir / f"{basename}.pdf",
        "quality": output_dir / "quality-report.json",
    }
    md = render_markdown(data)
    html_text = render_html(md, title)
    paths["markdown"].write_text(md, encoding="utf-8")
    paths["html"].write_text(html_text, encoding="utf-8")
    write_docx(data, paths["docx"])
    HTML(string=html_text, base_url=str(output_dir)).write_pdf(str(paths["pdf"]))
    quality = review(data, paths, md, html_text)
    quality["files"] = {key: str(path) for key, path in paths.items()}
    paths["quality"].write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding="utf-8")
    return quality


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--no-fail", action="store_true")
    args = parser.parse_args()
    quality = render(args.input, args.output_dir)
    print(json.dumps(quality, ensure_ascii=False, indent=2))
    return 0 if quality.get("overall_pass") or args.no_fail else 1


if __name__ == "__main__":
    sys.exit(main())
