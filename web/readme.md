# 🌐 SHIELD Web Interface

This folder contains the frontend web interface for the SHIELD Advanced Threat Detection System.

## 📄 Files

### Main Pages
- **`index.html`** - Threat Scanner input interface with real-time analysis
- **`dashboard.html`** - Threat Analysis Dashboard with system diagnostics and activity logs
- **`honeypot.html`** - Honeypot Console for attacker deception and engagement

### Documentation
- `readme.md` - This file

> **Note**: Graphics and assets have been moved to `/assets/images/` for better organization.

## ✨ Features

### 🎨 Visual Design
- **Color Scheme**: Dark navy blue (#0d1b2a) with cyan (#00d4ff) and green (#00ff88) accents
- **Typography**: Orbitron (headings) and Rajdhani (body) fonts for a futuristic look
- **Effects**: 
  - Glassmorphism UI elements
  - DarkVeil WebGL animated background
  - Decrypted text scramble animations
  - Gooey navigation with particle effects
  - Floating particles and glowing elements
- **Layout**: Modern defense company aesthetic with high-tech military-grade theme

### ⚡ Interactive Elements
- **Gooey Navigation**: Liquid morphing navigation with particle explosions
- **Decrypted Text**: Character scrambling reveal animations on headings
- **Animated Backgrounds**: WebGL shader effects and floating particles
- **Status Indicators**: Glowing, pulsing system status displays
- **Smooth Transitions**: Cubic-bezier animations throughout
- **Responsive Design**: Mobile-first approach for all devices

### 🚀 Page-Specific Features

#### index.html - Threat Scanner
- Real-time threat analysis input
- Visual feedback on submission
- Automatic redirect to dashboard for results
- Honeypot redirect for malicious inputs (opens in new tab)

#### dashboard.html - Analysis Dashboard
- Comprehensive threat report display
- System diagnostics (processing time, timestamp)
- Detected threats details with severity levels
- Activity log with recent scans
- Decrypted text animations on load

#### honeypot.html - Honeypot Console
- Terminal-style interface for attacker engagement
- Command execution simulation
- Realistic fake server responses
- Session-based interaction tracking

## 🔧 Usage

### Prerequisites
- SHIELD backend running on `http://127.0.0.1:8000`
- Modern web browser (Chrome, Firefox, Edge, Safari)

### Running the Frontend

1. **Start Backend First**
   ```bash
   # See /backend/README.md for backend setup
   cd backend
   uvicorn main:app --reload
   ```

2. **Open Web Interface**
   - Option 1: Open `index.html` directly in browser
   - Option 2: Use a local server (recommended):
     ```bash
     # Python
     python -m http.server 8080
     
     # Node.js
     npx http-server -p 8080
     ```
   - Navigate to `http://localhost:8080`

3. **Test Threat Analysis**
   - Enter text in the scanner (e.g., SQL injection: `' OR 1=1--`)
   - View results in dashboard
   - Malicious inputs trigger honeypot

## 🎯 API Integration

The frontend communicates with the backend via:

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000/api/v1';

// Main analysis endpoint
POST /api/v1/analyze

// Honeypot interaction
POST /api/v1/honeypot/interact
```

## 🎨 Design Philosophy

The interface provides a professional, high-tech experience suitable for:
- Military-grade security applications
- Defense contractor cybersecurity platforms  
- Enterprise-level threat intelligence systems
- Advanced AI/ML security positioning

## 📱 Browser Compatibility

- ✅ Chrome/Edge (Chromium) 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ⚠️ IE 11 not supported (uses modern ES6+ features)

## 🔐 Security Notes

- All sensitive configuration in backend `.env`
- No API keys or secrets in frontend code
- CORS configured for localhost development
- Production deployment requires proper HTTPS and CSP headers

---

For more information, see:
- [Main README](../README.md)
- [Backend Documentation](../backend/README.md)
- [Dashboard Guide](../docs/DASHBOARD_README.md)


