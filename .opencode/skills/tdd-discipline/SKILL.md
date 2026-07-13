---
name: tdd-discipline
description: Enforces red-green-refactor test-driven development on every code change in this repo. Use whenever writing, modifying, or fixing ANY Python code in src/ — even one-line changes, bug fixes, or "trivial" tweaks. Also use when the user asks to "just implement" something quickly: the answer is still test-first.
---

# TDD Discipline

Every behavior change follows red-green-refactor. No exceptions.

## The loop
1. **RED** — Write ONE failing test that pins the new behavior.
   Run `pytest -q` and PASTE the failure into your reply. If the test
   passes immediately, the test is wrong or the behavior already exists:
   stop and say so.
2. **GREEN** — Write the MINIMUM code to pass. Run `pytest -q` again
   and show the green output.
3. **REFACTOR** — Only now improve names/structure. Suite must stay green.

## Rules
- One behavior per test; test names state the business rule
  (`test_exactly_25_percent_drop_fires`, not `test_deal_1`).
- Business edges from openspec/specs/ get boundary tests (>= vs >).
- Pure core: analysis.py takes values, never reads clocks/files/network.
- I/O goes behind a Protocol; tests use fakes (FakePriceProvider,
  StaticCalendarProvider). NEVER hit the network in tests.
- A bug fix starts with a failing test that reproduces the bug.
- Never weaken or delete a test to make it pass without explaining to
  the user which requirement changed — and pointing at the OpenSpec
  change that authorizes it.

## Definition of done
`pytest -q` fully green + every new requirement traceable to a test.
