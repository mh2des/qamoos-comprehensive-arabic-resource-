# Frontend Production - Qamoos.org

## 📦 Contents

This directory contains the **complete production frontend** deployed on **Cloudflare Pages**.

### Main Pages
- **`index.html`** - Homepage with search and statistics
- **`search.html`** - Advanced search interface
- **`about.html`** - About page
- **`contact.html`** - Contact page
- **`sources.html`** - المصادر والمراجع
- **`methodology.html`** - منهجية القاموس
- **`terms.html`** - شروط الاستخدام
- **`privacy.html`** - سياسة الخصوصية

### Grammar Library
- **`grammar/`** - Complete grammar books system
  - `grammar/index.html` - Book listing (48 books)
  - `grammar/book.html` - Book reader interface
  - `grammar/data/` - JSON book data (books-summary.json, book-details/)

### Configuration Files
- **`_worker.js`** - Cloudflare Worker (proxies /api/* to backend)
- **`_routes.json`** - Cloudflare Pages routing
- **`_headers`** - Custom HTTP headers
- **`manifest.json`** - PWA manifest
- **`service-worker.js`** - Service worker for offline support
- **`robots.txt`** - SEO configuration
- **`sitemap.xml`** - Sitemap for search engines
- **`BingSiteAuth.xml`** - Bing verification

### Assets
- **`icon-512.png`** - App icon

### Functions
- **`functions/grammar/data/[[path]].js`** - Cloudflare Pages Function for grammar data

---

## 🚀 Deployment

### Cloudflare Pages (Current Production)

**Live URL**: https://qamoos.org

**Deploy command**:
```bash
cd frontend-deploy
npx wrangler pages deploy . --project-name qamoos-org --branch production
```

**Automatic deployment**:
- Push to `production` branch → auto-deploys to qamoos.org
- Push to `main` branch → auto-deploys to staging

### Environment Variables (Cloudflare)
- `BACKEND_URL` - Backend API URL (set in Cloudflare dashboard)

---

## 🏗️ Architecture

```
User → qamoos.org (Cloudflare Pages)
         ↓
     _worker.js (proxies /api/*)
         ↓
   Google Cloud Run (Backend API)
         ↓
   PostgreSQL Database
```

### Key Features
- **Static site hosting** - Fast global CDN
- **API proxy** - Worker proxies backend requests
- **PWA** - Offline support with service worker
- **Grammar library** - 48 books with 3-tier JSON loading
- **Mobile-first** - Responsive design for all devices

---

## 📂 Directory Structure

```
frontend-deploy/
├── index.html              # Homepage
├── search.html             # Search page
├── about.html              # About page
├── contact.html            # Contact
├── sources.html            # المصادر
├── methodology.html        # المنهجية
├── terms.html              # الشروط
├── privacy.html            # الخصوصية
├── _worker.js              # Cloudflare Worker
├── _routes.json            # Routing config
├── _headers                # HTTP headers
├── manifest.json           # PWA manifest
├── service-worker.js       # Service worker
├── robots.txt              # SEO
├── sitemap.xml             # Sitemap
├── icon-512.png            # App icon
├── grammar/                # Grammar library
│   ├── index.html          # Book listing
│   ├── book.html           # Book reader
│   └── data/               # Book JSON files
│       ├── books-summary.json (20KB)
│       ├── books-بلاغة.json
│       ├── books-صرف.json
│       ├── books-إعراب.json
│       ├── books-نحو.json
│       └── book-details/   # Individual book files
└── functions/              # Cloudflare Pages Functions
    └── grammar/data/[[path]].js
```

---

## 🎨 Features

### Dictionary Search
- 9 classical Arabic dictionaries
- 189,042 total entries
- Advanced search modes (exact, starts, contains, all)
- Fast autocomplete suggestions
- Mobile-responsive interface

### Grammar Library
- 48 books across 4 categories
  - بلاغة (Rhetoric): 20 books
  - صرف (Morphology): 4 books
  - إعراب (Syntax Analysis): 12 books
  - نحو (Grammar): 12 books
- 3-tier JSON loading (97% size reduction)
- Chapter-based navigation
- Mobile-friendly reader

### Performance Optimizations
- **JSON optimization**: 1.5MB → 20KB initial load
- **CDN caching**: 5-minute cache on API responses
- **Lazy loading**: Grammar books load on demand
- **Service worker**: Offline support for static pages

---

## 🔧 Maintenance

### Update Content
1. Edit HTML files in this directory
2. Deploy: `npx wrangler pages deploy . --project-name qamoos-org --branch production`

### Update Grammar Books
1. Run processing script: `python ../backend_production/scripts/process_grammar_books.py`
2. Copy generated JSON files to `grammar/data/`
3. Deploy

### Update Worker
1. Edit `_worker.js`
2. Deploy (Worker updates automatically with Pages deployment)

---

## 📱 Mobile Support

All pages fully responsive with:
- Touch-friendly navigation (55px×55px touch targets)
- Hamburger menu for mobile
- Fixed navbar with golden highlight
- Optimized search interface
- Readable Arabic fonts

---

## 🌐 SEO

- **Google Search Console**: Submitted and indexed
- **Bing Webmaster**: Verified with BingSiteAuth.xml
- **Sitemap**: Auto-generated, includes all pages
- **Meta tags**: Optimized for Arabic search
- **Structured data**: Coming soon

---

## 📝 Notes

- **No build process** - Pure HTML/CSS/JS
- **No backend needed** - API calls proxied through Worker
- **Fast deployments** - < 30 seconds to global CDN
- **Free tier** - Cloudflare Pages free plan
- **Analytics**: Google Analytics 4 integrated
