<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-explainer-builder
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式报告版式

## 共用规则

- 白底背景，不使用渐变、深色底或装饰性大色块。
- Markdown、HTML、Word、PDF 必须来自同一 section spec，标题集合必须一致。
- 表格边框对齐，行高稳定，单元格留白适中。
- 长中文句、URL、英文产品名、参数串必须自动换行。

## HTML 与 PDF

- HTML 使用 `background:#ffffff`、`border-collapse:collapse`、`overflow-wrap:anywhere`。
- 表格外层使用横向滚动容器，移动端不挤压正文。
- PDF 由 HTML 渲染，使用 A4 页面和稳定页边距。

## Word

- A4：`11906 x 16838 dxa`。
- 左右页边距：`1134 dxa`。
- 可用正文宽度：`9638 dxa`。
- 表格必须固定布局，`tblW` 和 `gridCol` 宽度总和不得超过 `9638 dxa`。
- 单元格内长 ASCII token 需要插入软换行，避免向右侧溢出。
- 每次生成后检查 `word/document.xml` 中表格宽度、长 token 和必备标题。
