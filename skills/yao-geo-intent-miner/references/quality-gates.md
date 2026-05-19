<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 质量门

- DOCX 可读，包含 `word/document.xml`。
- DOCX 每张表的 `w:tblW` 不超过页面可用宽度。
- DOCX 每张表的 `w:tblGrid` 列宽总和不超过页面可用宽度。
- DOCX 每张表都使用 `w:tblLayout w:type="fixed"`。
- PDF 为横向 A4。
- PDF 渲染 PNG 后右侧边缘不得出现非空白内容贴边。
