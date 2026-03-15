import streamlit as st

def inject_custom_css():
    st.markdown("""
    <style>
        html, body, [class*="css"] { font-size: 13px !important; }
        .block-container { padding-top: 4rem !important; padding-bottom: 1rem !important; }

        .stMarkdown p,
        .stMarkdown span,
        .stMarkdown li {
            font-size: 13px;
            word-wrap: break-word;
            overflow-wrap: break-word;
            white-space: normal;
        }

        /* FIX: Word Wrap and Clipping */
        .unified-chat-input div[data-testid="stChatInput"] textarea {
            padding-right: 95px !important;
            word-wrap: break-word !important;
            overflow-wrap: break-word !important;
            white-space: pre-wrap !important;
        }

        /* Compact elements from original code */
        [data-testid="stChart"] { height: 220px !important; }
        [data-testid="stSidebar"] { width: 300px !important; }

        .unified-chat-input {
            position: fixed;
            bottom: 1.5rem;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            max-width: 900px;
            z-index: 9999;
        }

        .unified-chat-input div[data-testid="stAudioInput"] {
            position: absolute !important;
            right: 52px !important;
            top: 50% !important;
            transform: translateY(-50%) !important;
            margin: 0 !important;
            padding: 0 !important;
            z-index: 10001 !important;
            background: transparent !important;
            border: none !important;
        }

        .unified-chat-input div[data-testid="stAudioInput"] div {
            border: none !important;
            background: transparent !important;
            box-shadow: none !important;
        }

        .unified-chat-input div[data-testid="stAudioInput"] label {
            display: none !important;
        }

        /* Ensure the Preview Header is always visible */
        .preview-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
            background: white;
            z-index: 10;
            padding: 5px 0;
        }

        /* Prevent Clipping in fixed containers */
        [data-testid="stVerticalBlock"] > div:has(div.stMetric) {
            padding: 5px !important;
        }

        /* IDE-style JSON Editor */
        .json-editor textarea {
            font-family: 'Cascadia Code', 'Consolas', monospace !important;
            font-size: 11px !important;
            line-height: 1.2 !important;
            background-color: #f8f9fa !important;
        }

        /* Shrink Visual Elements */
        [data-testid="stMetricValue"] { font-size: 1.5rem !important; }

        /* Hide redundant PBI headers in preview */
        .stMarkdown h2 { margin-top: 0px !important; padding-top: 0px !important; }

        /* Full Screen Toggle Simulation */
        .fullScreenFrame {
            position: fixed;
            top: 0; left: 0;
            width: 100vw; height: 100vh;
            background: white;
            z-index: 9999;
            padding: 2rem;
            overflow-y: auto;
        }

    </style>
    """, unsafe_allow_html=True)