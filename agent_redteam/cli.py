from typing import Optional

import click
from rich.console import Console

from agent_redteam.attack_generator import load_attacks
from agent_redteam.attack_runner import run_attack
from agent_redteam.models import Report
from agent_redteam.report_generator import (
    format_report,
    format_repo_report,
    write_repo_markdown,
)
from agent_redteam.repo_scanner import scan_repo
from agent_redteam.response_analyzer import analyze_response
from agent_redteam.risk_scoring import calculate_score, overall_risk


console = Console()


@click.group()
def main() -> None:
    """AI that tries to hack your AI agent."""
    pass


@main.command()
@click.argument("target_url")
def scan(target_url: str) -> None:
    """Run red-team attacks against a target agent HTTP endpoint."""
    console.print(f"[bold cyan]Scanning target:[/bold cyan] {target_url}")

    attacks = load_attacks()
    results = []

    for attack in attacks:
        console.print(f"→ Running [yellow]{attack.category}[/yellow]: {attack.prompt}")
        try:
            response_text = run_attack(target_url, attack.prompt)
            result = analyze_response(attack, response_text)
            results.append(result)
        except Exception as exc:
            console.print(f"[red]Error[/red] {attack.category}: {exc}")

    score = calculate_score(results)
    report = Report(
        target=target_url,
        results=results,
        score=score,
        overall_risk=overall_risk(score),
    )

    console.print()
    console.print(format_report(report))


@main.command()
@click.argument("repo_url")
@click.option("--markdown", "markdown_path", default=None, help="Write markdown report to file")
def scan_repo_cmd(repo_url: str, markdown_path: Optional[str]) -> None:
    """Clone and statically scan a repository for agent security risks."""
    console.print(f"[bold cyan]Cloning + scanning repo:[/bold cyan] {repo_url}")

    report = scan_repo(repo_url)

    console.print()
    console.print(format_repo_report(report))

    if markdown_path:
        write_repo_markdown(report, markdown_path)
        console.print(f"\n[green]Markdown report written to:[/green] {markdown_path}")
