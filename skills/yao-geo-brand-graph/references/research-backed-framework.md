<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 研究支撑框架

本 skill 采用“知识图谱 + 实体链接 + 证据治理 + 结构化数据一致性”的组合框架。

- Hogan, A. et al. “Knowledge Graphs.” https://arxiv.org/abs/2003.02320
- W3C. “RDF 1.1 Concepts and Abstract Syntax.” https://www.w3.org/TR/2014/REC-rdf11-concepts-20140225/
- W3C. “JSON-LD 1.1.” https://www.w3.org/TR/json-ld11/
- Shen, W., Wang, J., Han, J. “Entity Linking with a Knowledge Base: Issues, Techniques, and Solutions.” https://doi.org/10.1109/TKDE.2014.2327028

落地规则：先建立来源账本，再做实体和关系；把品牌资料拆成提及、候选、规范实体、关系边、证据五层；JSON-LD 只承载页面正文已写明且可验证的事实。
