# SHIELD Backend

## 🛡️ FastAPI Backend for Security Analysis

This is the production-ready backend API for the SHIELD Web Interface, built with FastAPI and designed for future integration of AI security models and honeypot systems.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone and navigate to backend directory:**
```bash
cd backend
```

2. **Create virtual environment:**
```bash
python -m venv venv
```

3. **Activate virtual environment:**
```bash
# Windows
venv\Scripts\activate

# Linux/macOS  
source venv/bin/activate
```

4. **Install dependencies:**
```bash
pip install -r requirements.txt
```

5. **Configure environment (optional):**
```bash
cp .env.example .env
# Edit .env file with your settings
```

### Running the Server

**Development Mode:**
```bash
python main.py
```

**Production Mode:**
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://127.0.0.1:8000
- **Documentation**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 📋 API Endpoints

### Core Analysis
- `POST /api/v1/analyze` - Analyze input for security threats
- `GET /api/v1/status/{job_id}` - Check analysis job status
- `GET /api/v1/health` - API health check

### Testing (Development)
- `POST /api/v1/test/benign` - Test benign result
- `POST /api/v1/test/malicious` - Test malicious result

## 🏗️ Architecture

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment configuration template
├── app/
│   ├── __init__.py
│   ├── api/              # API routes and endpoints
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes.py  # Main API endpoints
│   ├── core/             # Core configuration and utilities
│   │   ├── __init__.py
│   │   ├── config.py     # Application settings
│   │   └── logging_config.py  # Logging setup
│   ├── models/           # Pydantic data models
│   │   ├── __init__.py
│   │   └── schemas.py    # Request/response schemas
│   └── services/         # Business logic and services
│       ├── __init__.py
│       └── analysis.py   # Analysis workflow and stubs
└── logs/                 # Log files (auto-created)
```

## 🔧 Features

### Current Implementation
- ✅ **FastAPI Framework** - Modern, async Python web framework
- ✅ **Pydantic Validation** - Automatic request/response validation
- ✅ **CORS Support** - Frontend integration ready
- ✅ **Structured Logging** - Security and application logging
- ✅ **Async Processing** - Non-blocking request handling
- ✅ **Job Status Tracking** - Monitor long-running analysis jobs
- ✅ **Modular Architecture** - Easy to extend and maintain

### Input Type Support
- **Text Analysis** - SQL injection, XSS, command injection detection
- **URL Analysis** - Phishing, malicious links, SSRF detection
- **Image Analysis** - Steganography, payload detection (Base64)

### Security Features
- Input validation and sanitization
- Request/response logging
- Error handling and monitoring
- Security-focused logging

## 🤖 Integration Points

### Phase 1: AI Model Integration (Planned)
**Current Status**: Stub implementation in `services/analysis.py`

The `ai_analysis_stub()` function in `analysis.py` will be replaced with:
- Real AI model loading and inference
- Specialized models for each input type
- Confidence scoring and threat classification
- Model versioning and updates

**Integration Steps:**
1. Replace stub functions with actual AI model calls
2. Add model loading and caching
3. Implement model-specific preprocessing
4. Add model performance monitoring

### Phase 2: Honeypot System (Planned)
**Current Status**: Stub implementation in `services/analysis.py`

The `honeypot_engagement_stub()` function will be replaced with:
- Real honeypot session management
- GPT-powered fake terminal responses
- Attacker behavior logging
- Session state management

**Integration Steps:**
1. Implement honeypot session storage (Redis)
2. Add GPT API integration for responses
3. Create fake terminal interface
4. Add comprehensive attack logging

## 🛠️ Development

### Testing the API

**Using curl:**
```bash
# Analyze text input
curl -X POST "http://127.0.0.1:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "input_type": "text",
    "content": "SELECT * FROM users WHERE id = 1 OR 1=1",
    "ip_address": "192.168.1.100"
  }'

# Check job status
curl "http://127.0.0.1:8000/api/v1/status/analysis_1698765432_abc123"
```

**Using the documentation:**
Visit http://127.0.0.1:8000/docs for interactive API testing.

### Adding New Features

1. **New input types**: Add to `InputType` enum in `models/schemas.py`
2. **New attack types**: Add to `AttackType` enum in `models/schemas.py`
3. **New endpoints**: Add to `api/v1/routes.py`
4. **New services**: Create new files in `services/`

## 📊 Monitoring & Logging

### Log Files
- `logs/shield.log` - General application logs
- `logs/security.log` - Security-specific events
- `logs/honeypot/` - Honeypot interaction logs (Phase 2)

### Health Monitoring
- GET `/health` - Basic health check
- GET `/api/v1/health` - Detailed health status

## 🔒 Security Considerations

### Current Security Measures
- Input validation with Pydantic
- Request size limits
- CORS configuration
- Security logging
- Error message sanitization

### Production Deployment
- Change `SECRET_KEY` in production
- Enable HTTPS/TLS
- Configure proper CORS origins
- Set up log rotation
- Implement rate limiting
- Add authentication/authorization

## 🚀 Production Deployment

### Docker (Recommended)
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables
Set these in production:
- `DEBUG=false`
- `SECRET_KEY=<secure-random-key>`
- `ALLOWED_ORIGINS=<your-frontend-domains>`
- `LOG_LEVEL=WARNING`

---

**Last Updated**: October 30, 2025  
**Version**: 1.0.0  
**Status**: Ready for Phase 1 & 2 Integration