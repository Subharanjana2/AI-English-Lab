import os
from dotenv import load_dotenv
from livekit.agents import VoiceAssistant
from groq import Groq
from gtts import gTTS
import tempfile

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def text_to_speech(text):
    tts = gTTS(text=text, lang="en")
    f = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(f.name)
    return f.name

async def ai_response(transcript: str) -> str:
    prompt = f"""
    You are an interview coach.
    Analyze this answer and respond briefly:

    "{transcript}"
    """
    res = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return res.choices[0].message.content.strip()

assistant = VoiceAssistant(
    on_user_speech=ai_response,
    text_to_speech=text_to_speech
)

assistant.run()
