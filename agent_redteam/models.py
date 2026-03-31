from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AttackCase:
    category: str
    prompt: str


@dataclass
class AttackResult:
    category: str
    prompt: str
    response_text: str
    indicators: List[str] = field(default_factory=list)
    vulnerable: bool = False
    possible: bool = False


@dataclass
class RepoFinding:
    category: str
    file_path: str
    severity: str
    message: str
    snippet: Optional[str] = None


@dataclass
class Report:
    target: str
    results: List[AttackResult]
    score: int
    overall_risk: str


@dataclass
class RepoReport:
    target: str
    findings: List[RepoFinding]
    score: int
    overall_risk: str