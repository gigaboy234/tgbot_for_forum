
import re
from difflib import SequenceMatcher
from typing import List, Dict, Any
from services.kb import all_sections

def _norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"\s+", " ", s)
    return s

def _ratio(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

def search(question: str, limit: int = 5) -> List[Dict[str, Any]]:
    qn = _norm(question)
    res = []
    for sec in all_sections():
        for item in sec.get("faqs", []):
            qq = _norm(item["q"])
            aa = _norm(item["a"])
            score = max(_ratio(qn, qq), _ratio(qn, aa) * 0.6)
            # small boost for token overlap
            q_tokens = set(qn.split())
            qq_tokens = set(qq.split())
            if q_tokens and qq_tokens:
                score += (len(q_tokens & qq_tokens) / max(len(q_tokens), 1)) * 0.25
            res.append({
                "score": score,
                "section_id": sec["id"],
                "section_title": sec["title"],
                "q": item["q"],
                "a": item["a"],
            })
    res.sort(key=lambda x: x["score"], reverse=True)
    return [r for r in res[:limit] if r["score"] >= 0.35]
