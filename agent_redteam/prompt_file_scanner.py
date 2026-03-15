from pathlib import Path
from typing import List

from agent_redteam.models import RepoFinding


PROMPT_PATTERNS = [
    ("ignore previous instructions", "Prompt injection phrase found"),
    ("reveal system prompt", "System prompt exfiltration phrase found"),
    ("override system prompt", "System prompt override phrase found"),
    ("developer mode", "Developer mode bypass phrase found"),
    ("print hidden instructions", "Hidden instruction exfiltration phrase found"),
]

PROMPT_EXTENSIONS = {".txt", ".md", ".prompt", ".yaml", ".yml", ".json", ".py"}


def scan_prompt_file(file_path: Path) -> List[RepoFinding]:
    findings: List[RepoFinding] = []

    if file_path.suffix.lower() not in PROMPT_EXTENSIONS:
        return findings

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return findings

    for pattern, message in PROMPT_PATTERNS:
        if pattern in content:
            findings.append(
                RepoFinding(
                    category="prompt_injection_surface",
                    file_path=str(file_path),
                    severity="MEDIUM",
                    message=message,
                    snippet=pattern,
                )
            )

    return findings
