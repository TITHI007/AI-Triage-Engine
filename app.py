import streamlit as st
from triage.storage import init_db, save_case
from triage.llm import get_client_and_model
from triage.pipeline import run_triage

init_db()

st.title("AI Triage Engine")
st.caption("AI suggests triage + draft. Rules enforce safety. Humans own high-impact decisions.")

customer_message = st.text_area("Paste a customer message", height=180)

if "triage_result" not in st.session_state:
    st.session_state.triage_result = None

if st.button("Analyze") and customer_message.strip():
    client, model = get_client_and_model()
    st.session_state.triage_result = run_triage(client, model, customer_message.strip())

result = st.session_state.triage_result

if result:
    st.subheader("AI Output (Structured JSON)")
    st.json(result)

    needs_review = bool(result.get("needs_human_review"))

    if needs_review:
        st.error("HARD STOP: Human review required before sending any final response or taking high-impact action.")
        st.subheader("Draft Reply (Human must review & can edit)")
        edited_reply = st.text_area("Final reply", value=result.get("draft_reply", ""), height=140)
    else:
        st.subheader("AI Draft Reply (Low-risk)")
        st.write(result.get("draft_reply", ""))
        edited_reply = result.get("draft_reply", "")

    if result.get("critic_issues"):
        st.warning(f"Critic flagged issues: {result['critic_issues']}")

    st.subheader("Human decision")
    routes = ["self_serve", "agent_reply", "escalate_risk"]
    idx = routes.index(result.get("recommended_route", "agent_reply"))
    final_route = st.selectbox("Final route", routes, index=idx)

    human_decision = st.selectbox("Decision", ["approve", "edit_and_approve", "escalate", "reject"])
    human_reason = st.text_input("Reason (required for escalate/reject)", "")

    save_disabled = (human_decision in ["escalate", "reject"]) and (not human_reason.strip())
    if save_disabled:
        st.warning("Reason required for escalate/reject.")

    if st.button("Save case", disabled=save_disabled):
        case_id = save_case(
            customer_message=customer_message,
            ai_json=result,
            final_route=final_route,
            final_reply=edited_reply,
            human_decision=human_decision,
            human_reason=human_reason.strip(),
        )
        st.success(f"Saved case #{case_id}")