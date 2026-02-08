from fastapi import FastAPI, UploadFile
from livekit import AccessToken, VideoGrant
import os, tempfile
from groq import Groq
from ai_logic import analyze_answer
from tts import text_to_speech

app = FastAPI()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.get("/token")
def get_token():
    token = (
        AccessToken(
            os.getenv("LIVEKIT_API_KEY"),
            os.getenv("LIVEKIT_API_SECRET")
        )
        .with_identity("user")
        .with_grants(
            VideoGrant(
                room_join=True,
                room="ai-english-lab",
                can_publish=True,
                can_subscribe=True
            )
        )
    )
    return token.to_jwt()

@app.post("/process_audio")
async def process_audio(file: UploadFile):
    # Save audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
        f.write(await file.read())
        audio_path = f.name

    # Speech → Text
    with open(audio_path, "rb") as audio:
        transcript = client.audio.transcriptions.create(
            file=audio,
            model="whisper-large-v3",
            response_format="text"
        )

    # AI analysis
    feedback_text = analyze_answer(transcript)

    # Text → Speech
    voice_path = text_to_speech(feedback_text)

    return {
        "transcript": transcript,
        "feedback": feedback_text,
        "voice_file": voice_path
    }
