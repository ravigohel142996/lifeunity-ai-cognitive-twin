"""
LifeUnity AI - Chatbot Engine
Rule-based AI chat engine with context-aware responses.
Supports OpenAI API integration as optional enhancement.
"""

import os
import random
from typing import Optional

# Try to import OpenAI for optional LLM support
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class ChatEngine:
    """
    AI Chatbot engine for LifeUnity Cognitive Twin.
    Uses rule-based responses with optional OpenAI fallback.
    """
    
    def __init__(self):
        """Initialize the chat engine with response templates."""
        self.context = {}
        
        # Greeting responses
        self.greetings = [
            "Hello! 👋 I'm your LifeUnity AI Cognitive Twin. How can I help you today?",
            "Hi there! 😊 Welcome to LifeUnity AI. What would you like to explore?",
            "Hey! 🌟 Great to see you. I'm here to help with your cognitive wellness journey.",
        ]
        
        # Stress-related responses
        self.stress_responses = [
            "I understand stress can be challenging. Here are some tips:\n\n🧘 **Deep Breathing**: Try 4-7-8 breathing - inhale 4s, hold 7s, exhale 8s.\n\n🚶 **Take a Break**: A short walk can help reduce stress hormones.\n\n💭 **Journal**: Writing down thoughts can provide clarity.",
            "Stress management is important for your well-being. Consider:\n\n☕ **Stay Hydrated**: Reduce caffeine and drink more water.\n\n🎵 **Calming Music**: Listen to nature sounds or soft music.\n\n⏰ **Prioritize Tasks**: Focus on what's most important first.",
        ]
        
        # Productivity responses
        self.productivity_responses = [
            "Let's boost your productivity! 🚀\n\n**Try these strategies:**\n• Break large tasks into smaller chunks\n• Use the Pomodoro technique (25 min work, 5 min break)\n• Eliminate distractions (phone on silent)\n• Set specific goals for each hour",
            "To improve productivity: 💪\n\n• **Morning Routine**: Start with your most important task\n• **Time Blocking**: Schedule focused work periods\n• **Regular Breaks**: Short breaks boost concentration\n• **Track Progress**: Celebrate small wins!",
        ]
        
        # Mood-related responses
        self.mood_responses = [
            "I can help you understand your emotions better! 😊\n\n**Here's how:**\n• Go to **Mood Detection** to analyze your emotional state\n• Check **AI Insights** for patterns in your well-being\n• Track emotions over time to identify triggers\n\nHow are you feeling right now?",
            "Emotions are an important part of wellness! 💜\n\n• Use the **photo analysis** feature to detect your mood\n• Review your **emotion history** for patterns\n• **Regular tracking** helps with self-awareness\n\nWould you like to track your current mood?",
        ]
        
        # Memory-related responses
        self.memory_responses = [
            "Your cognitive memory graph helps organize thoughts! 🧩\n\n**Tips for better memory management:**\n• Add notes regularly to build your knowledge graph\n• Use tags to organize memories by topic\n• Search memories to find related thoughts\n\nWant to add a new memory?",
            "The Memory Graph is your personal knowledge base! 📚\n\n• Store important thoughts and ideas\n• Connect related concepts automatically\n• Search across all your memories\n• Build a cognitive profile over time",
        ]
        
        # Help responses
        self.help_responses = [
            "I'm your AI-powered Cognitive Twin! Here's what I can do: 🌟\n\n**🏠 Dashboard** - View overall wellness metrics\n**😊 Mood Detection** - Analyze emotions from photos\n**🧩 Cognitive Memory** - Build your knowledge graph\n**💡 AI Insights** - Get personalized recommendations\n**💬 Chat** - Talk to me anytime!\n\nJust ask about stress, productivity, emotions, or well-being!",
        ]
        
        # Thank you responses
        self.thank_responses = [
            "You're welcome! 😊 I'm always here to help.\n\nRemember: Taking care of your mental health is a strength! Keep tracking, keep growing! 💜",
            "Happy to help! 🌟 Feel free to ask me anything else.\n\nYour wellness journey matters. I'm here for you! 💙",
        ]
        
        # Today/how am I doing responses
        self.today_responses = [
            "Based on your profile, here's your current status:\n\n📊 **Stress Level**: {stress}%\n💪 **Productivity**: {productivity}%\n🧠 **Memories**: {memories}\n\nWould you like specific tips to improve any area?",
        ]
        
        # Insight responses
        self.insight_responses = [
            "Here are some insights from your data! 💡\n\n• Your memory graph shows **{connections}** connections\n• **Regular tracking** helps identify patterns\n• Consider generating a **Daily Report** for detailed analysis\n\nGo to AI Insights for a comprehensive report!",
        ]
        
        # Default responses
        self.default_responses = [
            "Thanks for your message! 🤖 I can help with:\n\n• **Emotional wellness** - Track and understand your moods\n• **Productivity** - Optimize your work patterns\n• **Memory** - Build your personal knowledge graph\n• **Insights** - Get AI-powered recommendations\n\nTry asking about stress management or productivity tips!",
            "I'm here to help! 😊\n\n**Quick suggestions:**\n• \"How am I doing today?\"\n• \"Give me stress management tips\"\n• \"How can I be more productive?\"\n• \"Explain my mood patterns\"\n\nWhat would you like to know?",
        ]
    
    def set_context(self, key: str, value):
        """Set context data for personalized responses."""
        self.context[key] = value
    
    def ask_ai(self, query: str, user_context: Optional[dict] = None) -> str:
        """
        Return chatbot reply using rule-based engine or optional LLM.
        
        Args:
            query: User's message/question
            user_context: Optional dict with user profile data
            
        Returns:
            AI-generated response string
        """
        if user_context:
            self.context.update(user_context)
        
        # Try OpenAI if available and configured
        api_key = os.environ.get("OPENAI_API_KEY", "")
        if OPENAI_AVAILABLE and api_key:
            try:
                return self._get_openai_response(query)
            except Exception:
                pass  # Fall back to rule-based
        
        # Use rule-based engine
        return self._get_rule_based_response(query)
    
    def _get_openai_response(self, query: str) -> str:
        """Get response from OpenAI API (if configured)."""
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        
        system_prompt = """You are LifeUnity AI, a friendly and helpful cognitive wellness assistant. 
        You help users with:
        - Understanding their emotions and mood patterns
        - Stress management and relaxation techniques
        - Productivity tips and time management
        - Building their cognitive memory graph
        - Providing AI-powered wellness insights
        
        Be warm, supportive, and provide actionable advice. Use emojis appropriately."""
        
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    def _get_rule_based_response(self, query: str) -> str:
        """Get response using rule-based matching."""
        query_lower = query.lower().strip()
        
        # Check for greetings
        if any(word in query_lower for word in ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening']):
            return random.choice(self.greetings)
        
        # Check for stress-related queries
        if any(word in query_lower for word in ['stress', 'stressed', 'anxious', 'anxiety', 'worried', 'overwhelmed', 'tense', 'nervous']):
            response = random.choice(self.stress_responses)
            if 'stress_level' in self.context:
                response = f"I see your stress level is at {self.context['stress_level']:.0f}%. " + response
            return response
        
        # Check for productivity queries
        if any(word in query_lower for word in ['productivity', 'productive', 'focus', 'work', 'efficiency', 'task', 'concentrate']):
            response = random.choice(self.productivity_responses)
            if 'productivity' in self.context:
                response = f"Your current productivity score is {self.context['productivity']:.0f}%. " + response
            return response
        
        # Check for mood/emotion queries
        if any(word in query_lower for word in ['mood', 'feeling', 'emotion', 'happy', 'sad', 'angry', 'fear', 'joy']):
            return random.choice(self.mood_responses)
        
        # Check for memory queries
        if any(word in query_lower for word in ['memory', 'memories', 'remember', 'note', 'notes', 'knowledge', 'graph']):
            response = random.choice(self.memory_responses)
            if 'total_memories' in self.context:
                response = f"You currently have {self.context['total_memories']} memories stored. " + response
            return response
        
        # Check for help queries
        if any(word in query_lower for word in ['help', 'what can you do', 'features', 'capabilities', 'options', 'menu']):
            return random.choice(self.help_responses)
        
        # Check for thank you
        if any(word in query_lower for word in ['thank', 'thanks', 'appreciate', 'grateful']):
            return random.choice(self.thank_responses)
        
        # Check for "how am I doing" type queries
        if any(phrase in query_lower for phrase in ['how am i', 'my status', 'my progress', 'doing today', 'my day']):
            response = random.choice(self.today_responses)
            return response.format(
                stress=self.context.get('stress_level', 50),
                productivity=self.context.get('productivity', 75),
                memories=self.context.get('total_memories', 0)
            )
        
        # Check for insight queries
        if any(word in query_lower for word in ['insight', 'insights', 'analysis', 'analyze', 'report', 'pattern']):
            response = random.choice(self.insight_responses)
            return response.format(
                connections=self.context.get('total_connections', 0)
            )
        
        # Check for app-specific queries
        if 'dashboard' in query_lower:
            return "The **Dashboard** shows your overall wellness metrics including stress levels, productivity scores, and memory statistics. It's your home base for tracking cognitive health! 📊"
        
        if 'detection' in query_lower or 'face' in query_lower or 'photo' in query_lower:
            return "The **Mood Detection** page analyzes your emotions from a photo. Upload a clear picture of your face, and our AI will detect your emotional state with confidence scores! 😊📷"
        
        # Default response
        default = random.choice(self.default_responses)
        
        # Add context if available
        if 'stress_level' in self.context or 'productivity' in self.context:
            stats = "\n\n**Your Quick Stats:**\n"
            if 'stress_level' in self.context:
                stats += f"• Stress Level: {self.context['stress_level']:.0f}/100\n"
            if 'productivity' in self.context:
                stats += f"• Productivity: {self.context['productivity']:.0f}/100\n"
            default += stats
        
        return default


# Singleton instance for easy access
_chat_engine_instance = None


def get_chat_engine() -> ChatEngine:
    """Get or create the chat engine singleton instance."""
    global _chat_engine_instance
    if _chat_engine_instance is None:
        _chat_engine_instance = ChatEngine()
    return _chat_engine_instance


def ask_ai(query: str, user_context: Optional[dict] = None) -> str:
    """
    Convenience function to get AI chatbot response.
    
    Args:
        query: User's message/question
        user_context: Optional dict with user profile data
        
    Returns:
        AI-generated response string
    """
    engine = get_chat_engine()
    return engine.ask_ai(query, user_context)
