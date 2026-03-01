from triage.config import HIGH_RISK_KEYWORDS

def apply_hard_rules(customer_message: str, result: dict) -> dict:
    msg_lower = customer_message.lower()
    if any(k in msg_lower for k in HIGH_RISK_KEYWORDS):
        result["needs_human_review"] = True
        result["recommended_route"] = "escalate_risk"
        result["urgency"] = "high"

        result.setdefault("risk_flags", [])
        result["risk_flags"] = list({*result["risk_flags"], "high_risk_keyword"})
        result["rule_override"] = "High-risk keyword detected (hard rule override)."
    return result