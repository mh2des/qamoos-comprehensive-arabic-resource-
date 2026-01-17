"""
Simplified working server for القاموس المحيط
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import sqlite3
from urllib.parse import urlparse, parse_qs
import os

DATABASE_PATH = 'qamoos_database.sqlite'
# Get parent directory for HTML files
PARENT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def normalize_arabic(text):
    """Remove Arabic diacritics for normalized search - MUST MATCH extraction script"""
    if not text:
        return text
    
    diacritics = [
        '\u064B',  # Tanween Fath
        '\u064C',  # Tanween Damm
        '\u064D',  # Tanween Kasr
        '\u064E',  # Fatha
        '\u064F',  # Damma
        '\u0650',  # Kasra
        '\u0651',  # Shadda
        '\u0652',  # Sukun
        '\u0653',  # Maddah
        '\u0654',  # Hamza above
        '\u0655',  # Hamza below
        '\u0656',  # Subscript alef
        '\u0640',  # Tatweel
        '\u0670',  # Alef khanjariyah
        '\u06E4',  # Small high madda
    ]
    
    for diacritic in diacritics:
        text = text.replace(diacritic, '')
    
    return text.strip()

class DictionaryHandler(SimpleHTTPRequestHandler):
    
    def do_GET(self):
        try:
            self._do_GET_impl()
        except Exception as e:
            print(f"❌ ERROR in do_GET: {e}")
            import traceback
            traceback.print_exc()
            self.send_error(500, f"Internal Server Error: {e}")
    
    def _do_GET_impl(self):
        parsed = urlparse(self.path)
        print(f"📥 Request: {parsed.path}")  # Debug logging
        
        # Serve main page (new professional design)
        if parsed.path == '/' or parsed.path == '':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            self.end_headers()
            with open(os.path.join(PARENT_DIR, 'index_professional.html'), 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Serve search page
        if parsed.path == '/search' or parsed.path == '/search.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'search.html'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                # Redirect to main page if search.html doesn't exist
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            return
        
        # Serve about page
        if parsed.path == '/about' or parsed.path == '/about.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'about.html'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Page not found")
            return
        
        # Serve privacy page
        if parsed.path == '/privacy' or parsed.path == '/privacy.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'privacy.html'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Page not found")
            return
        
        # Serve methodology page
        if parsed.path == '/methodology' or parsed.path == '/methodology.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'methodology.html'), 'rb') as f:
                    self.wfile.write(f.read())
                return
            except Exception as e:
                print(f"❌ Error serving methodology.html: {e}")
                self.send_error(500, f"Error loading page: {e}")
                return
        
        # Serve sources page
        if parsed.path == '/sources' or parsed.path == '/sources.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'sources.html'), 'rb') as f:
                    self.wfile.write(f.read())
                return
            except Exception as e:
                print(f"❌ Error serving sources.html: {e}")
                self.send_error(500, f"Error loading page: {e}")
                return
        
        # Serve terms page
        if parsed.path == '/terms' or parsed.path == '/terms.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'terms.html'), 'rb') as f:
                    self.wfile.write(f.read())
                return
            except Exception as e:
                print(f"❌ Error serving terms.html: {e}")
                self.send_error(500, f"Error loading page: {e}")
                return
        
        # Serve contact page
        if parsed.path == '/contact' or parsed.path == '/contact.html':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'contact.html'), 'rb') as f:
                    self.wfile.write(f.read())
                return
            except Exception as e:
                print(f"❌ Error serving contact.html: {e}")
                self.send_error(500, f"Error loading page: {e}")
                return
        
        # Serve PWA manifest
        if parsed.path == '/manifest.json':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'manifest.json'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Manifest not found")
            return
        
        # Serve service worker
        if parsed.path == '/service-worker.js':
            try:
                self.send_response(200)
                self.send_header('Content-type', 'application/javascript')
                self.send_header('Service-Worker-Allowed', '/')
                self.end_headers()
                with open(os.path.join(PARENT_DIR, 'service-worker.js'), 'rb') as f:
                    self.wfile.write(f.read())
            except FileNotFoundError:
                self.send_error(404, "Service worker not found")
            return
        
        # Serve sitemap
        if parsed.path == '/sitemap.xml':
            self.send_response(200)
            self.send_header('Content-type', 'application/xml')
            self.end_headers()
            with open('sitemap.xml', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # Serve robots.txt
        if parsed.path == '/robots.txt':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            with open('robots.txt', 'rb') as f:
                self.wfile.write(f.read())
            return
        
        # API endpoints
        if parsed.path == '/api/dictionaries':
            self.handle_dictionaries()
        elif parsed.path == '/api/stats':
            self.handle_stats(parse_qs(parsed.query))
        elif parsed.path == '/api/chapters':
            self.handle_chapters(parse_qs(parsed.query))
        elif parsed.path.startswith('/api/search'):
            self.handle_search(parse_qs(parsed.query))
        elif parsed.path.startswith('/api/browse/'):
            chapter = parsed.path.split('/api/browse/')[1]
            self.handle_browse(chapter, parse_qs(parsed.query))
        else:
            self.send_error(404)
    
    def handle_dictionaries(self):
        """Get list of available dictionaries"""
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dictionary_id, name_arabic, name_english, description
            FROM dictionaries
            ORDER BY dictionary_id
        ''')
        
        dictionaries = [{
            'id': row[0],
            'name_arabic': row[1],
            'name_english': row[2],
            'description': row[3]
        } for row in cursor.fetchall()]
        
        conn.close()
        self.send_json(dictionaries)
    
    def handle_stats(self, params):
        """Get statistics, optionally filtered by dictionary_id"""
        dictionary_id = params.get('dictionary_id', [None])[0]
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if dictionary_id and dictionary_id != 'all':
            # Stats for specific dictionary
            dict_id = int(dictionary_id)
            cursor.execute('SELECT COUNT(*) FROM entries WHERE dictionary_id = ?', (dict_id,))
            total_entries = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM definitions d JOIN entries e ON d.entry_id = e.entry_id WHERE e.dictionary_id = ?', (dict_id,))
            total_definitions = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT name_arabic) FROM chapters WHERE dictionary_id = ?', (dict_id,))
            total_chapters = cursor.fetchone()[0]
            
            cursor.execute('SELECT MIN(page_number), MAX(page_number) FROM entries WHERE dictionary_id = ? AND page_number IS NOT NULL', (dict_id,))
            min_page, max_page = cursor.fetchone()
        else:
            # Stats for all dictionaries
            cursor.execute('SELECT COUNT(*) FROM entries')
            total_entries = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(*) FROM definitions')
            total_definitions = cursor.fetchone()[0]
            
            cursor.execute('SELECT COUNT(DISTINCT name_arabic) FROM chapters')
            total_chapters = cursor.fetchone()[0]
            
            cursor.execute('SELECT MIN(page_number), MAX(page_number) FROM entries WHERE page_number IS NOT NULL')
            min_page, max_page = cursor.fetchone()
        
        conn.close()
        
        data = {
            'total_entries': total_entries,
            'total_definitions': total_definitions,
            'total_chapters': total_chapters,
            'page_range': {'min': min_page, 'max': max_page}
        }
        
        self.send_json(data)
    
    def handle_chapters(self, params):
        """Get chapters, optionally filtered by dictionary_id"""
        dictionary_id = params.get('dictionary_id', [None])[0]
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if dictionary_id and dictionary_id != 'all':
            cursor.execute('''
                SELECT DISTINCT name_arabic, chapter_order
                FROM chapters
                WHERE dictionary_id = ?
                ORDER BY chapter_order
            ''', (int(dictionary_id),))
        else:
            cursor.execute('''
                SELECT DISTINCT name_arabic, chapter_order
                FROM chapters
                ORDER BY chapter_order
            ''')
        
        chapters = [{'name': row[0], 'order': row[1]} for row in cursor.fetchall()]
        conn.close()
        
        self.send_json(chapters)
    
    def handle_search(self, params):
        """
        Smart search with intelligent ranking:
        1. Exact matches first (headword = query)
        2. Starts with query (headword starts with query)
        3. Contains query (headword contains query)
        4. Root matches (root contains query)
        """
        query = params.get('q', [''])[0]
        mode = params.get('mode', ['all'])[0]
        limit = min(int(params.get('limit', ['50'])[0]), 200)
        dictionary_id = params.get('dictionary_id', [None])[0]
        
        if not query:
            self.send_json({'error': 'Query required'}, 400)
            return
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        query_norm = normalize_arabic(query)
        
        try:
            # SMART SEARCH with ranking
            # Build dictionary filter
            dict_filter = ''
            dict_filter_entries = ''
            dict_params = []
            if dictionary_id and dictionary_id != 'all':
                dict_filter = ' AND dictionary_id = ?'
                dict_filter_entries = ' AND e.dictionary_id = ?'
                dict_params = [int(dictionary_id)]
            
            if mode == 'exact':
                # Only exact matches
                sql = f'''
                    SELECT entry_id, 1 as rank
                    FROM entries 
                    WHERE headword_normalized = ?{dict_filter}
                    ORDER BY rank
                    LIMIT ?
                '''
                params_sql = [query_norm] + dict_params + [limit]
            
            elif mode == 'starts':
                # Starts with matches, with preference for exact
                sql = f'''
                    SELECT entry_id,
                           CASE 
                               WHEN headword_normalized = ? THEN 1
                               ELSE 2
                           END as rank
                    FROM entries 
                    WHERE headword_normalized LIKE ?{dict_filter}
                    ORDER BY rank
                    LIMIT ?
                '''
                params_sql = [query_norm, query_norm + '%'] + dict_params + [limit]
            
            elif mode == 'root':
                # Root matches only
                sql = f'''
                    SELECT entry_id,
                           CASE 
                               WHEN root = ? THEN 1
                               WHEN root LIKE ? THEN 2
                               ELSE 3
                           END as rank
                    FROM entries 
                    WHERE root LIKE ?{dict_filter}
                    ORDER BY rank
                    LIMIT ?
                '''
                params_sql = [query_norm, query_norm + '%', '%' + query_norm + '%'] + dict_params + [limit]
            
            else:  # 'all' or 'contains' - COMPREHENSIVE SMART SEARCH
                # Smart ranking with CASE WHEN (comprehensive, no duplicates)
                sql = f'''
                    SELECT DISTINCT entry_id,
                           CASE 
                               WHEN headword_normalized = ? THEN 1
                               WHEN headword_normalized LIKE ? THEN 2
                               WHEN headword_normalized LIKE ? THEN 3
                               WHEN root = ? THEN 4
                               WHEN root LIKE ? THEN 5
                               ELSE 6
                           END as rank
                    FROM entries 
                    WHERE (
                        headword_normalized = ?
                        OR headword_normalized LIKE ?
                        OR headword_normalized LIKE ?
                        OR root = ?
                        OR root LIKE ?
                        OR root LIKE ?
                        OR full_text LIKE ?
                    ){dict_filter}
                    ORDER BY rank, LENGTH(headword_normalized), headword_normalized
                    LIMIT ?
                '''
                params_sql = [
                    query_norm,              # CASE: Exact match
                    query_norm + '%',        # CASE: Starts with
                    '%' + query_norm + '%',  # CASE: Contains
                    query_norm,              # CASE: Root exact
                    query_norm + '%',        # CASE: Root starts
                    # WHERE conditions (comprehensive search)
                    query_norm,              # headword exact
                    query_norm + '%',        # headword starts
                    '%' + query_norm + '%',  # headword contains
                    query_norm,              # root exact
                    query_norm + '%',        # root starts
                    '%' + query_norm + '%',  # root contains
                    '%' + query_norm + '%',  # full_text contains (get ALL related)
                ] + dict_params + [limit]
            
            cursor.execute(sql, params_sql)
            entry_rows = cursor.fetchall()
            entry_ids = [row[0] for row in entry_rows]
            entry_id_set = set(entry_ids)

            # Secondary pass: search English definitions for the query (case-insensitive)
            definition_like = f"%{query.lower()}%"
            def_sql = f'''
                SELECT DISTINCT e.entry_id
                FROM entries e
                JOIN definitions d ON e.entry_id = d.entry_id
                WHERE LOWER(d.definition_text) LIKE ?{dict_filter_entries}
                LIMIT ?
            '''
            def_params = [definition_like] + dict_params + [limit]

            cursor.execute(def_sql, def_params)
            for (entry_id,) in cursor.fetchall():
                if entry_id not in entry_id_set:
                    entry_ids.append(entry_id)
                    entry_id_set.add(entry_id)
                if len(entry_ids) >= limit:
                    break
            
            # OPTIMIZED: Batch fetch all entries in ONE query instead of looping
            results = self.get_entries_batch(cursor, entry_ids)
            
            conn.close()
            self.send_json({'query': query, 'total_results': len(results), 'results': results})
        except Exception as e:
            conn.close()
            self.send_json({'error': str(e)}, 500)
    
    def handle_browse(self, chapter_name, params):
        """Browse chapter entries, optionally filtered by dictionary_id"""
        limit = min(int(params.get('limit', ['100'])[0]), 200)
        dictionary_id = params.get('dictionary_id', [None])[0]
        
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        if dictionary_id and dictionary_id != 'all':
            cursor.execute('''
                SELECT e.entry_id
                FROM entries e
                LEFT JOIN sections s ON e.section_id = s.section_id
                LEFT JOIN chapters c ON s.chapter_id = c.chapter_id
                WHERE c.name_arabic LIKE ? AND e.dictionary_id = ?
                ORDER BY e.page_number, e.entry_order
                LIMIT ?
            ''', ('%' + chapter_name + '%', int(dictionary_id), limit))
        else:
            cursor.execute('''
                SELECT e.entry_id
                FROM entries e
                LEFT JOIN sections s ON e.section_id = s.section_id
                LEFT JOIN chapters c ON s.chapter_id = c.chapter_id
                WHERE c.name_arabic LIKE ?
                ORDER BY e.page_number, e.entry_order
                LIMIT ?
            ''', ('%' + chapter_name + '%', limit))
        
        entry_ids = [row[0] for row in cursor.fetchall()]
        
        # OPTIMIZED: Batch fetch instead of loop
        results = self.get_entries_batch(cursor, entry_ids)
        
        conn.close()
        self.send_json({'chapter': chapter_name, 'total_results': len(results), 'results': results})
    
    def get_entries_batch(self, cursor, entry_ids):
        """
        OPTIMIZED: Fetch multiple entries in batched queries instead of one-by-one
        This reduces 150+ queries to just 2-3 queries for 50 results!
        """
        if not entry_ids:
            return []
        
        # Build placeholders for IN clause
        placeholders = ','.join('?' * len(entry_ids))
        
        # Single query to get all entries with their metadata
        cursor.execute(f'''
            SELECT e.entry_id, e.headword, e.root, e.page_number, e.dictionary_id,
                   s.name_arabic as section_name,
                   c.name_arabic as chapter_name,
                   d.name_arabic as dictionary_name,
                   e.full_text
            FROM entries e
            LEFT JOIN sections s ON e.section_id = s.section_id
            LEFT JOIN chapters c ON s.chapter_id = c.chapter_id
            LEFT JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
            WHERE e.entry_id IN ({placeholders})
        ''', entry_ids)
        
        entries_data = {row[0]: row for row in cursor.fetchall()}
        
        # Single query to get all definitions
        cursor.execute(f'''
            SELECT entry_id, definition_text
            FROM definitions
            WHERE entry_id IN ({placeholders})
            ORDER BY entry_id, definition_order
        ''', entry_ids)
        
        definitions_map = {}
        for entry_id, def_text in cursor.fetchall():
            if entry_id not in definitions_map:
                definitions_map[entry_id] = []
            if len(definitions_map[entry_id]) < 10:  # Limit to 10 definitions
                definitions_map[entry_id].append(def_text)
        
        # Fetch plurals for all entries in batch
        cursor.execute(f'''
            SELECT entry_id, plural_form
            FROM plurals
            WHERE entry_id IN ({placeholders})
            ORDER BY entry_id, plural_order
        ''', entry_ids)
        
        plurals_map = {}
        for entry_id, plural_form in cursor.fetchall():
            if entry_id not in plurals_map:
                plurals_map[entry_id] = []
            plurals_map[entry_id].append(plural_form)
        
        # Fetch sub-entries for all entries in batch (related words)
        cursor.execute(f'''
            SELECT parent_entry_id, headword, definition_snippet
            FROM sub_entries
            WHERE parent_entry_id IN ({placeholders})
            ORDER BY parent_entry_id, sub_entry_id
        ''', entry_ids)
        
        sub_entries_map = {}
        for parent_id, sub_word, sub_def in cursor.fetchall():
            if parent_id not in sub_entries_map:
                sub_entries_map[parent_id] = []
            # Limit to 10 sub-entries per entry to avoid clutter
            if len(sub_entries_map[parent_id]) < 10:
                sub_entries_map[parent_id].append({
                    'word': sub_word,
                    'definition': sub_def[:100] if sub_def else ''  # Limit definition length
                })
        
        # Build results maintaining original order
        results = []
        for entry_id in entry_ids:
            if entry_id not in entries_data:
                continue
            
            row = entries_data[entry_id]
            definitions = definitions_map.get(entry_id, [])
            plurals = plurals_map.get(entry_id, [])
            sub_entries = sub_entries_map.get(entry_id, [])
            dictionary_id = row[4]
            root = row[2] or ''
            
            # Clean and validate root - hide bad roots
            # Dictionaries with reliable roots: 1 (Muhit), 3 (Ayn), 4 (Fiqhi), 7 (Muhit fil Lugha), 8 (Muasir), 10 (Sihah)
            # Hide roots from: 2 (Waseet - unreliable), 5 (Tarifat - no roots), 9 (Mawrid - Arabic-English)
            display_root = ''
            if dictionary_id not in [2, 5, 9] and root:
                # Only show if it looks like a valid 3-4 letter root (no spaces, no long text)
                root_clean = root.strip()
                if len(root_clean) >= 2 and len(root_clean) <= 6 and ' ' not in root_clean:
                    display_root = root_clean
            
            # If no definitions, use full_text
            if not definitions and row[8]:
                definitions = [row[8]]
            
            results.append({
                'id': row[0],
                'headword': row[1],
                'root': display_root,  # Only valid, clean roots
                'page': row[3],
                'dictionary_id': row[4],
                'dictionary_name': row[7] or '',
                'chapter': row[6] or '',
                'section': row[5] or '',
                'definitions': definitions,
                'plurals': plurals,  # Now includes actual plural forms!
                'hasPlurals': len(plurals) > 0,
                'subEntries': sub_entries,  # Related words under this entry
                'hasSubEntries': len(sub_entries) > 0
            })
        
        return results
    
    def get_entry_full(self, cursor, entry_id):
        cursor.execute('''
            SELECT e.entry_id, e.headword, e.root, e.page_number, e.dictionary_id,
                   s.name_arabic as section_name,
                   c.name_arabic as chapter_name,
                   d.name_arabic as dictionary_name,
                   e.full_text
            FROM entries e
            LEFT JOIN sections s ON e.section_id = s.section_id
            LEFT JOIN chapters c ON s.chapter_id = c.chapter_id
            LEFT JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
            WHERE e.entry_id = ?
        ''', (entry_id,))
        
        row = cursor.fetchone()
        if not row:
            return None
        
        # Try to get from definitions table first
        cursor.execute('SELECT definition_text FROM definitions WHERE entry_id = ? ORDER BY definition_order LIMIT 10', (entry_id,))
        definitions = [d[0] for d in cursor.fetchall()]
        
        # If no definitions, use full_text (for dictionaries like العين)
        if not definitions and row[8]:  # row[8] is full_text
            definitions = [row[8]]
        
        cursor.execute('SELECT plural_form FROM plurals WHERE entry_id = ?', (entry_id,))
        plurals = [p[0] for p in cursor.fetchall()]
        
        # Fetch sub-entries (related words)
        cursor.execute('''
            SELECT headword, definition_snippet
            FROM sub_entries
            WHERE parent_entry_id = ?
            ORDER BY sub_entry_id
            LIMIT 10
        ''', (entry_id,))
        sub_entries = []
        for sub_word, sub_def in cursor.fetchall():
            sub_entries.append({
                'word': sub_word,
                'definition': sub_def[:100] if sub_def else ''
            })
        
        dictionary_id = row[4]
        root = row[2] or ''
        
        # Clean and validate root - same logic as batch function
        display_root = ''
        if dictionary_id not in [2, 5, 9] and root:
            root_clean = root.strip()
            if len(root_clean) >= 2 and len(root_clean) <= 6 and ' ' not in root_clean:
                display_root = root_clean
        
        return {
            'id': row[0],
            'headword': row[1],
            'root': display_root,  # Only valid, clean roots
            'page': row[3],
            'dictionary_id': row[4],
            'dictionary_name': row[7] or '',
            'chapter': row[6] or '',
            'section': row[5] or '',
            'definitions': definitions,
            'plurals': plurals,
            'hasPlurals': len(plurals) > 0,
            'subEntries': sub_entries,
            'hasSubEntries': len(sub_entries) > 0,
            'full_text': row[8] or ''
        }
    
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

if __name__ == '__main__':
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database not found: {DATABASE_PATH}")
        exit(1)
    
    PORT = 5000
    print("=" * 60)
    print("Arabic Dictionary - Multi-Dictionary Server")
    print("=" * 60)
    print(f"Database: {DATABASE_PATH}")
    print(f"Server: http://localhost:{PORT}")
    print("")
    
    # Show which dictionaries are available
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute('SELECT dictionary_id, name_english FROM dictionaries ORDER BY dictionary_id')
        dicts = cursor.fetchall()
        print("Available dictionaries:")
        for dict_id, name in dicts:
            print(f"  {dict_id}. {name}")
        conn.close()
    except:
        print("Serving multiple dictionaries")
    
    print("")
    print(f"Open: http://localhost:5000")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    server = HTTPServer(('0.0.0.0', PORT), DictionaryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped")
        server.shutdown()
