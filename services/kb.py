
import json
from typing import Optional, Dict, Any, List

with open("data/kb.json", encoding="utf-8") as f:
    KB = json.load(f)

def get_section(section_id: str) -> Optional[Dict[str, Any]]:
    for s in KB["sections"]:
        if s["id"] == section_id:
            return s
    return None

def all_sections() -> List[Dict[str, Any]]:
    return KB["sections"]
