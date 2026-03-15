import click
from rich.console import Console

from agent_redteam.attack_generator import load_attacks
from agent_redteam.attack_runner import run_attack
from agent_redteam.models import Report
from agent_redteam.report_generator import format_report
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
