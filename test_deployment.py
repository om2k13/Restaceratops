#!/usr/bin/env python3
"""
🦖 Deployment Test Script for Restaceratops
Tests the deployment configuration locally before pushing to production
"""

import subprocess
import sys
import os
from pathlib import Path

def test_requirements_installation():
    """Test if requirements.txt can be installed without issues"""
    print("🔧 Testing requirements installation...")
    
    try:
        # Test pip install with --dry-run
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "-r", "backend/requirements.txt", "--dry-run"
        ], capture_output=True, text=True, cwd=".")
        
        if result.returncode == 0:
            print("✅ Requirements installation test passed")
            return True
        else:
            print(f"❌ Requirements installation test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing requirements: {e}")
        return False

def test_imports():
    """Test if all critical imports work"""
    print("📦 Testing critical imports...")
    
    try:
        # Test FastAPI import
        import fastapi
        print(f"✅ FastAPI {fastapi.__version__} imported successfully")
        
        # Test Pydantic import
        import pydantic
        print(f"✅ Pydantic {pydantic.__version__} imported successfully")
        
        # Test other critical imports
        import uvicorn
        import httpx
        import motor
        import openai
        import yaml
        
        print("✅ All critical imports successful")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during imports: {e}")
        return False

def test_configuration_files():
    """Test if configuration files are valid"""
    print("📋 Testing configuration files...")
    
    try:
        # Check if requirements.txt exists
        if not Path("backend/requirements.txt").exists():
            print("❌ backend/requirements.txt not found")
            return False
            
        # Check if runtime.txt exists
        if not Path("backend/runtime.txt").exists():
            print("❌ backend/runtime.txt not found")
            return False
            
        # Check if render.yaml exists
        if not Path("render.yaml").exists():
            print("❌ render.yaml not found")
            return False
            
        # Read and validate requirements.txt
        with open("backend/requirements.txt", "r") as f:
            requirements = f.read()
            
        # Check for problematic packages that require Rust compilation
        problematic_packages = [
            "pydantic>=2.0.0",  # Requires Rust compilation
            "pydantic==2.0.0",
            "pydantic==2.1.0",
            "pydantic==2.2.0",
            "pydantic==2.3.0",
            "pydantic==2.4.0",
            "pydantic==2.5.0",
            "pydantic==2.6.0",
            "pydantic==2.7.0"
        ]
        
        for package in problematic_packages:
            if package in requirements:
                print(f"❌ Found problematic package: {package}")
                return False
        
        # Check for correct Pydantic version
        if "pydantic==1.10.13" not in requirements:
            print("❌ Pydantic version should be 1.10.13 to avoid Rust compilation")
            return False
                
        print("✅ Configuration files are valid")
        return True
        
    except Exception as e:
        print(f"❌ Error testing configuration: {e}")
        return False

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    # Check if version is compatible
    if version.major == 3 and version.minor >= 11:
        print("✅ Python version is compatible")
        return True
    else:
        print("❌ Python version may not be compatible (recommended: 3.11+)")
        return False

def test_package_compatibility():
    """Test package compatibility"""
    print("🔗 Testing package compatibility...")
    
    try:
        # Test FastAPI and Pydantic compatibility
        import fastapi
        import pydantic
        
        # Check if we're using compatible versions
        fastapi_version = fastapi.__version__
        pydantic_version = pydantic.__version__
        
        print(f"FastAPI version: {fastapi_version}")
        print(f"Pydantic version: {pydantic_version}")
        
        # FastAPI 0.95.2 should work with Pydantic 1.10.13
        if fastapi_version.startswith("0.95") and pydantic_version.startswith("1.10"):
            print("✅ FastAPI and Pydantic versions are compatible")
            return True
        else:
            print("⚠️ FastAPI and Pydantic versions may have compatibility issues")
            return False
            
    except Exception as e:
        print(f"❌ Error testing package compatibility: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🦖 Restaceratops Deployment Test Suite")
    print("=" * 50)
    
    tests = [
        test_python_version,
        test_configuration_files,
        test_requirements_installation,
        test_imports,
        test_package_compatibility
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Deployment should work correctly.")
        return 0
    else:
        print("⚠️ Some tests failed. Please fix issues before deploying.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 