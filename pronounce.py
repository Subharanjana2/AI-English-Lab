# app.py
import streamlit as st
from gtts import gTTS
import tempfile
import os

st.set_page_config(page_title="Word Pronunciation", page_icon="🔊")

def pronounce_word():
    st.header("🔊 Word Pronunciation Practice")

    # Step 1: Enter a word
    word = st.text_input("Enter a word to practice pronunciation:")

    if word:
        st.write(f"📖 Word selected: **{word}**")

        # Step 2: AI Pronunciation (gTTS)
        tts = gTTS(word, lang="en")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")

        st.info("👆 Listen to the AI pronunciation")

def main():
    pronounce_word()

if __name__ == "__main__":
    main()
