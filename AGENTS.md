# AGENTS.md — instructions for AI agents working in this repo

You are working on **CariocaScout**. Before writing ANY code:

1. Read `openspec/config.yaml` and the specs under `openspec/specs/`.
   They are the source of truth. Code that contradicts a spec is a bug
   even if it "works".
2. Load the relevant skills from `.opencode/skills/`:
   - touching any Python in `src/` → **tdd-discipline**
   - starting/finishing a feature, committing → **openspec-git-discipline**
   - writing a real data collector → **scraper-etiquette**
   - touching `docs/` → **dashboard-ipad-first**
3. New behavior starts with `/opsx:propose` (an OpenSpec change folder),
   never with code. See `openspec/changes/add-sparkline-trend/` for a
   worked example of the lifecycle.

## Commands
- Test: `python3 -m pytest -q` (must be green before every commit)
- Daily pipeline (manual run): `python3 scripts/run_daily.py`
- Dashboard preview: `python3 -m http.server -d docs 8000`

## Architecture in one paragraph
Pure analytical core (`analysis.py`) + versioned temporal store
(`history.py`) + I/O behind Protocols (`prices.py`, `holidays.py`) +
one visible orchestration function (`pipeline.py`). `deals.json` is the
only backend↔frontend contract; its shape is pinned by
`tests/test_deals.py::TestExport::test_payload_contract_for_dashboard`.
