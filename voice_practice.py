import streamlit as st
import tempfile
import os
from groq import Groq
from dotenv import load_dotenv

# ------------------------------
# Load environment variables
# ------------------------------
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found. Please set it in .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

# ------------------------------
# Generate one interview question
# ------------------------------
def generate_question(role: str, difficulty: str):
    prompt = f"""
    You are an expert HR interviewer.
    Generate ONE {difficulty}-level interview question for a candidate applying as a {role}.
    Respond with only the question text.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an experienced HR interviewer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"⚠️ Error generating question: {e}")
        return "Tell me about yourself."

# ------------------------------
# Transcribe audio
# ------------------------------
def transcribe_with_groq(audio_path: str) -> str:
    try:
        with open(audio_path, "rb") as f:
            response = client.audio.transcriptions.create(
                file=f,
                model="whisper-large-v3",
                response_format="text"
            )
        return response.strip()
    except Exception as e:
        return f"⚠️ Error in transcription: {str(e)}"

# ------------------------------
# Analyze answer
# ------------------------------
def analyze_answer(answer_text: str) -> str:
    prompt = f"""
    You are an interview coach analyzing this answer:
    "{answer_text}"

    Provide:
    1. Corrected grammar version
    2. 2 short suggestions to improve clarity or confidence
    3. Score out of 10 for communication & relevance
    Keep the response short and easy to understand.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a professional English and communication coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error analyzing answer: {str(e)}"

# ------------------------------
# Suggest sample answer
# ------------------------------
def get_suggestion(question: str, role: str, level: str):
    prompt = f"""
    You are a helpful career assistant.
    Give a short, natural sample answer (under 80 words) for this interview question:
    "{question}"

    The answer should sound like a {level} applying for a {role}.
    """
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You give short and practical example interview answers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error generating suggestion: {str(e)}"

# ------------------------------
# Main Interactive Voice Practice
# ------------------------------
def voice_practice():
    st.title("🎙️ AI-Powered Mock Interview")

    role = st.text_input("Enter your interview role (e.g., Data Scientist, Frontend Developer):")
    difficulty = st.radio("Select difficulty level:", ["Easy", "Medium", "Hard"])

    if role:
        if "active" not in st.session_state:
            st.session_state.active = False
            st.session_state.question = None
            st.session_state.feedback = None
            st.session_state.suggestion = None

        if not st.session_state.active:
            if st.button("🚀 Start Interview"):
                st.session_state.active = True
                st.session_state.question = generate_question(role, difficulty)
                st.rerun()

        if st.session_state.active:
            st.subheader("🗣️ Current Question:")
            st.write(st.session_state.question)

            audio_bytes = st.audio_input("🎤 Record your answer here:")

            if audio_bytes:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
                    tmpfile.write(audio_bytes.getbuffer())
                    audio_path = tmpfile.name

                st.success("✅ Audio recorded successfully!")

                user_answer = transcribe_with_groq(audio_path)
                st.write("🧾 You said:")
                st.info(user_answer)

                feedback = analyze_answer(user_answer)
                st.session_state.feedback = feedback

                st.subheader("💬 AI Feedback:")
                st.write(feedback)

            st.markdown("---")
            st.subheader("💡 Need Help Answering?")
            answer_level = st.radio("Select answer type:", ["Fresher", "Professional"], horizontal=True)

            if st.button("💬 Get Suggestion"):
                suggestion = get_suggestion(
                    st.session_state.question, role, answer_level
                )
                st.info(suggestion)

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Next Question ▶️"):
                    st.session_state.question = generate_question(role, difficulty)
                    st.session_state.feedback = None
                    st.session_state.suggestion = None
                    st.rerun()

            with col2:
                if st.button("⏹️ Stop Interview"):
                    st.session_state.clear()
                    st.rerun()

# ------------------------------
# Run app
# ------------------------------
if __name__ == "__main__":
    voice_practice()
