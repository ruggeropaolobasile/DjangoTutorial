#!/usr/bin/env python3
"""Generate a cycle health report for the Polls project."""

from __future__ import annotations

import json
import pathlib
import shlex
import subprocess
import sys
import textwrap
from datetime import datetime, timezone

PROJECT_OWNER = "ruggeropaolobasile"
PROJECT_NUMBER = "1"
PROJECT_ID = "PVT_kwHOAdTEjs4BRxAX"
REPORT_TARGET = pathlib.Path("reports/cycle-report.md")


def run(command: list[str]) -> str:
    """Run a command and return its stdout as a string."""
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def gather_project_items() -> list[dict]:
    """Fetch project board items via the GitHub CLI."""
    command = [
        "gh",
        "project",
        "item-list",
        PROJECT_NUMBER,
        "--owner",
        PROJECT_OWNER,
        "--format",
        "json",
        "--limit",
        "100",
    ]
    raw = run(command)
    payload = json.loads(raw)
    return payload.get("items", [])


def normalize_status(item: dict) -> str:
    """Return the status label for an item."""
    status = item.get("status")
    if isinstance(status, dict):
        return status.get("name", "Todo")
    if isinstance(status, str):
        return status
    return "Todo"


def normalize_priority(item: dict) -> str | None:
    """Return the priority label for an item, if set."""
    priority = item.get("priority")
    if isinstance(priority, dict):
        return priority.get("name")
    if isinstance(priority, str):
        return priority
    return None


def summarize(items: list[dict]) -> str:
    """Format the summary table and insights for the report."""
    counts = {"Todo": 0, "In progress": 0, "Done": 0}
    priority = {}

    for item in items:
        status = normalize_status(item)
        counts[status] = counts.get(status, 0) + 1
        priority_name = normalize_priority(item)
        if priority_name:
            priority.setdefault(priority_name, 0)
            priority[priority_name] += 1

    lines = [
        "| Status | Count |",
        "| ------ | ----- |",
    ]
    for status, total in counts.items():
        lines.append(f"| {status} | {total} |")

    priority_lines = ["| Priority | Items |", "| -------- | ----- |"]
    for label, total in sorted(priority.items()):
        priority_lines.append(f"| {label} | {total} |")

    return "\n".join(lines + ["", "**Priority spread**", ""] + priority_lines)


def build_report(items: list[dict]) -> str:
    """Construct the markdown report text."""
    now = datetime.now(timezone.utc).astimezone()
    summary = summarize(items)
    open_tasks = [item for item in items if normalize_status(item) != "Done"]

    report_lines = [
        f"# Cycle Report ({now.strftime('%Y-%m-%d %H:%M %Z')})",
        "",
        "- Branch: `feature/polls-insights-followups` (tracking)",
        "- PR: #9 (feature/polls-insights-followups)",
        "",
        "## Project Overview",
        summary,
        "",
        "## Open items (non-Done)",
    ]

    for item in sorted(open_tasks, key=lambda doc: normalize_priority(doc) or ""):
        name = item.get("title")
        status = normalize_status(item)
        report_lines.append(f"- {name} — status `{status}`")

    report_lines.append("")
    report_lines.append("## Recommendations")
    report_lines.append(
        textwrap.dedent(
            """\
            1. Keep the GitHub Project in sync whenever a PR touches more than one task.
            2. Run this report before each sprint review to catch bottlenecks early.
            3. Automate the branch cleanup script once `gh` credentials are stable.
            """
        ).strip()
    )
    report_lines.append("")
    report_lines.append(f"Generated from project {PROJECT_ID} via `gh project item-list`.")
    return "\n".join(report_lines)


def main() -> None:
    """Main entrypoint for report generation."""
    items = gather_project_items()
    report_text = build_report(items)
    REPORT_TARGET.parent.mkdir(exist_ok=True)
    REPORT_TARGET.write_text(report_text, encoding="utf-8")
    print(f"Wrote report to {REPORT_TARGET}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(exc.stderr or exc.stdout, file=sys.stderr)
        raise
