<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 页面 GEO 诊断研究依据

## 底层模型

本 skill 将页面 GEO 表现拆成四段链路：

1. 检索候选：页面能否被搜索、AI 搜索或 RAG 系统召回。
2. 主内容抽取：系统是否能从 HTML 中抽出正文，而不是导航、广告、页脚或空容器。
3. 证据质量：被抽取片段是否相关、准确、清晰、可追责、足够新。
4. 生成引用：生成式引擎是否能把页面片段用于回答、引用或推荐。

## 研究启发

- `GEO: Generative Engine Optimization` 强调生成式引擎可见性不等同于传统搜索排名。
- `Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks` 提醒页面诊断要关注可召回、可抽取和可引用，而不只是页面文案。
- `SourceBench: Can AI Answers Reference Quality Web Sources?` 将引用源质量拆成相关性、事实准确性、客观性、新鲜度、权威/责任归属和清晰度。
- Web boilerplate removal 研究提醒，HTML 中的正文、导航、页脚、广告和动态渲染内容会影响机器抽取结果。

## 诊断影响

- 不把 schema 当作独立答案源；schema 必须和正文事实一致。
- 不把 SEO 关键词密度当作 GEO 可见性的核心指标；更重视事实原子性、段落独立性、来源可追责和证据一致性。
- 不把最终浏览器截图等同于机器可读页面；必须检查初始 HTML 和 JS 渲染依赖。
