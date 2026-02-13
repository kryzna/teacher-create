import streamlit as st

from src.monty.session import init_session_state, require_auth


def render():
    init_session_state()
    require_auth()
    
    st.set_page_config(page_title="Materials - Monty", page_icon="📦", layout="wide")
    
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
    st.title("📦 Materials Library")
    
    tab1, tab2, tab3 = st.tabs(["Browse Materials", "Add Material", "Usage Statistics"])
    
    with tab1:
        render_browse_materials()
    
    with tab2:
        render_add_material_form()
    
    with tab3:
        render_usage_statistics()


def render_browse_materials():
    categories = ["All", "Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science"]
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_category = st.selectbox("Filter by Category", categories, index=0)
        st.session_state.material_category = selected_category
    
    with col2:
        search = st.text_input("Search", placeholder="Search...")
        st.session_state.material_search = search
    
    materials = get_filtered_materials()
    
    if not materials:
        st.info("No materials found matching your criteria.")
        return
    
    st.markdown(f"**{len(materials)} material(s) found**")
    
    cols = st.columns(3)
    
    for i, material in enumerate(materials):
        with cols[i % 3]:
            render_material_card(material)


def get_filtered_materials():
    materials = st.session_state.materials
    
    category = st.session_state.get("material_category", "All")
    search = st.session_state.get("material_search", "")
    
    if category != "All":
        materials = [m for m in materials if m["category"] == category]
    
    if search:
        materials = [m for m in materials if search.lower() in m["name"].lower() or search.lower() in m["description"].lower()]
    
    return materials


def render_material_card(material):
    with st.container(border=True):
        st.subheader(f"📦 {material['name']}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write(f"**Category:** {material['category']}")
            st.write(f"**Age Range:** {material['age_range']}")
        
        with col2:
            status = "✅ In Stock" if material["in_stock"] else "❌ Out of Stock"
            st.write(status)
            st.write(f"**Used:** {material.get('times_used', 0)} times")
        
        st.markdown("---")
        
        st.write(material['description'][:100] + "..." if len(material['description']) > 100 else material['description'])
        
        col_view, col_use = st.columns(2)
        
        with col_view:
            if st.button("View", key=f"view_{material['id']}", use_container_width=True):
                st.session_state.view_material = material
                st.rerun()
        
        with col_use:
            if st.button("Use", key=f"use_{material['id']}", use_container_width=True):
                for m in st.session_state.materials:
                    if m["id"] == material["id"]:
                        m["times_used"] = m.get("times_used", 0) + 1
                        break
                st.success(f"Recorded use of {material['name']}")
                st.rerun()
    
    if "view_material" in st.session_state and st.session_state.view_material["id"] == material["id"]:
        render_view_dialog(st.session_state.view_material)


def render_view_dialog(material):
    with st.expander(f"📦 {material['name']} - Details", expanded=True):
        st.markdown(f"### {material['name']}")
        st.write(f"**Category:** {material['category']}")
        st.write(f"**Age Range:** {material['age_range']}")
        st.write(f"**Status:** {'In Stock' if material['in_stock'] else 'Out of Stock'}")
        st.write(f"**Times Used:** {material.get('times_used', 0)}")
        
        st.markdown("---")
        
        st.write("**Description:**")
        st.write(material['description'])
        
        if st.button("Close", key=f"close_{material['id']}"):
            del st.session_state.view_material
            st.rerun()


def render_add_material_form():
    st.subheader("➕ Add New Material")
    
    if "edit_material" in st.session_state:
        material = st.session_state.edit_material
        st.info(f"Editing {material['name']}")
        
        name = st.text_input("Material Name", value=material["name"])
        category = st.selectbox("Category", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science"],
                                index=["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science"].index(material["category"]))
        age_range = st.text_input("Age Range", value=material["age_range"])
        description = st.text_area("Description", value=material["description"])
        in_stock = st.checkbox("In Stock", value=material["in_stock"])
        
        col_save, col_cancel = st.columns(2)
        
        with col_save:
            if st.button("Update Material", use_container_width=True):
                for m in st.session_state.materials:
                    if m["id"] == material["id"]:
                        m["name"] = name
                        m["category"] = category
                        m["age_range"] = age_range
                        m["description"] = description
                        m["in_stock"] = in_stock
                        break
                del st.session_state.edit_material
                st.success("Material updated successfully!")
                st.rerun()
        
        with col_cancel:
            if st.button("Cancel Edit", use_container_width=True):
                del st.session_state.edit_material
                st.rerun()
    
    else:
        name = st.text_input("Material Name", placeholder="e.g., Pink Tower")
        category = st.selectbox("Category", ["Practical Life", "Sensorial", "Language", "Mathematics", "Art", "Science"])
        age_range = st.text_input("Age Range", placeholder="e.g., 3-6")
        description = st.text_area("Description", placeholder="Describe the material and its purpose...")
        in_stock = st.checkbox("In Stock", value=True)
        
        if st.button("Add Material", use_container_width=True):
            if not name:
                st.error("Material name is required!")
            elif not description:
                st.error("Description is required!")
            else:
                new_id = max([m["id"] for m in st.session_state.materials], default=0) + 1
                new_material = {
                    "id": new_id,
                    "name": name,
                    "category": category,
                    "age_range": age_range,
                    "description": description,
                    "in_stock": in_stock,
                    "times_used": 0
                }
                st.session_state.materials.append(new_material)
                st.success(f"Added {name} successfully!")
                st.rerun()


def render_usage_statistics():
    st.subheader("📊 Material Usage Statistics")
    
    materials = st.session_state.materials
    
    if not materials:
        st.info("No materials available.")
        return
    
    total_uses = sum(m.get("times_used", 0) for m in materials)
    in_stock_count = sum(1 for m in materials if m["in_stock"])
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Materials", len(materials))
    with col2:
        st.metric("Total Uses", total_uses)
    with col3:
        st.metric("In Stock", in_stock_count)
    
    st.markdown("---")
    
    st.markdown("### Usage by Category")
    categories = {}
    for m in materials:
        cat = m["category"]
        if cat not in categories:
            categories[cat] = {"count": 0, "uses": 0}
        categories[cat]["count"] += 1
        categories[cat]["uses"] += m.get("times_used", 0)
    
    for cat, data in categories.items():
        with st.expander(f"{cat}"):
            st.write(f"**Materials:** {data['count']}")
            st.write(f"**Total Uses:** {data['uses']}")
    
    st.markdown("---")
    
    st.markdown("### Most Used Materials")
    sorted_materials = sorted(materials, key=lambda x: x.get("times_used", 0), reverse=True)
    
    for m in sorted_materials[:5]:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{m['name']}** ({m['category']})")
            
            with col2:
                st.write(f"Used {m.get('times_used', 0)} times")


if __name__ == "__main__":
    render()
