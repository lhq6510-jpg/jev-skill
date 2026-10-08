"""Local conservative preprocessing and accounting. No model/API calls or file writes."""
import argparse
import json
import math
import re
import sys
from pathlib import Path


def tokens(text):
    cjk = len(re.findall(r"[\u3400-\u9fff\uf900-\ufaff]", text))
    return math.ceil(cjk + (len(text) - cjk) / 4)


def paragraphs(text):
    return [p for p in re.split(r"\n\s*\n", text.replace("\r\n", "\n")) if p.strip()]


def unsafe_code(text):
    return bool(re.search(r"```|~~~|(?m:^\t|^ {4}\S)|\b(?:def|function|class)\s+\w+|[{}]|\breturn\s+", text))


def anchors(text):
    technical = re.findall(r'https?://[^\s<>"）]+|(?:[A-Za-z]:\\|/)[^\s"<>]+|\b[\w.-]+\.(?:py|js|json|md|txt|csv|ts|yaml|yml)\b|\b[A-Za-z_][\w]*(?:_[\w]+)+\b|\b[A-Za-z]+(?:[A-Z][a-z]+)+\b|\b[A-Z][A-Z0-9_-]+\b|\d+(?:\.\d+)*(?:\s*(?:ms|秒|分钟|MB|GB|%|个|条|元))?', text)
    strong = [p for p in paragraphs(text) if re.search(r"必须|不允许|禁止|不得|不能|不要|仅|只|先|再|然后|最后|之前|之后|依赖|顺序|输出|格式|must|never|not\b|before|after|only|output|depends", p, re.I)]
    return set(technical), set(strong)


def cleanup(text):
    # Adjacent identical entire paragraphs only. No rearrangement, paraphrasing, or global dedup.
    parts = re.split(r"(\n[ \t]*\n(?:[ \t]*\n)*)", text)
    output = []
    previous = None
    for i in range(0, len(parts), 2):
        p = parts[i]
        if previous is not None and p == previous:
            continue
        if output:
            output.append("\n\n")
        output.append(p)
        previous = p
    return "".join(output)


def verify(original, candidate, inventory=None, semantic_reviewed=False):
    if not isinstance(candidate, str) or not candidate.strip():
        return False, "Empty or malformed candidate"
    tech, strong = anchors(original)
    candidate_tech, _ = anchors(candidate)
    if not tech.issubset(candidate_tech) or any(a not in candidate for a in strong):
        return False, "Protected identifier/constraint/order missing"
    cursor = 0
    for p in list(dict.fromkeys(paragraphs(original))):
        if p in strong:
            pos = candidate.find(p,cursor)
            if pos < 0:
                return False, "Protected constraint/order moved"
            cursor = pos + len(p)
    # Default cleanup must preserve every unique source paragraph exactly and in order.
    source = list(dict.fromkeys(paragraphs(original)))
    if inventory is None:
        cursor = 0
        for p in source:
            pos = candidate.find(p, cursor)
            if pos < 0:
                return False, "Original paragraph lost or reordered"
            cursor = pos + len(p)
    else:
        if not semantic_reviewed:
            return False, "Semantic equivalence not reviewed"
        entries = inventory.get("requirements", [])
        if not isinstance(entries, list):
            return False, "Invalid inventory"
        if any(not isinstance(e, dict) or not isinstance(e.get("original"), str) or not isinstance(e.get("candidate"), str) for e in entries):
            return False, "Invalid inventory entries"
        if any(not e["candidate"] or e["original"] not in original or e["candidate"] not in candidate or e.get("equivalent") is not True for e in entries):
            return False, "Unverified requirement"
        if any(not any(p in e["original"] for e in entries) for p in source):
            return False, "Incomplete requirement inventory"
    return True, "Literal protection passed; semantic equivalence is Agent-reviewed when applicable"


def optimize(text, candidate=None, inventory=None, semantic_reviewed=False, unseen=False, extra_tokens=0, overhead=None, reuse_count=0):
    root = Path(__file__).resolve().parents[1]
    if overhead is None:
        overhead = tokens((root / "SKILL.md").read_text(encoding="utf-8")) + 200
    semantic_cost = 0 if candidate is None else tokens(text) + tokens(candidate if isinstance(candidate,str) else '') + tokens((root / "references" / "semantic.md").read_text(encoding="utf-8")) + 250
    cost = overhead + max(0, extra_tokens, semantic_cost)
    before = tokens(text)
    reason = None
    proposed = text
    if before < 256:
        reason = "Prompt already concise"
    elif unsafe_code(text):
        reason = "Code/structured input: preserve original"
    else:
        try:
            proposed = cleanup(text) if candidate is None else candidate
            valid, detail = verify(text, proposed, inventory, semantic_reviewed)
            if not valid:
                proposed, reason = text, detail
        except Exception:
            proposed, reason = text, "Optimization failed; use original"
    after = tokens(proposed)
    recoverable = max(0, before - after) if unseen else 0
    net = recoverable - cost
    if reason is None and net <= max(64, before * .05):
        reason = "Optimization cost exceeds benefit or benefit is marginal"
    applied = reason is None
    selected = proposed if applied else text
    return {"measurement": "estimate", "original_input_tokens": before,
            "candidate_input_tokens": after, "optimized_input_tokens": tokens(selected),
            "optimization_extra_tokens": cost, "estimated_net_saved_tokens": net if applied else -cost,
            "estimated_net_saved_percent": round((net if applied else -cost) / max(1, before) * 100, 2),
            "recoverable_input_tokens": recoverable if applied else 0,
            "hypothetical_reuse_saved_tokens": max(0, before-after) * reuse_count,
            "reuse_is_realized": False, "input_already_read": not unseen,
            "applied": applied, "skip": not applied, "reason": reason or "Positive estimated net benefit",
            "selected_text": selected, "original_preserved": True,
            "count_sensitivity": "Text count heuristic ±30%; not calibrated uncertainty", "actual_total_usage": None}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--file")
    p.add_argument("--candidate")
    p.add_argument("--inventory")
    p.add_argument("--semantic-reviewed", action="store_true")
    p.add_argument("--unseen", action="store_true")
    p.add_argument("--extra-tokens", type=int, default=0)
    p.add_argument("--reuse-count", type=int, default=0)
    a = p.parse_args()
    text = Path(a.file).read_text(encoding="utf-8-sig") if a.file else sys.stdin.read()
    try:
        result = optimize(text, Path(a.candidate).read_text(encoding="utf-8-sig") if a.candidate else None,
                          json.loads(Path(a.inventory).read_text(encoding="utf-8-sig")) if a.inventory else None,
                          a.semantic_reviewed, a.unseen, a.extra_tokens, reuse_count=max(0,a.reuse_count))
    except Exception:
        result = {"selected_text": text, "applied": False, "skip": True, "reason": "Skill failure; use original", "actual_total_usage": None, "measurement": "estimate"}
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stdin, "reconfigure"):
        sys.stdin.reconfigure(encoding="utf-8")
    main()
