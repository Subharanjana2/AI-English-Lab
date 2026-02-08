import time
import jwt
import os
from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

LIVEKIT_API_KEY = os.getenv("LIVEKIT_API_KEY")
LIVEKIT_API_SECRET = os.getenv("LIVEKIT_API_SECRET")

@app.get("/token")
def generate_token():
    now = int(time.time())

    payload = {
        "iss": LIVEKIT_API_KEY,
        "sub": "user",
        "nbf": now,
        "exp": now + 3600,
        "video": {
            "roomJoin": True,
            "room": "ai-english-lab",
            "canPublish": True,
            "canSubscribe": True
        }
    }

    token = jwt.encode(
        payload,
        LIVEKIT_API_SECRET,
        algorithm="HS256"
    )

    return token
