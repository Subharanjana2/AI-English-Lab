import streamlit as st
import tempfile
import os
from groq import Groq
from dotenv import load_dotenv

# -------------------------------
# Load environment
# -------------------------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env")

client = Groq(api_key=groq_api_key)


# -------------------------------
# AI Evaluation
# -------------------------------
def analyze_initial_answer(answer_text: str, task_type: str) -> str:
    prompt = f"""
    You are an English coach. Evaluate this {task_type} response:

    "{answer_text}"

    Give a short, clear report:
    - Grammar (/10): Simple rating and short comment
    - Fluency (/10): Smoothness of speech or writing
    - Vocabulary (/10): Word choice and range
    - Pronunciation (/10): Only if Reading or Speaking
    - Overall (/10): Based on overall communication
    - Suggestion (1 line): One short, clear tip to improve
    - Example fix (1 line): A better way to say one sentence
    Keep it brief and easy for students to understand.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a friendly English teacher giving short, clear feedback."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=350
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


# -------------------------------
# Audio Transcription
# -------------------------------
def transcribe_with_groq(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3",
                response_format="text"
            )
        return response
    except Exception as e:
        return f"⚠️ Error in transcription: {str(e)}"


# -------------------------------
# Main Assessment UI
# -------------------------------
def run_initial_assessment():
    st.title("📊 English Communication Assessment")
    st.write("Let's quickly assess your English speaking or writing skills.")

    task_options = ["📝 Typing Response", "🎤 Voice Response", "📖 Reading Task"]
    task_type = st.radio("Choose your task:", task_options)

    default_task_typing = "Introduce yourself and talk about your hobbies in 1 minute."
    default_task_reading = """Reading Passage:
Technology is changing how we live and work. 
AI and automation bring both new chances and new challenges."""

    st.subheader("📌 Task:")

    # -------------------------------
    # Typing Assessment
    # -------------------------------
    if task_type == "📝 Typing Response":
        st.write(default_task_typing)
        answer_text = st.text_area("✍️ Type your response:")
        if answer_text:
            st.subheader("📋 AI Feedback")
            report = analyze_initial_answer(answer_text, "typing")
            st.markdown(report)

    # -------------------------------
    # Voice Assessment
    # -------------------------------
    elif task_type == "🎤 Voice Response":
        st.write(default_task_typing)
        audio = st.audio_input("🎤 Record your voice:")
        if audio:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(audio.getbuffer())
                audio_path = tmpfile.name

            st.success("✅ Audio recorded successfully!")
            answer_text = transcribe_with_groq(audio_path)

            st.subheader("📝 Your Words (Transcribed)")
            st.write(answer_text)

            st.subheader("📋 AI Feedback")
            report = analyze_initial_answer(answer_text, "voice")
            st.markdown(report)

    # -------------------------------
    # Reading Assessment
    # -------------------------------
    elif task_type == "📖 Reading Task":
        st.write(default_task_reading)
        audio = st.audio_input("🎤 Read this aloud:")
        if audio:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                tmpfile.write(audio.getbuffer())
                audio_path = tmpfile.name

            st.success("✅ Audio recorded successfully!")
            answer_text = transcribe_with_groq(audio_path)

            st.subheader("📝 Your Reading (Transcribed)")
            st.write(answer_text)

            st.subheader("📋 AI Feedback")
            report = analyze_initial_answer(answer_text, "reading")
            st.markdown(report)
