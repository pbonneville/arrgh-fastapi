# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a minimal FastAPI application designed for deployment on Google Cloud Run. The project serves as a foundation for building a larger application, potentially related to generative AI.

## Key Commands

### Local Development with Virtual Environment
```bash
# Create and activate virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run locally with hot reload
uvicorn src.main:app --reload --port 8000
```

### Local Development with Docker
```bash
# Quick development script that builds and runs Docker container
./scripts/dev-local.sh

# Or manually:
docker build -t genai .
docker run -p 8080:8080 genai
```

### Testing
```bash
# Run tests (no pytest configuration, use Python directly)
python -m pytest tests/
```

### Deployment
```bash
# Deploy to Google Cloud Run (automatic CI/CD is configured for main branch)
gcloud run deploy genai \
  --image gcr.io/paulbonneville-com/genai \
  --platform managed \
  --region us-central1 \
  --no-allow-unauthenticated
```

## Architecture

### Project Structure
- `src/main.py` - Core FastAPI application entry point
- `tests/` - Unit tests using FastAPI's TestClient
- `scripts/dev-local.sh` - Docker development automation
- Service runs on port 8080 (Google Cloud Run standard)

### Key Technical Details
- **Framework**: FastAPI with Uvicorn server
- **Python**: 3.11
- **Deployment**: Docker on Google Cloud Run
- **Authentication**: Service account required (no public access)
- **CI/CD**: Automatic deployment on push to main branch

### Testing Approach
Tests use manual path manipulation to import the app. When adding new tests, follow the pattern in `tests/test_main.py`:
```python
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
```

### Google Cloud Configuration
- **Project**: paulbonneville-com
- **Service**: genai
- **Region**: us-central1
- **Service Account**: genai-app@paulbonneville-com.iam.gserviceaccount.com
- **Service URL**: https://genai-860937201650.us-central1.run.app

## Important Notes

- The application requires authentication via service account for Cloud Run access
- No linting or type checking is currently configured
- Tests should be run before committing changes
- The Docker container exposes port 8080 as required by Google Cloud Run
- Continuous deployment is enabled - changes to main branch automatically deploy