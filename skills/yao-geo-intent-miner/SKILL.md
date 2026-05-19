---
name: yao-geo-intent-miner
description: Use when a user asks for GEO 意图拓词、AI 搜索意图挖掘、AI 搜索问题集、问题簇、追问链路、查询重写、内容选题库、FAQ 题库、监测 Prompt 库, or AI Intent Miner.
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Intent Miner

## 使用场景

- 把种子词、品牌、产品、竞品、区域、人群和业务材料扩展成 AI 搜索问题集。
- 先于内容生产建立问题底座，输出意图簇、追问链路、查询重写、内容选题、FAQ、知识库和监测 Prompt。
- 面向 DeepSeek、豆包、千问、Kimi、元宝适配国内 AI 平台的口语、多轮、场景和复杂决策问法。

## 必读资料

- `references/intent-mining-method.md`
- `references/cn-platform-adaptation.md`
- `references/scoring-and-mapping.md`
- `references/four-format-output.md`
- `references/quality-gates.md`

## 执行流程

1. 归一化输入对象：主对象、品牌、产品线、行业、竞品、区域、人群、预算、场景、痛点、资质、规模、时效和材料来源。
2. 建立双层意图：先映射到信息、导航/验证、交易/行动任务层，再扩展为九类 GEO 操作意图。
3. 生成完整自然语言问题，不能只堆短关键词。
4. 输出五段式重写：口语问法、独立重写、检索短语、证据查询、标题输入。
5. 保留多轮追问链路：`root_question_id / parent_question_id / standalone_rewrite / context_dependency / platform_fit`。
6. 聚类去重，按问题目标、用户角色、约束条件、资产用途和合规等级合并同义问题。
7. 八维评分：商业价值、AI 答案触发概率、内容缺口、品牌植入空间、证据可得性、竞争难度、对话延展价值、合规风险。
8. 映射资产：文章、页面模块、FAQ、知识库条目、监测 Prompt、标题生成输入包。
9. 输出 Word/PDF/HTML/Markdown 时必须遵守 `references/four-format-output.md`。Word 宽表必须横向 A4、固定表格布局、表格总宽不超过页面可用宽度；PDF 默认横向 A4，宽表自动换行且不向右溢出。
10. 自 review：检查四个报告是否存在、格式是否有效、内容是否一致、HTML/Word/PDF 是否白底且表格不溢出。

## 输出契约

- AI 搜索问题集与意图地图。
- 问题聚类、追问链路和查询重写清单。
- 评分矩阵与优先级排序。
- 内容选题、FAQ 题库、知识库条目建议。
- 监测 Prompt 库。
- 默认四件套：Markdown、HTML、Word、PDF。
