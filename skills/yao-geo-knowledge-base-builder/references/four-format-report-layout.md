# Four-Format Report Layout

This skill produces Markdown, HTML, Word, and PDF reports. The visual formats must be readable as client-facing documents, not raw Markdown exports.

## Page System

- Background: white.
- PDF and Word: A4 portrait.
- Page margin: about 18-20 mm.
- Body text: Chinese serif/sans fallback with stable line height around 1.55-1.65.
- Headings: ink-blue hierarchy, restrained spacing, no decorative gradient.
- Tables: borders aligned, cells top-aligned, no clipped text.

## Table Rules

- Use `table-layout: fixed` and `overflow-wrap: anywhere` in HTML/PDF.
- Use fixed OpenXML table layout in DOCX:
  - `w:tblLayout w:type="fixed"`
  - `w:tblW w:type="dxa"`
  - each `w:gridCol` sum must not exceed printable body width
  - no `w:noWrap`
- Keep fact-card tables to five columns by default. If source Markdown contains a wider fact-card table, visual formats must compact it to:
  - fact ID
  - subject
  - fact statement
  - confidence/source
  - scenario
- Do not render eight-column fact-card tables in Word/PDF.
- Render source indexes with URLs as two-column evidence ledgers in HTML/PDF/Word:
  - source
  - evidence detail including publisher, type, verification date, and URL
- Long URLs and long English tokens must receive soft breakpoints before DOCX generation.

## Overflow Self-Review

Run these checks after every render:

1. All four files exist.
2. DOCX tables are fixed layout and use A4 body-width `dxa`.
3. DOCX has no `w:noWrap`.
4. DOCX has no unbreakable text segment longer than 80 characters after soft-break handling.
5. PDF opens and has at least one page.
6. PDF preview PNGs are generated.
7. PDF preview PNGs show no right-edge ink in the page edge scan.
8. HTML contains no absolute local `/Users/...` paths.

If any check fails, repair the renderer or report structure and rerun the full four-format build.
