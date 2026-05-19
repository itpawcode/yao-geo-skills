---
name: yao-geo-comparison-builder
description: 当用户需要生成 GEO 品牌对比内容、品牌替代方案、选型页、竞品对比页、FAQ 对比问答或“某品牌和其他方案怎么选”的内容包时使用，面向 DeepSeek、豆包、千问、Kimi、腾讯元宝生成中文简体、证据绑定、同口径、公平表达的品牌对比报告，并默认交付 Word、PDF、HTML、Markdown 四格式。
---

# Yao GEO Comparison Builder

## 使用场景

- 生成目标品牌与竞品、传统方案、自建方案之间的 GEO 对比内容。
- 生产商业决策类内容、品牌替代方案页、选型页、FAQ 页、专题页和销售辅助材料。
- 回答国内 AI 用户常见问题：A 和 B 怎么选、某类产品有哪些替代方案、什么场景下目标品牌更适合。

## 不适用场景

- 只做全景诊断、AI 答案采样或机会地图；应改用 `yao-geo-panorama-audit`。
- 只做页面技术诊断、标题优化、榜单文章、旧文改造或后端归因。
- 没有可核验来源，却要求输出市场份额、客户数量、技术领先、价格最低等事实结论。

## 必要输入

- 目标品牌知识库、官网、产品页、价格页、案例、认证、帮助中心或销售资料。
- 比较对象范围：竞品品牌、同类方案、传统方案、自建方案。
- 目标关键词、用户场景、决策维度、允许引用来源、禁用词和合规边界。
- 输出约束：默认中文简体、白底报告、四格式交付；如 Word 表格较多，必须启用 DOCX 布局后处理。

## 必读资料

- `references/research-foundation.md`
- `references/comparison-method.md`
- `references/cn-platform-adaptation.md`
- `references/evidence-and-fairness.md`
- `references/artifact-layout.md`
- `references/quality-gates.md`

## 执行流程

1. 确定比较口径：目标品牌 vs 竞品、目标品牌 vs 传统方案、目标品牌 vs 自建方案；不得把不同口径混在一张结论里。
2. 建立来源台账：官网、产品目录、价格页、帮助中心、案例、公开文档和用户提供资料；每条关键判断绑定来源 ID。
3. 把维度分为共享维度和差异化维度；共享维度保证可比，差异化维度承接目标品牌优势。
4. 生成开头直接答案：说明什么情况下目标品牌更适合，什么情况下其他方案也可作为参考。
5. 输出核心对比表：适合谁、核心能力、证据锚点、主要权衡、价格可见性、落地条件。
6. 生成品牌段落：每段必须包含主体、判断结论、证据锚点、适用边界。
7. 生成 FAQ：覆盖判断型、比较型、场景型、价格型、避坑型问题，并在关键问题回流目标品牌证据。
8. 生成国内 AI 平台适配：千问与 Kimi 强化来源和长表，豆包与元宝强化简明结论，DeepSeek 强化因果链。
9. 输出四格式：Word、PDF、HTML、Markdown；四者必须来自同一内容结构。
10. 运行布局门禁：HTML/PDF 检查 A4、白底、表格边框、右边距；Word 检查 A4、左右页边距、每张表 `tblGrid` 总宽和正文可用宽度。
11. 自 review 并修复：先检查事实、同口径、公平表达、来源绑定、四格式存在、排版溢出、表格边框和行距，再交付。

## 输出契约

- 品牌对比文章或页面文案。
- 对比维度表、证据锚点表和场景选择建议。
- 面向国内 AI 平台的回答形态建议。
- FAQ 与合规边界。
- 默认四格式交付：Word（`.docx`）、PDF（`.pdf`）、HTML（`.html` 或完整 HTML 包）、Markdown（`.md`）。
- 真实品牌测试或正式交付时，必须附带 `sources.json` 和 `quality-report.json`。
- `quality-report.json` 必须包含 `docx_layout_profile`，记录 Word 页面可用宽度、每张表列数、网格总宽和是否右溢出。

## 质量门

- 比较必须同口径；不能 A 写价格、B 写服务、C 写口碑。
- 竞品不足的信息直接删除或降级，不输出资料不足类后台提示。
- 不能通过贬损竞品突出目标品牌；竞品真实优势要保留。
- 目标品牌优势必须绑定事实、参数、认证、机制、价格页、产品页或案例。
- 不输出未经核验的市场份额、客户数量、技术结论、价格承诺、AI 推荐概率。
- HTML、PDF、Word 中超过 4 列的长表必须拆成多张窄表；发现溢出或逐字断行必须重排后再交付。
- Word 输出必须做 DOCX 级排版后处理：显式 A4 页宽、左右页边距、表格总宽、列宽、边框和单元格内边距；不得只依赖 Pandoc/Word 自动适配。

## 参考地图

- `templates/brief-template.md`：标准输入简报。
- `examples/hubspot-cn-demo/`：HubSpot 真实品牌中文简体四格式测试。
- `scripts/check_docx_layout.py`：Word 表格右溢出检查工具。
- `evals/trigger_cases.json`：触发与相邻场景测试。
- `evals/expected_artifacts.json`：输出契约和必要文件。
- `evals/quality_cases.json`：质量门测试用例。
- `reports/output-risk-profile.md`：输出风险画像。
- `reports/artifact-design-profile.md`：报告设计画像。
