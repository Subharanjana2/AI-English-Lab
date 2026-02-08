import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

# -------------------------------
# Load Environment
# -------------------------------
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("⚠️ Missing GROQ_API_KEY. Please add it to your .env file.")
else:
    client = Groq(api_key=groq_api_key)

# -------------------------------
# Get AI Response
# -------------------------------
def chat_with_groq(conversation_history, scenario):
    if not groq_api_key:
        return "⚠️ GROQ_API_KEY not found. Please configure your environment."

    # Format conversation text
    formatted_history = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in conversation_history]
    )

    prompt = f"""
    You are a friendly English-speaking partner.
    Scenario: {scenario}

    You are having a natural, back-and-forth conversation with the learner.
    Keep responses short (1–3 sentences), positive, and natural.
    If the learner makes mistakes, gently correct them and keep the flow.

    Current conversation:
    {formatted_history}

    Now reply as the AI partner.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error getting AI response: {str(e)}"


# -------------------------------
# Speaking Conversation Module
# -------------------------------
def speaking_practice():
    st.title("🎙️ AI Speaking Partner")

    scenario = st.selectbox(
        "Choose a conversation scenario:",
        ["Ordering Food at a Restaurant", "Booking a Taxi", "Job Interview", "Casual Chat"]
    )

    st.info(f"🗣️ Scenario: {scenario}")

    # Initialize conversation state
    if "conversation" not in st.session_state:
        st.session_state.conversation = []
    if "active" not in st.session_state:
        st.session_state.active = False

    # Start Conversation Button
    if not st.session_state.active:
        if st.button("▶️ Start Conversation"):
            st.session_state.active = True
            if scenario == "Ordering Food at a Restaurant":
                first_question = "👋 Hello! Welcome to our restaurant. What would you like to order today?"
            elif scenario == "Booking a Taxi":
                first_question = "🚕 Hi there! Where would you like to go today?"
            elif scenario == "Job Interview":
                first_question = "💼 Hello! Can you tell me a bit about yourself?"
            else:
                first_question = "😊 Hi there! How’s your day going so far?"

            st.session_state.conversation = [{"role": "ai", "content": first_question}]
            st.rerun()

    # Active Conversation Loop
    if st.session_state.active:
        st.subheader("🗨️ Live Conversation")

        # Display Conversation History
        for msg in st.session_state.conversation:
            if msg["role"] == "user":
                st.markdown(f"**🧑 You:** {msg['content']}")
            else:
                st.markdown(f"**🤖 AI:** {msg['content']}")

        # User input
        user_input = st.text_input("Your reply:", key="user_message")

        col1, col2 = st.columns(2)
        with col1:
            send = st.button("Send")
        with col2:
            stop = st.button("⛔ Stop Conversation")

        if send and user_input.strip():
            st.session_state.conversation.append({"role": "user", "content": user_input})
            ai_reply = chat_with_groq(st.session_state.conversation, scenario)
            st.session_state.conversation.append({"role": "ai", "content": ai_reply})
            st.rerun()

        if stop:
            st.session_state.active = False
            st.success("✅ Conversation Ended. Great job practicing!")
            st.session_state.conversation = []
