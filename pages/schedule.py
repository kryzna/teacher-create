import streamlit as st
from src.monty.session import init_session_state, require_auth


def render():
    init_session_state()
    require_auth()
    
    st.markdown("""<style>[data-testid="stSidebarNav"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.set_page_config(page_title="Schedule - Monty", page_icon="📅", layout="wide")
    
    render_sidebar()
    render_main_content()


def render_sidebar():
    with st.sidebar:
        st.title("📚 Monty")
        st.write(f"Welcome, **{st.session_state.user['name']}**")
        st.write(f"📍 {st.session_state.user['school']} - {st.session_state.user['classroom']}")
        
        st.markdown("---")
        
        st.page_link("app.py", label="🏠 Dashboard", icon="🏠")
        st.page_link("pages/students.py", label="👥 Students", icon="👥")
        st.page_link("pages/schedule.py", label="📅 Schedule", icon="📅")
        st.page_link("pages/observations.py", label="👁️ Observations", icon="👁️")
        st.page_link("pages/reports.py", label="📊 Reports", icon="📊")
        st.page_link("pages/materials.py", label="📦 Materials", icon="📦")
        st.page_link("pages/daily_tracking.py", label="📝 Daily Tracking", icon="📝")
        st.page_link("pages/settings.py", label="⚙️ Settings", icon="⚙️")
        
        st.markdown("---")
        
        if st.button("Logout", use_container_width=True):
            from src.monty.session import logout_user
            logout_user()
            st.rerun()


def render_main_content():
    st.title("📅 Schedule")
    
    tab1, tab2 = st.tabs(["Weekly Calendar", "Add Activity"])
    
    with tab1:
        render_week_view()
    
    with tab2:
        render_add_activity_form()


def render_week_view():
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    
    st.subheader("📅 This Week's Schedule")
    
    selected_day = st.selectbox("Select Day", days)
    
    day_activities = [a for a in st.session_state.schedule if a["day"] == selected_day]
    day_activities.sort(key=lambda x: x["time"])
    
    if not day_activities:
        st.info(f"No activities scheduled for {selected_day}.")
        return
    
    for activity in day_activities:
        with st.container(border=True):
            col_time, col_activity, col_duration, col_students = st.columns([1, 3, 1, 1])
            
            with col_time:
                st.write(f"🕐 **{activity['time']}**")
            
            with col_activity:
                st.subheader(activity["activity"])
            
            with col_duration:
                st.write(f"⏱️ {activity['duration']} min")
            
            with col_students:
                st.write(f"👥 {activity['students']}")
            
            col_edit, col_delete = st.columns([1, 1])
            
            with col_edit:
                if st.button("Edit", key=f"edit_activity_{activity['id']}", use_container_width=True):
                    st.session_state.edit_activity = activity
                    st.rerun()
            
            with col_delete:
                if st.button("Delete", key=f"delete_activity_{activity['id']}", use_container_width=True):
                    st.session_state.schedule = [a for a in st.session_state.schedule if a["id"] != activity["id"]]
                    st.success(f"Deleted {activity['activity']}")
                    st.rerun()


def render_add_activity_form():
    st.subheader("➕ Add New Activity")
    
    if "edit_activity" in st.session_state:
        activity = st.session_state.edit_activity
        st.info(f"Editing {activity['activity']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], 
                             index=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"].index(activity["day"]))
            time = st.text_input("Time", value=activity["time"])
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=activity["duration"])
            students = st.selectbox("Students", ["All", "Primary A", "Primary B"], 
                                  index=["All", "Primary A", "Primary B"].index(activity["students"]) if activity["students"] in ["All", "Primary A", "Primary B"] else 0)
        
        activity_name = st.text_input("Activity Name", value=activity["activity"])
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.button("Update Activity", use_container_width=True):
                for a in st.session_state.schedule:
                    if a["id"] == activity["id"]:
                        a["day"] = day
                        a["time"] = time
                        a["duration"] = duration
                        a["students"] = students
                        a["activity"] = activity_name
                        break
                del st.session_state.edit_activity
                st.success("Activity updated successfully!")
                st.rerun()
        
        with col_cancel:
            if st.button("Cancel Edit", use_container_width=True):
                del st.session_state.edit_activity
                st.rerun()
    
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            day = st.selectbox("Day", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
            time = st.text_input("Time", placeholder="e.g., 9:00 AM")
        
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=5, max_value=120, value=30)
            students = st.selectbox("Students", ["All", "Primary A", "Primary B"])
        
        activity_name = st.text_input("Activity Name", placeholder="e.g., Morning Circle")
        
        if st.button("Add Activity", use_container_width=True):
            if not activity_name:
                st.error("Activity name is required!")
            elif not time:
                st.error("Time is required!")
            else:
                new_id = max([a["id"] for a in st.session_state.schedule], default=0) + 1
                new_activity = {
                    "id": new_id,
                    "day": day,
                    "time": time,
                    "activity": activity_name,
                    "duration": duration,
                    "students": students
                }
                st.session_state.schedule.append(new_activity)
                st.success(f"Added {activity_name} successfully!")
                st.rerun()


if __name__ == "__main__":
    render()
