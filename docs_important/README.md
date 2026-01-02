# Arabic Qamoos - Project Organization# القاموس المحيط Dictionary Extraction System



## 📁 Directory StructureProfessional extraction system for converting the HTML dictionary into a structured SQLite database for Flutter mobile application integration.



```## 📋 Project Overview

arabic_qamoos/

├── backend_production/          # Production backend (Google Cloud Run)**Dictionary:** القاموس المحيط (Al-Qamus Al-Muhit)  

│   ├── server_postgresql.py     # Flask API server**Author:** الفيروزآبادي (Al-Firuzabadi)  

│   ├── extract_dictionary_v2.py # Dictionary extraction**Edition:** 8th Edition, 2005  

│   ├── scripts/                 # Processing scripts**Source:** HTML file (1,392 lines, ~1,357 pages)  

│   ├── requirements_postgresql.txt**Target:** SQLite database for Flutter mobile app

│   ├── Dockerfile

│   ├── Procfile## 🏗️ Architecture

│   └── README.md                # Backend documentation

│### Phase 1: Data Extraction (Current)

├── frontend-deploy/             # Production frontend (Cloudflare Pages)- **HTML Parser:** BeautifulSoup-based parser for structured extraction

│   ├── index.html               # Homepage- **Text Normalizer:** Arabic diacritic removal for search optimization

│   ├── search.html              # Search interface- **Database Manager:** SQLite schema creation and data insertion

│   ├── grammar/                 # Grammar library (48 books)- **Entry Parser:** Intelligent parsing of dictionary entries

│   ├── _worker.js               # API proxy

│   ├── robots.txt, sitemap.xml  # SEO### Components

│   └── README.md                # Frontend documentation

│1. **`extract_dictionary.py`** - Main extraction script

├── docs_important/              # Essential documentation2. **`validate_database.py`** - Database validation and quality checks

│   ├── README.md                # Project overview (this file)3. **`requirements.txt`** - Python dependencies

│   ├── FLUTTER_INTEGRATION_GUIDE.md

│   └── FLUTTER_API_QUICK_REFERENCE.md## 🚀 Quick Start

│

├── data/                        # Source data (HTML dictionaries)### Prerequisites

│   ├── القاموس المحيط.htm

│   ├── alwaseet1.htm, alwaseet2.htm- Python 3.8 or higher

│   ├── العين/                   # 8 HTML files- pip package manager

│   └── grammar/                 # Grammar books HTML

│### Installation

├── _archive/                    # Old files (not needed for production)

│   ├── test_files/              # Test scripts1. **Install dependencies:**

│   ├── old_scripts/             # Legacy scripts```bash

│   ├── old_md_files/            # Old documentationpip install -r requirements.txt

│   └── logs/                    # Log files```

│

├── .env                         # Environment variables (local)2. **Run extraction:**

├── .env.example                 # Example env file```bash

├── qamoos_database.sqlite       # Local SQLite (development)python extract_dictionary.py

└── requirements.txt             # Python dependencies```

```

3. **Validate results:**

---```bash

python validate_database.py

## 🎯 Quick Start```



### Run Backend Locally## 📊 Database Schema

```bash

cd backend_production### Core Tables

pip install -r requirements_postgresql.txt

export DATABASE_URL=postgresql://localhost:5432/qamoos_db- **chapters** - باب level (e.g., باب الهمزة)

python server_postgresql.py- **sections** - فصل level (e.g., فصل الباء)

```- **entries** - Individual dictionary entries with full metadata

- **definitions** - Multiple definitions per entry

### Deploy Backend- **grammatical_forms** - Verb conjugations and patterns

```bash- **plurals** - Plural forms (ج:)

cd backend_production- **markers** - Place markers (ع، د، ة، م)

gcloud run deploy qamoos-api --source . --region us-east1- **cross_references** - Inter-entry references

```- **notes** - Editorial notes and corrections

- **entries_fts** - Full-text search index (FTS5)

### Deploy Frontend

```bash### Key Features

cd frontend-deploy

npx wrangler pages deploy . --project-name qamoos-org --branch production- ✅ **Hierarchical organization** preserved (باب → فصل → entries)

```- ✅ **Dual text storage** (original with diacritics + normalized)

- ✅ **Full-text search** enabled via FTS5

---- ✅ **Page references** maintained

- ✅ **Foreign key constraints** for data integrity

## 🌐 Production URLs- ✅ **Optimized indexes** for fast queries



- **Website**: https://qamoos.org## 📝 Entry Structure

- **API**: https://qamoos.org/api (proxied to Google Cloud Run)

- **Grammar Library**: https://qamoos.org/grammar/Each dictionary entry contains:



---- **Headword** (with diacritics)

- **Normalized headword** (no diacritics for search)

## 📚 What's What- **Root letters** (trilateral/quadrilateral)

- **Grammatical pattern** (e.g., كَرَضِيَ، كَدَعَا)

### Essential Files (Keep These!)- **Multiple definitions**

- **Plural forms** marked with ج:

#### Backend- **Place markers** (ع، د، ة، م)

- `backend_production/server_postgresql.py` - Main API server- **Cross-references** to related entries

- `backend_production/extract_dictionary_v2.py` - Dictionary extraction- **Page number** from original source

- `backend_production/scripts/` - Data processing scripts- **Full text** preserved

- `backend_production/requirements_postgresql.txt` - Dependencies

## 🔍 Search Capabilities

#### Frontend

- Everything in `frontend-deploy/` - Complete production siteThe database supports:

- `frontend-deploy/_worker.js` - API proxy (critical!)

- `frontend-deploy/grammar/` - Grammar library1. **Exact search** - Match with diacritics

2. **Fuzzy search** - Match without diacritics

#### Documentation3. **Root-based search** - Find all derivatives

- `docs_important/FLUTTER_INTEGRATION_GUIDE.md` - API integration guide4. **Full-text search** - Search within definitions

- `docs_important/FLUTTER_API_QUICK_REFERENCE.md` - Quick API reference5. **Autocomplete** - Prefix-based suggestions

- `backend_production/README.md` - Backend docs

- `frontend-deploy/README.md` - Frontend docs## 📈 Expected Output



#### DataAfter successful extraction:

- `data/` - Source HTML files (needed for re-extraction)

- `qamoos_database.sqlite` - Local database (development)- **Database file:** `qamoos_database.sqlite`

- **Log file:** `extraction.log`

### Archived Files (Can Delete If Needed)- **Statistics:**

  - ~1,392 pages processed

All files in `_archive/` are old/unused:  - Multiple chapters (باب)

- `_archive/test_files/` - Test scripts (test_*.py, check_*.py)  - Hundreds of sections (فصل)

- `_archive/old_scripts/` - Legacy scripts (migrate_*.py, simple_server.py)  - Thousands of entries

- `_archive/old_md_files/` - Old documentation (50+ MD files)  - Complete metadata

- `_archive/logs/` - Log files

## 🧪 Validation Tests

---

The validation script checks:

## 🗄️ Database

- ✓ Schema completeness (all tables exist)

### Production- ✓ Data counts (entries, chapters, sections)

- **PostgreSQL** on Google Cloud SQL- ✓ Page coverage (all pages processed)

- **189,042 entries** (177,075 main + 11,967 sub-entries)- ✓ Hierarchy integrity (no orphaned records)

- **9 dictionaries**- ✓ Text normalization (diacritics properly removed)

- Connection: Set via `DATABASE_URL` environment variable- ✓ FTS index (search capability)

- ✓ Sample searches (functionality tests)

### Local Development

- **SQLite** (`qamoos_database.sqlite`)## 📂 File Structure

- Same schema as PostgreSQL

- Good for testing extraction scripts```

arabic_qamoos/

---├── data/

│   └── القاموس المحيط.htm          # Source HTML file

## 🔄 Common Tasks├── extract_dictionary.py            # Main extraction script

├── validate_database.py             # Validation script

### Re-extract Dictionaries├── requirements.txt                 # Python dependencies

```bash├── README.md                        # This file

cd backend_production├── extraction.log                   # Execution log (generated)

python extract_dictionary_v2.py  # Dictionaries 1, 2, 4, 5, 7-10└── qamoos_database.sqlite          # Output database (generated)

python scripts/extract_ayn_fixed.py  # Dictionary 3 (كتاب العين)```

```

## 🔧 Configuration

### Update Grammar Books

```bashEdit the following in `extract_dictionary.py` if needed:

cd backend_production

python scripts/process_grammar_books.py  # Process HTML files```python

python scripts/optimize_books_json.py     # Create optimized JSONsHTML_FILE = r"c:\python apps\arabic_qamoos\data\القاموس المحيط.htm"

# Copy output to frontend-deploy/grammar/data/DB_FILE = r"c:\python apps\arabic_qamoos\qamoos_database.sqlite"

``````



### Deploy Updates## 📊 Sample Statistics

```bash

# BackendExpected extraction results:

cd backend_production

gcloud run deploy qamoos-api --source .- **Total Pages:** ~1,392

- **Total Chapters:** ~29 (based on Arabic letters)

# Frontend- **Total Sections:** Hundreds (فصل subdivisions)

cd frontend-deploy- **Total Entries:** Thousands

npx wrangler pages deploy . --project-name qamoos-org --branch production- **Total Definitions:** Tens of thousands

```- **Total Plurals:** Thousands



---## 🐛 Troubleshooting



## 📊 Statistics### Issue: Import errors

```bash

- **Dictionaries**: 9 classical Arabic dictionaries# Solution: Install dependencies

- **Entries**: 189,042 totalpip install -r requirements.txt

- **Grammar Books**: 48 books (4 categories)```

- **API Endpoints**: 6 main endpoints

- **Response Time**: < 200ms average### Issue: File not found

- **Monthly Requests**: < 2M (within free tier)```bash

# Solution: Check HTML file path

---# Verify the file exists at the specified location

```

## 🛠️ Tech Stack

### Issue: Database locked

**Backend:**```bash

- Python 3.12# Solution: Close any open connections

- Flask (REST API)# Delete the .sqlite file and re-run extraction

- PostgreSQL (database)```

- Google Cloud Run (hosting)

## 🚦 Next Steps (Phases 2-6)

**Frontend:**

- HTML5, CSS3, JavaScript- [ ] **Phase 2:** Enhanced entry parsing (cross-references, notes)

- Cloudflare Pages (hosting)- [ ] **Phase 3:** Search algorithm optimization

- Cloudflare Worker (API proxy)- [ ] **Phase 4:** Flutter app integration

- AOS (animations)- [ ] **Phase 5:** UI/UX implementation

- [ ] **Phase 6:** Testing and deployment

**Tools:**

- BeautifulSoup4 (HTML parsing)## 📞 Support

- Wrangler (Cloudflare CLI)

- gcloud (Google Cloud CLI)For issues or questions:

1. Check the `extraction.log` file for errors

---2. Run validation script for diagnostics

3. Review this README for configuration

## 📝 Notes

## 📜 License

### Why This Organization?

This extraction system is created for the القاموس المحيط dictionary project.

1. **Clear separation**: Backend, Frontend, Docs, Archive

2. **Production-ready**: Only essential files in main directories## 🎯 Quality Standards

3. **Easy deployment**: Each directory has its own README

4. **Clean workspace**: Old files archived, not deleted- **Code Quality:** Professional, documented, modular

5. **Documentation**: Critical docs in `docs_important/`- **Data Integrity:** Foreign keys, constraints, validation

- **Performance:** Indexed searches, optimized queries

### What Was Archived?- **Completeness:** All data preserved from source

- **Maintainability:** Clear structure, logging, error handling

- **50+ old MD files** - Migration guides, old status reports, completion summaries

- **20+ test scripts** - check_*.py, test_*.py, analyze_*.py---

- **Old servers** - simple_server.py, server_postgresql_BROKEN.py.bak

- **Migration scripts** - migrate_*.py (PostgreSQL migration complete)**Status:** Phase 1 Implementation Complete ✓  

- **Log files** - *.log, sub_output.txt**Next:** Run extraction and validate results

- **Duplicate HTML** - Root-level HTML files (duplicates of frontend-deploy/)

### Can I Delete _archive/?

Yes, if you don't need old code for reference. Everything essential is in:
- `backend_production/`
- `frontend-deploy/`
- `docs_important/`
- `data/`

---

## 🆘 Help

- **Backend issues**: See `backend_production/README.md`
- **Frontend issues**: See `frontend-deploy/README.md`
- **Flutter integration**: See `docs_important/FLUTTER_INTEGRATION_GUIDE.md`
- **API reference**: See `docs_important/FLUTTER_API_QUICK_REFERENCE.md`

---

## ✅ Project Status

**Current State**: ✅ Production-ready and deployed

- [x] Backend deployed to Google Cloud Run
- [x] Frontend deployed to Cloudflare Pages
- [x] API fully functional (189K entries)
- [x] Grammar library live (48 books)
- [x] Mobile-responsive design
- [x] SEO optimized
- [x] Documentation complete
- [x] Workspace organized

**Next Steps**: Flutter app integration (see Flutter guides in docs_important/)
