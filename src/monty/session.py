import streamlit as st

from src.monty.database import init_db
from src.monty.crud import (
    list_students,
    list_observations,
    list_schedules,
    list_materials,
    list_daily_entries,
    get_user_settings,
)


def _get_user_id() -> int | None:
    user = st.session_state.get("user")
    if user and isinstance(user, dict):
        return user.get("db_id")
    return None


def init_session_state():
    # Ensure database tables exist and demo data is seeded on first run
    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state.db_initialized = True

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"
    if "show_login_modal" not in st.session_state:
        st.session_state.show_login_modal = False

    # Load data from DB when user is authenticated
    user_id = _get_user_id()
    if user_id is not None:
        if "students" not in st.session_state:
            st.session_state.students = list_students(user_id)
        if "schedule" not in st.session_state:
            st.session_state.schedule = list_schedules(user_id)
        if "observations" not in st.session_state:
            st.session_state.observations = list_observations(user_id)
        if "materials" not in st.session_state:
            st.session_state.materials = list_materials(user_id)
        if "daily_entries" not in st.session_state:
            st.session_state.daily_entries = list_daily_entries(user_id)
    else:
        if "students" not in st.session_state:
            st.session_state.students = []
        if "schedule" not in st.session_state:
            st.session_state.schedule = []
        if "observations" not in st.session_state:
            st.session_state.observations = []
        if "materials" not in st.session_state:
            st.session_state.materials = []
        if "daily_entries" not in st.session_state:
            st.session_state.daily_entries = []


def reload_from_db():
    """Force reload all data from the database into session state."""
    user_id = _get_user_id()
    if user_id is not None:
        st.session_state.students = list_students(user_id)
        st.session_state.schedule = list_schedules(user_id)
        st.session_state.observations = list_observations(user_id)
        st.session_state.materials = list_materials(user_id)
        st.session_state.daily_entries = list_daily_entries(user_id)


def login_user(user_data):
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.current_page = "dashboard"
    st.session_state.show_login_modal = False
    # Clear cached data so it reloads from DB for the new user
    for key in ["students", "schedule", "observations", "materials", "daily_entries", "settings"]:
        st.session_state.pop(key, None)


def logout_user():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.current_page = "landing"
    # Clear cached data
    for key in ["students", "schedule", "observations", "materials", "daily_entries", "settings"]:
        st.session_state.pop(key, None)


def flash(message: str, level: str = "success"):
    """Store a flash message to display after st.rerun()."""
    st.session_state._flash = {"message": message, "level": level}


def show_flash():
    """Display and clear any pending flash message. Call at top of render()."""
    flash_data = st.session_state.pop("_flash", None)
    if flash_data:
        getattr(st, flash_data["level"], st.info)(flash_data["message"])


def require_auth():
    if not st.session_state.authenticated:
        st.session_state.current_page = "landing"
        try:
            st.switch_page("app.py")
        except Exception:
            st.stop()
