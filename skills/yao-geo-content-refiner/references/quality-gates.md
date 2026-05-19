<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-content-refiner
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 质量门

## 内容质量门

- 必须包含原文 GEO 评分、改造版文章、差异报告、原子事实卡、FAQ、理论映射、证据账本和 CMS HTML 建议。
- 新增事实必须有来源或证据状态，弱证据不得写成强结论。
- 医疗、金融、法律等敏感领域必须保留限制条件。

## Word/PDF 排版质量门

- 四格式文件必须真实存在且非空。
- Word 必须检查所有表格 `tblGrid` 总宽，任何表格都不得大于页面可用宽度。
- Word 中超过 4 列的表格必须转成纵向事实卡，不允许 6-8 列宽表直接输出。
- Word 长 URL 必须可换行，不得向右穿出单元格。
- PDF 必须渲染成 PNG，并检查右侧留白；不得出现文字或表格贴边、裁切、乱码。
- HTML 必须白底、表格可横向滚动、无本地绝对路径。

## 失败处理

发现任一右溢出、贴边、裁切、表格过窄或长 URL 穿出页面时，必须先修渲染逻辑并重新生成 Word/PDF/HTML/Markdown，不能只手工改单个文件。
