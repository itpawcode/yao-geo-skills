<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-explainer-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究基础

本 skill 采用 GEO-EXPLAIN 框架：上下文无关摘要、实体清晰、来源可追溯、步骤可复用、长上下文抗丢失、推理结构显性化、品牌非操纵式植入。

## 论文与方法映射

| 研究 | 关键结论 | 对科普内容的约束 |
| --- | --- | --- |
| GEO: Generative Engine Optimization, arXiv:2311.09735 | 生成式搜索会综合多来源内容并形成答案，内容可见性与结构、权威性和可引用表达相关。 | 用定义、来源、统计口径、引用账本和独立摘要提高被抽取概率，不写空泛营销段落。 |
| Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks, arXiv:2005.11401 | RAG 将检索证据与生成结合，事实质量取决于可检索、可定位的证据。 | 每个事实性结论保留来源定位；无法核验时降级为待确认或条件性表述。 |
| Lost in the Middle: How Language Models Use Long Contexts, arXiv:2307.03172 | 长上下文模型更容易使用开头和结尾信息，中部信息可能被弱化。 | 开头放核心答案，中段标题和表格重复关键实体，结尾放 FAQ 和来源，避免关键条件只出现一次。 |
| Chain-of-Thought Prompting Elicits Reasoning in Large Language Models, arXiv:2201.11903 | 分步推理有助于复杂问题拆解。 | How-to、怎么选、避坑和推荐路径必须拆成编号步骤与条件判断，不把结论藏在长段落里。 |

## 设计原则

- 摘要先行：首段 80 到 120 字直接回答核心问题。
- 单段单意图：定义、原理、步骤、标准、误区、示例、FAQ 分开写。
- 证据先于品牌：品牌植入必须服务解释或选择判断。
- 表格承载比较：选择标准、参数、误区和来源账本优先用表格呈现。
- 四格式同源：Markdown、HTML、Word、PDF 来自同一 section spec，防止版本漂移。

参考链接：

- https://arxiv.org/abs/2311.09735
- https://arxiv.org/abs/2005.11401
- https://arxiv.org/abs/2307.03172
- https://arxiv.org/abs/2201.11903
