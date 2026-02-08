from gtts import gTTS
import tempfile

def speak_text(text: str) -> str:
    """
    Converts text to speech and returns the audio file path
    """
    tts = gTTS(text=text, lang="en")
    temp_audio = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    tts.save(temp_audio.name)
    return temp_audio.name
