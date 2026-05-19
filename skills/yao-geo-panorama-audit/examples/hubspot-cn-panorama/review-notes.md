<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-panorama-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# 示例报告自检记录

- 自检日期：2026-05-19
- 示例性质：公开事实 + 国内 AI 平台测试样本，不代表真实平台长期结论
- 版式基准：kami 专业文档纪律 + 白底报告约束

| 检查项 | 结果 | 说明 |
| --- | --- | --- |
| hubspot-cn-panorama-audit.md | 通过 | 文件存在且非空 |
| hubspot-cn-panorama-audit.html | 通过 | 文件存在且非空 |
| hubspot-cn-panorama-audit.docx | 通过 | 文件存在且非空 |
| hubspot-cn-panorama-audit.pdf | 通过 | 文件存在且非空 |
| HTML 白底 | 通过 | 白底与浅色模式存在 |
| HTML 防溢出 | 通过 | 表格与长文本防溢出规则存在 |
| 中文字段 | 通过 | 核心字段为中文简体 |
| 问题覆盖 | 通过 | 九类意图覆盖矩阵存在 |
| 格式一致 | 通过 | HTML 与 Markdown 章节一致 |
| Word 表格结构 | 通过 | 检测到 11 张表格 |
| Word 表格宽度 | 通过 | 最大表宽约 15.5cm |
| PDF 无本地路径页脚 | 通过 | 未检测到浏览器默认路径页脚 |

## 自检结论
四种格式均已生成；HTML/PDF 采用白底报告版式，表格设置固定布局与长文本换行；Word 使用标题样式、显式列宽、固定表格网格、表格边框和中文字段，密集 8 列表已按 Word 版拆成窄表。
受本机缺少 LibreOffice 影响，未执行 DOCX 页面图片渲染检查；已完成结构与文件完整性检查。
