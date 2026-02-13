import streamlit as st

from src.monty.session import init_session_state, require_auth, logout_user


def render():
    init_session_state()
    require_auth()
    
    st.markdown("""<style>[data-testid="stSidebarNav"] {display: none !important;}</style>""", unsafe_allow_html=True)
    st.set_page_config(page_title="Settings - Monty", page_icon="⚙️", layout="wide")
    
    init_settings_session_state()
    inject_mobile_css()
    
    render_sidebar()
    render_main_content()
    render_mobile_nav()


def init_settings_session_state():
    if "settings" not in st.session_state:
        st.session_state.settings = {
            "profile": {
                "name": "Jennifer Adams",
                "email": "jennifer.adams@montessori.edu",
                "phone": "(555) 123-4567",
                "bio": "Certified Montessori teacher with 8 years of experience in primary education."
            },
            "classroom": {
                "school_name": "Willow Creek Montessori",
                "classroom_name": "Primary A (Ages 3-6)",
                "academic_year": "2025-2026",
                "student_count": 18,
                "assistant_teachers": ["Maria Garcia", "David Chen"]
            },
            "notifications": {
                "email_observations": True,
                "email_reports": True,
                "email_parent_communications": True,
                "push_activities": True,
                "push_schedule_changes": True,
                "weekly_digest": True,
                "reminder_time": "6:00 PM"
            },
            "privacy_security": {
                "two_factor_auth": False,
                "session_timeout": 30,
                "data_export": True,
                "share_progress_with_parents": True,
                "analytics_tracking": True
            },
            "appearance": {
                "theme": "light",
                "accent_color": "Purple",
                "font_size": "Medium",
                "compact_mode": False,
                "sidebar_collapsed": False
            }
        }


def inject_mobile_css():
    st.markdown("""
    <style>
    @media (max-width: 768px) {
        .stSidebar {
            display: none;
        }
        .mobile-nav {
            display: flex !important;
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: white;
            border-top: 1px solid #e0e0e0;
            padding: 8px 16px;
            justify-content: space-around;
            z-index: 1000;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }
        .mobile-nav a {
            text-decoration: none;
            color: #666;
            font-size: 12px;
            text-align: center;
            padding: 4px;
        }
        .mobile-nav a.active {
            color: #667eea;
        }
        .mobile-nav .nav-icon {
            font-size: 24px;
            display: block;
        }
        .main-content {
            padding-bottom: 80px;
        }
    }
    @media (min-width: 769px) {
        .mobile-nav {
            display: none !important;
        }
    }
    .mobile-nav {
        display: none;
    }
    .settings-section {
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 10px;
        background: #f8f9fa;
    }
    .settings-card {
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)


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


def render_mobile_nav():
    st.markdown("""
    <div class="mobile-nav">
        <a href="#" onclick="window.location.href='app.py'">
            <span class="nav-icon">🏠</span>
            Dashboard
        </a>
        <a href="#" onclick="window.location.href='pages/students.py'">
            <span class="nav-icon">👥</span>
            Students
        </a>
        <a href="#" onclick="window.location.href='pages/schedule.py'">
            <span class="nav-icon">📅</span>
            Schedule
        </a>
        <a href="#" onclick="window.location.href='pages/settings.py'" class="active">
            <span class="nav-icon">⚙️</span>
            Settings
        </a>
    </div>
    """, unsafe_allow_html=True)


def render_main_content():
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["👤 Profile", "🏫 Classroom", "🔔 Notifications", "🔒 Privacy", "🎨 Appearance"])
    
    with tab1:
        render_profile_section()
    
    with tab2:
        render_classroom_section()
    
    with tab3:
        render_notifications_section()
    
    with tab4:
        render_privacy_section()
    
    with tab5:
        render_appearance_section()


def render_profile_section():
    st.subheader("👤 Profile Settings")
    
    settings = st.session_state.settings["profile"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Full Name", value=settings["name"])
        email = st.text_input("Email", value=settings["email"])
    
    with col2:
        phone = st.text_input("Phone", value=settings["phone"])
    
    bio = st.text_area("Bio", value=settings["bio"], height=100)
    
    if st.button("Save Profile", type="primary"):
        st.session_state.settings["profile"] = {
            "name": name,
            "email": email,
            "phone": phone,
            "bio": bio
        }
        st.success("Profile saved successfully!")
    
    st.markdown("---")
    
    st.subheader("🔑 Change Password")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_password = st.text_input("Current Password", type="password")
    
    with col2:
        new_password = st.text_input("New Password", type="password")
    
    confirm_password = st.text_input("Confirm New Password", type="password")
    
    if st.button("Update Password"):
        if new_password == confirm_password:
            st.success("Password updated successfully!")
        else:
            st.error("Passwords do not match!")


def render_classroom_section():
    st.subheader("🏫 Classroom Settings")
    
    settings = st.session_state.settings["classroom"]
    
    col1, col2 = st.columns(2)
    
    with col1:
        school_name = st.text_input("School Name", value=settings["school_name"])
        classroom_name = st.text_input("Classroom Name", value=settings["classroom_name"])
    
    with col2:
        academic_year = st.text_input("Academic Year", value=settings["academic_year"])
        student_count = st.number_input("Student Count", min_value=1, max_value=50, value=settings["student_count"])
    
    assistant_input = ", ".join(settings["assistant_teachers"])
    assistant_teachers_str = st.text_input("Assistant Teachers (comma-separated)", value=assistant_input)
    assistant_teachers = [t.strip() for t in assistant_teachers_str.split(",") if t.strip()]
    
    if st.button("Save Classroom Settings", type="primary"):
        st.session_state.settings["classroom"] = {
            "school_name": school_name,
            "classroom_name": classroom_name,
            "academic_year": academic_year,
            "student_count": student_count,
            "assistant_teachers": assistant_teachers
        }
        st.success("Classroom settings saved successfully!")


def render_notifications_section():
    st.subheader("🔔 Notification Preferences")
    
    settings = st.session_state.settings["notifications"]
    
    st.write("**Email Notifications**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        email_observations = st.checkbox("Observation Updates", value=settings["email_observations"])
        email_reports = st.checkbox("Report Reminders", value=settings["email_reports"])
    
    with col2:
        email_parent = st.checkbox("Parent Communications", value=settings["email_parent_communications"])
        weekly_digest = st.checkbox("Weekly Digest", value=settings["weekly_digest"])
    
    st.markdown("---")
    st.write("**Push Notifications**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        push_activities = st.checkbox("Activity Reminders", value=settings["push_activities"])
    
    with col2:
        push_schedule = st.checkbox("Schedule Changes", value=settings["push_schedule_changes"])
    
    from datetime import datetime, time
    
    stored_time = st.session_state.settings["notifications"].get("reminder_time", "18:00")
    if isinstance(stored_time, str):
        default_time = datetime.strptime(stored_time, "%H:%M:%S").time()
    else:
        default_time = stored_time
    
    reminder_time = st.time_input("Daily Reminder Time", value=default_time)
    
    if st.button("Save Notification Settings", type="primary"):
        st.session_state.settings["notifications"] = {
            "email_observations": email_observations,
            "email_reports": email_reports,
            "email_parent_communications": email_parent,
            "push_activities": push_activities,
            "push_schedule_changes": push_schedule,
            "weekly_digest": weekly_digest,
            "reminder_time": str(reminder_time)
        }
        st.success("Notification settings saved successfully!")


def render_privacy_section():
    st.subheader("🔒 Privacy & Security")
    
    settings = st.session_state.settings["privacy_security"]
    
    st.write("**Security**")
    
    two_factor = st.checkbox("Enable Two-Factor Authentication", value=settings["two_factor_auth"])
    
    timeout_options = [15, 30, 60, 120]
    session_timeout = st.selectbox("Session Timeout (minutes)", timeout_options, index=timeout_options.index(settings["session_timeout"]))
    
    st.markdown("---")
    st.write("**Data & Privacy**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        data_export = st.checkbox("Allow Data Export", value=settings["data_export"])
    
    with col2:
        share_parents = st.checkbox("Share Progress with Parents", value=settings["share_progress_with_parents"])
    
    analytics = st.checkbox("Analytics Tracking", value=settings["analytics_tracking"])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Save Privacy Settings", type="primary"):
            st.session_state.settings["privacy_security"] = {
                "two_factor_auth": two_factor,
                "session_timeout": session_timeout,
                "data_export": data_export,
                "share_progress_with_parents": share_parents,
                "analytics_tracking": analytics
            }
            st.success("Privacy settings saved successfully!")
    
    with col2:
        if st.button("Export My Data", use_container_width=True):
            st.info("Data export feature coming soon!")


def render_appearance_section():
    st.subheader("🎨 Appearance Settings")
    
    settings = st.session_state.settings["appearance"]
    
    theme = st.radio("Theme", ["Light", "Dark", "System"], index=["light", "dark", "system"].index(settings["theme"]) if settings["theme"] in ["light", "dark", "system"] else 0)
    
    accent_colors = ["Purple", "Blue", "Green", "Orange", "Pink", "Red"]
    accent_color = st.selectbox("Accent Color", accent_colors, index=accent_colors.index(settings["accent_color"]) if settings["accent_color"] in accent_colors else 0)
    
    font_sizes = ["Small", "Medium", "Large"]
    font_size = st.selectbox("Font Size", font_sizes, index=font_sizes.index(settings["font_size"]) if settings["font_size"] in font_sizes else 1)
    
    compact_mode = st.checkbox("Compact Mode", value=settings["compact_mode"])
    sidebar_collapsed = st.checkbox("Collapse Sidebar by Default", value=settings["sidebar_collapsed"])
    
    if st.button("Save Appearance Settings", type="primary"):
        st.session_state.settings["appearance"] = {
            "theme": theme.lower(),
            "accent_color": accent_color,
            "font_size": font_size,
            "compact_mode": compact_mode,
            "sidebar_collapsed": sidebar_collapsed
        }
        st.success("Appearance settings saved successfully!")
    
    st.markdown("---")
    st.markdown("**Preview**")
    
    preview_style = "compact" if compact_mode else "normal"
    st.info(f"Theme: {theme} | Accent: {accent_color} | Font: {font_size} | Mode: {preview_style}")


if __name__ == "__main__":
    render()
