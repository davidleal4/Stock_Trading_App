#!/usr/bin/env python3
"""
Test script to verify setup is working correctly
"""

import sys
import subprocess
import os
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a file exists"""
    if Path(file_path).exists():
        print(f"✅ {description}: {file_path}")
        return True
    else:
        print(f"❌ {description}: {file_path}")
        return False

def check_directory_structure():
    """Check if all required directories exist"""
    print("\n🏗️  Checking directory structure...")
    
    dirs_to_check = [
        ("backend", "Backend directory"),
        ("frontend", "Frontend directory"),
        ("ml", "ML service directory"),
        ("infra", "Infrastructure directory"),
        ("tests", "Tests directory"),
        ("backend/core", "Backend core"),
        ("backend/api", "Backend API"),
        ("backend/services", "Backend services"),
        ("frontend/src", "Frontend source"),
        ("frontend/src/components", "Frontend components"),
        ("ml/core", "ML core"),
        ("ml/services", "ML services"),
    ]
    
    all_good = True
    for dir_path, description in dirs_to_check:
        if Path(dir_path).exists() and Path(dir_path).is_dir():
            print(f"✅ {description}: {dir_path}")
        else:
            print(f"❌ {description}: {dir_path}")
            all_good = False
    
    return all_good

def check_key_files():
    """Check if key files exist"""
    print("\n📁 Checking key files...")
    
    files_to_check = [
        ("docker-compose.yml", "Docker Compose configuration"),
        ("backend/main.py", "Backend main application"),
        ("backend/requirements.txt", "Backend dependencies"),
        ("backend/Dockerfile", "Backend Docker config"),
        ("frontend/package.json", "Frontend dependencies"),
        ("frontend/Dockerfile", "Frontend Docker config"),
        ("frontend/src/app/page.tsx", "Frontend main page"),
        ("ml/main.py", "ML service main"),
        ("ml/requirements.txt", "ML dependencies"),
        ("ml/Dockerfile", "ML Docker config"),
        ("infra/init.sql", "Database initialization"),
        ("README.md", "Documentation"),
        (".gitignore", "Git ignore file"),
        (".env.example", "Environment example"),
    ]
    
    all_good = True
    for file_path, description in files_to_check:
        if not check_file_exists(file_path, description):
            all_good = False
    
    return all_good

def check_docker_compose():
    """Check if docker-compose configuration is valid"""
    print("\n🐳 Checking Docker Compose configuration...")
    
    try:
        result = subprocess.run(
            ["docker", "compose", "config", "--quiet"],
            cwd=".",
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Docker Compose configuration is valid")
            return True
        else:
            print(f"❌ Docker Compose configuration error: {result.stderr}")
            return False
    except FileNotFoundError:
        print("❌ Docker Compose not found")
        return False
    except Exception as e:
        print(f"❌ Error checking Docker Compose: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Stock Trading App - Setup Verification")
    print("=" * 50)
    
    # Change to project root
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    
    print(f"📍 Working directory: {os.getcwd()}")
    
    # Run checks
    checks = [
        ("Directory Structure", check_directory_structure),
        ("Key Files", check_key_files),
        ("Docker Compose", check_docker_compose),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Error in {check_name}: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n📊 Summary")
    print("=" * 20)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 All checks passed! Setup looks good.")
        print("\n🚀 To start the application:")
        print("   docker compose up --build")
        print("\n🌐 Access points:")
        print("   Frontend: http://localhost:3000")
        print("   Backend:  http://localhost:8000")
        print("   API Docs: http://localhost:8000/docs")
        return 0
    else:
        print("⚠️  Some checks failed. Please review the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())