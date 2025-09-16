# Sentinel View System 🤖

A modern React TypeScript frontend for Raspberry Pi autonomous navigation systems with automatic discovery and deployment capabilities.

## 🚀 Quick Start (One Command)

```bash
npm run quick-setup
```

This will automatically:
- Install all dependencies
- Discover your Raspberry Pi
- Configure environment variables
- Build the frontend
- Deploy to GitHub Pages
- Deploy to Raspberry Pi (optional)

## 📋 Manual Setup

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Discover Raspberry Pi:**
   ```bash
   npm run discover
   ```

3. **Deploy:**
   ```bash
   npm run deploy          # GitHub Pages only
   npm run auto-deploy     # Both GitHub Pages and RPi
   ```

## 🎯 Available Commands

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server |
| `npm run build:prod` | Build for production |
| `npm run deploy` | Deploy to GitHub Pages |
| `npm run discover` | Find and configure Raspberry Pi |
| `npm run auto-deploy` | Deploy to both GitHub and RPi |
| `npm run quick-setup` | Complete automated setup |

## 🔧 Features

- **Automatic RPi Discovery** - Scans network and finds your Raspberry Pi
- **Dynamic Configuration** - No hardcoded IP addresses
- **Dual Deployment** - GitHub Pages and direct RPi hosting
- **Real-time Dashboard** - Live telemetry and navigation controls
- **Type Safety** - Full TypeScript implementation
- **Responsive Design** - Works on desktop and mobile

## 📱 Access Points

After deployment, access your system via:
- **GitHub Pages**: `https://sikandar-irfan.github.io/Drishti-frontend/`
- **Raspberry Pi**: `http://your-rpi-ip:8080`
- **Development**: `http://localhost:5173`

## 🛠️ Tech Stack

- **Frontend**: React 18 + TypeScript + Vite
- **UI**: ShadCN UI Components + Tailwind CSS
- **State**: Zustand
- **Backend**: Flask API on Raspberry Pi
- **Deployment**: GitHub Actions + Pages

## 📋 Prerequisites

- Node.js 18+
- Python 3.7+
- Git
- Raspberry Pi with Flask API running

## 🔍 Troubleshooting

**RPi not found?**
```bash
python discover_rpi.py  # Manual discovery
```

**Build issues?**
```bash
rm -rf node_modules && npm install
```

**Deployment failed?**
- Check GitHub repository settings
- Ensure RPi is accessible via SSH
- Verify API endpoints are working

For detailed setup instructions, see [VSCODE_SETUP_PROMPT.md](./VSCODE_SETUP_PROMPT.md)

---

Made with ❤️ for autonomous navigation systems
