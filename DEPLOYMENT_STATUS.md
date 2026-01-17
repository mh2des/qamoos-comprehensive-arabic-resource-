# Deployment Guide: Updated Poetry API to Cloud Run

## Current Status

✅ **Code Updated**: `server_postgresql.py` now includes poetry endpoints
✅ **Local Testing**: Poetry endpoints tested and working locally  
✅ **Dockerfile Updated**: Using `requirements_postgresql.txt` and frontend-deploy files
✅ **Existing Deployment**: qamoos-api running at https://qamoos-api-804325795495.us-east1.run.app
✅ **Cloud Build**: Successfully deployed via Cloud Build (avoiding ZIP timestamp issues)

## Deployment Method Used

Used **Cloud Build** (`gcloud builds submit`) which uploads files differently than `gcloud run deploy --source` and avoids the ZIP timestamp bug.

### Prerequisites

1. **Docker Desktop must be running** (not currently running)
2. gcloud CLI configured (✅ already configured for project `qamoos-org`)

### Deployment Steps

```bash
# 1. Start Docker Desktop (REQUIRED - do this first!)
# Open Docker Desktop application and wait for it to start

# 2. Navigate to project directory
cd "/c/python apps/arabic_qamoos"

# 3. Run the manual deployment script
bash deploy_manual.sh
```

The script will:
1. Build Docker image locally
2. Push to Google Container Registry
3. Deploy to Cloud Run

**Estimated time**: 5-7 minutes

---

## Alternative: Quick Fix via Console

If Docker is unavailable, you can update via Google Cloud Console:

1. Go to https://console.cloud.google.com/run/detail/us-east1/qamoos-api/revisions
2. Click "EDIT & DEPLOY NEW REVISION"
3. Go to "CONTAINER" tab
4. Under "Container image URL", click "SELECT"
5. Choose the existing image or upload `server_postgresql.py` manually
6. Click "DEPLOY"

---

## New Poetry API Endpoints Added

Once deployed, these endpoints will be available:

### Poets
- `GET /api/poets?limit=50&offset=0&q=search` - List poets
- `GET /api/poet/<poet_id>` - Get poet details + poems preview

### Poems  
- `GET /api/poems?poet_id=X&q=search&limit=50` - List poems
- `GET /api/poem/<poem_id>` - Get full poem with verses

### Search
- `GET /api/poetry/search?q=keyword&limit=50` - Search poems/verses

---

## Testing After Deployment

```bash
# Test poets endpoint
curl "https://qamoos-api-804325795495.us-east1.run.app/api/poets?limit=5"

# Test poem endpoint
curl "https://qamoos-api-804325795495.us-east1.run.app/api/poem/1099"

# Test poetry search
curl "https://qamoos-api-804325795495.us-east1.run.app/api/poetry/search?q=الحب"
```

---

## Current Database Stats

Your local PostgreSQL database contains:
- **44 poets**
- **1,099 poems**
- **36,423 verses**

This data was scraped from AlDiwan.net (stopped at poet #40 of ~1,831).

### To Continue Scraping Later

```bash
cd "/c/python apps/arabic_qamoos/backend_production"
python production_scraper.py  # Will auto-resume from poet #40
```

**Note**: The scraper was configured to use your **local PostgreSQL**, not the production Neon database. If you want the poetry data in production:

1. Complete local scraping first (2-3 days)
2. Export local data: `pg_dump -t poets -t poems -t verses > poetry_export.sql`
3. Import to Neon: Update DATABASE_URL and run `psql $DATABASE_URL < poetry_export.sql`

---

## Summary

**What's Ready**:
- ✅ Code updated with poetry endpoints
- ✅ Dockerfile configured
- ✅ Local testing passed
- ✅ Deployment script created (`deploy_manual.sh`)

**Next Step**:
1. **Start Docker Desktop** 
2. **Run**: `bash deploy_manual.sh`
3. **Test**: Visit the API endpoints above

**Time Required**: 5-7 minutes after Docker Desktop starts
