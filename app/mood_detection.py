"""
Mood Detection module for LifeUnity AI Cognitive Twin System.
Emotion detection using DeepFace (Streamlit Cloud compatible).
"""

import numpy as np
from PIL import Image
import tempfile
from app.utils.logger import get_logger

logger = get_logger("MoodDetection")

# Try to import DeepFace, but handle gracefully if not available
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
    logger.info("DeepFace loaded successfully")
except (ImportError, ValueError) as e:
    DEEPFACE_AVAILABLE = False
    logger.warning(f"DeepFace not available: {e}. Emotion detection will use mock data.")


class MoodDetector:
    """Mood detector using DeepFace emotion analysis."""

    def __init__(self):
        self.emotion_labels = [
            'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
        ]
        self.deepface_available = DEEPFACE_AVAILABLE
        if self.deepface_available:
            logger.info("MoodDetector initialized using DeepFace")
        else:
            logger.warning("MoodDetector initialized in demo mode (DeepFace not available)")

    def detect_emotion(self, image: np.ndarray, return_all=False):
        """
        Detect emotion using DeepFace.
        If DeepFace is not available, returns demo data.
        """
        
        # If DeepFace is not available, return demo emotion
        if not self.deepface_available:
            # Use thread-safe random generation
            rng = np.random.default_rng()
            demo_emotion_idx = rng.integers(0, len(self.emotion_labels))
            demo_emotion = self.emotion_labels[demo_emotion_idx]
            demo_confidence = rng.uniform(0.5, 0.9)
            response = {
                "emotion": demo_emotion,
                "confidence": float(demo_confidence),
                "face_detected": True,
                "demo_mode": True,
                "message": "DeepFace not available. Using demo mode."
            }
            if return_all:
                # Generate mock emotions using thread-safe random
                all_emotions = {emotion: float(rng.uniform(0.0, 1.0)) for emotion in self.emotion_labels}
                # Normalize
                total = sum(all_emotions.values())
                all_emotions = {k: v/total for k, v in all_emotions.items()}
                response["all_emotions"] = all_emotions
            logger.info(f"Demo mode: Returning {demo_emotion} with confidence {demo_confidence:.2f}")
            return response

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
