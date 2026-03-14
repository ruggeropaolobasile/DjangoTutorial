# Consolidate Preflight Checks Across Script, Docs, and PR Workflow

This ExecPlan is a living document. The sections `Progress`, `Surprises & Discoveries`, `Decision Log`, and `Outcomes & Retrospective` must be kept up to date as work proceeds.

This plan must be maintained in accordance with `agent-docs/PLANS.md`.

## Purpose / Big Picture

After this change, contributors can rely on a single documented preflight flow that matches the actual script behavior, the repository guidance, and the PR expectations. Success is observable when `scripts/preflight.ps1` runs the intended checks, the onboarding docs describe the same flow, and a new session can follow the process without reading prior chat history.

## Progress

- [x] (2026-03-14 19:56 Europe/Rome) Initial draft created.
- [ ] (YYYY-MM-DD HH:MM TZ) Implementation started.
- [ ] (YYYY-MM-DD HH:MM TZ) Validation completed.

## Surprises & Discoveries

- Observation: The repository already has most of the required pieces: `scripts/preflight.ps1`, AGENTS guidance, README checks, and plan rules.
  Evidence: `AGENTS.md`, `README.md`, `agent-docs/07-unlock-agentic-loops.md`, and `scripts/preflight.ps1` all define overlapping parts of the workflow.

## Decision Log

- Decision: Use preflight hardening as the example ExecPlan instead of a UI-only task.
  Rationale: It crosses script behavior, documentation, and workflow, so it clearly demonstrates when a prompt is too small and a living plan is justified.
  Date/Author: 2026-03-14 / Codex

## Outcomes & Retrospective

This example plan defines how to approach a multi-step repository workflow change. It is intentionally not implemented in this session. What remains is the actual execution: align the script, docs, and validation flow, then record outcomes and surprises as the work proceeds.

## Context and Orientation

This repository uses Django under `mysite/` and keeps repository-level automation scripts under `scripts/`. A "preflight" is the repeatable verification loop that runs checks before commit or PR. The current primary script is `scripts/preflight.ps1`, which runs `manage.py check`, optional tests, lint, and optional deploy checks. Guidance about when and how to run these checks is split across `AGENTS.md`, `README.md`, and `agent-docs/07-unlock-agentic-loops.md`.

Key files:

- `scripts/preflight.ps1`: PowerShell entry point for local verification.
- `README.md`: contributor-facing setup and quality workflow.
- `AGENTS.md`: repository rules for agents and validation expectations.
- `agent-docs/07-unlock-agentic-loops.md`: rationale for codifying repetitive verification loops.
- `agent-docs/03-pr-ci-process.md`: place to align PR expectations if workflow text changes.

## Plan of Work

First, inspect `scripts/preflight.ps1` and identify exactly which checks it runs, which flags it supports, and which assumptions it makes about the virtualenv and working directory. Then compare that behavior against `README.md`, `AGENTS.md`, and `agent-docs/07-unlock-agentic-loops.md` to locate mismatches or undocumented behavior.

Next, decide whether the change is documentation-only, script-only, or both. If the script behavior is correct but the docs drifted, update the docs to match the script. If the script is missing a repository-standard check that contributors run manually, add the missing check in the script and document the reason. Keep the behavior minimal and avoid adding checks that are redundant with existing CI unless they reduce a real local failure mode.

After the behavior is aligned, update the contributor-facing guidance so that a novice can run a single command from the repository root and understand what happened if it fails. If the PR process depends on reporting which validations were executed, make sure the docs state that expectation explicitly.

## Concrete Steps

Work from repository root unless stated otherwise.

1. Read the current script and docs:
   - `Get-Content -Raw scripts/preflight.ps1`
   - `Get-Content -Raw README.md`
   - `Get-Content -Raw AGENTS.md`
   - `Get-Content -Raw agent-docs/07-unlock-agentic-loops.md`
   Expected result: clear list of current checks, flags, and documented commands.

2. Identify mismatches:
   - compare script behavior with repository defaults in docs
   - record any missing checks, duplicated guidance, or misleading instructions
   Expected result: a short mismatch list that can drive minimal edits.

3. Apply minimal edits:
   - update `scripts/preflight.ps1` if behavior must change
   - update `README.md`, `AGENTS.md`, and related onboarding docs if wording must change
   Expected result: one consistent preflight story across script and docs.

4. Validate behavior:
   - from root: `.\scripts\preflight.ps1`
   - optionally: `.\scripts\preflight.ps1 -SkipTests`
   - optionally: `.\scripts\preflight.ps1 -DeployChecks`
   Expected result: successful runs or actionable failures with correct messages.

5. Prepare handoff notes:
   - summarize what changed
   - list commands executed and result
   - note any prerequisites such as `.venv` creation
   Expected result: another session can continue without re-discovering context.

## Validation and Acceptance

Acceptance criteria:

- `scripts/preflight.ps1` completes successfully in a correctly prepared local environment.
- The checks described in `README.md` and `AGENTS.md` match the real script behavior.
- A contributor can understand from the docs whether to run root-level preflight or per-project commands under `mysite/`.
- If deploy checks are documented, `-DeployChecks` behavior is described accurately.

Behavior-oriented validation:

- command output clearly shows which check is running;
- failures stop the script with a non-zero exit code;
- success ends with the expected completion message;
- documentation references the same commands and flags that actually exist.

## Idempotence and Recovery

Documentation reads are fully repeatable. Running `.\scripts\preflight.ps1` is safe to repeat as long as the environment is unchanged. If validation fails because `.venv` is missing, recover by creating the virtual environment through the documented setup flow before retrying. If a script edit causes a new failure, revert only the relevant script/doc changes and rerun the previous known-good command set.

## Artifacts and Notes

Useful evidence to capture during real execution:

- `git diff` for `scripts/preflight.ps1`, `README.md`, and `AGENTS.md`
- terminal output for `.\scripts\preflight.ps1`
- short note of any mismatch found between docs and script

## Interfaces and Dependencies

Required interfaces and dependencies at completion:

- PowerShell execution of `scripts/preflight.ps1`
- local Django project under `mysite/`
- project virtualenv at `mysite/.venv`
- `python manage.py check`
- `python manage.py test`
- `ruff check .`
- optional `python manage.py check --deploy`

## Revision Note

- 2026-03-14 19:56 Europe/Rome - Initial example ExecPlan added to demonstrate when a prompt should escalate into a living plan.
