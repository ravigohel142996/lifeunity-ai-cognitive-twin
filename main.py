import sys
import os

# Path setup for Streamlit Cloud compatibility (must be before any other imports)
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

"""
LifeUnity AI - Cognitive Twin System
Your AI-driven companion for mood analysis, memory intelligence, and proactive mental wellness.
"""

import streamlit as st
import numpy as np
from PIL import Image
from datetime import datetime

# Direct imports from app directory (Streamlit Cloud compatible)
from mood_detection import get_mood_detector
from memory_graph import get_memory_graph
from user_profile import get_user_profile
from insights_engine import get_insights_engine
import ui

# Page configuration
st.set_page_config(
    page_title="LifeUnity AI — Your Cognitive Twin AI-powered emotional intelligence, cognitive memory mapping, and personalized wellness insights.",
    layout="wide",
    page_icon="🧠",
    initial_sidebar_state="expanded"
)

# Load custom CSS
ui.load_global_css()

# Constants
INITIAL_ASSISTANT_MESSAGE = "Hello! 👋 I'm your LifeUnity AI Cognitive Twin. Ask me anything about your emotional well-being, productivity, stress management, or how to use this app. How can I help you today?"

# Initialize session state for backend instances
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = get_user_profile()
if 'mood_detector' not in st.session_state:
    st.session_state.mood_detector = get_mood_detector()
if 'memory_graph' not in st.session_state:
    st.session_state.memory_graph = get_memory_graph()
if 'insights_engine' not in st.session_state:
    st.session_state.insights_engine = get_insights_engine()
if 'first_visit' not in st.session_state:
    st.session_state.first_visit = True


def render_dashboard():
    """Render the main Dashboard page with world-class UI."""
    ui.page_transition()
    
    # Check for first-time visit and show onboarding
    profile = st.session_state.user_profile
    profile_summary = profile.get_summary()
    
    # Show onboarding only for new users with no tracked emotions
    # This provides a better first-time user experience
    if profile_summary['total_emotions_tracked'] == 0 and st.session_state.first_visit:
        ui.render_onboarding_message()
        st.session_state.first_visit = False
    
    # Hero section with large gradient title
    st.markdown("""
    <div class="hero-section" style="background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(20px); border-radius: 30px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 4rem 3rem; margin: 1rem 0 2rem 0; text-align: center; position: relative; overflow: hidden;">
        <div style="font-size: 5rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.5));">🧠</div>
        <h1 style="font-size: 3.2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 1rem;">LifeUnity AI</h1>
        <p style="font-size: 1.4rem; color: #94A3B8; max-width: 600px; margin: 0 auto;">Cognitive Twin System</p>
        <p style="font-size: 1rem; color: #64748B; margin-top: 0.5rem;">Your Personal AI-Powered Mental Health & Productivity Companion</p>
    </div>
    """, unsafe_allow_html=True)
    
    # AI Avatar section
    ui.ai_avatar_section()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Get profile data
    memory_stats = st.session_state.memory_graph.get_graph_stats()
    
    # 3 Glowing Analytics Cards
    ui.gradient_text("📊 Analytics Overview", size="1.8rem")
    
    cards_data = [
        {
            "icon": "😊",
            "title": "Emotion Status",
            "value": str(profile_summary['total_emotions_tracked']),
            "description": "Emotions tracked"
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
            "description": "Current indicator"
        }
    ]
    
    ui.dashboard_cards(cards_data)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Animated Confidence/Progress Bar
    ui.gradient_text("📈 Overall Wellness Score", size="1.5rem")
    wellness_score = max(0, 100 - profile_summary['current_stress_level'])
    ui.render_animated_confidence_bar(int(wellness_score), "Wellness Level")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Stats Row
    ui.section_divider()
    ui.gradient_text("⚡ Quick Stats", size="1.8rem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ui.metric_card("Total Emotions", profile_summary['total_emotions_tracked'])
    
    with col2:
        ui.metric_card("Memory Nodes", memory_stats['total_memories'])
    
    with col3:
        ui.metric_card("Connections", memory_stats['total_connections'])
    
    with col4:
        ui.metric_card("Clusters", memory_stats['num_clusters'])
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Two-column layout for Memory Preview and Daily Insight
    col1, col2 = st.columns(2)
    
    with col1:
        ui.gradient_text("🧩 Memory Graph", size="1.5rem")
        ui.render_memory_preview_card(
            memory_stats['total_memories'],
            memory_stats['total_connections']
        )
    
    with col2:
        ui.gradient_text("💡 Daily AI Insight", size="1.5rem")
        
        # Generate a simple daily insight with clear stress level categorization
        stress_level = profile_summary['current_stress_level']
        if stress_level < 40:
            stress_status = "Low"
        elif stress_level < 70:
            stress_status = "Moderate"
        else:
            stress_status = "High"
        
        insight_content = (
            f"Your current stress level is <strong>{stress_status}</strong> ({stress_level:.0f}%). "
            f"Productivity score is at <strong>{profile_summary['current_productivity']:.0f}%</strong>."
            f"<br><br>💡 <em>Tip: Regular emotion tracking helps improve self-awareness and well-being.</em>"
        )
        ui.render_daily_insight_card("Today's Overview", insight_content, "🌟")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Recent Activity
    ui.section_divider()
    ui.gradient_text("📜 Recent Activity", size="1.8rem")
    
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
    
    # Why This Dashboard Matters section - Story-driven with benefits
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("🔹 Why This Dashboard Matters", size="1.8rem")
    
    # Story-driven benefits using columns for better Streamlit compatibility
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 1.5rem; position: relative; overflow: hidden; height: 100%;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #10B981, #34D399);"></div>
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🧠</div>
            <h3 style="color: #F1F5F9; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.1rem;">Understand Your Emotional State</h3>
            <p style="color: #94A3B8; line-height: 1.6; margin: 0; font-size: 0.9rem;">Track happiness, stress, fatigue, and emotional balance. AI-powered analysis helps identify patterns in your mental well-being.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 1.5rem; position: relative; overflow: hidden; height: 100%;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #6366F1, #8B5CF6);"></div>
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">💡</div>
            <h3 style="color: #F1F5F9; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.1rem;">Mental Wellbeing Guidance</h3>
            <p style="color: #94A3B8; line-height: 1.6; margin: 0; font-size: 0.9rem;">Receive personalized recommendations for stress management, productivity optimization, and cognitive wellness.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 1.5rem; position: relative; overflow: hidden; height: 100%;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #EC4899, #F472B6);"></div>
            <div style="font-size: 2.5rem; margin-bottom: 1rem;">🤖</div>
            <h3 style="color: #F1F5F9; font-weight: 700; margin-bottom: 0.75rem; font-size: 1.1rem;">Your Personal Cognitive Twin</h3>
            <p style="color: #94A3B8; line-height: 1.6; margin: 0; font-size: 0.9rem;">An AI that learns and evolves with you, monitoring cognitive patterns and providing automation for better decisions.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Additional expandable details
    with st.expander("🚀 Future Vision: LifeUnity AI Brain 2.0"):
        st.markdown("""
        **Coming Soon:**
        - 🔮 Predictive mood forecasting with machine learning
        - 🧬 Habit embeddings for behavioral optimization
        - 🎭 Adaptive personality AI that grows with you
        - 💬 Memory-aware smart conversations
        - 📊 Advanced analytics and trend visualization
        
        *Your Cognitive Twin evolves with you, becoming smarter and more personalized over time.*
        """)
    
    # Footer
    ui.footer()


def render_emotion_detection():
    """Render the Emotion Detection page with world-class UI."""
    ui.page_transition()
    
    ui.hero_section(
        title="Mood Detection",
        subtitle="Upload a photo to detect your emotional state with AI-powered analysis",
        emoji="😊"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    detector = st.session_state.mood_detector
    profile = st.session_state.user_profile
    
    # Instructions with glass card styling
    ui.info_box(
        "📸 <strong>How it works:</strong> Upload a clear photo of your face. Our AI will analyze your expression and detect your current emotional state with confidence scores.",
        box_type="info"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # File uploader with styled container
    uploaded_file = st.file_uploader(
        "Choose an image...",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo showing your face for accurate emotion analysis"
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
            
            with st.spinner("🔍 Analyzing emotion..."):
                result = detector.detect_emotion(image_np, return_all=True)
            
            if result['face_detected']:
                emotion = result['emotion']
                confidence = result['confidence']
                emoji = detector.get_emotion_emoji(emotion)
                
                # Display emotion card
                st.markdown(f"""
                <div style="text-align: center; padding: 2rem;">
                    <div style="font-size: 5rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.5));">{emoji}</div>
                    <h2 style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">{emotion.title()}</h2>
                </div>
                """, unsafe_allow_html=True)
                
                ui.render_animated_confidence_bar(int(confidence * 100), "Confidence Score")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if ui.animated_button("💾 Save to Profile", key="save_emotion"):
                    profile.add_emotion_record(emotion, confidence)
                    ui.info_box("✅ Emotion saved successfully to your profile!", box_type="success")
                
                # Show all emotions breakdown
                if result.get('all_emotions'):
                    st.markdown("<br>", unsafe_allow_html=True)
                    ui.gradient_text("📊 Emotion Breakdown", size="1.3rem")
                    
                    emotions_data = result['all_emotions']
                    for emo, score in sorted(emotions_data.items(), key=lambda x: x[1], reverse=True):
                        emo_emoji = detector.get_emotion_emoji(emo)
                        ui.render_animated_confidence_bar(int(score * 100), f"{emo_emoji} {emo.title()}")
            else:
                ui.info_box(
                    "❌ <strong>No face detected.</strong> Please upload a clearer photo with a visible face for accurate emotion analysis.",
                    box_type="error"
                )
    else:
        # Show helpful empty state
        ui.render_empty_state(
            icon="📷",
            title="Upload a Photo",
            message="Upload an image above to analyze your emotional state"
        )
    
    # Recent Emotion History
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("📜 Recent Emotion History", size="1.8rem")
    
    emotion_history = profile.get_emotion_history(limit=5)
    
    if emotion_history:
        for record in reversed(emotion_history):
            emotion_emoji = detector.get_emotion_emoji(record['emotion'])
            timestamp = datetime.fromisoformat(record['timestamp'])
            
            ui.info_box(
                f"{emotion_emoji} <strong>{record['emotion'].title()}</strong> - "
                f"Confidence: {record['confidence']*100:.1f}% - "
                f"📅 {timestamp.strftime('%Y-%m-%d %H:%M')}",
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
        subtitle="Build your personal knowledge graph powered by AI embeddings",
        emoji="🧩"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    memory_graph = st.session_state.memory_graph
    
    # Instructions
    ui.info_box(
        "💡 <strong>How it works:</strong> Add notes, thoughts, or experiences. The AI will automatically embed and connect related memories to build your cognitive knowledge graph.",
        box_type="info"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Add new memory section
    ui.gradient_text("➕ Add New Memory", size="1.8rem")
    
    with st.form("add_memory_form"):
        note_content = st.text_area(
            "Write your note or memory:",
            height=150,
            placeholder="Enter your thoughts, ideas, experiences, or learnings...",
            help="Your memory will be embedded using AI and connected to related memories"
        )
        
        tags_input = st.text_input(
            "Tags (comma-separated):",
            placeholder="work, personal, idea, learning, project, etc."
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submitted = st.form_submit_button("💾 Save Memory", type="primary")
        
        if submitted and note_content:
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
            
            with st.spinner("🔄 Processing and embedding memory..."):
                memory_id = memory_graph.add_memory(note_content, tags=tags)
            
            if memory_id > 0:
                ui.info_box(f"✅ Memory saved successfully! (ID: {memory_id})", box_type="success")
                st.session_state.user_profile.add_note(note_content, tags=tags)
            else:
                ui.info_box("❌ Failed to save memory. Please try again.", box_type="error")
        elif submitted and not note_content:
            ui.info_box("⚠️ Please enter some content for your memory.", box_type="warning")
    
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    
    # Memory Statistics and Search side by side
    col1, col2 = st.columns(2)
    
    with col1:
        ui.gradient_text("📊 Memory Statistics", size="1.5rem")
        stats = memory_graph.get_graph_stats()
        
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(20px); border-radius: 16px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 1.5rem; margin-bottom: 1rem;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{stats['total_memories']}</div>
                    <div style="color: #94A3B8; font-size: 0.85rem;">Total Memories</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{stats['total_connections']}</div>
                    <div style="color: #94A3B8; font-size: 0.85rem;">Connections</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{stats['num_clusters']}</div>
                    <div style="color: #94A3B8; font-size: 0.85rem;">Clusters</div>
                </div>
                <div style="text-align: center; padding: 1rem;">
                    <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{stats['avg_connections']:.1f}</div>
                    <div style="color: #94A3B8; font-size: 0.85rem;">Avg Connections</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        ui.gradient_text("🔍 Search Memories", size="1.5rem")
        search_query = st.text_input(
            "Search your memories:",
            placeholder="What are you looking for?",
            help="Search uses AI embeddings to find semantically similar memories"
        )
        
        if search_query:
            with st.spinner("🔍 Searching..."):
                results = memory_graph.search_memories(search_query, top_k=5)
            
            if results:
                st.markdown(f"**Found {len(results)} relevant memories:**")
                for result in results:
                    with st.expander(f"📝 Memory #{result['id']} - Similarity: {result['similarity']*100:.1f}%"):
                        st.write(result['content'])
                        st.caption(f"📅 {result['timestamp'][:10]}")
                        if result['tags']:
                            st.write(f"🏷️ Tags: {', '.join(result['tags'])}")
            else:
                ui.info_box("No matching memories found. Try different keywords.", box_type="info")
    
    # Display all memories
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("📚 All Memories", size="1.8rem")
    
    memories = memory_graph.get_all_memories()
    
    if memories:
        sorted_memories = sorted(memories, key=lambda x: x['timestamp'], reverse=True)
        
        for memory in sorted_memories:
            with st.expander(f"📝 Memory #{memory['id']} - {memory['timestamp'][:10]}"):
                st.write(memory['content'])
                
                if memory.get('tags'):
                    st.write(f"🏷️ **Tags:** {', '.join(memory['tags'])}")
                
                related = memory_graph.get_related_memories(memory['id'])
                if related:
                    st.write(f"🔗 **Connected to {len(related)} other memories**")
                
                if st.button(f"🗑️ Delete Memory", key=f"del_{memory['id']}"):
                    if memory_graph.delete_memory(memory['id']):
                        ui.info_box("✅ Memory deleted successfully!", box_type="success")
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
        subtitle="Proactive well-being intelligence powered by AI analysis",
        emoji="💡"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    insights_engine = st.session_state.insights_engine
    
    # Instructions
    ui.info_box(
        "🧠 <strong>AI-Powered Analysis:</strong> Generate comprehensive daily reports based on your emotional patterns, stress levels, and productivity metrics.",
        box_type="info"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate Report Button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if ui.animated_button("🔄 Generate Daily Report", key="gen_report"):
            with st.spinner("🧠 Analyzing your data and generating insights..."):
                report = insights_engine.generate_daily_report()
                st.session_state.daily_report = report
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Display report if available
    if 'daily_report' in st.session_state:
        report = st.session_state.daily_report
        
        ui.gradient_text(f"📋 Daily Report - {report['date']}", size="2rem")
        st.caption(f"Generated at: {report['generated_at'][:19]}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Metrics Cards
        col1, col2, col3 = st.columns(3)
        metrics = report['metrics']
        
        with col1:
            stress = metrics['stress_level']
            stress_status = "good" if stress < 40 else "warning" if stress < 70 else "alert"
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 2rem; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">😰</div>
                <div style="font-size: 0.9rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Stress Level</div>
                <div style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{stress:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
            ui.render_status_indicator(stress_status, "Low" if stress < 40 else "Moderate" if stress < 70 else "High")
        
        with col2:
            productivity = metrics['productivity_score']
            prod_status = "good" if productivity >= 70 else "warning" if productivity >= 50 else "alert"
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 2rem; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💪</div>
                <div style="font-size: 0.9rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Productivity</div>
                <div style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{productivity:.0f}/100</div>
            </div>
            """, unsafe_allow_html=True)
            ui.render_status_indicator(prod_status, "Excellent" if productivity >= 70 else "Good" if productivity >= 50 else "Needs Work")
        
        with col3:
            fatigue = metrics['fatigue_risk']
            fatigue_status = "good" if fatigue == "low" else "warning" if fatigue == "moderate" else "alert"
            fatigue_emoji = "😊" if fatigue == "low" else "😐" if fatigue == "moderate" else "😴"
            st.markdown(f"""
            <div style="background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(20px); border-radius: 20px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 2rem; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{fatigue_emoji}</div>
                <div style="font-size: 0.9rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Fatigue Risk</div>
                <div style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{fatigue.title()}</div>
            </div>
            """, unsafe_allow_html=True)
            ui.render_status_indicator(fatigue_status, fatigue.title())
        
        # Alerts
        if report['alerts']:
            st.markdown("<br>", unsafe_allow_html=True)
            ui.gradient_text("⚠️ Alerts", size="1.5rem")
            for alert in report['alerts']:
                ui.info_box(f"🚨 {alert['message']}", box_type="warning")
        
        # Insights
        st.markdown("<br>", unsafe_allow_html=True)
        ui.section_divider()
        ui.gradient_text("🧠 Detailed Insights", size="1.8rem")
        
        col1, col2 = st.columns(2)
        
        with col1:
            ui.gradient_text("😰 Stress Analysis", size="1.3rem")
            stress_insight = report['insights']['stress']
            ui.render_daily_insight_card(
                f"Status: {stress_insight['status']}",
                stress_insight['description'],
                "📊"
            )
        
        with col2:
            ui.gradient_text("💪 Productivity Analysis", size="1.3rem")
            prod_insight = report['insights']['productivity']
            ui.render_daily_insight_card(
                f"Status: {prod_insight['status']}",
                prod_insight['description'],
                "📈"
            )
        
        # Recommendations
        st.markdown("<br>", unsafe_allow_html=True)
        ui.section_divider()
        ui.gradient_text("💡 AI Recommendations", size="1.8rem")
        
        recommendations = report['recommendations']
        
        if recommendations:
            for rec in recommendations:
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                priority_box = "error" if rec['priority'] == 'high' else "warning" if rec['priority'] == 'medium' else "success"
                
                ui.info_box(
                    f"{priority_emoji} <strong>{rec['category']}</strong><br><br>"
                    f"💡 {rec['suggestion']}<br><br>"
                    f"✅ <em>Action:</em> {rec['action']}",
                    box_type=priority_box
                )
        else:
            ui.info_box("✨ No specific recommendations at this time. Keep up the good work!", box_type="success")
    
    else:
        # Empty state
        st.markdown("<br>", unsafe_allow_html=True)
        ui.render_empty_state(
            icon="💡",
            title="No Report Generated",
            message="Click 'Generate Daily Report' above to get your personalized AI insights!"
        )
    
    # Memory Insights Section
    st.markdown("<br>", unsafe_allow_html=True)
    ui.section_divider()
    ui.gradient_text("🧩 Memory Insights", size="1.8rem")
    
    memory_insights = insights_engine.suggest_memory_insights(limit=5)
    
    if memory_insights:
        ui.info_box("📚 Recent memories with their relationship network:", box_type="info")
        
        for insight in memory_insights:
            with st.expander(f"📝 Memory #{insight['memory_id']} - {insight['related_count']} connections"):
                st.write(insight['content_preview'])
                st.caption(f"📅 {insight['timestamp'][:10]}")
                if insight['tags']:
                    st.write(f"🏷️ **Tags:** {', '.join(insight['tags'])}")
                st.write(f"🔗 **Connections:** {insight['related_count']} related memories")
    else:
        ui.render_empty_state(
            icon="🧩",
            title="No Memory Insights Available",
            message="Add some memories in the Memory Graph page to see insights here!"
        )
    
    ui.footer()


def generate_ai_response(user_message: str) -> str:
    """
    Generate AI response based on user message and context.
    Uses the centralized chat engine for consistent responses.
    """
    try:
        from app.utils.chatbot import ask_ai
    except ImportError:
        try:
            from utils.chatbot import ask_ai
        except ImportError:
            # Fallback to inline response
            return _fallback_response(user_message)
    
    # Get user context for personalized responses
    context = {}
    try:
        profile_summary = st.session_state.user_profile.get_summary()
        context['stress_level'] = profile_summary['current_stress_level']
        context['productivity'] = profile_summary['current_productivity']
        context['total_emotions'] = profile_summary['total_emotions_tracked']
        
        memory_stats = st.session_state.memory_graph.get_graph_stats()
        context['total_memories'] = memory_stats['total_memories']
        context['total_connections'] = memory_stats['total_connections']
    except Exception:
        pass
    
    return ask_ai(user_message, context)


def _fallback_response(user_message: str) -> str:
    """Fallback response generator when chat engine is unavailable."""
    user_message_lower = user_message.lower()
    
    # Get user context
    profile_summary = st.session_state.user_profile.get_summary()
    memory_graph = st.session_state.memory_graph
    
    # Context-aware responses
    if any(word in user_message_lower for word in ['stress', 'stressed', 'anxious', 'anxiety']):
        stress_level = profile_summary['current_stress_level']
        if stress_level > 70:
            return f"I notice your stress level is currently at {stress_level:.0f}/100, which is elevated. Here are some suggestions:\n\n🧘 **Deep breathing**: Try 4-7-8 breathing - inhale for 4 seconds, hold for 7, exhale for 8.\n\n🚶 **Take a break**: A short walk can help reduce stress hormones.\n\n💭 **Journal your thoughts**: Writing down what's bothering you can provide clarity."
        elif stress_level > 40:
            return f"Your stress level is at {stress_level:.0f}/100, which is moderate. To keep it in check:\n\n☕ **Stay hydrated** and avoid excessive caffeine.\n\n🎵 **Listen to calming music** or nature sounds.\n\n⏰ **Prioritize tasks** - focus on what's most important first."
        else:
            return f"Great news! Your stress level is at {stress_level:.0f}/100, which is well-managed. Keep up the good work! 🌟\n\n💡 **Tip**: Continue your current wellness practices and track your emotions regularly."
    
    elif any(word in user_message_lower for word in ['productivity', 'productive', 'focus', 'work']):
        productivity = profile_summary['current_productivity']
        if productivity >= 70:
            return f"Excellent! Your productivity score is {productivity:.0f}/100. You're in a great zone! 🚀\n\n**Maximize this state by:**\n• Tackling your most challenging tasks now\n• Using the Pomodoro technique (25 min work, 5 min break)\n• Staying hydrated and energized"
        else:
            return f"Your productivity is at {productivity:.0f}/100. Let's boost it! 💪\n\n**Try these strategies:**\n• Break large tasks into smaller, manageable chunks\n• Eliminate distractions (phone on silent, close unnecessary tabs)\n• Set specific goals for the next hour\n• Take short breaks to recharge"
    
    elif any(word in user_message_lower for word in ['mood', 'feeling', 'emotion', 'happy', 'sad']):
        return "I can help you understand your emotions better! 😊\n\n**Here's how I can assist:**\n• Go to **Mood Detection** to analyze your current emotional state from a photo\n• Check **AI Insights** for patterns in your emotional well-being\n• Track emotions over time to identify triggers and trends\n\nHow are you feeling right now? I'm here to listen! 💜"
    
    elif any(word in user_message_lower for word in ['memory', 'memories', 'remember', 'note']):
        stats = memory_graph.get_graph_stats()
        return f"Your cognitive memory graph currently has **{stats['total_memories']} memories** with **{stats['total_connections']} connections**! 🧩\n\n**Tips for better memory management:**\n• Add notes regularly to build your knowledge graph\n• Use tags to organize memories by topic\n• Search memories to find related thoughts and ideas\n\nWant to add a new memory? Head to the **Cognitive Memory** page!"
    
    elif any(word in user_message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
        return "Hello! 👋 Welcome to LifeUnity AI - your Cognitive Twin!\n\n**I can help you with:**\n🧠 Understanding your emotions and mood patterns\n📊 Tracking and improving your productivity\n💡 Getting personalized AI insights\n🧩 Building your cognitive memory graph\n\nWhat would you like to explore today?"
    
    elif any(word in user_message_lower for word in ['help', 'what can you do', 'features']):
        return "I'm your AI-powered Cognitive Twin! Here's what I can do: 🌟\n\n**🏠 Dashboard** - View your overall wellness metrics\n\n**😊 Mood Detection** - Analyze emotions from photos using AI\n\n**🧩 Cognitive Memory** - Build a knowledge graph of your thoughts\n\n**💡 AI Insights** - Get personalized recommendations\n\n**💬 Chat** - Talk to me anytime for guidance!\n\nJust ask me anything about stress, productivity, emotions, or well-being!"
    
    elif any(word in user_message_lower for word in ['thank', 'thanks', 'appreciate']):
        return "You're welcome! 😊 I'm always here to help you on your wellness journey.\n\nRemember: Taking care of your mental health is a strength, not a weakness. Keep tracking, keep growing! 💜\n\nIs there anything else I can help you with?"
    
    else:
        # Default intelligent response
        return f"Thanks for your message! 🤖\n\nI'm your Cognitive Twin assistant, designed to help with:\n\n• **Emotional wellness** - Track and understand your moods\n• **Productivity** - Optimize your work patterns\n• **Memory** - Build your personal knowledge graph\n• **Insights** - Get AI-powered recommendations\n\n**Quick stats:**\n• Stress Level: {profile_summary['current_stress_level']:.0f}/100\n• Productivity: {profile_summary['current_productivity']:.0f}/100\n\nTry asking about stress management, productivity tips, or how to track your emotions!"


def render_ask_me_anything():
    """Render the Ask Me Anything chatbot page with world-class UI."""
    ui.page_transition()
    
    ui.hero_section(
        title="Ask Me Anything",
        subtitle="Your AI Cognitive Twin is ready to assist you with personalized guidance",
        emoji="🤖"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Initialize chat history
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = [
            {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
        ]
    
    # Instructions
    ui.info_box(
        "💬 <strong>Chat with your AI Twin:</strong> Ask questions about stress management, productivity tips, emotional well-being, or any features of the app. I provide personalized responses based on your profile data.",
        box_type="info"
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat container with messages
    chat_container = st.container()
    
    with chat_container:
        for message in st.session_state.chat_messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                    <div style="background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); 
                                color: white; padding: 1rem 1.5rem; border-radius: 20px 20px 5px 20px; 
                                max-width: 80%; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);">
                        {message["content"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                    <div style="background: rgba(30, 41, 59, 0.8); backdrop-filter: blur(20px);
                                color: #F1F5F9; padding: 1rem 1.5rem; border-radius: 20px 20px 20px 5px; 
                                max-width: 80%; border: 1px solid rgba(99, 102, 241, 0.2);
                                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);">
                        <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem;">
                            <span style="font-size: 1.2rem;">🤖</span>
                            <span style="font-weight: 600; color: #8B5CF6;">LifeUnity AI</span>
                        </div>
                        <div style="line-height: 1.6; white-space: pre-line;">{message["content"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Chat input with form for enter key support
    with st.form(key="chat_form", clear_on_submit=True):
        col1, col2 = st.columns([6, 1])
        with col1:
            user_input = st.text_input(
                "Type your message:",
                placeholder="Ask me anything...",
                label_visibility="collapsed",
                key="chat_input"
            )
        with col2:
            submit_button = st.form_submit_button("Send 🚀", use_container_width=True)
        
        if submit_button and user_input:
            # Add user message
            st.session_state.chat_messages.append({"role": "user", "content": user_input})
            
            # Generate AI response
            response = generate_ai_response(user_input)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            
            # Rerun to show new messages
            st.rerun()
    
    def handle_quick_action(message: str, button_key: str, button_label: str) -> bool:
        """Handle quick action button click."""
        if st.button(button_label, use_container_width=True, key=button_key):
            st.session_state.chat_messages.append({"role": "user", "content": message})
            response = generate_ai_response(message)
            st.session_state.chat_messages.append({"role": "assistant", "content": response})
            st.rerun()
        return False
    
    # Quick action buttons
    st.markdown("<br>", unsafe_allow_html=True)
    ui.gradient_text("⚡ Quick Questions", size="1.3rem")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        handle_quick_action("How can I manage my stress?", "quick_stress", "😰 Stress Tips")
    
    with col2:
        handle_quick_action("How can I be more productive?", "quick_prod", "💪 Productivity")
    
    with col3:
        handle_quick_action("How do I track my mood?", "quick_mood", "😊 Track Mood")
    
    with col4:
        handle_quick_action("What can you help me with?", "quick_help", "❓ Help")
    
    # Clear chat button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🗑️ Clear Chat History", key="clear_chat"):
        st.session_state.chat_messages = [
            {"role": "assistant", "content": INITIAL_ASSISTANT_MESSAGE}
        ]
        st.rerun()
    
    ui.footer()


def render_floating_chatbot():
    """Render the floating chatbot bubble that's always visible."""
    # Initialize floating chat state
    if 'floating_chat_open' not in st.session_state:
        st.session_state.floating_chat_open = False
    if 'floating_chat_messages' not in st.session_state:
        st.session_state.floating_chat_messages = [
            {"role": "assistant", "content": "Hi! 👋 I'm your quick AI assistant. How can I help?"}
        ]
    
    # Inject floating chatbot CSS and HTML
    floating_css = """
    <style>
    /* Floating Chatbot Bubble */
    .floating-chat-bubble {
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5);
        z-index: 9999;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        animation: chatPulse 2s ease-in-out infinite;
    }
    
    .floating-chat-bubble:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 40px rgba(99, 102, 241, 0.6);
    }
    
    .floating-chat-bubble span {
        font-size: 1.8rem;
    }
    
    @keyframes chatPulse {
        0%, 100% { box-shadow: 0 8px 30px rgba(99, 102, 241, 0.5); }
        50% { box-shadow: 0 8px 40px rgba(99, 102, 241, 0.7); }
    }
    
    /* Floating Chat Window */
    .floating-chat-window {
        position: fixed;
        bottom: 100px;
        right: 30px;
        width: 380px;
        max-height: 500px;
        background: rgba(15, 23, 42, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        z-index: 9998;
        overflow: hidden;
        animation: slideUp 0.3s ease;
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .floating-chat-header {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        padding: 1rem 1.5rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .floating-chat-header h4 {
        margin: 0;
        color: white;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .floating-chat-close {
        background: rgba(255, 255, 255, 0.2);
        border: none;
        color: white;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        cursor: pointer;
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .floating-chat-body {
        padding: 1rem;
        max-height: 350px;
        overflow-y: auto;
    }
    
    .floating-chat-input-container {
        padding: 1rem;
        border-top: 1px solid rgba(99, 102, 241, 0.2);
        display: flex;
        gap: 0.5rem;
    }
    
    .floating-chat-input {
        flex: 1;
        background: rgba(30, 41, 59, 0.8);
        border: 1px solid rgba(99, 102, 241, 0.3);
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: #F1F5F9;
        font-size: 0.9rem;
    }
    
    .floating-chat-send {
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        border: none;
        border-radius: 12px;
        padding: 0.75rem 1rem;
        color: white;
        cursor: pointer;
        font-weight: 600;
    }
    
    /* Mobile responsiveness */
    @media (max-width: 768px) {
        .floating-chat-window {
            width: calc(100% - 40px);
            right: 20px;
            bottom: 90px;
        }
        
        .floating-chat-bubble {
            bottom: 20px;
            right: 20px;
            width: 55px;
            height: 55px;
        }
    }
    </style>
    """
    st.markdown(floating_css, unsafe_allow_html=True)


def main():
    """Main application entry point with world-class UI navigation."""
    
    # Show startup badge once for missing dependencies (non-intrusive)
    if 'startup_badge_shown' not in st.session_state:
        st.session_state.startup_badge_shown = True
        # Check dependencies silently - no warnings shown to user
    
    # Render floating chatbot (always visible) - use new chatbot_component
    from chatbot_component import load_chatbot
    load_chatbot()
    
    # Sidebar with glassmorphism navigation
    with st.sidebar:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Brand Logo
        st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 3rem; margin-bottom: 0.5rem;">🧠</div>
            <h1 style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;">LifeUnity AI</h1>
            <p style="color: #64748B; font-size: 0.9rem; margin-top: 0.5rem;">Cognitive Twin System</p>
        </div>
        """, unsafe_allow_html=True)
        
        ui.section_divider()
        
        # Navigation with styled radio buttons - Added Ask Me Anything
        st.markdown("<p style='color: #94A3B8; font-weight: 600; margin-bottom: 0.5rem; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;'>📍 Navigation</p>", unsafe_allow_html=True)
        
        page = st.radio(
            "Navigate to:",
            ["🏠 Dashboard", "😊 Mood Detection", "🧩 Cognitive Memory", "💡 AI Insights", "💬 Ask Me Anything"],
            label_visibility="collapsed"
        )
        
        ui.section_divider()
        
        # Quick stats in sidebar with enhanced styling
        st.markdown("<p style='color: #94A3B8; font-weight: 600; margin-bottom: 1rem; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em;'>📊 Quick Stats</p>", unsafe_allow_html=True)
        
        profile_summary = st.session_state.user_profile.get_summary()
        
        # Styled metrics
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
            <div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.25rem;">Stress Level</div>
            <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{profile_summary['current_stress_level']:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 1rem; margin-bottom: 0.75rem;">
            <div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.25rem;">Productivity</div>
            <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{profile_summary['current_productivity']:.0f}/100</div>
        </div>
        """, unsafe_allow_html=True)
        
        memory_stats = st.session_state.memory_graph.get_graph_stats()
        st.markdown(f"""
        <div style="background: rgba(99, 102, 241, 0.1); border-radius: 12px; padding: 1rem;">
            <div style="color: #94A3B8; font-size: 0.8rem; margin-bottom: 0.25rem;">Total Memories</div>
            <div style="font-size: 1.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{memory_stats['total_memories']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Version info at bottom with updated credits
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="text-align: center; padding-top: 1rem; border-top: 1px solid rgba(99, 102, 241, 0.2);">
            <p style="color: #F1F5F9; font-size: 0.8rem; font-weight: 600;">Built by Ravi Gohel • Hack4Unity 2025</p>
            <p style="color: #8B5CF6; font-size: 0.65rem; margin-top: 0.25rem;">Empowering humanity with AI-based cognitive wellness</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Render selected page based on navigation
    if "Dashboard" in page:
        render_dashboard()
    elif "Mood Detection" in page:
        render_emotion_detection()
    elif "Cognitive Memory" in page:
        render_memory_graph()
    elif "AI Insights" in page:
        render_insights()
    elif "Ask Me Anything" in page:
        render_ask_me_anything()


if __name__ == "__main__":
    main()
