#!/usr/bin/env python3
"""
🦖 Restaceratops System Test
Comprehensive test of backend, frontend, and AI integration
"""

import asyncio
import requests
import json
import time
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

class RestaceratopsTester:
    def __init__(self):
        self.backend_url = "http://127.0.0.1:8000"
        self.frontend_url = "http://127.0.0.1:5173"
        self.test_results = {}
    
    def test_backend_health(self):
        """Test backend health endpoint"""
        try:
            print("🔍 Testing backend health...")
            response = requests.get(f"{self.backend_url}/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend health: {data.get('status', 'unknown')}")
                print(f"   AI System: {data.get('ai_system', 'unknown')}")
                print(f"   WebSocket Connections: {data.get('websocket_connections', 0)}")
                self.test_results['backend_health'] = True
                return True
            else:
                print(f"❌ Backend health failed: {response.status_code}")
                self.test_results['backend_health'] = False
                return False
        except Exception as e:
            print(f"❌ Backend health error: {e}")
            self.test_results['backend_health'] = False
            return False
    
    def test_ai_chat(self):
        """Test AI chat functionality"""
        try:
            print("🤖 Testing AI chat...")
            payload = {
                "message": "Hello! Can you help me create a test for a user API endpoint?"
            }
            response = requests.post(
                f"{self.backend_url}/api/chat",
                json=payload,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ AI Chat working: {data.get('response', '')[:100]}...")
                print(f"   Model: {data.get('ai_model', 'unknown')}")
                self.test_results['ai_chat'] = True
                return True
            else:
                print(f"❌ AI Chat failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.test_results['ai_chat'] = False
                return False
        except Exception as e:
            print(f"❌ AI Chat error: {e}")
            self.test_results['ai_chat'] = False
            return False
    
    def test_dashboard(self):
        """Test dashboard endpoint"""
        try:
            print("📊 Testing dashboard...")
            response = requests.get(f"{self.backend_url}/api/dashboard", timeout=10)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Dashboard working: {data.get('total_tests', 0)} total tests")
                print(f"   Success Rate: {data.get('success_rate', 0)}%")
                self.test_results['dashboard'] = True
                return True
            else:
                print(f"❌ Dashboard failed: {response.status_code}")
                self.test_results['dashboard'] = False
                return False
        except Exception as e:
            print(f"❌ Dashboard error: {e}")
            self.test_results['dashboard'] = False
            return False
    
    def test_file_upload(self):
        """Test file upload functionality"""
        try:
            print("📁 Testing file upload...")
            # Create a simple test file
            test_content = """
name: "Simple API Test"
description: "Test file upload functionality"
base_url: "https://httpbin.org"
tests:
  - name: "Test GET request"
    method: "GET"
    path: "/get"
    expected_status: 200
"""
            files = {'file': ('test_upload.yml', test_content, 'text/yaml')}
            response = requests.post(
                f"{self.backend_url}/api/upload",
                files=files,
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                print(f"✅ File upload working: {data.get('filename', 'unknown')}")
                self.test_results['file_upload'] = True
                return True
            else:
                print(f"❌ File upload failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.test_results['file_upload'] = False
                return False
        except Exception as e:
            print(f"❌ File upload error: {e}")
            self.test_results['file_upload'] = False
            return False
    
    def test_frontend(self):
        """Test frontend accessibility"""
        try:
            print("🌐 Testing frontend...")
            response = requests.get(self.frontend_url, timeout=10)
            if response.status_code == 200:
                print("✅ Frontend accessible")
                self.test_results['frontend'] = True
                return True
            else:
                print(f"❌ Frontend failed: {response.status_code}")
                self.test_results['frontend'] = False
                return False
        except Exception as e:
            print(f"❌ Frontend error: {e}")
            self.test_results['frontend'] = False
            return False
    
    def test_ai_system_direct(self):
        """Test AI system directly"""
        try:
            print("🧠 Testing AI system directly...")
            from core.agents.enhanced_ai_system import EnhancedAISystem
            
            ai = EnhancedAISystem()
            response = asyncio.run(ai.handle_conversation("Test the AI system"))
            
            if response and len(response) > 10:
                print(f"✅ AI system working: {response[:100]}...")
                self.test_results['ai_system_direct'] = True
                return True
            else:
                print("❌ AI system returned empty response")
                self.test_results['ai_system_direct'] = False
                return False
        except Exception as e:
            print(f"❌ AI system error: {e}")
            self.test_results['ai_system_direct'] = False
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("🦖 Starting Restaceratops System Test")
        print("=" * 50)
        
        tests = [
            ("Backend Health", self.test_backend_health),
            ("AI System Direct", self.test_ai_system_direct),
            ("AI Chat API", self.test_ai_chat),
            ("Dashboard API", self.test_dashboard),
            ("File Upload", self.test_file_upload),
            ("Frontend", self.test_frontend),
        ]
        
        passed = 0
        total = len(tests)
        
        for test_name, test_func in tests:
            print(f"\n🧪 {test_name}")
            print("-" * 30)
            try:
                if test_func():
                    passed += 1
            except Exception as e:
                print(f"❌ {test_name} crashed: {e}")
                self.test_results[test_name.lower().replace(' ', '_')] = False
        
        print("\n" + "=" * 50)
        print(f"📊 Test Results: {passed}/{total} tests passed")
        
        if passed == total:
            print("🎉 All tests passed! System is ready for deployment.")
            return True
        else:
            print("⚠️ Some tests failed. Check the issues above.")
            return False
    
    def print_summary(self):
        """Print test summary"""
        print("\n📋 Test Summary:")
        for test, result in self.test_results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test}: {status}")

def main():
    tester = RestaceratopsTester()
    success = tester.run_all_tests()
    tester.print_summary()
    
    if success:
        print("\n🚀 System is ready for deployment!")
        return 0
    else:
        print("\n🔧 Please fix the failing tests before deployment.")
        return 1

if __name__ == "__main__":
    exit(main()) 