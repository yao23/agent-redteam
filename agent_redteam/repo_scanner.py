from pathlib import Path
from typing import List
import git

from agent_redteam.models import RepoFinding, RepoReport
from agent_redteam.prompt_file_scanner import scan_prompt_file
from agent_redteam.secret_scanner import scan_secret_file
from agent_redteam.utils import make_temp_dir, cleanup_dir


SKIP_DIRS = {
    ".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"
}


def clone_repo(repo_url: str) -> Path:
    tmp_dir = make_temp_dir()
    git.Repo.clone_from(repo_url, tmp_dir)
    return tmp_dir


def iter_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def scan_repo_path(repo_path: Path) -> List[RepoFinding]:
    findings: List[RepoFinding] = []

    for file_path in iter_files(repo_path):
        findings.extend(scan_secret_file(file_path))
        findings.extend(scan_prompt_file(file_path))

    return findings


def repo_score(findings: List[RepoFinding]) -> int:
    score = 0
    for f in findings:
        if f.severity == "HIGH":
            score += 25
        elif f.severity == "MEDIUM":
            score += 12
        else:
            score += 5
    return min(score, 100)


def repo_risk(score: int) -> str:
    if score >= 70:
        return "HIGH"
    if score >= 35:
        return "MEDIUM"
    return "LOW"


def scan_repo(repo_url: str) -> RepoReport:
    repo_path = clone_repo(repo_url)
    try:
        findings = scan_repo_path(repo_path)
        score = repo_score(findings)
        return RepoReport(
            target=repo_url,
            findings=findings,
            score=score,
            overall_risk=repo_risk(score),
        )
    finally:
        cleanup_dir(repo_path)
