# Quick Setup Guide

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set API Key
```bash
# IMPORTANT: Set your Gemini API key (shared separately for security)
export GEMINI_API_KEY="your-gemini-api-key-here"
```

### 3. Run the Application
```bash
# Option A: Local development
uvicorn app.main:app --reload

# Option B: Docker (recommended)
docker compose up -d
```

## 🔧 Configuration Options

### Switch AI Methods (Optional)
```bash
# Default: Gemini (requires API key)
export SUMMARIZER="gemini"

# Local alternatives (no API key needed):
export SUMMARIZER="bart"        # BART model
export SUMMARIZER="extractive"  # Simple extractive
```

## 📡 API Endpoints

Once running, access:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Docs**: http://localhost:8000/docs

## 🆘 Troubleshooting

**Missing API Key Error?**
```bash
# Make sure to set the Gemini API key
export GEMINI_API_KEY="your-key-here"
```

**Docker Issues?**
```bash
# Restart containers
docker compose down && docker compose up -d
```
