#!/bin/bash
# Startup script for LifeUnity AI Cognitive Twin System - Render.com

echo "🧠 Starting LifeUnity AI - Cognitive Twin System..."
echo "=================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python version: $python_version"

# Create necessary directories
mkdir -p data logs
echo "✓ Created data and logs directories"

# Start Streamlit with Render-specific configuration
echo ""
echo "🚀 Launching Streamlit application on Render..."
echo "=================================================="
echo ""

streamlit run app/main.py --server.port $PORT --server.address 0.0.0.0
