<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-brand-graph
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 质量门槛

- 四件套必须真实存在：Word、PDF、HTML、Markdown。
- Word 必须包含真实 `w:tbl`，表格必须使用固定 `dxa` 表宽，不能使用 `auto`。
- Word 表格网格宽度必须小于正文宽度，并保留右侧安全边距。
- URL、英文实体 ID 和长英文短语必须在 Word 单元格内断行，避免向右溢出。
- PDF 必须可打开、页数大于 0、可抽取文本，页面物理边缘不得出现非白色溢出像素。
