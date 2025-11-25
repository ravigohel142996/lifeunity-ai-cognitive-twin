"""
Utilities package for LifeUnity AI Cognitive Twin System.
"""

# Export chat engine for easy imports
try:
    from .chatbot import ask_ai, get_chat_engine, ChatEngine
except ImportError:
    pass
