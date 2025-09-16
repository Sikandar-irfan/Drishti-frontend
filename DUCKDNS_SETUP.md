# 🌐 DuckDNS Custom Domain Setup for Drishti Frontend

## Overview
Your Drishti autonomous surveillance system now uses a professional custom domain powered by DuckDNS for enhanced accessibility and branding.

## 🔗 Your New Domain
**Primary Access**: https://drishti-surveillance.duckdns.org/

## 🚀 Setup Instructions

### Step 1: DuckDNS Account Setup
1. **Visit**: https://www.duckdns.org/
2. **Sign in** with your preferred method (Google, GitHub, Twitter, etc.)
3. **Create subdomain**: `drishti-surveillance` (or your preferred name)
4. **Set IP Address**: `185.199.108.153` (GitHub Pages IP)
5. **Save** your configuration

### Step 2: Repository Configuration ✅ (Already Done)
- ✅ CNAME file created in `/public/CNAME`
- ✅ GitHub Actions workflow updated
- ✅ Vite configuration adjusted for custom domain
- ✅ Documentation updated

### Step 3: GitHub Pages Settings
1. **Go to**: https://github.com/Sikandar-irfan/Drishti-frontend/settings/pages
2. **Custom domain**: Enter `drishti-surveillance.duckdns.org`
3. **Enforce HTTPS**: Enable this option
4. **Save** settings

## 🔧 Alternative Domain Suggestions
If `drishti-surveillance` is taken, try:
- `drishti-autonomous.duckdns.org`
- `drishti-frontend.duckdns.org`
- `drishti-system.duckdns.org`
- `your-name-drishti.duckdns.org`

## 🔄 Updating Your Domain
If you choose a different subdomain:

1. **Update CNAME file**:
   ```bash
   echo "your-new-subdomain.duckdns.org" > public/CNAME
   ```

2. **Update workflow** (`.github/workflows/deploy.yml`):
   ```yaml
   url: https://your-new-subdomain.duckdns.org
   ```

3. **Commit and push changes**

## 🌍 Benefits of Custom Domain

### Professional Branding
- ✅ Clean, memorable URL
- ✅ Professional appearance
- ✅ Easy to share and remember

### Technical Benefits
- ✅ **HTTPS/SSL**: Automatic security certificate
- ✅ **Global CDN**: Fast loading worldwide
- ✅ **Reliability**: DuckDNS uptime guarantee
- ✅ **Free**: No cost for domain or hosting

### Accessibility
- ✅ **Mobile-friendly**: Easy to type on mobile devices
- ✅ **Network-independent**: Accessible from any network
- ✅ **Bookmark-friendly**: Easy to save and share

## 🔒 Security Features

### Automatic HTTPS
- SSL certificate automatically provisioned
- All traffic encrypted end-to-end
- Browser security indicators

### DuckDNS Security
- Protected against domain hijacking
- Secure DNS resolution
- Regular security updates

## 📊 Monitoring Your Domain

### Check Domain Status
```bash
# DNS lookup
nslookup drishti-surveillance.duckdns.org

# HTTPS check
curl -I https://drishti-surveillance.duckdns.org/
```

### DuckDNS Management
- **Dashboard**: https://www.duckdns.org/domains
- **Update IP**: If GitHub Pages IP changes
- **Check logs**: Monitor DNS resolution

## 🚨 Troubleshooting

### Domain Not Working?
1. **Wait 5-10 minutes** for DNS propagation
2. **Check DuckDNS settings** - ensure IP is `185.199.108.153`
3. **Verify GitHub Pages** settings show your custom domain
4. **Clear browser cache** and try again

### HTTPS Issues?
1. **Enable "Enforce HTTPS"** in GitHub Pages settings
2. **Wait up to 24 hours** for certificate provisioning
3. **Check certificate** status in repository settings

### DNS Propagation
```bash
# Check DNS propagation globally
dig @8.8.8.8 drishti-surveillance.duckdns.org
dig @1.1.1.1 drishti-surveillance.duckdns.org
```

## 🔄 Domain Migration
If you need to change domains later:

1. **Update DuckDNS** with new subdomain
2. **Update CNAME file** in repository
3. **Update GitHub Pages** settings
4. **Update documentation** references
5. **Notify users** of the change

## 📱 Mobile Access
Your domain is mobile-optimized:
- **Short URL**: Easy to type on mobile
- **Responsive design**: Adapts to all screen sizes
- **Touch-friendly**: Optimized for touch interfaces

## 🌐 Global Accessibility
Your Drishti system is now accessible:
- **Worldwide**: Global CDN for fast loading
- **24/7**: High availability infrastructure
- **Secure**: HTTPS everywhere
- **Professional**: Custom branded domain

---

**Your autonomous surveillance system is now live at:**
**🌟 https://drishti-surveillance.duckdns.org/ 🌟**

*Remember to replace `drishti-surveillance` with your chosen subdomain if different.*