---
title: LifeUnity AI - Cognitive Twin
emoji: 🧠
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app/main.py
pinned: false
license: mit
---

# LifeUnity AI — Cognitive Twin System 🧠

An advanced AI-powered cognitive twin system for emotional tracking, semantic memory management, and proactive wellness insights.

## 🎯 Features

- **😊 Emotion Detection**: Upload your photo for AI-powered emotion analysis using FER models
- **🧩 Cognitive Memory**: Store notes with automatic semantic embeddings using Sentence-BERT
- **💡 AI Insights**: Get daily wellness reports with stress/productivity predictions
- **📊 Dashboard**: Track your emotional trends and memory patterns

## 🚀 How to Use

1. **Dashboard**: View your current emotional state and statistics
2. **Mood Detection**: Upload a photo of your face to detect emotions
3. **Cognitive Memory**: Add notes and explore your memory graph
4. **AI Insights**: Generate personalized daily wellness reports

## 🔧 Technology Stack

- **Frontend**: Streamlit
- **AI Models**: FER (emotion detection), Sentence-BERT (embeddings)
- **Storage**: JSON-based (cloud-compatible)
- **No API keys required** - all models run locally in the Space

## 📝 Note

This application is optimized for HuggingFace Spaces deployment and uses:
- Image upload only (no webcam support on HF Spaces)
- Lightweight models for fast inference
- Local rule-based AI reasoning

Built with ❤️ for better mental wellness and productivity.
