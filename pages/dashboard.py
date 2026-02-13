import streamlit as st
from datetime import datetime, date

from src.monty.session import init_session_state, require_auth, logout_user


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(
        page_title="Dashboard - Monty",
        page_icon="📚",
        layout="wide"
    )
    
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
            logout_user()
            st.rerun()


def render_main_content():
    render_welcome_banner()
    render_stats_cards()
    render_quick_actions()
    render_today_schedule()
    render_recent_observations()
    render_ai_assistant()


def render_welcome_banner():
    today = date.today().strftime("%A, %B %d, %Y")
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 30px;
    ">
        <h1 style="margin: 0; font-size: 32px;">Good {get_time_greeting()}! 👋</h1>
        <p style="margin: 10px 0 0 0; opacity: 0.9;">{today}</p>
        <p style="margin: 10px 0 0 0; opacity: 0.8;">Let's make today count for your students!</p>
    </div>
    """, unsafe_allow_html=True)


def get_time_greeting():
    hour = datetime.now().hour
    if hour < 12:
        return "Morning"
    elif hour < 17:
        return "Afternoon"
    else:
        return "Evening"


def render_stats_cards():
    st.subheader("📊 Today's Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Students", len(st.session_state.students), "+0 today")
    with col2:
        st.metric("Observations", len(st.session_state.observations), "+0 today")
    with col3:
        st.metric("Activities", len(st.session_state.daily_entries), "+0 today")
    with col4:
        st.metric("Materials Used", 0, "+0 today")


def render_quick_actions():
    st.subheader("⚡ Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("➕ Add Student", use_container_width=True):
            st.session_state.current_page = "students"
            st.rerun()
    with col2:
        if st.button("👁️ New Observation", use_container_width=True):
            st.session_state.current_page = "observations"
            st.rerun()
    with col3:
        if st.button("📝 Log Activity", use_container_width=True):
            st.session_state.current_page = "daily_tracking"
            st.rerun()
    with col4:
        if st.button("📧 Send Newsletter", use_container_width=True):
            st.session_state.current_page = "daily_tracking"
            st.rerun()


def render_today_schedule():
    st.subheader("📅 Today's Schedule")
    
    schedule_items = [
        {"time": "8:30 AM", "activity": "Morning Circle", "students": "All"},
        {"time": "9:00 AM", "activity": "Practical Life Work", "students": "Primary A"},
        {"time": "10:00 AM", "activity": "Language Arts", "students": "Primary B"},
        {"time": "11:00 AM", "activity": "Outdoor Time", "students": "All"},
        {"time": "12:00 PM", "activity": "Lunch", "students": "All"},
    ]
    
    with st.expander("View Today's Schedule", expanded=True):
        for item in schedule_items:
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                st.write(f"**{item['time']}**")
            with col2:
                st.write(item['activity'])
            with col3:
                st.caption(item['students'])


def render_recent_observations():
    st.subheader("👁️ Recent Observations")
    
    observations = st.session_state.observations[-5:] if st.session_state.observations else []
    
    if not observations:
        st.info("No observations recorded yet. Start documenting your students' progress!")
    else:
        for obs in reversed(observations):
            with st.expander(f"📝 {obs.get('student', 'Student')} - {obs.get('date', '')}"):
                st.write(f"**Area:** {obs.get('area', 'N/A')}")
                st.write(f"**Observation:** {obs.get('notes', 'No notes')}")


def render_ai_assistant():
    st.subheader("🤖 Ask Monty")
    
    with st.expander("AI Assistant", expanded=True):
        if "ai_messages" not in st.session_state:
            st.session_state.ai_messages = []
        
        for msg in st.session_state.ai_messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])
        
        prompt = st.chat_input("Ask Monty anything about your classroom, students, or Montessori methodology...")
        
        if prompt:
            st.session_state.ai_messages.append({"role": "user", "content": prompt})
            
            response = generate_ai_response(prompt)
            st.session_state.ai_messages.append({"role": "assistant", "content": response})
            
            st.rerun()


def generate_ai_response(prompt):
    prompt_lower = prompt.lower()
    
    if "lesson" in prompt_lower or "plan" in prompt_lower:
        return "I'd be happy to help you create a lesson plan! What subject area and age group are you working with? I can suggest activities aligned with Montessori curriculum standards."
    elif "observation" in prompt_lower or "observe" in prompt_lower:
        return "For effective observations, focus on: 1) What the child is choosing to do 2) How long they maintain focus 3) Any repeated behaviors 4) Social interactions. Would you like me to create an observation template?"
    elif "material" in prompt_lower or "materials" in prompt_lower:
        return "Montessori materials should be: accessible, self-correcting, and presented in a logical sequence. What specific material area are you looking to incorporate?"
    elif "progress" in prompt_lower or "report" in prompt_lower:
        return "I can help you generate progress reports! I can create personalized newsletters highlighting each student's achievements and next steps. Would you like me to generate one for a specific student or the whole class?"
    else:
        return f"That's a great question about '{prompt}'! As your Montessori assistant, I can help with lesson planning, observations, student progress tracking, and generating parent communications. What specific aspect would you like to explore?"


if __name__ == "__main__":
    render()
