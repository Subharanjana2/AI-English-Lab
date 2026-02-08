import streamlit as st
import auth

def show_login_box():
    st.markdown("""
    <style>
    .login-box {
        width: 480px;
        margin: 5rem auto;
        padding: 2rem 2.5rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        animation: slideUp 0.8s ease-in-out;
    }
    .login-title {
        font-size: 2rem;
        font-weight: 700;
        color: #0a192f;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    .login-sub {
        color: #64748b;
        text-align: center;
        margin-bottom: 2rem;
    }
    @keyframes slideUp {
        from {opacity: 0; transform: translateY(40px);}
        to {opacity: 1; transform: translateY(0);}
    }
    </style>
    """, unsafe_allow_html=True)

    if "mode" not in st.session_state:
        st.session_state.mode = "Sign In"

    with st.container():
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown(f"<div class='login-title'>{st.session_state.mode}</div>", unsafe_allow_html=True)
        if st.session_state.mode == "Sign In":
            st.markdown("<div class='login-sub'>Welcome back! Log in to continue learning.</div>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Sign In", use_container_width=True):
                user = auth.login(username, password)
                if user:
                    st.session_state.user = user
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

            st.write("New here? [Create an account](#)")
            if st.button("Switch to Sign Up"):
                st.session_state.mode = "Sign Up"
                st.rerun()

        else:
            st.markdown("<div class='login-sub'>Create your free account.</div>", unsafe_allow_html=True)
            username = st.text_input("New Username")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            confirm = st.text_input("Confirm Password", type="password")

            if st.button("Sign Up", use_container_width=True):
                if password == confirm:
                    msg = auth.signup(username, password, email)
                    st.success(msg)
                else:
                    st.error("Passwords do not match!")

            if st.button("Switch to Sign In"):
                st.session_state.mode = "Sign In"
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
