"""
Basic import and initialization tests for LifeUnity AI modules.
Run this to verify all modules can be imported successfully.
"""

import sys
import os

# Add app directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing imports...")
    
    try:
        print("✓ Testing utils...")
        from app.utils import logger, preprocess, embedder
        print("  ✓ logger imported")
        print("  ✓ preprocess imported")
        print("  ✓ embedder imported")
        
        print("\n✓ Testing core modules...")
        from app import mood_detection, memory_graph, user_profile, insights_engine
        print("  ✓ mood_detection imported")
        print("  ✓ memory_graph imported")
        print("  ✓ user_profile imported")
        print("  ✓ insights_engine imported")
        
        print("\n✓ Testing main app...")
        # Don't import main since it will try to run Streamlit
        # Just check the file exists
        import app.main
        print("  ✓ main imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import failed: {e}")
        return False


def test_initialization():
    """Test that core objects can be initialized."""
    print("\n" + "="*50)
    print("Testing initialization...")
    
    try:
        from app.utils.logger import get_logger
        logger = get_logger("test")
        logger.info("Logger test")
        print("✓ Logger initialized")
        
        from app.user_profile import UserProfile
        profile = UserProfile(user_id="test_user")
        print("✓ UserProfile initialized")
        
        print("\n✅ All initializations successful!")
        return True
        
    except Exception as e:
        print(f"\n❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("="*50)
    print("LifeUnity AI - Module Tests")
    print("="*50 + "\n")
    
    imports_ok = test_imports()
    init_ok = test_initialization()
    
    print("\n" + "="*50)
    if imports_ok and init_ok:
        print("✅ ALL TESTS PASSED")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED")
        sys.exit(1)
