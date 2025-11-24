"""
Mood Detection module for LifeUnity AI Cognitive Twin System.
Emotion detection using facial expression recognition via image upload.
"""

import numpy as np
from typing import Dict
from fer import FER
from .utils.logger import get_logger

logger = get_logger("MoodDetection")


class MoodDetector:
    """Mood detector using Facial Expression Recognition."""
    
    def __init__(self):
        """Initialize the mood detector."""
        self.detector = None
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
        ]
        logger.info("MoodDetector initialized")
    
    def load_model(self):
        """Load the FER model."""
        try:
            if self.detector is None:
                logger.info("Loading FER model...")
                self.detector = FER(mtcnn=False)
                logger.info("FER model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading FER model: {str(e)}", exc_info=True)
            raise
    
    def detect_emotion(
        self,
        image: np.ndarray,
        return_all: bool = False
    ) -> Dict[str, any]:
        """
        Detect emotion from an image.
        
        Args:
            image: Input image as numpy array
            return_all: Whether to return all emotion scores
            
        Returns:
            Dictionary with emotion, confidence, and optionally all scores
        """
        if self.detector is None:
            self.load_model()
        
        try:
            # Detect emotions
            result = self.detector.detect_emotions(image)
            
            if not result or len(result) == 0:
                logger.warning("No face detected in image")
                return {
                    'emotion': 'neutral',
                    'confidence': 0.0,
                    'all_emotions': {},
                    'face_detected': False
                }
            
            # Get the first face detected
            emotions = result[0]['emotions']
            
            # Find dominant emotion
            dominant_emotion = max(emotions, key=emotions.get)
            confidence = emotions[dominant_emotion]
            
            response = {
                'emotion': dominant_emotion,
                'confidence': confidence,
                'face_detected': True
            }
            
            if return_all:
                response['all_emotions'] = emotions
            
            logger.debug(f"Detected emotion: {dominant_emotion} (confidence: {confidence:.2f})")
            
            return response
            
        except Exception as e:
            logger.error(f"Error detecting emotion: {str(e)}", exc_info=True)
            return {
                'emotion': 'error',
                'confidence': 0.0,
                'all_emotions': {},
                'face_detected': False,
                'error': str(e)
            }
    
    def get_emotion_color(self, emotion: str) -> str:
        """
        Get color associated with emotion.
        
        Args:
            emotion: Emotion label
            
        Returns:
            Color code
        """
        emotion_colors = {
            'happy': '#FFD700',      # Gold
            'sad': '#4169E1',        # Royal Blue
            'angry': '#DC143C',      # Crimson
            'fear': '#9370DB',       # Medium Purple
            'surprise': '#FF8C00',   # Dark Orange
            'disgust': '#228B22',    # Forest Green
            'neutral': '#808080'     # Gray
        }
        return emotion_colors.get(emotion.lower(), '#808080')
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """
        Get emoji for emotion.
        
        Args:
            emotion: Emotion label
            
        Returns:
            Emoji string
        """
        emotion_emojis = {
            'happy': '😊',
            'sad': '😢',
            'angry': '😠',
            'fear': '😨',
            'surprise': '😲',
            'disgust': '🤢',
            'neutral': '😐'
        }
        return emotion_emojis.get(emotion.lower(), '😐')
    
    def analyze_emotion_trend(self, emotions_history: list) -> Dict[str, any]:
        """
        Analyze emotion trends from history.
        
        Args:
            emotions_history: List of emotion records
            
        Returns:
            Trend analysis
        """
        if not emotions_history:
            return {
                'dominant_emotion': 'neutral',
                'average_confidence': 0.0,
                'emotion_distribution': {}
            }
        
        # Count emotions
        emotion_counts = {}
        total_confidence = 0.0
        
        for record in emotions_history:
            emotion = record.get('emotion', 'neutral')
            confidence = record.get('confidence', 0.0)
            
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
            total_confidence += confidence
        
        # Calculate dominant emotion
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
        # Calculate distribution percentages
        total_records = len(emotions_history)
        emotion_distribution = {
            emotion: (count / total_records) * 100
            for emotion, count in emotion_counts.items()
        }
        
        return {
            'dominant_emotion': dominant_emotion,
            'average_confidence': total_confidence / total_records,
            'emotion_distribution': emotion_distribution,
            'total_records': total_records
        }


# Global detector instance
_detector = None


def get_mood_detector() -> MoodDetector:
    """
    Get or create a global mood detector instance.
    
    Returns:
        MoodDetector instance
    """
    global _detector
    if _detector is None:
        _detector = MoodDetector()
    return _detector
