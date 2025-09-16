#!/usr/bin/env python3
"""
PLAYALTER Production Environment Validator
Validates all configurations before deployment to www.playalter.com
"""

import os
import sys
import json
import requests
from pathlib import Path

def check_environment_variables():
    """Check if all required environment variables are set"""
    print("🔍 Checking Environment Variables...")
    
    # Check backend .env
    backend_env = Path("backend/.env")
    if not backend_env.exists():
        print("❌ Backend .env file not found")
        return False
    
    # Check frontend .env  
    frontend_env = Path("frontend/.env")
    if not frontend_env.exists():
        print("❌ Frontend .env file not found")
        return False
    
    # Read and validate frontend environment
    with open(frontend_env, 'r') as f:
        frontend_content = f.read()
        
    if "www.playalter.com" not in frontend_content:
        print("❌ Frontend not configured for www.playalter.com domain")
        return False
    
    if "VITE_NODE_ENV=production" not in frontend_content:
        print("❌ Frontend not set to production mode")
        return False
    
    print("✅ Environment variables configured correctly")
    return True

def check_vercel_config():
    """Check Vercel configuration"""
    print("\n🔍 Checking Vercel Configuration...")
    
    vercel_json = Path("vercel.json")
    if not vercel_json.exists():
        print("❌ vercel.json not found")
        return False
    
    with open(vercel_json, 'r') as f:
        config = json.load(f)
    
    # Check domain aliases
    aliases = config.get("alias", [])
    if "www.playalter.com" not in aliases:
        print("❌ www.playalter.com not in Vercel aliases")
        return False
    
    # Check CORS configuration
    headers = config.get("headers", [])
    cors_configured = False
    for header_config in headers:
        if any("Access-Control-Allow-Origin" in h.get("key", "") for h in header_config.get("headers", [])):
            cors_configured = True
            break
    
    if not cors_configured:
        print("❌ CORS not configured in vercel.json")
        return False
    
    print("✅ Vercel configuration is correct")
    return True

def check_dependencies():
    """Check if all dependencies are installed"""
    print("\n🔍 Checking Dependencies...")
    
    # Check backend dependencies
    backend_reqs = Path("backend/requirements_enhanced.txt")
    if not backend_reqs.exists():
        print("❌ Backend requirements file not found")
        return False
    
    # Check frontend dependencies
    frontend_package = Path("frontend/package.json")
    node_modules = Path("frontend/node_modules")
    
    if not frontend_package.exists():
        print("❌ Frontend package.json not found")
        return False
    
    if not node_modules.exists():
        print("⚠️  Frontend node_modules not found - run 'npm install' in frontend/")
        return False
    
    print("✅ Dependencies are ready")
    return True

def check_file_structure():
    """Check if all required files exist"""
    print("\n🔍 Checking File Structure...")
    
    required_files = [
        "backend/app_enhanced.py",
        "backend/platform_orchestrator.py", 
        "frontend/src/App.jsx",
        "frontend/index.html",
        "vercel.json",
        "PROJECT_SUMMARY.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def check_backend_integration():
    """Check backend integration capabilities"""
    print("\n🔍 Checking Backend Integration...")
    
    try:
        # Import the backend app to check for import errors
        sys.path.append('backend')
        import app_enhanced
        
        # Check if critical integrations are imported
        required_modules = [
            'stripe', 'requests', 'flask', 'flask_cors'
        ]
        
        for module in required_modules:
            try:
                __import__(module)
            except ImportError:
                print(f"❌ Missing required module: {module}")
                return False
        
        print("✅ Backend integrations ready")
        return True
        
    except Exception as e:
        print(f"❌ Backend import error: {str(e)}")
        return False

def validate_hierarchical_ai_system():
    """Validate hierarchical AI agent system"""
    print("\n🔍 Checking Hierarchical AI Agent System...")
    
    try:
        sys.path.append('backend')
        from platform_orchestrator import PlatformOrchestrator
        
        # Check if the orchestrator has the required methods
        orchestrator = PlatformOrchestrator()
        
        required_methods = [
            'orchestrate_mask_stream',
            '_initialize_agents',
            '_master_agent_decide',
            '_replicate_agent_process_mask',
            '_agora_agent_setup_stream'
        ]
        
        for method in required_methods:
            if not hasattr(orchestrator, method):
                print(f"❌ Missing orchestrator method: {method}")
                return False
        
        print("✅ Hierarchical AI Agent system ready")
        return True
        
    except Exception as e:
        print(f"❌ AI system validation error: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("🚀 PLAYALTER Production Deployment Validator")
    print("Target Domain: www.playalter.com")
    print("=" * 50)
    
    checks = [
        check_environment_variables,
        check_vercel_config,
        check_dependencies,
        check_file_structure,
        check_backend_integration,
        validate_hierarchical_ai_system
    ]
    
    all_passed = True
    for check in checks:
        if not check():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Ready for deployment to www.playalter.com")
        print("\nNext steps:")
        print("1. Run: vercel --prod")
        print("2. Test: ./test-production.sh")
        print("3. Monitor: https://www.playalter.com/api/health")
        return 0
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before deployment")
        return 1

if __name__ == "__main__":
    sys.exit(main())
