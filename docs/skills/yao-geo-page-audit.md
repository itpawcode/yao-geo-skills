<!--
Copyright © 2026 姚金刚. All rights reserved.
Project: yao-geo-page-audit
Created by: 姚金刚
Date: 2026-05-16
X: https://x.com/yaojingang
-->

# yao-geo-page-audit

`yao-geo-page-audit` 是页面技术类 GEO skill，用于输入网址后诊断首页、代表性一级页和二级页，输出代码层与内容层优化建议，并默认支持 Word、PDF、HTML、Markdown 四件套交付。

## 使用场景

- 诊断官网首页、栏目页、产品页、文章页、帮助中心和文档页的 GEO 准备度。
- 检查页面是否可抓取、正文是否可读、结构是否清晰、事实是否可切片引用。
- 输出开发可执行的 HTML、schema、渲染、移动端和 CMS 字段建议。
- 生成国内 AI 平台适配视角的中文简体交付报告。

## 示例报告

合成示例：

- [Markdown](../../skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.md)
- [HTML](../../skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.html)
- [Word](../../skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.docx)
- [PDF](../../skills/yao-geo-page-audit/examples/example-site-demo/example-site-geo-page-audit.pdf)

HubSpot 国内 AI 平台测试示例：

- [Markdown](../../skills/yao-geo-page-audit/examples/hubspot-domestic-ai-demo/hubspot-geo-page-audit.md)
- [HTML](../../skills/yao-geo-page-audit/examples/hubspot-domestic-ai-demo/hubspot-geo-page-audit.html)
- [Word](../../skills/yao-geo-page-audit/examples/hubspot-domestic-ai-demo/hubspot-geo-page-audit.docx)
- [PDF](../../skills/yao-geo-page-audit/examples/hubspot-domestic-ai-demo/hubspot-geo-page-audit.pdf)

## 质量门

- 必须覆盖可抓取性、结构规范性、内容信号、AI 可抽取性和证据质量。
- 必须区分用户可见内容、爬虫可读内容和 AI 可抽取内容。
- 代码层建议必须给字段、代码片段或复测命令。
- schema 必须与页面正文事实一致。
- Word 表格最多 5 列；长 URL 和长命令必须拆分，防止向右溢出。
- PDF 交付前必须渲染检查右边缘安全带。
