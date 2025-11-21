# Quick Start Guide

Get started with LifeUnity AI — Cognitive Twin System in under 5 minutes!

## Prerequisites

- Python 3.8 or higher
- pip package manager
- (Optional) Webcam for live emotion detection

## Installation

### Option 1: Local Setup (Recommended for Development)

```bash
# 1. Clone the repository
git clone https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin.git
cd lifeunity-ai-cognitive-twin

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

### Option 2: Using Docker

```bash
# 1. Clone the repository
git clone https://github.com/ravigohel142996/lifeunity-ai-cognitive-twin.git
cd lifeunity-ai-cognitive-twin

# 2. Build and run with Docker Compose
docker-compose up

# Or build manually
docker build -t lifeunity-ai .
docker run -p 8501:8501 lifeunity-ai
```

### Option 3: Quick Run Script

```bash
# Make the script executable
chmod +x run.sh

# Run the application
./run.sh
```

## First Steps

### 1. Explore the Dashboard 📊
- View your cognitive state overview
- Check stress and productivity metrics
- See emotion trends

### 2. Detect Your Mood 😊
- Go to "Mood Detection" page
- Upload a photo OR use your webcam
- View detected emotion and confidence
- Save to your profile

### 3. Add Memories 🧩
- Navigate to "Cognitive Memory"
- Write a note or thought
- Add optional tags
- System creates embeddings automatically
- Search and explore connections

### 4. Get AI Insights 💡
- Visit "AI Insights" page
- Click "Generate Daily Report"
- Review your metrics and recommendations
- Analyze emotion patterns

## Cloud Deployment (No Setup Required!)

### Streamlit Cloud
1. Fork this repository
2. Visit [share.streamlit.io](https://share.streamlit.io)
3. Create new app: `your-username/lifeunity-ai-cognitive-twin`
4. Set main file: `app/main.py`
5. Deploy! ✨

### Render
1. Connect your GitHub repo to Render
2. Select this repository
3. Render uses `render.yaml` automatically
4. Deploy! ✨

See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for detailed instructions.

## Troubleshooting

### ImportError: No module named 'XXX'
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt
```

### Webcam not working
- Grant browser camera permissions
- Try image upload instead
- Check if camera is in use by another app

### Slow first load
- Models download on first run (normal)
- Subsequent loads will be faster
- Can take 2-5 minutes for initial setup

### Port already in use
```bash
# Use a different port
streamlit run app/main.py --server.port 8502
```

## Configuration

### Custom Settings

Edit `.streamlit/config.toml` to customize:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
# ... more options
```

### Data Storage

Data is stored locally in:
- `data/` - User profiles and memories
- `logs/` - Application logs

## Tips

🎯 **Best Practices:**
- Take mood readings at consistent times
- Add detailed memories for better connections
- Generate insights weekly
- Use tags to organize memories

📸 **For Best Results:**
- Use well-lit photos
- Ensure face is clearly visible
- Front-facing camera works best
- Natural expressions preferred

## Next Steps

- Read the [README](README.md) for full documentation
- Check [DEPLOYMENT](docs/DEPLOYMENT.md) for cloud hosting
- Explore [CONTRIBUTING](CONTRIBUTING.md) to contribute

## Support

- 📖 Documentation: See README.md
- 🐛 Issues: Open on GitHub
- 💬 Questions: GitHub Discussions

---

**Ready to start your cognitive twin journey!** 🧠✨
