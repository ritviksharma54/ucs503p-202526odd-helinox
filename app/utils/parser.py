import json
import re
import json5

def parse_model_json(result):
    """
    Robustly parse JSON from LLM output:
      - Accept dicts directly
      - Strip ```json ... ``` or ``` ... ``` fences if present
      - Extract the first full {...} object via brace counting
      - Try json.loads -> json5.loads -> cleaned json.loads
    Raises ValueError with a short raw excerpt if all attempts fail.
    """
    raw = getattr(result, "content", result)

    if isinstance(raw, dict):
        return raw
    if not isinstance(raw, str):
        raise ValueError(f"Model returned non-string content: {type(raw)}")

    text = raw.strip()
    if not text:
        raise ValueError("Model returned empty content.")

    # 1) Remove markdown code fences if present
    fenced = _extract_fenced_block(text)
    if fenced is not None:
        text = fenced.strip()

    # 2) Extract first full JSON object by brace counting
    obj = _extract_first_json_object(text)
    candidates = [c for c in [obj, text] if c]  # try object, then whole text

    # 3) Try strict JSON then JSON5 then quick-fix+strict
    for cand in candidates:
        cand = cand.strip()
        for parser in (_strict_json, _json5_json, _clean_then_strict):
            parsed = parser(cand)
            if parsed is not None:
                return parsed

    raise ValueError(f"Could not parse JSON from model. Raw (truncated):\n{text[:1500]}")

def _extract_fenced_block(s: str) -> str | None:
    """
    If the text contains ```json ... ``` or ``` ... ```, return the inner block.
    Otherwise None.
    """
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", s, flags=re.IGNORECASE)
    return fence.group(1) if fence else None

def _extract_first_json_object(s: str) -> str | None:
    """
    Extract the first complete {...} JSON object using brace counting.
    Handles braces inside strings in a minimal way.
    """
    in_str = False
    esc = False
    start = None
    depth = 0
    for i, ch in enumerate(s):
        if ch == '"' and not esc:
            in_str = not in_str
        esc = (ch == '\\' and not esc) if in_str else False
        if in_str:
            continue
        if ch == '{':
            if depth == 0:
                start = i
            depth += 1
        elif ch == '}':
            if depth > 0:
                depth -= 1
                if depth == 0 and start is not None:
                    return s[start:i+1]
    return None

def _strict_json(s: str):
    try:
        return json.loads(s)
    except Exception:
        return None

def _json5_json(s: str):
    try:
        return json5.loads(s)
    except Exception:
        return None

def _clean_then_strict(s: str):
    # Strip backticks and BOM, remove trailing commas before } or ]
    cleaned = s.strip().strip('`').replace("\ufeff", "")
    cleaned = re.sub(r",(\s*[}\]])", r"\1", cleaned)
    try:
        return json.loads(cleaned)
    except Exception:
        return None
