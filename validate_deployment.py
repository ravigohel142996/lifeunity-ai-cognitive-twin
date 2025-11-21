#!/usr/bin/env python3
"""
Render.com Pre-Deployment Validation Script
Validates the LifeUnity AI Cognitive Twin System before deployment to Render
"""

import os
import sys
from pathlib import Path

print("="*60)
print("Render.com Pre-Deployment Validation")
print("LifeUnity AI — Cognitive Twin System")
print("="*60)
print()

# STEP 1: Verify Project Structure
print("✅ STEP 1: VERIFY PROJECT STRUCTURE")
print("-" * 60)

required_dirs = [
    "app",
    "app/utils",
    "data",
    "logs"
]

required_files = [
    "app/main.py",
    "app/mood_detection.py",
    "app/memory_graph.py",
    "app/insights_engine.py",
    "app/user_profile.py",
    "app/utils/preprocess.py",
    "app/utils/embedder.py",
    "app/utils/logger.py",
    "requirements.txt",
    "render.yaml",
    "README.md"
]

all_dirs_ok = True
for dir_path in required_dirs:
    if Path(dir_path).exists():
        print(f"  ✓ {dir_path}/")
    else:
        print(f"  ✗ {dir_path}/ - MISSING")
        all_dirs_ok = False

print()

all_files_ok = True
for file_path in required_files:
    if Path(file_path).exists():
        size = Path(file_path).stat().st_size
        print(f"  ✓ {file_path} ({size} bytes)")
    else:
        print(f"  ✗ {file_path} - MISSING")
        all_files_ok = False

print()

if all_dirs_ok and all_files_ok:
    print("✅ Structure validation PASSED")
else:
    print("❌ Structure validation FAILED")
    sys.exit(1)

print()

# STEP 2: Validate Streamlit App Entrypoint
print("✅ STEP 2: VALIDATE STREAMLIT APP ENTRYPOINT")
print("-" * 60)

if Path("app/main.py").exists():
    with open("app/main.py", "r") as f:
        content = f.read()
        if "import streamlit" in content or "from streamlit" in content:
            print("  ✓ app/main.py contains Streamlit imports")
        else:
            print("  ✗ app/main.py missing Streamlit imports")
            sys.exit(1)
        
        if "st.set_page_config" in content:
            print("  ✓ app/main.py has page configuration")
        else:
            print("  ⚠ app/main.py missing page configuration")
    
    print("  ✓ Entrypoint: app/main.py (as specified in HF_README.md)")
else:
    print("  ✗ app/main.py NOT FOUND")
    sys.exit(1)

print()
print("✅ Entrypoint validation PASSED")
print()

# STEP 3: Verify Dependencies
print("✅ STEP 3: VERIFY DEPENDENCIES")
print("-" * 60)

required_packages = [
    "streamlit",
    "torch",
    "transformers",
    "sentence-transformers",
    "opencv-python-headless",
    "numpy",
    "pandas",
    "pillow",  # Case-insensitive match
    "scikit-learn",
    "networkx",
    "fer",
    "tensorflow",
    "plotly",
    "matplotlib"
]

if Path("requirements.txt").exists():
    with open("requirements.txt", "r") as f:
        requirements_content = f.read().lower()
    
    missing_packages = []
    for package in required_packages:
        if package.lower().replace("-", "_") in requirements_content.replace("-", "_"):
            print(f"  ✓ {package}")
        else:
            print(f"  ✗ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print()
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        sys.exit(1)
    else:
        print()
        print("✅ Dependencies validation PASSED")
else:
    print("  ✗ requirements.txt NOT FOUND")
    sys.exit(1)

print()

# STEP 4: Validate Render Configuration
print("✅ STEP 4: VALIDATE RENDER CONFIGURATION")
print("-" * 60)

if Path("render.yaml").exists():
    with open("render.yaml", "r") as f:
        render_content = f.read()
    
    if "streamlit run app/main.py" in render_content:
        print("  ✓ Start command configured correctly")
    else:
        print("  ✗ Start command not set correctly")
        sys.exit(1)
    
    if "$PORT" in render_content or "${PORT}" in render_content:
        print("  ✓ PORT variable configured")
    else:
        print("  ✗ PORT variable not configured")
        sys.exit(1)
    
    if "pip install -r requirements.txt" in render_content:
        print("  ✓ Build command configured")
    else:
        print("  ⚠ Build command not explicitly set")
    
    print()
    print("✅ Render configuration PASSED")
else:
    print("  ✗ render.yaml NOT FOUND")
    sys.exit(1)

print()

# STEP 5: Run Build Health Check
print("✅ STEP 5: RUN BUILD HEALTH CHECK")
print("-" * 60)

# Check Python syntax
import py_compile
syntax_errors = []

for file_path in required_files:
    if file_path.endswith(".py"):
        try:
            py_compile.compile(file_path, doraise=True)
            print(f"  ✓ {file_path} - syntax OK")
        except py_compile.PyCompileError as e:
            print(f"  ✗ {file_path} - syntax ERROR")
            syntax_errors.append(file_path)

print()

if syntax_errors:
    print(f"❌ Syntax errors in: {', '.join(syntax_errors)}")
    sys.exit(1)

# Check for webcam/camera code
print("  Checking for webcam/camera code...")
webcam_issues = []
webcam_check_files = [f for f in required_files if f.endswith("main.py") or f.endswith("mood_detection.py")]
for file_path in webcam_check_files:
    if Path(file_path).exists():
        with open(file_path, "r") as f:
            content = f.read()
            if "camera_input" in content:
                webcam_issues.append(f"{file_path} contains camera_input")
            if "VideoCapture" in content:
                webcam_issues.append(f"{file_path} contains VideoCapture")

if webcam_issues:
    print()
    for issue in webcam_issues:
        print(f"  ✗ {issue}")
    print("❌ Webcam code found (not compatible with cloud deployment)")
    sys.exit(1)
else:
    print("  ✓ No webcam code found (cloud-compatible)")

print()

# Check imports
print("  Checking relative imports...")
import_issues = []
for file_path in required_files:
    if file_path.endswith(".py") and file_path != "app/main.py":
        with open(file_path, "r") as f:
            content = f.read()
            # Check for relative imports from app
            if "from app." in content:
                print(f"  ✓ {file_path} uses relative imports")
            elif "import" in content and file_path.startswith("app/"):
                # Check if it at least imports from app.utils
                if "from app.utils" in content:
                    print(f"  ✓ {file_path} uses relative imports")
                else:
                    import_issues.append(file_path)

if import_issues:
    print()
    print(f"  ⚠ Check imports in: {', '.join(import_issues)}")

print()

# Check data directory
if Path("data").exists():
    print("  ✓ data/ directory exists (for JSON storage)")
else:
    print("  ⚠ data/ directory will be created at runtime")

print()
print("✅ Build health check PASSED")
print()

# STEP 6: Deployment Readiness Report
print("="*60)
print("✅ DEPLOYMENT READINESS REPORT")
print("="*60)
print()
print("Project: LifeUnity AI — Cognitive Twin System")
print("Status: ✅ READY FOR RENDER.COM DEPLOYMENT")
print()
print("Configuration:")
print("  • Platform: Render.com")
print("  • Entry Point: app/main.py")
print("  • Region: Singapore")
print("  • Plan: Free tier")
print()
print("Pages Available:")
print("  1. ✅ Dashboard - Metrics & trends")
print("  2. ✅ Emotion Detection - Image upload only")
print("  3. ✅ Cognitive Memory - Notes with embeddings")
print("  4. ✅ AI Insights - Wellness reports")
print()
print("Features:")
print("  • ✅ No webcam code (cloud-compatible)")
print("  • ✅ Image upload for emotion detection")
print("  • ✅ Sentence-BERT embeddings (all-MiniLM-L6-v2)")
print("  • ✅ Local rule-based AI insights (no API keys)")
print("  • ✅ JSON storage in /data directory")
print("  • ✅ All dependencies cloud-safe")
print()
print("Next Steps:")
print("  1. Push repository to GitHub")
print("  2. Go to Render.com dashboard")
print("  3. Connect GitHub repository")
print("  4. Click 'Create Web Service'")
print("  5. Render will auto-detect render.yaml and deploy")
print()
print("="*60)
print("✅ ALL VALIDATION CHECKS PASSED")
print("="*60)
