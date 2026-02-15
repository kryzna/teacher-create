import streamlit as st
from datetime import datetime

from src.monty.session import init_session_state, require_auth, reload_from_db, flash, show_flash
from src.monty.crud import create_observation, update_observation, delete_observation


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(page_title="Observations - Monty", page_icon="👁️", layout="wide")
    st.markdown("""<style>[data-testid="stSidebarNav"] {display: none !important;}</style>""", unsafe_allow_html=True)
    
    show_flash()
    render_sidebar()
    render_main_content()


def render_sidebar():
    with st.sidebar:
        st.title("📚 Monty")
        st.write(f"Welcome, **{st.session_state.user['name']}**")
        st.write(f"📍 {st.session_state.user['school']} - {st.session_state.user['classroom']}")
        
        st.markdown("---")
        
        st.page_link("app.py", label="Dashboard", icon="🏠")
        st.page_link("pages/students.py", label="Students", icon="👥")
        st.page_link("pages/schedule.py", label="Schedule", icon="📅")
        st.page_link("pages/observations.py", label="Observations", icon="👁️")
        st.page_link("pages/reports.py", label="Reports", icon="📊")
        st.page_link("pages/materials.py", label="Materials", icon="📦")
        st.page_link("pages/daily_tracking.py", label="Daily Tracking", icon="📝")
        st.page_link("pages/settings.py", label="Settings", icon="⚙️")
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            from src.monty.session import logout_user
            logout_user()
            st.rerun()


def render_main_content():
    st.title("👁️ Observations")
    
    tab1, tab2 = st.tabs(["Observation Feed", "New Observation"])
    
    with tab1:
        render_observation_filters()
        render_observation_feed()
    
    with tab2:
        render_new_observation_form()


def render_observation_filters():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search observations", placeholder="Search by student or notes...")
        st.session_state.obs_search = search_query
    
    with col2:
        student_filter = st.selectbox("Filter by student", ["All Students"] + [s["name"] for s in st.session_state.students])
        st.session_state.obs_student_filter = student_filter
    
    with col3:
        area_filter = st.selectbox("Filter by area", ["All Areas", "Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music"])
        st.session_state.obs_area_filter = area_filter


def get_filtered_observations():
    observations = st.session_state.observations
    
    search = st.session_state.get("obs_search", "")
    student_filter = st.session_state.get("obs_student_filter", "All Students")
    area_filter = st.session_state.get("obs_area_filter", "All Areas")
    
    if search:
        observations = [o for o in observations if search.lower() in o["student"].lower() or search.lower() in o["notes"].lower()]
    
    if student_filter != "All Students":
        observations = [o for o in observations if o["student"] == student_filter]
    
    if area_filter != "All Areas":
        observations = [o for o in observations if o["area"] == area_filter]
    
    return observations


def render_observation_feed():
    observations = get_filtered_observations()
    
    if not observations:
        st.info("No observations found matching your criteria.")
        return
    
    st.markdown(f"**{len(observations)} observation(s) found**")
    
    for obs in reversed(observations):
        with st.container(border=True):
            col1, col2, col3 = st.columns([2, 2, 1])
            
            with col1:
                st.subheader(f"👤 {obs['student']}")
                st.write(f"📅 {obs['date']}")
            
            with col2:
                st.write(f"**Area:** {obs['area']}")
                skills = obs.get("skills", [])
                if skills:
                    st.write("**Skills:** " + ", ".join([f"🏷️ {s}" for s in skills]))
            
            with col3:
                st.write(f"🆔 #{obs['id']}")
            
            st.markdown("---")
            st.write(obs['notes'])
            
            col_edit, col_delete = st.columns([1, 1])
            
            with col_edit:
                if st.button("Edit", key=f"edit_obs_{obs['id']}", use_container_width=True):
                    st.session_state.edit_observation = obs
                    st.rerun()
            
            with col_delete:
                if st.button("Delete", key=f"delete_obs_{obs['id']}", use_container_width=True):
                    delete_observation(obs["id"])
                    reload_from_db()
                    flash(f"Deleted observation for {obs['student']}")
                    st.rerun()


def render_new_observation_form():
    st.subheader("➕ New Observation")
    
    if "edit_observation" in st.session_state:
        obs = st.session_state.edit_observation
        st.info(f"Editing observation for {obs['student']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student = st.selectbox("Student", [s["name"] for s in st.session_state.students], 
                                 index=[s["name"] for s in st.session_state.students].index(obs["student"]))
            date = st.date_input("Date", datetime.strptime(obs["date"], "%Y-%m-%d").date())
            area = st.selectbox("Area", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music"],
                              index=["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music"].index(obs["area"]))
        
        with col2:
            skills_input = ", ".join(obs.get("skills", []))
            skills_str = st.text_input("Skills Observed (comma-separated)", value=skills_input)
            skills = [s.strip() for s in skills_str.split(",") if s.strip()]
        
        notes = st.text_area("Observation Notes", value=obs["notes"], height=150)
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.button("Update Observation", use_container_width=True):
                user_id = st.session_state.user["db_id"]
                update_observation(obs["id"], user_id, {
                    "student": student, "date": date.strftime("%Y-%m-%d"),
                    "area": area, "skills": skills, "notes": notes,
                })
                del st.session_state.edit_observation
                reload_from_db()
                flash("Observation updated successfully!")
                st.rerun()
        
        with col_cancel:
            if st.button("Cancel Edit", use_container_width=True):
                del st.session_state.edit_observation
                st.rerun()
    
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            student = st.selectbox("Student", [s["name"] for s in st.session_state.students])
            date = st.date_input("Date", datetime.now().date())
            area = st.selectbox("Area", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music"])
        
        with col2:
            skills_str = st.text_input("Skills Observed (comma-separated)", placeholder="e.g., Concentration, Fine Motor")
            skills = [s.strip() for s in skills_str.split(",") if s.strip()]
        
        notes = st.text_area("Observation Notes", placeholder="Document your observation here...", height=150)
        
        if st.button("Save Observation", use_container_width=True):
            if not student:
                st.error("Please select a student!")
            elif not notes:
                st.error("Please add observation notes!")
            else:
                user_id = st.session_state.user["db_id"]
                create_observation(user_id, {
                    "student": student, "date": date.strftime("%Y-%m-%d"),
                    "area": area, "skills": skills, "notes": notes,
                })
                reload_from_db()
                flash(f"Observation for {student} saved successfully!")
                st.rerun()


render()
