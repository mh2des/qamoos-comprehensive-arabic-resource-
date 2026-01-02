<div align="center">

# 📚 Qamoos.org

### المرجع العربي الشامل | Comprehensive Arabic Reference

[![Live](https://img.shields.io/badge/Live-qamoos.org-green?style=for-the-badge)](https://qamoos.org)
[![API](https://img.shields.io/badge/API-REST-blue?style=for-the-badge)](https://qamoos.org/api)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

**9 Classical Dictionaries • 48 Grammar Books • Poetry Library**

[Live Demo](https://qamoos.org) · [API Docs](docs_important/FLUTTER_API_QUICK_REFERENCE.md) · [Tech Stack](TECH_STACK_AND_FEATURES.md)

</div>

---

## 🌟 Overview

**Qamoos.org** is a comprehensive Arabic language platform featuring classical dictionaries, grammar books, and poetry. Built with Python Flask backend and vanilla JavaScript frontend, deployed on Google Cloud Run and Cloudflare Pages.

### Key Features

- 🔍 **Multi-Dictionary Search** - 189,042 entries across 9 classical dictionaries
- 📖 **Grammar Library** - 48 complete books with 3,384 chapters
- 🎭 **Poetry Collection** - Growing library of Arabic poems
- ⚡ **Fast API** - REST API with <200ms response time
- 📱 **Mobile-Ready** - PWA with offline support

---

## 📊 Content Statistics

| Resource | Count | Details |
|----------|-------|---------|
| Dictionaries | 9 | القاموس المحيط، المعجم الوسيط، كتاب العين، الصحاح، المحيط، المعاصر، الفقهي، التعريفات، المورد |
| Entries | 189,042 | 177,075 main + 11,967 sub-entries |
| Grammar Books | 48 | نحو، إعراب، صرف، بلاغة |
| Chapters | 3,384 | Interactive reader with progress tracking |
| Poems | 1,099+ | 44 poets, 36,423 verses |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Backend** | Python 3.12, Flask, PostgreSQL |
| **Hosting** | Cloudflare Pages (frontend), Google Cloud Run (API) |
| **Database** | PostgreSQL (Cloud SQL) |

> 📄 See [TECH_STACK_AND_FEATURES.md](TECH_STACK_AND_FEATURES.md) for complete details.

---

## 📁 Project Structure

```
qamoos/
├── backend_production/     # Flask API server
│   ├── server_postgresql.py
│   ├── Dockerfile
│   └── requirements_postgresql.txt
├── frontend-deploy/        # Static website
│   ├── index.html
│   ├── search.html
│   ├── grammar/           # 48 grammar books
│   └── _worker.js         # Cloudflare API proxy
├── docs_important/         # API documentation
└── .github/               # GitHub configuration
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Node.js (for Cloudflare deployment)

### Local Development

```bash
# 1. Clone repository
git clone https://github.com/YOUR_USERNAME/qamoos.git
cd qamoos

# 2. Setup environment
cp .env.example .env
# Edit .env with your database credentials

# 3. Install dependencies
cd backend_production
pip install -r requirements_postgresql.txt

# 4. Run server
python server_postgresql.py
# Server runs at http://localhost:5000
```

### Deployment

```bash
# Backend (Google Cloud Run)
cd backend_production
gcloud run deploy qamoos-api --source .

# Frontend (Cloudflare Pages)
cd frontend-deploy
npx wrangler pages deploy . --project-name qamoos-org
```

---

## 🔌 API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/dictionaries` | List all 9 dictionaries |
| `GET /api/search?q=كتاب` | Search entries |
| `GET /api/entry/{id}` | Get entry details |
| `GET /api/stats` | Database statistics |
| `GET /api/poets` | List poets |
| `GET /api/poem/{id}` | Get poem with verses |

> 📄 See [API Quick Reference](docs_important/FLUTTER_API_QUICK_REFERENCE.md) for full documentation.

---

## 📱 Screenshots

<div align="center">
<img src="https://qamoos.org/icon-512.png" alt="Qamoos Logo" width="128">
</div>

| Homepage | Search | Grammar |
|----------|--------|---------|
| Dictionary stats & search | Multi-mode search | 48 books reader |

---

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting PRs.

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

**[qamoos.org](https://qamoos.org)** - Making Arabic heritage accessible to everyone

</div>
