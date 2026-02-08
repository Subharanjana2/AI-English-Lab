import os
from groq import Groq

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_question(role, difficulty):
    prompt = f"""
    Generate one {difficulty} interview question for a {role}.
    """
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return res.choices[0].message.content.strip()


def analyze_answer(answer):
    prompt = f"""
    Analyze this interview answer:
    "{answer}"

    Give:
    - Corrected grammar
    - 2 suggestions
    - Score /10
    """
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    return res.choices[0].message.content.strip()
