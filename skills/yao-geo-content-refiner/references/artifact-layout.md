<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-content-refiner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 内容改造报告版式

## 四格式规则

- Markdown：审阅母版，保留标准 Markdown 表格。
- HTML：白底、最大宽度受控，宽表使用横向滚动；`overflow-wrap:anywhere` 和 `word-break:break-word` 必须开启。
- Word：默认使用横向 A4、固定表宽、显式列宽；不使用自动列宽。
- PDF：A4 白底，可复制中文文本，表格或事实卡不得贴近页面右边界。

## Word 防右溢出规则

- 页面使用横向 A4，左右边距 1.35 cm。
- 表格总宽使用安全值 `15260 dxa`，必须小于页面可用宽度。
- 4 列及以下使用固定宽度表格；短字段列压窄，说明列加宽。
- 超过 4 列的表格转成纵向事实卡：每条记录是一个两列表格，左列为字段名，右列为内容。
- 长 URL 在 Word/PDF 中插入可换行空格，避免单词级右溢出。
- 行高不固定，允许内容自然换行；禁止使用固定行高截断内容。

## PDF 防溢出规则

- PDF 生成后必须用 `pdftoppm` 渲染为 PNG。
- 检查每页右侧非白像素边界，右边留白应为正且稳定，不得贴到页面边缘。
- 宽表同样转成纵向事实卡，避免 6-8 列表格在 PDF 中过窄或裁切。

## 自检命令建议

```bash
pdftoppm -png -r 130 report.pdf tmp/page
```

Word 结构检查应读取 `word/document.xml` 中 `w:pgSz`、`w:pgMar` 和每张表的 `w:tblGrid/w:gridCol`，确保表格总宽小于可用宽度。
