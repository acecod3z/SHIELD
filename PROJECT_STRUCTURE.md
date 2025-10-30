# 📁 SHIELD Project Structure

This document outlines the organization of the SHIELD repository.

## 🗂️ Directory Structure

```
SHIELD/
├── 📄 README.md                    # Main project documentation
├── 📄 .gitignore                   # Git ignore rules
├── 📄 docker-compose.yml           # Docker orchestration
├── 📄 Dockerfile                   # Docker container configuration
├── 🔧 start_backend.bat            # Windows backend startup script
├── 🔧 start_backend.sh             # Linux/macOS backend startup script
│
├── 📂 backend/                     # FastAPI Backend Server
│   ├── 📄 main.py                  # Application entry point
│   ├── 📄 requirements.txt         # Python dependencies
│   ├── 📄 .env.example             # Environment variables template
│   ├── 📄 README.md                # Backend documentation
│   ├── 📄 README_DEPLOYMENT.md     # Deployment guide
│   ├── 🧪 test_integration.py      # Integration tests
│   ├── 🧪 test_end_to_end.py       # End-to-end tests
│   │
│   ├── 📂 app/                     # Application code
│   │   ├── 📂 api/                 # API routes
│   │   │   └── 📂 v1/              # API version 1
│   │   │       ├── routes.py       # Main route definitions
│   │   │       └── honeypot.py     # Honeypot endpoints
│   │   ├── 📂 core/                # Core configurations
│   │   │   ├── config.py           # App configuration
│   │   │   └── logging_config.py   # Logging setup
│   │   ├── 📂 models/              # Data models
│   │   │   └── schemas.py          # Pydantic schemas
│   │   └── 📂 services/            # Business logic
│   │       ├── analysis.py         # Analysis service
│   │       └── sql_injection_detector.py  # SQL injection detection
│   │
│   └── 📂 logs/                    # Application logs (generated)
│
├── 📂 web/                         # Frontend Web Interface
│   ├── 🌐 index.html               # Main threat scanner page
│   ├── 🌐 dashboard.html           # Analysis dashboard
│   ├── 🌐 honeypot.html            # Honeypot console interface
│   └── 📄 readme.md                # Frontend documentation
│
├── 📂 model/                       # ML Models & Training
│   ├── 🧠 hackathon_sql_detector.pkl  # Trained model file
│   ├── 📄 hackathon_sql_detector.py   # Model training script
│   ├── 📄 readme.py                   # Model documentation
│   └── 📂 final/                      # Training datasets
│       ├── Modified_SQL_Dataset_train.csv
│       ├── Modified_SQL_Dataset_test.csv
│       └── Modified_SQL_Dataset_validation.csv
│
├── 📂 dataset/                     # Training Datasets
│   ├── 📄 Attack_Dataset.csv       # Attack patterns dataset
│   ├── 📄 Modified_SQL_Dataset.csv # SQL injection dataset
│   ├── 📄 url_xss_dataset_25000.csv # XSS dataset
│   └── 📄 readme.md                # Dataset documentation
│
├── 📂 docs/                        # Documentation
│   ├── 📄 DASHBOARD_README.md      # Dashboard documentation
│   └── 📂 guides/                  # Setup & integration guides
│       ├── 📄 AI_HONEYPOT_SETUP.md
│       ├── 📄 HONEYPOT_GUIDE.md
│       ├── 📄 INTEGRATION_GUIDE.md
│       └── 📄 OPENAI_SETUP.md
│
├── 📂 assets/                      # Static Assets
│   └── 📂 images/                  # Images & graphics
│       ├── confusion_matrix.png
│       ├── secure-icon.svg
│       ├── shield-logo.svg
│       ├── tech-background.svg
│       ├── threat-icon.svg
│       └── *.jpg (design references)
│
├── 📂 misc/                        # Miscellaneous files
│   └── 📄 readme.md
│
└── 📂 logs/                        # Application logs (root level)
```

## 🎯 Key Components

### Backend (`/backend`)
- **FastAPI** application with async support
- RESTful API with versioning (v1)
- Modular service architecture
- Comprehensive logging and error handling
- Honeypot interaction system

### Frontend (`/web`)
- Pure HTML/CSS/JavaScript (no framework dependencies)
- Three main interfaces:
  - **index.html**: Threat scanner input interface
  - **dashboard.html**: Real-time threat analysis dashboard
  - **honeypot.html**: Attacker deception terminal

### Models (`/model`)
- SQL injection detection model
- Training scripts and datasets
- Model evaluation metrics

### Documentation (`/docs`)
- Setup guides
- Integration documentation
- API references
- Deployment instructions

## 🔧 Configuration Files

| File | Purpose |
|------|---------|
| `.env` | Environment variables (not committed) |
| `.env.example` | Template for environment configuration |
| `requirements.txt` | Python package dependencies |
| `docker-compose.yml` | Container orchestration |
| `Dockerfile` | Container build instructions |

## 🚫 Ignored Files (.gitignore)

- Virtual environments (`.venv/`, `venv/`)
- Python cache (`__pycache__/`, `*.pyc`)
- Environment files (`.env`)
- Log files (`logs/`, `*.log`)
- IDE settings (`.vscode/`, `.idea/`)
- Temporary files

## 📝 Notes

- **Logs**: Generated at runtime in `backend/logs/` and root `logs/`
- **Virtual Environment**: `.venv/` in project root (ignored by git)
- **Model Files**: Large `.pkl` files may be ignored in production
- **Assets**: Images and graphics centralized in `/assets`
- **Documentation**: Guides and docs organized in `/docs`

## 🔄 Recent Reorganization

The project was recently reorganized to improve structure:
- Documentation moved to `/docs/guides/`
- Images consolidated in `/assets/images/`
- Removed duplicate virtual environments
- Cleaned up temporary files
- Improved `.gitignore` coverage
