import os
import json
import time
import hashlib
from datetime import datetime
from typing import List, Dict

import streamlit as st

# Local modules
from llm import generate_questions_llm
from question_bank import fallback_questions
from storage import save_candidate_record
from prompts import SYSTEM_PROMPT

APP_TITLE = "TalentScout – Hiring Assistant"
END_KEYWORDS = {"end", "quit", "exit", "stop", "bye"}

st.set_page_config(page_title=APP_TITLE, page_icon="🧭", layout="centered")

# --- Header ---
st.title(APP_TITLE)
st.caption("Initial screening chatbot that collects candidate info and asks tech-stack-specific questions.")
st.info("Type 'end', 'quit', 'exit', 'stop', or 'bye' at any time to finish the conversation.", icon="💡")

# --- Consent / Privacy gate ---
with st.expander("Privacy & Consent", expanded=True):
    st.markdown("""
This demo stores minimal data **locally** on your device (a JSONL file under `./data/`). 
We hash sensitive fields (email, phone) using SHA-256 + random salt for privacy. 
No data is sent to third parties unless you provide an OpenAI API key in `.env` or environment variables.
    """)
    consent = st.checkbox("I understand and consent to this local data handling.", value=False)

if not consent:
    st.warning("Please provide consent to proceed.", icon="⚠️")
    st.stop()

# --- Session state ---
if "stage" not in st.session_state:
    st.session_state.stage = "greeting"   # greeting -> form -> questions -> chatting -> end
if "messages" not in st.session_state:
    st.session_state.messages = []
if "candidate" not in st.session_state:
    st.session_state.candidate = {}
if "questions" not in st.session_state:
    st.session_state.questions = []

# --- Greeting ---
if st.session_state.stage == "greeting":
    st.success("Hello! I'm the TalentScout Hiring Assistant. I'll gather a few details and ask tailored technical questions based on your tech stack.")
    st.session_state.stage = "form"

# --- Candidate info form ---
if st.session_state.stage == "form":
    with st.form("candidate_form"):
        full_name = st.text_input("Full Name *")
        email = st.text_input("Email Address *")
        phone = st.text_input("Phone Number *")
        years_exp = st.number_input("Years of Experience *", min_value=0.0, step=0.5)
        desired_position = st.text_input("Desired Position(s) *", placeholder="e.g., Python Developer; Data Scientist")
        location = st.text_input("Current Location *")
        tech_stack = st.text_area(
            "Tech Stack *",
            placeholder="List programming languages, frameworks, databases, tools (comma-separated). e.g., Python, Django, PostgreSQL, Docker"
        )
        submitted = st.form_submit_button("Continue")

    if submitted:
        required = [full_name, email, phone, desired_position, location, tech_stack]
        if any(not x.strip() for x in required):
            st.error("Please fill all required fields marked with *.", icon="❗")
        else:
            st.session_state.candidate = {
                "full_name": full_name.strip(),
                "email": email.strip(),
                "phone": phone.strip(),
                "years_experience": years_exp,
                "desired_position": desired_position.strip(),
                "location": location.strip(),
                "tech_stack": [t.strip() for t in tech_stack.split(",") if t.strip()],
                "timestamp": datetime.utcnow().isoformat() + "Z",
            }
            st.session_state.stage = "questions"

# --- Generate questions ---
def generate_questions(candidate: Dict) -> List[str]:
    # Try LLM first; fall back to rule-based question bank
    questions = generate_questions_llm(candidate)
    if not questions:
        questions = fallback_questions(candidate.get("tech_stack", []), per_tech=2, max_total=5)
    # De-duplicate and trim
    uniq = []
    for q in questions:
        q = q.strip()
        if q and q not in uniq:
            uniq.append(q)
    return uniq[:5]

if st.session_state.stage == "questions":
    with st.spinner("Creating tailored technical questions..."):
        st.session_state.questions = generate_questions(st.session_state.candidate)
        time.sleep(0.2)
    st.success("I’ve prepared a few questions to gauge your proficiency.", icon="✅")
    for i, q in enumerate(st.session_state.questions, 1):
        st.markdown(f"**Q{i}. {q}**")
    st.session_state.stage = "chatting"

# --- Chatting / Answers collection ---
if st.session_state.stage == "chatting":
    st.divider()
    st.subheader("Your Answers")
    st.caption("Answer the questions one by one in the chat below. You can also ask for clarification.")
    chat_container = st.container()

    # Initialize message history with system prompt
    if not st.session_state.messages:
        st.session_state.messages.append({"role": "system", "content": SYSTEM_PROMPT})
        intro = "Let's begin. Please answer Q1. You can type 'end' to finish anytime."
        st.session_state.messages.append({"role": "assistant", "content": intro})

    # Display history (assistant/user only)
    for m in st.session_state.messages:
        if m["role"] in ("assistant", "user"):
            with chat_container:
                st.chat_message(m["role"]).markdown(m["content"])

    user_input = st.chat_input("Type your answer or question...")
    if user_input:
        if user_input.strip().lower() in END_KEYWORDS:
            st.session_state.stage = "end"
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            # Simple heuristic: provide a generic acknowledgement + prompt to continue
            # (We keep the LLM usage focused on question generation per assignment.)
            reply = "Thanks! Noted. When ready, continue with the next question or type **end** to finish."
            st.session_state.messages.append({"role": "assistant", "content": reply})

# --- End conversation ---
if st.session_state.stage == "end":
    st.balloons()
    st.success("Thanks for your time! We'll review your responses and get back to you with next steps.", icon="🎉")

    # Persist locally (privacy-aware)
    try:
        save_candidate_record(st.session_state.candidate, st.session_state.questions, st.session_state.messages)
        st.caption("Your submission has been saved locally (hashed identifiers).")
    except Exception as e:
        st.error(f"Could not save your submission: {e}")

    st.stop()
