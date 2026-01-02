# Backend Production - Arabic Qamoos API

## 📦 Contents

### Production Server
- **`server_postgresql.py`** - Main Flask API server with PostgreSQL backend
- **`requirements_postgresql.txt`** - Python dependencies for production
- **`runtime.txt`** - Python version for deployment (3.12)
- **`Procfile`** - Heroku/Cloud Run configuration
- **`Dockerfile`** - Docker containerization
- **`.dockerignore`** / **`.gcloudignore`** - Deployment exclusions

### Data Extraction Scripts
- **`extract_dictionary_v2.py`** - Main extraction script for dictionaries 1, 2, 4, 5, 7-10
- **`scripts/`** - Additional extraction and processing scripts
  - `extract_ayn_fixed.py` - Dictionary 3 (كتاب العين) with special handling
  - `process_grammar_books.py` - Grammar books extraction
  - `optimize_books_json.py` - JSON optimization for grammar library
  - `fix_grammar_books.py` - Content cleanup and quality improvements

### Database
- **PostgreSQL** (not included - hosted on Google Cloud Run)
- Database URL set via `DATABASE_URL` environment variable

---

## 🚀 Deployment

### Google Cloud Run (Current Production)

1. **Build and deploy**:
```bash
gcloud run deploy qamoos-api \
  --source . \
  --region us-east1 \
  --allow-unauthenticated \
  --set-env-vars DATABASE_URL=postgresql://...
```

2. **Environment variables**:
```bash
DATABASE_URL=postgresql://user:pass@host:5432/qamoos_db
PORT=8080
FLASK_ENV=production
```

### Local Development

1. **Install dependencies**:
```bash
pip install -r requirements_postgresql.txt
```

2. **Set environment**:
```bash
export DATABASE_URL=postgresql://localhost:5432/qamoos_db
export FLASK_ENV=development
```

3. **Run server**:
```bash
python server_postgresql.py
```

Server runs on: `http://localhost:5000`

---

## 📊 Database Schema

### Main Tables
- **dictionaries** (9 dictionaries)
- **entries** (177,075 main entries)
- **sub_entries** (11,967 derivative entries)
- **definitions** (structured definitions)
- **chapters** (أبواب)
- **sections** (فصول)

### Data Sources
Located in parent directory: `../data/`
- `القاموس المحيط.htm` - Dictionary 1
- `alwaseet1.htm`, `alwaseet2.htm` - Dictionary 2
- `العين/001.htm - 008.htm` - Dictionary 3 (8 files)
- Grammar books in `../data/grammar/`

---

## 🔧 API Endpoints

All endpoints documented in: `../docs_important/FLUTTER_INTEGRATION_GUIDE.md`

### Quick Reference
- `GET /api/dictionaries` - List all 9 dictionaries
- `GET /api/search?q=كتب&mode=all&limit=20` - Search entries
- `GET /api/entry/<id>` - Get entry details
- `GET /api/stats` - Database statistics
- `GET /api/chapters?dictionary_id=2` - Get chapters

---

## 🛡️ Security

**Current**: Public API (no authentication)
- CORS enabled for mobile apps
- Rate limiting: None (Google Cloud Run auto-scales)
- Cost: Within free tier (< 2M requests/month)

**Future considerations**:
- Add API keys for premium features
- Rate limiting via Cloudflare Worker
- Request logging and analytics

---

## 📝 Notes

- **Production URL**: https://qamoos-api-804325795495.us-east1.run.app
- **Frontend proxy**: Cloudflare Worker at qamoos.org proxies to this backend
- **Database**: PostgreSQL hosted on Google Cloud SQL
- **Monitoring**: Google Cloud Console → Cloud Run dashboard
