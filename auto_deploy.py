#!/usr/bin/env python3
"""
Complete Deployment Script
Auto-discovers RPi, builds frontend, and deploys to both GitHub Pages and RPi
"""

import os
import subprocess
import sys
import json
import time
from discover_rpi import RaspberryPiDiscovery

def run_command(command, description, capture_output=False):
    """Run a command with proper error handling"""
    print(f"🔄 {description}...")
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {description} - Success")
                return result.stdout
            else:
                print(f"❌ {description} - Failed")
                print(f"Error: {result.stderr}")
                return None
        else:
            result = subprocess.run(command, shell=True)
            if result.returncode == 0:
                print(f"✅ {description} - Success")
                return True
            else:
                print(f"❌ {description} - Failed")
                return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def deploy_to_rpi(rpi_ip, username="srihari"):
    """Deploy built frontend to Raspberry Pi"""
    print(f"\n📡 DEPLOYING TO RASPBERRY PI ({rpi_ip})")
    print("=" * 40)
    
    # Create web directory on RPi
    ssh_commands = [
        f"mkdir -p ~/autonomy_system/web/dist",
        f"rm -rf ~/autonomy_system/web/dist/*"
    ]
    
    for cmd in ssh_commands:
        full_cmd = f'ssh {username}@{rpi_ip} "{cmd}"'
        run_command(full_cmd, f"Preparing RPi directory: {cmd}")
    
    # Copy built files to RPi
    scp_cmd = f"scp -r dist/* {username}@{rpi_ip}:~/autonomy_system/web/dist/"
    if run_command(scp_cmd, "Copying built files to Raspberry Pi"):
        print(f"✅ Frontend deployed to RPi!")
        print(f"🌐 Access via: http://{rpi_ip}:5000/web")
        return True
    else:
        print("❌ Failed to deploy to RPi")
        return False

def create_rpi_web_server(rpi_ip, username="srihari"):
    """Create a simple web server script on RPi to serve the frontend"""
    web_server_script = '''#!/usr/bin/env python3
"""
Simple web server to serve the frontend on Raspberry Pi
"""

import http.server
import socketserver
import os
import sys

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="web/dist", **kwargs)
    
    def end_headers(self):
        # Add CORS headers
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

def main():
    port = 8080
    
    # Change to autonomy_system directory
    os.chdir(os.path.expanduser("~/autonomy_system"))
    
    if not os.path.exists("web/dist"):
        print("❌ Frontend not found. Deploy first with deployment script.")
        sys.exit(1)
    
    print(f"🌐 Starting web server on port {port}")
    print(f"📁 Serving from: {os.getcwd()}/web/dist")
    print(f"🔗 Access at: http://localhost:{port}")
    
    with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
        print(f"✅ Server running...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\n🛑 Server stopped")

if __name__ == "__main__":
    main()
'''
    
    # Write script to temp file and copy to RPi
    with open('temp_web_server.py', 'w') as f:
        f.write(web_server_script)
    
    scp_cmd = f"scp temp_web_server.py {username}@{rpi_ip}:~/autonomy_system/web_server.py"
    if run_command(scp_cmd, "Installing web server on RPi"):
        os.remove('temp_web_server.py')
        
        # Make executable
        chmod_cmd = f'ssh {username}@{rpi_ip} "chmod +x ~/autonomy_system/web_server.py"'
        run_command(chmod_cmd, "Making web server executable")
        
        print(f"✅ Web server installed on RPi")
        print(f"💡 Start with: ssh {username}@{rpi_ip} 'cd ~/autonomy_system && python3 web_server.py'")
        return True
    else:
        if os.path.exists('temp_web_server.py'):
            os.remove('temp_web_server.py')
        return False

def main():
    print("🚀 COMPLETE AUTONOMOUS SYSTEM DEPLOYMENT")
    print("=" * 50)
    
    # Step 1: Discover Raspberry Pi
    print("\n📡 STEP 1: DISCOVERING RASPBERRY PI")
    print("-" * 35)
    
    discovery = RaspberryPiDiscovery()
    
    # Try existing config first
    rpi_ip = None
    try:
        with open('rpi_config.json', 'r') as f:
            config = json.load(f)
        if discovery.check_rpi_api(config['rpi_ip']):
            rpi_ip = config['rpi_ip']
            print(f"✅ Using cached IP: {rpi_ip}")
    except:
        pass
    
    if not rpi_ip:
        rpi_ip = discovery.discover_raspberry_pi()
    
    if not rpi_ip:
        print("❌ Cannot proceed without Raspberry Pi")
        print("💡 Make sure RPi is running with autonomy system API")
        return False
    
    # Update configurations
    discovery.update_environment_files(rpi_ip)
    discovery.update_github_workflow(rpi_ip)
    discovery.save_config(rpi_ip)
    
    # Step 2: Install dependencies
    print("\n📦 STEP 2: INSTALLING DEPENDENCIES")
    print("-" * 35)
    
    if not run_command("npm install", "Installing npm dependencies"):
        return False
    
    # Step 3: Build frontend
    print("\n🔨 STEP 3: BUILDING FRONTEND")
    print("-" * 30)
    
    if not run_command("npm run build:prod", "Building production frontend"):
        return False
    
    # Step 4: Deploy to GitHub Pages
    print("\n🌐 STEP 4: GITHUB PAGES DEPLOYMENT")
    print("-" * 38)
    
    print("💡 Make sure you have:")
    print("   - Created GitHub repository")
    print("   - Pushed code to GitHub")
    print("   - Enabled GitHub Pages")
    
    deploy_github = input("\n🚀 Deploy to GitHub Pages? (y/n): ").lower().strip()
    if deploy_github == 'y':
        if run_command("npm run deploy", "Deploying to GitHub Pages"):
            print("✅ GitHub Pages deployment initiated!")
        else:
            print("⚠️ GitHub Pages deployment failed (you can try manually later)")
    
    # Step 5: Deploy to Raspberry Pi
    print(f"\n📡 STEP 5: RASPBERRY PI DEPLOYMENT")
    print("-" * 37)
    
    deploy_rpi = input(f"\n🚀 Deploy frontend to Raspberry Pi ({rpi_ip})? (y/n): ").lower().strip()
    if deploy_rpi == 'y':
        if deploy_to_rpi(rpi_ip):
            # Install web server
            create_rpi_web_server(rpi_ip)
        else:
            print("⚠️ RPi deployment failed")
    
    # Step 6: Summary
    print(f"\n🎉 DEPLOYMENT COMPLETE!")
    print("=" * 25)
    print(f"✅ Raspberry Pi IP: {rpi_ip}")
    print(f"🔗 Backend API: http://{rpi_ip}:5000")
    print(f"📹 Video Stream: http://{rpi_ip}:5000/video_feed")
    
    if deploy_github == 'y':
        print(f"🌐 GitHub Pages: https://sikandar-irfan.github.io/sentinel-view-system/")
    
    if deploy_rpi == 'y':
        print(f"🏠 RPi Frontend: http://{rpi_ip}:8080")
        print(f"💡 Start RPi web server: ssh srihari@{rpi_ip} 'cd ~/autonomy_system && python3 web_server.py'")
    
    print(f"\n📋 Configuration saved to rpi_config.json")
    print(f"🔄 Re-run this script anytime to auto-discover and redeploy!")
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Deployment cancelled by user")
    except Exception as e:
        print(f"\n❌ Deployment error: {e}")
        sys.exit(1)