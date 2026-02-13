import streamlit as st

from src.monty.session import init_session_state


def main():
    init_session_state()
    
    if st.session_state.authenticated:
        from src.monty.pages import dashboard
        dashboard.render()
    else:
        from src.monty.pages import landing
        landing.render()


if __name__ == "__main__":
    main()
