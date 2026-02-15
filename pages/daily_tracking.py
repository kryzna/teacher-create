import streamlit as st
from datetime import datetime, timedelta
import time
from src.monty.session import init_session_state, require_auth, reload_from_db, flash, show_flash
from src.monty.crud import create_daily_entry, update_daily_entry


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(page_title="Daily Tracking - Monty", page_icon="📝", layout="wide")
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
    st.title("📝 Daily Tracking")
    
    tab1, tab2, tab3 = st.tabs(["➕ Add Entry", "📅 Week View", "📰 Newsletter"])
    
    with tab1:
        render_add_entry()
    
    with tab2:
        render_week_view()
    
    with tab3:
        render_newsletter()


def render_add_entry():
    st.subheader("➕ Add Daily Entry")
    
    if "edit_entry" in st.session_state:
        entry = st.session_state.edit_entry
        st.info(f"Editing entry for {entry['student']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            student = st.selectbox("Student", [s["name"] for s in st.session_state.students],
                                 index=[s["name"] for s in st.session_state.students].index(entry["student"]))
            date = st.date_input("Date", datetime.strptime(entry["date"], "%Y-%m-%d").date())
            subject = st.selectbox("Subject", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music", "Outdoor"],
                                 index=["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music", "Outdoor"].index(entry["subject"]))
        
        with col2:
            activities_str = ", ".join(entry.get("activities", []))
            activities_input = st.text_input("Activities (comma-separated)", value=activities_str)
            activities = [a.strip() for a in activities_input.split(",") if a.strip()]
            
            skill_level = st.selectbox("Skill Level", ["Emerging", "Developing", "Proficient", "Advanced"],
                                      index=["Emerging", "Developing", "Proficient", "Advanced"].index(entry["skill_level"]))
        
        notes = st.text_area("Notes", value=entry["notes"], height=150)
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.button("Update Entry", use_container_width=True):
                user_id = st.session_state.user["db_id"]
                update_daily_entry(entry["id"], user_id, {
                    "student": student, "date": date.strftime("%Y-%m-%d"),
                    "subject": subject, "activities": activities,
                    "skill_level": skill_level, "notes": notes,
                })
                del st.session_state.edit_entry
                reload_from_db()
                flash("Entry updated successfully!")
                st.rerun()
        
        with col_cancel:
            if st.button("Cancel Edit", use_container_width=True):
                del st.session_state.edit_entry
                st.rerun()
    
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            student = st.selectbox("Student", [s["name"] for s in st.session_state.students])
            date = st.date_input("Date", datetime.now().date())
            subject = st.selectbox("Subject", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science", "Music", "Outdoor"])
        
        with col2:
            activities_input = st.text_input("Activities (comma-separated)", placeholder="e.g., Pouring, Sweeping, Cutting")
            activities = [a.strip() for a in activities_input.split(",") if a.strip()]
            
            skill_level = st.selectbox("Skill Level", ["Emerging", "Developing", "Proficient", "Advanced"])
        
        notes = st.text_area("Notes", placeholder="Document what the student worked on today...", height=150)
        
        date_str = date.strftime("%Y-%m-%d") if date else None
        existing_entry = any(
            e["student"] == student and e["date"] == date_str and e["subject"] == subject
            for e in st.session_state.daily_entries
        )
        
        if existing_entry:
            st.warning(f"Entry already exists for {student} on {date_str} with subject {subject}")
        
        if st.button("Save Entry", use_container_width=True, disabled=existing_entry):
            if not student:
                st.error("Please select a student!")
            elif not activities:
                st.error("Please add at least one activity!")
            else:
                user_id = st.session_state.user["db_id"]
                create_daily_entry(user_id, {
                    "student": student, "date": date_str,
                    "subject": subject, "activities": activities,
                    "skill_level": skill_level, "notes": notes,
                })
                reload_from_db()
                flash(f"Entry for {student} saved successfully!")
                st.rerun()


def render_week_view():
    st.subheader("📅 Week View")
    
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        week_offset = st.number_input("Week offset", min_value=-4, max_value=0, value=0, format="%d")
    
    with col2:
        if st.button("Go to Today", use_container_width=True):
            st.rerun()
    
    selected_week_start = start_of_week + timedelta(days=week_offset * 7)
    week_dates = [selected_week_start + timedelta(days=i) for i in range(7)]
    
    st.markdown(f"**Week of {week_dates[0].strftime('%B %d, %Y')} - {week_dates[-1].strftime('%B %d, %Y')}**")
    
    week_strs = [d.strftime("%Y-%m-%d") for d in week_dates]
    
    student_filter = st.selectbox("Filter by student", ["All Students"] + [s["name"] for s in st.session_state.students])
    
    if student_filter == "All Students":
        entries = [e for e in st.session_state.daily_entries if e["date"] in week_strs]
    else:
        entries = [e for e in st.session_state.daily_entries if e["date"] in week_strs and e["student"] == student_filter]
    
    if not entries:
        st.info("No entries found for this week.")
        return
    
    st.markdown(f"**{len(entries)} entry(s) found**")
    
    if student_filter == "All Students":
        student_entries = {}
        for entry in entries:
            if entry["student"] not in student_entries:
                student_entries[entry["student"]] = []
            student_entries[entry["student"]].append(entry)
        
        for student_name, student_entries_list in sorted(student_entries.items()):
            with st.container(border=True):
                st.subheader(f"👤 {student_name}")
                
                for day_idx, day_date in enumerate(week_dates):
                    day_str = day_date.strftime("%Y-%m-%d")
                    day_entries = [e for e in student_entries_list if e["date"] == day_str]
                    
                    if day_entries:
                        day_name = day_date.strftime("%A")
                        st.markdown(f"**{day_name} ({day_date.strftime('%b %d')}):**")
                        
                        for entry in day_entries:
                            with st.container():
                                col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                                
                                with col1:
                                    st.write(f"📚 {entry['subject']}")
                                with col2:
                                    st.write(f"🎯 {', '.join(entry['activities'][:2])}")
                                with col3:
                                    skill_emoji = {"Emerging": "🌱", "Developing": "🌿", "Proficient": "🌳", "Advanced": "⭐"}
                                    st.write(f"{skill_emoji.get(entry['skill_level'], '')} {entry['skill_level']}")
                                with col4:
                                    if st.button("Edit", key=f"edit_{entry['id']}", use_container_width=True):
                                        st.session_state.edit_entry = entry
                                        st.rerun()
                                
                                if entry["notes"]:
                                    st.write(f"📝 {entry['notes']}")
                                st.markdown("---")
    else:
        for day_idx, day_date in enumerate(week_dates):
            day_str = day_date.strftime("%Y-%m-%d")
            day_entries = [e for e in entries if e["date"] == day_str]
            
            if day_entries:
                day_name = day_date.strftime("%A")
                st.markdown(f"**{day_name} ({day_date.strftime('%b %d')}):**")
                
                for entry in day_entries:
                    with st.container():
                        col1, col2, col3, col4 = st.columns([2, 2, 2, 1])
                        
                        with col1:
                            st.write(f"📚 {entry['subject']}")
                        with col2:
                            st.write(f"🎯 {', '.join(entry['activities'][:2])}")
                        with col3:
                            skill_emoji = {"Emerging": "🌱", "Developing": "🌿", "Proficient": "🌳", "Advanced": "⭐"}
                            st.write(f"{skill_emoji.get(entry['skill_level'], '')} {entry['skill_level']}")
                        with col4:
                            if st.button("Edit", key=f"edit_{entry['id']}", use_container_width=True):
                                st.session_state.edit_entry = entry
                                st.rerun()
                        
                        if entry["notes"]:
                            st.write(f"📝 {entry['notes']}")
                        st.markdown("---")


def render_newsletter():
    st.subheader("📰 Newsletter")
    
    col1, col2 = st.columns(2)
    
    with col1:
        newsletter_type = st.radio("Newsletter Type", ["Individual Student", "Whole Class"])
    
    with col2:
        week_offset = st.number_input("Week offset for newsletter", min_value=-4, max_value=0, value=0, format="%d")
    
    today = datetime.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    selected_week_start = start_of_week + timedelta(days=week_offset * 7)
    week_dates = [selected_week_start + timedelta(days=i) for i in range(7)]
    week_strs = [d.strftime("%Y-%m-%d") for d in week_dates]
    
    if newsletter_type == "Individual Student":
        selected_student = st.selectbox("Select Student", [s["name"] for s in st.session_state.students])
        
        student_obj = next((s for s in st.session_state.students if s["name"] == selected_student), None)
        
        if student_obj:
            st.write(f"**Parent:** {student_obj['parent_name']} ({student_obj['parent_email']})")
        
        entries = [e for e in st.session_state.daily_entries if e["date"] in week_strs and e["student"] == selected_student]
        
        if not entries:
            st.info(f"No entries found for {selected_student} this week.")
            return
        
        newsletter_content = generate_individual_newsletter(selected_student, student_obj, entries, week_dates)
        
        st.text_area("Newsletter Preview", value=newsletter_content, height=300)
        
        st.download_button("📥 Download Newsletter (Markdown)", newsletter_content, 
                          file_name=f"newsletter_{selected_student.lower().replace(' ', '_')}_{week_dates[0].strftime('%Y%m%d')}.md",
                          mime="text/markdown")
    
    else:
        st.write("**Whole Class Newsletter**")
        
        all_entries = [e for e in st.session_state.daily_entries if e["date"] in week_strs]
        
        if not all_entries:
            st.info("No entries found this week.")
            return
        
        newsletter_content = generate_class_newsletter(all_entries, week_dates, st.session_state.students)
        
        st.text_area("Newsletter Preview", value=newsletter_content, height=300)
        
        st.download_button("📥 Download Class Newsletter (Markdown)", newsletter_content,
                          file_name=f"class_newsletter_{week_dates[0].strftime('%Y%m%d')}.md",
                          mime="text/markdown")


def generate_individual_newsletter(student_name, student_obj, entries, week_dates):
    content = f"# Weekly Update for {student_name}\n\n"
    content += f"**Week of {week_dates[0].strftime('%B %d, %Y')} - {week_dates[-1].strftime('%B %d, %Y')}**\n\n"
    
    if student_obj:
        content += f"**Parent:** {student_obj['parent_name']}\n\n"
    
    content += "---\n\n"
    content += "## This Week's Activities\n\n"
    
    subject_entries = {}
    for entry in entries:
        if entry["subject"] not in subject_entries:
            subject_entries[entry["subject"]] = []
        subject_entries[entry["subject"]].append(entry)
    
    for subject, subject_entries_list in sorted(subject_entries.items()):
        content += f"### {subject}\n"
        for entry in subject_entries_list:
            date_obj = datetime.strptime(entry["date"], "%Y-%m-%d")
            content += f"- **{date_obj.strftime('%A, %b %d')}**: {', '.join(entry['activities'])} ({entry['skill_level']})\n"
            if entry["notes"]:
                content += f"  - {entry['notes']}\n"
        content += "\n"
    
    content += "---\n\n"
    content += "## Skills Development\n\n"
    
    skill_counts = {}
    for entry in entries:
        skill_level = entry["skill_level"]
        if skill_level not in skill_counts:
            skill_counts[skill_level] = 0
        skill_counts[skill_level] += 1
    
    for skill, count in sorted(skill_counts.items()):
        content += f"- {skill}: {count} sessions\n"
    
    content += "\n---\n\n"
    content += "*Thank you for being part of our Montessori community!*\n"
    
    return content


def generate_class_newsletter(entries, week_dates, students):
    content = f"# Weekly Class Update\n\n"
    content += f"**Week of {week_dates[0].strftime('%B %d, %Y')} - {week_dates[-1].strftime('%B %d, %Y')}**\n\n"
    
    content += "---\n\n"
    content += "## Class Highlights\n\n"
    
    student_entries = {}
    for entry in entries:
        if entry["student"] not in student_entries:
            student_entries[entry["student"]] = []
        student_entries[entry["student"]].append(entry)
    
    for student_name, student_entries_list in sorted(student_entries.items()):
        content += f"### {student_name}\n"
        subjects = set(e["subject"] for e in student_entries_list)
        content += f"- Explored: {', '.join(sorted(subjects))}\n"
        
        activities_flat = []
        for e in student_entries_list:
            activities_flat.extend(e["activities"])
        unique_activities = list(set(activities_flat))[:5]
        content += f"- Highlights: {', '.join(unique_activities)}\n"
        content += "\n"
    
    content += "---\n\n"
    content += "## Subject Overview\n\n"
    
    subject_counts = {}
    for entry in entries:
        if entry["subject"] not in subject_counts:
            subject_counts[entry["subject"]] = 0
        subject_counts[entry["subject"]] += 1
    
    for subject, count in sorted(subject_counts.items(), key=lambda x: -x[1]):
        content += f"- {subject}: {count} sessions\n"
    
    content += "\n---\n\n"
    content += f"**Total Entries This Week:** {len(entries)}\n\n"
    content += "---\n\n"
    content += "*Thank you for being part of our Montessori community!*\n"
    
    return content


render()
