# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Monty is a Streamlit-based AI teacher assistant for Montessori educators. It helps manage classrooms, track student progress, manage materials, and generate parent communications. Currently uses in-memory session state with demo data (no database persistence).

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py

# Run on a specific port
streamlit run app.py --server.port 8501
```

There are no tests, linting, or CI/CD configured.

## Architecture

### Entry Point & Routing

`app.py` initializes session state, then routes to the landing page (unauthenticated) or dashboard (authenticated). Authentication is demo-only: username `demo`, password `demo`.

### Key Modules

- `src/monty/session.py` — Session state initialization with all demo data (students, schedule, observations, materials). Contains `login_user()`, `logout_user()`, `require_auth()`.
- `src/monty/auth.py` — Demo authentication logic and `DEMO_USER` constant.
- `src/monty/pages/` — Primary page implementations imported by `app.py` and the navigation system.
- `pages/` — Streamlit multipage app directory. These files also exist as standalone entry points but the app routes through `src/monty/pages/`.

### Page Pattern

Every page follows this structure:
1. Call `init_session_state()` and `require_auth()`
2. Call `st.set_page_config()` as the **first** Streamlit command (required by Streamlit)
3. Inject CSS to hide native Streamlit nav: `[data-testid="stSidebarNav"] {display: none !important;}`
4. Render a custom sidebar with navigation links and logout
5. Render main content

The sidebar is duplicated in every page file (~30 lines each).

### State Management

All application state lives in `st.session_state` (Streamlit's built-in session dictionary). Data resets on browser refresh. Key state keys: `authenticated`, `user`, `current_page`, `students`, `schedule`, `observations`, `materials`, `daily_entries`, `show_login_modal`.

### AI Integration

The "Ask Monty" chat in the dashboard returns hardcoded keyword-matched responses. OpenAI is listed as a dependency but not actively called. Newsletter generation in daily tracking is template-based.

## Streamlit Gotchas

- `st.set_page_config()` must be the first Streamlit call in any page render — placing it after other `st.*` calls causes errors.
- `st.rerun()` can cause infinite loops if state isn't properly guarded.
- `st.page_link()` paths must be relative to the project root.
