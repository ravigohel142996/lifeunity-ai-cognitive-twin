#!/bin/bash
# Startup script for LifeUnity AI Cognitive Twin System

echo "🧠 Starting LifeUnity AI - Cognitive Twin System..."
echo "=================================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1)
echo "✓ Python version: $python_version"

# Check if requirements are installed
echo ""
echo "📦 Checking dependencies..."

# Create necessary directories
mkdir -p data logs

echo "✓ Created data and logs directories"

# Start Streamlit
echo ""
echo "🚀 Launching Streamlit application..."
echo "=================================================="
echo ""

streamlit run app/main.py
