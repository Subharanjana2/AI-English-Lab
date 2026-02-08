import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

def show_dashboard():
    st.title("📊 Your AI English Lab Dashboard")

    st.markdown("""
    ### 🧠 Learning Overview
    Track your daily progress, assessment scores, and speaking improvements below.
    """)

    # -----------------------------
    # Sample data (replace later with user-specific data)
    # -----------------------------
    np.random.seed(42)
    days = pd.date_range(end=pd.Timestamp.today(), periods=14)
    practice_time = np.random.randint(10, 60, size=14)
    speaking_score = np.random.randint(60, 95, size=14)

    data = pd.DataFrame({
        "Day": days.strftime("%b %d"),
        "Practice Time (min)": practice_time,
        "Speaking Score": speaking_score
    })

    st.write("#### 🕒 Your Practice Summary (Past 2 Weeks)")
    st.dataframe(data, use_container_width=True)

    # -----------------------------
    # 3D Learning Streak Visualization
    # -----------------------------
    st.markdown("### 🌟 3D Learning Streak Visualization")

    # Create meshgrid for a proper 3D surface
    x = np.arange(1, len(data) + 1)
    y = np.linspace(0, 1, len(data))
    X, Y = np.meshgrid(x, y)

    # Create a smooth Z surface (mix practice and score)
    Z = np.outer(practice_time, speaking_score) / 100  # normalized intensity

    fig = go.Figure(data=[go.Surface(
        x=X,
        y=Y,
        z=Z,
        colorscale="Viridis",
        showscale=True,
        opacity=0.95,
        hovertemplate="Day %{x}<br>Engagement %{y:.2f}<br>Score Intensity %{z:.2f}<extra></extra>"
    )])

    fig.update_layout(
        title="Your 3D Learning Streak 📈",
        scene=dict(
            xaxis_title="Day",
            yaxis_title="Engagement",
            zaxis_title="Performance Index",
            xaxis=dict(showbackground=True, backgroundcolor="rgba(0,0,0,0.05)"),
            yaxis=dict(showbackground=True, backgroundcolor="rgba(0,0,0,0.05)"),
            zaxis=dict(showbackground=True, backgroundcolor="rgba(0,0,0,0.05)"),
        ),
        height=600,
        margin=dict(l=0, r=0, b=0, t=50),
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # Summary Metrics
    # -----------------------------
    avg_time = np.mean(practice_time)
    avg_score = np.mean(speaking_score)

    st.markdown("### 📈 Weekly Summary")
    c1, c2, c3 = st.columns(3)
    c1.metric("Average Practice Time", f"{avg_time:.1f} mins/day")
    c2.metric("Average Speaking Score", f"{avg_score:.1f} / 100")
    c3.metric("Active Days", f"{len(days)} days")

    st.markdown("---")
    st.success("🔥 Keep your streak going! Practice daily to level up your English communication skills.")
