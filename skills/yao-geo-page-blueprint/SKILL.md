---
name: yao-geo-page-blueprint
description: Use when the user needs a GEO-friendly page blueprint for a specific product, topic, article, ranking, comparison, FAQ, knowledge-base, or case page, especially when the work must become implementable page structure rather than only copywriting.
metadata:
  owner: Yao Team
  family: geo-page-technical
  maturity: beta
  requires_web: false
  default_outputs: Word, PDF, HTML, Markdown
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-blueprint
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Page Blueprint

## 使用场景

- 把目标内容、目标问题、品牌知识库、用户路径和转化目标，落成 GEO 友好的页面方案。
- 页面类型属于产品页、专题页、文章页、榜单页、对比页、科普页、知识库页、案例页或 FAQ 页。
- 页面要同时服务国内 AI 平台抓取、答案抽取、真实用户阅读和转化。
- 交付物需要包含 HTML 语义结构、Schema 建议、CMS 字段清单和四格式报告。

## 不适用场景

- 全站品牌、竞品、信源和 AI 答案样本诊断；应改用 `yao-geo-panorama-audit`。
- GEO 后端效果归因、埋点或追踪闭环；应改用 `yao-geo-tracking`。
- 只写文章、标题、公众号推文或内容改写，而不需要页面落地方案。

## 必读资料

- `references/page-blueprint-method.md`
- `references/research-foundation.md`
- `references/cn-ai-platform-adaptation.md`
- `references/schema-html-cms-contract.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`
- `references/output-file-workflow.md`

## 执行流程

1. 选择页面类型：产品页、专题页、榜单页、对比页、科普页、知识库页、案例页或 FAQ 页。
2. 对齐目标问题、用户路径、品牌事实、转化目标和合规边界。
3. 建立研究依据映射：把 GEO 可见性、长上下文位置偏置、RAG 证据可追溯、结构化特征和 Schema 规则转成页面设计原则。
4. 生成信息架构：首屏直接答案、结构化摘要、核心事实卡、对比表、证据区、FAQ、案例、来源和转化模块。
5. 设计 AI 可抽取模块：键值对、表格、步骤、原子事实、实体关系、问答和上下文无关摘要。
6. 设计用户转化模块：CTA、表单、咨询、下载、试用、案例入口和内链；CTA 不能干扰核心答案和证据区。
7. 输出 HTML 语义结构与 Schema 候选，包括 Article、FAQPage、Product、Organization、BreadcrumbList、Review 等。
8. 输出 CMS 字段清单，说明字段 key、中文名、类型、必填性、来源、校验规则、前端位置和是否进入 Schema。
9. 输出桌面端、移动端和公众号版排版建议。
10. 如需文件交付，使用 `scripts/render_yao_geo_page_blueprint.py` 从 `report_input.json` 生成 Markdown、HTML、Word、PDF。
11. 按 `references/quality-gates.md` 自 review；发现格式缺失、溢出、字段英文化、Schema 越界或 CTA 干扰时，先修复再交付。

## 输出契约

- `GEO 页面设计方案`
- `页面模块与信息架构图`
- `研究依据与页面设计原则`
- `证据区与来源台账`
- `AI 可抽取模块设计`
- `用户转化模块设计`
- `HTML 结构样例`
- `Schema 建议`
- `CMS 字段清单`
- `桌面端、移动端和公众号版建议`
- 默认四格式交付：Word（`.docx`）、PDF（`.pdf`）、HTML（`.html`）、Markdown（`.md`）

## 校验清单

- 首屏不能只有营销口号，必须有直接答案、关键事实和摘要。
- FAQ 不能只放页面底部；高价值问题要进入页面中前段或关键模块旁。
- HTML 语义必须清楚，表格、问答、步骤和事实卡不能只靠视觉卡片表达。
- Schema 不得包含正文没有的事实，不得伪造评分、评价、价格、资质或案例。
- 证据区必须明确来源、页面内位置、核验日期和用途，不能只列参考链接。
- FAQPage 不能被当成通用流量技巧或 Google 富结果承诺；FAQ 内容必须真实可见，且不用于广告目的。
- 四格式报告必须白底、对齐稳定、表格可读、无溢出、无异常行距，并完成自 review。
