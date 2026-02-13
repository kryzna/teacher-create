import streamlit as st

from src.monty.session import login_user, logout_user


DEMO_USER = {
    "id": "demo_001",
    "name": "Demo Teacher",
    "email": "demo@monty.app",
    "school": "Montessori Academy",
    "classroom": "Primary",
}


def login(username, password):
    if username == "demo" and password == "demo":
        login_user(DEMO_USER)
        return True
    return False


def logout():
    logout_user()


def get_current_user():
    return st.session_state.user if hasattr(st.session_state, "user") else None
