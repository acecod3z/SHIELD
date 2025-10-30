# SHIELD Backend - Deployment Guide

## 🚀 Team Deployment & Python Compatibility

This guide helps ensure the SHIELD backend works across different Python environments and team setups.

## Quick Setup for Team Members

### Step 1: Install Python 3.8+
- Download from https://python.org
- Verify installation: `python --version` or `python3 --version`

### Step 2: Run the Startup Script

**Windows:**
```cmd
# Double-click or run in PowerShell/Command Prompt
start_backend.bat
```

**Linux/macOS:**
```bash
# Run in terminal
./start_backend.sh
```

### Step 3: Access the API
- API: http://127.0.0.1:8000
- Documentation: http://127.0.0.1:8000/docs

## Troubleshooting Common Issues

### ❌ "Python version conflict" or "dependency installation failed"

**Root Cause**: Different Python versions or package conflicts

**Solution**: The startup scripts now handle this automatically by:
- Detecting multiple Python installations
- Using flexible version ranges in requirements.txt
- Graceful fallback for optional dependencies

### ❌ "Virtual environment creation failed"

**Linux/macOS Solution:**
```bash
# Install python3-venv if missing
sudo apt-get install python3-venv  # Ubuntu/Debian
sudo yum install python3-venv      # CentOS/RHEL
```

**Windows Solution:**
```cmd
# Try different Python commands
py -m venv venv
# or
python3 -m venv venv
```

### ❌ "Command not found: python"

**Solution**: The startup script tries multiple Python commands:
- `python3` (Linux/macOS preferred)
- `python` (Windows common)
- `py` (Windows Python Launcher)
- `python3.11`, `python3.10`, etc.

### ❌ "Permission denied" on Linux/macOS

**Solution:**
```bash
# Make the script executable
chmod +x start_backend.sh
```

## Version Compatibility

### Supported Python Versions
- ✅ Python 3.8
- ✅ Python 3.9  
- ✅ Python 3.10
- ✅ Python 3.11
- ✅ Python 3.12+

### Dependency Strategy
The `requirements.txt` uses flexible versioning to avoid conflicts:

```txt
# Core dependencies with version ranges
fastapi>=0.95.0,<1.0.0
uvicorn[standard]>=0.20.0,<1.0.0
pydantic>=2.0.0,<3.0.0

# Optional dependencies with graceful degradation
structlog>=22.0.0; python_version>="3.8"
```

### What Changed to Fix Compatibility

1. **Flexible Requirements**: Changed from exact versions to ranges
2. **Python Detection**: Enhanced startup scripts to find any Python 3.8+
3. **Import Fallbacks**: Added graceful handling for missing optional packages
4. **Better Error Messages**: Clearer troubleshooting guidance

## Manual Setup (If Scripts Don't Work)

### Windows
```cmd
cd backend
python -m venv venv
venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
python main.py
```

### Linux/macOS
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
python main.py
```

## Testing the Installation

### 1. Check Server Status
```bash
curl http://127.0.0.1:8000/api/v1/health
```

**Expected Response:**
```json
{"status": "healthy", "version": "1.0.0"}
```

### 2. Test API Documentation
- Visit: http://127.0.0.1:8000/docs
- Should see interactive Swagger UI

### 3. Test Analysis Endpoint
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"data": "test input", "analysis_type": "text"}'
```

## Environment Configuration

### Default Settings (.env file)
```env
DEBUG=true
HOST=127.0.0.1
PORT=8000
LOG_LEVEL=INFO
```

### Production Settings
```env
DEBUG=false
HOST=0.0.0.0
PORT=8000
LOG_LEVEL=WARNING
SECRET_KEY=your-secure-secret-key
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/analyze` | POST | Submit data for analysis |
| `/api/v1/status` | GET | Get system status |
| `/api/v1/health` | GET | Health check |
| `/docs` | GET | API documentation |

## Architecture Overview

```
SHIELD/
├── start_backend.bat       # Windows startup script
├── start_backend.sh        # Linux/macOS startup script
└── backend/
    ├── main.py            # FastAPI application
    ├── requirements.txt   # Python dependencies
    ├── .env.example      # Configuration template
    └── app/
        ├── api/v1/routes.py    # API endpoints
        ├── models/schemas.py   # Data models
        ├── services/analysis.py # Business logic
        └── core/
            ├── config.py       # Settings
            └── logging_config.py # Logging
```

## Integration Points

### Phase 1: AI Models (Ready)
- Stubs in `services/analysis.py`
- Ready for model integration
- Async processing support

### Phase 2: Honeypot System (Ready)
- Stubs in `services/analysis.py`
- Ready for honeypot integration
- Session management prepared

## For Developers

### Adding New Features
1. **New API endpoints**: Edit `app/api/v1/routes.py`
2. **New data models**: Edit `app/models/schemas.py`
3. **New business logic**: Edit `app/services/analysis.py`

### Development Mode
```bash
# Run with auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Testing
```bash
# Interactive API testing
# Visit: http://127.0.0.1:8000/docs
```

## Support

If you encounter issues not covered here:

1. **Check Python version**: Must be 3.8+
2. **Try manual setup**: Follow manual installation steps
3. **Check internet connection**: Required for dependency installation
4. **Review error messages**: The startup scripts provide detailed feedback

## What's Next

Once the backend is running successfully:

1. ✅ **Backend is operational**
2. 🔄 **Ready for frontend integration**
3. 🔄 **Ready for AI model integration (Phase 1)**
4. 🔄 **Ready for honeypot integration (Phase 2)**

---

**Status**: ✅ Cross-platform compatibility resolved  
**Last Updated**: December 2024  
**Version**: 1.0.0-compatible