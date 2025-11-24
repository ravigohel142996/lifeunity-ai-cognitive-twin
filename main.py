"""
LifeUnity AI - Cognitive Twin System
Main Streamlit Application with World-Class UI
"""

import streamlit as st
from app.mood_detection import get_mood_detector, DEEPFACE_AVAILABLE
from app.memory_graph import get_memory_graph
from app.user_profile import get_user_profile
from app.insights_engine import get_insights_engine
from app.utils.embedder import SENTENCE_TRANSFORMERS_AVAILABLE
from app import ui
import numpy as np
from PIL import Image
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="LifeUnity – AI Cognitive Twin",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# Load custom CSS
ui.load_global_css()

# Check for missing dependencies and show warning
missing_deps = []
if not DEEPFACE_AVAILABLE:
    missing_deps.append("DeepFace (emotion detection)")
if not SENTENCE_TRANSFORMERS_AVAILABLE:
    missing_deps.append("Sentence-Transformers (memory embeddings)")

if missing_deps:
    st.warning(f"⚠️ **Demo Mode**: Some ML libraries are not available ({', '.join(missing_deps)}). The app will use fallback implementations. To enable full functionality, ensure all dependencies from requirements.txt are installed.")

# Initialize session state for backend instances
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = get_user_profile()
if 'mood_detector' not in st.session_state:
    st.session_state.mood_detector = get_mood_detector()
if 'memory_graph' not in st.session_state:
    st.session_state.memory_graph = get_memory_graph()
if 'insights_engine' not in st.session_state:
    st.session_state.insights_engine = get_insights_engine()


def render_dashboard():
    """Render the main Dashboard page with world-class UI."""
    ui.page_transition()
    
    # Hero section
    ui.render_welcome_banner()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # AI Avatar section
    ui.ai_avatar_section()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get profile data
    profile = st.session_state.user_profile
    profile_summary = profile.get_summary()
    memory_stats = st.session_state.memory_graph.get_graph_stats()
    
    # Dashboard cards
    cards_data = [
        {
            "icon": "😊",
            "title": "Emotion Tracking",
            "value": str(profile_summary['total_emotions_tracked']),
            "description": "Emotions captured"
        },
        {
            "icon": "🧠",
            "title": "Memory Nodes",
            "value": str(memory_stats['total_memories']),
            "description": "Active memories"
        },
        {
            "icon": "💪",
            "title": "Productivity",
            "value": f"{profile_summary['current_productivity']:.0f}%",
            "description": "Current score"
        },
        {
            "icon": "😌",
            "title": "Stress Level",
            "value": f"{profile_summary['current_stress_level']:.0f}%",
            "description": "Current level"
        }
    ]
    
    ui.dashboard_cards(cards_data)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Quick Stats Section
    ui.gradient_text("📊 Quick Overview", size="2rem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui.metric_card("Total Emotions", profile_summary['total_emotions_tracked'])
    
    with col2:
        ui.metric_card("Memory Connections", memory_stats['total_connections'])
    
    with col3:
        ui.metric_card("Memory Clusters", memory_stats['num_clusters'])
    
    with col4:
        avg_conn = memory_stats.get('avg_connections', 0)
        ui.metric_card("Avg Connections", f"{avg_conn:.1f}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity
    ui.section_divider()
    ui.gradient_text("📈 Recent Activity", size="1.8rem")
    
    emotion_history = profile.get_emotion_history(limit=5)
    
    if emotion_history:
        for record in reversed(emotion_history):
            emotion_emoji = st.session_state.mood_detector.get_emotion_emoji(record['emotion'])
            timestamp = datetime.fromisoformat(record['timestamp'])
            
            ui.info_box(
                f"{emotion_emoji} **{record['emotion'].title()}** - "
                f"Confidence: {record['confidence']*100:.1f}% - "
                f"{timestamp.strftime('%Y-%m-%d %H:%M')}",
                box_type="info"
            )
    else:
        ui.render_empty_state(
            icon="📊",
            title="No Activity Yet",
            message="Start tracking your emotions to see your activity here!"
        )
    
    # Footer
    ui.footer()


def render_emotion_detection():
    """Render the Emotion Detection page with world-class UI."""
    ui.page_transition()
    
    ui.hero_section(
        title="Emotion Detection",
        subtitle="Upload a photo to detect your emotional state",
        emoji="😊"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    detector = st.session_state.mood_detector
    profile = st.session_state.user_profile
    
    ui.info_box(
        "📸 Upload a clear photo of your face for accurate emotion analysis",
        box_type="info"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo showing your face"
    )
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        
        col1, col2 = st.columns(2)
        
        with col1:
            ui.gradient_text("📷 Uploaded Image", size="1.5rem")
            ui.image_with_glass_border(image, caption="Your photo")
        
        with col2:
            ui.gradient_text("🎯 Analysis Results", size="1.5rem")
            
            with st.spinner("Analyzing emotion..."):
                result = detector.detect_emotion(image_np, return_all=True)
            
            if result['face_detected']:
                emotion = result['emotion']
                confidence = result['confidence']
                emoji = detector.get_emotion_emoji(emotion)
                
                st.markdown(f"<h2 style='text-align: center; font-size: 4rem;'>{emoji}</h2>", unsafe_allow_html=True)
                ui.gradient_text(f"{emotion.title()}", size="2.5rem")
                
                ui.progress_ring(int(confidence * 100), f"Confidence: {confidence*100:.1f}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if ui.animated_button("💾 Save to Profile", key="save_emotion"):
                    profile.add_emotion_record(emotion, confidence)
                    ui.info_box("✅ Emotion saved successfully!", box_type="success")
                
                # Show all emotions
                if result.get('all_emotions'):
                    st.markdown("<br>", unsafe_allow_html=True)
                    ui.gradient_text("📊 All Detected Emotions", size="1.3rem")
                    
                    emotions_data = result['all_emotions']
                    for emo, score in sorted(emotions_data.items(), key=lambda x: x[1], reverse=True):
                        ui.progress_ring(int(score * 100), emo.title())
            else:
                ui.info_box(
                    "❌ No face detected. Please upload a clearer photo with a visible face.",
                    box_type="error"
                )
    
    # Recent History
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("📜 Recent Emotion History", size="1.8rem")
    
    emotion_history = profile.get_emotion_history(limit=5)
    
    if emotion_history:
        for record in reversed(emotion_history):
            emotion_emoji = detector.get_emotion_emoji(record['emotion'])
            timestamp = datetime.fromisoformat(record['timestamp'])
            
            ui.info_box(
                f"{emotion_emoji} **{record['emotion'].title()}** - "
                f"Confidence: {record['confidence']*100:.1f}% - "
                f"{timestamp.strftime('%Y-%m-%d %H:%M')}",
                box_type="info"
            )
    else:
        ui.render_empty_state(
            icon="😊",
            title="No Emotions Detected Yet",
            message="Upload a photo above to detect your first emotion!"
        )
    
    ui.footer()


def render_memory_graph():
    """Render the Memory Graph page with world-class UI."""
    ui.page_transition()
    
    ui.hero_section(
        title="Cognitive Memory",
        subtitle="Your personal knowledge graph powered by AI",
        emoji="🧩"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    memory_graph = st.session_state.memory_graph
    
    # Add new memory section
    ui.gradient_text("➕ Add New Memory", size="1.8rem")
    
    with st.form("add_memory_form"):
        note_content = st.text_area(
            "Write your note or memory:",
            height=150,
            placeholder="Enter your thoughts, ideas, or experiences...",
            help="Your memory will be embedded and connected to related memories"
        )
        
        tags_input = st.text_input(
            "Tags (comma-separated):",
            placeholder="work, personal, idea, learning, etc."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submitted = st.form_submit_button("💾 Save Memory", type="primary")
        
        if submitted and note_content:
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
            
            with st.spinner("Processing and embedding memory..."):
                memory_id = memory_graph.add_memory(note_content, tags=tags)
            
            if memory_id > 0:
                ui.info_box(f"✅ Memory saved successfully! (ID: {memory_id})", box_type="success")
                st.session_state.user_profile.add_note(note_content, tags=tags)
            else:
                ui.info_box("❌ Failed to save memory. Please try again.", box_type="error")
    
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    
    # Memory Statistics
    col1, col2 = st.columns(2)
    
    with col1:
        ui.gradient_text("📊 Memory Statistics", size="1.5rem")
        stats = memory_graph.get_graph_stats()
        
        ui.metric_card("Total Memories", stats['total_memories'])
        ui.metric_card("Total Connections", stats['total_connections'])
        ui.metric_card("Memory Clusters", stats['num_clusters'])
        if stats['total_memories'] > 0:
            ui.metric_card("Avg Connections", f"{stats['avg_connections']:.2f}")
    
    with col2:
        ui.gradient_text("🔍 Search Memories", size="1.5rem")
        search_query = st.text_input(
            "Search your memories:",
            placeholder="What are you looking for?",
            help="Search uses AI embeddings to find semantically similar memories"
        )
        
        if search_query:
            with st.spinner("Searching..."):
                results = memory_graph.search_memories(search_query, top_k=5)
            
            if results:
                st.markdown(f"**Found {len(results)} relevant memories:**")
                for result in results:
                    with st.expander(f"Memory #{result['id']} - Similarity: {result['similarity']*100:.1f}%"):
                        st.write(result['content'])
                        st.caption(f"📅 {result['timestamp'][:10]}")
                        if result['tags']:
                            st.write(f"🏷️ Tags: {', '.join(result['tags'])}")
            else:
                ui.info_box("No matching memories found.", box_type="info")
    
    # Display all memories
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("📚 All Memories", size="1.8rem")
    
    memories = memory_graph.get_all_memories()
    
    if memories:
        sorted_memories = sorted(memories, key=lambda x: x['timestamp'], reverse=True)
        
        for memory in sorted_memories:
            with st.expander(f"Memory #{memory['id']} - {memory['timestamp'][:10]}"):
                st.write(memory['content'])
                
                if memory.get('tags'):
                    st.write(f"🏷️ Tags: {', '.join(memory['tags'])}")
                
                related = memory_graph.get_related_memories(memory['id'])
                if related:
                    st.write(f"🔗 Connected to {len(related)} other memories")
                
                if st.button(f"🗑️ Delete", key=f"del_{memory['id']}"):
                    if memory_graph.delete_memory(memory['id']):
                        ui.info_box("Memory deleted!", box_type="success")
                        st.rerun()
    else:
        ui.render_empty_state(
            icon="🧩",
            title="No Memories Yet",
            message="Add your first memory above to start building your knowledge graph!"
        )
    
    ui.footer()


def render_insights():
    """Render the AI Insights page with world-class UI."""
    ui.page_transition()
    
    ui.hero_section(
        title="AI Insights",
        subtitle="Proactive well-being intelligence powered by AI",
        emoji="💡"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    insights_engine = st.session_state.insights_engine
    
    # Generate Report Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if ui.animated_button("🔄 Generate Daily Report", key="gen_report"):
            with st.spinner("Analyzing your data and generating insights..."):
                report = insights_engine.generate_daily_report()
                st.session_state.daily_report = report
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display report if available
    if 'daily_report' in st.session_state:
        report = st.session_state.daily_report
        
        ui.gradient_text(f"📋 Daily Report - {report['date']}", size="2rem")
        st.caption(f"Generated at: {report['generated_at'][:19]}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        metrics = report['metrics']
        
        with col1:
            stress = metrics['stress_level']
            stress_emoji = "🟢" if stress < 40 else "🟡" if stress < 70 else "🔴"
            ui.metric_card("Stress Level", f"{stress:.0f}/100", delta=stress_emoji)
        
        with col2:
            productivity = metrics['productivity_score']
            prod_emoji = "🟢" if productivity >= 70 else "🟡" if productivity >= 50 else "🔴"
            ui.metric_card("Productivity", f"{productivity:.0f}/100", delta=prod_emoji)
        
        with col3:
            fatigue = metrics['fatigue_risk']
            fatigue_emoji = "🟢" if fatigue == "low" else "🟡" if fatigue == "moderate" else "🔴"
            ui.metric_card("Fatigue Risk", fatigue.title(), delta=fatigue_emoji)
        
        # Alerts
        if report['alerts']:
            st.markdown("<br>", unsafe_allow_html=True)
            ui.gradient_text("⚠️ Alerts", size="1.5rem")
            for alert in report['alerts']:
                ui.info_box(f"🚨 {alert['message']}", box_type="warning")
        
        # Insights
        st.markdown("<br>", unsafe_allow_html=True)
        ui.section_divider()
        ui.gradient_text("🧠 Insights", size="1.8rem")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stress Analysis")
            stress_insight = report['insights']['stress']
            ui.info_box(
                f"**Status:** {stress_insight['status']}\n\n{stress_insight['description']}",
                box_type="info"
            )
        
        with col2:
            st.markdown("#### Productivity Analysis")
            prod_insight = report['insights']['productivity']
            ui.info_box(
                f"**Status:** {prod_insight['status']}\n\n{prod_insight['description']}",
                box_type="info"
            )
        
        # Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        ui.section_divider()
        ui.gradient_text("💡 Recommendations", size="1.8rem")
        
        recommendations = report['recommendations']
        
        if recommendations:
            for rec in recommendations:
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                
                st.markdown(f"### {priority_emoji} {rec['category']}")
                ui.info_box(
                    f"**Suggestion:** {rec['suggestion']}\n\n**Action:** {rec['action']}",
                    box_type="success"
                )
        else:
            ui.info_box("No specific recommendations at this time. Keep up the good work!", box_type="info")
    
    else:
        ui.info_box(
            "👆 Click 'Generate Daily Report' above to get your personalized AI insights!",
            box_type="info"
        )
    
    # Memory Insights
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("🧩 Memory Insights", size="1.8rem")
    
    memory_insights = insights_engine.suggest_memory_insights(limit=5)
    
    if memory_insights:
        st.write("Recent memories with their relationship network:")
        
        for insight in memory_insights:
            with st.expander(f"Memory #{insight['memory_id']} - {insight['related_count']} connections"):
                st.write(insight['content_preview'])
                st.caption(f"📅 {insight['timestamp'][:10]}")
                if insight['tags']:
                    st.write(f"🏷️ Tags: {', '.join(insight['tags'])}")
    else:
        ui.render_empty_state(
            icon="💡",
            title="No Memory Insights Available",
            message="Add some memories in the Memory Graph page to see insights here!"
        )
    
    ui.footer()


def main():
    """Main application entry point with world-class UI navigation."""
    
    # Sidebar with glassmorphism
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align: center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>🧠 LifeUnity AI</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #b8c5d0;'>Cognitive Twin System</p>", unsafe_allow_html=True)
        
        ui.section_divider()
        
        # Navigation
        page = st.radio(
            "Navigate to:",
            ["Dashboard", "Emotion Detection", "Memory Graph", "Insights"],
            label_visibility="collapsed"
        )
        
        ui.section_divider()
        
        # Quick stats in sidebar
        st.markdown("### Quick Stats")
        profile_summary = st.session_state.user_profile.get_summary()
        st.metric("Stress Level", f"{profile_summary['current_stress_level']:.0f}/100")
        st.metric("Productivity", f"{profile_summary['current_productivity']:.0f}/100")
    
    # Render selected page
    if page == "Dashboard":
        render_dashboard()
    elif page == "Emotion Detection":
        render_emotion_detection()
    elif page == "Memory Graph":
        render_memory_graph()
    elif page == "Insights":
        render_insights()


if __name__ == "__main__":
    main()
