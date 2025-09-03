# TalentScout – Hiring Assistant (AI/ML Intern Assignment)

A Streamlit chatbot that performs **initial screening** for a fictional tech agency, **TalentScout**.  
It collects candidate info and generates **tech-stack-tailored** questions via LLM (with a **rule-based fallback**).

## ✨ Features
- Greeting + clear purpose and conversation end keywords (`end/quit/exit/stop/bye`).
- Form to collect: name, email, phone, years of experience, desired role(s), location, tech stack.
- LLM-based **question generation** (OpenAI) with robust **fallback** question bank.
- Context-aware chat area for answers and clarifications.
- Fallback responses when input is unexpected.
- Graceful conversation ending with local, privacy-aware storage.
- Streamlit UI; local deployment ready.
- GDPR-minded: hashes sensitive identifiers (email/phone) locally and stores in `data/candidates.jsonl`.

## 🧰 Tech
- **Python 3.9+**
- **Streamlit**
- **OpenAI** (optional; app works without it using fallback questions)
- **dotenv** (optional)

## 🚀 Quickstart

```bash
git clone <your-repo-url> talentscout
cd talentscout
# create venv if desired
pip install -r requirements.txt
# (optional) set your OpenAI key and model
echo "OPENAI_API_KEY=sk-..." > .env
echo "OPENAI_MODEL=gpt-4o-mini" >> .env
streamlit run app.py
```

> Without an API key, the app still works using a curated question bank.

## 🔐 Privacy & Data Handling
- All data is saved **locally** to `./data/candidates.jsonl`.
- Email and phone are **hashed with SHA-256** plus a random salt.
- Do not upload personal data in public repos.
- This demo is not production-ready compliance; for production, add consent logs, data retention policy, deletion endpoints, encryption at rest, and audit.

## 🧠 Prompt Design
- `prompts.py` holds a concise **system prompt** to keep the assistant focused on hiring, respectful tone, and safety boundaries.
- `llm.py` sends a short, structured user prompt with the candidate's stack and asks for **JSON-only** output (3–5 questions).

## 🧪 Fallback Mechanism
- If LLM calls fail or no key is configured, the app picks relevant questions from `question_bank.py` (keyword match across technologies) to keep the interview flowing.

## 🗂️ Project Structure
```
.
├── app.py                # Streamlit UI & chat flow
├── llm.py                # LLM wrapper (OpenAI) with safe JSON protocol
├── prompts.py            # System prompt for the assistant
├── question_bank.py      # Curated fallback questions
├── storage.py            # Local privacy-aware persistence
├── data/
│   └── candidates.jsonl  # Local, append-only storage (created at runtime)
├── requirements.txt
└── README.md
```

## 📹 Demo
- You can record a short walkthrough using Loom and attach the link in your submission.
- Suggested flow: consent → form → auto-generated questions → chat answers → end + save.

## 🧩 Optional Enhancements
- Sentiment analysis on answers (e.g., use `textblob` or OpenAI for classification).
- Multilingual support (detect language and regenerate questions accordingly).
- Personalized prompts using prior candidate history (if persisted).

## ✅ Submission Checklist
- [ ] Code compiles and runs: `streamlit run app.py`
- [ ] README updated with your repo URL and any changes
- [ ] Public Git repo OR zip file uploaded
- [ ] Demo video link (optional but recommended)
```

