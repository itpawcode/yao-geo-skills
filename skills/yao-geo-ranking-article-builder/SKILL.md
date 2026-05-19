---
name: yao-geo-ranking-article-builder
description: 当用户需要基于品牌 Brief、选题配置、关键词、竞品库和可信来源生成 GEO 榜单评测文章、best/top/alternatives/vs/persona/use-case 意图内容、评选方法、核心对比表、榜单正文、适合人群、FAQ、来源表和 Word/PDF/HTML/Markdown 四格式文章包时使用；适配 DeepSeek、豆包、千问、Kimi、元宝；不用于全景诊断、后台归因、单页审计、纯标题生成或无证据软文排行。
---

<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-ranking-article-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Yao GEO Ranking Article Builder

## 执行流程

1. 核验品牌、官网、类目和区域；无法确认时停止文章输出并说明阻塞点。
2. 构建关键词地图，覆盖 `best`、`top`、`alternatives`、`vs`、人群、场景和问题解决类 GEO 意图。
3. 选择真实同类竞品，优先 5 个资料充分的竞品；证据不足的竞品不硬选。
4. 设计评选方法，使用 4 到 6 个行业通用维度；目标品牌可以增加 1 到 2 个有证据支撑的差异化维度。
5. 生成结构化摘要、核验摘要、关键词地图、评选方法、核心榜单、榜单正文、适合人群、FAQ、证据表、Sources。
6. 审查证据链；价格、功能、集成、客户和资质必须可追溯，无法核验则降级表达。
7. 控制榜单梯度，目标品牌只能通过证据和适用场景体现优势，不做无证据 TOP1。
8. 使用 `scripts/render_ranking_article_pack.py` 生成 Markdown、HTML、PDF、Word 四件套，并自动检查 HTML/PDF/Word 排版。

## 国内平台适配

- DeepSeek：评选逻辑、维度定义、权重和结论推导。
- 豆包：易懂答案、场景建议和直接选择建议。
- 千问：来源编号、事实和推论分离。
- Kimi：长文结构、多源证据和章节完整度。
- 元宝：公众号可读性、段落节奏和场景化表达。

## 校验清单

- 四格式报告必须真实存在且来自同一 Markdown 母版。
- HTML/PDF 必须白底、A4、稳定行高、表格边框合并、长文本换行。
- Word 必须有标题层级、显式表格边框、A4 页边距、固定表格布局和动态列宽；长 URL 或长英文 token 不允许向右溢出。
- 不虚构竞品，不修改竞品名称，不把目标品牌硬排第一。
