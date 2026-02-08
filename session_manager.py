import time
from datetime import date

# ------------------------------------
# In-memory user session store
# ------------------------------------
USER_SESSIONS = {}

def create_empty_session():
    """
    Creates a fresh session structure for a new user.
    """
    return {
        "practice_time": [],      # list[int]  – minutes per session
        "speaking_score": [],     # list[int]  – 0–100
        "dates": [],              # list[date] – practice dates
        "weak_areas": [],         # list[str]
        "current_page": "home",   # navigation state
        "last_seen": time.time()
    }

def get_user_session(user_id):
    """
    Returns the user's session map.
    Creates one if it does not exist.
    """
    if user_id not in USER_SESSIONS:
        USER_SESSIONS[user_id] = create_empty_session()

    USER_SESSIONS[user_id]["last_seen"] = time.time()
    return USER_SESSIONS[user_id]

def update_practice(
    user_id,
    minutes: int,
    speaking_score: int,
    weak_area: str | None = None
):
    """
    Update user session after a practice activity.
    """
    session = get_user_session(user_id)

    session["practice_time"].append(minutes)
    session["speaking_score"].append(speaking_score)
    session["dates"].append(date.today())

    if weak_area:
        session["weak_areas"].append(weak_area)

def set_current_page(user_id, page: str):
    """
    Track user navigation per session.
    """
    session = get_user_session(user_id)
    session["current_page"] = page

def get_current_page(user_id) -> str:
    """
    Get last visited page for user.
    """
    session = get_user_session(user_id)
    return session.get("current_page", "home")

def clear_user_session(user_id):
    """
    Completely removes user session (on logout).
    """
    if user_id in USER_SESSIONS:
        del USER_SESSIONS[user_id]

def cleanup_inactive_sessions(timeout: int = 3600):
    """
    Removes inactive sessions to save memory.
    """
    now = time.time()
    inactive_users = [
        uid for uid, session in USER_SESSIONS.items()
        if now - session["last_seen"] > timeout
    ]

    for uid in inactive_users:
        del USER_SESSIONS[uid]
