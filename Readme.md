# AI Triage Engine

AI Triage Engine is an AI-native workflow system that triages financial support messages, drafts compliant responses, enforces deterministic safety rules, and explicitly defines where AI must stop and humans must take control.

This project demonstrates production-oriented AI systems thinking — not just prompt engineering.

It is a workflow system.

It deliberately assigns responsibility between:

- Machine intelligence  
- Deterministic safeguards  
- Human judgment  

That boundary is the core design decision.
---

## 🎯 Objective

Redesign a legacy support workflow as an AI-first system that:

- Expands human capability
- Handles structured decision-making
- Enforces safety deterministically
- Preserves human authority for high-impact actions
- Operates with full auditability

The goal is not to replace judgment — but to responsibly augment it.

---

## 🧠 What the Human Can Now Do That They Couldn't Before

Before AI Triage Engine:

- Agents manually read and triaged every message
- Risk detection was inconsistent
- Draft quality varied by experience
- Escalation decisions depended heavily on cognitive load
- No consistent audit trail of structured reasoning

With AI Triage Engine:

- Messages are automatically classified at scale
- Urgency and risk are surfaced immediately
- Draft replies are structured and policy-aware
- High-risk signals trigger automatic escalation
- All decisions are logged and auditable

The human now focuses on judgment rather than repetitive triage.

---

## ⚙️ System Architecture

Customer Message  
↓  
LLM Triage (Structured JSON Output)  
↓  
Deterministic Hard Rule Engine  
↓  
LLM Safety Critic (Second Pass Validation)  
↓  
Human Decision Layer  
↓  
SQLite + JSONL Audit Log  

---

## 🏗 Core Components

### 1️⃣ LLM Triage

The first OpenAI call:

- Classifies intent
- Assesses urgency
- Detects risk signals
- Recommends routing
- Drafts a compliant response

The model is forced to return structured JSON only.

---

### 2️⃣ Deterministic Hard Rules

A rule engine enforces:

- Fraud keyword detection
- Legal escalation triggers
- Forced human review for high-risk signals

These overrides always win over the model.

AI suggestions never bypass deterministic safeguards.

---

### 3️⃣ LLM Safety Critic

A second LLM pass validates the draft response.

It blocks replies that:

- Promise refunds or reversals
- Request sensitive data (OTP, SIN/SSN, passwords)
- Claim actions were taken without verification

If unsafe:
- The draft is rewritten
- Human review is forced

This creates layered AI responsibility.

---

### 4️⃣ Human Boundary

AI suggests. Humans decide.

AI does NOT:

- Execute financial transactions
- Reverse trades
- Guarantee outcomes
- Override fraud systems
- Make irreversible decisions

High-risk cases require human approval.

Low-risk cases allow fast processing.

Final authority always remains human.

---

### 5️⃣ Audit & Traceability

All decisions are saved in:

- SQLite database (`data/triage.db`)
- Append-only JSON log (`data/audit_log.jsonl`)

Each case stores:

- Original message
- AI structured output
- Final route
- Final reply
- Human decision
- Human reason (if escalated/rejected)
- Timestamp

This ensures transparency and operational accountability.

---

## 📁 Project Structure

AI TRIAGE ENGINE/

├── app.py                # Streamlit UI  
├── requirements.txt  
├── .env  

├── triage/  
│   ├── config.py         # Prompts and constants  
│   ├── llm.py            # OpenAI wrapper  
│   ├── schema.py         # JSON normalization  
│   ├── rules.py          # Deterministic overrides  
│   ├── pipeline.py       # AI orchestration logic  
│   ├── storage.py        # SQLite + audit logging  
│   └── __init__.py  

└── data/  
    └── triage.db  

---

## 🤖 Where AI Is Responsible

AI handles:

- Intent classification
- Urgency assessment
- Risk flag detection
- Draft generation
- Confidence scoring
- Safety re-checking

AI meaningfully expands operational throughput.

---

## 🛑 Where AI Must Stop

AI must stop when:

- Fraud indicators are present
- Legal threats are detected
- Sensitive data could be requested
- Financial actions are implied
- Confidence is low

In these cases:

- Escalation is forced
- Human review is required
- AI cannot auto-approve

This boundary is explicit and enforced by code.

---

## 🚀 How to Run

1️⃣ Install dependencies:
```powershell
py -m pip install -r requirements.txt


2️⃣ Create `.env` file:

OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini


3️⃣ Start application:
```python
py -m streamlit run app.py

