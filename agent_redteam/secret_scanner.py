import re
from pathlib import Path
from typing import List

from agent_redteam.models import RepoFinding


SECRET_PATTERNS = [
    (r"sk-[A-Za-z0-9_-]{10,}", "Possible OpenAI-style secret"),
    (r"anthropic[_-]?api[_-]?key", "Possible Anthropic API key reference"),
    (r"api[_-]?key\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded API key assignment"),
    (r"token\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded token assignment"),
    (r"secret\s*[:=]\s*['\"][^'\"]+['\"]", "Hardcoded secret assignment"),
    (r"aws_access_key_id\s*[:=]\s*['\"][^'\"]+['\"]", "Possible AWS Access Key"),
    (r"ghp_[a-zA-Z0-9]{36}", "Possible GitHub Personal Access Token"),
    (r"AIza[0-9A-Za-z-_]{35}", "Possible Google API Key"),
    (r"xoxb-[0-9]{11}-[0-9]{11}-[0-9a-zA-Z]{24}", "Possible Slack Bot Token"),
    (r"-----BEGIN RSA PRIVATE KEY-----", "RSA Private Key found"),
]

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".json", ".yaml", ".yml",
    ".env", ".txt", ".md", ".ini", ".cfg"
}


def scan_secret_file(file_path: Path) -> List[RepoFinding]:
    findings: List[RepoFinding] = []

    if file_path.suffix.lower() not in TEXT_EXTENSIONS and file_path.name != ".env":
        return findings

    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return findings

    for pattern, message in SECRET_PATTERNS:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            snippet = match.group(0)[:200]
            findings.append(
                RepoFinding(
                    category="secret_leak",
                    file_path=str(file_path),
                    severity="HIGH",
                    message=message,
                    snippet=snippet,
                )
            )

    return findings
