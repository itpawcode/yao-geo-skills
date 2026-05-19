# 品牌对比报告版式

- Markdown：内容母版，语义化标题、中文字段和标准 Markdown 表格。
- HTML：白底、最大宽度受控、响应式表格、边框对齐、长文本可换行。
- PDF：从已校验 HTML 渲染，A4 页面、白底、合理页边距，避免表格跨页错位。
- Word：使用 `.docx`，保持与 Markdown/HTML 同一章节结构，标题、正文和表格边框必须可读；必须显式设置 A4、左右页边距、表格总宽、列宽、单元格内边距和边框。
- 四格式必须从单一内容结构生成；只能改变布局，不能删减章节、表格、FAQ、来源或自检记录。
- HTML/PDF/Word 中超过 4 列的长表必须拆成多张窄表。
- DOCX 表格不得依赖 Word 自动伸缩。生成后检查每张表的 `tblGrid` 宽度总和必须小于等于正文可用宽度；如果有一张表超过可用宽度，必须缩短字段、拆表或重设列宽后重新生成。

```css
body { background: #fff; color: #1f2933; line-height: 1.68; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
th, td { border: 1px solid #d7dde5; padding: 10px 12px; vertical-align: top; overflow-wrap: anywhere; }
```
