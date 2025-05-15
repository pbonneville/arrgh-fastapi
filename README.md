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
   uvicorn src.main:app --reload
   ```
3. Visit [http://localhost:8000](http://localhost:8000)

## Building and Running with Docker

1. Build the Docker image:
   ```sh
   docker build -t genai .
   ```
2. Run the Docker container:
   ```sh
   docker run -p 8080:8080 genai
   ```
3. Visit [http://localhost:8080](http://localhost:8080)

## Deploying to Google Cloud Run

1. Set your Google Cloud project:
   ```sh
   gcloud config set project paulbonneville-com
   ```
2. Build the container and push to Google Container Registry:
   ```sh
   docker build -t gcr.io/paulbonneville-com/genai .
   docker push gcr.io/paulbonneville-com/genai
   ```
3. Deploy to Cloud Run (with authentication required):
   ```sh
   gcloud run deploy genai \
     --image gcr.io/paulbonneville-com/genai \
     --platform managed \
     --region us-central1 \
     --no-allow-unauthenticated
   ```
4. After deployment, Cloud Run will provide a service URL. For this project, it is:
   ```
   https://genai-860937201650.us-central1.run.app
   ```

---

## Authenticating and Testing the Cloud Run Service with a Service Account

To securely test your private Cloud Run service, use a dedicated service account. **Do not commit the key file to version control.**

1. **Create the service account:**
   ```sh
   gcloud iam service-accounts create genai-app \
     --display-name="GenAI App Service Account"
   ```
2. **Grant the service account the Cloud Run Invoker role:**
   ```sh
   gcloud run services add-iam-policy-binding genai \
     --region us-central1 \
     --member="serviceAccount:genai-app@paulbonneville-com.iam.gserviceaccount.com" \
     --role="roles/run.invoker"
   ```
3. **Create and download the service account key:**
   ```sh
   gcloud iam service-accounts keys create genai-app-key.json \
     --iam-account genai-app@paulbonneville-com.iam.gserviceaccount.com
   ```
   - This will create a file called `genai-app-key.json` in your current directory.
   - **Keep this file secure and do not commit it to version control.**
4. **Authenticate locally using the service account:**
   ```sh
   gcloud auth activate-service-account \
     --key-file=genai-app-key.json
   ```
5. **Obtain an identity token and test the service:**
   ```sh
   export SERVICE_URL="https://genai-860937201650.us-central1.run.app"
   export TOKEN=$(gcloud auth print-identity-token)
   curl -H "Authorization: Bearer $TOKEN" $SERVICE_URL
   ```

You should receive the expected JSON response from your service if authentication is configured correctly.

---

Replace `[REGION]` with your actual Google Cloud region if different from `us-central1`.

## Continuous Deployment with Google Cloud Run

This project is configured so that Google Cloud Run automatically builds and deploys your application whenever you push changes to the `main` branch of your repository. This is achieved by a Cloud Build trigger in the Google Cloud Console that watches your repository for changes. When a new commit is pushed to `main`, Cloud Build builds your Docker image and deploys it to Cloud Run automatically.

This enables a seamless CI/CD workflow, ensuring that your latest code is always running in production without manual intervention.

For more information, see the [Cloud Run Continuous Deployment documentation](https://cloud.google.com/run/docs/continuous-deployment).

