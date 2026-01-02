# Arabic Qamoos Dictionary Project - AI Coding Guidelines

## Project Overview
A multi-dictionary Arabic reference system with 3 classic Arabic dictionaries extracted from HTML to SQLite database, with a Flask REST API and browser-based demo interface. The project supports searching across **القاموس المحيط** (Al-Qamus Al-Muhit), **المعجم الوسيط** (Al-Mu'jam Al-Wasit), and **كتاب العين** (Kitab Al-Ayn).

## Database Architecture

### Multi-Dictionary Design
- **1 SQLite database** (`qamoos_database.sqlite`) stores all 3 dictionaries
- **dictionaries table** tracks metadata for each dictionary
- **Hierarchical structure**: dictionaries → chapters → sections → entries → definitions
- **Current stats**: 70,772 total entries across 3 dictionaries
  - Dict 1 (القاموس المحيط): 10,363 entries
  - Dict 2 (المعجم الوسيط): 35,457 entries
  - Dict 3 (كتاب العين): 24,952 entries

### Key Tables & Relationships
```
dictionaries (id, name_arabic, name_english, author, year)
  └─ chapters (chapter_id, dictionary_id, name_arabic, order)
      └─ sections (section_id, chapter_id, name_arabic)
          └─ entries (entry_id, section_id, dictionary_id, headword, headword_normalized, root, full_text, page_number)
              └─ definitions (definition_id, entry_id, definition_text, order)
```

- **Foreign keys** enforce referential integrity
- **headword_normalized**: Arabic text with diacritics removed for fuzzy search
- **dictionary_id** on entries table allows filtering by specific dictionary

## Extraction Workflows

### Critical HTML Parsing Pattern
All 3 dictionaries are HTML-based with **different structures**:

1. **القاموس المحيط & المعجم الوسيط**: Extract from `<div class='Entry'>` elements
2. **كتاب العين**: Complex extraction requiring special handling of `</p>` tags

### العين Dictionary Extraction (CRITICAL)
Located in `scripts/extract_ayn_fixed.py` - uses a unique approach:

```python
# CRITICAL FIX: Replace </p> with ". </p>" in raw HTML BEFORE parsing
html_content = html_content.replace('</p>', '. </p>')
```

**Why this matters:**
- Some entries in العين HTML have NO period between entries
- Example: `قد ناهزا للفِطامِ أو فُطِما</p>نزه: مكانُ نَزِهٌ`
- Without the fix, "نزه" concatenates with previous text and becomes unsearchable
- This fix added ~3,300 entries that were previously missed (21,648 → 24,952)

### Re-extraction Commands
```bash
# Clear and re-extract specific dictionary
python extract_dictionary_v2.py     # Dict 1 & 2
python scripts/extract_ayn_fixed.py # Dict 3 (العين) - uses the </p> fix
```

## API Server Pattern

### Server: `simple_server.py`
- **Flask-based** REST API on port 5000
- **CORS enabled** for browser/Flutter access
- **No authentication** - designed for local/demo use

### Key Endpoints
```python
GET /api/dictionaries              # List all 3 dictionaries
GET /api/stats?dictionary_id=N     # Stats for specific dictionary
GET /api/search?q=TEXT&dictionary_id=N&mode=MODE&limit=N
GET /api/entry/<int:entry_id>      # Full entry details
GET /api/chapters?dictionary_id=N  # Chapter list for dictionary
```

### Search Modes
1. `exact`: Exact match with diacritics
2. `starts_with`: Prefix search (normalized)
3. `contains`: Substring search (normalized)
4. `all`: Searches headword_normalized, root, AND full_text

**Always use `headword_normalized` for fuzzy searching** - removes all Arabic diacritics for better UX.

## Testing & Debugging

### Server Testing Pattern
```bash
# Start server in background
cd "/c/python apps/arabic_qamoos" && python -B simple_server.py &

# Test with curl (URL-encoded Arabic)
curl "http://localhost:5000/api/search?q=%D9%86%D8%B2%D9%87&dictionary_id=3"

# Kill server when done
taskkill //F //IM python.exe  # Windows
pkill -9 python               # Linux/Mac
```

### Database Inspection Commands
```python
import sqlite3
conn = sqlite3.connect('qamoos_database.sqlite')
cursor = conn.cursor()

# Check entries by dictionary
cursor.execute('SELECT COUNT(*) FROM entries WHERE dictionary_id = 3')

# Search for specific word
cursor.execute('''
    SELECT headword, full_text 
    FROM entries 
    WHERE dictionary_id = 3 AND headword = 'نزه'
''')
```

## Common Pitfalls

### ❌ Don't create separate databases for each dictionary
- Use `dictionary_id` filtering in queries instead
- All data is in one `qamoos_database.sqlite` file

### ❌ Don't modify HTML files in `data/` directory
- These are source files - extraction scripts read them
- Changes should be in extraction logic, not source data

### ❌ Don't forget to clear old data before re-extraction
```python
cursor.execute('DELETE FROM entries WHERE dictionary_id = ?', (dictionary_id,))
```

### ❌ Don't use `python -c "..."` for complex database operations
- Create proper test scripts in `test_*.py` format
- Helps with debugging and reusability

### ✅ DO use URL encoding for Arabic in curl requests
```bash
# Use Python to encode
python -c "from urllib.parse import quote; print(quote('نزه'))"
# Output: %D9%86%D8%B2%D9%87
```

## File Organization

### Main Scripts
- `extract_dictionary_v2.py` - Extracts dictionaries 1 & 2
- `scripts/extract_ayn_fixed.py` - Extracts dictionary 3 with `</p>` fix
- `simple_server.py` - Flask API server
- `demo_dictionary_live.html` - Browser demo (connects to server)

### Test Scripts (All in root)
- `test_*.py` - Various test scripts
- Pattern: Create new `test_*.py` files, don't modify existing ones

### Data Files
- `data/القاموس المحيط.htm` - Dictionary 1 source
- `data/alwaseet1.htm`, `data/alwaseet2.htm` - Dictionary 2 source (2 files)
- `data/العين/001.htm` through `008.htm` - Dictionary 3 source (8 files)

## Key Conventions

1. **Arabic text normalization**: Always call `normalize_arabic()` when preparing search queries
2. **Dictionary filtering**: Use `WHERE dictionary_id = ?` in ALL entry queries
3. **Error handling**: Extraction scripts use try/except with continue to skip malformed entries
4. **Commit frequency**: Commit every 1000 entries during bulk inserts for performance
5. **FTS search**: Don't use for main search - only for full-text searches within definitions

## Next Steps for Development

When adding features:
1. **New search modes**: Add to `simple_server.py` `/api/search` endpoint
2. **New extraction logic**: Create `scripts/extract_*.py` file, don't modify `extract_dictionary_v2.py`
3. **UI changes**: Modify `demo_dictionary_live.html`, test locally before deploying
4. **Schema changes**: Requires re-extraction of ALL dictionaries

## Important Notes

- **Windows environment**: All paths use Windows format (`c:\python apps\arabic_qamoos`)
- **Shell**: Uses bash.exe (Git Bash or WSL)
- **Python version**: Python 3.x required (uses f-strings, type hints)
- **Dependencies**: BeautifulSoup4, Flask, Flask-CORS (see `requirements.txt`)
