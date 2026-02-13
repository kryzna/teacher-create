import streamlit as st
from src.monty.session import init_session_state, require_auth


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(page_title="Students - Monty", page_icon="👥", layout="wide")
    st.markdown("""<style>[data-testid="stSidebarNav"] {display: none !important;}</style>""", unsafe_allow_html=True)
    
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
    st.title("👥 Students")
    
    tab1, tab2 = st.tabs(["Student List", "Add Student"])
    
    with tab1:
        render_student_filters()
        render_student_grid()
    
    with tab2:
        render_add_student_form()


def render_student_filters():
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_query = st.text_input("🔍 Search by name", placeholder="Enter student name...")
        st.session_state.search_query = search_query
    
    with col2:
        age_filter = st.selectbox("Filter by age", ["All Ages", "3", "4", "5", "6", "7"])
        st.session_state.age_filter = age_filter
    
    with col3:
        interest_filter = st.selectbox("Filter by interest", ["All Interests", "Nature", "Painting", "Building Blocks", "Music", "Reading", "Science", "Sports", "Animals", "Dancing", "Art", "Mathematics", "Puzzles"])
        st.session_state.interest_filter = interest_filter


def get_filtered_students():
    students = st.session_state.students
    
    search_query = st.session_state.get("search_query", "")
    age_filter = st.session_state.get("age_filter", "All Ages")
    interest_filter = st.session_state.get("interest_filter", "All Interests")
    
    if search_query:
        students = [s for s in students if search_query.lower() in s["name"].lower()]
    
    if age_filter != "All Ages":
        students = [s for s in students if s["age"] == int(age_filter)]
    
    if interest_filter != "All Interests":
        students = [s for s in students if interest_filter in s["interests"]]
    
    return students


def render_student_grid():
    students = get_filtered_students()
    
    if not students:
        st.info("No students found matching your criteria.")
        return
    
    st.markdown(f"**{len(students)} student(s) found**")
    
    for i in range(0, len(students), 2):
        col1, col2 = st.columns(2)
        
        with col1:
            render_student_card(students[i])
        
        with col2:
            if i + 1 < len(students):
                render_student_card(students[i + 1])


def render_student_card(student):
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"👤 {student['name']}")
            st.write(f"**Age:** {student['age']} years")
        
        with col2:
            st.write(f"🆔 #{student['id']}")
        
        st.markdown("---")
        
        col_interests, col_allergies = st.columns(2)
        
        with col_interests:
            st.write("**Interests:**")
            for interest in student["interests"]:
                st.write(f"🏷️ {interest}")
        
        with col_allergies:
            st.write("**Allergies:**")
            if student["allergies"]:
                for allergy in student["allergies"]:
                    st.write(f"⚠️ {allergy}")
            else:
                st.write("None")
        
        st.markdown("---")
        
        with st.expander("Parent Contact"):
            st.write(f"**Name:** {student['parent_name']}")
            st.write(f"**Email:** {student['parent_email']}")
        
        col_edit, col_delete = st.columns(2)
        
        with col_edit:
            if st.button("Edit", key=f"edit_{student['id']}", use_container_width=True):
                st.session_state.edit_student = student
                st.rerun()
        
        with col_delete:
            if st.button("Delete", key=f"delete_{student['id']}", use_container_width=True):
                st.session_state.students = [s for s in st.session_state.students if s["id"] != student["id"]]
                st.success(f"Deleted {student['name']}")
                st.rerun()


def render_add_student_form():
    st.subheader("➕ Add New Student")
    
    if "edit_student" in st.session_state:
        student = st.session_state.edit_student
        st.info(f"Editing {student['name']}")
        
        name = st.text_input("Student Name", value=student["name"])
        age = st.number_input("Age", min_value=1, max_value=12, value=student["age"])
        
        interests_input = ", ".join(student["interests"])
        interests_str = st.text_input("Interests (comma-separated)", value=interests_input)
        interests = [i.strip() for i in interests_str.split(",") if i.strip()]
        
        allergies_input = ", ".join(student["allergies"])
        allergies_str = st.text_input("Allergies (comma-separated)", value=allergies_input)
        allergies = [a.strip() for a in allergies_str.split(",") if a.strip()]
        
        parent_name = st.text_input("Parent Name", value=student["parent_name"])
        parent_email = st.text_input("Parent Email", value=student["parent_email"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Update Student", use_container_width=True):
                for s in st.session_state.students:
                    if s["id"] == student["id"]:
                        s["name"] = name
                        s["age"] = age
                        s["interests"] = interests
                        s["allergies"] = allergies
                        s["parent_name"] = parent_name
                        s["parent_email"] = parent_email
                        break
                del st.session_state.edit_student
                st.success("Student updated successfully!")
                st.rerun()
        
        with col2:
            if st.button("Cancel Edit", use_container_width=True):
                del st.session_state.edit_student
                st.rerun()
    
    else:
        name = st.text_input("Student Name", placeholder="Enter student name...")
        age = st.number_input("Age", min_value=1, max_value=12, value=3)
        
        interests_str = st.text_input("Interests (comma-separated)", placeholder="e.g., Nature, Painting, Music")
        interests = [i.strip() for i in interests_str.split(",") if i.strip()]
        
        allergies_str = st.text_input("Allergies (comma-separated)", placeholder="e.g., Peanuts, Milk")
        allergies = [a.strip() for a in allergies_str.split(",") if a.strip()]
        
        parent_name = st.text_input("Parent Name", placeholder="Enter parent name...")
        parent_email = st.text_input("Parent Email", placeholder="Enter parent email...")
        
        if st.button("Add Student", use_container_width=True):
            if not name:
                st.error("Student name is required!")
            elif not parent_name:
                st.error("Parent name is required!")
            else:
                new_id = max([s["id"] for s in st.session_state.students], default=0) + 1
                new_student = {
                    "id": new_id,
                    "name": name,
                    "age": age,
                    "interests": interests,
                    "allergies": allergies,
                    "parent_name": parent_name,
                    "parent_email": parent_email
                }
                st.session_state.students.append(new_student)
                st.success(f"Added {name} successfully!")
                st.rerun()


if __name__ == "__main__":
    render()
