# yao-geo-execution-roadmap

`yao-geo-execution-roadmap` 用于把 GEO 全景诊断、机会地图和平台采样结论转成 30/60/90 天综合实施方案。

## 适用任务

- GEO 项目启动后，把诊断结果落成可执行计划。
- 给 CEO、市场负责人、增长、内容、技术和客户交付团队同步 90 天节奏。
- 覆盖 DeepSeek、豆包、千问、Kimi、元宝五个平台差异化执行动作。
- 需要默认输出 Markdown、HTML、Word、PDF 四格式报告。

## 核心输出

- GEO 综合实施方案。
- 六个项目包：页面技术、内容矩阵、标题体系、知识库、外部证据、监测闭环。
- 30/60/90 天路线图。
- 角色分工与验收指标表。
- 风险预案和合规节点。

## 示例

- Lingxu 基准样例：`skills/yao-geo-execution-roadmap/examples/lingxu-demo/`
- HubSpot 中文测试样例：`skills/yao-geo-execution-roadmap/examples/hubspot-cn-demo/`

## 生成方式

```bash
python3 skills/yao-geo-execution-roadmap/scripts/render_yao_geo_execution_roadmap.py \
  --input skills/yao-geo-execution-roadmap/examples/hubspot-cn-demo/report_input.json \
  --output-dir skills/yao-geo-execution-roadmap/examples/hubspot-cn-demo
```
