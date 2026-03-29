from collections import defaultdict
from pathlib import Path

from agent_redteam.models import Report, RepoReport


def format_report(report: Report) -> str:
    grouped = defaultdict(list)
    for result in report.results:
        grouped[result.category].append(result)

    lines = [
        f"Target: {report.target}",
        "",
        f"Overall Risk: {report.overall_risk}",
        f"Score: {report.score}/100",
        "",
        "Findings:",
    ]

    for category, results in grouped.items():
        vulnerable = any(r.vulnerable for r in results)
        possible = any(r.possible for r in results)
        if vulnerable:
            status = "VULNERABLE"
        elif possible:
            status = "POSSIBLE"
        else:
            status = "SAFE"
        lines.append(f"- {category}: {status}")

    lines.append("")
    lines.append("Detailed Results:")
    for result in report.results:
        status = "VULNERABLE" if result.vulnerable else "POSSIBLE" if result.possible else "SAFE"
        lines.append(f"\n[{result.category}] {status}")
        lines.append(f"Prompt: {result.prompt}")
        if result.indicators:
            lines.append(f"Indicators: {', '.join(result.indicators)}")

    return "\n".join(lines)


def format_repo_report(report: RepoReport) -> str:
    lines = [
        f"Target Repo: {report.target}",
        "",
        f"Overall Risk: {report.overall_risk}",
        f"Score: {report.score}/100",
        "",
        "Findings:",
    ]

    if not report.findings:
        lines.append("- No findings")
        return "\n".join(lines)

    for finding in report.findings:
        lines.append(
            f"- [{finding.severity}] {finding.category} | {finding.file_path} | {finding.message}"
        )
    return "\n".join(lines)


def write_repo_markdown(report: RepoReport, output_path: str) -> None:
    lines = [
        "# Agent Redteam Report",
        "",
        f"**Target Repo:** `{report.target}`  ",
        f"**Overall Risk:** {report.overall_risk}  ",
        f"**Score:** {report.score}/100",
        "",
        "## Findings",
    ]

    if not report.findings:
        lines.append("- No findings")
    else:
        for finding in report.findings:
            lines.append(
                f"- **[{finding.severity}]** `{finding.category}` in `{finding.file_path}` — {finding.message}"
            )
            if finding.snippet:
                lines.append("")
                lines.append("```text")
                lines.append(finding.snippet)
                lines.append("```")

    Path(output_path).write_text("\n".join(lines), encoding="utf-8")        if result.indicators:
            lines.append(f"Indicators: {', '.join(result.indicators)}")

    return "\n".join(lines)
