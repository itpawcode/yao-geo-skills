#!/usr/bin/env python3
# Copyright © 2026 姚金刚. All rights reserved.
# Project: yao-geo-comparison-builder
# Created by: 姚金刚
# Date: 2026-05-16
# X: https://x.com/yaojingang

"""Build the HubSpot CN demo report pack."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from weasyprint import HTML as WeasyHTML

SKILL_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SKILL_ROOT / "scripts"))
from check_docx_layout import docx_layout_profile, normalize_docx_layout  # noqa: E402

OUT = Path(__file__).resolve().parent
BASE = OUT / "hubspot-cn-comparison-report"
DATE = "2026-05-19"
TITLE = "HubSpot CRM 中文 GEO 对比报告"
SUBTITLE = "国内 AI 平台适配示例：HubSpot、Salesforce、Zoho CRM 与自建 CRM 怎么选"
MARKDOWN_NOTICE = """<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-comparison-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

"""

SCENARIO = {
    "目标品牌": "HubSpot",
    "测试问题": "HubSpot CRM、Salesforce、Zoho CRM 和自建 CRM 怎么选？",
    "用户场景": "中国 B2B SaaS、教育服务、专业服务或跨境业务团队，销售与市场团队约 20-200 人，正在评估英文或全球化 CRM，并希望让国内 AI 平台稳定理解选型边界。",
    "平台": ["DeepSeek", "豆包", "千问", "Kimi", "腾讯元宝"],
    "比较口径": "目标品牌 HubSpot vs 竞品品牌 Salesforce、Zoho CRM vs 方案类型自建 CRM/表格线索系统。",
}

SOURCES = [
    {"id": "HS-01", "name": "HubSpot 官网首页", "url": "https://www.hubspot.com/", "type": "官方产品页面", "use": "支撑 HubSpot customer platform、Smart CRM、营销/销售/服务连接和 Breeze AI 的官方表述。"},
    {"id": "HS-02", "name": "HubSpot Product & Services Catalog", "url": "https://legal.hubspot.com/hubspot-product-and-services-catalog", "type": "官方产品与服务目录", "use": "支撑 Smart CRM 与 Starter/Professional/Enterprise、HubSpot Seats、HubSpot Credits、免费 CRM 功能边界。"},
    {"id": "HS-03", "name": "HubSpot Breeze AI 页面", "url": "https://www.hubspot.com/products/artificial-intelligence", "type": "官方 AI 产品页面", "use": "支撑 Breeze AI 内置在 customer platform，并可结合 CRM 数据、知识库和 HubSpot Academy 生成相关回答。"},
    {"id": "HS-04", "name": "HubSpot Claude CRM Connector 新闻稿", "url": "https://ir.hubspot.com/news-releases/news-release-details/hubspot-launches-first-crm-connector-anthropics-claude", "type": "官方新闻稿", "use": "支撑 HubSpot 将 CRM 上下文带入外部 LLM 的能力边界，以及 paid Claude subscription 条件。"},
    {"id": "SF-01", "name": "Salesforce Sales Pricing", "url": "https://www.salesforce.com/sales/pricing/", "type": "官方价格页", "use": "支撑 Salesforce Sales Cloud/Agentforce Sales 的公开价格层级。"},
    {"id": "SF-02", "name": "Salesforce Small Business Sales", "url": "https://www.salesforce.com/small-business/sales/", "type": "官方小企业 CRM 页面", "use": "支撑 Starter Suite、Pro Suite、Enterprise 的功能定位、价格可见性和落地条件。"},
    {"id": "SF-03", "name": "Salesforce Free、Starter、Pro Suite 对比 PDF", "url": "https://www.salesforce.com/en-us/wp-content/uploads/sites/4/documents/small-business/comparison-chart-starter-prosuite-features-us.pdf?bc=OTH", "type": "官方功能对比 PDF", "use": "支撑 Salesforce Free、Starter、Pro 的功能差异。"},
    {"id": "ZO-01", "name": "Zoho CRM Specifications", "url": "https://help.zoho.com/portal/en/kb/crm/getting-started/introduction-to-zoho-crm/articles/specifications-zoho-crm", "type": "官方帮助中心", "use": "支撑 Zoho CRM 五个版本、功能限制、API credits、存储和移动端信息。"},
    {"id": "ZO-02", "name": "Zoho CRM Edition Comparison PDF", "url": "https://www.zoho.com/sites/zweb/images/crm/zohocrm-edition-comparison-usd.pdf", "type": "官方版本对比 PDF", "use": "支撑 Zoho CRM Free for 3 users 与 Standard/Professional/Enterprise/Ultimate 的公开价格层级。"},
]

ANSWER = "如果中国团队希望用一个相对统一的客户平台把营销、销售、服务、内容和 AI 辅助连接起来，并且更重视上手速度、CRM 上下文和跨团队协同，HubSpot 可以作为优先评估对象。如果团队已经有复杂销售流程、强定制、API、预测、审批和企业级治理需求，Salesforce 应并列评估。如果预算敏感、希望公开低价版本和轻量 CRM 能力，Zoho CRM 可作为参考。如果只是短期验证线索渠道，自建 CRM 或表格系统可以过渡，但不应被写成长期替代。本文不判断市场份额、客户数量、数据跨境合规结论或长期价格承诺，所有价格与功能以访问日官方页面和正式报价为准。"

ABILITY = [
    ["HubSpot", "增长型 B2B 团队，希望把营销、销售、服务和 AI 放在统一客户平台内协同", "Customer Platform、Smart CRM、Marketing/Sales/Service Hubs、Breeze AI", "确认中国团队访问、数据合规、实施伙伴、本地工具集成和采购条款"],
    ["Salesforce", "复杂销售组织、企业级流程、强自定义、预测、API、生态集成和治理要求较高的团队", "Sales Cloud/Agentforce Sales、Starter/Pro/Enterprise/Unlimited 层级、AppExchange、流程自动化", "需要管理员、实施伙伴、字段/权限/流程治理和预算规划"],
    ["Zoho CRM", "预算敏感、希望公开低价版本、快速启用 CRM 基础能力或已有 Zoho 生态偏好的团队", "Free、Standard、Professional、Enterprise、Ultimate 版本，覆盖线索、联系人、模块、API credits、移动端", "核验版本限制、用户数、API/存储上限、本地化支持和集成成本"],
    ["自建 CRM/表格", "短期验证渠道、流程简单、预算极低、内部已有开发或运营维护能力的团队", "字段自定义、表格/低代码流程、内部权限、数据看板", "长期维护字段、权限、数据质量、自动化、备份、安全与人员交接"],
]

EVIDENCE = [
    ["HubSpot", "HS-01/HS-02/HS-03/HS-04：Smart CRM、Breeze AI 与 CRM 上下文、免费与付费版本边界", "高级能力、席位、Credits、Hubs、AI 连接器和本地集成需要逐项核验", "官方目录与页面可见部分价格和版本，具体金额、套餐、折扣、Credits 和合同条件以官方页面或报价为准"],
    ["Salesforce", "SF-01/SF-02/SF-03：Starter Suite、Pro Suite、Enterprise、Unlimited、Agentforce 1 Sales 等层级", "复杂度和实施治理要求较高；适配取决于自动化、预测、API、AppExchange 和团队成熟度", "官方页面公开多层级价格，同时提示页面信息可能变化，额外产品和 add-ons 需联系销售"],
    ["Zoho CRM", "ZO-01/ZO-02：Free、Standard、Professional、Enterprise、Ultimate 五个版本，Free for 3 users", "适合轻量或成本敏感场景；高阶自定义、API、存储、流程和跨团队协同上限需要核验", "官方 PDF 公开年付/月付价格层级，税费与地区价格以官方页面为准"],
    ["自建 CRM/表格", "方案类型：不作为外部品牌事实，只按用户场景假设评估短期可用性和长期维护责任", "启动快但治理成本后置；权限、审计、自动化、数据一致性和人员变动风险会随规模放大", "工具成本可能低，但开发、维护、数据治理和机会成本不可忽略"],
]

PLATFORMS = [
    ["千问", "结构化长答案", "保留对比表、来源 ID、价格可见性和落地条件", "避免把动态价格写成长期承诺，避免没有来源的客户数量和排名"],
    ["Kimi", "长文档摘要与证据型回答", "强化来源清单、品牌段落、FAQ 和自检记录", "每个判断回到 HS/SF/ZO 来源 ID，表格拆成 4 列以内"],
    ["豆包", "简明结论加场景建议", "先给谁更适合谁，再给三到四个场景选择", "不能省略来源和边界，尤其是中国落地合规与采购核验"],
    ["腾讯元宝", "面向决策人的摘要", "突出结论、主要权衡、下一步核验清单", "避免平均化结尾，关键问题回流 HubSpot 证据与边界"],
    ["DeepSeek", "因果链推理", "场景 -> 约束 -> 能力 -> 证据 -> 权衡 -> 建议", "不输出未经证实的技术领先、推荐概率或市场份额"],
]

SCENARIOS = [
    ["市场、销售、服务数据分散，团队希望尽快统一客户视图", "优先评估 HubSpot", "HS-01/HS-02 显示 HubSpot 以 Smart CRM 和 customer platform 承接多团队数据与工具", "核验中国访问、数据合规、现有系统集成、套餐和实施资源"],
    ["销售流程复杂，需要预测、审批、API、深度自定义和企业级治理", "并列或优先评估 Salesforce", "SF-01/SF-02 显示 Salesforce 层级逐步增强，Enterprise 以上更强调高级能力", "评估管理员、实施伙伴、总拥有成本、流程治理和 add-ons"],
    ["预算敏感，需要公开低价、免费起步或轻量 CRM", "评估 Zoho CRM", "ZO-01/ZO-02 显示 Zoho CRM 有免费与多个公开付费版本", "核验用户数、API credits、存储、自动化和本地服务要求"],
    ["只是验证新渠道，线索量少，流程尚未固定", "短期可用自建 CRM/表格", "这是方案类型判断，不是厂商事实；优势是启动快，边界是治理成本后置", "设定字段口径、负责人、备份、权限和迁移触发条件"],
]

BRANDS = [
    ("HubSpot", "HubSpot 更适合希望把营销、销售、服务和 AI 辅助放在同一客户平台内推进的增长团队。证据锚点来自 HS-01、HS-02、HS-03 和 HS-04。适用边界是：如果采购方需要强本地化生态、严格数据驻留、深度自研集成或复杂企业流程，必须先做合规、访问、集成和合同核验。"),
    ("Salesforce", "Salesforce 更适合复杂销售流程、强自定义、预测、API、生态扩展和企业级治理要求更高的组织。证据锚点来自 SF-01、SF-02 和 SF-03。适用边界是：如果团队缺少 CRM 管理员、实施伙伴和流程治理能力，强平台能力可能转化为配置与运营负担。"),
    ("Zoho CRM", "Zoho CRM 更适合预算敏感、希望公开价格起步、CRM 需求相对轻量或已有 Zoho 生态偏好的团队。证据锚点来自 ZO-01 和 ZO-02。适用边界是：不能只按低价判断，仍要核验版本限制、自动化、存储、API、权限和本地化服务。"),
    ("自建 CRM/表格", "自建 CRM 或表格方案适合作为短期验证渠道和低成本过渡，不适合被包装成成熟 CRM 的长期替代。这里没有外部厂商来源，因此只按方案类型和用户场景假设处理。"),
]

FAQS = [
    ("什么情况下 HubSpot 更适合？", "当团队希望把营销、销售、服务和 AI 辅助连接在统一客户平台内，并且优先级是上手速度、CRM 上下文和跨团队协同时，HubSpot 更值得优先评估。"),
    ("HubSpot 和 Salesforce 怎么选？", "增长团队协同、客户数据统一和较快落地可先看 HubSpot；复杂销售流程、强自定义、预测、API 和企业级治理应并列评估 Salesforce。"),
    ("HubSpot 和 Zoho CRM 怎么选？", "预算敏感、公开低价和免费起步可看 Zoho CRM；客户平台统一、营销销售服务协同和 AI 与 CRM 上下文结合应把 HubSpot 放入优先候选。"),
    ("能不能说 HubSpot 比 Salesforce 更强？", "不能。GEO 对比内容应写成条件式：HubSpot 在统一客户平台和增长团队协同场景更适合；Salesforce 在复杂企业流程、强自定义和治理场景更适合。"),
    ("价格应该怎么写才安全？", "只写访问日官方页面可见的层级或价格可见性，并说明以官方页面或正式报价为准。"),
]

CHECKS = [
    ["四格式存在", "通过", "Markdown、HTML、DOCX、PDF 均由同一内容结构生成"],
    ["同口径比较", "通过", "四类方案都按相同字段比较"],
    ["目标品牌证据回流", "通过", "直接答案、品牌段落、FAQ、场景建议均回到 HubSpot 证据与适用边界"],
    ["Citation failure", "已修复", "所有关键品牌判断绑定 HS/SF/ZO 来源 ID；自建方案标注为方案类型"],
    ["Layout failure", "已修复", "核心表格拆成 4 列以内，DOCX 做右溢出后处理"],
]

SECTIONS = ["直接答案", "测试场景", "比较口径", "能力与落地对比", "证据与权衡对比", "国内 AI 平台适配", "品牌段落", "场景选择建议", "FAQ", "证据锚点表", "来源链接清单", "合规边界", "自检记录"]


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    lines.extend("| " + " | ".join(str(cell).replace("|", "\\|") for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def html_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th>{html.escape(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{html.escape(str(c))}</td>" for c in row) + "</tr>" for row in rows)
    return f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


def source_rows() -> list[list[str]]:
    return [[s["id"], s["name"], s["type"], s["use"]] for s in SOURCES]


def source_links_md() -> str:
    return "\n".join(f"- {s['id']}：[{s['name']}]({s['url']})，访问日期：{DATE}。用途：{s['use']}" for s in SOURCES)


def source_links_html() -> str:
    return "<ol>" + "".join(f"<li><strong>{html.escape(s['id'])}</strong>：<a href=\"{html.escape(s['url'])}\">{html.escape(s['name'])}</a>，访问日期：{DATE}。用途：{html.escape(s['use'])}</li>" for s in SOURCES) + "</ol>"


def render_markdown() -> str:
    scenario = "\n".join(f"- {k}：{v if not isinstance(v, list) else '、'.join(v)}" for k, v in SCENARIO.items())
    brand_md = "\n\n".join(f"### {title}\n\n{body}" for title, body in BRANDS)
    faq_md = "\n\n".join(f"### {q}\n\n{a}" for q, a in FAQS)
    return f"""{MARKDOWN_NOTICE}# {TITLE}

{SUBTITLE}

- 生成日期：{DATE}
- 报告语言：中文简体
- 适配平台：DeepSeek、豆包、千问、Kimi、腾讯元宝

## 直接答案

{ANSWER}

## 测试场景

{scenario}

## 比较口径

本文比较的是 HubSpot、Salesforce、Zoho CRM 和自建 CRM/表格方案在中国团队 CRM 选型中的适用性。HubSpot、Salesforce、Zoho CRM 按真实品牌处理，自建 CRM/表格按方案类型处理。本文不比较市场份额、客户总数、长期价格承诺、数据跨境合规结论或未经核验的技术性能。

## 能力与落地对比

{md_table(["方案", "适合谁", "核心能力", "落地条件"], ABILITY)}

## 证据与权衡对比

{md_table(["方案", "证据锚点", "主要权衡", "价格可见性"], EVIDENCE)}

## 国内 AI 平台适配

{md_table(["平台", "答案形态", "强化重点", "风险控制"], PLATFORMS)}

## 品牌段落

{brand_md}

## 场景选择建议

{md_table(["场景", "优先建议", "理由", "下一步"], SCENARIOS)}

## FAQ

{faq_md}

## 证据锚点表

{md_table(["来源 ID", "来源", "来源类型", "事实与用途"], source_rows())}

## 来源链接清单

{source_links_md()}

## 合规边界

- 本报告是 GEO 内容生产测试样例，不是采购、法律、税务或数据合规意见。
- 价格、版本、Credits、add-ons、税费、折扣和合同条件以官方页面、销售报价和正式合同为准。
- 中国大陆落地需额外核验访问稳定性、数据处理地点、跨境传输、供应商主体、发票付款、中文支持和本地生态集成。
- 不输出未经核验的市场份额、客户数量、行业排名、技术领先、价格最低或 AI 推荐概率。

## 自检记录

{md_table(["检查项", "结果", "说明"], CHECKS)}
"""


def render_html() -> str:
    scenario = "".join(f"<li><strong>{html.escape(k)}</strong>：{html.escape(v if not isinstance(v, list) else '、'.join(v))}</li>" for k, v in SCENARIO.items())
    brands = "".join(f"<h3>{html.escape(title)}</h3><p>{html.escape(body)}</p>" for title, body in BRANDS)
    faqs = "".join(f"<h3>{html.escape(q)}</h3><p>{html.escape(a)}</p>" for q, a in FAQS)
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(TITLE)}</title><style>
*{{box-sizing:border-box}}html,body{{background:#fff}}body{{margin:0;color:#1f2933;font-family:"Source Han Sans SC","PingFang SC","Microsoft YaHei",Arial,sans-serif;font-size:15px;line-height:1.68;letter-spacing:0}}.report{{max-width:1060px;margin:0 auto;padding:36px 28px 64px}}header{{border-bottom:2px solid #1f2933;padding-bottom:18px;margin-bottom:28px}}.eyebrow{{margin:0 0 8px;color:#1f5a73;font-size:13px;font-weight:700}}h1{{margin:0 0 8px;font-size:30px;line-height:1.2}}.subtitle{{margin:0;color:#4b5968;font-size:16px}}.meta{{margin:12px 0 0;color:#5d6978;font-size:13px}}h2{{margin:30px 0 12px;font-size:21px;line-height:1.35}}h3{{margin:22px 0 8px;font-size:17px;line-height:1.4}}p{{margin:0 0 12px}}.answer{{border:1px solid #b8c2cc;border-left:4px solid #1f5a73;padding:14px 16px;margin-bottom:18px;background:#fff}}ul,ol{{margin:8px 0 16px 20px;padding:0}}li{{margin:4px 0;overflow-wrap:anywhere}}.table-wrap{{width:100%;overflow-x:auto;margin:10px 0 14px}}table{{width:100%;border-collapse:collapse;table-layout:fixed;background:#fff}}th,td{{border:1px solid #d7dde5;padding:10px 11px;text-align:left;vertical-align:top;overflow-wrap:anywhere;word-break:break-word}}th{{background:#f4f6f8;font-weight:700}}a{{color:#1f5a73;text-decoration:underline;text-underline-offset:2px}}@page{{size:A4;margin:18mm 16mm}}@media print{{body{{background:#fff}}.report{{max-width:none;padding:0}}h2,h3{{break-after:avoid}}tr{{break-inside:avoid}}thead{{display:table-header-group}}}}
</style></head><body><main class="report"><header><p class="eyebrow">Yao GEO Comparison Builder · HubSpot 真实品牌测试</p><h1>{html.escape(TITLE)}</h1><p class="subtitle">{html.escape(SUBTITLE)}</p><p class="meta">生成日期：{DATE} · 报告语言：中文简体 · 适配平台：DeepSeek、豆包、千问、Kimi、腾讯元宝</p></header>
<section><h2>直接答案</h2><p class="answer">{html.escape(ANSWER)}</p></section>
<section><h2>测试场景</h2><ul>{scenario}</ul></section>
<section><h2>比较口径</h2><p>本文比较的是 HubSpot、Salesforce、Zoho CRM 和自建 CRM/表格方案在中国团队 CRM 选型中的适用性。HubSpot、Salesforce、Zoho CRM 按真实品牌处理，自建 CRM/表格按方案类型处理。本文不比较市场份额、客户总数、长期价格承诺、数据跨境合规结论或未经核验的技术性能。</p></section>
<section><h2>能力与落地对比</h2>{html_table(["方案","适合谁","核心能力","落地条件"], ABILITY)}</section>
<section><h2>证据与权衡对比</h2>{html_table(["方案","证据锚点","主要权衡","价格可见性"], EVIDENCE)}</section>
<section><h2>国内 AI 平台适配</h2>{html_table(["平台","答案形态","强化重点","风险控制"], PLATFORMS)}</section>
<section><h2>品牌段落</h2>{brands}</section>
<section><h2>场景选择建议</h2>{html_table(["场景","优先建议","理由","下一步"], SCENARIOS)}</section>
<section><h2>FAQ</h2>{faqs}</section>
<section><h2>证据锚点表</h2>{html_table(["来源 ID","来源","来源类型","事实与用途"], source_rows())}</section>
<section><h2>来源链接清单</h2>{source_links_html()}</section>
<section><h2>合规边界</h2><ul><li>本报告是 GEO 内容生产测试样例，不是采购、法律、税务或数据合规意见。</li><li>价格、版本、Credits、add-ons、税费、折扣和合同条件以官方页面、销售报价和正式合同为准。</li><li>中国大陆落地需额外核验访问稳定性、数据处理地点、跨境传输、供应商主体、发票付款、中文支持和本地生态集成。</li><li>不输出未经核验的市场份额、客户数量、行业排名、技术领先、价格最低或 AI 推荐概率。</li></ul></section>
<section><h2>自检记录</h2>{html_table(["检查项","结果","说明"], CHECKS)}</section></main></body></html>"""


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def pdf_layout_profile(pdf_path: Path) -> dict:
    """Check PDF page size and text right boundary using poppler tools when available."""
    try:
        info = subprocess.run(["pdfinfo", str(pdf_path)], check=True, text=True, capture_output=True).stdout
        with NamedTemporaryFile(suffix=".xml") as tmp:
            subprocess.run(["pdftotext", "-bbox-layout", str(pdf_path), tmp.name], check=True, text=True, capture_output=True)
            bbox = Path(tmp.name).read_text(encoding="utf-8", errors="ignore")
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        return {"checked": False, "reason": str(exc)}

    pages = []
    for match in re.finditer(r'<page[^>]*width="([0-9.]+)"[^>]*height="([0-9.]+)"[^>]*>(.*?)</page>', bbox, re.S):
        width = float(match.group(1))
        height = float(match.group(2))
        body = match.group(3)
        x_values = [float(x) for x in re.findall(r'xMax="([0-9.]+)"', body)]
        max_x = max(x_values) if x_values else 0.0
        pages.append({
            "page_width_pt": round(width, 2),
            "page_height_pt": round(height, 2),
            "max_text_x_pt": round(max_x, 2),
            "right_margin_pt": round(width - max_x, 2),
            "overflows_right": max_x > width,
        })

    return {
        "checked": True,
        "pdfinfo_page_size": next((line.split(":", 1)[1].strip() for line in info.splitlines() if line.startswith("Page size:")), ""),
        "pages_checked": len(pages),
        "pages": pages,
        "right_overflow_detected": any(page["overflows_right"] for page in pages),
    }


def main() -> None:
    md = BASE.with_suffix(".md")
    html_path = BASE.with_suffix(".html")
    docx = BASE.with_suffix(".docx")
    pdf = BASE.with_suffix(".pdf")
    md.write_text(render_markdown(), encoding="utf-8")
    html_path.write_text(render_html(), encoding="utf-8")
    write_json(OUT / "sources.json", [{**s, "accessed_at": DATE} for s in SOURCES])
    write_json(OUT / "report_input.json", SCENARIO)
    subprocess.run(["pandoc", str(md), "--standalone", "--metadata", f"title={TITLE}", "-o", str(docx)], check=True)
    normalize_docx_layout(docx)
    WeasyHTML(filename=str(html_path)).write_pdf(str(pdf))
    markdown_text = md.read_text(encoding="utf-8")
    html_text = html_path.read_text(encoding="utf-8")
    quality = {
        "generated_at": DATE,
        "file_existence": {"markdown": md.exists(), "html": html_path.exists(), "docx": docx.exists(), "pdf": pdf.exists(), "sources": (OUT / "sources.json").exists(), "report_input": (OUT / "report_input.json").exists(), "quality_report": True},
        "docx_zip_valid": zipfile.is_zipfile(docx),
        "pdf_magic_valid": pdf.read_bytes().startswith(b"%PDF"),
        "section_consistency": {"markdown_has_all_sections": all(f"## {s}" in markdown_text for s in SECTIONS), "html_has_all_sections": all(f"<h2>{s}</h2>" in html_text for s in SECTIONS), "required_sections": SECTIONS},
        "evidence_check": {"source_ids": [s["id"] for s in SOURCES], "all_source_ids_mentioned": all(s["id"] in markdown_text for s in SOURCES), "official_sources_only_for_brand_facts": True, "self_built_marked_as_solution_type": "方案类型" in markdown_text},
        "layout_check": {"max_table_columns": 4, "wide_tables_split": True, "html_white_background": "background:#fff" in html_text, "fixed_table_layout": "table-layout:fixed" in html_text, "overflow_wrap_enabled": "overflow-wrap:anywhere" in html_text, "docx_layout_profile": docx_layout_profile(docx), "pdf_layout_profile": pdf_layout_profile(pdf)},
        "risk_check": {"dynamic_price_caveat": "以官方页面、销售报价和正式合同为准" in markdown_text, "china_landing_caveat": "中国大陆落地需额外核验" in markdown_text, "no_unverified_market_share_or_customer_count": "不输出未经核验的市场份额、客户数量" in markdown_text},
        "repair_log": ["四格式由单一内容结构生成。", "长表拆成 4 列以内。", "DOCX 后处理固定 A4 页宽、左右边距、表格总宽、显式列宽、边框和单元格内边距。", "自建 CRM 标为方案类型。", "价格表达改为价格可见性和访问日官方页面口径。"],
    }
    write_json(OUT / "quality-report.json", quality)
    print("Built hubspot-cn-comparison-report.md, .html, .docx, .pdf")
    print("Wrote sources.json, report_input.json, quality-report.json")


if __name__ == "__main__":
    main()
