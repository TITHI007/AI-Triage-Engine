import re
from triage.config import SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT, RISKY_REPLY_PATTERNS, HIGH_RISK_KEYWORDS
from triage.llm import call_json_chat
from triage.schema import normalize_result
from triage.rules import apply_hard_rules

def should_run_critic(customer_message: str, result: dict) -> bool:
    if result.get("needs_human_review"):
        return True
    if result.get("confidence", 0) < 0.55:
        return True

    msg_lower = customer_message.lower()
    if any(k in msg_lower for k in HIGH_RISK_KEYWORDS):
        return True

    draft = result.get("draft_reply", "") or ""
    for pat in RISKY_REPLY_PATTERNS:
        if re.search(pat, draft, flags=re.IGNORECASE):
            return True
    return False

def run_triage(client, model: str, customer_message: str) -> dict:
    triage_messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Customer message: {customer_message}"},
    ]

    raw = call_json_chat(client, model, triage_messages)
    result = normalize_result(raw)
    result = apply_hard_rules(customer_message, result)

    if should_run_critic(customer_message, result):
        critic_messages = [
            {"role": "system", "content": CRITIC_SYSTEM_PROMPT},
            {"role": "user", "content": f"Customer message:\n{customer_message}\n\nDraft reply:\n{result.get('draft_reply','')}"},
        ]
        critic_raw = call_json_chat(client, model, critic_messages)
        ok = bool(critic_raw.get("ok", True))
        if not ok:
            result["needs_human_review"] = True
            result["critic_issues"] = critic_raw.get("issues", [])
            fixed = critic_raw.get("fixed_reply", "")
            if fixed:
                result["draft_reply"] = fixed

    return result