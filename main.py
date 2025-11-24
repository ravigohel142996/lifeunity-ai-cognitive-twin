import streamlit as st
from app.mood_detection import get_mood_detector
from app.memory_graph import get_memory_graph
from app.user_profile import get_user_profile
from app.insights_engine import get_insights_engine

st.set_page_config(
    page_title="LifeUnity – AI Cognitive Twin",
    layout="wide",
    page_icon="🧠"
)

def main():
    st.sidebar.title("🧠 LifeUnity AI – Cognitive Twin")
    page = st.sidebar.radio("Navigation", ["Dashboard", "Emotion Detection", "Memory Graph", "Insights"])

    if page == "Dashboard":
        st.title("📊 Cognitive Dashboard")
        st.write("Welcome! Your AI Twin is running successfully.")

    elif page == "Emotion Detection":
        get_mood_detector()

    elif page == "Memory Graph":
        get_memory_graph()

    elif page == "Insights":
        get_insights_engine()

if __name__ == "__main__":
    main()
