"""
Insights Engine module for LifeUnity AI Cognitive Twin System.
Generates proactive AI-powered insights and recommendations.
"""

from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
from .utils.logger import get_logger
from .user_profile import get_user_profile
from .memory_graph import get_memory_graph

logger = get_logger("InsightsEngine")


class InsightsEngine:
    """AI-powered insights and recommendations engine."""
    
    def __init__(self):
        """Initialize the insights engine."""
        self.user_profile = get_user_profile()
        self.memory_graph = get_memory_graph()
        logger.info("InsightsEngine initialized")
    
    def generate_daily_report(self) -> Dict:
        """
        Generate a comprehensive daily AI report.
        
        Returns:
            Dictionary containing the daily report
        """
        try:
            # Get user data
            stress_level = self.user_profile.calculate_stress_level()
            productivity = self.user_profile.calculate_productivity_score()
            emotion_history = self.user_profile.get_emotion_history(limit=20)
            
            # Analyze patterns
            fatigue_risk = self._predict_fatigue(emotion_history, stress_level)
            stress_insights = self._analyze_stress(stress_level)
            productivity_insights = self._analyze_productivity(productivity)
            
            # Generate recommendations
            recommendations = self._generate_recommendations(
                stress_level, productivity, fatigue_risk
            )
            
            report = {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'generated_at': datetime.now().isoformat(),
                'metrics': {
                    'stress_level': stress_level,
                    'productivity_score': productivity,
                    'fatigue_risk': fatigue_risk
                },
                'insights': {
                    'stress': stress_insights,
                    'productivity': productivity_insights
                },
                'recommendations': recommendations,
                'alerts': self._generate_alerts(stress_level, fatigue_risk)
            }
            
            logger.info("Generated daily report")
            return report
            
        except Exception as e:
            logger.error(f"Error generating daily report: {str(e)}", exc_info=True)
            return self._get_default_report()
    
    def _predict_fatigue(self, emotion_history: List[Dict], stress_level: float) -> str:
        """
        Predict fatigue level based on emotions and stress.
        
        Args:
            emotion_history: Recent emotion records
            stress_level: Current stress level
            
        Returns:
            Fatigue risk level (low, moderate, high)
        """
        if not emotion_history:
            return "moderate"
        
        # Count negative emotions
        negative_emotions = ['sad', 'angry', 'fear', 'disgust']
        negative_count = sum(
            1 for record in emotion_history
            if record.get('emotion') in negative_emotions
        )
        
        negative_ratio = negative_count / len(emotion_history)
        
        # Combine with stress level
        fatigue_score = (negative_ratio * 100 + stress_level) / 2
        
        if fatigue_score < 40:
            return "low"
        elif fatigue_score < 70:
            return "moderate"
        else:
            return "high"
    
    def _analyze_stress(self, stress_level: float) -> Dict:
        """
        Analyze stress level and provide insights.
        
        Args:
            stress_level: Current stress level
            
        Returns:
            Stress analysis
        """
        if stress_level < 30:
            status = "Low"
            description = "Your stress levels are well-managed. Keep maintaining your current lifestyle and coping strategies."
        elif stress_level < 60:
            status = "Moderate"
            description = "Your stress levels are within a manageable range. Consider incorporating more relaxation techniques."
        else:
            status = "High"
            description = "Your stress levels are elevated. It's important to take breaks and practice stress-reduction activities."
        
        return {
            'level': stress_level,
            'status': status,
            'description': description
        }
    
    def _analyze_productivity(self, productivity: float) -> Dict:
        """
        Analyze productivity score and provide insights.
        
        Args:
            productivity: Current productivity score
            
        Returns:
            Productivity analysis
        """
        if productivity >= 70:
            status = "Excellent"
            description = "You're in a great productive state! Your emotional balance is supporting high performance."
        elif productivity >= 50:
            status = "Good"
            description = "Your productivity is stable. Small improvements in mood management could enhance performance."
        else:
            status = "Needs Attention"
            description = "Your productivity may be affected by emotional factors. Focus on well-being to improve output."
        
        return {
            'score': productivity,
            'status': status,
            'description': description
        }
    
    def _generate_recommendations(
        self,
        stress_level: float,
        productivity: float,
        fatigue_risk: str
    ) -> List[Dict]:
        """
        Generate personalized recommendations.
        
        Args:
            stress_level: Current stress level
            productivity: Current productivity score
            fatigue_risk: Fatigue risk level
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # Stress-based recommendations
        if stress_level > 70:
            recommendations.append({
                'category': 'Stress Management',
                'priority': 'high',
                'suggestion': 'Take a 10-minute meditation break to reduce elevated stress levels.',
                'action': 'Practice deep breathing exercises or use a meditation app.'
            })
        elif stress_level > 50:
            recommendations.append({
                'category': 'Stress Management',
                'priority': 'medium',
                'suggestion': 'Consider a short walk or stretching session to manage stress.',
                'action': 'Take a 5-minute break every hour.'
            })
        
        # Fatigue-based recommendations
        if fatigue_risk == "high":
            recommendations.append({
                'category': 'Energy Management',
                'priority': 'high',
                'suggestion': 'High fatigue risk detected. Ensure adequate rest and avoid overexertion.',
                'action': 'Schedule a longer break or end your work session early if possible.'
            })
        elif fatigue_risk == "moderate":
            recommendations.append({
                'category': 'Energy Management',
                'priority': 'medium',
                'suggestion': 'Monitor your energy levels and take breaks when needed.',
                'action': 'Stay hydrated and have a healthy snack.'
            })
        
        # Productivity-based recommendations
        if productivity < 50:
            recommendations.append({
                'category': 'Productivity Enhancement',
                'priority': 'medium',
                'suggestion': 'Your mood may be affecting productivity. Focus on emotional well-being first.',
                'action': 'Engage in a mood-boosting activity like listening to music or talking to a friend.'
            })
        elif productivity >= 70:
            recommendations.append({
                'category': 'Productivity Enhancement',
                'priority': 'low',
                'suggestion': 'Great productive state! Use this momentum to tackle challenging tasks.',
                'action': 'Focus on high-priority items while you\'re in this optimal state.'
            })
        
        # General well-being recommendations
        recommendations.append({
            'category': 'Well-being',
            'priority': 'low',
            'suggestion': 'Maintain work-life balance by setting clear boundaries.',
            'action': 'Schedule time for hobbies and social connections.'
        })
        
        return recommendations
    
    def _generate_alerts(self, stress_level: float, fatigue_risk: str) -> List[Dict]:
        """
        Generate alerts for critical conditions.
        
        Args:
            stress_level: Current stress level
            fatigue_risk: Fatigue risk level
            
        Returns:
            List of alerts
        """
        alerts = []
        
        if stress_level > 80:
            alerts.append({
                'type': 'warning',
                'message': 'Critical stress level detected. Immediate action recommended.',
                'timestamp': datetime.now().isoformat()
            })
        
        if fatigue_risk == "high":
            alerts.append({
                'type': 'warning',
                'message': 'High fatigue risk. Consider resting to prevent burnout.',
                'timestamp': datetime.now().isoformat()
            })
        
        return alerts
    
    def analyze_emotion_patterns(self, days: int = 7) -> Dict:
        """
        Analyze emotion patterns over a period.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            Pattern analysis
        """
        try:
            emotion_history = self.user_profile.get_emotion_history()
            
            if not emotion_history:
                return {
                    'pattern': 'No data available',
                    'dominant_emotions': [],
                    'trend': 'neutral'
                }
            
            # Filter recent emotions
            cutoff_date = datetime.now() - timedelta(days=days)
            recent_emotions = [
                e for e in emotion_history
                if datetime.fromisoformat(e['timestamp']) > cutoff_date
            ]
            
            if not recent_emotions:
                recent_emotions = emotion_history[-10:]  # Use last 10 if no recent
            
            # Count emotions
            emotion_counts = {}
            for record in recent_emotions:
                emotion = record.get('emotion', 'neutral')
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            
            # Get dominant emotions
            sorted_emotions = sorted(
                emotion_counts.items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            # Determine trend
            positive_emotions = ['happy', 'surprise']
            negative_emotions = ['sad', 'angry', 'fear', 'disgust']
            
            positive_count = sum(
                emotion_counts.get(e, 0) for e in positive_emotions
            )
            negative_count = sum(
                emotion_counts.get(e, 0) for e in negative_emotions
            )
            
            if positive_count > negative_count * 1.5:
                trend = 'positive'
            elif negative_count > positive_count * 1.5:
                trend = 'negative'
            else:
                trend = 'neutral'
            
            return {
                'period_days': days,
                'total_records': len(recent_emotions),
                'dominant_emotions': [e[0] for e in sorted_emotions[:3]],
                'emotion_distribution': emotion_counts,
                'trend': trend
            }
            
        except Exception as e:
            logger.error(f"Error analyzing emotion patterns: {str(e)}", exc_info=True)
            return {'pattern': 'Error analyzing patterns', 'dominant_emotions': [], 'trend': 'neutral'}
    
    def suggest_memory_insights(self, limit: int = 5) -> List[Dict]:
        """
        Generate insights from memory graph.
        
        Args:
            limit: Number of insights to generate
            
        Returns:
            List of memory-based insights
        """
        try:
            memories = self.memory_graph.get_all_memories()
            
            if not memories:
                return []
            
            insights = []
            
            # Get recent memories
            recent_memories = sorted(
                memories,
                key=lambda x: x['timestamp'],
                reverse=True
            )[:limit]
            
            for memory in recent_memories:
                # Find related memories
                related = self.memory_graph.get_related_memories(memory['id'])
                
                insight = {
                    'memory_id': memory['id'],
                    'content_preview': memory['content'][:100] + '...' if len(memory['content']) > 100 else memory['content'],
                    'timestamp': memory['timestamp'],
                    'related_count': len(related),
                    'tags': memory.get('tags', [])
                }
                
                insights.append(insight)
            
            return insights
            
        except Exception as e:
            logger.error(f"Error generating memory insights: {str(e)}", exc_info=True)
            return []
    
    def _get_default_report(self) -> Dict:
        """Get a default report when generation fails."""
        return {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'generated_at': datetime.now().isoformat(),
            'metrics': {
                'stress_level': 50.0,
                'productivity_score': 50.0,
                'fatigue_risk': 'moderate'
            },
            'insights': {
                'stress': {
                    'level': 50.0,
                    'status': 'Moderate',
                    'description': 'Unable to generate insights at this time.'
                },
                'productivity': {
                    'score': 50.0,
                    'status': 'Good',
                    'description': 'Unable to generate insights at this time.'
                }
            },
            'recommendations': [],
            'alerts': []
        }


# Global insights engine instance
_insights_engine = None


def get_insights_engine() -> InsightsEngine:
    """
    Get or create a global insights engine instance.
    
    Returns:
        InsightsEngine instance
    """
    global _insights_engine
    if _insights_engine is None:
        _insights_engine = InsightsEngine()
    return _insights_engine
