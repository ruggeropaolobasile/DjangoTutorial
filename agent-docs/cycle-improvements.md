# Cycle Improvements

## Observed blockers

- There are multiple outstanding `Todo` items in the GitHub Project that touch the Polls slice, so branch churn can easily drift ahead of the board.
- Without a dedicated routine, the board is stale the moment a PR covers more than one entry.
- The workspace relies on ad-hoc notes while the canonical cycle expects a clean branch/PR per task.

## Completed actions

- Created `scripts/cycle_report.py` to call `gh project item-list` and emit a Markdown snapshot under `reports/cycle-report.md`.
- Updated the live project board by marking five covered tasks as `Done`, keeping the backlog aligned with `feature/polls-insights-followups`.
- Added a formal “Export Leaderboard” CTA plus regression coverage so the Polls insights page now ships a finishing touch.

## Next steps

1. Run `python scripts/cycle_report.py` before planning meetings so the backlog/PR state is explicit.
2. Pair the report script with a scheduled GitHub Actions job (using the `gh` CLI credentials already in the repo) to auto-flag drifting tasks.
3. Keep the `.git/info/exclude` pattern and VS Code workspace local to this clone so workspace files never leak into the shareable worktree.

## How to rerun the report

```bash
cd C:/repo/DjangoTutorial
gh auth refresh --hostname github.com -s project
python scripts/cycle_report.py
```

The generated markdown lands in `reports/cycle-report.md`, which you can reference for the latest status and action items.
