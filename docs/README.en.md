# Yao GEO Skills

Reusable skills for `GEO` (`Generative Engine Optimization`) workflows.

In this repository, `GEO` means Generative Engine Optimization, not geographic information systems.

Visual catalog:
[index.html](../index.html)

## Current Inventory

The repository currently contains `17` GEO-related skills.

| Family | Count | Skills |
|---|---:|---|
| `geo-operations` | 3 | `yao-geoflow-cli`, `yao-geoflow-template`, `yao-geoflow-design` |
| `geo-strategy` | 2 | `yao-geo-panorama-audit`, `yao-geo-execution-roadmap` |
| `geo-page-technical` | 2 | `yao-geo-page-audit`, `yao-geo-page-blueprint` |
| `geo-content-production` | 5 | `yao-geo-title-optimizer`, `yao-geo-explainer-builder`, `yao-geo-comparison-builder`, `yao-geo-content-refiner`, `yao-geo-ranking-article-builder` |
| `geo-knowledge-assets` | 2 | `yao-geo-brand-graph`, `yao-geo-knowledge-base-builder` |
| `geo-measurement` | 2 | `yao-geo-tracking`, `yao-geo-effect-monitor` |
| `geo-research` | 1 | `yao-geo-intent-miner` |

## Skill Catalog

| Skill | Type | What it does | Links |
|---|---|---|---|
| `yao-geoflow-cli` | Operations | Operates an existing GEOFlow system through the local CLI or Laravel API fallback. | [Package](../skills/yao-geoflow-cli) / [Guide](skills/yao-geoflow-cli.md) |
| `yao-geoflow-template` | Operations | Maps a reference URL onto GEOFlow frontend modules and prepares a preview-first theme package plan. | [Package](../skills/yao-geoflow-template) / [Guide](skills/yao-geoflow-template.md) |
| `yao-geoflow-design` | Operations | Discovers and preview-edits GEOFlow Laravel Blade themes without changing business logic or data contracts. | [Package](../skills/yao-geoflow-design) / [Guide](skills/yao-geoflow-design.md) |
| `yao-geo-panorama-audit` | Strategy | Builds a brand GEO baseline, AI-answer visibility diagnosis, competitor gap map, and opportunity roadmap. | [Package](../skills/yao-geo-panorama-audit) / [Guide](skills/yao-geo-panorama-audit.md) |
| `yao-geo-execution-roadmap` | Strategy | Turns GEO diagnosis and opportunity maps into a 30/60/90-day execution plan. | [Package](../skills/yao-geo-execution-roadmap) / [Guide](skills/yao-geo-execution-roadmap.md) |
| `yao-geo-page-audit` | Page technical | Audits page crawlability, structure, content signals, and AI extractability. | [Package](../skills/yao-geo-page-audit) / [Guide](skills/yao-geo-page-audit.md) |
| `yao-geo-page-blueprint` | Page technical | Produces GEO-friendly page architecture, semantic HTML, schema, CMS fields, and layout guidance. | [Package](../skills/yao-geo-page-blueprint) / [Guide](skills/yao-geo-page-blueprint.md) |
| `yao-geo-title-optimizer` | Content production | Generates GEO title candidates, scorecards, compliance checks, and title-to-article mappings. | [Package](../skills/yao-geo-title-optimizer) / [Guide](skills/yao-geo-title-optimizer.md) |
| `yao-geo-explainer-builder` | Content production | Builds GEO explainers, how-to guides, FAQs, glossaries, and brand insertion guidance. | [Package](../skills/yao-geo-explainer-builder) / [Guide](skills/yao-geo-explainer-builder.md) |
| `yao-geo-comparison-builder` | Content production | Creates fair, evidence-bound brand comparisons, alternatives pages, and comparison FAQs. | [Package](../skills/yao-geo-comparison-builder) / [Guide](skills/yao-geo-comparison-builder.md) |
| `yao-geo-content-refiner` | Content production | Refines existing SEO or brand content into structured, verifiable, AI-citable GEO content. | [Package](../skills/yao-geo-content-refiner) / [Guide](skills/yao-geo-content-refiner.md) |
| `yao-geo-ranking-article-builder` | Content production | Generates evidence-backed ranking and review articles with four-format deliverables. | [Package](../skills/yao-geo-ranking-article-builder) / [Guide](skills/yao-geo-ranking-article-builder.md) |
| `yao-geo-brand-graph` | Knowledge assets | Turns company materials into auditable brand entity graphs and evidence ledgers. | [Package](../skills/yao-geo-brand-graph) / [Guide](skills/yao-geo-brand-graph.md) |
| `yao-geo-knowledge-base-builder` | Knowledge assets | Builds GEO brand knowledge bases, fact cards, FAQ, prohibited expressions, and prompt input packs. | [Package](../skills/yao-geo-knowledge-base-builder) / [Guide](skills/yao-geo-knowledge-base-builder.md) |
| `yao-geo-tracking` | Measurement | Designs company-specific GEO backend tracking and attribution plans. | [Package](../skills/yao-geo-tracking) / [Guide](skills/yao-geo-tracking.md) |
| `yao-geo-effect-monitor` | Measurement | Designs GEO signal monitoring, AI answer sampling, citation tracking, and monthly reporting loops. | [Package](../skills/yao-geo-effect-monitor) / [Guide](skills/yao-geo-effect-monitor.md) |
| `yao-geo-intent-miner` | Research | Expands seed terms and business context into AI-search question sets, intent clusters, follow-up chains, and monitoring prompts. | [Package](../skills/yao-geo-intent-miner) / [Guide](skills/yao-geo-intent-miner.md) |

## Repository Contract

Each published skill should include:

- `SKILL.md`
- `manifest.json`
- `templates/brief-template.md`
- `evals/trigger_cases.json`
- `evals/expected_artifacts.json`
- a human-readable guide under `docs/skills/`

Run validation before publishing:

```bash
python3 scripts/validate_repository.py
```
