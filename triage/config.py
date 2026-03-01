import re

SYSTEM_PROMPT = """
You are a fintech support triage AI.

Return ONLY valid JSON with these fields:
- intent (string)
- urgency (low, medium, high)
- risk_flags (array of strings)
- recommended_route (self_serve, agent_reply, escalate_risk)
- needs_human_review (true/false)
- confidence (0-1 number)
- draft_reply (string)

Rules:
- If message suggests fraud, hacking, unauthorized activity, legal threat, or regulator complaint:
  set urgency=high, needs_human_review=true, and recommended_route=escalate_risk.
- Never promise refunds or reversals.
- Never request sensitive data like passwords, SIN/SSN, or one-time codes (OTP).
"""

CRITIC_SYSTEM_PROMPT = """
You are a strict safety/compliance checker for fintech support replies.
Return ONLY JSON: {"ok": boolean, "issues": [strings], "fixed_reply": string}.

Mark ok=false if the reply:
- promises outcomes (refund, reversal, guarantees)
- requests sensitive info (passwords, SIN/SSN, OTP, full account/card numbers)
- claims actions were taken (e.g., "we reversed it") without verification
If ok=false, provide a safer fixed_reply.
"""

HIGH_RISK_KEYWORDS = {
    "hacked", "unauthorized", "fraud",
    "regulator", "lawsuit", "legal",
    "reverse transaction", "chargeback", "scam"
}

RISKY_REPLY_PATTERNS = [
    r"\brefund(ed|s)?\b",
    r"\brevers(e|ed|al)\b",
    r"\bguarantee(d|s)?\b",
    r"\bOTP\b|\bone[- ]time code\b",
    r"\bSIN\b|\bSSN\b",
    r"\bpassword\b",
    r"\bfull (card|account) number\b",
]