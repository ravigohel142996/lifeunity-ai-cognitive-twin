"""
Mood Detection module for LifeUnity AI Cognitive Twin System.
Emotion detection using DeepFace (Streamlit Cloud compatible).
"""

import numpy as np
from PIL import Image
import tempfile
from deepface import DeepFace
from app.utils.logger import get_logger

logger = get_logger("MoodDetection")


class MoodDetector:
    """Mood detector using DeepFace emotion analysis."""

    def __init__(self):
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
        ]
        logger.info("MoodDetector initialized using DeepFace")

    def detect_emotion(self, image: np.ndarray, return_all=False):
        """
        Detect emotion using DeepFace.
        """

        try:
            pil_img = Image.fromarray(image)

            # DeepFace requires a file path
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                pil_img.save(tmp.name)
                img_path = tmp.name

            result = DeepFace.analyze(
                img_path=img_path,
                actions=['emotion'],
                enforce_detection=False
            )

            emotions = result[0]['emotion']
            dominant = result[0]['dominant_emotion']
            confidence = emotions.get(dominant, 0.0)

            response = {
                "emotion": dominant.lower(),
                "confidence": float(confidence),
                "face_detected": True
            }

            if return_all:
                response["all_emotions"] = emotions

            logger.debug(f"Detected emotion: {dominant} (confidence {confidence:.2f})")

            return response

        except Exception as e:
            logger.error(f"Error in emotion detection: {str(e)}", exc_info=True)
            return {
                "emotion": "neutral",
                "confidence": 0.0,
                "face_detected": False,
                "error": str(e)
            }

    def get_emotion_color(self, emotion: str) -> str:
        emotion_colors = {
            'happy': '#FFD700',
            'sad': '#4169E1',
            'angry': '#DC143C',
            'fear': '#9370DB',
            'surprise': '#FF8C00',
            'disgust': '#228B22',
            'neutral': '#808080'
        }
        return emotion_colors.get(emotion.lower(), '#808080')

    def get_emotion_emoji(self, emotion: str) -> str:
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


_detector = None


def get_mood_detector() -> MoodDetector:
    global _detector
    if _detector is None:
        _detector = MoodDetector()
    return _detector
