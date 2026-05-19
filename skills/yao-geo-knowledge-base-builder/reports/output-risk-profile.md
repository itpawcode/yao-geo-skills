# Output Risk Profile

## High-Risk Failures

- Treating a knowledge base as a long brand introduction instead of reusable fact cards.
- Mixing brand self-description, official evidence, third-party evidence, and pending facts into one confidence level.
- Omitting source IDs, verification dates, or update cadence.
- Letting wide fact-card/source-index tables overflow in Word or PDF.
- Copying unverified China-market claims into the strong-evidence or prompt-input area.

## Controls

- Official-source-first evidence collection.
- A/B/C/D confidence tiers with pending-confirmation separation.
- Mandatory fact cards with source ID, update time, confidence, and use scenario.
- Fixed-layout four-format renderer with DOCX and PDF overflow checks.
- Prohibited-expression section for claims that cannot be safely reused.

## Review Signals

- `quality-report.json` must pass.
- DOCX must report fixed tables, body-width `dxa`, no `w:noWrap`, and no long unbreakable token.
- PDF must be preview-rendered and pass the right-edge scan.
- Source index must keep publisher, source type, verification date, and URL.
