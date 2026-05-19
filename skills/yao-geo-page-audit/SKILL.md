---
name: yao-geo-page-audit
description: Diagnose a website page or small page set for GEO readiness, including crawlability, renderability, semantic structure, content evidence, AI extractability, schema consistency, and four-format Chinese report delivery.
metadata:
  owner: Yao Team
  family: geo-page-technical
  maturity: beta
  requires_web: true
  default_outputs: Word, PDF, HTML, Markdown
---

# yao-geo-page-audit

Use this skill when the user wants a GEO Page Audit, website/page GEO diagnosis, page technical audit, AI extractability audit, schema/HTML module advice, or code/content repair list for a URL.

## Job

Given a target URL or website, diagnose the homepage, a representative first-level page, and a representative second-level page when possible. Output development-ready and content-ready recommendations that improve how public pages can be retrieved, parsed, cited, and summarized by search-driven AI systems.

## Workflow

1. Read `references/research-foundation.md` and frame the audit as a four-stage chain: retrieval candidate, main-content extraction, evidence quality, generated citation.
2. Identify page type and sample scope. If the input is a homepage, select homepage, one representative first-level page, and one representative second-level page. State the selection basis.
3. Check crawlability and renderability: status code, robots, canonical, meta robots, mobile render, JavaScript dependency, and whether primary content appears in initial HTML.
4. Check structural quality: H1-H3, summary, table of contents, FAQ, tables, lists, breadcrumbs, internal links, anchor text, and schema.
5. Check content evidence: conclusions first, full entity names, data, citations, cases, dates, author/source, price, and service boundaries.
6. Check AI extractability: key-value facts, atomic facts, comparison tables, steps, Q&A, context-independent summary, and paragraph independence.
7. Produce code-layer fixes, content-layer fixes, page-module suggestions, schema/HTML snippets, priority, owner, acceptance test, and estimated cost.
8. Deliver Word, PDF, HTML, and Markdown from one Markdown content source. Follow `references/report-formatting-spec.md` and `references/output-layout-policy.md`.
9. Run `scripts/review_report_layout.py` and `references/quality-gates.md` before claiming completion.

## Boundaries

- Without crawl/log access, only report front-end observable evidence. Do not infer log-level crawl frequency.
- Distinguish user-visible content, crawler-readable content, and AI-extractable content.
- Schema must match page body facts. Do not use schema to invent facts absent from the page.
- Domestic AI platform adaptation should consider search results, public webpages, news pages, encyclopedia pages, WeChat public articles, documentation, and help-center pages as possible answer material.

## Outputs

- Page GEO diagnosis report.
- Code-layer repair checklist.
- Content-structure remodeling advice.
- Schema and HTML module suggestions.
- Default four-piece deliverable: Word, PDF, HTML package, Markdown.
- `quality-report.json` with artifact existence, byte size, and layout checks.
