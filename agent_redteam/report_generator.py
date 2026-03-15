from collections import defaultdict

from agent_redteam.models import Report


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
