# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

CariocaScout is a teaching project for Spec-Driven Development (SDD) + TDD.
It's a small but real daily monitor: flights from Rio (GIG/SDU) to POA,
FLN, NYC, FLR, alerting on price drops ≥25% vs a 30-day moving average,
timed around RJ state/municipal holidays. Read **AGENTS.md** and
**MANUAL.md** before making changes — they are the actual onboarding
docs for this repo and take priority over generic instincts.

## The one rule that matters

**Specs before code.** `openspec/specs/` is the source of truth. Any
behavior change starts with an OpenSpec change folder
(`openspec/changes/<id>/proposal.md` → `design.md` → `tasks.md` →
spec delta), never with a direct edit to `src/`. If a request
contradicts a spec in `openspec/specs/`, say which requirement
conflicts instead of just implementing it. See
`openspec/changes/add-sparkline-trend/` for a worked example frozen
mid-lifecycle, and `openspec/config.yaml` for the project's
non-negotiables.

Load skills from `.opencode/skills/` based on what you're touching:
- any Python in `src/` → `tdd-discipline` (strict red-green-refactor,
  one behavior per test, paste the RED failure before writing GREEN code)
- starting/finishing a feature, or committing → `openspec-git-discipline`
- writing/editing a real price collector in `prices.py` → `scraper-etiquette`
  (official APIs first; if scraping, robots.txt/ToS/backoff/caching are
  non-negotiable)
- touching `docs/` → `dashboard-ipad-first`

## Commands

```bash
python3 -m pytest -q                 # full suite — must be green before every commit
python3 -m pytest tests/test_analysis.py::test_exactly_25_percent_drop_fires  # single test
python3 scripts/run_daily.py         # manual "one cron day" run (uses fakes, no network)
python3 -m http.server -d docs 8000  # dashboard preview at localhost:8000
```

No lint/format/build tooling is configured — stdlib-only core, pytest is the only dependency.

## Architecture

Pure analytical core + ports-and-adapters, wired by one visible orchestration function:

- `analysis.py` — pure functions only (`is_deal`, `moving_average`,
  `has_enough_history`). No clock, no files, no network. This is why
  the whole suite runs in milliseconds and why business-rule edges
  (`>=` vs `>` on the 25% threshold, the cold-start guard) are one-liner tests.
- `prices.py` / `holidays.py` — the flaky outside world (fare data, AI
  holiday endpoint) sits behind `Protocol`s (`PriceProvider`,
  `CalendarProvider`) with deterministic fakes (`FakePriceProvider`,
  `StaticCalendarProvider`). Tests never touch the network — only fakes
  or recorded fixtures.
- `history.py` — versioned temporal store (`PriceHistory`), the append-only
  price series each route/date pair is judged against.
- `config.py` — every business number (origins, destinations, 25%
  threshold, 30-day window, 12-month coverage) lives here as data,
  traced back to a spec requirement in a comment. Change thresholds
  here, not inline in logic.
- `pipeline.py` — `daily_run()` is the entire cron-day business flow
  (calendar → prices → history → analysis → deals) as one readable,
  dependency-injected function, so `tests/test_pipeline.py` can
  simulate a full day in memory. `publish()` isolates the git
  commit/push side effect so it's never invoked from tests.
- `deals.py` — builds and exports `Deal` records to `docs/deals.json`.
  This file is the **only** contract between backend and frontend; its
  exact shape is pinned by
  `tests/test_deals.py::TestExport::test_payload_contract_for_dashboard`.
  Renaming/adding/removing a field is a spec change touching backend +
  frontend + that contract test together, not a solo edit.
- `scripts/run_daily.py` — the only place real adapters get wired in
  (`load_calendar`, `load_price_provider`); ships with fakes by
  default and stays thin by design.
- `docs/` — zero-build GitHub Pages dashboard (`index.html`/`style.css`/`app.js`),
  read-only consumer of `deals.json`. No frameworks, no bundlers, no CDN deps.

Traceability convention: every `openspec/specs/*/spec.md` requirement
has a `#### Scenario:` (GIVEN/WHEN/THEN), and each scenario maps to a
named test (e.g. *"Queda exata de 25% dispara"* → `test_exactly_25_percent_drop_fires`).
When adding a rule, follow that chain end to end rather than just
writing code that happens to work.
