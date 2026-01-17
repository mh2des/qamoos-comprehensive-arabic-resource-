<div align="center">

# 📚 Qamoos.org - Arabic Language Platform

### المرجع العربي الشامل | Comprehensive Arabic Reference

[![Live Site](https://img.shields.io/badge/🌐_Live-qamoos.org-success?style=for-the-badge)](https://qamoos.org)
[![API Status](https://img.shields.io/badge/API-Online-blue?style=for-the-badge&logo=googlecloud)](https://qamoos-api-804325795495.us-east1.run.app/health)
[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

<br/>

**🔍 189,042 Dictionary Entries** · **📖 48 Grammar Books** · **🎭 36,423 Poetry Verses**

<br/>

[🌐 Live Demo](https://qamoos.org) · [📡 API Docs](docs_important/FLUTTER_API_QUICK_REFERENCE.md) · [⚙️ Tech Stack](TECH_STACK_AND_FEATURES.md)

</div>

---

## 💡 Why I Built This

As a native Arabic speaker passionate about preserving linguistic heritage, I noticed that classical Arabic dictionaries were scattered across outdated websites with poor UX. **Qamoos.org** unifies **9 major classical dictionaries** into a single, fast, searchable API — making centuries of Arabic scholarship accessible to modern developers and researchers.

**The Challenge:** Extracting and normalizing 189,000+ entries from heterogeneous HTML sources (some dating back to early 2000s web standards) while handling:
- Arabic diacritics normalization for fuzzy search
- Right-to-left text rendering
- Cross-dictionary entry linking
- Poetry verse alignment (hemistiches)

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              QAMOOS.ORG ARCHITECTURE                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────┐         ┌─────────────────┐         ┌─────────────────┐  │
│   │   Browser   │────────▶│  Cloudflare     │────────▶│  Static Files   │  │
│   │   Client    │         │  Pages (CDN)    │         │  (HTML/CSS/JS)  │  │
│   └──────┬──────┘         └────────┬────────┘         └─────────────────┘  │
│          │                         │                                        │
│          │ API Requests            │ Proxy via _worker.js                   │
│          ▼                         ▼                                        │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                      Google Cloud Run                                │  │
│   │   ┌─────────────────────────────────────────────────────────────┐   │  │
│   │   │                    Flask API Server                          │   │  │
│   │   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │  │
│   │   │  │/search   │  │/entry    │  │/poets    │  │/poem     │    │   │  │
│   │   │  │          │  │          │  │          │  │          │    │   │  │
│   │   │  │ 4 modes: │  │ Full     │  │ 44 poets │  │ 36K      │    │   │  │
│   │   │  │ exact,   │  │ entry    │  │ metadata │  │ verses   │    │   │  │
│   │   │  │ starts,  │  │ with     │  │ + poem   │  │ with     │    │   │  │
│   │   │  │ contains,│  │ defs +   │  │ counts   │  │ hemis-   │    │   │  │
│   │   │  │ all      │  │ refs     │  │          │  │ tichs    │    │   │  │
│   │   │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │   │  │
│   │   │       │             │             │             │           │   │  │
│   │   │       └─────────────┴─────────────┴─────────────┘           │   │  │
│   │   │                           │                                  │   │  │
│   │   │                    ┌──────▼──────┐                          │   │  │
│   │   │                    │  psycopg2   │                          │   │  │
│   │   │                    │  (DB Pool)  │                          │   │  │
│   │   │                    └──────┬──────┘                          │   │  │
│   │   └──────────────────────────┼──────────────────────────────────┘   │  │
│   └──────────────────────────────┼──────────────────────────────────────┘  │
│                                  │                                          │
│                                  ▼                                          │
│   ┌─────────────────────────────────────────────────────────────────────┐  │
│   │                    Google Cloud SQL (PostgreSQL)                     │  │
│   │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌───────────┐   │  │
│   │  │dictionaries │  │  entries    │  │   poets     │  │  poems    │   │  │
│   │  │ (9 dicts)   │  │ (177,075)   │  │   (44)      │  │ (1,099)   │   │  │
│   │  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├───────────┤   │  │
│   │  │sub_entries  │  │ definitions │  │   verses    │  │ chapters  │   │  │
│   │  │ (11,967)    │  │ (332,888)   │  │  (36,423)   │  │  (126)    │   │  │
│   │  └─────────────┘  └─────────────┘  └─────────────┘  └───────────┘   │  │
│   └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📊 Database Statistics

| Resource | Count | Technical Details |
|----------|------:|-------------------|
| **Dictionaries** | 9 | القاموس المحيط، المعجم الوسيط، كتاب العين، الصحاح، المحيط، المعاصر، الفقهي، التعريفات، المورد |
| **Main Entries** | 177,075 | Indexed with FTS5, normalized headwords |
| **Sub-Entries** | 11,967 | Two-tier search architecture |
| **Definitions** | 332,888 | Full-text searchable |
| **Grammar Books** | 48 | نحو، صرف، بلاغة، إعراب |
| **Chapters** | 3,384 | With progress tracking |
| **Poets** | 44 | With biographical data |
| **Poems** | 1,099 | Categorized by meter/theme |
| **Verses** | 36,423 | Hemistich-aligned for display |

---

## 🛠️ Tech Stack

### Backend
| Technology | Purpose |
|------------|---------|
| ![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white) | Runtime environment |
| ![Flask](https://img.shields.io/badge/Flask-3.0-000000?logo=flask) | RESTful API framework |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14-316192?logo=postgresql&logoColor=white) | Primary database |
| ![Gunicorn](https://img.shields.io/badge/Gunicorn-21.2-499848?logo=gunicorn) | WSGI production server |
| ![Docker](https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white) | Containerization |

### Frontend
| Technology | Purpose |
|------------|---------|
| ![HTML5](https://img.shields.io/badge/HTML5-Semantic-E34F26?logo=html5&logoColor=white) | Structure |
| ![CSS3](https://img.shields.io/badge/CSS3-Grid/Flexbox-1572B6?logo=css3&logoColor=white) | Responsive styling |
| ![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black) | Interactivity |
| ![PWA](https://img.shields.io/badge/PWA-Offline_Support-5A0FC8?logo=pwa) | Progressive Web App |

### Infrastructure
| Service | Role |
|---------|------|
| ![Google Cloud](https://img.shields.io/badge/Google_Cloud_Run-API_Hosting-4285F4?logo=googlecloud&logoColor=white) | Serverless containers |
| ![Cloudflare](https://img.shields.io/badge/Cloudflare_Pages-CDN-F38020?logo=cloudflare&logoColor=white) | Static hosting + proxy |
| ![Cloud SQL](https://img.shields.io/badge/Cloud_SQL-PostgreSQL-4285F4?logo=googlecloud&logoColor=white) | Managed database |

---

## 📁 Project Structure

```
qamoos/
├── 📂 backend/                    # Local development server (SQLite)
│   ├── simple_server.py           # 736-line Flask server
│   └── requirements.txt
│
├── 📂 backend_production/         # Production server (PostgreSQL)
│   ├── server_postgresql.py       # 503-line production API
│   ├── Dockerfile                 # Multi-stage build
│   ├── requirements_postgresql.txt
│   └── scrape_aldiwan.py          # Poetry scraper
│
├── 📂 frontend-deploy/            # Cloudflare Pages static site
│   ├── index.html                 # Landing page
│   ├── search.html                # Dictionary search UI
│   ├── poetry.html                # Poetry browser
│   ├── grammar/                   # 48 grammar books (HTML)
│   └── _worker.js                 # API proxy (CORS)
│
├── 📂 data/                       # Source HTML files
│   ├── القاموس المحيط.htm         # Dictionary 1 source
│   ├── alwaseet1.htm              # Dictionary 2 source
│   └── العين/                     # Dictionary 3 (8 files)
│
├── 📂 docs_important/             # API documentation
│   ├── FLUTTER_API_QUICK_REFERENCE.md
│   └── FLUTTER_INTEGRATION_GUIDE.md
│
├── 📄 extract_dictionary_v2.py    # ETL: HTML → SQLite
├── 📄 Dockerfile                  # Production container
├── 📄 deploy.sh                   # One-click GCP deployment
└── 📄 TECH_STACK_AND_FEATURES.md  # Complete tech documentation
```

---

## 🔌 REST API Reference

### Dictionary Endpoints

| Method | Endpoint | Description | Response Time |
|--------|----------|-------------|---------------|
| `GET` | `/api/dictionaries` | List all 9 dictionaries | ~50ms |
| `GET` | `/api/search?q=كتاب&mode=all` | Multi-mode search | ~100ms |
| `GET` | `/api/entry/{id}` | Full entry with definitions | ~80ms |
| `GET` | `/api/stats` | Database statistics | ~30ms |

### Poetry Endpoints

| Method | Endpoint | Description | Response Time |
|--------|----------|-------------|---------------|
| `GET` | `/api/poets?limit=50` | List poets with poem counts | ~60ms |
| `GET` | `/api/poet/{id}` | Poet details + poems preview | ~90ms |
| `GET` | `/api/poem/{id}` | Full poem with verses | ~70ms |
| `GET` | `/api/poetry/search?q=الحب` | Search poems/verses | ~120ms |

### Search Modes

```bash
# Exact match (with diacritics)
curl "https://qamoos.org/api/search?q=كِتَاب&mode=exact"

# Starts with (normalized)
curl "https://qamoos.org/api/search?q=كتب&mode=starts_with"

# Contains (substring)
curl "https://qamoos.org/api/search?q=كتاب&mode=contains"

# Full-text (headword + root + definitions)
curl "https://qamoos.org/api/search?q=كتاب&mode=all"
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+ (or SQLite for local dev)
- Docker (for production deployment)

### Local Development (SQLite)

```bash
# Clone repository
git clone https://github.com/mh2des/qamoos-comprehensive-arabic-resource-.git
cd qamoos-comprehensive-arabic-resource-

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run local server
cd backend
python simple_server.py
# 🚀 Server at http://localhost:8000
```

### Production Deployment (Docker + GCP)

```bash
# Build Docker image
docker build -t qamoos-api .

# Deploy to Google Cloud Run
gcloud run deploy qamoos-api \
  --image gcr.io/PROJECT_ID/qamoos-api \
  --platform managed \
  --region us-east1 \
  --allow-unauthenticated
```

---

## 🧪 API Examples

### Search for "كتاب" (book)

```bash
curl "https://qamoos-api-804325795495.us-east1.run.app/api/search?q=كتاب&limit=5"
```

**Response:**
```json
{
  "results": [
    {
      "entry_id": 12345,
      "headword": "كِتَاب",
      "dictionary": "المعجم الوسيط",
      "definition_preview": "ما يُكتب فيه..."
    }
  ],
  "total": 47,
  "query_time_ms": 89
}
```

### Get Poem by ID

```bash
curl "https://qamoos-api-804325795495.us-east1.run.app/api/poem/1099"
```

**Response:**
```json
{
  "poem": {
    "id": 1099,
    "title": "قصيدة الحب",
    "poet": "أحمد شوقي",
    "verses": [
      {"hemistich1": "...", "hemistich2": "..."}
    ]
  }
}
```

---

## 📈 Performance Metrics

| Metric | Value |
|--------|-------|
| API Response Time (p50) | 89ms |
| API Response Time (p99) | 187ms |
| Database Query Time | 15-45ms |
| Cold Start Time | ~2.5s |
| Concurrent Users Tested | 100+ |
| Uptime (30 days) | 99.9% |

---

## 🎯 Skills Demonstrated

| Category | Technologies & Concepts |
|----------|------------------------|
| **Backend Development** | Python, Flask, REST API design, CORS |
| **Database Engineering** | PostgreSQL, SQLite, FTS5, query optimization, schema design |
| **Data Engineering/ETL** | HTML parsing (BeautifulSoup), data normalization, bulk imports |
| **DevOps** | Docker, Gunicorn, Cloud Run, environment configuration |
| **Cloud Infrastructure** | Google Cloud Platform, Cloudflare, serverless architecture |
| **Frontend** | Responsive design, PWA, accessibility (RTL support) |
| **Internationalization** | Arabic text normalization, diacritics handling, bidirectional text |
| **Web Scraping** | Ethical scraping, rate limiting, data attribution |

---

## 🤝 Contributing

Contributions are welcome! 

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Classical Arabic dictionaries from public domain sources
- Grammar books from Islamic heritage libraries
- Poetry from AlDiwan.net (scraped ethically with attribution)

---

<div align="center">

### 🌐 [qamoos.org](https://qamoos.org) - Making Arabic heritage accessible to everyone

<br/>

**Built with ❤️ for the Arabic language community**

[![GitHub](https://img.shields.io/badge/GitHub-mh2des-181717?style=flat&logo=github)](https://github.com/mh2des)

</div>
