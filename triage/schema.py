DEFAULT_RESULT = {
    "intent": "",
    "urgency": "low",
    "risk_flags": [],
    "recommended_route": "agent_reply",
    "needs_human_review": False,
    "confidence": 0.0,
    "draft_reply": "",
}

def normalize_result(obj: dict) -> dict:
    out = dict(DEFAULT_RESULT)

    out["intent"] = str(obj.get("intent", out["intent"]))

    urgency = obj.get("urgency", out["urgency"])
    out["urgency"] = urgency if urgency in ("low", "medium", "high") else "low"

    rf = obj.get("risk_flags", out["risk_flags"])
    out["risk_flags"] = rf if isinstance(rf, list) else []

    rr = obj.get("recommended_route", out["recommended_route"])
    out["recommended_route"] = rr if rr in ("self_serve", "agent_reply", "escalate_risk") else "agent_reply"

    out["needs_human_review"] = bool(obj.get("needs_human_review", out["needs_human_review"]))

    conf = obj.get("confidence", out["confidence"])
    try:
        conf = float(conf)
    except Exception:
        conf = out["confidence"]
    out["confidence"] = min(max(conf, 0.0), 1.0)

    out["draft_reply"] = str(obj.get("draft_reply", out["draft_reply"]))

    for k in ("rule_override", "critic_issues"):
        if k in obj:
            out[k] = obj[k]

    return out