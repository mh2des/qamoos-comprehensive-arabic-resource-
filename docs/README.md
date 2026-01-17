# القاموس المحيط Dictionary Extraction System

Professional extraction system for converting the HTML dictionary into a structured SQLite database for Flutter mobile application integration.

## 📋 Project Overview

**Dictionary:** القاموس المحيط (Al-Qamus Al-Muhit)  
**Author:** الفيروزآبادي (Al-Firuzabadi)  
**Edition:** 8th Edition, 2005  
**Source:** HTML file (1,392 lines, ~1,357 pages)  
**Target:** SQLite database for Flutter mobile app

## 🏗️ Architecture

### Phase 1: Data Extraction (Current)
- **HTML Parser:** BeautifulSoup-based parser for structured extraction
- **Text Normalizer:** Arabic diacritic removal for search optimization
- **Database Manager:** SQLite schema creation and data insertion
- **Entry Parser:** Intelligent parsing of dictionary entries

### Components

1. **`extract_dictionary.py`** - Main extraction script
2. **`validate_database.py`** - Database validation and quality checks
3. **`requirements.txt`** - Python dependencies

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run extraction:**
```bash
python extract_dictionary.py
```

3. **Validate results:**
```bash
python validate_database.py
```

## 📊 Database Schema

### Core Tables

- **chapters** - باب level (e.g., باب الهمزة)
- **sections** - فصل level (e.g., فصل الباء)
- **entries** - Individual dictionary entries with full metadata
- **definitions** - Multiple definitions per entry
- **grammatical_forms** - Verb conjugations and patterns
- **plurals** - Plural forms (ج:)
- **markers** - Place markers (ع، د، ة، م)
- **cross_references** - Inter-entry references
- **notes** - Editorial notes and corrections
- **entries_fts** - Full-text search index (FTS5)

### Key Features

- ✅ **Hierarchical organization** preserved (باب → فصل → entries)
- ✅ **Dual text storage** (original with diacritics + normalized)
- ✅ **Full-text search** enabled via FTS5
- ✅ **Page references** maintained
- ✅ **Foreign key constraints** for data integrity
- ✅ **Optimized indexes** for fast queries

## 📝 Entry Structure

Each dictionary entry contains:

- **Headword** (with diacritics)
- **Normalized headword** (no diacritics for search)
- **Root letters** (trilateral/quadrilateral)
- **Grammatical pattern** (e.g., كَرَضِيَ، كَدَعَا)
- **Multiple definitions**
- **Plural forms** marked with ج:
- **Place markers** (ع، د، ة، م)
- **Cross-references** to related entries
- **Page number** from original source
- **Full text** preserved

## 🔍 Search Capabilities

The database supports:

1. **Exact search** - Match with diacritics
2. **Fuzzy search** - Match without diacritics
3. **Root-based search** - Find all derivatives
4. **Full-text search** - Search within definitions
5. **Autocomplete** - Prefix-based suggestions

## 📈 Expected Output

After successful extraction:

- **Database file:** `qamoos_database.sqlite`
- **Log file:** `extraction.log`
- **Statistics:**
  - ~1,392 pages processed
  - Multiple chapters (باب)
  - Hundreds of sections (فصل)
  - Thousands of entries
  - Complete metadata

## 🧪 Validation Tests

The validation script checks:

- ✓ Schema completeness (all tables exist)
- ✓ Data counts (entries, chapters, sections)
- ✓ Page coverage (all pages processed)
- ✓ Hierarchy integrity (no orphaned records)
- ✓ Text normalization (diacritics properly removed)
- ✓ FTS index (search capability)
- ✓ Sample searches (functionality tests)

## 📂 File Structure

```
arabic_qamoos/
├── data/
│   └── القاموس المحيط.htm          # Source HTML file
├── extract_dictionary.py            # Main extraction script
├── validate_database.py             # Validation script
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
├── extraction.log                   # Execution log (generated)
└── qamoos_database.sqlite          # Output database (generated)
```

## 🔧 Configuration

Edit the following in `extract_dictionary.py` if needed:

```python
HTML_FILE = r"c:\python apps\arabic_qamoos\data\القاموس المحيط.htm"
DB_FILE = r"c:\python apps\arabic_qamoos\qamoos_database.sqlite"
```

## 📊 Sample Statistics

Expected extraction results:

- **Total Pages:** ~1,392
- **Total Chapters:** ~29 (based on Arabic letters)
- **Total Sections:** Hundreds (فصل subdivisions)
- **Total Entries:** Thousands
- **Total Definitions:** Tens of thousands
- **Total Plurals:** Thousands

## 🐛 Troubleshooting

### Issue: Import errors
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

### Issue: File not found
```bash
# Solution: Check HTML file path
# Verify the file exists at the specified location
```

### Issue: Database locked
```bash
# Solution: Close any open connections
# Delete the .sqlite file and re-run extraction
```

## 🚦 Next Steps (Phases 2-6)

- [ ] **Phase 2:** Enhanced entry parsing (cross-references, notes)
- [ ] **Phase 3:** Search algorithm optimization
- [ ] **Phase 4:** Flutter app integration
- [ ] **Phase 5:** UI/UX implementation
- [ ] **Phase 6:** Testing and deployment

## 📞 Support

For issues or questions:
1. Check the `extraction.log` file for errors
2. Run validation script for diagnostics
3. Review this README for configuration

## 📜 License

This extraction system is created for the القاموس المحيط dictionary project.

## 🎯 Quality Standards

- **Code Quality:** Professional, documented, modular
- **Data Integrity:** Foreign keys, constraints, validation
- **Performance:** Indexed searches, optimized queries
- **Completeness:** All data preserved from source
- **Maintainability:** Clear structure, logging, error handling

---

**Status:** Phase 1 Implementation Complete ✓  
**Next:** Run extraction and validate results
