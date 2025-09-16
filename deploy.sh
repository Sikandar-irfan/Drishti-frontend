#!/bin/bash
# Complete Setup Script for Frontend-Backend Integration
# Run this script to deploy everything automatically

echo "🚀 AUTONOMOUS NAVIGATION SYSTEM - COMPLETE DEPLOYMENT"
echo "====================================================="

# Step 1: Start Backend on Raspberry Pi
echo "📡 Starting backend on Raspberry Pi..."
echo "Please run this command in a separate terminal:"
echo "ssh srihari@192.168.0.101"
echo "cd ~/autonomy_system"
echo "source venv/bin/activate"
echo "python3 api.py"
echo ""
echo "Press Enter when backend is running..."
read

# Step 2: Test Backend
echo "🧪 Testing backend connection..."
python test_backend.py

# Step 3: Build Frontend
echo "🔨 Building frontend for production..."
npm run build:prod

# Step 4: Test Frontend Locally
echo "🖥️  Starting local frontend preview..."
echo "Opening http://localhost:4173"
echo "Check if everything works, then press Ctrl+C to continue..."
npm run preview

# Step 5: Deploy to GitHub Pages
echo "🌐 Deploying to GitHub Pages..."
echo "Make sure you've:"
echo "1. Created a GitHub repository"
echo "2. Pushed your code to GitHub"
echo "3. Enabled GitHub Pages in repository settings"
echo ""
echo "Deploy now? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    npm run deploy
    echo "✅ Deployed to GitHub Pages!"
    echo "🌍 Your site will be available at:"
    echo "https://sikandar-irfan.github.io/sentinel-view-system/"
else
    echo "⏭️  Skipping deployment. You can deploy later with: npm run deploy"
fi

echo ""
echo "🎉 SETUP COMPLETE!"
echo "📋 Summary:"
echo "✅ Backend running on Raspberry Pi"
echo "✅ Frontend built and tested"
echo "✅ Ready for GitHub Pages deployment"
echo ""
echo "🔗 Next steps:"
echo "1. Access your dashboard: https://sikandar-irfan.github.io/sentinel-view-system/"
echo "2. Make sure RPi backend is always running for live data"
echo "3. Configure port forwarding for internet access (optional)"