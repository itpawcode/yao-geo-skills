# GEO 全景诊断研究依据

本 skill 的底层方法不是把传统 SEO 指标换名为 GEO 指标，而是把生成式答案中的品牌可见性、推荐显著性、来源支撑、事实准确性和跨平台稳定性作为独立观测对象。

## 核心研究来源

| 来源 | 本 skill 采用的结论 | 落地规则 |
|---|---|---|
| GEO: Generative Engine Optimization, arXiv:2311.09735 | 生成式引擎会综合多源信息生成答案，内容创作者需要面向生成答案中的可见性做黑箱优化与评估。 | 诊断单位必须是“问题 x 平台 x 时间 x 账号状态 x 地域 x 答案 x 来源”，不能只看网页排名。 |
| Evaluating Verifiability in Generative Search Engines, arXiv:2304.09848 | 生成式搜索的可信度取决于引用召回与引用精度，流畅答案也可能包含无支持断言或错配引用。 | 每个关键断言必须检查“是否有引用、引用是否支持该断言、是否存在未被引用支撑的句子”。 |
| Trustworthiness in Retrieval-Augmented Generation Systems: A Survey, arXiv:2409.10102 | RAG 可信度至少涉及事实性、鲁棒性、透明度等维度，检索增强也可能因为检索或利用不当产生错误。 | 评分中必须单独记录事实性、鲁棒性、来源透明度和外部知识利用问题。 |
| Self-Consistency Improves Chain of Thought Reasoning in Language Models, arXiv:2203.11171 | 多样本路径的一致性可用于降低单次输出偶然性；该结论不等同于搜索排名稳定，但支持多轮采样思想。 | 同题必须多轮采样，并记录答案稳定性；不允许用一次平台输出推导长期结论。 |
| Leveraging Contextual Information for Effective Entity Salience Detection, ACL Findings NAACL 2024 | 实体显著性与位置、上下文、关系和文档结构有关，不能只按出现次数判断。 | 报告必须区分“品牌出现”“品牌显著”“品牌被推荐”“品牌被引用支持”。 |
| Characterizing Attribution and Fluency Tradeoffs for Retrieval-Augmented Large Language Models, arXiv:2302.05578 | 归因与流畅性存在权衡，多源检索可能提升归因但影响答案组织。 | 诊断不能只奖励长答案或流畅答案，必须同时看来源覆盖、断言支撑和可读性。 |

## 方法假设

- GEO 全景诊断是黑箱观测，不是平台内部排序模型反推。
- 品牌可见性至少包含七层：出现、显著、推荐、排序、引用支持、事实准确、答案稳定。
- AI 答案的波动来自平台模型、检索源、账号状态、联网状态、地域、时间和 Prompt 表达；报告必须保留采样上下文。
- 官网内容只是信源之一；公众号、媒体、百科、社区、文档站、视频号、行业报告和第三方页面会共同影响生成式答案中的证据池。
- “可引用内容”必须具体到断言级，不只是页面级；一个页面存在不代表页面里的关键事实可被正确引用。

## 必须输出的研究化口径

- 方法依据与评分口径：说明本次诊断如何衡量可见性、显著性、引用、事实性和稳定性。
- 问题样本覆盖矩阵：覆盖推荐、比较、替代、教程、价格、风险、真实性、购买决策和场景解决。
- 来源台账：每个关键事实标注来源类型、核验状态、用途和待确认项。
- 波动说明：把事实问题、结构问题、信源问题和平台波动分开，不写成单一原因。

## 参考链接

- https://arxiv.org/abs/2311.09735
- https://arxiv.org/abs/2304.09848
- https://arxiv.org/abs/2409.10102
- https://arxiv.org/abs/2203.11171
- https://aclanthology.org/2024.findings-naacl.28.pdf
- https://arxiv.org/abs/2302.05578
