# CariocaScout — Senior Tutor's Manual

*Spec-Driven Development + TDD with OpenCode, OpenSpec and Skills*

You asked me to teach you what the "orchestrated, multi-agent, skill-driven" workflow actually is, minus the YouTube glamour. Here it is, end to end, using a project small enough to hold in your head but real enough to have every problem that matters: flaky external data, a business rule with a sharp edge (25%), a cron job nobody watches, and a frontend contract that breaks silently if you're sloppy.

Read this top to bottom once. Then re-read section 4 with the repo open.

---

## 1. The idea in one paragraph

"Vibe coding" is prompting an agent from a one-line idea straight to code. It works just often enough to be dangerous: a week later nobody remembers *why* a decision was made, because the reasoning lived only in a chat transcript. **Spec-Driven Development (SDD)** inverts that: you and the agent first agree on a written, versioned specification of *what* will be built and *why*; only then does the agent write code, and the code is judged against the spec. **TDD** is the same inversion one level down: agree on the behavior (a failing test) before writing the implementation. SDD disciplines the *feature*; TDD disciplines the *function*. You already practice this instinct in PumpLab — your Phase 0 "define *what* before *how*" pushback is literally SDD; OpenSpec just gives it folders, commands and a lifecycle.

## 2. The three tools and what each one is

**OpenCode** (opencode.ai) — an open-source terminal agent, in the same category as Claude Code. It hosts the LLM session, executes commands, edits files. It reads `AGENTS.md` at the repo root for standing instructions, `opencode.json` for permissions, and loads **skills** from `.opencode/skills/`.

**OpenSpec** (github.com/Fission-AI/OpenSpec) — a lightweight SDD framework. `npx openspec init` scaffolds an `openspec/` directory and installs slash commands into 20+ agents (OpenCode and Claude Code included). It gives you a three-phase lifecycle:

- `/opsx:propose` → creates `openspec/changes/<id>/` with `proposal.md`, `design.md`, `tasks.md` and a *spec delta*
- `/opsx:apply` → the agent implements `tasks.md` against the approved spec
- `/opsx:archive` → folds only the spec delta into `openspec/specs/` (the living source of truth) and discards the scaffolding

**Skills** — small Markdown rulebooks (`SKILL.md` with a YAML `name` + `description` header) that the agent loads *when relevant*. This is the same format Anthropic uses for Claude skills. A skill is not code; it's a tightly-written policy that shapes agent behavior in one phase of work. The "multiagency" you saw in the videos is mostly this: different skills (and sometimes different sub-agents, e.g., one authoring a spec while another adversarially reviews it) activating at different lifecycle phases.

The mental model: **OpenSpec is the process, OpenCode is the worker, skills are the worker's professional habits.**

## 3. A guided tour of this repo

```
carioca-scout/
├── MANUAL.md               ← you are here
├── AGENTS.md               ← standing orders every agent session reads first
├── opencode.json           ← OpenCode permissions (git push asks; rm -rf denied)
├── openspec/
│   ├── config.yaml         ← project context + non-negotiables for the agent
│   ├── specs/              ← THE SOURCE OF TRUTH (4 living specs)
│   │   ├── alerting/           the 25% trigger, moving average, cold-start guard
│   │   ├── price-monitoring/   routes, 12-month window, idempotent daily minimum
│   │   ├── holiday-calendar/   AI ingestion, local bridge-day derivation
│   │   └── dashboard/          deals.json contract, iPad-first rules
│   └── changes/
│       └── add-sparkline-trend/  ← a change FROZEN MID-LIFECYCLE so you can
│                                    study proposal → design → tasks → delta
├── .opencode/skills/
│   ├── tdd-discipline/         red-green-refactor, enforced
│   ├── openspec-git-discipline/ lifecycle gates + commit hygiene
│   ├── scraper-etiquette/      how a real collector must behave
│   └── dashboard-ipad-first/   frontend constraints
├── src/carioca_scout/      ← implementation (pure core + ports & adapters)
├── tests/                  ← 42 tests; every business rule is pinned here
├── docs/                   ← GitHub Pages dashboard (HTML/CSS/JS puro)
├── scripts/run_daily.py    ← cron entrypoint; the only place real adapters wire in
└── cron/crontab.example
```

Three files deserve a slow read:

1. **`openspec/specs/alerting/spec.md`** — notice the format: each `### Requirement:` uses SHALL/SHALL NOT, and each has at least one `#### Scenario:` in GIVEN/WHEN/THEN. Scenarios are the bridge to TDD: every scenario maps to a named test. Look at *"Queda exata de 25% dispara"*, then open `tests/test_analysis.py` and find `test_exactly_25_percent_drop_fires`. That traceability — requirement → scenario → test → code — is the entire payoff of the method.

2. **`openspec/changes/add-sparkline-trend/`** — a worked example of one change. `proposal.md` says *why* and records the questions that were "grilled" out before design. `design.md` records the decision **and the rejected alternatives** (Chart.js rejected because it violates the static-stack requirement — see how specs constrain design?). `tasks.md` is a checklist written in RED/GREEN pairs. The `specs/dashboard/spec.md` inside it is a *delta* — only the modified requirement — which is what `/opsx:archive` folds into the living spec.

3. **`.opencode/skills/tdd-discipline/SKILL.md`** — read the `description:` line carefully. That description is the *trigger*: the agent sees name+description always, and loads the body only when the description matches the task. Writing good descriptions is half the craft of skills ("pushy" descriptions trigger better than timid ones).

## 4. The full workflow, step by step (do this yourself)

### Phase 0 — Setup (once per machine)

```bash
# OpenCode (terminal agent)
curl -fsSL https://opencode.ai/install | bash    # or: npm i -g opencode-ai
opencode auth login                               # pick your model provider

# OpenSpec (spec framework) — run inside the repo
cd carioca-scout
npx openspec@latest init                          # select "OpenCode" when asked
```

`openspec init` will detect the agent and install the `/opsx:*` slash commands. This repo already ships the resulting structure, so you can also just explore it as-is. (Commands and flags evolve fast — trust `npx openspec@latest --help` over any tutorial, including this one.)

### Phase 1 — PROPOSE (spec before code)

Open OpenCode in the repo (`opencode`) and type:

```
/opsx:propose add a minimum-seats filter: ignore fares with fewer than 2 seats available
```

Watch what happens, and *why* it happens:

- The agent reads `AGENTS.md` → which points it to `openspec/` and the skills.
- The **openspec-git-discipline** skill gates it: no `src/` edits are allowed yet.
- It drafts `openspec/changes/add-min-seats-filter/proposal.md` and asks you clarifying questions *before* writing spec deltas (in the polished setups you saw on YouTube, a dedicated "grill-me" skill forces one-question-at-a-time interrogation here).
- **Your job in this phase is to be the difficult reviewer.** Push back exactly like you did in PumpLab Phase 0. Bad proposal → bad everything downstream. This is where senior engineering happens; the typing later is the cheap part.

Approve the proposal only when the requirement has sharp edges: what does "available seats" mean when the provider doesn't report it? (Answer belongs in the spec, not in someone's head.)

### Phase 2 — APPLY (TDD inside the spec)

```
/opsx:apply add-min-seats-filter
```

Now the **tdd-discipline** skill takes over inside each task:

1. **RED** — the agent writes `test_fare_with_one_seat_is_ignored`, runs `pytest -q`, and shows you the failure. *A test that never failed proves nothing.* If it passes immediately, the skill instructs the agent to stop and say so.
2. **GREEN** — the minimum code to pass. Not the prettiest — the minimum.
3. **REFACTOR** — names and structure, with the suite kept green.

Each task ends with a small commit (`test(...)`, `feat(...)`) — the git skill again. You review diffs per task, not one giant "here's the feature" blob.

Notice how the *architecture* of this repo makes TDD cheap, which is not an accident:

- `analysis.py` is **pure** — no clock, no files, no network. Testing `is_deal(300, history)` is a one-liner.
- The messy outside world (airline sites, the AI holiday endpoint) sits behind **Protocols** (`PriceProvider`, `CalendarProvider`) with deterministic fakes. `tests/test_pipeline.py` runs an *entire simulated cron day* in memory in milliseconds.
- The frontend contract is itself a test: `test_payload_contract_for_dashboard` pins the exact field set of `deals.json`. Rename a field in Python and the suite screams before the iPad dashboard ever renders `undefined`.

This is the discipline transfer for PumpLab: your trusted computation core should be the pure center, file/UI/report generation should be adapters behind interfaces, and every API 610 acceptance rule (like your balancing grades) should be a named test pinning a boundary — exactly like `test_exactly_25_percent_drop_fires` pins `>=` vs `>`.

### Phase 3 — ARCHIVE (the spec absorbs the change)

```
/opsx:archive add-min-seats-filter
```

The delta merges into `openspec/specs/price-monitoring/spec.md`; the change folder is retired. Proposal, design and tasks were scaffolding. **The living spec is what future-you and future agents read.** Six months from now, "why do we ignore single-seat fares?" has an answer with a date and a rationale.

### Phase 4 — Run it

```bash
python3 -m pytest -q                      # 42 tests, green
python3 scripts/run_daily.py              # one manual "cron day"
python3 -m http.server -d docs 8000       # open http://localhost:8000 → the dashboard
crontab -e                                # paste cron/crontab.example when ready
```

`run_daily.py` ships with `FakePriceProvider` wired in on purpose. Plugging a real source is *your* first real OpenSpec change — and when you ask the agent to write it, the **scraper-etiquette** skill will force the conversation about official APIs, robots.txt and rate limits before any code appears. That's skills doing their job: encoding judgment you don't want to re-litigate every session.

## 5. Where the "multi-agent" part comes in

Everything above runs fine with a single agent. The orchestration patterns you saw demoed layer on top, in roughly this order of ambition:

1. **Skills per phase** (this repo) — one agent, different rulebooks per lifecycle phase. Do this first; it's 80% of the value.
2. **Parallel changes with git worktrees** — propose several changes on `main`, then run one OpenCode session per change, each in its own `git worktree`, merging back before archive. The git-discipline skill's "every state change crosses main" rule exists precisely to keep this sane.
3. **Adversarial spec authoring** — one sub-agent writes the spec delta, a second (often a different model) attacks it looking for ambiguity and missing scenarios, before you ever see it. Cheap way to reduce single-model bias in the most leveraged artifact.

Don't start at 3. A senior dev with one agent and good specs beats a junior with a swarm.

## 6. Exercises (in order — each one exercises a different muscle)

1. **Read-only:** trace requirement → scenario → test → code for the cold-start guard (alerting spec → `test_cold_start_never_alerts_even_on_crash` → `has_enough_history`). Say out loud where the number 7 lives and why it's not in three places.
2. **TDD only:** add a rule — a deal must also be at least R$80 absolute savings (percentage alone flags cheap-route noise). Write the failing test first, by hand, before asking any agent for anything.
3. **Full lifecycle:** run `/opsx:propose` for exercise 2's rule properly, and go propose → apply → archive. Compare the archived spec with what you'd have documented on your own.
4. **Skill authoring:** write `.opencode/skills/bilingual-output/SKILL.md` enforcing PT-BR user-facing strings + English code identifiers (a rule this repo follows implicitly — make it explicit). You'll reuse that exact skill in PumpLab.
5. **Contract break, on purpose:** rename `drop_pct` to `discount_pct` in `deals.py` only, run the suite, watch which test catches it, then do the rename *correctly* as one OpenSpec change touching backend + frontend + contract test together.

## 7. Honest limits (a senior tells you the downsides)

- **Ceremony tax.** For a throwaway script, SDD is overhead. Use it where change is continuous and memory matters — PumpLab yes, a one-off plot no.
- **Specs rot if you cheat.** One "quick fix" straight to `src/` and the spec is now partially fiction. The git-discipline skill mitigates; your habits decide.
- **Skills are suggestions, not laws.** Agents occasionally ignore them, especially in long sessions. Review diffs. The tests are the only enforcement that can't be sweet-talked.
- **The ecosystem moves monthly.** OpenSpec's schemas/profiles and OpenCode's config have both changed in 2026 alone. Anchor on the *concepts* (spec first, delta lifecycle, skills-as-policy, tests as contract); re-check command syntax against current docs.

## 8. References worth your time

- OpenSpec: `github.com/Fission-AI/OpenSpec` and the docs at intent-driven.dev/knowledge/openspec
- OpenCode: `opencode.ai/docs` (AGENTS.md, skills, permissions)
- Anthropic skills format & engineering blog on writing skills
- Kent Beck, *Test-Driven Development: By Example* — still the book
- "Ports & adapters / hexagonal architecture" (Alistair Cockburn) — the pattern behind `PriceProvider`/`CalendarProvider`

Boa sorte — e lembra: a especificação é o produto; o código é consequência.

— seu tutor
