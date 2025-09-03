import os
import json
from typing import Dict, List, Optional

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

SYSTEM_INSTRUCTIONS = """You are an expert technical interviewer. 
Generate concise, senior-practical questions (no trivia) that test fundamentals and applied skills. 
Return only a JSON list of strings without any commentary."""

def _client():
    if OpenAI is None:
        return None
    try:
        return OpenAI()
    except Exception:
        return None

def generate_questions_llm(candidate: Dict) -> List[str]:
    """
    Tries to call an LLM to generate tailored questions.
    Returns [] if API isn't available or an error occurs.
    """
    techs = candidate.get("tech_stack", [])
    if not techs:
        return []

    client = _client()
    if client is None:
        return []

    prompt = f"""Candidate tech stack: {', '.join(techs)}
Years of experience: {candidate.get('years_experience', 'N/A')}
Desired role: {candidate.get('desired_position', 'N/A')}

Generate 3-5 technical interview questions tailored to the stack. 
Avoid duplicates, keep each question in one sentence.
Output a pure JSON list of strings."""

    try:
        resp = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
        )
        content = resp.choices[0].message.content.strip()
        # Try to parse JSON; if it isn't, return [] to fall back
        if content.startswith("["):
            return json.loads(content)
        return []
    except Exception:
        return []
