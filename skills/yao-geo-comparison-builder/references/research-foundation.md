# 研究基础：GEO-CITER 对比框架

本 skill 使用 `GEO-CITER`：Comparison scope、Information gain、Traceable evidence、Equitable comparison、Repair loop。

- Comparison scope：先锁定目标品牌、比较对象、用户场景和决策边界。
- Information gain：每个维度必须提供对决策有增量的信息。
- Traceable evidence：关键判断必须绑定来源 ID；来源不足时降级判断。
- Equitable comparison：保留竞品优势和目标品牌边界，不靠贬损竞品制造优势。
- Repair loop：生成后必须检查事实、引用、同口径、格式和排版，再迭代修复。

参考论文：

- GEO: Generative Engine Optimization: https://arxiv.org/abs/2311.09735
- Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks: https://arxiv.org/abs/2005.11401
- Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection: https://arxiv.org/abs/2310.11511
- Chain-of-Thought Prompting Elicits Reasoning in Large Language Models: https://arxiv.org/abs/2201.11903
