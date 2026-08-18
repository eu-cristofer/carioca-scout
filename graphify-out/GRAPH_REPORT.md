# Graph Report - .  (2026-08-18)

## Corpus Check
- Corpus is ~8,920 words - fits in a single context window. You may not need a graph.

## Summary
- 206 nodes · 405 edges · 11 communities (9 shown, 2 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 71 edges (avg confidence: 0.78)
- Token cost: 90,938 input · 0 output

## Community Hubs (Navigation)
- Docs, Skills & Governance
- Deal Analysis Rules
- Config, Deals Export & Pipeline Core
- Price History Store
- Holiday Calendar & Travel Windows
- Price Providers & Daily Run Loop
- OpenCode Permissions
- Cron Entrypoint & Publish
- Dashboard Frontend (app.js)
- Package Init
- Package Metadata

## God Nodes (most connected - your core abstractions)
1. `MANUAL.md — Senior Tutor's Manual` - 24 edges
2. `daily_run()` - 21 edges
3. `PriceHistory` - 13 edges
4. `FakePriceProvider` - 12 edges
5. `moving_average()` - 11 edges
6. `is_deal()` - 11 edges
7. `StaticCalendarProvider` - 10 edges
8. `derive_window()` - 10 edges
9. `export_deals()` - 9 edges
10. `TestBridgeDerivation` - 9 edges

## Surprising Connections (you probably didn't know these)
- `dashboard-ipad-first SKILL.md` --semantically_similar_to--> `SVG polyline sparkline design decision (vs Chart.js/braille)`  [INFERRED] [semantically similar]
  .opencode/skills/dashboard-ipad-first/SKILL.md → openspec/changes/add-sparkline-trend/design.md
- `scraper-etiquette SKILL.md` --semantically_similar_to--> `Spec: Price Monitoring`  [INFERRED] [semantically similar]
  .opencode/skills/scraper-etiquette/SKILL.md → openspec/specs/price-monitoring/spec.md
- `load_calendar()` --calls--> `StaticCalendarProvider`  [INFERRED]
  scripts/run_daily.py → src/carioca_scout/holidays.py
- `load_price_provider()` --calls--> `FakePriceProvider`  [INFERRED]
  scripts/run_daily.py → src/carioca_scout/prices.py
- `main()` --calls--> `daily_run()`  [INFERRED]
  scripts/run_daily.py → src/carioca_scout/pipeline.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **add-sparkline-trend OpenSpec change lifecycle documents** — openspec_changes_add_sparkline_trend_proposal_doc, openspec_changes_add_sparkline_trend_design_doc, openspec_changes_add_sparkline_trend_tasks_doc, openspec_changes_add_sparkline_trend_specs_dashboard_spec_doc [EXTRACTED 1.00]
- **Four .opencode skills governing agent behavior in this repo** — _opencode_skills_dashboard_ipad_first_skill_doc, _opencode_skills_openspec_git_discipline_skill_doc, _opencode_skills_scraper_etiquette_skill_doc, _opencode_skills_tdd_discipline_skill_doc [EXTRACTED 1.00]
- **Four living OpenSpec specs forming the project's source of truth** — openspec_specs_alerting_spec_doc, openspec_specs_dashboard_spec_doc, openspec_specs_holiday_calendar_spec_doc, openspec_specs_price_monitoring_spec_doc [EXTRACTED 1.00]

## Communities (11 total, 2 thin omitted)

### Community 0 - "Docs, Skills & Governance"
Cohesion: 0.17
Nodes (32): dashboard-ipad-first SKILL.md, iPad-first responsive layout rules, openspec-git-discipline SKILL.md, OpenSpec propose/apply/archive lifecycle, scraper-etiquette SKILL.md, tdd-discipline SKILL.md, TDD red-green-refactor loop, CalendarProvider Protocol (+24 more)

### Community 1 - "Deal Analysis Rules"
Cohesion: 0.09
Nodes (16): has_enough_history(), is_deal(), moving_average(), price_delta(), Analytical core: moving average, price delta and the 25% trigger.  This module i, Mean of the last `window` observations (or all, if fewer).      REQ alerting#2:, Relative variation of `current` vs `baseline`.      Negative = price dropped. -0, True iff `current` is at least `threshold` below the moving average.      REQ al (+8 more)

### Community 2 - "Config, Deals Export & Pipeline Core"
Cohesion: 0.11
Nodes (19): datetime, Path, Business-rule configuration for CariocaScout.  Every number here traces back to, ScoutConfig, build_deal(), Deal, export_deals(), Path (+11 more)

### Community 3 - "Price History Store"
Cohesion: 0.10
Nodes (12): Observation, PriceHistory, date, Path, Local temporal store: price_history.json.  Schema (versioned so future migration, Record today's minimum. Idempotent per (route, observed_on):         keeps the L, Chronological daily-minimum series for one route., route_key() (+4 more)

### Community 4 - "Holiday Calendar & Travel Windows"
Cohesion: 0.15
Nodes (15): CalendarProvider, derive_window(), Holiday, Protocol, Holiday-calendar ingestion (REQ holiday-calendar spec).  The spec says: "consume, A holiday plus its derived bridge days — the dates worth pricing., Deterministic provider: loads holidays from a local JSON file.      File format:, Expand a holiday into the travel window including bridge days.      Rules (pinne (+7 more)

### Community 5 - "Price Providers & Daily Run Loop"
Cohesion: 0.17
Nodes (12): daily_run(), date, One cron tick. Returns the deals found (already exported)., FakePriceProvider, date, Quote, Cheapest fare found today for one route/date, or None if         the source had, Deterministic double for tests: returns scripted quotes. (+4 more)

### Community 6 - "OpenCode Permissions"
Cohesion: 0.20
Nodes (9): *, git push, rm -rf *, instructions, permission, bash, edit, $schema (+1 more)

### Community 7 - "Cron Entrypoint & Publish"
Cohesion: 0.28
Nodes (8): load_calendar(), load_price_provider(), main(), Production would call the AI endpoint here and cache the JSON;     on failure we, Swap in a real PriceProvider adapter here.     Read .opencode/skills/scraper-eti, publish(), Path, Commit and push deals.json (REQ ci-cd). Isolated so tests never     run git; scr

### Community 8 - "Dashboard Frontend (app.js)"
Cohesion: 0.43
Nodes (7): brl(), CIDADES, dataBr(), main(), renderCard(), renderMessage(), sparklinePoints()

## Knowledge Gaps
- **10 isolated node(s):** `CIDADES`, `$schema`, `AGENTS.md`, `edit`, `git push` (+5 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `daily_run()` connect `Price Providers & Daily Run Loop` to `Deal Analysis Rules`, `Config, Deals Export & Pipeline Core`, `Price History Store`, `Holiday Calendar & Travel Windows`, `Cron Entrypoint & Publish`?**
  _High betweenness centrality (0.136) - this node is a cross-community bridge._
- **Why does `PriceHistory` connect `Price History Store` to `Config, Deals Export & Pipeline Core`, `Price Providers & Daily Run Loop`?**
  _High betweenness centrality (0.119) - this node is a cross-community bridge._
- **Why does `is_deal()` connect `Deal Analysis Rules` to `Config, Deals Export & Pipeline Core`, `Price Providers & Daily Run Loop`?**
  _High betweenness centrality (0.069) - this node is a cross-community bridge._
- **Are the 7 inferred relationships involving `daily_run()` (e.g. with `main()` and `seed_history()`) actually correct?**
  _`daily_run()` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `PriceHistory` (e.g. with `store()` and `TestPersistence`) actually correct?**
  _`PriceHistory` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Are the 8 inferred relationships involving `FakePriceProvider` (e.g. with `load_price_provider()` and `seed_history()`) actually correct?**
  _`FakePriceProvider` has 8 INFERRED edges - model-reasoned connections that need verification._
- **What connects `CIDADES`, `$schema`, `AGENTS.md` to the rest of the system?**
  _10 weakly-connected nodes found - possible documentation gaps or missing edges._