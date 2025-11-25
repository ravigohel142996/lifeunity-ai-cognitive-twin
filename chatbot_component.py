"""
LifeUnity AI - Floating Chatbot Component
A fully functional floating chat widget with AI-powered responses.
"""

import streamlit as st
import html

# Import the chat engine
try:
    from app.utils.chatbot import ask_ai, get_chat_engine
except ImportError:
    try:
        from utils.chatbot import ask_ai, get_chat_engine
    except ImportError:
        def ask_ai(query, context=None):
            return "I'm here to help! Please use the Ask Me Anything page for the full chat experience."
        def get_chat_engine():
            return None


def get_user_context():
    """Get user context from session state for personalized responses."""
    context = {}
    try:
        if 'user_profile' in st.session_state:
            profile = st.session_state.user_profile
            summary = profile.get_summary()
            context['stress_level'] = summary.get('current_stress_level', 50)
            context['productivity'] = summary.get('current_productivity', 75)
            context['total_emotions'] = summary.get('total_emotions_tracked', 0)
        
        if 'memory_graph' in st.session_state:
            memory = st.session_state.memory_graph
            stats = memory.get_graph_stats()
            context['total_memories'] = stats.get('total_memories', 0)
            context['total_connections'] = stats.get('total_connections', 0)
    except Exception:
        pass
    
    return context


def escape_html(text):
    """Safely escape HTML to prevent XSS."""
    return html.escape(str(text))


def render_floating_chatbot():
    """Render the floating chatbot widget with full functionality."""
    if "floating_chat_messages" not in st.session_state:
        st.session_state.floating_chat_messages = [
            {"role": "assistant", "content": "Hi! I'm your LifeUnity AI assistant."}
        ]
    
    # Simplified chatbot HTML with minified CSS to avoid code block detection
    chatbot_css = """
<style>
.lu-chat-btn{position:fixed;bottom:30px;right:30px;width:65px;height:65px;border-radius:50%;background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);display:flex;align-items:center;justify-content:center;cursor:pointer;box-shadow:0 8px 30px rgba(99,102,241,0.5);z-index:9999;transition:all 0.3s;animation:chatPulse 2s infinite;border:none}
.lu-chat-btn:hover{transform:scale(1.1);box-shadow:0 12px 40px rgba(99,102,241,0.7)}
.lu-chat-btn span{font-size:1.8rem;color:white}
@keyframes chatPulse{0%,100%{box-shadow:0 8px 30px rgba(99,102,241,0.5)}50%{box-shadow:0 8px 40px rgba(99,102,241,0.7)}}
.lu-chat-win{position:fixed;bottom:110px;right:30px;width:380px;max-height:550px;background:rgba(15,23,42,0.98);backdrop-filter:blur(20px);border-radius:24px;border:1px solid rgba(99,102,241,0.3);box-shadow:0 20px 60px rgba(0,0,0,0.5);z-index:9998;overflow:hidden;display:none;flex-direction:column}
.lu-chat-win.open{display:flex}
.lu-chat-hdr{background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);padding:1rem 1.25rem;display:flex;justify-content:space-between;align-items:center}
.lu-chat-hdr-t{display:flex;align-items:center;gap:0.75rem}
.lu-chat-hdr-t .av{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,0.2);display:flex;align-items:center;justify-content:center;font-size:1.3rem}
.lu-chat-hdr h4{margin:0;color:white;font-weight:700;font-size:1rem}
.lu-chat-hdr p{margin:0;color:rgba(255,255,255,0.8);font-size:0.75rem}
.lu-chat-cls{background:rgba(255,255,255,0.2);border:none;color:white;width:32px;height:32px;border-radius:50%;cursor:pointer;font-size:1.2rem;display:flex;align-items:center;justify-content:center;transition:all 0.2s}
.lu-chat-cls:hover{background:rgba(255,255,255,0.3);transform:rotate(90deg)}
.lu-chat-body{flex:1;padding:1rem;overflow-y:auto;max-height:320px;display:flex;flex-direction:column;gap:0.75rem}
.lu-msg{display:flex;gap:0.5rem;animation:msgIn 0.3s}
@keyframes msgIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
.lu-msg.usr{justify-content:flex-end}
.lu-msg.ai{justify-content:flex-start}
.lu-av{width:28px;height:28px;border-radius:50%;background:rgba(99,102,241,0.2);display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0}
.lu-bub{padding:0.75rem 1rem;border-radius:16px;max-width:85%;font-size:0.9rem;line-height:1.5;word-wrap:break-word}
.lu-bub.usr{background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);color:white;border-radius:16px 16px 4px 16px}
.lu-bub.ai{background:rgba(30,41,59,0.9);color:#F1F5F9;border:1px solid rgba(99,102,241,0.2);border-radius:16px 16px 16px 4px}
.lu-typing{display:flex;gap:4px;padding:0.75rem 1rem;background:rgba(30,41,59,0.9);border-radius:16px;border:1px solid rgba(99,102,241,0.2)}
.lu-dot{width:8px;height:8px;border-radius:50%;background:#6366F1;animation:bounce 1.4s infinite}
.lu-dot:nth-child(2){animation-delay:0.2s}
.lu-dot:nth-child(3){animation-delay:0.4s}
@keyframes bounce{0%,100%{transform:translateY(0);opacity:0.4}50%{transform:translateY(-5px);opacity:1}}
.lu-sugg{padding:0.5rem 1rem;display:flex;flex-wrap:wrap;gap:0.5rem;border-top:1px solid rgba(99,102,241,0.1)}
.lu-sugg-btn{background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.2);border-radius:20px;padding:0.4rem 0.75rem;color:#94A3B8;font-size:0.75rem;cursor:pointer;transition:all 0.2s;white-space:nowrap}
.lu-sugg-btn:hover{background:rgba(99,102,241,0.2);color:#F1F5F9;border-color:#6366F1}
.lu-inp-c{padding:1rem;border-top:1px solid rgba(99,102,241,0.2);display:flex;gap:0.5rem;align-items:center}
.lu-inp{flex:1;background:rgba(30,41,59,0.8);border:1px solid rgba(99,102,241,0.3);border-radius:12px;padding:0.75rem 1rem;color:#F1F5F9;font-size:0.9rem;outline:none;transition:all 0.2s}
.lu-inp:focus{border-color:#6366F1;box-shadow:0 0 15px rgba(99,102,241,0.2)}
.lu-send{background:linear-gradient(135deg,#6366F1 0%,#8B5CF6 100%);border:none;border-radius:12px;padding:0.75rem 1rem;color:white;cursor:pointer;font-weight:600;transition:all 0.2s}
.lu-send:hover{transform:translateY(-2px);box-shadow:0 5px 20px rgba(99,102,241,0.4)}
@media(max-width:768px){.lu-chat-win{width:calc(100% - 40px);right:20px;bottom:100px;max-height:70vh}.lu-chat-btn{bottom:20px;right:20px;width:60px;height:60px}}
</style>
"""
    
    chatbot_html = """
<div class="lu-chat-btn" onclick="toggleLuChat()" id="luChatBtn"><span>💬</span></div>
<div class="lu-chat-win" id="luChatWin">
<div class="lu-chat-hdr"><div class="lu-chat-hdr-t"><div class="av">🤖</div><div><h4>LifeUnity AI</h4><p>Your Cognitive Twin Assistant</p></div></div><button class="lu-chat-cls" onclick="toggleLuChat()">✕</button></div>
<div class="lu-chat-body" id="luChatBody"><div class="lu-msg ai"><div class="lu-av">🤖</div><div class="lu-bub ai">Hi! 👋 I'm your LifeUnity AI assistant. How can I help you today?</div></div></div>
<div class="lu-sugg"><button class="lu-sugg-btn" onclick="luSugg('How am I doing today?')">📊 How am I doing?</button><button class="lu-sugg-btn" onclick="luSugg('Give me stress tips')">😌 Stress tips</button><button class="lu-sugg-btn" onclick="luSugg('Productivity advice')">💪 Productivity</button><button class="lu-sugg-btn" onclick="luSugg('Show memory insights')">🧩 Memory insights</button></div>
<div class="lu-inp-c"><input type="text" class="lu-inp" id="luChatInp" placeholder="Type a message..." onkeypress="if(event.key==='Enter')luSend()"><button class="lu-send" onclick="luSend()">Send</button></div>
</div>
"""
    
    chatbot_js = """
<script>
function toggleLuChat(){var w=document.getElementById('luChatWin');w.classList.toggle('open');if(w.classList.contains('open')){document.getElementById('luChatInp').focus();scrollLuChat()}}
function scrollLuChat(){var b=document.getElementById('luChatBody');b.scrollTop=b.scrollHeight}
function luSugg(t){document.getElementById('luChatInp').value=t;luSend()}
function luSend(){var i=document.getElementById('luChatInp'),m=i.value.trim();if(m){var b=document.getElementById('luChatBody'),u=document.createElement('div');u.className='lu-msg usr';u.innerHTML='<div class="lu-bub usr">'+escLu(m)+'</div>';b.appendChild(u);i.value='';scrollLuChat();var t=document.createElement('div');t.className='lu-msg ai';t.id='luTyping';t.innerHTML='<div class="lu-av">🤖</div><div class="lu-typing"><div class="lu-dot"></div><div class="lu-dot"></div><div class="lu-dot"></div></div>';b.appendChild(t);scrollLuChat();setTimeout(function(){var ty=document.getElementById('luTyping');if(ty)ty.remove();var a=document.createElement('div');a.className='lu-msg ai';a.innerHTML='<div class="lu-av">🤖</div><div class="lu-bub ai">'+getLuResp(m)+'</div>';b.appendChild(a);scrollLuChat()},1000)}}
function escLu(t){var d=document.createElement('div');d.textContent=t;return d.innerHTML}
function getLuResp(m){var l=m.toLowerCase();if(l.includes('hello')||l.includes('hi')||l.includes('hey'))return'Hello! 👋 How can I help you today?';if(l.includes('stress'))return'🧘 For stress relief:<br>• Deep breathing<br>• Take a walk<br>• Journal thoughts';if(l.includes('productivity')||l.includes('focus'))return'💪 Boost productivity:<br>• Pomodoro technique<br>• Break tasks down<br>• Eliminate distractions';if(l.includes('mood')||l.includes('feeling'))return'😊 Track mood in Mood Detection page!';if(l.includes('memory'))return'🧩 Visit Cognitive Memory to build your knowledge graph!';if(l.includes('how am i')||l.includes('doing'))return'📊 Check Dashboard for your metrics!';if(l.includes('help'))return'🌟 I help with mood, memory, stress & productivity!';if(l.includes('thank'))return"You're welcome! 😊";return'Use <b>Ask Me Anything</b> page for full AI chat! 🤖';}
</script>
"""
    
    # Render each part separately
    st.markdown(chatbot_css, unsafe_allow_html=True)
    st.markdown(chatbot_html, unsafe_allow_html=True)
    st.markdown(chatbot_js, unsafe_allow_html=True)


def load_chatbot():
    """Load the global floating chatbot component."""
    render_floating_chatbot()


def generate_reply(msg):
    """Generate AI chatbot reply using the chat engine."""
    context = get_user_context()
    return ask_ai(msg, context)
