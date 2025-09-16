#!/usr/bin/env python3
"""
Dynamic Raspberry Pi Discovery and Configuration
Auto-discovers RPi on network and updates configuration dynamically
"""

import socket
import subprocess
import threading
import time
import json
import requests
from concurrent.futures import ThreadPoolExecutor
import os

class RaspberryPiDiscovery:
    def __init__(self):
        self.potential_ips = []
        self.confirmed_rpi_ip = None
        self.api_port = 5000
        
    def get_local_network_range(self):
        """Get local network range"""
        try:
            # Get local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            
            # Extract network base (assumes /24 subnet)
            network_base = '.'.join(local_ip.split('.')[:-1])
            return network_base
        except Exception:
            return "192.168.1"  # Default fallback
    
    def ping_host(self, ip):
        """Check if host is reachable"""
        try:
            result = subprocess.run(
                ['ping', '-n', '1', '-w', '1000', ip] if os.name == 'nt' else ['ping', '-c', '1', '-W', '1', ip],
                capture_output=True,
                timeout=2
            )
            return ip if result.returncode == 0 else None
        except:
            return None
    
    def check_rpi_api(self, ip):
        """Check if IP has our autonomy system API running"""
        try:
            response = requests.get(f"http://{ip}:{self.api_port}/api/system_status", timeout=3)
            if response.status_code == 200:
                data = response.json()
                # Check if it's our autonomy system
                if 'system_status' in data or 'cpu_usage' in data:
                    return ip
        except:
            pass
        return None
    
    def discover_raspberry_pi(self):
        """Discover Raspberry Pi with autonomy system"""
        print("🔍 Discovering Raspberry Pi on network...")
        
        # Get network range
        network_base = self.get_local_network_range()
        print(f"📡 Scanning network: {network_base}.1-254")
        
        # First, find reachable hosts
        reachable_hosts = []
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(self.ping_host, f"{network_base}.{i}") 
                for i in range(1, 255)
            ]
            
            for future in futures:
                result = future.result()
                if result:
                    reachable_hosts.append(result)
                    print(f"  📱 Found host: {result}")
        
        print(f"✅ Found {len(reachable_hosts)} reachable hosts")
        
        # Now check which ones have our API
        print("🔍 Checking for autonomy system API...")
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(self.check_rpi_api, ip) 
                for ip in reachable_hosts
            ]
            
            for future in futures:
                result = future.result()
                if result:
                    print(f"🎯 Found Raspberry Pi with autonomy system: {result}")
                    self.confirmed_rpi_ip = result
                    return result
        
        # If not found, try common RPi IPs
        common_ips = [f"{network_base}.{i}" for i in [101, 102, 103, 104, 105, 150, 200]]
        print("🔄 Checking common Raspberry Pi IP addresses...")
        
        for ip in common_ips:
            if self.check_rpi_api(ip):
                print(f"🎯 Found Raspberry Pi at common IP: {ip}")
                self.confirmed_rpi_ip = ip
                return ip
        
        print("❌ Raspberry Pi with autonomy system not found")
        return None
    
    def update_environment_files(self, rpi_ip):
        """Update .env files with discovered IP"""
        env_content = f"""# Dynamic configuration - Auto-generated
VITE_API_BASE_URL=http://{rpi_ip}:{self.api_port}
VITE_STREAM_URL=http://{rpi_ip}:{self.api_port}/video_feed
VITE_UPDATE_INTERVAL=2000
VITE_ENVIRONMENT=development
"""
        
        env_prod_content = f"""# Production configuration - Auto-generated
VITE_API_BASE_URL=http://{rpi_ip}:{self.api_port}
VITE_STREAM_URL=http://{rpi_ip}:{self.api_port}/video_feed
VITE_UPDATE_INTERVAL=2000
VITE_ENVIRONMENT=production
"""
        
        # Write .env files
        with open('.env', 'w') as f:
            f.write(env_content)
        
        with open('.env.production', 'w') as f:
            f.write(env_prod_content)
        
        print(f"✅ Updated .env files with IP: {rpi_ip}")
    
    def update_github_workflow(self, rpi_ip):
        """Update GitHub Actions workflow with discovered IP"""
        workflow_content = f"""name: Deploy to GitHub Pages

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v4

    - name: Setup Node.js
      uses: actions/setup-node@v4
      with:
        node-version: '18'
        cache: 'npm'

    - name: Install dependencies
      run: npm ci

    - name: Build for production
      run: npm run build
      env:
        VITE_API_BASE_URL: http://{rpi_ip}:{self.api_port}
        VITE_STREAM_URL: http://{rpi_ip}:{self.api_port}/video_feed
        VITE_UPDATE_INTERVAL: 2000
        VITE_ENVIRONMENT: production

    - name: Deploy to GitHub Pages
      uses: peaceiris/actions-gh-pages@v3
      if: github.ref == 'refs/heads/main' || github.ref == 'refs/heads/master'
      with:
        github_token: ${{{{ secrets.GITHUB_TOKEN }}}}
        publish_dir: ./dist
"""
        
        os.makedirs('.github/workflows', exist_ok=True)
        with open('.github/workflows/deploy.yml', 'w') as f:
            f.write(workflow_content)
        
        print(f"✅ Updated GitHub workflow with IP: {rpi_ip}")
    
    def save_config(self, rpi_ip):
        """Save configuration for future use"""
        config = {
            "rpi_ip": rpi_ip,
            "api_port": self.api_port,
            "last_updated": time.time(),
            "base_url": f"http://{rpi_ip}:{self.api_port}",
            "stream_url": f"http://{rpi_ip}:{self.api_port}/video_feed"
        }
        
        with open('rpi_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Saved configuration to rpi_config.json")

def main():
    print("🚀 DYNAMIC RASPBERRY PI DISCOVERY & CONFIGURATION")
    print("=" * 55)
    
    discovery = RaspberryPiDiscovery()
    
    # Try to load existing config first
    try:
        with open('rpi_config.json', 'r') as f:
            config = json.load(f)
        
        print(f"📁 Found existing config: {config['rpi_ip']}")
        
        # Test if it still works
        if discovery.check_rpi_api(config['rpi_ip']):
            print(f"✅ Existing IP {config['rpi_ip']} still works!")
            discovery.confirmed_rpi_ip = config['rpi_ip']
        else:
            print(f"❌ Existing IP {config['rpi_ip']} not reachable, discovering new...")
            discovery.discover_raspberry_pi()
    except FileNotFoundError:
        print("📁 No existing config found, discovering...")
        discovery.discover_raspberry_pi()
    
    if discovery.confirmed_rpi_ip:
        print(f"\n🎯 Using Raspberry Pi IP: {discovery.confirmed_rpi_ip}")
        
        # Update all configuration files
        discovery.update_environment_files(discovery.confirmed_rpi_ip)
        discovery.update_github_workflow(discovery.confirmed_rpi_ip)
        discovery.save_config(discovery.confirmed_rpi_ip)
        
        print(f"\n✅ CONFIGURATION COMPLETE!")
        print(f"🌐 Backend URL: http://{discovery.confirmed_rpi_ip}:5000")
        print(f"📹 Stream URL: http://{discovery.confirmed_rpi_ip}:5000/video_feed")
        print(f"\n🚀 Ready to build and deploy!")
        
        return discovery.confirmed_rpi_ip
    else:
        print("\n❌ DISCOVERY FAILED!")
        print("💡 Make sure:")
        print("   - Raspberry Pi is powered on")
        print("   - Connected to same network")
        print("   - Autonomy system API is running")
        print("   - Run: ssh srihari@RPI_IP 'cd ~/autonomy_system && source venv/bin/activate && python3 api.py'")
        return None

if __name__ == "__main__":
    main()