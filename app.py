import streamlit as st
import db, auth
from initial_assessment import run_initial_assessment
from speaking import speaking_practice
from voice_practice import voice_practice
from pronounce import pronounce_word
from book_helper_ai import run_book_helper
from dashboard import show_dashboard

# -----------------------------
# Setup & Light Green Background
# -----------------------------
st.set_page_config(page_title="AI English Lab", layout="wide")
db.init_db()

st.markdown("""
<style>
html, body, .stApp {
    min-height: 100vh;
    background: linear-gradient(120deg, #f2fff3 0%, #d8fcd6 100%) !important;
    box-sizing: border-box;
    padding: 0 !important;
    margin: 0 !important;
}
body {font-family: 'Segoe UI', sans-serif;}
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    padding: 1rem 3rem 0.5rem 3rem;
    border-bottom: 1px solid #eee;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    position: sticky;
    top: 0;
    z-index: 100;
    margin: 0 !important;
}
.logo {
    font-size: 1.7rem;
    font-weight: 700;
    color: #0a192f;
    padding-bottom: 0.2rem;
}
.logout-btn {
    background: #0a192f;
    color: white;
    padding: 8px 14px;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: 0.3s;
}
.logout-btn:hover {background: #112240;}
.nav-container {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
    margin-bottom: 0;
}
.nav-btn {
    background: none;
    border: none;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    color: #0a192f;
    padding: 8px 18px;
    border-radius: 6px;
    border-bottom: 2px solid transparent;
    transition: all 0.3s ease;
    flex: 1;
    text-align: center;
    min-width: 120px;
}
.nav-btn:hover {
    color: #64ffda;
    border-bottom: 2px solid #64ffda;
    background-color: #f0fdf9;
}
.nav-btn.active {
    color: #64ffda;
    border-bottom: 2px solid #64ffda;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Session Setup
# -----------------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"

def switch_page(page):
    st.session_state.page = page

# -----------------------------
# Login Section
# -----------------------------
if not st.session_state.user:
    st.markdown("<div class='header'><div class='logo'>AI English Lab</div></div>", unsafe_allow_html=True)
    st.title("Learn, Speak, and Grow with AI 🚀")
    st.write("Improve your English with AI-driven practice, pronunciation help, and comprehension analysis.")

    st.divider()
    mode = st.radio("Choose Action", ["Sign In", "Sign Up"], horizontal=True)

    if mode == "Sign In":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            user = auth.login(username, password)
            if user:
                st.session_state.user = user
                st.success(f"Welcome {user['username']}!")
                st.rerun()
            else:
                st.error("Invalid credentials.")
    else:
        username = st.text_input("New Username")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        if st.button("Create Account"):
            if password == confirm:
                st.info(auth.signup(username, password, email))
            else:
                st.error("Passwords do not match.")

# -----------------------------
# Dashboard Section (After Login)
# -----------------------------
else:
    st.markdown("<div class='header'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 8, 2])
    with col1:
        st.markdown("<div class='logo'>AI English Lab</div>", unsafe_allow_html=True)
    with col2:
        # Book Helper added back to navbar!
        pages = ["home", "assessment", "dashboard", "speaking", "voice", "pronounce", "book"]
        labels = ["🏠 Home", "🧩 Assessment", "📊 Dashboard", "💬 Speaking", "🎙️ Voice", "🔊 Pronounce", "📚 Book Helper"]

        st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
        nav_cols = st.columns(len(pages))
        for i, p in enumerate(pages):
            with nav_cols[i]:
                if st.button(labels[i], key=p, use_container_width=True):
                    switch_page(p)
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.write(f"👋 Hi, {st.session_state.user['username']}")
        if st.button("Logout", key="logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()
    if st.session_state.page == "home":
        st.markdown("### 🏠 Welcome to AI English Lab Dashboard")
        st.info("Use the navigation bar to explore assessments, speaking, book helper, and more features.")
    elif st.session_state.page == "assessment":
        run_initial_assessment()
    elif st.session_state.page == "dashboard":
        show_dashboard()
    elif st.session_state.page == "speaking":
        speaking_practice()
    elif st.session_state.page == "voice":
        voice_practice()
    elif st.session_state.page == "pronounce":
        pronounce_word()
    elif st.session_state.page == "book":
        run_book_helper()
