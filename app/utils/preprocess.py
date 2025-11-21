"""
Preprocessing utilities for LifeUnity AI Cognitive Twin System.
Handles data preprocessing, validation, and transformation.
"""

import cv2
import numpy as np
from PIL import Image
from typing import Union, Tuple, Optional
import re


def preprocess_image_for_emotion(
    image: Union[np.ndarray, Image.Image],
    target_size: Tuple[int, int] = (48, 48),
    grayscale: bool = True
) -> np.ndarray:
    """
    Preprocess an image for emotion detection.
    
    Args:
        image: Input image (numpy array or PIL Image)
        target_size: Target size for the image
        grayscale: Whether to convert to grayscale
        
    Returns:
        Preprocessed image as numpy array
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Convert to grayscale if needed
    if grayscale and len(image.shape) == 3:
        if image.shape[2] == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        elif image.shape[2] == 4:
            image = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)
    
    # Resize to target size
    image = cv2.resize(image, target_size)
    
    # Normalize pixel values
    image = image.astype('float32') / 255.0
    
    return image


def preprocess_face_region(
    image: np.ndarray,
    face_cascade: Optional[cv2.CascadeClassifier] = None
) -> Optional[np.ndarray]:
    """
    Detect and extract face region from image.
    
    Args:
        image: Input image
        face_cascade: Face cascade classifier (if None, will load default)
        
    Returns:
        Face region as numpy array or None if no face detected
    """
    if face_cascade is None:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )
    
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30)
    )
    
    # Return first face found
    if len(faces) > 0:
        x, y, w, h = faces[0]
        return image[y:y+h, x:x+w]
    
    return None


def clean_text(text: str) -> str:
    """
    Clean and normalize text input.
    
    Args:
        text: Input text
        
    Returns:
        Cleaned text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading/trailing whitespace
    text = text.strip()
    
    return text


def validate_emotion_input(emotion: str, confidence: float) -> bool:
    """
    Validate emotion detection output.
    
    Args:
        emotion: Detected emotion label
        confidence: Confidence score
        
    Returns:
        True if valid, False otherwise
    """
    valid_emotions = [
        'angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral'
    ]
    
    if emotion.lower() not in valid_emotions:
        return False
    
    if not (0.0 <= confidence <= 1.0):
        return False
    
    return True


def normalize_array(arr: np.ndarray) -> np.ndarray:
    """
    Normalize array to 0-1 range.
    
    Args:
        arr: Input array
        
    Returns:
        Normalized array
    """
    min_val = np.min(arr)
    max_val = np.max(arr)
    
    if max_val - min_val == 0:
        return arr
    
    return (arr - min_val) / (max_val - min_val)


def prepare_batch_images(images: list, target_size: Tuple[int, int] = (48, 48)) -> np.ndarray:
    """
    Prepare a batch of images for model input.
    
    Args:
        images: List of images
        target_size: Target size for images
        
    Returns:
        Batch of preprocessed images
    """
    processed = []
    
    for img in images:
        processed_img = preprocess_image_for_emotion(img, target_size)
        processed.append(processed_img)
    
    return np.array(processed)
