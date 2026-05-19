<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-execution-roadmap
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Research-Backed Framework

## 底层理论

本 skill 使用“可发现性、可验证性、可抽取性、可复测性”四层模型组织实施方案。

| 层级 | 含义 | 执行动作 |
|---|---|---|
| 可发现性 | 平台检索、网页抓取、生态入口能找到品牌资产 | 站点结构、索引入口、外部信源、平台生态内容 |
| 可验证性 | 关键断言有真实来源和可追溯证据 | 来源台账、客户案例、第三方证据、引用规范 |
| 可抽取性 | 模型能从页面/知识库中稳定抽取实体、场景、对比、答案 | 摘要句、FAQ、表格、结构化数据、术语表 |
| 可复测性 | 团队能用同一问题、口径和样本复测变化 | Prompt 样本、采样频率、基线数据、质量看板 |

## 论文依据到执行原则

- RAG 研究表明，外部非参数知识和检索结果会影响知识密集型生成任务的事实性与具体性。因此 GEO 执行不能只写“观点文章”，必须建设可检索、可引用、可更新的证据资产。
- Self-RAG 强调按需检索、生成与自我反思能改善事实性和引用准确性。因此方案必须加入来源台账、引用支持检查和复测质检。
- 长上下文研究显示，相关信息处在长文本中间时更容易被忽略。因此长文知识库要前置结论摘要、事实卡和目录锚点，避免关键品牌事实埋在长段落中间。

## 落地规则

1. 每个核心断言必须绑定来源或标记“待确认”。
2. 每个页面和知识库条目必须有前置摘要、关键事实、适用问题和更新时间。
3. 每个平台动作都要服务一个可测目标，不以“多发内容”作为目标。
4. 监测应记录平台、问题、账号状态、时间、地域、轮次、答案文本、引用源、品牌位置和事实错误。

## 参考文献

- Lewis et al., 2020, Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, arXiv:2005.11401.
- Asai et al., 2023, Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection, arXiv:2310.11511.
- Liu et al., 2023, Lost in the Middle: How Language Models Use Long Contexts, arXiv:2307.03172.
