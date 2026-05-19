<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-brand-graph

`yao-geo-brand-graph` 是知识资产类 GEO skill，用于把企业资料转换为可审计的品牌实体知识图谱。

## 适用场景

- 知识库升级。
- 官网、FAQ、公众号、百科页结构设计。
- 国内 AI 平台监测纠偏。
- 品牌百科化和 AI 内容一致性治理。

## 核心输出

- 实体清单、关系清单和可信等级表。
- 消歧表、来源账本和隐私授权检查。
- Mermaid 图、JSON-LD 建议和 RDF 式三元组样例。
- 国内 AI 平台测试场景和图谱补强建议。
- 默认四件套：Word、PDF、HTML、Markdown。

## HubSpot 测试样例

- [输入 JSON](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/report_input.json)
- [Markdown](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.md)
- [HTML](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.html)
- [Word](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.docx)
- [PDF](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/hubspot-domestic-ai-yao-geo-brand-graph.pdf)
- [质量报告](../../skills/yao-geo-brand-graph/examples/hubspot-domestic-ai-test/quality-report.json)

## 排版质量门

- Word 必须是真实表格结构，固定表宽，不能向右溢出。
- PDF 必须可打开、可抽取文本，边缘不能出现溢出像素。
- HTML 必须白底、表格自动换行、边框对齐。
