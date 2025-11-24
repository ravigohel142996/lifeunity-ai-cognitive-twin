"""
User Profile module for LifeUnity AI Cognitive Twin System.
Manages user data, preferences, and behavior tracking.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path
from .utils.logger import get_logger

logger = get_logger("UserProfile")


class UserProfile:
    """User profile manager for the Cognitive Twin system."""
    
    def __init__(self, user_id: str = "default_user", data_dir: str = "data"):
        """
        Initialize user profile.
        
        Args:
            user_id: Unique user identifier
            data_dir: Directory to store user data
        """
        self.user_id = user_id
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.profile_file = self.data_dir / f"{user_id}_profile.json"
        self.profile = self._load_profile()
        
        logger.info(f"UserProfile initialized for user: {user_id}")
    
    def _load_profile(self) -> Dict:
        """Load user profile from file."""
        try:
            if self.profile_file.exists():
                with open(self.profile_file, 'r') as f:
                    profile = json.load(f)
                logger.info(f"Loaded profile for user: {self.user_id}")
                return profile
            else:
                # Create default profile
                default_profile = self._create_default_profile()
                self._save_profile(default_profile)
                return default_profile
        except Exception as e:
            logger.error(f"Error loading profile: {str(e)}", exc_info=True)
            return self._create_default_profile()
    
    def _create_default_profile(self) -> Dict:
        """Create a default user profile."""
        return {
            'user_id': self.user_id,
            'created_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'baseline_data': {
                'average_mood': 'neutral',
                'stress_baseline': 50.0,
                'productivity_baseline': 50.0,
                'sleep_hours': 7.0
            },
            'emotion_history': [],
            'behavior_patterns': {
                'peak_productivity_hours': [],
                'common_stress_triggers': [],
                'mood_trends': {}
            },
            'notes': [],
            'preferences': {
                'notification_enabled': True,
                'data_retention_days': 90
            }
        }
    
    def _save_profile(self, profile: Optional[Dict] = None):
        """Save user profile to file."""
        try:
            if profile is None:
                profile = self.profile
            
            profile['last_updated'] = datetime.now().isoformat()
            
            with open(self.profile_file, 'w') as f:
                json.dump(profile, f, indent=2)
            
            logger.debug(f"Profile saved for user: {self.user_id}")
            
        except Exception as e:
            logger.error(f"Error saving profile: {str(e)}", exc_info=True)
    
    def update_baseline(self, baseline_data: Dict):
        """
        Update user baseline data.
        
        Args:
            baseline_data: Dictionary with baseline metrics
        """
        self.profile['baseline_data'].update(baseline_data)
        self._save_profile()
        logger.info(f"Updated baseline data for user: {self.user_id}")
    
    def add_emotion_record(
        self,
        emotion: str,
        confidence: float,
        timestamp: Optional[str] = None
    ):
        """
        Add emotion record to history.
        
        Args:
            emotion: Detected emotion
            confidence: Confidence score
            timestamp: Optional timestamp (ISO format)
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()
        
        record = {
            'emotion': emotion,
            'confidence': confidence,
            'timestamp': timestamp
        }
        
        self.profile['emotion_history'].append(record)
        
        # Keep only recent records (last 1000)
        if len(self.profile['emotion_history']) > 1000:
            self.profile['emotion_history'] = self.profile['emotion_history'][-1000:]
        
        self._save_profile()
        logger.debug(f"Added emotion record: {emotion} ({confidence:.2f})")
    
    def get_emotion_history(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get emotion history.
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of emotion records
        """
        history = self.profile.get('emotion_history', [])
        if limit:
            return history[-limit:]
        return history
    
    def add_note(self, content: str, tags: Optional[List[str]] = None):
        """
        Add a note to user profile.
        
        Args:
            content: Note content
            tags: Optional tags for the note
        """
        note = {
            'id': len(self.profile['notes']) + 1,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'tags': tags or []
        }
        
        self.profile['notes'].append(note)
        self._save_profile()
        logger.info(f"Added note for user: {self.user_id}")
    
    def get_notes(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get user notes.
        
        Args:
            limit: Maximum number of notes to return
            
        Returns:
            List of notes
        """
        notes = self.profile.get('notes', [])
        if limit:
            return notes[-limit:]
        return notes
    
    def update_behavior_pattern(self, pattern_type: str, data: any):
        """
        Update behavior pattern.
        
        Args:
            pattern_type: Type of pattern (e.g., 'peak_productivity_hours')
            data: Pattern data
        """
        self.profile['behavior_patterns'][pattern_type] = data
        self._save_profile()
        logger.info(f"Updated behavior pattern: {pattern_type}")
    
    def get_behavior_patterns(self) -> Dict:
        """Get all behavior patterns."""
        return self.profile.get('behavior_patterns', {})
    
    def calculate_stress_level(self) -> float:
        """
        Calculate current stress level based on recent emotions.
        
        Returns:
            Stress level (0-100)
        """
        recent_emotions = self.get_emotion_history(limit=10)
        
        if not recent_emotions:
            return 50.0  # Default neutral stress level
        
        # Stress weights for different emotions
        stress_weights = {
            'angry': 90,
            'fear': 85,
            'disgust': 70,
            'sad': 75,
            'surprise': 40,
            'happy': 20,
            'neutral': 50
        }
        
        total_stress = 0.0
        for record in recent_emotions:
            emotion = record.get('emotion', 'neutral')
            confidence = record.get('confidence', 0.5)
            weight = stress_weights.get(emotion, 50)
            total_stress += weight * confidence
        
        avg_stress = total_stress / len(recent_emotions)
        return round(avg_stress, 2)
    
    def calculate_productivity_score(self) -> float:
        """
        Calculate productivity score based on mood and patterns.
        
        Returns:
            Productivity score (0-100)
        """
        recent_emotions = self.get_emotion_history(limit=10)
        
        if not recent_emotions:
            return 50.0  # Default neutral productivity
        
        # Productivity weights for different emotions
        productivity_weights = {
            'happy': 90,
            'neutral': 70,
            'surprise': 60,
            'sad': 40,
            'angry': 30,
            'fear': 35,
            'disgust': 45
        }
        
        total_productivity = 0.0
        for record in recent_emotions:
            emotion = record.get('emotion', 'neutral')
            confidence = record.get('confidence', 0.5)
            weight = productivity_weights.get(emotion, 50)
            total_productivity += weight * confidence
        
        avg_productivity = total_productivity / len(recent_emotions)
        return round(avg_productivity, 2)
    
    def get_summary(self) -> Dict:
        """
        Get user profile summary.
        
        Returns:
            Summary dictionary
        """
        return {
            'user_id': self.user_id,
            'created_at': self.profile['created_at'],
            'last_updated': self.profile['last_updated'],
            'total_emotions_tracked': len(self.profile['emotion_history']),
            'total_notes': len(self.profile['notes']),
            'current_stress_level': self.calculate_stress_level(),
            'current_productivity': self.calculate_productivity_score(),
            'baseline_data': self.profile['baseline_data']
        }


# Global profile instance
_profile = None


def get_user_profile(user_id: str = "default_user") -> UserProfile:
    """
    Get or create a user profile instance.
    
    Args:
        user_id: User identifier
        
    Returns:
        UserProfile instance
    """
    global _profile
    if _profile is None or _profile.user_id != user_id:
        _profile = UserProfile(user_id)
    return _profile
