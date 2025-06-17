import os
import signal
import sys
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Environment configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")
VERSION = os.getenv("VERSION", "1.0.0")

# Global shutdown flag
shutdown_event = False

def signal_handler(signum, frame):
    """Handle shutdown signals gracefully."""
    global shutdown_event
    logger.info(f"Received signal {signum}, initiating graceful shutdown...")
    shutdown_event = True

# Register signal handlers
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info(f"Starting FastAPI app - Environment: {ENVIRONMENT}, Version: {VERSION}")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI app")

app = FastAPI(
    title="FastAPI Cloud Run App",
    version=VERSION,
    lifespan=lifespan
)

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {
        "message": "Welcome to your FastAPI app on Google Cloud Run! This is a test.",
        "environment": ENVIRONMENT,
        "version": VERSION
    }

@app.get("/health")
def health_check():
    """Health check endpoint for Cloud Run."""
    if shutdown_event:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "message": "Service is shutting down"}
        )
    
    return {
        "status": "healthy",
        "environment": ENVIRONMENT,
        "version": VERSION,
        "service": "fastapi-cloud-run"
    }

@app.get("/ready")
def readiness_check():
    """Readiness check endpoint for Cloud Run."""
    # Add any application-specific readiness checks here
    # (database connections, external services, etc.)
    return {
        "status": "ready",
        "environment": ENVIRONMENT,
        "version": VERSION
    } 