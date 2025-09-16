# 🚀 **FRONTEND-BACKEND INTEGRATION & GITHUB PAGES DEPLOYMENT**
*Complete guide for connecting React frontend to Raspberry Pi backend and deploying to GitHub Pages*

---

## 📊 **INTEGRATION OVERVIEW**

### **Architecture:**
- **Frontend:** React + TypeScript + Vite (Modern UI)
- **Backend:** Flask API on Raspberry Pi 4 (192.168.0.101:5000)
- **Deployment:** GitHub Pages (Public Access)
- **Real-time Data:** Live telemetry, video stream, SLAM data

### **Connection Flow:**
```
GitHub Pages Frontend ↔ Internet ↔ Your Network ↔ Raspberry Pi Backend
```

---

## 🔧 **SETUP INSTRUCTIONS**

### **Step 1: Install Frontend Dependencies**

```bash
cd "C:\Users\Sikandar Irfan\OneDrive\Desktop\CodeBox\sentinel-view-system-main"
npm install
npm install gh-pages --save-dev
```

### **Step 2: Start Backend on Raspberry Pi**

SSH to your Raspberry Pi:
```bash
ssh srihari@192.168.0.101
cd ~/autonomy_system
source venv/bin/activate
python3 api.py
```

The backend will start on: `http://192.168.0.101:5000`

### **Step 3: Test Local Frontend**

```bash
cd "C:\Users\Sikandar Irfan\OneDrive\Desktop\CodeBox\sentinel-view-system-main"
npm run dev
```

This will start the frontend on: `http://localhost:8080`

---

## 🌐 **GITHUB PAGES DEPLOYMENT**

### **Step 1: Push to GitHub**

1. **Initialize Git repository:**
```bash
cd "C:\Users\Sikandar Irfan\OneDrive\Desktop\CodeBox\sentinel-view-system-main"
git init
git add .
git commit -m "Initial commit: Frontend-backend integration"
```

2. **Create GitHub repository:**
   - Go to https://github.com/new
   - Name: `sentinel-view-system` (or any name you prefer)
   - Make it **Public** for GitHub Pages
   - Don't initialize with README (we have files already)

3. **Link and push to GitHub:**
```bash
git remote add origin https://github.com/Sikandar-irfan/sentinel-view-system.git
git branch -M main
git push -u origin main
```

### **Step 2: Enable GitHub Pages**

1. **Go to your repository on GitHub**
2. **Click "Settings" tab**
3. **Scroll to "Pages" in left sidebar**
4. **Source:** Deploy from a branch
5. **Branch:** Select `gh-pages` (will be created automatically)
6. **Folder:** `/ (root)`
7. **Click "Save"**

### **Step 3: Deploy**

```bash
npm run deploy
```

This will:
- Build the production version
- Create a `gh-pages` branch
- Deploy to GitHub Pages

**Your site will be available at:**
`https://sikandar-irfan.github.io/sentinel-view-system/`

---

## 🔌 **BACKEND API INTEGRATION**

### **API Endpoints Used:**
```
GET  /api/system_status     # System telemetry and health
GET  /api/slam_map          # Robot location and SLAM data  
GET  /api/voice_status      # Voice control status
GET  /video_feed            # Live camera stream
POST /api/navigation        # Send navigation commands
POST /api/emergency_stop    # Emergency stop command
```

### **Real-time Data Flow:**
1. **Frontend polls backend every 2 seconds**
2. **Updates telemetry (battery, CPU, temperature)**
3. **Updates robot location on map**
4. **Streams live video feed**
5. **Shows connection status**

---

## 🎯 **CONFIGURATION FILES CREATED**

### **1. Environment Configuration**
- `.env` - Development environment
- `.env.production` - Production environment  

### **2. API Service**
- `src/services/apiService.ts` - Backend communication

### **3. Updated Store**
- `src/store/botStore.ts` - Real backend integration

### **4. Deployment**
- `.github/workflows/deploy.yml` - Auto-deployment
- `vite.config.ts` - GitHub Pages configuration

---

## 🚨 **IMPORTANT NETWORK CONSIDERATIONS**

### **For Local Network Access:**
- Frontend on GitHub Pages can connect to RPi if on same network
- Works when accessing from devices on your home network

### **For Internet Access:**
You'll need one of these options:

#### **Option A: Port Forwarding (Recommended)**
1. **Router Settings:**
   - Forward port 5000 to 192.168.0.101:5000
   - Get your public IP: https://whatismyipaddress.com/

2. **Update Environment:**
```bash
# .env.production
VITE_API_BASE_URL=http://YOUR_PUBLIC_IP:5000
VITE_STREAM_URL=http://YOUR_PUBLIC_IP:5000/video_feed
```

#### **Option B: Cloudflare Tunnel (Advanced)**
```bash
# On Raspberry Pi
npm install -g cloudflared
cloudflared tunnel --url http://localhost:5000
```

#### **Option C: ngrok (Quick Setup)**
```bash
# On Raspberry Pi  
npm install -g ngrok
ngrok http 5000
# Use the ngrok URL in .env.production
```

---

## 🧪 **TESTING & VERIFICATION**

### **Test Backend Connection:**
```bash
# Test from Windows machine
curl http://192.168.0.101:5000/api/system_status
```

### **Test Frontend Locally:**
```bash
npm run dev
# Open http://localhost:8080
# Check browser console for connection status
```

### **Test Production Build:**
```bash
npm run build:prod
npm run preview
```

---

## 🎊 **FEATURES IMPLEMENTED**

### **✅ Real-time Dashboard:**
- Live telemetry data from Raspberry Pi
- Battery level, CPU usage, temperature
- Robot location tracking on map
- Live camera video stream

### **✅ Connection Management:**
- Auto-reconnection to backend
- Connection status indicators
- Offline mode handling
- Error recovery

### **✅ Production Ready:**
- Environment-based configuration
- GitHub Pages deployment
- CORS enabled backend
- Performance optimized

---

## 🔧 **TROUBLESHOOTING**

### **Backend Connection Issues:**
```bash
# Check if backend is running
ssh srihari@192.168.0.101 "ps aux | grep python"

# Check port accessibility  
telnet 192.168.0.101 5000
```

### **CORS Issues:**
- Backend already has CORS enabled
- Check browser console for errors
- Verify API URLs in environment files

### **GitHub Pages Issues:**
- Ensure repository is public
- Check GitHub Actions tab for build status
- Verify GitHub Pages settings

---

## 🚀 **DEPLOYMENT COMMANDS**

### **Quick Deployment:**
```bash
# 1. Start backend on RPi
ssh srihari@192.168.0.101 "cd ~/autonomy_system && source venv/bin/activate && python3 api.py"

# 2. Deploy frontend
cd "C:\Users\Sikandar Irfan\OneDrive\Desktop\CodeBox\sentinel-view-system-main"
npm run deploy

# 3. Access your site
# https://sikandar-irfan.github.io/sentinel-view-system/
```

### **Development Mode:**
```bash
# Terminal 1: Backend
ssh srihari@192.168.0.101 "cd ~/autonomy_system && source venv/bin/activate && python3 api.py"

# Terminal 2: Frontend  
cd "C:\Users\Sikandar Irfan\OneDrive\Desktop\CodeBox\sentinel-view-system-main"
npm run dev
```

---

## 🎯 **NEXT STEPS**

1. **Deploy to GitHub Pages** following the steps above
2. **Configure port forwarding** for internet access (optional)
3. **Test all features** with real hardware
4. **Customize the domain** if desired
5. **Add authentication** for security (future enhancement)

**Your autonomous robot surveillance system is now ready for global access via GitHub Pages!** 🤖🌐✨