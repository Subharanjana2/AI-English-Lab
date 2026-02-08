import streamlit as st
import PyPDF2
import tempfile
import os
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
import base64

# ---------------------------------
# Setup
# ---------------------------------
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------------------------
# Helper Functions
# ---------------------------------
def extract_text_from_pdf(file):
    """Extracts text content from a PDF."""
    pdf_reader = PyPDF2.PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text.strip()

def speak_text(text, filename="output.mp3"):
    """Converts text to speech and returns file path."""
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def chat_with_ai(prompt):
    """Sends a message to the Groq model and returns response."""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a friendly and intelligent reading assistant who explains stories clearly and interactively."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message.content.strip()

# ---------------------------------
# Streamlit UI
# ---------------------------------
def run_book_helper():
    st.markdown(
        """
        <style>
        .chat-bubble {
            background-color: #f0f2f6;
            padding: 15px;
            border-radius: 15px;
            margin-bottom: 10px;
            width: 80%;
        }
        .user-bubble {
            background-color: #DCF8C6;
            align-self: flex-end;
        }
        .assistant-bubble {
            background-color: #E9E9EB;
            align-self: flex-start;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("📖 Chat with Your Book")
    st.write("Upload a storybook, get an AI-powered narration, understand words, and test how well you followed the story!")

    uploaded_file = st.file_uploader("📘 Upload your book (PDF only):", type=["pdf"])

    if uploaded_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        with open(tmp_path, "rb") as f:
            book_text = extract_text_from_pdf(f)

        st.session_state.book_text = book_text
        st.success("✅ Book uploaded successfully!")

        preview = book_text[:1500] + "..." if len(book_text) > 1500 else book_text
        st.text_area("📚 Book Preview:", preview, height=200)

        st.subheader("🎧 Story Summary")
        if st.button("Summarize Story"):
            with st.spinner("AI reading and summarizing your story..."):
                summary_prompt = f"Summarize the story below in a simple and emotional storytelling way that a reader can easily understand:\n\n{book_text[:7000]}"
                summary = chat_with_ai(summary_prompt)
                st.session_state.story_summary = summary

            st.success("✨ Story summarized successfully!")
            st.markdown(f"<div class='assistant-bubble'>{summary}</div>", unsafe_allow_html=True)

            audio_path = speak_text(summary)
            st.audio(audio_path, format="audio/mp3")

        # ---------------------------------
        # Word Understanding Section
        # ---------------------------------
        st.subheader("🪄 Ask Word Meanings Instantly")
        user_word = st.text_input("Enter a word from the book you'd like to understand:")
        if st.button("Explain Word"):
            meaning_prompt = f"Explain the meaning of the word '{user_word}' in simple terms with a short example."
            meaning = chat_with_ai(meaning_prompt)
            st.markdown(f"<div class='assistant-bubble'>{meaning}</div>", unsafe_allow_html=True)
            audio_path = speak_text(meaning)
            st.audio(audio_path, format="audio/mp3")

        # ---------------------------------
        # Reader Engagement & Analysis
        # ---------------------------------
        st.subheader("💭 Reader Understanding & Feedback")
        st.write("Answer this in your own words: *What did you understand or feel about the story?*")
        user_reflection = st.text_area("✍️ Type your thoughts here...")

        if st.button("Analyze My Understanding"):
            with st.spinner("Analyzing your response..."):
                analyze_prompt = f"Here’s a summary of a story: {st.session_state.get('story_summary', '')}\n\nUser reflection: {user_reflection}\n\nEvaluate how deeply the user understood the story, highlight their emotional connection, and suggest one similar story/book they might enjoy next."
                feedback = chat_with_ai(analyze_prompt)
                st.markdown(f"<div class='assistant-bubble'>{feedback}</div>", unsafe_allow_html=True)
                audio_path = speak_text(feedback)
                st.audio(audio_path, format="audio/mp3")

