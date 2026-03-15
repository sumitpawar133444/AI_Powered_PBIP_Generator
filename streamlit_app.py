import json
import os
from pathlib import Path

import streamlit as st

from Core.architect import update_project_spec
from Backend.compiler import build_pbip_semantic_model, bundle_pbip_to_zip
from Frontend.compiler import compile_to_pbip
from Config.styles import inject_custom_css
from Config.state import init_session_state
from Modules.preview_engine import render_preview_content
from Utils.file_io import save_specs_to_input_folder

# 1. Config & Theme
st.set_page_config(page_title="AI Power BI Architect", layout="wide", initial_sidebar_state="collapsed")
inject_custom_css()
init_session_state()


# Initialize Full Screen State
if "full_screen" not in st.session_state:
    st.session_state.full_screen = False

# ---- HELPER: GET ACTIVE CHAT --------------------------------------------------


def get_active_chat():
    active_id = st.session_state.current_chat_id
    return active_id, st.session_state.chats[active_id]

# ---- SYNC DATA BEFORE WIDGETS ARE DRAWN ---------------------------------------

active_id, active_chat = get_active_chat()

front_key = f"front_{active_id}"
back_key = f"back_{active_id}"

if st.session_state.get("needs_sync"):
    st.session_state[front_key] = json.dumps(active_chat["frontend_spec"], indent=2)
    st.session_state[back_key] = json.dumps(active_chat["backend_spec"], indent=2)
    st.session_state.needs_sync = False

# --- SIDEBAR: CHAT HISTORY & JSON EDITOR ---
with st.sidebar:
    st.title("🚀 Power BI AI")

    if st.button("➕ New Chat", use_container_width=True, type="primary"):
        create_new_chat()
        st.rerun()

    st.divider()
    st.subheader("Recent Chats")
    for chat_id, chat_data in st.session_state.chats.items():
        # Highlight active chat
        btn_type = "secondary" if chat_id != st.session_state.current_chat_id else "primary"
        if st.button(chat_data["name"], key=f"btn_{chat_id}", use_container_width=True):
            st.session_state.current_chat_id = chat_id
            st.rerun()

    st.divider()
    st.header("🎨 Theme & Branding")
    # Interactive style controls
    st.session_state.style_spec["primary_color"] = st.color_picker("Primary Brand Color", st.session_state.style_spec["primary_color"])
    st.session_state.style_spec["secondary_color"] = st.color_picker("Secondary Accent", st.session_state.style_spec["secondary_color"])

    # NEW: Reset Button
    if st.button("🔄 Reset to Default Colors", use_container_width=True):
        st.session_state.style_spec["primary_color"] = "#118DFF"  # Standard PBI Blue
        st.session_state.style_spec["secondary_color"] = "#12239E" # Dark Blue
        st.rerun()

    st.divider()
    st.header("🧠 Project Memory (JSON)")
    st.caption("The bot updates this automatically. You can also edit it manually before building.")

    # FIX: Use the active_chat data instead of st.session_state.frontend_spec
    active_id = st.session_state.current_chat_id
    active_chat = st.session_state.chats[active_id]

    # Define keys for the widgets
    front_key = f"front_{active_id}"
    back_key = f"back_{active_id}"

    # Initialize the widget memory if it doesn't exist
    if front_key not in st.session_state:
        st.session_state[front_key] = json.dumps(active_chat["frontend_spec"], indent=2)
    if back_key not in st.session_state:
        st.session_state[back_key] = json.dumps(active_chat["backend_spec"], indent=2)

    st.subheader("Frontend Configuration")
    front_raw = st.text_area("Frontend JSON", height=180, key=front_key)

    st.subheader("Backend Configuration")
    back_raw = st.text_area("Backend JSON", height=180, key=back_key)

    try:
        active_chat["frontend_spec"] = json.loads(front_raw)
        active_chat["backend_spec"] = json.loads(back_raw)

        # Save every time a manual change is detected in the sidebar
        save_specs_to_input_folder(
            active_chat["name"],
            active_chat["frontend_spec"],
            active_chat["backend_spec"]
        )

    except json.JSONDecodeError:
        st.error("Syntax error in JSON editing.")

# --- MAIN UI LAYOUT ---
active_id = st.session_state.current_chat_id
active_chat = st.session_state.chats[active_id]

# Toggle Logic for Full Screen
if st.session_state.full_screen:
    col_btn, col_select = st.columns([1, 4])
    with col_btn:
        if st.button("⬅️ Exit Full Screen"):
            st.session_state.full_screen = False
            st.rerun()

    # Extract pages to render the selector in full screen
    frontend = active_chat.get("frontend_spec", {})
    pages = frontend.get("pages", [])
    selected_page_idx = 0

    if pages:
        page_names = [p.get("displayName", p.get("name", f"Page {i+1}")) for i, p in enumerate(pages)]
        with col_select:
            selected_page_name = st.selectbox(
                "Select Page Preview:",
                page_names,
                key=f"page_selector_{active_id}_fullscreen"
            )
        selected_page_idx = page_names.index(selected_page_name)

    render_preview_content(active_chat, selected_page_idx=selected_page_idx, is_full=True, preview_key="fullscreen_preview")
else:
    col_chat, col_preview = st.columns([1, 1.4])

    with col_chat:
        st.title("💬 Requirement Architect")

        chat_container = st.container(height=500)
        with chat_container:
            for m in active_chat["messages"]:
                with st.chat_message(m["role"]):
                    st.markdown(m["content"])
            if not active_chat["messages"]:
                st.chat_message("assistant").write("Hello! I'm your BI Architect. You can upload a Qlik/Tableau JSON, a BRD, or record your requirements.")

        input_wrapper = st.container()
        with input_wrapper:
            st.markdown('<div class="unified-chat-input">', unsafe_allow_html=True)

            audio_payload = st.audio_input("Mic", label_visibility="collapsed", key="voice_input")
            chat_payload = st.chat_input(
                "Describe requirements or attach files...",
                accept_file=True,
                file_type=["csv","json","pdf","txt","png","jpg"],
                key="chat_input",
            )
            st.markdown("</div>", unsafe_allow_html=True)

        if chat_payload or audio_payload:
            user_text = ""
            files = []

            # Process Text/Files
            if chat_payload:
                user_text = chat_payload.text
                files = getattr(chat_payload, "files", [])
                if user_text:
                    active_chat["messages"].append({"role": "user", "content": user_text})
                    chat_container.chat_message("user").write(user_text)
                for f in files:
                    st.toast(f"📎 Attached: {f.name}")

            # Process Audio
            if audio_payload:
                if not user_text:
                    active_chat["messages"].append({"role": "user", "content": "🎤 *Voice Requirement Received*"})
                    chat_container.chat_message("user").write("🎤 *Voice Requirement Received*")
                st.toast("Recording processed!")

            # C. The "Gemini Thinking" Animation
            with st.spinner("Gemini is architecting your BI solution..."):
                # Construct the final prompt (Text + Audio reference)
                final_prompt = user_text if user_text else "Please process the attached voice requirement."

                new_data = update_project_spec(
                    final_prompt,
                    active_chat["frontend_spec"],
                    active_chat["backend_spec"],
                    files,
                    audio_payload
                )

                if new_data:
                    # Update Specs
                    active_chat["frontend_spec"] = new_data.get("frontend_spec") or {"title": "New Dashboard", "visuals": []}
                    active_chat["backend_spec"] = new_data.get("backend_spec") or {"tables": [], "relationships": []}

                    # Sync Project Name
                    current_name = active_chat["frontend_spec"].get("title", "New Project")
                    active_chat["name"] = current_name[:25] # Keep it short for UI

                    # Save & Set Sync Flag
                    save_specs_to_input_folder(
                        active_chat["name"],
                        active_chat["frontend_spec"],
                        active_chat["backend_spec"]
                    )
                    st.session_state.needs_sync = True
                    bot_reply = new_data.get("bot_reply", "I've updated the semantic model and visuals based on your input.")
                else:
                    bot_reply = "I encountered an issue processing that. Could you try rephrasing or re-uploading the file?"

                # Append Bot Reply to History
                active_chat["messages"].append({"role": "assistant", "content": bot_reply})

                # Immediate UI refresh to show new preview & history
                st.rerun()

    # --- RIGHT COLUMN: PREVIEW & BUILD ---
    with col_preview:
        preview_container = st.container(height=650)

        with preview_container:
            h_col1, h_col2 = st.columns([3, 1])
            with h_col1:
                st.subheader("👁️ Dashboard Preview")
            with h_col2:
                label = "Exit Full Screen" if st.session_state.full_screen else "⛶ Full Screen"
                if st.button(label, use_container_width=True, type="secondary"):
                    st.session_state.full_screen = not st.session_state.full_screen
                    st.rerun()

            active_id = st.session_state.current_chat_id
            active_chat = st.session_state.chats[active_id]
            frontend = active_chat.get("frontend_spec", {})
            pages = frontend.get("pages", [])

            if pages:
                page_names = [p.get("displayName", p.get("name", f"Page {i+1}")) for i, p in enumerate(pages)]

                # UNIQUE KEY using active_id + "page_selector"
                selected_page_name = st.selectbox(
                    "Select Page Preview:",
                    page_names,
                    key=f"page_selector_{active_id}"
                )

                # Find selected page INDEX (0-based)
                selected_page_idx = page_names.index(selected_page_name)

                st.caption(f"Page: {page_names[selected_page_idx]} | Visuals: {len(pages[selected_page_idx].get('visuals', []))}")

                # Pass FULL frontend + selected page index
                preview_key = "fullscreen_preview" if st.session_state.full_screen else "normal_preview"

                if st.session_state.full_screen:
                    st.divider()
                    render_preview_content(active_chat, selected_page_idx=selected_page_idx, is_full=True, preview_key=preview_key)
                else:
                    # Scrollable preview with proper spacing
                    preview_scroll_box = st.container(height=580)  # Reduced for better fit
                    with preview_scroll_box:
                        st.markdown("---")  # Thin divider for visual separation
                        render_preview_content(active_chat, selected_page_idx, is_full=False, preview_key=preview_key)
            else:
                st.info("Chat with the architect to create your dashboard!")

    st.divider()

    # 2. Compile to PBIP Button
    st.subheader("🚀 Final Output")

    if st.button("🚀 Convert to PBIP Folder", use_container_width=True, type="primary"):
        with st.spinner("Compiling TMDL and Report configurations..."):
            project_name = active_chat["name"].replace(" ", "_")
            output_folder = Path(f"Data/Output/{project_name}")
            os.makedirs(output_folder, exist_ok=True)

            # Use pure code compilers
            build_pbip_semantic_model(active_chat["backend_spec"], project_name)

            compile_to_pbip(project_name, active_chat["frontend_spec"])

            zip_path = bundle_pbip_to_zip(output_folder, f"{project_name}_Ready")

        with open(zip_path, "rb") as f:
            st.download_button("💾 Download .ZIP Workspace", f, file_name=f"{project_name}.zip", use_container_width=True)
        st.success("Compilation complete! Your PBIP is ready.")
