from typing import Dict
import requests


def run_attack(target_url: str, prompt: str, timeout: int = 20) -> str:
    """
    Expects a simple JSON API:
    POST { "prompt": "..." }
    Response JSON:
    { "response": "..." }
    """
    payload: Dict[str, str] = {"prompt": prompt}
    response = requests.post(target_url, json=payload, timeout=timeout)
    response.raise_for_status()

    data = response.json()
    if "response" not in data:
        raise ValueError("Target API response must contain a 'response' field.")
    return str(data["response"])
