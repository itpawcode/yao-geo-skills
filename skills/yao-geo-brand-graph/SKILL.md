---
name: yao-geo-brand-graph
description: 当用户需要把企业资料、官网、产品、客户案例、人物、地点、证据源和场景词整理成品牌实体知识图谱时使用；用于知识库升级、页面结构设计、监测纠偏、品牌百科化和 AI 内容一致性治理。
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Brand Graph

## 执行流程

1. 按 `references/skill-method.md` 建立来源账本，区分官网、官方文档、投资者关系、客户案例、第三方资料和待确认素材。
2. 按 mention -> candidate -> canonical entity 做实体消歧。
3. 按 `references/entity-schema.md` 抽取品牌、产品、服务、功能、技术、行业、用户、场景、客户、案例、证据、地点、时间。
4. 按 `references/evidence-policy.md` 抽取有方向的关系边，每条关系必须有证据 ID。
5. 输出实体清单、关系清单、可信等级、消歧表、Mermaid、JSON-LD、RDF 三元组、国内 AI 平台测试场景和补强建议。

## 排版质量门

- Word 必须使用横向页面、真实 w:tbl 表格、固定 dxa 表宽，禁止自动表宽撑出页面。
- Word 表格网格总宽必须小于正文宽度，并保留右侧安全边距。
- URL、英文实体 ID、英文产品名和长英文短语必须在单元格内主动断行。
- HTML/PDF 必须白底，表格边框对齐，长文本不向右溢出。

## 工具入口

- `scripts/render_yao_geo_brand_graph.py`：从结构化 `report_input.json` 生成 Word、PDF、HTML、Markdown 和 `quality-report.json`。
- `examples/hubspot-domestic-ai-test/report_input.json`：HubSpot 国内 AI 平台测试样例输入。
- `templates/brief-template.md`：项目输入简报模板。
- `evals/expected_artifacts.json`：必要文件和示例交付检查清单。
- `reports/output-risk-profile.md` 与 `reports/artifact-design-profile.md`：输出风险和排版设计约束。
