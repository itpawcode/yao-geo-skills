# yao-geo-explainer-builder

`yao-geo-explainer-builder` 用于生成 GEO 科普文章、How-to 教程、概念解释、怎么选、避坑指南、FAQ、术语表和品牌自然植入建议。

## 适用场景

- 品牌教育与行业知识科普。
- 产品购买前的选择指南。
- 怎么做、怎么选、适合谁、常见误区和推荐路径类内容。
- 面向 Kimi、千问、豆包、DeepSeek、元宝等国内 AI 搜索/问答平台的可抽取内容。

## 交付件

- Markdown 文章。
- HTML 包。
- Word DOCX。
- PDF。
- `quality-report.json` 自动质检报告。

## 关键规则

- 开头必须有 80 到 120 字上下文无关摘要。
- How-to 步骤必须编号，选择标准必须表格化。
- 品牌只能在示例、适用场景、FAQ 或结尾建议中自然出现。
- 健康、金融、法律、收益、安全等敏感领域必须补充边界提醒。
- Word、PDF、HTML、Markdown 必须来自同一内容结构；Word 表格固定正文宽度并处理长 URL/英文 token，避免右侧溢出。

## 示例

示例输入位于 `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/report_input.json`。

运行渲染脚本后会生成：

- `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.md`
- `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/html-package/index.html`
- `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.docx`
- `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/deliverables/acme-sleep-geo-explainer.pdf`
- `skills/yao-geo-explainer-builder/examples/acme-sleep-demo/rendered/quality-report.json`
