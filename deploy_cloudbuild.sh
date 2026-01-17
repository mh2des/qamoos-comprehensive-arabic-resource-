#!/bin/bash
# Deploy using Cloud Build (avoids local ZIP issue)
set -e

PROJECT_ID="qamoos-org"
SERVICE_NAME="qamoos-api"
REGION="us-east1"

echo "================================================"
echo "Deploying via Cloud Build (source upload)..."
echo "================================================"

# Submit build to Cloud Build service
gcloud builds submit \
  --tag gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest \
  --timeout=10m \
  .

echo ""
echo "================================================"
echo "Deploying to Cloud Run..."
echo "================================================"

# Deploy the built image
gcloud run deploy ${SERVICE_NAME} \
  --image gcr.io/${PROJECT_ID}/${SERVICE_NAME}:latest \
  --region ${REGION} \
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
echo "URL: https://qamoos-api-804325795495.us-east1.run.app"
