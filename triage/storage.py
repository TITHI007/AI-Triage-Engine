import os
import json
import sqlite3
import time

DB_PATH = os.path.join("data", "triage.db")
AUDIT_PATH = os.path.join("data", "audit_log.jsonl")

def init_db():
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS cases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at INTEGER,
            customer_message TEXT,
            ai_json TEXT,
            final_route TEXT,
            final_reply TEXT,
            human_decision TEXT,
            human_reason TEXT
        )
        """)
        con.commit()

def save_case(customer_message, ai_json, final_route, final_reply, human_decision, human_reason):
    created_at = int(time.time())

    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("""
        INSERT INTO cases(created_at, customer_message, ai_json, final_route, final_reply, human_decision, human_reason)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            created_at,
            customer_message,
            json.dumps(ai_json),
            final_route,
            final_reply,
            human_decision,
            human_reason
        ))
        con.commit()
        case_id = cur.lastrowid

    audit = {
        "case_id": case_id,
        "created_at": created_at,
        "customer_message": customer_message,
        "ai_json": ai_json,
        "final_route": final_route,
        "final_reply": final_reply,
        "human_decision": human_decision,
        "human_reason": human_reason
    }

    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(audit) + "\n")

    return case_id

