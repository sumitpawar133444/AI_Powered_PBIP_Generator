import streamlit as st
import uuid

def init_session_state():
    if "style_spec" not in st.session_state:
        st.session_state.style_spec = {"primary_color": "#118DFF", "secondary_color": "#12239E",
        "chart_theme": "streamlit"}
    if "chats" not in st.session_state:
        st.session_state.chats = {}
    if "current_chat_id" not in st.session_state:
        create_new_chat()

def create_new_chat():
    new_id = str(uuid.uuid4())[:8]
    st.session_state.chats[new_id] = {
        "name": f"New Dashboard {len(st.session_state.chats) + 1}",
        "messages": [{"role": "assistant", "content": "Hi! What kind of dashboard are we building today? Let's start with the key metrics you want to see (e.g., 'A Sales dashboard with cards for Revenue and Margin, and a bar chart for Sales by Category')."}],
        "frontend_spec": {"title": "New Dashboard", "visuals": []},
        "backend_spec": {"tables": [], "measures": [], "relationships": []}
    }
    st.session_state.current_chat_id = new_id