import hashlib
import db

def hash_pwd(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password, email):
    if db.get_user(username):
        return "User already exists"
    db.add_user(username, hash_pwd(password), email)
    return "✅ Signup successful!"

def login(username, password):
    user = db.get_user(username)
    if not user:
        return None
    stored = user[2]
    if stored == hash_pwd(password):
        return {"id": user[0], "username": user[1], "email": user[3]}
    return None
