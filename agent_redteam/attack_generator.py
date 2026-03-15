import json
from pathlib import Path
from typing import List

from agent_redteam.models import AttackCase


def load_attacks() -> List[AttackCase]:
    dataset_path = Path(__file__).resolve().parent.parent / "datasets" / "attack_prompts.json"
    raw = json.loads(dataset_path.read_text(encoding="utf-8"))

    attacks: List[AttackCase] = []
    for category, prompts in raw.items():
        for prompt in prompts:
            attacks.append(AttackCase(category=category, prompt=prompt))
    return attacks
