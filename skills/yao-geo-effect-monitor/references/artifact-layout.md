<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-effect-monitor
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# Artifact Layout

- Markdown 是内容源，HTML、Word、PDF 从同一份 Markdown 或结构化数据生成。
- HTML、Word、PDF 必须白底，正文黑灰色，避免深色背景和复杂装饰。
- 表格需要完整边框、固定列宽或可控换行；长 URL 和中文长词必须允许断行。
- PDF 优先使用 A4 landscape 或足够宽的页面，避免指标表被挤压。
- Word 需要保留标题层级、表格边框和段落间距。

建议渲染链路：维护 `report_input.json` 和 `*.md`；用 `pandoc` 生成 HTML 和 DOCX；用 `weasyprint` 从 HTML 生成 PDF；用 `file`、`pdftotext`、`pandoc -t plain` 检查四件套。
