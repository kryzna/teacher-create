import streamlit as st


def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "landing"
    if "students" not in st.session_state:
        st.session_state.students = [
            {"id": 1, "name": "Emma Johnson", "age": 5, "interests": ["Nature", "Painting"], "allergies": ["Peanuts"], "parent_name": "Sarah Johnson", "parent_email": "sarah.j@email.com"},
            {"id": 2, "name": "Liam Chen", "age": 4, "interests": ["Building Blocks", "Music"], "allergies": [], "parent_name": "David Chen", "parent_email": "david.c@email.com"},
            {"id": 3, "name": "Olivia Martinez", "age": 6, "interests": ["Reading", "Science"], "allergies": ["Milk", "Eggs"], "parent_name": "Maria Martinez", "parent_email": "maria.m@email.com"},
            {"id": 4, "name": "Noah Williams", "age": 5, "interests": ["Sports", "Animals"], "allergies": [], "parent_name": "James Williams", "parent_email": "james.w@email.com"},
            {"id": 5, "name": "Ava Thompson", "age": 4, "interests": ["Dancing", "Art"], "allergies": ["Tree Nuts"], "parent_name": "Lisa Thompson", "parent_email": "lisa.t@email.com"},
            {"id": 6, "name": "Ethan Brown", "age": 6, "interests": ["Mathematics", "Puzzles"], "allergies": ["Wheat"], "parent_name": "Robert Brown", "parent_email": "robert.b@email.com"},
        ]
    if "schedule" not in st.session_state:
        st.session_state.schedule = [
            {"id": 1, "day": "Monday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
            {"id": 2, "day": "Monday", "time": "9:00 AM", "activity": "Practical Life", "duration": 45, "students": "Primary A"},
            {"id": 3, "day": "Monday", "time": "10:00 AM", "activity": "Language Arts", "duration": 45, "students": "Primary B"},
            {"id": 4, "day": "Monday", "time": "11:00 AM", "activity": "Outdoor Play", "duration": 30, "students": "All"},
            {"id": 5, "day": "Tuesday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
            {"id": 6, "day": "Tuesday", "time": "9:00 AM", "activity": "Mathematics", "duration": 45, "students": "Primary A"},
            {"id": 7, "day": "Tuesday", "time": "10:00 AM", "activity": "Sensory Activities", "duration": 45, "students": "Primary B"},
            {"id": 8, "day": "Wednesday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
            {"id": 9, "day": "Wednesday", "time": "9:00 AM", "activity": "Art & Creativity", "duration": 60, "students": "All"},
            {"id": 10, "day": "Thursday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
            {"id": 11, "day": "Thursday", "time": "9:00 AM", "activity": "Science & Nature", "duration": 45, "students": "Primary A"},
            {"id": 12, "day": "Thursday", "time": "10:00 AM", "activity": "Music & Movement", "duration": 45, "students": "Primary B"},
            {"id": 13, "day": "Friday", "time": "8:30 AM", "activity": "Morning Circle", "duration": 15, "students": "All"},
            {"id": 14, "day": "Friday", "time": "9:00 AM", "activity": "Free Choice Work", "duration": 60, "students": "All"},
            {"id": 15, "day": "Friday", "time": "11:00 AM", "activity": "Show & Tell", "duration": 30, "students": "All"},
        ]
    if "observations" not in st.session_state:
        st.session_state.observations = [
            {"id": 1, "student": "Emma Johnson", "date": "2026-02-10", "area": "Practical Life", "notes": "Emma showed excellent concentration while working with the pouring activity. She was able to pour water from one jug to another with minimal spills.", "skills": ["Concentration", "Fine Motor"]},
            {"id": 2, "student": "Liam Chen", "date": "2026-02-10", "area": "Sensorial", "notes": "Liam spent 20 minutes working with the pink tower. He carefully stacked the cubes from largest to smallest, showing good visual discrimination.", "skills": ["Visual Discrimination", "Math Readiness"]},
            {"id": 3, "student": "Olivia Martinez", "date": "2026-02-11", "area": "Language", "notes": "Olivia is beginning to sound out CVC words using the movable alphabet. She successfully wrote 'cat', 'dog', and 'sun'.", "skills": ["Phonics", "Writing"]},
            {"id": 4, "student": "Noah Williams", "date": "2026-02-11", "area": "Mathematics", "notes": "Noah demonstrated understanding of number rods 1-10. He was able to count accurately and associate quantity with symbol.", "skills": ["Counting", "Quantity/Symbol"]},
            {"id": 5, "student": "Ava Thompson", "date": "2026-02-12", "area": "Art", "notes": "Ava enjoyed the cutting activity with scissors. She showed good control and was able to follow curved lines.", "skills": ["Fine Motor", "Hand-eye Coordination"]},
        ]
    if "materials" not in st.session_state:
        st.session_state.materials = [
            {"id": 1, "name": "Pink Tower", "category": "Sensorial", "age_range": "3-6", "description": "Ten pink wooden cubes of varying sizes to develop visual discrimination of dimension.", "in_stock": True, "times_used": 45},
            {"id": 2, "name": "Brown Stairs", "category": "Sensorial", "age_range": "3-6", "description": "Ten brown wooden prisms of varying thickness to develop visual discrimination.", "in_stock": True, "times_used": 38},
            {"id": 3, "name": "Red Rods", "category": "Sensorial", "age_range": "3-6", "description": "Ten red wooden rods of varying length to develop visual discrimination of length.", "in_stock": True, "times_used": 32},
            {"id": 4, "name": "Movable Alphabet", "category": "Language", "age_range": "3-6", "description": "Set of wooden letters for building words and sentences phonetically.", "in_stock": True, "times_used": 67},
            {"id": 5, "name": "Number Rods", "category": "Mathematics", "age_range": "3-6", "description": "Red and blue wooden rods for learning numbers 1-10 and quantity.", "in_stock": True, "times_used": 52},
            {"id": 6, "name": "Sandpaper Letters", "category": "Language", "age_range": "2.5-4", "description": "Rough letters for tactile letter recognition and learning letter sounds.", "in_stock": True, "times_used": 28},
        ]
    if "daily_entries" not in st.session_state:
        st.session_state.daily_entries = []
    if "show_login_modal" not in st.session_state:
        st.session_state.show_login_modal = False


def login_user(user_data):
    st.session_state.authenticated = True
    st.session_state.user = user_data
    st.session_state.current_page = "dashboard"
    st.session_state.show_login_modal = False


def logout_user():
    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.current_page = "landing"


def require_auth():
    if not st.session_state.authenticated:
        st.session_state.current_page = "landing"
        st.rerun()
