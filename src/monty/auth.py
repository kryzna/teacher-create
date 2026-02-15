import streamlit as st

from src.monty.database import get_session, hash_password
from src.monty.models import User
from src.monty.session import login_user, logout_user


def login(username, password):
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and user.password_hash == hash_password(password):
            user_data = {
                "db_id": user.id,
                "id": f"user_{user.id:03d}",
                "name": user.name,
                "email": user.email,
                "school": user.school or "",
                "classroom": user.classroom or "",
            }
            login_user(user_data)
            return True
        return False
    finally:
        session.close()


def logout():
    logout_user()


def get_current_user():
    return st.session_state.user if hasattr(st.session_state, "user") else None
