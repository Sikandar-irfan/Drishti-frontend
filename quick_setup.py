#!/usr/bin/env python3
"""
Quick Setup Script for Sentinel View System
Handles complete setup, discovery, and deployment in one go.
"""

import subprocess
import sys
import os
import json
import time
from pathlib import Path

def run_command(command, shell=False):
    """Run a command and return the result."""
    try:
        if isinstance(command, str) and not shell:
            command = command.split()
        
        result = subprocess.run(
            command, 
            capture_output=True, 
            text=True,
            shell=shell
        )
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def check_prerequisites():
    """Check if all prerequisites are available."""
    print("🔍 Checking prerequisites...")
    
    # Check Node.js
    success, stdout, stderr = run_command("node --version")
    if not success:
        print("❌ Node.js not found. Please install Node.js first.")
        return False
    print(f"✅ Node.js: {stdout.strip()}")
    
    # Check npm
    success, stdout, stderr = run_command("npm --version")
    if not success:
        print("❌ npm not found. Please install npm first.")
        return False
    print(f"✅ npm: {stdout.strip()}")
    
    # Check Python
    success, stdout, stderr = run_command("python --version")
    if not success:
        print("❌ Python not found. Please install Python first.")
        return False
    print(f"✅ Python: {stdout.strip()}")
    
    # Check git
    success, stdout, stderr = run_command("git --version")
    if not success:
        print("❌ Git not found. Please install Git first.")
        return False
    print(f"✅ Git: {stdout.strip()}")
    
    return True

def install_dependencies():
    """Install npm dependencies."""
    print("\n📦 Installing dependencies...")
    success, stdout, stderr = run_command("npm install")
    if not success:
        print(f"❌ Failed to install dependencies: {stderr}")
        return False
    print("✅ Dependencies installed successfully")
    return True

def discover_rpi():
    """Run RPi discovery."""
    print("\n🔍 Discovering Raspberry Pi...")
    success, stdout, stderr = run_command("python discover_rpi.py")
    if not success:
        print(f"❌ RPi discovery failed: {stderr}")
        return False
    print("✅ Raspberry Pi discovered and configured")
    return True

def build_frontend():
    """Build the frontend."""
    print("\n🏗️ Building frontend...")
    success, stdout, stderr = run_command("npm run build:prod")
    if not success:
        print(f"❌ Build failed: {stderr}")
        return False
    print("✅ Frontend built successfully")
    return True

def deploy_to_github():
    """Deploy to GitHub Pages."""
    print("\n🚀 Deploying to GitHub Pages...")
    success, stdout, stderr = run_command("npm run deploy")
    if not success:
        print(f"❌ GitHub Pages deployment failed: {stderr}")
        return False
    print("✅ Deployed to GitHub Pages successfully")
    return True

def deploy_to_rpi():
    """Deploy to Raspberry Pi."""
    print("\n🤖 Deploying to Raspberry Pi...")
    success, stdout, stderr = run_command("python auto_deploy.py --skip-github --skip-discovery")
    if not success:
        print(f"⚠️ RPi deployment failed: {stderr}")
        print("This is optional - GitHub Pages deployment is still working")
        return False
    print("✅ Deployed to Raspberry Pi successfully")
    return True

def main():
    """Main setup function."""
    print("🚀 Sentinel View System - Quick Setup")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Discover RPi
    if not discover_rpi():
        print("⚠️ RPi discovery failed, but continuing with manual configuration...")
        # Create basic env files
        with open('.env', 'w') as f:
            f.write("VITE_API_BASE_URL=http://192.168.1.100:5000\n")
            f.write("VITE_APP_TITLE=Sentinel View System\n")
            f.write("VITE_APP_VERSION=1.0.0\n")
        
        with open('.env.production', 'w') as f:
            f.write("VITE_API_BASE_URL=http://192.168.1.100:5000\n")
            f.write("VITE_APP_TITLE=Sentinel View System\n")
            f.write("VITE_APP_VERSION=1.0.0\n")
        
        print("📝 Created basic environment files. Please update the IP address manually.")
    
    # Build frontend
    if not build_frontend():
        sys.exit(1)
    
    # Deploy to GitHub Pages
    if not deploy_to_github():
        print("⚠️ GitHub Pages deployment failed. Check your repository settings.")
    
    # Deploy to RPi (optional)
    deploy_to_rpi()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("=" * 50)
    
    # Check if rpi_config.json exists
    rpi_config_path = Path("rpi_config.json")
    if rpi_config_path.exists():
        with open(rpi_config_path, 'r') as f:
            config = json.load(f)
        
        print(f"🌐 Raspberry Pi IP: {config.get('ip', 'Not found')}")
        print(f"🔗 RPi Web Interface: http://{config.get('ip', 'localhost')}:8080")
    
    # Get GitHub username from git config or package.json
    success, stdout, stderr = run_command("git config user.name")
    if success:
        username = stdout.strip()
        print(f"📱 Custom Domain: https://drishti-asb.duckdns.org/")
        print(f"📱 GitHub Pages: https://{username.lower()}.github.io/Drishti-frontend/")
    else:
        print("📱 GitHub Pages: Check your repository settings for the URL")
    
    print("\n📋 Available Commands:")
    print("  npm run dev          - Start development server")
    print("  npm run build:prod   - Build for production")
    print("  npm run deploy       - Deploy to GitHub Pages")
    print("  npm run discover     - Rediscover Raspberry Pi")
    print("  npm run auto-deploy  - Deploy to both GitHub and RPi")
    
    print("\n🔧 Configuration Files:")
    print("  .env                 - Development environment")
    print("  .env.production      - Production environment")
    print("  rpi_config.json      - RPi discovery results")
    
    print("\nSetup completed successfully! 🎉")

if __name__ == "__main__":
    main()