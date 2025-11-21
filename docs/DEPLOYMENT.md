# Deployment Guide

This guide provides detailed instructions for deploying LifeUnity AI — Cognitive Twin System to various cloud platforms.

## Table of Contents
- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Render Deployment](#render-deployment)
- [HuggingFace Spaces Deployment](#huggingface-spaces-deployment)
- [Docker Deployment](#docker-deployment)

---

## Streamlit Cloud Deployment

Streamlit Cloud is the easiest way to deploy this application.

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://share.streamlit.io)

### Steps

1. **Fork or push this repository to your GitHub account**

2. **Go to [Streamlit Cloud](https://share.streamlit.io)**

3. **Click "New app"**

4. **Configure the app:**
   - Repository: `your-username/lifeunity-ai-cognitive-twin`
   - Branch: `main`
   - Main file path: `app/main.py`

5. **Advanced settings (optional):**
   - Python version: 3.9 or higher
   - Environment variables: None required

6. **Click "Deploy"**

7. **Wait for deployment** (may take 5-10 minutes for first deployment)

8. **Access your app** at `https://[your-app-name].streamlit.app`

### Troubleshooting
- If deployment fails, check the logs in Streamlit Cloud
- Ensure all dependencies in requirements.txt are compatible
- Large models (like transformers) may take time to download on first run

---

## Render Deployment

Render provides free web service hosting with automatic deployments.

### Prerequisites
- GitHub account
- Render account (free at https://render.com)

### Steps

1. **Push this repository to GitHub**

2. **Go to [Render Dashboard](https://dashboard.render.com)**

3. **Click "New +" and select "Web Service"**

4. **Connect your GitHub repository**

5. **Configure the service:**
   - Name: `lifeunity-ai-cognitive-twin`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app/main.py --server.port=$PORT --server.address=0.0.0.0`

6. **Select the free plan**

7. **Advanced settings:**
   - Auto-Deploy: Yes (recommended)
   - Environment variables: None required

8. **Click "Create Web Service"**

9. **Wait for deployment** (first deployment may take 10-15 minutes)

10. **Access your app** at the provided Render URL

### Using render.yaml (Alternative)

The repository includes a `render.yaml` file. You can:

1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically use `render.yaml` configuration

---

## HuggingFace Spaces Deployment

HuggingFace Spaces provides free hosting with GPU support options.

### Prerequisites
- HuggingFace account (free at https://huggingface.co)

### Steps

1. **Go to [HuggingFace Spaces](https://huggingface.co/spaces)**

2. **Click "Create new Space"**

3. **Configure the Space:**
   - Owner: Your username
   - Space name: `lifeunity-ai-cognitive-twin`
   - License: MIT
   - Select SDK: **Streamlit**
   - Space hardware: CPU basic (free) or GPU (paid)
   - Visibility: Public or Private

4. **Click "Create Space"**

5. **Clone the Space repository:**
   ```bash
   git clone https://huggingface.co/spaces/[your-username]/lifeunity-ai-cognitive-twin
   ```

6. **Copy files to the Space:**
   ```bash
   cp -r app requirements.txt README.md render.yaml [space-directory]/
   ```

7. **Create a simple `app.py` at the root:**
   ```python
   # app.py - Entry point for HuggingFace Spaces
   import os
   import sys
   
   # Add app directory to path
   sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))
   
   # Import and run main
   from app.main import main
   
   if __name__ == "__main__":
       main()
   ```

8. **Push to HuggingFace:**
   ```bash
   cd [space-directory]
   git add .
   git commit -m "Initial deployment"
   git push
   ```

9. **Wait for deployment** (automatic)

10. **Access your Space** at `https://huggingface.co/spaces/[your-username]/lifeunity-ai-cognitive-twin`

---

## Docker Deployment

For self-hosting or custom cloud deployments.

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY app/ ./app/
COPY README.md .

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run application
ENTRYPOINT ["streamlit", "run", "app/main.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t lifeunity-ai .

# Run container
docker run -p 8501:8501 lifeunity-ai
```

### Docker Compose (Optional)

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
```

---

## Post-Deployment

### Testing Your Deployment

1. **Open the application URL**
2. **Navigate through all pages:**
   - Dashboard
   - Mood Detection
   - Cognitive Memory
   - AI Insights
3. **Test core features:**
   - Upload an image for mood detection
   - Add a memory note
   - Generate a daily report
4. **Check for errors in logs**

### Monitoring

- **Streamlit Cloud:** Use built-in logs and metrics
- **Render:** Check logs in the Render dashboard
- **HuggingFace:** Use the Spaces logs tab
- **Docker:** Use `docker logs [container-id]`

### Updating Your Deployment

**Streamlit Cloud & Render:**
- Push changes to your GitHub repository
- Deployment updates automatically

**HuggingFace Spaces:**
- Push changes to the Space repository
- Rebuild happens automatically

**Docker:**
- Rebuild image: `docker build -t lifeunity-ai .`
- Restart container

---

## Troubleshooting

### Common Issues

**Out of Memory:**
- Use smaller models in `requirements.txt`
- Reduce batch sizes
- Upgrade to paid tier with more RAM

**Slow First Load:**
- Models download on first run (expected)
- Consider caching models in Docker image

**Port Issues:**
- Ensure using correct port for platform
- Streamlit Cloud: Auto-configured
- Render: Use `$PORT` environment variable
- HuggingFace: Port 7860 (default for Streamlit)

**Dependency Conflicts:**
- Check Python version (3.9+ recommended)
- Update requirements.txt versions
- Use virtual environment for testing

### Getting Help

- Check platform-specific documentation
- Open an issue on GitHub
- Contact platform support
- Review application logs

---

## Security Best Practices

1. **Environment Variables:**
   - Store secrets in platform-specific secrets management
   - Never commit sensitive data

2. **Data Privacy:**
   - User data stays in deployment
   - Consider adding authentication for production

3. **Updates:**
   - Keep dependencies updated
   - Monitor security advisories

4. **Backups:**
   - Regularly backup data directories
   - Use version control

---

For more information, see the main [README.md](../README.md)
