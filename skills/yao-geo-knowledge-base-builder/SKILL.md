---
name: yao-geo-knowledge-base-builder
description: Build evidence-backed GEO brand knowledge bases from official sites, product pages, help centers, white papers, sales materials, media releases, certifications, and trusted third-party sources. Use when asked to generate reusable brand fact cards, FAQ, prohibited expressions, source indexes, prompt input packs, or Word/PDF/HTML/Markdown four-format Chinese GEO knowledge-base deliverables for Kimi, Qianwen, DeepSeek, Doubao, Yuanbao, content production, monitoring, page design, or customer-service preparation.
---

# yao-geo-knowledge-base-builder

把官网、产品页、帮助中心、白皮书、品牌资料、销售材料、媒体稿和资质文件，整理成可审计、可复用的 GEO 品牌知识库。

## When To Use

Use this skill when the user needs:

- a GEO brand knowledge-base document
- a brand fact-card library with evidence, source, update time, confidence, and use cases
- FAQ and prohibited-expression lists for AI answers and content teams
- prompt input packs for rankings, comparisons, explainers, title generation, content rewrite, page design, monitoring, and customer service
- a Chinese simplified four-format package: Markdown, HTML, Word, and PDF

Do not use this skill for one-off brand copywriting without source evidence, pure competitive ranking articles, page technical audits, or relationship-graph-only work.

## Workflow

1. Define the test scenario and target domestic AI platforms: Kimi, Qianwen, DeepSeek, Doubao, and Yuanbao.
2. Collect and verify sources with official-site-first priority: homepage, product pages, pricing/catalog pages, help center, case pages, white papers, investor/news pages, and authoritative third-party sources.
3. Separate evidence tiers:
   - `A`: official current public sources or legally authoritative documents.
   - `B`: reputable third-party reports or public media with clear dates.
   - `C`: brand self-description without enough operational detail.
   - `D`: unverified or market-specific boundary items that must stay in the pending-confirmation area.
4. Extract brand entities: brand, products, services, team, regions, customers, channels, certifications, technologies, cases, prices, and timeline.
5. Build fact cards. Each card must contain subject, attribute or statement, value, evidence, source ID, update time, confidence level, and reusable scenarios.
6. Build reusable content modules: brand intro, core capabilities, product parameters, applicable scenarios, customer/case notes, FAQ, prohibited expressions, and domestic-market boundary notes.
7. Build the prompt input pack for downstream GEO skills. Strong facts and pending facts must stay separated.
8. Produce version number and update mechanism. High-volatility facts such as prices, AI features, product names, customer counts, and compliance boundaries need explicit review cadence.
9. Render Markdown, HTML, Word, and PDF using the fixed-layout renderer in `scripts/render_four_format.py`.
10. Run quality review and repair before handoff.

## Required Outputs

- GEO brand knowledge-base document
- Brand fact-card library
- FAQ and prohibited-expression list
- Content-generation prompt input pack
- Source index with verification date
- Pending-confirmation list
- Four-format report package: `.md`, `.html`, `.docx`, `.pdf`
- `quality-report.json`

## Layout Rules

Follow `references/four-format-report-layout.md`.

Critical rules:

- White background for HTML, Word, and PDF.
- A4 geometry for Word/PDF.
- No table wider than the printable page body.
- Word tables must use fixed OpenXML layout, `dxa` table width, and grid widths that sum to the printable body width.
- Fact-card tables default to five columns or fewer.
- Source-index URL tables render as a two-column evidence ledger in HTML/PDF/Word to prevent right overflow.
- Long URLs and long English tokens must be soft-wrapped before DOCX generation.
- No `nowrap` table cells.

## Quality Gates

Before completion, verify:

- all four deliverable files exist and are non-empty
- DOCX has fixed tables, A4 body-width `dxa` table widths, no `w:noWrap`, and no unbreakable segment longer than 80 characters
- PDF is readable, preview-rendered, and checked for right-edge visual overflow
- HTML contains no absolute local `/Users/...` paths
- sources retain date, publisher, URL, and confidence tier
- unverified domestic-market claims stay in the pending-confirmation area

## Example

The HubSpot Chinese simplified test output is under:

`examples/hubspot-demo/deliverables/`

Use the renderer like this:

```bash
python3 scripts/render_four_format.py \
  --source examples/hubspot-demo/deliverables/hubspot-demo-geo-knowledge-base.md \
  --out-dir examples/hubspot-demo/deliverables \
  --base-name hubspot-demo-geo-knowledge-base \
  --quality-report examples/hubspot-demo/quality-report.json \
  --preview-dir examples/hubspot-demo/previews
```
