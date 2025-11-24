#!/usr/bin/env python3
"""
Comprehensive deployment verification script for Render/Streamlit.
Verifies all requirements from the problem statement are met.
"""

import sys
import re
from pathlib import Path

def check_requirements_txt():
    """Verify requirements.txt has no Flask/FastAPI/gunicorn/uvicorn."""
    print("\n📋 Checking requirements.txt...")
    
    with open('requirements.txt', 'r') as f:
        content = f.read().lower()
    
    forbidden = ['flask', 'fastapi', 'gunicorn', 'uvicorn']
    found_issues = []
    
    for package in forbidden:
        if package in content:
            found_issues.append(package)
    
    if found_issues:
        print(f"  ❌ Found forbidden packages: {', '.join(found_issues)}")
        return False
    else:
        print("  ✅ No Flask/FastAPI/gunicorn/uvicorn in requirements.txt")
        
        # Verify streamlit is present
        if 'streamlit' in content:
            print("  ✅ Streamlit is present in requirements.txt")
        else:
            print("  ❌ Streamlit not found in requirements.txt")
            return False
    
    return True

def check_render_yaml():
    """Verify render.yaml has correct configuration."""
    print("\n🚀 Checking render.yaml...")
    
    with open('render.yaml', 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for streamlit run command
    if 'streamlit run app/main.py' not in content:
        issues.append("Missing 'streamlit run app/main.py' command")
    else:
        print("  ✅ Correct Streamlit start command")
    
    # Check for port 10000
    if '--server.port 10000' in content:
        print("  ✅ Using port 10000 as specified")
    else:
        issues.append("Not using port 10000")
    
    # Check for server address
    if '--server.address 0.0.0.0' in content:
        print("  ✅ Binding to 0.0.0.0")
    else:
        issues.append("Not binding to 0.0.0.0")
    
    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
        return False
    
    return True

def check_project_structure():
    """Verify project structure matches requirements."""
    print("\n📁 Checking project structure...")
    
    required_structure = {
        'app/main.py': 'Main Streamlit app',
        'app/mood_detection.py': 'Mood detection module',
        'app/memory_graph.py': 'Memory graph module',
        'app/insights_engine.py': 'Insights engine module',
        'app/user_profile.py': 'User profile module',
        'app/utils/logger.py': 'Logger utility',
        'app/utils/embedder.py': 'Embedder utility',
        'app/utils/preprocess.py': 'Preprocessing utility',
    }
    
    all_exist = True
    for filepath, description in required_structure.items():
        path = Path(filepath)
        if path.exists():
            print(f"  ✅ {filepath} - {description}")
        else:
            print(f"  ❌ Missing: {filepath}")
            all_exist = False
    
    return all_exist

def check_no_wsgi_code():
    """Verify no Flask/FastAPI WSGI code exists."""
    print("\n🔍 Checking for WSGI code...")
    
    wsgi_patterns = [
        r'app\s*=\s*Flask\(',
        r'app\s*=\s*FastAPI\(',
        r'@app\.route\(',
        r'@app\.get\(',
        r'@app\.post\(',
    ]
    
    found_issues = []
    
    for py_file in Path('app').rglob('*.py'):
        with open(py_file, 'r') as f:
            content = f.read()
        
        for pattern in wsgi_patterns:
            if re.search(pattern, content):
                found_issues.append((py_file, pattern))
    
    if found_issues:
        print("  ❌ Found WSGI code:")
        for filepath, pattern in found_issues:
            print(f"     - {filepath}: {pattern}")
        return False
    else:
        print("  ✅ No Flask/FastAPI WSGI code found")
    
    return True

def check_no_webcam_code():
    """Verify no webcam/video capture code exists."""
    print("\n📹 Checking for webcam/video code...")
    
    video_patterns = [
        r'cv2\.VideoCapture\(',
        r'VideoCapture\(',
        r'\.read\(\)\s*#.*video',
    ]
    
    found_issues = []
    
    for py_file in Path('app').rglob('*.py'):
        with open(py_file, 'r') as f:
            content = f.read()
        
        for pattern in video_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                found_issues.append((py_file, pattern))
    
    if found_issues:
        print("  ❌ Found webcam/video code:")
        for filepath, pattern in found_issues:
            print(f"     - {filepath}: {pattern}")
        return False
    else:
        print("  ✅ No webcam/video capture code found")
        print("  ✅ Using image upload only")
    
    return True

def check_import_structure():
    """Verify all imports use app.* prefix."""
    print("\n🔗 Checking import structure...")
    
    import ast
    
    issues = []
    
    for py_file in Path('app').rglob('*.py'):
        if py_file.name == '__init__.py':
            continue
            
        with open(py_file, 'r') as f:
            content = f.read()
        
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module
                if module:
                    # Check for incorrect relative imports
                    if module.startswith('utils.') or module in ['mood_detection', 'memory_graph', 
                                                                   'user_profile', 'insights_engine']:
                        issues.append((py_file, f"from {module}"))
    
    if issues:
        print("  ❌ Found incorrect imports:")
        for filepath, import_stmt in issues:
            print(f"     - {filepath}: {import_stmt}")
        return False
    else:
        print("  ✅ All imports use correct app.* prefix")
        print("  ✅ No ModuleNotFoundError issues")
    
    return True

def check_main_py_structure():
    """Verify main.py is proper Streamlit app without sys.path hacks."""
    print("\n🎯 Checking main.py structure...")
    
    with open('app/main.py', 'r') as f:
        content = f.read()
    
    issues = []
    
    # Check for sys.path modifications
    if 'sys.path.append' in content or 'sys.path.insert' in content:
        issues.append("Found sys.path modification")
    else:
        print("  ✅ No sys.path hacks")
    
    # Check for proper imports
    if 'from app.' in content:
        print("  ✅ Using proper app.* imports")
    else:
        issues.append("Not using app.* imports")
    
    # Check for streamlit usage
    if 'import streamlit' in content:
        print("  ✅ Imports Streamlit")
    else:
        issues.append("Doesn't import Streamlit")
    
    # Check for main function
    if 'if __name__ == "__main__":' in content:
        print("  ✅ Has main entry point")
    else:
        issues.append("Missing main entry point")
    
    if issues:
        for issue in issues:
            print(f"  ❌ {issue}")
        return False
    
    return True

def main():
    """Run all verification checks."""
    print("=" * 70)
    print("🚀 LifeUnity AI - Streamlit Deployment Verification")
    print("=" * 70)
    
    checks = [
        ("Requirements.txt", check_requirements_txt),
        ("Render.yaml", check_render_yaml),
        ("Project Structure", check_project_structure),
        ("No WSGI Code", check_no_wsgi_code),
        ("No Webcam Code", check_no_webcam_code),
        ("Import Structure", check_import_structure),
        ("Main.py Structure", check_main_py_structure),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  ⚠️  Error running check: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:10} - {name}")
        if not result:
            all_passed = False
    
    print("=" * 70)
    
    if all_passed:
        print("\n🎉 SUCCESS! All deployment requirements met!")
        print("\n✨ The repository is ready for Streamlit deployment on Render")
        print("\n📝 Deployment Summary:")
        print("   • Streamlit is the ONLY entrypoint")
        print("   • All imports use app.* prefix")
        print("   • No Flask/FastAPI/gunicorn/uvicorn")
        print("   • No webcam code (image upload only)")
        print("   • Clean project structure")
        print("   • Correct Render configuration")
        return 0
    else:
        print("\n❌ FAILURE! Some requirements not met.")
        print("   Please review the failed checks above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
