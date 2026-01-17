#!/bin/bash
# Deploy script for Cloud Run
set -e

echo "Deploying qamoos-api to Cloud Run..."
echo "Region: us-east1"
echo "Project: qamoos-org"
echo ""

# Deploy to Cloud Run
gcloud run deploy qamoos-api \
  --source . \
  --region us-east1 \
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
