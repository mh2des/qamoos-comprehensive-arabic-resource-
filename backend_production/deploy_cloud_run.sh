#!/usr/bin/env bash
# Deployment helper: build image and deploy to Google Cloud Run
# Usage:
#   PROJECT_ID=my-gcp-project IMAGE_NAME=qamoos-poetry REGION=us-central1 SERVICE_NAME=qamoos-service ./deploy_cloud_run.sh

set -euo pipefail

PROJECT_ID=${PROJECT_ID:-}
IMAGE_NAME=${IMAGE_NAME:-qamoos-poetry}
REGION=${REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-qamoos-service}
TAG=${TAG:-latest}

if [ -z "$PROJECT_ID" ]; then
  echo "PROJECT_ID is required. Example: PROJECT_ID=my-project ./deploy_cloud_run.sh"
  exit 1
fi

# Build Docker image locally
echo "Building Docker image: gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG}"
docker build -t gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG} ..

# Push to Google Container Registry
echo "Pushing image to gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG}"
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG}

# Deploy to Cloud Run
echo "Deploying to Cloud Run service: ${SERVICE_NAME} in ${REGION}"
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${IMAGE_NAME}:${TAG} \
  --region ${REGION} \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars "DATABASE_URL=${DATABASE_URL:-}" \
  --memory 512Mi

echo "Deployment finished. Visit the Cloud Run URL shown above."
