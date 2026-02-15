import streamlit as st

from src.monty.session import init_session_state, require_auth


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(page_title="Reports - Monty", page_icon="📊", layout="wide")
    st.markdown("""<style>[data-testid="stSidebarNav"] {display: none !important;}</style>""", unsafe_allow_html=True)
    
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
    st.title("📊 Reports")
    
    col_list, col_preview = st.columns([1, 2])
    
    with col_list:
        render_student_list()
    
    with col_preview:
        render_report_preview()


def render_student_list():
    st.subheader("👥 Students")
    
    search = st.text_input("🔍 Search students", placeholder="Search by name...")
    
    if search:
        students = [s for s in st.session_state.students if search.lower() in s["name"].lower()]
    else:
        students = st.session_state.students
    
    if not students:
        st.info("No students found.")
        return
    
    for student in students:
        is_selected = st.session_state.get("selected_student_id") == student["id"]
        button_label = f"👤 {student['name']}"
        
        if st.button(button_label, key=f"select_{student['id']}", use_container_width=True):
            st.session_state.selected_student_id = student["id"]
            st.rerun()
        
        if is_selected:
            st.markdown("✅ Selected")
        else:
            st.markdown("")


def render_report_preview():
    st.subheader("📋 Report Preview")
    
    if "selected_student_id" not in st.session_state or not st.session_state.selected_student_id:
        st.info("Select a student from the list to view their report.")
        return
    
    student = next((s for s in st.session_state.students if s["id"] == st.session_state.selected_student_id), None)
    
    if not student:
        st.error("Student not found.")
        return
    
    student_observations = [o for o in st.session_state.observations if o["student"] == student["name"]]
    
    with st.container(border=True):
        st.markdown(f"## 📄 Progress Report")
        st.markdown(f"**Student:** {student['name']}")
        st.markdown(f"**Age:** {student['age']} years")
        st.markdown(f"**Parent:** {student['parent_name']}")
        
        st.markdown("---")
        
        st.markdown("### 🎯 Interests")
        if student["interests"]:
            for interest in student["interests"]:
                st.write(f"🏷️ {interest}")
        else:
            st.write("No interests recorded.")
        
        st.markdown("---")
        
        st.markdown("### ⚠️ Allergies")
        if student["allergies"]:
            for allergy in student["allergies"]:
                st.write(f"⚠️ {allergy}")
        else:
            st.write("No allergies recorded.")
        
        st.markdown("---")
        
        st.markdown("### 👁️ Observations")
        if student_observations:
            for obs in student_observations:
                with st.expander(f"{obs['date']} - {obs['area']}"):
                    st.write(f"**Area:** {obs['area']}")
                    st.write(f"**Skills:** {', '.join(obs.get('skills', []))}")
                    st.write(f"**Notes:** {obs['notes']}")
        else:
            st.write("No observations recorded yet.")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Download Report", use_container_width=True):
                report_content = generate_report(student, student_observations)
                st.download_button(
                    label="📥 Download PDF",
                    data=report_content,
                    file_name=f"report_{student['name'].replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        
        with col2:
            if st.button("Print Report", use_container_width=True):
                st.info("Print functionality coming soon!")


def generate_report(student, observations):
    content = f"""
PROGRESS REPORT
===============

Student: {student['name']}
Age: {student['age']} years
Parent: {student['parent_name']}
Email: {student['parent_email']}

INTERESTS
---------
"""
    for interest in student["interests"]:
        content += f"- {interest}\n"
    
    content += "\nALLERGIES\n---------\n"
    if student["allergies"]:
        for allergy in student["allergies"]:
            content += f"- {allergy}\n"
    else:
        content += "None reported\n"
    
    content += "\nOBSERVATIONS\n------------\n"
    for obs in observations:
        content += f"\nDate: {obs['date']}\n"
        content += f"Area: {obs['area']}\n"
        content += f"Skills: {', '.join(obs.get('skills', []))}\n"
        content += f"Notes: {obs['notes']}\n"
    
    return content


if __name__ == "__main__":
    render()
