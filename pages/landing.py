import streamlit as st

from src.monty.auth import login
from src.monty.session import init_session_state


def render():
    init_session_state()
    
    st.set_page_config(
        page_title="Monty - AI Teacher Assistant",
        page_icon="📚",
        layout="centered"
    )
    
    st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    .gradient-bg {
        background: linear-gradient(135deg, #1e3a8a 0%, #0d9488 100%);
        padding: 60px 20px;
        border-radius: 20px;
        text-align: center;
        color: white;
        margin-bottom: 40px;
    }
    .gradient-title {
        font-size: 48px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .gradient-subtitle {
        font-size: 20px;
        opacity: 0.9;
        margin-bottom: 30px;
    }
    .feature-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
        text-align: center;
    }
    .feature-icon {
        font-size: 40px;
        margin-bottom: 15px;
    }
    .feature-title {
        font-size: 20px;
        font-weight: bold;
        color: #333;
        margin-bottom: 10px;
    }
    .feature-desc {
        color: #666;
        font-size: 14px;
    }
    .login-btn {
        background: white;
        color: #667eea;
        padding: 15px 40px;
        border-radius: 30px;
        font-size: 18px;
        font-weight: bold;
        border: none;
        cursor: pointer;
        transition: transform 0.2s;
    }
    .login-btn:hover {
        transform: scale(1.05);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="gradient-bg">
        <div class="gradient-title">Meet Monty</div>
        <div class="gradient-subtitle">Your AI-powered Montessori Teaching Assistant</div>
        <button class="login-btn" onclick="document.getElementById('login-trigger').click()">
            Get Started
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    if "show_login_modal" not in st.session_state:
        st.session_state.show_login_modal = False
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📋</div>
            <div class="feature-title">Smart Planning</div>
            <div class="feature-desc">AI-generated lesson plans tailored to each student's learning journey</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👁️</div>
            <div class="feature-title">Observation Tracking</div>
            <div class="feature-desc">Record and analyze student observations with intelligent insights</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📊</div>
            <div class="feature-title">Progress Reports</div>
            <div class="feature-desc">Beautiful parent newsletters and student progress reports in seconds</div>
        </div>
        """, unsafe_allow_html=True)
    
    if st.session_state.show_login_modal:
        render_login_modal()
    else:
        if st.button("Sign In", key="login-trigger"):
            st.session_state.show_login_modal = True
            st.rerun()


def render_login_modal():
    st.markdown("""
    <style>
    .modal-overlay {
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
    }
    .modal-content {
        background: white;
        padding: 40px;
        border-radius: 20px;
        width: 90%;
        max-width: 400px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    .modal-title {
        font-size: 24px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 30px;
        color: #333;
    }
    </style>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="modal-content">', unsafe_allow_html=True)
        
        st.markdown('<div class="modal-title">Welcome Back</div>', unsafe_allow_html=True)
        
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Sign In", use_container_width=True):
                if login(username, password):
                    st.rerun()
                else:
                    st.error("Invalid credentials. Try demo/demo")
        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.show_login_modal = False
                st.rerun()
        
        st.markdown("---")
        
        if st.button("👤 Login as Demo User (Sarah Johnson)", use_container_width=True):
            if login("demo", "demo"):
                st.rerun()
        
        st.markdown("*Demo: username: `demo`, password: `demo`*")
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render()
