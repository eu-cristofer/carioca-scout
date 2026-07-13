---
name: openspec-git-discipline
description: Governs the OpenSpec lifecycle (propose/apply/archive) and git hygiene in this repo. Use whenever starting a new feature, changing behavior, editing anything under openspec/, committing, or when the user asks to "add" or "change" functionality — the first step is a proposal, not code.
---

# OpenSpec + Git Discipline

## Lifecycle gates
1. **Propose first.** Any behavior change starts as
   `openspec/changes/<change-id>/` with proposal.md (+ design.md when
   architecture is involved, + tasks.md). NEVER edit src/ for a change
   that has no proposal. Ask the user to approve the proposal before
   touching code.
2. **Apply against the spec.** Implement tasks.md in order, TDD-style
   (see tdd-discipline skill). Check items off as you complete them.
3. **Archive.** After the code is merged and green, fold ONLY the spec
   delta into openspec/specs/ and delete/archive the change folder.
   proposal/design/tasks are scaffolding — the living spec is the truth.

## Git rules
- Small commits, one lifecycle phase each:
  `spec(<id>): propose ...` / `feat(<id>): ...` / `test(<id>): ...` /
  `spec(<id>): archive ...`
- A change's proposal must be committed before implementation commits.
- Never commit with a red test suite. Run `pytest -q` before EVERY commit.
- data/price_history.json is machine-written state — never hand-edit;
  docs/deals.json is committed only by the pipeline or by intentional
  sample updates.

## Conflict rule
If the user asks for code that contradicts openspec/specs/, stop and
say which requirement conflicts; offer to open a change proposal.
