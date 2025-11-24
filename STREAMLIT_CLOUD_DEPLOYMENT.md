# Streamlit Cloud Deployment Guide 🚀

## Quick Answer: Main File Path

**For Streamlit Cloud deployment, use:**

```
main.py
```

That's it! The main file path is simply `main.py` (located in the root directory of the repository).

---

## Step-by-Step Deployment Instructions

### 1. Fork or Push Repository to GitHub
- Ensure your code is pushed to GitHub
- Repository: `ravigohel142996/lifeunity-ai-cognitive-twin` (or `your-username/lifeunity-ai-cognitive-twin` if you forked it)

### 2. Go to Streamlit Cloud
- Visit [Streamlit Cloud](https://share.streamlit.io/)
- Sign in with your GitHub account

### 3. Deploy New App
Click "New app" or "Deploy an app" and enter the following:

| Field | Value |
|-------|-------|
| **Repository** | `ravigohel142996/lifeunity-ai-cognitive-twin` (or `your-username/lifeunity-ai-cognitive-twin` if forked) |
| **Branch** | `main` |
| **Main file path** | `main.py` |
| **App URL (optional)** | `lifeunity-ai-cognitive-twin` (or your preferred name) |

### 4. Click "Deploy"
- Streamlit Cloud will automatically:
  - Install dependencies from `requirements.txt`
  - Run `streamlit run main.py`
  - Deploy your app to a public URL

### 5. Access Your App
- Your app will be available at: `https://[your-app-name].streamlit.app`
- First deployment takes 5-10 minutes

---

## Important Notes

### ✅ Correct Main File Path
- **Use:** `main.py` (root directory)
- **Don't use:** `app/main.py` (this file doesn't exist)

### 📁 Repository Structure
```
lifeunity-ai-cognitive-twin/
├── main.py                 ← Main Streamlit application (ENTRY POINT)
├── app/
│   ├── mood_detection.py
│   ├── memory_graph.py
│   ├── insights_engine.py
│   ├── user_profile.py
│   ├── ui.py
│   └── utils/
├── requirements.txt
└── data/
```

### 🎯 Features Available After Deployment
- ✅ Dashboard with real-time metrics
- ✅ Mood detection via image upload
- ✅ Cognitive memory graph
- ✅ AI-powered insights and recommendations
- ✅ User profile management

### 📦 Dependencies
All required dependencies are in `requirements.txt` and will be automatically installed by Streamlit Cloud:
- Streamlit
- PyTorch & TorchVision
- TensorFlow
- Sentence-Transformers
- OpenCV (headless version)
- FER (Facial Expression Recognition)
- And more...

### ⚙️ Configuration
The repository includes a `.streamlit/config.toml` file with optimized settings for Streamlit Cloud deployment.

---

## Troubleshooting

### Issue: "File not found" error
**Solution:** Make sure you entered `main.py` (not `app/main.py`)

### Issue: Long deployment time
**Solution:** First deployment takes 5-10 minutes as it downloads and installs all AI models and dependencies. Subsequent deployments are faster.

### Issue: Memory issues
**Solution:** Streamlit Cloud free tier has limited memory. If you encounter memory issues, consider:
- Using Streamlit Cloud's paid tiers
- Deploying to Render.com (see `DEPLOYMENT_GUIDE.md`)

---

## Alternative Deployment: Render.com

If you prefer Render.com for more resources:
1. See `DEPLOYMENT_GUIDE.md` for detailed instructions
2. The `render.yaml` file is already configured
3. Start command uses: `streamlit run main.py`

---

## Support

If you have any issues:
1. Double-check the main file path is `main.py`
2. Verify your repository is pushed to GitHub
3. Check Streamlit Cloud logs for any error messages
4. See `README.md` for local testing instructions

---

**Last Updated:** 2025-11-24  
**Status:** ✅ Ready for Streamlit Cloud Deployment

**Main File Path:** `main.py` (root directory)
