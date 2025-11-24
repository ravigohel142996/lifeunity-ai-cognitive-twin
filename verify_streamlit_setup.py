"""
Verification script for Streamlit Cloud deployment setup.
This script validates the repository structure and configuration.
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and report status."""
    if Path(filepath).exists():
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ MISSING {description}: {filepath}")
        return False

def check_main_py_location():
    """Verify main.py is in the root directory."""
    print("\n=== Checking main.py location ===")
    root_main = check_file_exists("main.py", "Main Streamlit app (root)")
    app_main_should_not_exist = not Path("app/main.py").exists()
    
    if app_main_should_not_exist:
        print("✓ app/main.py does NOT exist (correct)")
    else:
        print("✗ WARNING: app/main.py exists but should not (will cause confusion)")
    
    return root_main and app_main_should_not_exist

def check_app_structure():
    """Verify the app module structure."""
    print("\n=== Checking app module structure ===")
    checks = [
        ("app/__init__.py", "App package marker"),
        ("app/mood_detection.py", "Mood detection module"),
        ("app/memory_graph.py", "Memory graph module"),
        ("app/insights_engine.py", "Insights engine module"),
        ("app/user_profile.py", "User profile module"),
        ("app/ui.py", "UI components module"),
        ("app/utils/__init__.py", "Utils package marker"),
        ("app/utils/logger.py", "Logger utility"),
        ("app/utils/embedder.py", "Embedder utility"),
        ("app/utils/preprocess.py", "Preprocess utility"),
    ]
    
    all_exist = True
    for filepath, description in checks:
        if not check_file_exists(filepath, description):
            all_exist = False
    
    return all_exist

def check_deployment_files():
    """Verify deployment configuration files."""
    print("\n=== Checking deployment files ===")
    checks = [
        ("requirements.txt", "Dependencies file"),
        ("render.yaml", "Render configuration"),
        (".streamlit/config.toml", "Streamlit config (optional)"),
        ("STREAMLIT_CLOUD_DEPLOYMENT.md", "Streamlit Cloud guide"),
    ]
    
    all_exist = True
    for filepath, description in checks:
        # Optional files don't fail the check
        exists = check_file_exists(filepath, description)
        if not exists and "optional" not in description.lower():
            all_exist = False
    
    return all_exist

def check_main_py_imports():
    """Verify main.py has correct imports."""
    print("\n=== Checking main.py imports ===")
    try:
        with open("main.py", "r") as f:
            content = f.read()
        
        required_imports = [
            "from app.mood_detection import",
            "from app.memory_graph import",
            "from app.user_profile import",
            "from app.insights_engine import",
            "from app import ui",
            "import streamlit",
        ]
        
        all_correct = True
        for imp in required_imports:
            if imp in content:
                print(f"✓ Found: {imp}")
            else:
                print(f"✗ MISSING: {imp}")
                all_correct = False
        
        # Check for bad imports
        bad_imports = [
            "sys.path.append",
            "from utils import",  # Should be app.utils
        ]
        
        for bad in bad_imports:
            if bad in content:
                print(f"✗ WARNING: Found problematic import: {bad}")
                all_correct = False
        
        return all_correct
    except Exception as e:
        print(f"✗ Error reading main.py: {e}")
        return False

def verify_render_yaml():
    """Verify render.yaml has correct configuration."""
    print("\n=== Checking render.yaml configuration ===")
    try:
        with open("render.yaml", "r") as f:
            content = f.read()
        
        if "streamlit run main.py" in content:
            print("✓ Start command uses 'main.py' (correct)")
            return True
        elif "streamlit run app/main.py" in content:
            print("✗ ERROR: Start command uses 'app/main.py' (incorrect)")
            print("  Should be: streamlit run main.py")
            return False
        else:
            print("⚠ Could not verify start command in render.yaml")
            return True  # Don't fail on this
    except Exception as e:
        print(f"⚠ Could not read render.yaml: {e}")
        return True  # Don't fail if file missing

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("Streamlit Cloud Deployment Verification")
    print("=" * 60)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Run all checks
    results = [
        check_main_py_location(),
        check_app_structure(),
        check_deployment_files(),
        check_main_py_imports(),
        verify_render_yaml(),
    ]
    
    # Summary
    print("\n" + "=" * 60)
    if all(results):
        print("✓ ALL CHECKS PASSED")
        print("\nFor Streamlit Cloud deployment:")
        print("  Repository: ravigohel142996/lifeunity-ai-cognitive-twin")
        print("  Branch: main")
        print("  Main file path: main.py")
        print("\nSee STREAMLIT_CLOUD_DEPLOYMENT.md for detailed instructions.")
        print("=" * 60)
        sys.exit(0)
    else:
        print("✗ SOME CHECKS FAILED")
        print("\nPlease fix the issues above before deploying.")
        print("=" * 60)
        sys.exit(1)

if __name__ == "__main__":
    main()
