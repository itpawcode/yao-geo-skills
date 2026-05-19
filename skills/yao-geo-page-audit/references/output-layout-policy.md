# 输出排版防溢出策略

## Word 优先规则

- 报告源 Markdown 中不得出现 6 列及以上表格；超过 5 列时必须拆成 5 列以内表格，或改成“问题卡片 + 字段列表”。
- Word 可见文本中不得出现 42 字符以上的英文、URL 或代码连续 token；长 URL 必须改为超链接文字，命令中的长 URL 必须拆成变量和路径片段。
- 代码块单行建议控制在 76 字符以内；确实需要长命令时使用 shell 变量或分行。
- DOCX 表格必须固定在页面正文宽度内，不允许依赖 Word 自动扩宽。
- Word 报告优先可读性；宽表在 Word 中可以与 HTML/PDF 使用不同版式。

## HTML/PDF 规则

- 表格使用 `table-layout: fixed`、`max-width: 100%`、`overflow-wrap: anywhere`。
- `a`、`code`、`pre` 必须允许换行，避免裸 URL、schema、命令右溢。
- PDF 使用 A4 页面和固定页边距；最终必须渲染 PNG 页面检查右边缘。

## 自动质检门

- Markdown：检查 `|` 表格列数，任一表格超过 5 列即失败。
- DOCX：解析 `word/document.xml`，最大表格列数超过 5 即失败。
- DOCX：可见 URL 连续 token 超过 40 字符即失败。
- PDF：使用 `pdftoppm` 渲染页面，最右侧安全带不得出现文本或表格边框。
- 四件套必须重新生成后再写入 `quality-report.json`。
