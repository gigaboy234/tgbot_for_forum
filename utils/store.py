
import json
import os
from typing import Dict, Any

DB_PATH = os.path.join("storage", "users.json")

def _load() -> Dict[str, Any]:
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save(data: Dict[str, Any]) -> None:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get(user_id: int) -> Dict[str, Any]:
    return _load().get(str(user_id), {})

def set(user_id: int, patch: Dict[str, Any]) -> None:
    data = _load()
    uid = str(user_id)
    cur = data.get(uid, {})
    cur.update(patch)
    data[uid] = cur
    _save(data)
