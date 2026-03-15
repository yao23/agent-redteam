from dataclasses import dataclass, field
from typing import List


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
class Report:
    target: str
    results: List[AttackResult]
    score: int
    overall_risk: str
