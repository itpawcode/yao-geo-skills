<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-intent-miner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 四格式输出与防溢出规范

- Word 使用横向 A4：`w:pgSz w:w="16838" w:h="11906" w:orient="landscape"`。
- 左右页边距建议不高于 `850 dxa`，页面可用宽度为 `15138 dxa`。
- 每张 Word 表必须写入 `w:tblW`、`w:tblLayout w:type="fixed"` 和 `w:tblGrid`。
- `w:tblW` 与 `w:tblGrid` 列宽总和不得超过页面可用宽度。
- 不得对 8-10 列宽表使用每列 `2200 dxa` 这类固定大宽度。
- PDF 默认 `@page { size: A4 landscape; }`，表格使用 `table-layout: fixed`、`overflow-wrap: anywhere`，并禁止表格行跨页拆分。
