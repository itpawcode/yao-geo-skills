# 四格式报告排版规范

## 总体

- 白底背景，深色正文，使用清晰层级和足够留白。
- Word、PDF、HTML、Markdown 必须来自同一份 Markdown 内容源。
- 报告首先保证 Word 和 PDF 不溢出，再追求 HTML 视觉丰富度。

## HTML

- 使用 `box-sizing: border-box`。
- 页面主体设置最大宽度，移动端保留安全边距。
- 表格使用 `table-layout: fixed`、`max-width: 100%`、`overflow-wrap: anywhere`。
- `a`、`code`、`pre` 必须允许换行。

## Word

- Word 表格最多 5 列；超过 5 列必须拆表或改成字段块。
- 可见长 URL 改成超链接文字；命令中的长 URL 拆成变量。
- 代码块单行建议控制在 76 字符以内。
- 表格必须可编辑，不能截图化。

## PDF

- 使用 A4 页面和固定页边距。
- 宽表和代码块不得裁切；交付前渲染 PNG 检查右边缘安全带。

## Markdown

- 保留关键表格、代码块、证据台账和优先级。
- Markdown 源文件同样不得出现 6 列及以上宽表。
