"""Simple JSON storage for shift state."""
import json
import os
from typing import Dict


def load_shift_state(path: str) -> Dict:
    if not os.path.exists(path):
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_shift_state(path: str, shift_counter: int, month: int) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump({'shift_counter': int(shift_counter), 'month': int(month)}, f)
