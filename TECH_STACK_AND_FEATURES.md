# 🛠️ Complete Tech Stack & Features - Qamoos.org

**Last Updated**: January 2, 2026

---

## 📋 TABLE OF CONTENTS

1. [Frontend Technologies](#frontend-technologies)
2. [Backend Technologies](#backend-technologies)
3. [Database & Storage](#database--storage)
4. [Infrastructure & Hosting](#infrastructure--hosting)
5. [Development Tools](#development-tools)
6. [Libraries & Dependencies](#libraries--dependencies)
7. [Complete Feature List](#complete-feature-list)
8. [Performance Tools](#performance-tools)
9. [SEO & Analytics](#seo--analytics)
10. [APIs & Integrations](#apis--integrations)

---

## 🎨 FRONTEND TECHNOLOGIES

### Core Languages
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with Grid & Flexbox
- **JavaScript (ES6+)** - Vanilla JS, no frameworks

### Fonts
- **Google Fonts**
  - Amiri (400, 700) - Traditional Arabic serif
  - Cairo (300, 400, 600, 700, 900) - Modern Arabic sans-serif
- **Traditional Naskh** - Grammar books (from Shamela library)

### Icon Libraries
- **Font Awesome 6.5.1** - Professional icons
  - CDN: `https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css`

### Animation Libraries
- **AOS (Animate On Scroll) 2.3.1**
  - CDN: `https://unpkg.com/aos@2.3.1/dist/aos.css`
  - Smooth scroll animations

### PWA Technologies
- **Service Worker** - Offline support
- **Web App Manifest** - Add to home screen
- **Cache API** - Static resource caching

---

## ⚙️ BACKEND TECHNOLOGIES

### Core Framework
- **Python 3.12** - Runtime environment
- **Flask** - Lightweight web framework
- **Flask-CORS** - Cross-Origin Resource Sharing

### Database Driver
- **psycopg2** - PostgreSQL adapter for Python
- **psycopg2.extras.RealDictCursor** - Dictionary-based results

### Python Libraries
```
beautifulsoup4==4.12.2    # HTML parsing
flask==3.0.0               # Web framework
flask-cors==4.0.0          # CORS support
psycopg2-binary==2.9.9     # PostgreSQL driver
python-dotenv==1.0.0       # Environment variables
gunicorn==21.2.0           # Production WSGI server
```

### Environment Management
- **python-dotenv** - Load `.env` files
- **virtualenv** - Python virtual environments

---

## 🗄️ DATABASE & STORAGE

### Primary Database
- **PostgreSQL 14+** - Production database
  - Full-text search (FTS)
  - JSON support
  - Advanced indexing

### Database Schema
- **9 Tables (Dictionary)**:
  - `dictionaries`
  - `chapters`
  - `sections`
  - `entries`
  - `sub_entries`
  - `definitions`
  - `plurals`
  - `grammatical_forms`
  - `cross_references`

- **8 Tables (Poetry)**:
  - `poetry_eras`
  - `poetry_countries`
  - `poetry_topics`
  - `poetry_meters`
  - `poets`
  - `poems`
  - `verses`
  - `poetry_favorites`

### Local Development
- **SQLite 3** - Development database
- **DB Browser for SQLite** - Database inspection

---

## ☁️ INFRASTRUCTURE & HOSTING

### Frontend Hosting
- **Cloudflare Pages**
  - Global CDN
  - Automatic HTTPS
  - 5-minute cache
  - Edge computing

### Backend Hosting
- **Google Cloud Run**
  - Container-based deployment
  - Auto-scaling (0-100 instances)
  - Pay-per-use pricing
  - Region: us-east1

### Database Hosting
- **Google Cloud SQL**
  - Managed PostgreSQL
  - Automatic backups
  - High availability

### DNS & CDN
- **Cloudflare DNS**
  - Global DNS resolution
  - DDoS protection
  - SSL/TLS certificates

### Edge Computing
- **Cloudflare Workers**
  - API proxy (`_worker.js`)
  - Request routing
  - Header manipulation

---

## 🛠️ DEVELOPMENT TOOLS

### Version Control
- **Git** - Source control
- **GitHub** - Repository hosting

### Code Editors
- **VS Code** - Primary IDE
  - Python extension
  - Prettier (formatting)
  - ESLint (linting)

### Command Line Tools
- **gcloud CLI** - Google Cloud deployment
- **wrangler CLI** - Cloudflare Pages deployment
- **curl** - API testing
- **bash** - Shell scripting

### Containerization
- **Docker** - Container images
- **Dockerfile** - Container configuration
- **Docker Desktop** - Local container management

### Deployment Scripts
```bash
deploy.sh              # Main deployment script
deploy_manual.sh       # Manual Docker build
deploy_cloudbuild.sh   # Cloud Build deployment
```

---

## 📚 LIBRARIES & DEPENDENCIES

### Frontend Libraries (CDN)
```html
<!-- Fonts -->
fonts.googleapis.com
fonts.gstatic.com

<!-- Icons -->
cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/

<!-- Animation -->
unpkg.com/aos@2.3.1/dist/aos.css

<!-- Analytics -->
www.googletagmanager.com/gtag/js?id=G-ZMTXZ4F8QF
```

### Backend Dependencies (requirements_postgresql.txt)
```
beautifulsoup4==4.12.2
flask==3.0.0
flask-cors==4.0.0
psycopg2-binary==2.9.9
python-dotenv==1.0.0
gunicorn==21.2.0
lxml==4.9.3
requests==2.31.0
```

### Development Dependencies
```
pip==23.3.1
setuptools==69.0.2
wheel==0.42.0
```

---

## 🎯 COMPLETE FEATURE LIST

### 1. MULTI-DICTIONARY SEARCH
- **9 Classical Dictionaries**: 189,042 entries
  - القاموس المحيط (10,363 entries)
  - المعجم الوسيط (35,457 entries)
  - كتاب العين (24,952 + 11,967 sub-entries)
  - الصحاح تاج اللغة (44,479 entries)
  - المحيط في اللغة (30,767 entries)
  - معجم اللغة العربية المعاصرة (17,817 entries)
  - القاموس الفقهي (3,223 entries)
  - التعريفات (1,772 entries)
  - المورد العربي الإنجليزي (7,278 entries)

- **5 Search Modes**:
  - Exact match (with diacritics)
  - Starts with (prefix search)
  - Contains (substring)
  - Root-based (trilateral roots)
  - Full-text (definitions & content)

- **Smart Features**:
  - Real-time autocomplete
  - Arabic diacritic normalization
  - Two-tier search architecture
  - Smart ranking algorithm
  - Dictionary filtering
  - Cross-reference linking

### 2. GRAMMAR LIBRARY
- **48 Books**: 3,384 chapters
  - بلاغة (Rhetoric): 20 books
  - نحو (Grammar): 12 books
  - إعراب (Syntax): 13 books
  - صرف (Morphology): 3 books

- **Interactive Reader**:
  - Collapsible table of contents
  - Progress tracking (LocalStorage)
  - Font size controls
  - Dark mode toggle
  - Bookmark system
  - Chapter navigation
  - Original formatting preserved

- **3-Tier JSON Loading**:
  - Level 1: Summary (20KB)
  - Level 2: Category files (4 files)
  - Level 3: Book details (48 files)
  - 97% size reduction (1.5MB → 20KB initial)

### 3. POETRY LIBRARY
- **Current**: 44 poets, 1,099 poems, 36,423 verses
- **Target**: 1,831 poets, 142,805 poems

- **Organization**:
  - 9 historical eras
  - 21 countries
  - 17 topics/themes
  - 16 classical meters (بحور)

- **Features**:
  - Browse poets by era/country
  - Search poems by keyword
  - View full verses (شطر أول/ثاني)
  - Poet biographies
  - Integration with dictionary

### 4. REST API
- **12 Endpoints**:
  - `GET /health` - Health check
  - `GET /api/dictionaries` - List dictionaries
  - `GET /api/stats` - Statistics
  - `GET /api/search` - Search entries
  - `GET /api/entry/<id>` - Entry details
  - `GET /api/chapters` - Chapter list
  - `GET /api/random` - Random entries
  - `GET /api/poets` - List poets
  - `GET /api/poet/<id>` - Poet details
  - `GET /api/poems` - List poems
  - `GET /api/poem/<id>` - Poem details
  - `GET /api/poetry/search` - Poetry search

- **API Features**:
  - JSON responses
  - CORS enabled
  - Pagination support
  - Error handling
  - Response time: <200ms

### 5. USER INTERFACE
- **Pages**:
  - Homepage (index.html)
  - Search interface (search.html)
  - Poetry page (poetry.html)
  - Grammar library (grammar/index.html)
  - Book reader (grammar/book.html)
  - About page (about.html)
  - Contact page (contact.html)
  - Sources (sources.html)
  - Methodology (methodology.html)
  - Terms of use (terms.html)
  - Privacy policy (privacy.html)

- **Design Features**:
  - RTL (Right-to-Left) layout
  - Responsive design (mobile-first)
  - Touch-friendly buttons
  - Smooth animations
  - Color-coded categories
  - Expandable cards
  - Sticky navigation

### 6. PERFORMANCE OPTIMIZATIONS
- **Loading**:
  - Lazy loading for books
  - Dynamic chapter loading
  - Image optimization
  - Minified assets

- **Caching**:
  - CDN caching (5 minutes)
  - Browser caching
  - Service worker caching
  - LocalStorage for progress

- **Response Times**:
  - Database queries: <100ms
  - API responses: <200ms
  - Page load: <2 seconds

### 7. PWA FEATURES
- **Offline Support**:
  - Service worker registration
  - Cache-first strategy
  - Offline fallback page

- **Install Prompts**:
  - Add to home screen
  - App-like experience
  - Fullscreen mode

- **Manifest**:
  - App name & icons
  - Theme colors
  - Display mode
  - Start URL

### 8. SEO OPTIMIZATIONS
- **Meta Tags**:
  - Title & description (Arabic/English)
  - Keywords (قاموس عربي, معاني الكلمات, etc.)
  - Author & robots
  - Canonical URLs

- **Open Graph**:
  - og:type, og:url, og:title
  - og:description, og:image
  - Facebook preview

- **Twitter Cards**:
  - twitter:card (summary_large_image)
  - twitter:title, twitter:description
  - twitter:image

- **Schema.org**:
  - WebSite schema
  - WebApplication schema
  - SearchAction schema
  - CollectionPage schema

- **Sitemaps**:
  - sitemap.xml (main)
  - Dynamic sitemaps (planned)

- **Search Console**:
  - Google Search Console
  - Bing Webmaster Tools
  - BingSiteAuth.xml

### 9. MOBILE FEATURES
- **Responsive Design**:
  - Mobile-first approach
  - Viewport optimization
  - Touch gestures

- **Arabic Support**:
  - RTL layout
  - Arabic fonts
  - Proper text rendering

- **Performance**:
  - Fast loading on 3G
  - Optimized images
  - Minimal JavaScript

### 10. ACCESSIBILITY
- **ARIA Labels**:
  - Screen reader support
  - Semantic HTML
  - Proper headings

- **Keyboard Navigation**:
  - Tab navigation
  - Enter/Space actions
  - Escape to close

- **Visual**:
  - High contrast colors
  - Readable font sizes
  - Focus indicators

---

## 📊 PERFORMANCE TOOLS

### Monitoring
- **Google Analytics 4** (GA4)
  - ID: G-ZMTXZ4F8QF
  - Event tracking
  - User behavior analytics
  - Real-time monitoring

### Performance Testing
- **Lighthouse** (Chrome DevTools)
  - Performance score
  - Accessibility audit
  - Best practices
  - SEO audit

### Load Testing
- **curl** - API endpoint testing
- **Browser DevTools** - Network analysis

---

## 🔍 SEO & ANALYTICS

### Analytics Platforms
- **Google Analytics 4**
  - gtag.js tracking
  - Custom events
  - User demographics
  - Traffic sources

### Search Console
- **Google Search Console**
  - Site verification (pending)
  - Sitemap submission
  - Indexing status
  - Search performance

- **Bing Webmaster Tools**
  - BingSiteAuth.xml verification
  - URL inspection
  - SEO reports

### SEO Tools
- **robots.txt** - Crawler directives
- **sitemap.xml** - Site structure
- **Canonical tags** - Duplicate prevention
- **Hreflang tags** - Multi-language support

---

## 🔌 APIS & INTEGRATIONS

### External APIs
None currently - fully self-hosted

### Internal API
- **Base URL**: `https://qamoos-api-804325795495.us-east1.run.app`
- **Protocol**: REST
- **Format**: JSON
- **Authentication**: None (public API)

### Third-Party CDNs
- Google Fonts
- Font Awesome (Cloudflare CDN)
- AOS Animation Library (unpkg)
- Google Analytics

---

## 🎨 DESIGN SYSTEM

### Color Palette
```css
--primary: #1B4332        /* Forest Green */
--primary-light: #2D6A4F  /* Light Green */
--secondary: #D4AF37      /* Gold */
--bg: #F8F5F0            /* Cream */
--card-bg: #FFFFFF       /* White */
--text: #1B4332          /* Dark Green */
--text-muted: #52796F    /* Muted Green */
--border: #D8E2DC        /* Light Gray */
```

### Typography Scale
```css
--font-arabic: 'Amiri', serif
--font-ui: 'Cairo', sans-serif

Font Sizes:
- Headwords: 24-32pt, Bold
- Definitions: 16pt, Regular
- Metadata: 12pt, Medium
- UI text: 14-16pt
```

### Spacing System
```css
--spacing-xs: 0.25rem   /* 4px */
--spacing-sm: 0.5rem    /* 8px */
--spacing-md: 1rem      /* 16px */
--spacing-lg: 2rem      /* 32px */
--spacing-xl: 4rem      /* 64px */
```

---

## 📦 BUILD & DEPLOYMENT

### Frontend Build
```bash
# No build step - pure HTML/CSS/JS
# Deploy directly to Cloudflare Pages
cd frontend-deploy
npx wrangler pages deploy . --project-name qamoos-org
```

### Backend Build
```bash
# Docker build
docker build -t qamoos-api .

# Deploy to Cloud Run
gcloud run deploy qamoos-api --source .
```

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host:5432/qamoos_db
PORT=8080
FLASK_ENV=production

# Cloudflare Worker
BACKEND_URL=https://qamoos-api-804325795495.us-east1.run.app
```

---

## 📈 DATA & STATISTICS

### Content Volumes
- **Dictionary entries**: 189,042
- **Definitions**: 100,000+
- **Grammar chapters**: 3,384
- **Poetry verses**: 36,423 (1,099 poems)
- **Database size**: ~150MB

### File Statistics
- **HTML files**: 50+ pages
- **Python scripts**: 20+ files
- **JSON files**: 53 (grammar data)
- **Documentation**: 60+ MD files

---

## 🔧 CONFIGURATION FILES

### Frontend
- `manifest.json` - PWA configuration
- `robots.txt` - SEO directives
- `sitemap.xml` - Site structure
- `_worker.js` - Cloudflare Worker
- `_routes.json` - Routing rules
- `_headers` - HTTP headers
- `BingSiteAuth.xml` - Bing verification

### Backend
- `Dockerfile` - Container config
- `Procfile` - Process management
- `runtime.txt` - Python version
- `requirements_postgresql.txt` - Dependencies
- `.dockerignore` - Build exclusions
- `.gcloudignore` - Deploy exclusions

### Development
- `.env` - Environment variables
- `.env.example` - Template
- `.gitignore` - Git exclusions

---

## 🚀 DEPLOYMENT WORKFLOW

### Frontend Pipeline
1. Edit files in `frontend-deploy/`
2. Test locally (open in browser)
3. Deploy: `npx wrangler pages deploy .`
4. Cloudflare builds and serves globally
5. Updates live in ~2 minutes

### Backend Pipeline
1. Edit `backend_production/server_postgresql.py`
2. Test locally: `python server_postgresql.py`
3. Deploy: `bash deploy_manual.sh`
4. Docker builds image
5. Google Cloud Run serves containerized app
6. Updates live in ~5-7 minutes

### Database Updates
1. Edit extraction scripts
2. Run: `python extract_dictionary_v2.py`
3. Data imports to PostgreSQL
4. API serves updated data automatically

---

## 📝 EXTRACTION TOOLS

### HTML Parsing
- **BeautifulSoup4** - HTML/XML parsing
- **lxml** - Fast XML parser
- **requests** - HTTP library

### Extraction Scripts
- `extract_dictionary_v2.py` - Main extraction (Dict 1,2,4-9)
- `scripts/extract_ayn_fixed.py` - Dict 3 (كتاب العين)
- `scripts/process_grammar_books.py` - Grammar extraction
- `scripts/optimize_books_json.py` - JSON optimization
- `production_scraper.py` - Poetry scraping (AlDiwan.net)

### Text Processing
- **normalize_arabic()** - Diacritic removal
- **Regex patterns** - Content extraction
- **String manipulation** - Cleaning & formatting

---

## 🎯 FEATURE COMPLETENESS

| Feature | Status | Progress |
|---------|--------|----------|
| Dictionary Search | ✅ Complete | 100% |
| Grammar Library | ✅ Complete | 100% |
| Poetry Database | 🔄 In Progress | 7% (44/1,831 poets) |
| REST API | ✅ Complete | 100% |
| Frontend UI | ✅ Complete | 100% |
| SEO Optimization | ⚠️ Partial | 40% |
| Mobile App | 📋 Planned | 0% |
| User Accounts | 📋 Planned | 0% |

---

## 🌐 LIVE URLS

- **Main Site**: https://qamoos.org
- **API**: https://qamoos-api-804325795495.us-east1.run.app
- **Grammar**: https://qamoos.org/grammar/
- **Search**: https://qamoos.org/search
- **Poetry**: https://qamoos.org/poetry

---

## 📞 TECH SUPPORT RESOURCES

### Documentation
- Flask: https://flask.palletsprojects.com/
- PostgreSQL: https://www.postgresql.org/docs/
- Cloudflare Pages: https://developers.cloudflare.com/pages/
- Google Cloud Run: https://cloud.google.com/run/docs

### Community
- Stack Overflow (Flask, PostgreSQL)
- GitHub Issues
- Python Discord

---

**Document Version**: 1.0  
**Last Updated**: January 2, 2026  
**Total Technologies Listed**: 70+
