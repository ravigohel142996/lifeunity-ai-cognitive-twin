# LifeUnity AI — Cognitive Twin System 🧠

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/🤗%20HuggingFace-Spaces-yellow?style=for-the-badge)](https://huggingface.co/spaces)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)](https://tensorflow.org)

An advanced AI-powered cognitive twin system that tracks your emotional state, builds a personalized memory graph, and provides proactive well-being insights. **Optimized for HuggingFace Spaces deployment.**

## 🌟 Features

### 1. **Emotion Detection via Image Upload** 😊
- Facial expression recognition using lightweight FER models
- Image upload support for emotion analysis (HuggingFace Spaces compatible)
- 7 emotion categories: happy, sad, angry, fear, surprise, disgust, neutral
- Confidence scoring for each detected emotion
- Automatic emotion history tracking

### 2. **Cognitive Memory Graph** 🧩
- Semantic memory storage using Sentence-BERT embeddings
- Automatic relationship discovery between memories
- Intelligent memory search and retrieval
- Graph-based visualization of connected thoughts
- Tag-based organization system

### 3. **AI Insights Engine** 💡
- Daily AI-generated wellness reports
- Stress level prediction and analysis
- Productivity score calculation
- Fatigue risk assessment
- Personalized recommendations based on patterns
- Proactive alerts for critical conditions

### 4. **User Profile Management** 👤
- Baseline data tracking
- Emotion history storage
- Behavior pattern analysis
- Customizable preferences
- Long-term trend analysis

## 🏗️ Architecture

```
LifeUnity AI Cognitive Twin System
│
├── Frontend (Streamlit Web App)
│   ├── Dashboard Page
│   ├── Mood Detection Page
│   ├── Cognitive Memory Page
│   └── AI Insights Page
│
├── Core AI Modules
│   ├── mood_detection.py      # FER-based emotion detection
│   ├── memory_graph.py         # Semantic memory with embeddings
│   ├── insights_engine.py      # AI reasoning & recommendations
│   └── user_profile.py         # User data management
│
├── Utilities
│   ├── logger.py               # Logging system
│   ├── preprocess.py           # Data preprocessing
│   └── embedder.py             # Text embedding wrapper
│
└── Data Storage (JSON-based)
    ├── User profiles
    ├── Memory embeddings
    └── Emotion history
```

## 🚀 Quick Start - HuggingFace Spaces

### Deploy on HuggingFace Spaces (Recommended)

This application is optimized for **HuggingFace Spaces** deployment:

1. **Fork or upload this repository to HuggingFace Spaces**
2. **Select Streamlit SDK** in your Space settings
3. **The app will automatically deploy** - no configuration needed!
4. **Access your Space URL** and start using the app immediately

The application runs completely in the cloud with:
- ✅ Image upload for emotion detection (no webcam needed)
- ✅ All AI models loaded automatically
- ✅ JSON-based storage in `/data` directory
- ✅ No API keys required

### HuggingFace Spaces Configuration

The repository includes:
- `app.py` - Entry point for HuggingFace Spaces
- `requirements.txt` - All cloud-compatible dependencies
- `.gitignore` - Proper exclusions for cloud deployment

## 🖥️ Local Installation (Optional)

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin.git
cd lifeunity-ai-cognitive-twin
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app/main.py
```

The application will open in your default web browser at `http://localhost:8501`

## ☁️ Cloud Deployment

### Deploy to Streamlit Cloud

1. **Fork/Push this repository to GitHub**

2. **Visit [Streamlit Cloud](https://share.streamlit.io/)**

3. **Create a new app**
   - Repository: `your-username/lifeunity-ai-cognitive-twin`
   - Branch: `main`
   - Main file path: `app/main.py`

4. **Click "Deploy"**

### Deploy to Render

1. **Create a `render.yaml` file** (already included)

2. **Connect your GitHub repository to Render**

3. **Deploy as a Web Service**

### Deploy to HuggingFace Spaces (Recommended)

**This application is optimized for HuggingFace Spaces!**

1. **Create a new Space on HuggingFace**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"

2. **Configure your Space**
   - Space name: `lifeunity-ai-cognitive-twin`
   - SDK: **Streamlit**
   - Space hardware: CPU basic (free)

3. **Upload or git push your code**
   - Use the HuggingFace UI to upload files
   - Or clone the Space repo and push code via git

4. **The app will automatically deploy**
   - First deployment may take 5-10 minutes
   - Models download automatically on first run

5. **Access your Space**
   - Your app will be live at: `https://huggingface.co/spaces/[username]/[space-name]`

**Note**: The app is configured to work without webcam support (HF limitation) - only image upload is available.

## 📖 Usage Guide

### Dashboard 📊
The dashboard provides an overview of your cognitive state:
- Current stress levels
- Productivity score
- Recent mood trends
- Memory graph statistics
- Quick access to all features

### Mood Detection 😊
Upload your photo for emotion analysis:

1. **Image Upload**
   - Navigate to "Mood Detection" page
   - Click "Upload an image of your face"
   - Select a clear photo showing your face
   - View detected emotion with confidence score
   - Save to your profile for tracking
   - See all detected emotions breakdown

### Cognitive Memory 🧩
Build your personal knowledge graph:

1. **Add Memories**
   - Write notes, thoughts, or experiences
   - Add optional tags for organization
   - System automatically creates embeddings

2. **Search Memories**
   - Enter a search query
   - AI finds semantically similar memories
   - View similarity scores

3. **View Connections**
   - See how memories relate to each other
   - Explore memory clusters
   - Understand thought patterns

### AI Insights 💡
Get personalized recommendations:

1. **Generate Daily Report**
   - Click "Generate Daily Report"
   - Review stress, productivity, and fatigue metrics
   - Read AI-generated insights

2. **View Recommendations**
   - High-priority actions for critical issues
   - Medium-priority suggestions for improvement
   - General well-being tips

3. **Analyze Patterns**
   - Select time period for analysis
   - View emotion trends
   - Understand behavior patterns

## 🔧 Configuration

### Environment Variables
Create a `.streamlit/config.toml` file for custom configuration:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
```

### Data Storage
By default, all data is stored locally in JSON files:
- `data/default_user_profile.json` - User profile
- `data/memory_graph.json` - Memory embeddings
- `logs/` - Application logs

## 🛠️ Technology Stack

### AI/ML Models
- **FER (Facial Expression Recognition)** - Emotion detection
- **Sentence-BERT** (all-MiniLM-L6-v2) - Text embeddings
- **NetworkX** - Graph analysis

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Pandas** - Data manipulation

### Backend
- **Python 3.8+** - Core language
- **NumPy** - Numerical computing
- **OpenCV** - Image processing
- **TensorFlow** - Deep learning backend

## 📊 Data Privacy

- All data is stored locally or in your cloud deployment
- No data is sent to external servers (except model downloads)
- You have full control over your data
- Can delete memories and history at any time

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FER Library** - For emotion detection capabilities
- **Sentence-Transformers** - For semantic embeddings
- **Streamlit** - For the amazing web framework
- **NetworkX** - For graph analysis tools

## 📧 Contact

**Ravi Gohel**
- GitHub: [@ravigohel142996](https://github.com/ravigohel142996)

## 🗺️ Roadmap

- [ ] Integration with wearable devices
- [ ] Voice emotion detection
- [ ] Multi-user support
- [ ] Advanced LLM integration for deeper insights
- [ ] Mobile app version
- [ ] Real-time collaboration features
- [ ] Export data analytics reports
- [ ] Integration with calendar and productivity tools

## 📸 Screenshots

### Dashboard
![Dashboard Screenshot](docs/screenshots/dashboard.png)
*The main dashboard showing your current cognitive state and trends*

### Mood Detection
![Mood Detection Screenshot](docs/screenshots/mood_detection.png)
*Real-time emotion detection from webcam or uploaded images*

### Cognitive Memory
![Cognitive Memory Screenshot](docs/screenshots/memory_graph.png)
*Your personal knowledge graph with semantic connections*

### AI Insights
![AI Insights Screenshot](docs/screenshots/insights.png)
*Personalized recommendations and daily wellness report*

---

**Built with ❤️ for better mental wellness and productivity**
