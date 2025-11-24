"""
LifeUnity AI - Cognitive Twin Dashboard
World-Class Professional UI Components
Studio-Grade Design System
"""

import streamlit as st
from pathlib import Path
import base64


def load_global_css():
    """
    Load custom CSS for glassmorphism, animations, and neon effects.
    Creates a next-gen cyber-neon theme with smooth transitions.
    """
    css_file = Path(__file__).parent / "assets" / "style.css"
    
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    else:
        # Fallback minimal CSS if file not found
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #1e1e2e 0%, #2a2a3e 50%, #1e1e2e 100%);
        }
        </style>
        """, unsafe_allow_html=True)


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
        <div style="font-size: 5rem; margin-bottom: 1rem;">{emoji}</div>
        <h1 class="hero-title">{title}</h1>
        <p class="hero-subtitle">{subtitle}</p>
    </div>
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
            <h3 style="margin: 0; color: #fff;">Ask Me Anything</h3>
            <p style="margin: 0.5rem 0 0 0; color: #b8c5d0; font-size: 0.95rem;">
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
        <div class="card-icon">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-value">{value}</div>
        <div class="card-description">{description}</div>
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
    Smooth pulse animation effect.
    """
    footer_html = """
    <div class="footer">
        <p class="footer-text">
            ✨ Powered by <strong>LifeUnity AI</strong> - Cognitive Twin System
        </p>
        <p class="footer-text" style="font-size: 0.85rem; margin-top: 0.5rem;">
            © 2025 LifeUnity AI | MU IDEA 2025 | Hack4Unity Winner
        </p>
        <div class="footer-links">
            <a href="#" class="footer-link" title="GitHub">🐙</a>
            <a href="#" class="footer-link" title="Twitter">🐦</a>
            <a href="#" class="footer-link" title="LinkedIn">💼</a>
            <a href="#" class="footer-link" title="Website">🌐</a>
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
    <div style="height: 2px; background: linear-gradient(90deg, transparent, #667eea, #764ba2, transparent); 
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
        "info": "#00d4ff",
        "success": "#00ff88",
        "warning": "#ffaa00",
        "error": "#ff4466"
    }
    
    color = colors.get(box_type, colors["info"])
    
    box_html = f"""
    <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(20px);
                border-radius: 12px; border-left: 4px solid {color};
                padding: 1rem 1.5rem; margin: 1rem 0;">
        <p style="margin: 0; color: #ffffff;">{text}</p>
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
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
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
        <p style="color: #b8c5d0; margin-top: 1rem; animation: pulse 1.5s ease-in-out infinite;">{text}</p>
    </div>
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
    st.markdown(f"<p style='color: #b8c5d0; margin-bottom: 0.5rem;'>{label}</p>", unsafe_allow_html=True)
    st.progress(percentage / 100)
    st.markdown(f"<p style='text-align: right; color: #667eea; font-weight: 600;'>{percentage}%</p>", unsafe_allow_html=True)


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
        <div style="font-size: 5rem; opacity: 0.5; margin-bottom: 1rem;">{icon}</div>
        <h3 style="color: #b8c5d0; margin-bottom: 0.5rem;">{title}</h3>
        <p style="color: #7a8a99;">{message}</p>
    </div>
    """, unsafe_allow_html=True)
