"""
LifeUnity AI - Cognitive Twin Dashboard
"""

import streamlit as st
from pathlib import Path
import base64


def inject_css():
    """
    Inject custom CSS for glassmorphism, glow borders, and animations.
    Creates a neon indigo cyber-futuristic theme.
    """
    custom_css = """
    <style>
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25);
        padding: 2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
        border-color: rgba(99, 102, 241, 0.5);
    }
    
    /* Glow Borders */
    .glow-border {
        position: relative;
    }
    
    .glow-border::before {
        content: '';
        position: absolute;
        inset: -2px;
        background: linear-gradient(135deg, #6366F1, #8B5CF6, #EC4899);
        border-radius: inherit;
        opacity: 0;
        z-index: -1;
        transition: opacity 0.3s ease;
    }
    
    .glow-border:hover::before {
        opacity: 0.3;
    }
    
    /* Gradient Text Animation */
    .gradient-text-animated {
        background: linear-gradient(135deg, #6366F1, #8B5CF6, #EC4899, #6366F1);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: gradientShift 4s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Hero Title Styling */
    .hero-title-large {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 50%, #A855F7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        animation: gradientText 5s ease infinite;
        background-size: 200% 200%;
    }
    
    @keyframes gradientText {
        0%, 100% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
    }
    
    /* Custom Emoji Scaling */
    .emoji-large {
        font-size: 5rem;
        filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.5));
        animation: emojiFloat 3s ease-in-out infinite;
    }
    
    @keyframes emojiFloat {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Section Headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 1rem;
        margin: 2rem 0 1.5rem;
    }
    
    .section-header-text {
        font-size: 1.3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* Smooth Hover Animations */
    .hover-lift {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .hover-lift:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(99, 102, 241, 0.3);
    }
    
    /* Navigation Bar Styling */
    .nav-bar {
        background: rgba(30, 41, 59, 0.8);
        backdrop-filter: blur(30px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 0.75rem 1.5rem;
        margin-bottom: 2rem;
    }
    
    /* Animated Confidence Bar */
    .confidence-bar {
        width: 100%;
        height: 12px;
        background: rgba(99, 102, 241, 0.2);
        border-radius: 6px;
        overflow: hidden;
        position: relative;
    }
    
    .confidence-fill {
        height: 100%;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
        border-radius: 6px;
        transition: width 1s ease-out;
        animation: confidenceGlow 2s ease-in-out infinite;
    }
    
    @keyframes confidenceGlow {
        0%, 100% { box-shadow: 0 0 10px rgba(99, 102, 241, 0.5); }
        50% { box-shadow: 0 0 20px rgba(99, 102, 241, 0.8); }
    }
    
    /* Daily Insight Card */
    .insight-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .insight-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
    }
    
    /* Memory Graph Preview */
    .memory-preview {
        background: rgba(30, 41, 59, 0.6);
        border-radius: 20px;
        border: 2px dashed rgba(99, 102, 241, 0.3);
        padding: 2rem;
        text-align: center;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    /* Onboarding Welcome Card */
    .onboarding-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 3rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .onboarding-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)


def load_global_css():
    """
    Load custom CSS for glassmorphism, animations, and neon effects.
    Creates a next-gen cyber-neon theme with smooth transitions.
    """
    # Load CSS from external file
    css_file = Path(__file__).parent / "assets" / "style.css"
    
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    
    # Inject additional inline CSS
    inject_css()
    
    # Add enhanced inline CSS for better emotion cards and insights
    st.markdown("""
    <style>
    /* Enhanced emotion card styling */
    .emotion-card {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 24px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.25);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .emotion-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 60px rgba(99, 102, 241, 0.4);
    }
    
    .emotion-emoji {
        font-size: 5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.5));
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    .emotion-label {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
    }
    
    .confidence-bar-container {
        width: 100%;
        height: 12px;
        background: rgba(99, 102, 241, 0.15);
        border-radius: 6px;
        overflow: hidden;
        margin: 1rem 0;
    }
    
    .confidence-bar {
        height: 100%;
        background: linear-gradient(90deg, #6366F1 0%, #8B5CF6 100%);
        border-radius: 6px;
        transition: width 1s ease-out;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);
    }
    
    .confidence-text {
        color: #94A3B8;
        font-size: 1.1rem;
        font-weight: 600;
    }
    
    /* AI Insights box with gradient background */
    .insights-box {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        padding: 2rem;
        margin: 1rem 0;
        position: relative;
        overflow: hidden;
    }
    
    .insights-box::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);
    }
    
    .insights-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F1F5F9;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .insights-content {
        color: #94A3B8;
        line-height: 1.8;
    }
    
    /* Memory graph placeholder */
    .memory-placeholder {
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 2px dashed rgba(99, 102, 241, 0.3);
        padding: 4rem 2rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    .memory-placeholder-icon {
        font-size: 4rem;
        opacity: 0.5;
        margin-bottom: 1rem;
    }
    
    /* Loading spinner animation */
    .loading-spinner {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        padding: 3rem;
    }
    
    .loading-dots {
        display: flex;
        gap: 8px;
    }
    
    .loading-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        animation: loadingPulse 1.4s ease-in-out infinite;
    }
    
    .loading-dot:nth-child(2) { animation-delay: 0.2s; }
    .loading-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes loadingPulse {
        0%, 100% { transform: scale(0.6); opacity: 0.5; }
        50% { transform: scale(1); opacity: 1; }
    }
    
    /* Top navigation bar enhancement */
    .top-nav {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    }
    
    .top-nav-brand {
        font-size: 1.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .top-nav-links {
        display: flex;
        gap: 1rem;
    }
    
    .top-nav-link {
        padding: 0.5rem 1rem;
        border-radius: 8px;
        color: #94A3B8;
        text-decoration: none;
        transition: all 0.3s ease;
    }
    
    .top-nav-link:hover {
        background: rgba(99, 102, 241, 0.2);
        color: #F1F5F9;
    }
    
    /* Quick Stats Row */
    .quick-stats-row {
        display: flex;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .quick-stat-item {
        flex: 1;
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 1.5rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .quick-stat-item:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.3);
    }
    
    /* Analytics Cards Grid */
    .analytics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .analytics-card {
        background: rgba(30, 41, 59, 0.7);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(99, 102, 241, 0.2);
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 50px rgba(99, 102, 241, 0.35);
        border-color: rgba(99, 102, 241, 0.4);
    }
    
    /* Status Indicators */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    .status-good {
        background: rgba(16, 185, 129, 0.2);
        color: #10B981;
    }
    
    .status-warning {
        background: rgba(245, 158, 11, 0.2);
        color: #F59E0B;
    }
    
    .status-alert {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
    }
    </style>
    """, unsafe_allow_html=True)


def top_navigation():
    """
    Render a professional top navigation bar.
    """
    nav_html = """
    <div class="top-nav">
        <span class="top-nav-brand">🧠 LifeUnity AI</span>
        <div class="top-nav-links">
            <span class="top-nav-link">📊 Dashboard</span>
            <span class="top-nav-link">😊 Emotions</span>
            <span class="top-nav-link">🧩 Memory</span>
            <span class="top-nav-link">💡 Insights</span>
        </div>
    </div>
    """
    st.markdown(nav_html, unsafe_allow_html=True)


def navbar(active_page="Dashboard"):
    """
    Animated top navigation bar with glassmorphism and hover glow effects.
    
    Args:
        active_page: Currently active page name
    """
    pages = ["Dashboard", "Emotion Detection", "Memory Graph", "Insights"]
    
    nav_html = '<div class="navbar">'
    
    for page in pages:
        active_class = "active" if page == active_page else ""
        icon = {
            "Dashboard": "📊",
            "Emotion Detection": "😊",
            "Memory Graph": "🧩",
            "Insights": "💡"
        }.get(page, "📄")
        
        nav_html += f'<span class="navbar-item {active_class}">{icon} {page}</span>'
    
    nav_html += '</div>'
    
    st.markdown(nav_html, unsafe_allow_html=True)


def emotion_card(emoji: str, emotion: str, confidence: float):
    """
    Display an enhanced emotion card with emoji and confidence bar.
    
    Args:
        emoji: Emotion emoji
        emotion: Detected emotion name
        confidence: Confidence score (0-1)
    """
    confidence_pct = int(confidence * 100)
    
    card_html = f"""
    <div class="emotion-card">
        <div class="emotion-emoji">{emoji}</div>
        <div class="emotion-label">{emotion.title()}</div>
        <div class="confidence-bar-container">
            <div class="confidence-bar" style="width: {confidence_pct}%;"></div>
        </div>
        <div class="confidence-text">Confidence: {confidence_pct}%</div>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)


def insights_box(title: str, content: str, icon: str = "💡"):
    """
    Display an AI insights box with gradient background.
    
    Args:
        title: Box title
        content: Content text
        icon: Title icon
    """
    box_html = f"""
    <div class="insights-box">
        <div class="insights-title">{icon} {title}</div>
        <div class="insights-content">{content}</div>
    </div>
    """
    
    st.markdown(box_html, unsafe_allow_html=True)


def memory_graph_placeholder():
    """
    Display a placeholder when memory graph is empty.
    """
    placeholder_html = """
    <div class="memory-placeholder">
        <div class="memory-placeholder-icon">🧩</div>
        <h3 style="color: #b8c5d0; margin-bottom: 0.5rem;">No Memories Yet</h3>
        <p style="color: #7a8a99;">Add your first memory above to start building your cognitive graph!</p>
    </div>
    """
    
    st.markdown(placeholder_html, unsafe_allow_html=True)


def loading_dots(text: str = "Processing..."):
    """
    Display animated loading dots.
    
    Args:
        text: Loading message
    """
    loading_html = f"""
    <div class="loading-spinner">
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        <p style="color: #b8c5d0; margin-top: 1rem;">{text}</p>
    </div>
    """
    
    st.markdown(loading_html, unsafe_allow_html=True)


def hero_section(title, subtitle, emoji="🧠"):
    """
    Glass morph hero banner with fade-in animation.
    Displays main title with gradient text effect.
    
    Args:
        title: Main heading text
        subtitle: Subheading text
        emoji: Large emoji for visual impact
    """
    hero_html = f"""
    <div class="hero-section">
        <div style="font-size: 5rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 20px rgba(99, 102, 241, 0.5)); animation: emojiFloat 3s ease-in-out infinite;">{emoji}</div>
        <h1 class="hero-title" style="background: linear-gradient(135deg, #6366F1, #8B5CF6, #A855F7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; font-size: 3rem; font-weight: 800; margin-bottom: 1rem;">{title}</h1>
        <p class="hero-subtitle" style="color: #94A3B8; font-size: 1.3rem; max-width: 600px; margin: 0 auto;">{subtitle}</p>
    </div>
    <style>
    @keyframes emojiFloat {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    </style>
    """
    
    st.markdown(hero_html, unsafe_allow_html=True)


def ai_avatar_section():
    """
    Circle avatar with glowing ring animation.
    Floating effect with "Ask Me Anything" speech bubble.
    """
    avatar_html = """
    <div class="ai-avatar-container">
        <div class="ai-avatar">
            🤖
        </div>
        <div class="ai-speech-bubble">
            <h3 style="margin: 0; color: #F1F5F9; font-weight: 700;">Ask Me Anything</h3>
            <p style="margin: 0.5rem 0 0 0; color: #94A3B8; font-size: 0.95rem;">
                Your AI Twin is ready to assist you
            </p>
        </div>
    </div>
    """
    
    st.markdown(avatar_html, unsafe_allow_html=True)


def dashboard_card(icon, title, value, description, col=None):
    """
    Single dashboard card with animated hover lift and gradient highlights.
    
    Args:
        icon: Emoji or icon
        title: Card title
        value: Main metric value
        description: Short description
        col: Streamlit column to render in (optional)
    """
    card_html = f"""
    <div class="dashboard-card">
        <div class="card-icon" style="font-size: 3rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 15px rgba(99, 102, 241, 0.5));">{icon}</div>
        <div class="card-title" style="font-size: 1rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.75rem;">{title}</div>
        <div class="card-value" style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin-bottom: 0.5rem;">{value}</div>
        <div class="card-description" style="font-size: 0.9rem; color: #64748B;">{description}</div>
    </div>
    """
    
    if col:
        col.markdown(card_html, unsafe_allow_html=True)
    else:
        st.markdown(card_html, unsafe_allow_html=True)


def dashboard_cards(cards_data):
    """
    Responsive grid of 3-4 dashboard cards with animations.
    
    Args:
        cards_data: List of dicts with keys: icon, title, value, description
        
    Example:
        cards_data = [
            {"icon": "😊", "title": "Mood Score", "value": "85%", "description": "Positive"},
            {"icon": "🧠", "title": "Memory Nodes", "value": "42", "description": "Active"},
            {"icon": "💡", "title": "Insights", "value": "12", "description": "Generated"},
        ]
    """
    num_cards = len(cards_data)
    cols = st.columns(num_cards if num_cards <= 4 else 4)
    
    for idx, card in enumerate(cards_data):
        col_idx = idx % len(cols)
        dashboard_card(
            icon=card.get("icon", "📊"),
            title=card.get("title", "Metric"),
            value=card.get("value", "0"),
            description=card.get("description", ""),
            col=cols[col_idx]
        )


def glass_container(content_func, padding="2rem"):
    """
    Wraps content in a glassmorphism container.
    
    Args:
        content_func: Function that renders content inside
        padding: CSS padding value
    """
    st.markdown(f'<div class="glass-card" style="padding: {padding};">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)


def metric_card(label, value, delta=None, delta_color="normal"):
    """
    Enhanced metric card with glassmorphism styling.
    
    Args:
        label: Metric label
        value: Metric value
        delta: Change indicator (optional)
        delta_color: Color of delta (normal, inverse, off)
    """
    st.metric(label=label, value=value, delta=delta, delta_color=delta_color)


def footer():
    """
    Glass footer with credits and social icons.
    Smooth pulse animation effect - Sticky footer.
    """
    footer_html = """
    <style>
        .sticky-footer {
            position: relative;
            margin-top: 4rem;
            padding-bottom: 2rem;
        }
        .sticky-footer .footer {
            background: linear-gradient(135deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 41, 59, 0.95) 100%);
            backdrop-filter: blur(30px);
            -webkit-backdrop-filter: blur(30px);
            border-radius: 24px 24px 0 0;
            border: 1px solid rgba(99, 102, 241, 0.2);
            border-bottom: none;
            padding: 2.5rem;
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        .sticky-footer .footer::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899, #6366F1);
            background-size: 300% 100%;
            animation: gradientMove 3s linear infinite;
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            100% { background-position: 300% 50%; }
        }
    </style>
    <div class="sticky-footer">
        <div class="footer">
            <div style="margin-bottom: 1.5rem;">
                <span style="font-size: 2.5rem; filter: drop-shadow(0 4px 15px rgba(99, 102, 241, 0.5));">🧠</span>
            </div>
            <p class="footer-text" style="color: #94A3B8; font-size: 1rem; margin-bottom: 0.5rem;">
                ✨ Powered by <strong style="background: linear-gradient(135deg, #6366F1, #8B5CF6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">LifeUnity AI</strong> - Cognitive Twin System
            </p>
            <hr style="border: none; height: 1px; background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent); margin: 1.5rem 0;">
            <p class="footer-text" style="font-size: 1.1rem; color: #F1F5F9; font-weight: 700; margin-bottom: 0.5rem;">
                Built by Ravi Gohel • Hack4Unity 2025
            </p>
            <p class="footer-text" style="font-size: 0.9rem; color: #8B5CF6; margin-bottom: 1rem;">
                Empowering humanity with AI-based cognitive wellness.
            </p>
            <p class="footer-text" style="font-size: 0.75rem; color: #64748B;">
                © 2025 LifeUnity AI | All Rights Reserved
            </p>
            <div class="footer-links" style="display: flex; justify-content: center; gap: 1.5rem; margin-top: 1.5rem;">
                <a href="https://github.com/GohelR" class="footer-link" title="GitHub" style="color: #94A3B8; text-decoration: none; font-size: 1.3rem; display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(51, 65, 85, 0.5); border: 1px solid rgba(99, 102, 241, 0.2); transition: all 0.3s ease;">🐙</a>
                <a href="https://portfolioravigohel.netlify.app/" class="footer-link" title="Portfolio" style="color: #94A3B8; text-decoration: none; font-size: 1.3rem; display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(51, 65, 85, 0.5); border: 1px solid rgba(99, 102, 241, 0.2); transition: all 0.3s ease;">🐦</a>
                <a href="https://www.linkedin.com/in/ravi-gohel-733172245/" class="footer-link" title="LinkedIn" style="color: #94A3B8; text-decoration: none; font-size: 1.3rem; display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(51, 65, 85, 0.5); border: 1px solid rgba(99, 102, 241, 0.2); transition: all 0.3s ease;">💼</a>
                <a href="https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin" class="footer-link" title="This project code" style="color: #94A3B8; text-decoration: none; font-size: 1.3rem; display: inline-flex; align-items: center; justify-content: center; width: 44px; height: 44px; border-radius: 12px; background: rgba(51, 65, 85, 0.5); border: 1px solid rgba(99, 102, 241, 0.2); transition: all 0.3s ease;">🌐</a>
            </div>
        </div>
    </div>
    """
    
    st.markdown(footer_html, unsafe_allow_html=True)


def page_transition():
    """
    Adds page transition animation effect.
    Call at the start of each page render.
    """
    st.markdown('<div class="page-transition">', unsafe_allow_html=True)


def section_divider():
    """
    Animated section divider with gradient.
    """
    st.markdown("""
    <div style="height: 2px; background: linear-gradient(90deg, transparent, #6366F1, #8B5CF6, transparent); 
                margin: 3rem 0; border-radius: 2px; animation: shimmer 2s infinite;"></div>
    """, unsafe_allow_html=True)


def info_box(text, box_type="info"):
    """
    Styled information box with glassmorphism.
    
    Args:
        text: Message to display
        box_type: Type of box (info, success, warning, error)
    """
    colors = {
        "info": "#6366F1",
        "success": "#10B981",
        "warning": "#F59E0B",
        "error": "#EF4444"
    }
    
    bg_colors = {
        "info": "rgba(99, 102, 241, 0.1)",
        "success": "rgba(16, 185, 129, 0.1)",
        "warning": "rgba(245, 158, 11, 0.1)",
        "error": "rgba(239, 68, 68, 0.1)"
    }
    
    color = colors.get(box_type, colors["info"])
    bg_color = bg_colors.get(box_type, bg_colors["info"])
    
    box_html = f"""
    <div style="background: {bg_color}; backdrop-filter: blur(20px);
                border-radius: 14px; border-left: 4px solid {color};
                padding: 1rem 1.5rem; margin: 1rem 0;">
        <p style="margin: 0; color: #F1F5F9; line-height: 1.6;">{text}</p>
    </div>
    """
    
    st.markdown(box_html, unsafe_allow_html=True)


def gradient_text(text, size="2rem"):
    """
    Display text with gradient effect.
    
    Args:
        text: Text to display
        size: Font size
    """
    st.markdown(f"""
    <h2 style="font-size: {size}; font-weight: 800; 
                background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%);
                -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                background-clip: text; margin: 1rem 0;">
        {text}
    </h2>
    """, unsafe_allow_html=True)


def loading_animation(text="Loading..."):
    """
    Show loading animation with pulsing effect.
    
    Args:
        text: Loading message
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem;">
        <div style="font-size: 4rem; animation: pulse 1.5s ease-in-out infinite;">⚡</div>
        <p style="color: #94A3B8; margin-top: 1rem; animation: pulse 1.5s ease-in-out infinite;">{text}</p>
    </div>
    <style>
    @keyframes pulse {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.7; transform: scale(1.05); }}
    }}
    </style>
    """, unsafe_allow_html=True)


def stats_row(stats):
    """
    Display a row of statistics with animated cards.
    
    Args:
        stats: List of tuples (label, value)
        
    Example:
        stats = [("Total Users", "1,234"), ("Active Sessions", "56"), ("Uptime", "99.9%")]
    """
    cols = st.columns(len(stats))
    
    for idx, (label, value) in enumerate(stats):
        with cols[idx]:
            metric_card(label, value)


def progress_ring(percentage, label="Progress"):
    """
    Circular progress indicator with gradient.
    
    Args:
        percentage: Progress value (0-100)
        label: Progress label
    """
    # Use Streamlit's native progress for simplicity
    st.markdown(f"<p style='color: #94A3B8; margin-bottom: 0.5rem; font-weight: 500;'>{label}</p>", unsafe_allow_html=True)
    st.progress(percentage / 100)
    st.markdown(f"<p style='text-align: right; color: #6366F1; font-weight: 700;'>{percentage}%</p>", unsafe_allow_html=True)


def create_tabs(tab_names):
    """
    Create styled tabs with glassmorphism.
    
    Args:
        tab_names: List of tab names
        
    Returns:
        Streamlit tabs object
    """
    return st.tabs([f"✨ {name}" for name in tab_names])


def image_with_glass_border(image_source, caption=None):
    """
    Display image with glassmorphism border.
    
    Args:
        image_source: Image file path or PIL Image
        caption: Optional caption
    """
    st.markdown('<div class="glass-card" style="padding: 1rem;">', unsafe_allow_html=True)
    st.image(image_source, caption=caption, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)


def animated_button(label, key=None, button_type="primary"):
    """
    Create an animated button with hover effects.
    
    Args:
        label: Button text
        key: Unique key for button
        button_type: primary or secondary
        
    Returns:
        Boolean indicating if button was clicked
    """
    if button_type == "primary":
        return st.button(label, key=key, type="primary")
    else:
        return st.button(label, key=key)


# ========================================================================
# HELPER FUNCTIONS FOR SPECIFIC PAGES
# ========================================================================

def render_welcome_banner():
    """Renders the main welcome banner for the dashboard."""
    hero_section(
        title="LifeUnity AI - Cognitive Twin",
        subtitle="Your Personal AI-Powered Mental Health & Productivity Companion",
        emoji="🧠"
    )


def render_empty_state(icon, title, message):
    """
    Render an empty state placeholder.
    
    Args:
        icon: Large emoji
        title: Empty state title
        message: Descriptive message
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 4rem 2rem;">
        <div style="font-size: 5rem; opacity: 0.4; margin-bottom: 1rem; animation: floatAnimation 4s ease-in-out infinite;">{icon}</div>
        <h3 style="color: #94A3B8; margin-bottom: 0.5rem; font-weight: 600;">{title}</h3>
        <p style="color: #64748B; max-width: 400px; margin: 0 auto;">{message}</p>
    </div>
    <style>
    @keyframes floatAnimation {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-10px); }}
    }}
    </style>
    """, unsafe_allow_html=True)


def render_onboarding_message():
    """
    Render an onboarding welcome message for first-time users.
    """
    onboarding_html = """
    <div class="onboarding-card" style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.15) 0%, rgba(139, 92, 246, 0.15) 100%); backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(99, 102, 241, 0.2); padding: 3rem; text-align: center; margin: 2rem 0; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);"></div>
        <div style="font-size: 4rem; margin-bottom: 1.5rem;">👋</div>
        <h2 style="color: #F1F5F9; font-weight: 700; margin-bottom: 1rem; font-size: 1.8rem;">Welcome to LifeUnity AI!</h2>
        <p style="color: #94A3B8; max-width: 500px; margin: 0 auto 1.5rem; line-height: 1.7;">
            Your personal AI-powered Cognitive Twin is here to help you track emotions, 
            manage cognitive memories, and gain proactive insights for better well-being.
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap; margin-top: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">😊</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">Track Emotions</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧩</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">Build Memory</p>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 0.5rem;">💡</div>
                <p style="color: #94A3B8; font-size: 0.9rem;">Get Insights</p>
            </div>
        </div>
    </div>
    """
    st.markdown(onboarding_html, unsafe_allow_html=True)


def render_daily_insight_card(title, content, icon="💡"):
    """
    Render a daily AI insight card with gradient background.
    
    Args:
        title: Card title
        content: Insight content (should be pre-sanitized or contain trusted HTML)
        icon: Title icon
    """
    # For trusted internal content that may contain safe HTML tags like <strong>, <em>, <br>
    # The content is generated internally and not from user input
    
    insight_html = f"""
    <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(99, 102, 241, 0.3); padding: 2rem; position: relative; overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899);"></div>
        <div style="font-size: 1.3rem; font-weight: 700; color: #F1F5F9; margin-bottom: 1rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">{icon}</span> {title}
        </div>
        <div style="color: #94A3B8; line-height: 1.7;">
            {content}
        </div>
    </div>
    """
    st.markdown(insight_html, unsafe_allow_html=True)


def render_memory_preview_card(memory_count, connection_count):
    """
    Render a memory graph preview card.
    
    Args:
        memory_count: Number of memories
        connection_count: Number of connections
    """
    preview_html = f"""
    <div class="memory-preview" style="background: rgba(30, 41, 59, 0.6); border-radius: 20px; border: 2px dashed rgba(99, 102, 241, 0.3); padding: 2rem; text-align: center; min-height: 200px; display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="font-size: 3rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 15px rgba(99, 102, 241, 0.5));">🧩</div>
        <h3 style="color: #F1F5F9; margin-bottom: 0.5rem; font-weight: 600;">Memory Graph</h3>
        <p style="color: #94A3B8; margin-bottom: 1.5rem;">Your cognitive knowledge network</p>
        <div style="display: flex; gap: 2rem; justify-content: center;">
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{memory_count}</div>
                <div style="color: #64748B; font-size: 0.85rem;">Memories</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #6366F1 0%, #8B5CF6 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{connection_count}</div>
                <div style="color: #64748B; font-size: 0.85rem;">Connections</div>
            </div>
        </div>
    </div>
    """
    st.markdown(preview_html, unsafe_allow_html=True)


def render_animated_confidence_bar(percentage, label="Confidence"):
    """
    Render an animated confidence bar.
    
    Args:
        percentage: Confidence value (0-100)
        label: Bar label
    """
    bar_html = f"""
    <div style="margin: 1.5rem 0;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style="color: #94A3B8; font-weight: 500;">{label}</span>
            <span style="color: #6366F1; font-weight: 700;">{percentage}%</span>
        </div>
        <div class="confidence-bar" style="width: 100%; height: 12px; background: rgba(99, 102, 241, 0.15); border-radius: 6px; overflow: hidden; position: relative;">
            <div class="confidence-fill" style="width: {percentage}%; height: 100%; background: linear-gradient(90deg, #6366F1, #8B5CF6, #EC4899); border-radius: 6px; transition: width 1s ease-out; box-shadow: 0 0 15px rgba(99, 102, 241, 0.5);"></div>
        </div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)


def render_status_indicator(status, text):
    """
    Render a status indicator badge.
    
    Args:
        status: Status type (good, warning, alert)
        text: Status text
    """
    status_colors = {
        "good": ("#10B981", "rgba(16, 185, 129, 0.2)"),
        "warning": ("#F59E0B", "rgba(245, 158, 11, 0.2)"),
        "alert": ("#EF4444", "rgba(239, 68, 68, 0.2)")
    }
    
    color, bg = status_colors.get(status, status_colors["good"])
    
    indicator_html = f"""
    <span style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; background: {bg}; color: {color};">
        <span style="width: 8px; height: 8px; border-radius: 50%; background: {color};"></span>
        {text}
    </span>
    """
# ---- FIX CLICKABLE LINKS (Glassmorphism z-index bug) ----
st.markdown("""
<style>
/* Force footer links to become clickable above blur/glass layers */
.footer-link {
    position: relative !important;
    z-index: 999999 !important;
    pointer-events: auto !important;
}

/* Fix invisible overlay blocking clicks */
.stApp {
    position: relative;
    z-index: 0;
}
.stApp > div {
    position: relative;
    z-index: 0;
}

/* Remove overlay from footer container */
.sticky-footer, .footer {
    overflow: visible !important;
}

/* Fix global overlay that Streamlit adds */
.block-container {
    position: relative !important;
    z-index: 0 !important;
}

/* Fix emoji buttons from catching clicks */
button, .stButton button {
    z-index: 1000000 !important;
}

/* Fix ANY accidental invisible floating div */
div[style*="position: absolute"] {
    pointer-events: none !important;
}
</style>
""", unsafe_allow_html=True)
