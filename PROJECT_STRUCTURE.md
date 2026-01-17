# Arabic Qamoos - Clean Project Structure

## Ì≥ã Overview

Your workspace has been organized into clear, separated directories:

```
arabic_qamoos/
‚îú‚îÄ‚îÄ Ì≥¶ backend_production/     ‚Üê Backend API (Google Cloud Run)
‚îú‚îÄ‚îÄ Ìºê frontend-deploy/        ‚Üê Frontend website (Cloudflare Pages)  
‚îú‚îÄ‚îÄ Ì≥ö docs_important/          ‚Üê Essential documentation
‚îú‚îÄ‚îÄ Ì≥Å data/                    ‚Üê Source HTML dictionaries
‚îú‚îÄ‚îÄ Ì∑ÑÔ∏è _archive/                ‚Üê Old/unused files (can delete)
‚îî‚îÄ‚îÄ Ì¥ß Root files               ‚Üê Config files (.env, requirements.txt)
```

---

## ÌæØ Production Files

### Backend (backend_production/)
**Purpose**: Flask API server with PostgreSQL database

**Essential files**:
- `server_postgresql.py` - Main API server ‚≠ê
- `extract_dictionary_v2.py` - Dictionary extraction
- `scripts/` - Processing scripts
- `requirements_postgresql.txt` - Dependencies
- `Dockerfile`, `Procfile` - Deployment configs

**Deploy**: `gcloud run deploy qamoos-api --source .`

---

### Frontend (frontend-deploy/)
**Purpose**: Complete production website

**Essential files**:
- `index.html` - Homepage ‚≠ê
- `search.html` - Search interface ‚≠ê
- `_worker.js` - Cloudflare Worker (API proxy) ‚≠ê
- `grammar/` - Grammar library (48 books) ‚≠ê
- Static pages: about.html, contact.html, sources.html, etc.
- SEO: robots.txt, sitemap.xml

**Deploy**: `npx wrangler pages deploy . --project-name qamoos-org --branch production`

---

### Documentation (docs_important/)
**Purpose**: Essential guides and references

**Files**:
- `README.md` - Project overview ‚≠ê
- `FLUTTER_INTEGRATION_GUIDE.md` - Complete Flutter guide ‚≠ê
- `FLUTTER_API_QUICK_REFERENCE.md` - Quick API reference ‚≠ê

---

### Data (data/)
**Purpose**: Source HTML files for extraction

**Contents**:
- `ÿßŸÑŸÇÿßŸÖŸàÿ≥ ÿßŸÑŸÖÿ≠Ÿäÿ∑.htm` - Dictionary 1
- `alwaseet1.htm`, `alwaseet2.htm` - Dictionary 2
- `ÿßŸÑÿπŸäŸÜ/` - Dictionary 3 (8 HTML files)
- `grammar/` - Grammar books HTML

**Note**: Keep these! Needed for re-extraction.

---

## Ì∑ëÔ∏è Archived Files (_archive/)

Everything in `_archive/` is **OLD/UNUSED**. Safe to delete if you don't need historical reference.

### What's Archived:
- **test_files/** - 20+ test scripts (test_*.py, check_*.py, analyze_*.py)
- **old_scripts/** - Legacy scripts (migrate_*.py, simple_server.py, etc.)
- **old_md_files/** - 50+ old documentation files
- **logs/** - Log files (*.log, sub_output.txt)

### Why Archived:
- Test scripts ‚Üí No longer needed (testing complete)
- Migration scripts ‚Üí Migration to PostgreSQL complete
- Old MD files ‚Üí Replaced by organized documentation
- simple_server.py ‚Üí Using server_postgresql.py instead

---

## Ì¥ß Root Level Files

### Keep These:
- `.env` - Environment variables (local development)
- `.env.example` - Example environment file
- `requirements.txt` - Python dependencies
- `qamoos_database.sqlite` - Local SQLite database (development)
- `PROJECT_STRUCTURE.md` - This file!

### Optional:
- `.github/` - GitHub workflows (if using)
- `.venv/` - Python virtual environment
- `__pycache__/` - Python cache (can delete, auto-regenerates)

---

## Ì≥ä Quick Stats

- **Dictionaries**: 9 classical Arabic dictionaries
- **Total Entries**: 189,042 (177,075 main + 11,967 sub-entries)
- **Grammar Books**: 48 books
- **API Endpoints**: 6 main endpoints
- **Response Time**: < 200ms average

---

## Ì∫Ä Common Commands

### Backend
```bash
# Run locally
cd backend_production
pip install -r requirements_postgresql.txt
python server_postgresql.py

# Deploy
gcloud run deploy qamoos-api --source .
```

### Frontend
```bash
# Deploy
cd frontend-deploy
npx wrangler pages deploy . --project-name qamoos-org --branch production
```

### Re-extract Dictionaries
```bash
cd backend_production
python extract_dictionary_v2.py  # Most dictionaries
python scripts/extract_ayn_fixed.py  # ŸÉÿ™ÿßÿ® ÿßŸÑÿπŸäŸÜ
```

---

## Ìºê Live URLs

- **Website**: https://qamoos.org
- **API**: https://qamoos.org/api
- **Grammar**: https://qamoos.org/grammar/

---

## Ì≥ñ Documentation

All essential docs are in `docs_important/`:
- Project overview ‚Üí `docs_important/README.md`
- Flutter integration ‚Üí `docs_important/FLUTTER_INTEGRATION_GUIDE.md`
- API reference ‚Üí `docs_important/FLUTTER_API_QUICK_REFERENCE.md`
- Backend details ‚Üí `backend_production/README.md`
- Frontend details ‚Üí `frontend-deploy/README.md`

---

## ‚úÖ Cleanup Summary

### Moved to Archive:
- 20+ test Python scripts
- 50+ old Markdown documentation files
- Legacy migration scripts
- Old server files (simple_server.py)
- Log files
- Duplicate HTML files

### Organized Into:
- `backend_production/` - All backend code
- `frontend-deploy/` - All frontend code
- `docs_important/` - Essential documentation
- `_archive/` - Everything else

### Result:
- ‚úÖ Clear separation of concerns
- ‚úÖ Easy to find production files
- ‚úÖ Clean workspace
- ‚úÖ Nothing deleted (just organized)

---

## ÌæØ Next Steps

1. **Review** the organized structure
2. **Delete** `_archive/` if you don't need old files
3. **Use** Flutter guides in `docs_important/` for app integration
4. **Deploy** any pending updates

---

## Ì≤° Tips

- Want to find something? Check `_archive/` first
- Need to re-extract? Scripts are in `backend_production/`
- Deploying? Use commands above
- Stuck? Read READMEs in each directory

**Your project is now clean and organized!** Ìæâ
