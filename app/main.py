"""
LifeUnity AI — Cognitive Twin System
Main Streamlit Application with 4-page interface
"""

import streamlit as st
import cv2
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd

# Import modules
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from mood_detection import get_mood_detector
from memory_graph import get_memory_graph
from user_profile import get_user_profile
from insights_engine import get_insights_engine
from utils.logger import get_logger

# Initialize logger
logger = get_logger("MainApp")

# Page configuration
st.set_page_config(
    page_title="LifeUnity AI - Cognitive Twin",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = get_user_profile()
if 'mood_detector' not in st.session_state:
    st.session_state.mood_detector = get_mood_detector()
if 'memory_graph' not in st.session_state:
    st.session_state.memory_graph = get_memory_graph()
if 'insights_engine' not in st.session_state:
    st.session_state.insights_engine = get_insights_engine()


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.markdown("# 🧠 LifeUnity AI")
        st.markdown("### Cognitive Twin System")
        st.markdown("---")
        
        # User info
        profile_summary = st.session_state.user_profile.get_summary()
        st.markdown(f"**User:** {profile_summary['user_id']}")
        st.markdown(f"**Tracked Emotions:** {profile_summary['total_emotions_tracked']}")
        st.markdown(f"**Memory Notes:** {profile_summary['total_notes']}")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate to:",
            ["📊 Dashboard", "😊 Mood Detection", "🧩 Cognitive Memory", "💡 AI Insights"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("### Quick Stats")
        st.metric("Stress Level", f"{profile_summary['current_stress_level']:.0f}/100")
        st.metric("Productivity", f"{profile_summary['current_productivity']:.0f}/100")
        
        return page


def render_dashboard():
    """Render the Dashboard page."""
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown("### Welcome to Your Cognitive Twin System")
    
    # Get data
    profile = st.session_state.user_profile
    profile_summary = profile.get_summary()
    emotion_history = profile.get_emotion_history(limit=10)
    insights = st.session_state.insights_engine
    memory_stats = st.session_state.memory_graph.get_graph_stats()
    
    # Top metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        stress_level = profile_summary['current_stress_level']
        stress_color = "🟢" if stress_level < 40 else "🟡" if stress_level < 70 else "🔴"
        st.metric(
            label="Current Stress",
            value=f"{stress_level:.0f}/100",
            delta=f"{stress_color}",
            delta_color="off"
        )
    
    with col2:
        productivity = profile_summary['current_productivity']
        prod_color = "🟢" if productivity >= 70 else "🟡" if productivity >= 50 else "🔴"
        st.metric(
            label="Productivity Score",
            value=f"{productivity:.0f}/100",
            delta=f"{prod_color}",
            delta_color="off"
        )
    
    with col3:
        st.metric(
            label="Tracked Emotions",
            value=profile_summary['total_emotions_tracked']
        )
    
    with col4:
        st.metric(
            label="Memory Nodes",
            value=memory_stats['total_memories']
        )
    
    st.markdown("---")
    
    # Two column layout
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.markdown("### 📈 Recent Mood Trend")
        if emotion_history:
            # Prepare data for chart
            emotions_df = pd.DataFrame(emotion_history)
            emotions_df['timestamp'] = pd.to_datetime(emotions_df['timestamp'])
            
            # Create emotion mapping for numeric representation
            emotion_map = {
                'happy': 5, 'surprise': 4, 'neutral': 3,
                'sad': 2, 'angry': 1, 'fear': 1, 'disgust': 1
            }
            emotions_df['emotion_value'] = emotions_df['emotion'].map(emotion_map)
            
            # Plot
            fig = px.line(
                emotions_df,
                x='timestamp',
                y='emotion_value',
                markers=True,
                title="Emotion Timeline (Higher = More Positive)"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            # Emotion distribution
            st.markdown("### 😊 Emotion Distribution")
            emotion_counts = emotions_df['emotion'].value_counts()
            fig_pie = px.pie(
                values=emotion_counts.values,
                names=emotion_counts.index,
                title="Recent Emotion Breakdown"
            )
            fig_pie.update_layout(height=300)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No emotion data yet. Visit the Mood Detection page to get started!")
    
    with col_right:
        st.markdown("### 🧩 Memory Graph Preview")
        st.metric("Total Memories", memory_stats['total_memories'])
        st.metric("Connections", memory_stats['total_connections'])
        st.metric("Memory Clusters", memory_stats['num_clusters'])
        
        if memory_stats['total_memories'] > 0:
            avg_connections = memory_stats['avg_connections']
            st.metric("Avg Connections", f"{avg_connections:.1f}")
            
            st.markdown("### 📝 Recent Memories")
            memories = st.session_state.memory_graph.get_all_memories()
            recent = sorted(memories, key=lambda x: x['timestamp'], reverse=True)[:3]
            
            for mem in recent:
                with st.expander(f"Memory #{mem['id']}"):
                    st.write(mem['content'][:150] + "..." if len(mem['content']) > 150 else mem['content'])
                    st.caption(f"📅 {mem['timestamp'][:10]}")
        else:
            st.info("No memories yet. Add some in the Cognitive Memory page!")


def render_mood_detection():
    """Render the Mood Detection page."""
    st.markdown('<div class="main-header">😊 Mood Detection</div>', unsafe_allow_html=True)
    st.markdown("### Emotion Detection via Image Upload")
    st.info("ℹ️ Upload a clear photo of your face for emotion analysis")
    
    detector = st.session_state.mood_detector
    profile = st.session_state.user_profile
    
    st.markdown("---")
    
    # Image upload for emotion detection
    uploaded_file = st.file_uploader(
        "Upload an image of your face",
        type=['jpg', 'jpeg', 'png'],
        help="Upload a clear photo showing your face for emotion detection"
    )
    
    if uploaded_file is not None:
        # Load and display image
        image = Image.open(uploaded_file)
        image_np = np.array(image)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(image, caption="Uploaded Image", use_column_width=True)
        
        with col2:
            with st.spinner("Analyzing emotion..."):
                result = detector.detect_emotion(image_np, return_all=True)
            
            if result['face_detected']:
                emotion = result['emotion']
                confidence = result['confidence']
                
                # Display result
                st.markdown(f"### Detected Emotion: {emotion.title()} {detector.get_emotion_emoji(emotion)}")
                st.markdown(f"**Confidence:** {confidence*100:.1f}%")
                
                # Progress bar for confidence
                st.progress(confidence)
                
                # Save to profile
                if st.button("💾 Save to Profile", key="save_emotion"):
                    profile.add_emotion_record(emotion, confidence)
                    st.success("✅ Emotion saved to your profile!")
                
                # Show all emotions
                if result.get('all_emotions'):
                    st.markdown("### All Detected Emotions")
                    emotions_data = result['all_emotions']
                    for emo, score in sorted(emotions_data.items(), key=lambda x: x[1], reverse=True):
                        st.write(f"{emo.title()}: {score*100:.1f}%")
            else:
                st.error("❌ No face detected in the image. Please upload a clearer photo with a visible face.")
    
    # Recent emotion history
    st.markdown("---")
    st.markdown("### 📊 Recent Emotion History")
    
    emotion_history = profile.get_emotion_history(limit=5)
    if emotion_history:
        for record in reversed(emotion_history):
            col1, col2, col3 = st.columns([2, 2, 3])
            with col1:
                st.write(f"{detector.get_emotion_emoji(record['emotion'])} **{record['emotion'].title()}**")
            with col2:
                st.write(f"Confidence: {record['confidence']*100:.1f}%")
            with col3:
                timestamp = datetime.fromisoformat(record['timestamp'])
                st.write(f"📅 {timestamp.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.info("No emotion history yet. Detect your first emotion above!")


def render_cognitive_memory():
    """Render the Cognitive Memory page."""
    st.markdown('<div class="main-header">🧩 Cognitive Memory</div>', unsafe_allow_html=True)
    st.markdown("### Your Personal Knowledge Graph")
    
    memory_graph = st.session_state.memory_graph
    
    # Add new memory
    st.markdown("### ➕ Add New Memory")
    
    with st.form("add_memory_form"):
        note_content = st.text_area(
            "Write your note or memory:",
            height=100,
            placeholder="Enter your thoughts, ideas, or experiences..."
        )
        
        tags_input = st.text_input(
            "Tags (comma-separated):",
            placeholder="work, personal, idea, etc."
        )
        
        submitted = st.form_submit_button("💾 Save Memory")
        
        if submitted and note_content:
            tags = [tag.strip() for tag in tags_input.split(',')] if tags_input else []
            
            with st.spinner("Processing and embedding memory..."):
                memory_id = memory_graph.add_memory(note_content, tags=tags)
            
            if memory_id > 0:
                st.success(f"✅ Memory saved! (ID: {memory_id})")
                
                # Also add to user profile
                st.session_state.user_profile.add_note(note_content, tags=tags)
            else:
                st.error("❌ Failed to save memory. Please try again.")
    
    st.markdown("---")
    
    # Memory statistics
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📊 Memory Statistics")
        stats = memory_graph.get_graph_stats()
        
        st.metric("Total Memories", stats['total_memories'])
        st.metric("Total Connections", stats['total_connections'])
        st.metric("Memory Clusters", stats['num_clusters'])
        if stats['total_memories'] > 0:
            st.metric("Avg Connections", f"{stats['avg_connections']:.2f}")
    
    with col2:
        st.markdown("### 🔍 Search Memories")
        search_query = st.text_input(
            "Search your memories:",
            placeholder="What are you looking for?"
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
                st.info("No matching memories found.")
    
    # Display all memories
    st.markdown("---")
    st.markdown("### 📚 All Memories")
    
    memories = memory_graph.get_all_memories()
    
    if memories:
        # Sort by timestamp (newest first)
        sorted_memories = sorted(memories, key=lambda x: x['timestamp'], reverse=True)
        
        for memory in sorted_memories:
            with st.expander(f"Memory #{memory['id']} - {memory['timestamp'][:10]}"):
                st.write(memory['content'])
                
                if memory.get('tags'):
                    st.write(f"🏷️ Tags: {', '.join(memory['tags'])}")
                
                # Show related memories
                related = memory_graph.get_related_memories(memory['id'])
                if related:
                    st.write(f"🔗 Connected to {len(related)} other memories")
                
                # Delete button
                if st.button(f"🗑️ Delete", key=f"del_{memory['id']}"):
                    if memory_graph.delete_memory(memory['id']):
                        st.success("Memory deleted!")
                        st.rerun()
    else:
        st.info("No memories yet. Add your first memory above!")
    
    # Memory graph visualization
    if memories and len(memories) > 1:
        st.markdown("---")
        st.markdown("### 🕸️ Memory Graph Visualization")
        
        clusters = memory_graph.get_memory_clusters()
        st.write(f"Your memories form {len(clusters)} clusters of related thoughts.")
        
        for idx, cluster in enumerate(clusters):
            st.write(f"**Cluster {idx + 1}:** {len(cluster)} memories")


def render_ai_insights():
    """Render the AI Insights page."""
    st.markdown('<div class="main-header">💡 AI Insights</div>', unsafe_allow_html=True)
    st.markdown("### Proactive Well-being Intelligence")
    
    insights_engine = st.session_state.insights_engine
    
    # Generate daily report button
    if st.button("🔄 Generate Daily Report", type="primary"):
        with st.spinner("Analyzing your data and generating insights..."):
            report = insights_engine.generate_daily_report()
            st.session_state.daily_report = report
    
    # Display report if available
    if 'daily_report' in st.session_state:
        report = st.session_state.daily_report
        
        # Header
        st.markdown(f"## 📋 Daily Report - {report['date']}")
        st.caption(f"Generated at: {report['generated_at'][:19]}")
        
        st.markdown("---")
        
        # Metrics row
        col1, col2, col3 = st.columns(3)
        
        metrics = report['metrics']
        
        with col1:
            stress = metrics['stress_level']
            stress_color = "🟢" if stress < 40 else "🟡" if stress < 70 else "🔴"
            st.metric("Stress Level", f"{stress:.0f}/100", delta=stress_color, delta_color="off")
        
        with col2:
            productivity = metrics['productivity_score']
            prod_color = "🟢" if productivity >= 70 else "🟡" if productivity >= 50 else "🔴"
            st.metric("Productivity", f"{productivity:.0f}/100", delta=prod_color, delta_color="off")
        
        with col3:
            fatigue = metrics['fatigue_risk']
            fatigue_emoji = "🟢" if fatigue == "low" else "🟡" if fatigue == "moderate" else "🔴"
            st.metric("Fatigue Risk", fatigue.title(), delta=fatigue_emoji, delta_color="off")
        
        # Alerts
        if report['alerts']:
            st.markdown("---")
            st.markdown("### ⚠️ Alerts")
            for alert in report['alerts']:
                st.markdown(f'<div class="warning-box">🚨 {alert["message"]}</div>', unsafe_allow_html=True)
        
        # Insights
        st.markdown("---")
        st.markdown("### 🧠 Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Stress Analysis")
            stress_insight = report['insights']['stress']
            st.markdown(f'<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"**Status:** {stress_insight['status']}")
            st.write(stress_insight['description'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### Productivity Analysis")
            prod_insight = report['insights']['productivity']
            st.markdown(f'<div class="insight-box">', unsafe_allow_html=True)
            st.markdown(f"**Status:** {prod_insight['status']}")
            st.write(prod_insight['description'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommendations
        st.markdown("---")
        st.markdown("### 💡 Recommendations")
        
        recommendations = report['recommendations']
        
        if recommendations:
            for rec in recommendations:
                priority_emoji = "🔴" if rec['priority'] == 'high' else "🟡" if rec['priority'] == 'medium' else "🟢"
                
                st.markdown(f'<div class="success-box">', unsafe_allow_html=True)
                st.markdown(f"### {priority_emoji} {rec['category']}")
                st.write(f"**Suggestion:** {rec['suggestion']}")
                st.write(f"**Action:** {rec['action']}")
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No specific recommendations at this time. Keep up the good work!")
    
    else:
        st.info("👆 Click 'Generate Daily Report' above to get your personalized AI insights!")
    
    # Emotion Pattern Analysis
    st.markdown("---")
    st.markdown("### 📊 Emotion Pattern Analysis")
    
    days_to_analyze = st.slider("Analyze last N days:", 1, 30, 7)
    
    if st.button("Analyze Patterns"):
        with st.spinner("Analyzing emotion patterns..."):
            patterns = insights_engine.analyze_emotion_patterns(days=days_to_analyze)
        
        st.markdown(f"### Analysis for Last {patterns.get('period_days', days_to_analyze)} Days")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Total Records", patterns.get('total_records', 0))
            st.write(f"**Overall Trend:** {patterns.get('trend', 'neutral').title()}")
            
            if patterns.get('dominant_emotions'):
                st.write("**Dominant Emotions:**")
                for emotion in patterns['dominant_emotions']:
                    st.write(f"- {emotion.title()}")
        
        with col2:
            if patterns.get('emotion_distribution'):
                st.write("**Emotion Distribution:**")
                dist = patterns['emotion_distribution']
                for emotion, count in sorted(dist.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"{emotion.title()}: {count}")
    
    # Memory Insights
    st.markdown("---")
    st.markdown("### 🧩 Memory Insights")
    
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
        st.info("No memory insights available. Add some memories in the Cognitive Memory page!")


def main():
    """Main application entry point."""
    try:
        # Render sidebar and get selected page
        page = render_sidebar()
        
        # Route to appropriate page
        if page == "📊 Dashboard":
            render_dashboard()
        elif page == "😊 Mood Detection":
            render_mood_detection()
        elif page == "🧩 Cognitive Memory":
            render_cognitive_memory()
        elif page == "💡 AI Insights":
            render_ai_insights()
    
    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        st.error("An error occurred. Please refresh the page or contact support.")
        st.exception(e)


if __name__ == "__main__":
    main()
