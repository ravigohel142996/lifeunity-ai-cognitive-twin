#!/usr/bin/env python3
"""
Test script to verify import structure for Streamlit deployment.
This verifies that all imports use the correct app.* prefix.
"""

import sys
import ast
from pathlib import Path

def check_imports_in_file(filepath):
    """Check if a file uses correct import structure."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"  ⚠️  Syntax error in {filepath}")
        return False
    
    issues = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = node.module
            if module:
                # Check for relative imports without app prefix
                incorrect_modules = ['utils.', 'mood_detection', 'memory_graph', 
                                     'user_profile', 'insights_engine']
                if any(module.startswith(prefix) for prefix in incorrect_modules):
                    if not module.startswith('app.'):
                        issues.append(f"Relative import: from {module}")
    
    if issues:
        print(f"  ❌ {filepath.name}:")
        for issue in issues:
            print(f"     - {issue}")
        return False
    else:
        print(f"  ✅ {filepath.name}: All imports correct")
        return True

def main():
    """Main test function."""
    print("=" * 60)
    print("Testing Import Structure for Streamlit Deployment")
    print("=" * 60)
    
    app_dir = Path(__file__).parent / 'app'
    
    all_correct = True
    
    # Check main files
    print("\n📁 Checking main app files:")
    for py_file in ['main.py', 'mood_detection.py', 'memory_graph.py', 
                    'user_profile.py', 'insights_engine.py']:
        filepath = app_dir / py_file
        if filepath.exists():
            if not check_imports_in_file(filepath):
                all_correct = False
    
    # Check utils files
    print("\n📁 Checking utils files:")
    utils_dir = app_dir / 'utils'
    for py_file in utils_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            if not check_imports_in_file(py_file):
                all_correct = False
    
    print("\n" + "=" * 60)
    if all_correct:
        print("✅ SUCCESS: All imports use correct app.* prefix")
        print("✅ Project is ready for Streamlit deployment on Render")
    else:
        print("❌ FAILURE: Some imports need fixing")
        return 1
    
    print("=" * 60)
    return 0

if __name__ == "__main__":
    sys.exit(main())
