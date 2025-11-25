import streamlit as st
import random

def load_chatbot():
    """
    Load the global floating chatbot component.
    This renders a floating chat button and window that appears on all pages.
    """
    if "global_chat_messages" not in st.session_state:
        st.session_state.global_chat_messages = []

    # Build chat history HTML
    chat_history_html = ""
    for role, msg in st.session_state.global_chat_messages:
        if role == "user":
            chat_history_html += f'<div style="text-align:right;margin:8px 0;"><span style="background:#6a5acd;color:white;padding:8px 12px;border-radius:12px;display:inline-block;max-width:80%;">{msg}</span></div>'
        else:
            chat_history_html += f'<div style="text-align:left;margin:8px 0;"><span style="background:#e0e0e0;color:#333;padding:8px 12px;border-radius:12px;display:inline-block;max-width:80%;">{msg}</span></div>'

    st.markdown(f"""
        <style>
            #chatbot-btn {{
                position: fixed;
                bottom: 25px;
                right: 25px;
                background-color: #6a5acd;
                border-radius: 50%;
                width: 65px;
                height: 65px;
                font-size: 32px;
                color: white;
                text-align: center;
                line-height: 65px;
                cursor: pointer;
                box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
                z-index: 9999;
            }}
            #chat-window {{
                position: fixed;
                bottom: 110px;
                right: 25px;
                width: 350px;
                height: 450px;
                background: rgba(255,255,255,0.95);
                backdrop-filter: blur(7px);
                border-radius: 15px;
                padding: 15px;
                box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
                display: none;
                flex-direction: column;
                z-index: 9998;
            }}
            #close-chat {{
                cursor: pointer;
                font-size: 22px;
                float: right;
                color: #333;
            }}
            #chat-container {{
                flex: 1;
                overflow-y: auto;
                margin: 10px 0;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 8px;
            }}
        </style>

        <div id="chatbot-btn" onclick="document.getElementById('chat-window').style.display='flex';">💬</div>
        <div id="chat-window">
            <div id="close-chat" onclick="document.getElementById('chat-window').style.display='none';">✖</div>
            <h4 style="color:#333;margin:0 0 10px 0;">LifeUnity AI Assistant</h4>
            <div id="chat-container">{chat_history_html}</div>
            <p style="color:#666;font-size:12px;margin-top:10px;">Use the Ask Me Anything page for full chat experience.</p>
        </div>
    """, unsafe_allow_html=True)

def generate_reply(msg):
    """Generate a simple fallback reply when LLM is not available."""
    responses = [
        "Interesting! Tell me more.",
        "I'm here with you. What's next?",
        "Good point — let's explore deeper.",
        "I understand. Continue…"
    ]
    return random.choice(responses)
