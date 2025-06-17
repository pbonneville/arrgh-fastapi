import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from main import app
from fastapi.testclient import TestClient
import main

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "environment" in data
    assert "version" in data
    assert data["message"] == "Welcome to your FastAPI app on Google Cloud Run! This is a test."

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "environment" in data
    assert "version" in data
    assert "service" in data

def test_readiness_check():
    response = client.get("/ready")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "environment" in data
    assert "version" in data

def test_health_check_during_shutdown():
    """Test that health check returns unhealthy status during shutdown."""
    # First, verify normal healthy state
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    
    # Simulate shutdown condition by setting the shutdown flag
    original_shutdown_event = main.shutdown_event
    try:
        main.shutdown_event = True
        
        # Now health check should return unhealthy
        response = client.get("/health")
        assert response.status_code == 503
        data = response.json()
        assert data["status"] == "unhealthy"
        assert data["message"] == "Service is shutting down"
        
    finally:
        # Reset the shutdown flag to not affect other tests
        main.shutdown_event = original_shutdown_event 