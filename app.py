"""
HuggingFace Spaces Entry Point for LifeUnity AI - Cognitive Twin System
This file serves as the main entry point when deployed on HuggingFace Spaces.
"""

import sys
import os

# Add the current directory to Python path to ensure imports work
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main Streamlit app
if __name__ == "__main__":
    # HuggingFace Spaces will automatically run this with streamlit
    import subprocess
    subprocess.run(["streamlit", "run", "app/main.py", "--server.port=7860", "--server.address=0.0.0.0"])
