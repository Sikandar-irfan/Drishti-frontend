# Complete VS Code Setup Prompt for Sentinel View System

## Overview
This is a complete React TypeScript frontend for a Raspberry Pi autonomous navigation system. It includes dynamic backend discovery, GitHub Pages deployment, and direct RPi deployment capabilities.

## Prerequisites Setup Instructions

### 1. Initial Repository Setup
```bash
# Clone your repository
git clone https://github.com/Sikandar-irfan/Drishti-frontend.git
cd Drishti-frontend

# Install all dependencies
npm install

# Make sure Python is available for the dynamic discovery scripts
python --version
```

### 2. GitHub Repository Configuration
Go to your GitHub repository settings and:
1. Navigate to `Settings` → `Pages`
2. Set source to `GitHub Actions`
3. Save the settings

### 3. Environment Variables Setup
The system will auto-configure these, but you can manually create:

Create `.env` file:
```env
VITE_API_BASE_URL=http://YOUR_RPI_IP:5000
VITE_APP_TITLE=Sentinel View System
VITE_APP_VERSION=1.0.0
```

Create `.env.production` file:
```env
VITE_API_BASE_URL=http://YOUR_RPI_IP:5000
VITE_APP_TITLE=Sentinel View System
VITE_APP_VERSION=1.0.0
```

## Quick Start Commands

### Option 1: Automatic Discovery and Deployment
```bash
# This will automatically discover your RPi and configure everything
npm run setup

# Deploy to GitHub Pages
npm run deploy

# Or deploy to both GitHub Pages and RPi
npm run auto-deploy
```

### Option 2: Manual Step-by-Step Process

#### Step 1: Discover Raspberry Pi
```bash
# Run the discovery script to find your RPi automatically
npm run discover
# This will:
# - Scan your network for Raspberry Pi devices
# - Test API connectivity
# - Update .env files automatically
# - Update GitHub Actions workflow
```

#### Step 2: Build and Test Locally
```bash
# Development build and serve
npm run dev

# Or production build and preview
npm run build:prod
npm run preview
```

#### Step 3: Deploy to GitHub Pages
```bash
npm run deploy
```

#### Step 4: Deploy to Raspberry Pi (Optional)
```bash
npm run auto-deploy
```

## What These Scripts Do

### `npm run setup`
- Installs all dependencies
- Runs automatic RPi discovery
- Configures environment variables
- Updates GitHub Actions workflow

### `npm run discover`
- Scans network range (192.168.x.x, 10.0.x.x, 172.16-31.x.x)
- Tests connectivity to potential RPi devices
- Verifies API endpoints (/api/status, /api/location)
- Updates .env and .env.production files
- Updates GitHub Actions workflow with correct IP
- Saves configuration to rpi_config.json

### `npm run deploy`
- Builds production version
- Deploys to GitHub Pages using gh-pages
- Site will be available at: 
  - **Custom Domain**: https://drishti-asb.duckdns.org/ ✨
  - **GitHub Pages**: https://sikandar-irfan.github.io/Drishti-frontend/

### `npm run auto-deploy`
- Discovers RPi automatically
- Builds frontend for production
- Deploys to GitHub Pages
- Transfers built files to RPi
- Sets up web server on RPi
- Provides multiple access methods

## Manual Configuration (If Auto-Discovery Fails)

If automatic discovery doesn't work, manually update these files:

### Update .env files
Replace `YOUR_RPI_IP` with your actual Raspberry Pi IP address in:
- `.env`
- `.env.production`

### Update GitHub Actions Workflow
In `.github/workflows/deploy.yml`, update the RPi IP address in the environment variables section.

## Raspberry Pi Backend Requirements

Your Raspberry Pi should have:
1. Flask API running on port 5000
2. CORS enabled for cross-origin requests
3. These endpoints available:
   - `GET /api/status` - System status
   - `GET /api/location` - Current location
   - `GET /api/telemetry` - Real-time telemetry
   - `POST /api/navigate` - Navigation commands

## Project Structure
```
sentinel-view-system/
├── src/
│   ├── components/       # Reusable UI components
│   ├── pages/           # Main page components
│   ├── services/        # API service layer
│   ├── store/           # Zustand state management
│   └── lib/             # Utilities and configurations
├── public/              # Static assets
├── .github/workflows/   # GitHub Actions for deployment
├── discover_rpi.py      # Automatic RPi discovery script
├── auto_deploy.py       # Complete deployment automation
└── package.json         # Dependencies and scripts
```

## Troubleshooting

### RPi Discovery Issues
```bash
# Check if Python is available
python --version

# Manually run discovery with verbose output
python discover_rpi.py

# Check network connectivity
ping YOUR_RPI_IP
```

### Build Issues
```bash
# Clear node modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Check TypeScript issues
npx tsc --noEmit
```

### Deployment Issues
```bash
# Check GitHub Pages settings
# Ensure source is set to "GitHub Actions"

# Manually trigger GitHub Actions
git add .
git commit -m "Trigger deployment"
git push origin main
```

### Backend Connectivity Issues
- Ensure RPi is on the same network
- Check if Flask API is running: `curl http://YOUR_RPI_IP:5000/api/status`
- Verify CORS is enabled in Flask app
- Check firewall settings on RPi

## Features

### Frontend Features
- Real-time telemetry dashboard
- Interactive navigation controls
- Live video streaming
- System status monitoring
- Responsive design with dark/light themes
- Real-time backend synchronization

### Deployment Features
- Automatic Raspberry Pi discovery
- Dynamic IP configuration
- GitHub Pages deployment
- Direct RPi deployment
- Automated build processes
- Environment-based configuration

### Development Features
- TypeScript for type safety
- ESLint for code quality
- Hot module replacement in development
- Component-based architecture
- State management with Zustand
- API service layer abstraction

## Advanced Usage

### Custom Network Ranges
Edit `discover_rpi.py` to add custom IP ranges if your network uses non-standard ranges.

### SSH Configuration for RPi Deployment
For automatic RPi deployment, ensure SSH access:
```bash
# Add your SSH key to RPi (run on your machine)
ssh-copy-id pi@YOUR_RPI_IP
```

### Environment Customization
You can customize the following environment variables:
- `VITE_API_BASE_URL` - Backend API URL
- `VITE_APP_TITLE` - Application title
- `VITE_APP_VERSION` - Version number
- `VITE_REFRESH_INTERVAL` - Data refresh interval (ms)

## Support

If you encounter issues:
1. Check the console for error messages
2. Verify network connectivity to RPi
3. Ensure all dependencies are installed
4. Check GitHub Actions logs for deployment issues
5. Verify RPi backend is running and accessible

## One-Line Setup (For Experienced Users)
```bash
git clone YOUR_REPO_URL && cd sentinel-view-system && npm install && npm run setup && npm run auto-deploy
```

This will clone, install, configure, and deploy everything automatically!