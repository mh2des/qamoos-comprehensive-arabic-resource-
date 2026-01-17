#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arabic Dictionary - PostgreSQL Server
======================================

Flask server with PostgreSQL backend for production deployment.

Environment variables:
    DATABASE_URL - PostgreSQL connection string (default: postgresql://localhost/qamoos_db)
    PORT - Server port (default: 5000)
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import sys
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

app = Flask(__name__)

# CORS configuration for production
ALLOWED_ORIGINS = [
    'https://qamoos.org',
    'https://www.qamoos.org',
    'http://localhost:5000',
    'http://127.0.0.1:5000'
]
CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# PostgreSQL connection from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@localhost:5432/qamoos_db')
PORT = int(os.getenv('PORT', 5000))
FLASK_ENV = os.getenv('FLASK_ENV', 'development')

def get_db_connection():
    """Create PostgreSQL connection"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    # Set search path for Neon compatibility
    cursor = conn.cursor()
    cursor.execute("SET search_path TO public")
    cursor.close()
    return conn

def normalize_arabic(text):
    """Remove Arabic diacritics for search normalization"""
    if not text:
        return ''
    diacritics = '\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0653\u0654\u0655\u0656\u0657\u0658\u0670'
    for d in diacritics:
        text = text.replace(d, '')
    text = text.replace('\u0640', '')
    return text

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dictionaries')
        count = cursor.fetchone()['count']
        conn.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'dictionaries': count,
            'environment': FLASK_ENV
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/')
def index():
    """Serve main page"""
    return send_file('index.html')

@app.route('/search')
def search_page():
    """Serve search page"""
    return send_file('search.html')

@app.route('/poetry.html')
def poetry_page():
    """Serve poetry page"""
    return send_file('poetry.html')

@app.route('/api/dictionaries')
def get_dictionaries():
    """Get list of all dictionaries"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT dictionary_id as id, name_arabic, name_english, author, year
            FROM dictionaries
            ORDER BY dictionary_id
        ''')
        
        dictionaries = cursor.fetchall()
        conn.close()
        
        return jsonify({'dictionaries': dictionaries})
    except Exception as e:
        print(f"❌ Dictionaries endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats')
def get_stats():
    """Get dictionary statistics"""
    try:
        dictionary_id = request.args.get('dictionary_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if dictionary_id and dictionary_id != 'all':
            # Stats for specific dictionary
            cursor.execute('''
                SELECT COUNT(*) as entry_count
                FROM entries
                WHERE dictionary_id = %s
            ''', (int(dictionary_id),))
            
            result = cursor.fetchone()
            
            cursor.execute('''
                SELECT COUNT(*) as sub_entry_count
                FROM sub_entries
                WHERE dictionary_id = %s
            ''', (int(dictionary_id),))
            
            sub_result = cursor.fetchone()
            
            stats = {
                'dictionary_id': int(dictionary_id),
                'entry_count': result['entry_count'],
                'sub_entry_count': sub_result['sub_entry_count'],
                'total': result['entry_count'] + sub_result['sub_entry_count']
            }
        else:
            # Overall stats
            cursor.execute('SELECT COUNT(*) as total FROM entries')
            entries = cursor.fetchone()
            
            cursor.execute('SELECT COUNT(*) as total FROM sub_entries')
            sub_entries = cursor.fetchone()
            
            stats = {
                'total_entries': entries['total'],
                'total_sub_entries': sub_entries['total'],
                'total': entries['total'] + sub_entries['total']
            }
        
        conn.close()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search')
def search():
    """
    Search API with two-tier architecture:
    - Tier 1: Fast indexed lookup in sub_entries (for كتاب العين derivatives)
    - Tier 2: Full-text search in entries table
    
    Parameters:
        q - search query
        dictionary_id - filter by dictionary (optional)
        mode - search mode: exact, starts, contains, all (default: all)
        limit - max results (default: 50)
    """
    try:
        query = request.args.get('q', '').strip()
        dictionary_id = request.args.get('dictionary_id')
        mode = request.args.get('mode', 'all')
        limit = min(int(request.args.get('limit', '50')), 200)
        
        if not query:
            return jsonify({'error': 'Query parameter required'}), 400
        
        query_norm = normalize_arabic(query)
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        dict_filter_tier1 = ""
        dict_filter_tier2 = ""
        dict_params = []
        if dictionary_id and dictionary_id != 'all':
            dict_filter_tier1 = " AND s.dictionary_id = %s"
            dict_filter_tier2 = " AND e.dictionary_id = %s"
            dict_params = [int(dictionary_id)]
        
        # ================================================================
        # TIER 1: Query sub_entries (Materialized Derivatives)
        # Only for dictionary_id=3 (كتاب العين) since that's where sub_entries exist
        # ================================================================
        if dictionary_id == '3' or (not dictionary_id or dictionary_id == 'all'):
            tier1_sql = f'''
                SELECT 
                    s.sub_entry_id,
                    s.headword,
                    s.definition_snippet,
                    s.definition_snippet as full_text,
                    s.root,
                    e.headword as root_headword,
                    e.entry_id as parent_entry_id,
                    e.full_text as parent_full_text,
                    d.name_arabic as dictionary_name,
                    s.dictionary_id,
                    1 as tier
                FROM sub_entries s
                JOIN entries e ON s.parent_entry_id = e.entry_id
                JOIN dictionaries d ON s.dictionary_id = d.dictionary_id
                WHERE s.headword_normalized = %s{dict_filter_tier1}
                LIMIT %s
            '''
            
            cursor.execute(tier1_sql, [query_norm] + dict_params + [limit])
            tier1_results = cursor.fetchall()
            
            if tier1_results and dictionary_id == '3':
                # If searching ONLY dict 3, return tier1 results
                results = [dict(row) for row in tier1_results]
                conn.close()
                return jsonify({
                    'tier': 1,
                    'query': query,
                    'results': results,
                    'count': len(results)
                })
            elif tier1_results and (not dictionary_id or dictionary_id == 'all'):
                # If searching ALL dicts, combine tier1 with tier2
                tier1_list = [dict(row) for row in tier1_results]
            else:
                tier1_list = []
        else:
            # Skip tier 1 for other specific dictionaries
            tier1_list = []
        
        # ================================================================
        # TIER 2: Full-Text Search Fallback (Comprehensive)
        # ================================================================
        if mode == 'exact':
            tier2_sql = f'''
                SELECT e.entry_id, e.headword, e.root, e.full_text,
                       d.name_arabic as dictionary_name, e.dictionary_id,
                       2 as tier
                FROM entries e
                JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
                WHERE (e.headword_normalized = %s OR e.headword_normalized = 'ال' || %s){dict_filter_tier2}
                ORDER BY LENGTH(e.headword) ASC
                LIMIT %s
            '''
            tier2_params = [query_norm, query_norm] + dict_params + [limit]
            
        elif mode == 'starts':
            tier2_sql = f'''
                SELECT e.entry_id, e.headword, e.root, e.full_text,
                       d.name_arabic as dictionary_name, e.dictionary_id,
                       2 as tier
                FROM entries e
                JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
                WHERE e.headword_normalized LIKE %s{dict_filter_tier2}
                LIMIT %s
            '''
            tier2_params = [query_norm + '%'] + dict_params + [limit]
            
        else:  # 'all' or 'contains' - Comprehensive search with smart ranking
            tier2_sql = f'''
                SELECT DISTINCT e.entry_id, e.headword, e.root, 
                       e.full_text,
                       d.name_arabic as dictionary_name,
                       e.dictionary_id,
                       2 as tier,
                       (CASE 
                        WHEN e.headword_normalized = %s THEN 1
                        WHEN e.headword_normalized LIKE %s THEN 2
                        WHEN e.root = %s THEN 3
                        WHEN e.root LIKE %s THEN 4
                        WHEN e.headword_normalized LIKE %s THEN 5
                        ELSE 6
                       END) as rank,
                       LENGTH(e.headword) as hw_length
                FROM entries e
                JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
                WHERE (
                    e.headword_normalized = %s
                    OR e.headword_normalized LIKE %s
                    OR e.headword_normalized LIKE %s
                    OR e.root = %s
                    OR e.root LIKE %s
                    OR e.full_text LIKE %s
                ){dict_filter_tier2}
                ORDER BY rank ASC, hw_length ASC
                LIMIT %s
            '''
            tier2_params = [
                # Ranking parameters
                query_norm,                  # Exact match
                query_norm + '%',            # Starts with
                query_norm,                  # Root exact
                query_norm + '%',            # Root starts
                '%' + query_norm + '%',      # Contains
                # WHERE clause parameters
                query_norm,                  # Exact match
                query_norm + '%',            # Starts with
                '%' + query_norm + '%',      # Contains in headword
                query_norm,                  # Root exact
                '%' + query_norm + '%',      # Root contains
                '%' + query_norm + '%',      # Full text contains
            ] + dict_params + [limit]
        
        cursor.execute(tier2_sql, tier2_params)
        tier2_results = cursor.fetchall()
        
        # Combine tier 1 and tier 2 results
        if tier2_results or tier1_list:
            tier2_list = [dict(row) for row in tier2_results] if tier2_results else []
            
            # Combine and deduplicate
            combined = tier1_list + tier2_list
            seen = set()
            unique_results = []
            for r in combined:
                key = (r.get('entry_id') or r.get('sub_entry_id'), r['headword'])
                if key not in seen:
                    seen.add(key)
                    unique_results.append(r)
            
            results = unique_results[:limit]  # Apply limit after combining
            
            # Fetch definitions for each result
            for result in results:
                entry_id = result.get('entry_id')
                if entry_id:
                    cursor.execute('''
                        SELECT definition_text
                        FROM definitions
                        WHERE entry_id = %s
                        ORDER BY definition_order
                        LIMIT 5
                    ''', (entry_id,))
                    defs = cursor.fetchall()
                    result['definitions'] = [d['definition_text'] for d in defs] if defs else []
                
                # Clean and validate root
                dictionary_id = result.get('dictionary_id')
                root = result.get('root', '')
                display_root = ''
                
                if dictionary_id not in [2, 5, 9] and root:
                    root_clean = root.strip() if root else ''
                    if len(root_clean) >= 2 and len(root_clean) <= 6 and ' ' not in root_clean:
                        display_root = root_clean
                
                result['root'] = display_root
            
            conn.close()
            return jsonify({
                'tier': 'combined' if tier1_list and tier2_list else (1 if tier1_list else 2),
                'query': query,
                'results': results,
                'count': len(results)
            })
        
        # No results found
        conn.close()
        return jsonify({
            'tier': 0,
            'query': query,
            'results': [],
            'count': 0,
            'message': 'No results found'
        })
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/entry/<int:entry_id>')
def get_entry(entry_id):
    """Get full entry details"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT e.*, d.name_arabic as dictionary_name
            FROM entries e
            JOIN dictionaries d ON e.dictionary_id = d.dictionary_id
            WHERE e.entry_id = %s
        ''', (entry_id,))
        
        entry = cursor.fetchone()
        
        if not entry:
            conn.close()
            return jsonify({'error': 'Entry not found'}), 404
        
        # Get definitions
        cursor.execute('''
            SELECT definition_text, definition_order
            FROM definitions
            WHERE entry_id = %s
            ORDER BY definition_order
        ''', (entry_id,))
        
        definitions = cursor.fetchall()
        
        result = dict(entry)
        result['definitions'] = [dict(d) for d in definitions]
        
        # Clean and validate root
        dictionary_id = result.get('dictionary_id')
        root = result.get('root', '')
        display_root = ''
        
        if dictionary_id not in [2, 5, 9] and root:
            root_clean = root.strip() if root else ''
            if len(root_clean) >= 2 and len(root_clean) <= 6 and ' ' not in root_clean:
                display_root = root_clean
        
        result['root'] = display_root
        
        conn.close()
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/chapters')
def get_chapters():
    """Get chapters for a dictionary"""
    try:
        dictionary_id = request.args.get('dictionary_id')
        
        if not dictionary_id or dictionary_id == 'all':
            return jsonify({'error': 'dictionary_id required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT chapter_id, name_arabic, chapter_order
            FROM chapters
            WHERE dictionary_id = %s
            ORDER BY chapter_order
        ''', (int(dictionary_id),))
        
        chapters = cursor.fetchall()
        conn.close()
        
        return jsonify([dict(c) for c in chapters])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poets')
def api_poets():
    """List poets with optional search, pagination"""
    try:
        q = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 50)), 200)
        offset = int(request.args.get('offset', 0))

        conn = get_db_connection()
        cursor = conn.cursor()

        base_sql = 'SELECT poet_id, name_arabic, bio_arabic, poems_count FROM poets'
        params = []
        if q:
            base_sql += ' WHERE name_arabic ILIKE %s OR bio_arabic ILIKE %s'
            like = f'%{q}%'
            params.extend([like, like])

        base_sql += ' ORDER BY poems_count DESC NULLS LAST, poet_id ASC LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        cursor.execute(base_sql, params)
        poets = cursor.fetchall()
        conn.close()

        return jsonify({'count': len(poets), 'poets': [dict(p) for p in poets]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poet/<int:poet_id>')
def api_poet(poet_id):
    """Get poet details and sample poems"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT poet_id, name_arabic, bio_arabic, poems_count FROM poets WHERE poet_id = %s', (poet_id,))
        poet = cursor.fetchone()
        if not poet:
            conn.close()
            return jsonify({'error': 'Poet not found'}), 404

        # Get first 20 poems for this poet as preview
        cursor.execute('SELECT poem_id, title_arabic, verses_count FROM poems WHERE poet_id = %s ORDER BY poem_id LIMIT 20', (poet_id,))
        poems = cursor.fetchall()

        result = dict(poet)
        result['poems_preview'] = [dict(p) for p in poems]

        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poems')
def api_poems():
    """List poems, filter by poet_id or search title/text"""
    try:
        poet_id = request.args.get('poet_id')
        q = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 50)), 200)
        offset = int(request.args.get('offset', 0))

        conn = get_db_connection()
        cursor = conn.cursor()

        params = []
        sql = 'SELECT poem_id, poet_id, title_arabic, verses_count FROM poems'
        where = []
        if poet_id:
            where.append('poet_id = %s')
            params.append(int(poet_id))
        if q:
            where.append('(title_arabic ILIKE %s OR full_text ILIKE %s)')
            like = f'%{q}%'
            params.extend([like, like])

        if where:
            sql += ' WHERE ' + ' AND '.join(where)

        sql += ' ORDER BY poem_id DESC LIMIT %s OFFSET %s'
        params.extend([limit, offset])

        cursor.execute(sql, params)
        poems = cursor.fetchall()
        conn.close()

        return jsonify({'count': len(poems), 'poems': [dict(p) for p in poems]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poem/<int:poem_id>')
def api_poem(poem_id):
    """Get full poem with verses"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT p.*, pt.name_arabic as topic, m.name_arabic as meter, po.name_arabic as poet_name FROM poems p LEFT JOIN poetry_topics pt ON p.topic_id = pt.topic_id LEFT JOIN poetry_meters m ON p.meter_id = m.meter_id LEFT JOIN poets po ON p.poet_id = po.poet_id WHERE p.poem_id = %s', (poem_id,))
        poem = cursor.fetchone()
        if not poem:
            conn.close()
            return jsonify({'error': 'Poem not found'}), 404

        # Get verses
        cursor.execute('SELECT verse_number, first_hemistich, second_hemistich, full_verse FROM verses WHERE poem_id = %s ORDER BY verse_number', (poem_id,))
        verses = cursor.fetchall()

        result = dict(poem)
        result['verses'] = [dict(v) for v in verses] if verses else []

        conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/poetry/search')
def api_poetry_search():
    """Search poems and verses by keyword (simple, safe)"""
    try:
        q = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 50)), 200)
        if not q:
            return jsonify({'error': 'q parameter required'}), 400

        like = f'%{q}%'
        conn = get_db_connection()
        cursor = conn.cursor()

        # Search in poem titles first
        cursor.execute('SELECT poem_id, poet_id, title_arabic, verses_count FROM poems WHERE title_arabic ILIKE %s LIMIT %s', (like, limit))
        title_matches = cursor.fetchall()

        # Search in verses
        cursor.execute('SELECT DISTINCT v.poem_id FROM verses v WHERE v.full_verse ILIKE %s LIMIT %s', (like, limit))
        verse_matches = cursor.fetchall()

        poem_ids = set([r['poem_id'] for r in title_matches] + [r['poem_id'] for r in verse_matches])

        if not poem_ids:
            conn.close()
            return jsonify({'count': 0, 'results': []})

        params = list(poem_ids)
        sql = 'SELECT poem_id, poet_id, title_arabic, verses_count FROM poems WHERE poem_id = ANY(%s)'
        cursor.execute(sql, (params,))
        poems = cursor.fetchall()
        conn.close()

        return jsonify({'count': len(poems), 'results': [dict(p) for p in poems]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Static file routes
@app.route('/<path:path>')
def static_files(path):
    """Serve static files"""
    try:
        return send_file(path)
    except:
        return "File not found", 404

if __name__ == '__main__':
    print("=" * 80)
    print("Arabic Dictionary - PostgreSQL Server")
    print("=" * 80)
    print(f"Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL}")
    print(f"Server: http://localhost:{PORT}")
    print("=" * 80)
    
    # Test connection
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM dictionaries')
        dict_count = cursor.fetchone()['count']
        print(f"\n✅ Connected to PostgreSQL")
        print(f"✅ Found {dict_count} dictionaries")
        conn.close()
    except Exception as e:
        print(f"\n❌ Database connection failed: {e}")
        print("Make sure PostgreSQL is running and DATABASE_URL is correct")
        exit(1)
    
    print(f"\nPress Ctrl+C to stop")
    print("=" * 80)
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
