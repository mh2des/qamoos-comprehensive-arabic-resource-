#!/bin/bash
# Manual Docker build and deploy script
set -e

PROJECT_ID="qamoos-org"
SERVICE_NAME="qamoos-api"
REGION="us-east1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest"

echo "================================================"
echo "Building Docker image locally..."
echo "================================================"

# Build the Docker image
docker build -t "${IMAGE_NAME}" .

echo ""
echo "================================================"
echo "Pushing image to Google Container Registry..."
echo "================================================"

# Configure Docker to use gcloud as credential helper
gcloud auth configure-docker gcr.io --quiet

# Push the image
docker push "${IMAGE_NAME}"

echo ""
echo "================================================"
echo "Deploying to Cloud Run..."
echo "================================================"

# Deploy the image to Cloud Run
gcloud run deploy "${SERVICE_NAME}" \
  --image "${IMAGE_NAME}" \
  --region "${REGION}" \
  --platform managed \
  --allow-unauthenticated \
  --memory 512Mi \
  --cpu 1 \
  --max-instances 10 \
  --timeout 120 \
  --set-env-vars "FLASK_ENV=production" \
  --quiet

echo ""
echo "✅ Deployment complete!"
echo "Service URL: https://qamoos-api-804325795495.us-east1.run.app"
echo "================================================"
