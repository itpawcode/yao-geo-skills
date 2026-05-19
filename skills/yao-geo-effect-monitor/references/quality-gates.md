# Quality Gates

- `SKILL.md`、`templates/brief-template.md`、`evals/trigger_cases.json`、`evals/expected_artifacts.json` 存在。
- registry 中存在同名条目，路径为 `skills/yao-geo-effect-monitor`。
- 示例四件套真实存在：Markdown、HTML、DOCX、PDF。
- 示例四件套结构一致，至少包含执行摘要、监测口径、指标、引用、纠偏、告警、自检。
- 公司专项测试示例必须包含公司测试场景发现、官方事实来源、国内五平台口径和合成/真实采样声明。
- 报告白底、表格有边框、长字段不断版、不溢出。
- DeepSeek、豆包、千问、Kimi、元宝均有独立采样字段。
- 指标体系必须包含候选率、推荐率、描述准确率、引用召回率、引用准确率。
- 归因必须有基线窗口、观察窗口、处理 Prompt、对照 Prompt 和混杂因素记录。
- JSON 文件可被 `python3 -m json.tool` 解析。

- 自检后不得保留 `待文件校验`、`ready_for_file_checks`、`TODO`、`TBD` 或占位标记。
