#!/bin/bash

# Stop and remove any running container named 'genai'
if [ $(docker ps -q -f name=genai) ]; then
  echo "Stopping running 'genai' container..."
  docker stop genai
  docker rm genai
fi

# Build the Docker image
echo "Building Docker image 'genai'..."
docker build -t genai .

# Run the Docker container
echo "Running Docker container 'genai' on port 8080..."
docker run -d --name genai -p 8080:8080 genai

# Wait for the app to start
echo "Waiting for the app to start..."
sleep 3

# Test the endpoint
echo "Testing the local endpoint: http://localhost:8080/"
curl --fail http://localhost:8080/ || { echo "App did not respond as expected."; exit 1; }
echo -e "\nApp is running and responded successfully." 