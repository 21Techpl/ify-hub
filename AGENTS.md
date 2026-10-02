# AGENTS.md — ify-hub

Worker router. Read BEFORE any code change.

## Invariants
- Feature branches only; never push `main` (protected).
- TDD (pytest): failing test first. The Tuya cloud client is mocked in tests; no live API calls in CI.
- Secrets ONLY in `.env` (gitignored); config via env vars; never log secrets.
- Device DP handling ONLY in `src/adapters/tuya/`; route handlers stay device-agnostic (contract models).
- Verify before requesting review: `pytest -q` green + server boots (`uvicorn` smoke) — report actual output.
- Sources of truth: Hermes Kanban (task card), contract version in `vendor/VERSION`.
