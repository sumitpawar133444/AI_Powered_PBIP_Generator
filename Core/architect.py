# Core/architect.py
import json
import streamlit as st
from google import genai
from google.genai import types
from prompts import ARCHITECT_SYSTEM_INSTRUCTION
from Core.utils import bypass_ssl
from dotenv import load_dotenv
import os

# --- 1. LOAD ENVIRONMENT VARIABLES ---
load_dotenv()
API_KEY = st.secrets("GEMINI_API_KEY")

# Initialize Client
bypass_ssl()

client = genai.Client(
    api_key=API_KEY,
    http_options=types.HttpOptions(
        client_args={"verify": False},
        async_client_args={"verify": False},
    ),
)

def update_project_spec(user_input, current_frontend, current_backend, files=None, audio_bytes=None):
    """
    Sends the current state and user request, files, and audio to Gemini.
    Returns the updated JSON states and the bot's conversational reply.
    """

    # 1. Build the text context
    context_text = f"""
    CURRENT FRONTEND SPEC: {json.dumps(current_frontend)}
    CURRENT BACKEND SPEC: {json.dumps(current_backend)}
    USER REQUEST: {user_input if user_input else "Analyze the attached multimodal data."}
    """

    # 2. Assemble the multimodal parts list
    parts = [
        ARCHITECT_SYSTEM_INSTRUCTION,
        context_text
    ]

    # Append uploaded files
    if files:
        for f in files:
            parts.append(
                types.Part.from_bytes(
                    data=f.getvalue(),
                    mime_type=f.type
                )
            )

    # Append voice recordings
    if audio_bytes:
        parts.append(
            types.Part.from_bytes(
                data=audio_bytes.getvalue(),
                mime_type="audio/wav"
            )
        )

    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents= parts,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    return json.loads(response.text)
