# genai

# FastAPI on Google Cloud Run

This project is a minimal FastAPI application ready to be deployed on Google Cloud Run using Docker.

## Prerequisites
- Python 3.11+
- Docker
- Google Cloud SDK (`gcloud`)
- A Google Cloud project with billing enabled

## Setting Up a Local Python Virtual Environment

It is recommended to use a Python virtual environment for local development to keep dependencies isolated.

1. Create a virtual environment:
   ```sh
   python3.11 -m venv .venv
   ```
2. Activate the virtual environment:
   - On macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

## Running Locally

1. Install dependencies (if not already done):
   ```sh
   pip install -r requirements.txt
   ```
2. Start the app:
   ```sh
   uvicorn main:app --reload
   ```
3. Visit [http://localhost:8000](http://localhost:8000)

## Building and Running with Docker

1. Build the Docker image:
   ```sh
   docker build -t nexus-app .
   ```
2. Run the Docker container:
   ```sh
   docker run -p 8080:8080 nexus-app
   ```
3. Visit [http://localhost:8080](http://localhost:8080)

## Deploying to Google Cloud Run

1. Set your Google Cloud project:
   ```sh
   gcloud config set project [PROJECT-ID]
   ```
2. Build the container and push to Google Container Registry:
   ```sh
   docker build -t gcr.io/[PROJECT-ID]/nexus-app .
   docker push gcr.io/[PROJECT-ID]/nexus-app
   ```
3. Deploy to Cloud Run:
   ```sh
   gcloud run deploy nexus-app \
     --image gcr.io/[PROJECT-ID]/nexus-app \
     --platform managed \
     --region [REGION] \
     --allow-unauthenticated
   ```
4. After deployment, Cloud Run will provide a service URL. Visit it in your browser.

---

Replace `[PROJECT-ID]` and `[REGION]` with your actual Google Cloud project ID and desired region (e.g., `us-central1`). 

