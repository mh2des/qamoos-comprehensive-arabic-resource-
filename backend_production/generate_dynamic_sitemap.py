#!/usr/bin/env python3
"""
Generate comprehensive sitemaps for all dictionary entries
This will create multiple sitemap files (max 50,000 URLs each) and a sitemap index
"""
import psycopg2
from datetime import datetime
import os
from urllib.parse import quote
import sys

def generate_entry_sitemaps():
    """Generate sitemaps with ALL dictionary entries"""
    
    # Get database connection
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set!")
        print("Please set it in your .env file or export it:")
        print('export DATABASE_URL="postgresql://user:pass@host/dbname"')
        sys.exit(1)
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        print("📊 Fetching all dictionary entries...")
        
        # Get all entries with their dictionary info
        cursor.execute('''
            SELECT 
                e.entry_id, 
                e.headword, 
                e.headword_normalized, 
                d.name_arabic,
                d.name_english
            FROM entries e
            JOIN sections s ON e.section_id = s.section_id
            JOIN chapters c ON s.chapter_id = c.chapter_id
            JOIN dictionaries d ON c.dictionary_id = d.dictionary_id
            ORDER BY e.entry_id
        ''')
        
        entries = cursor.fetchall()
        total_entries = len(entries)
        print(f"✅ Found {total_entries:,} entries")
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Create output directory if it doesn't exist
        output_dir = '../frontend-deploy'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create multiple sitemaps (max 25,000 URLs per sitemap to avoid size issues)
        chunk_size = 25000
        sitemap_files = []
        
        print(f"\n📝 Generating sitemap files (max {chunk_size:,} URLs per file)...")
        
        for i in range(0, total_entries, chunk_size):
            chunk = entries[i:i+chunk_size]
            sitemap_num = (i // chunk_size) + 1
            filename = f'sitemap-entries-{sitemap_num}.xml'
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
                
                for entry_id, headword, normalized, dict_arabic, dict_english in chunk:
                    # Use normalized headword for URL (better for search)
                    url_word = quote(normalized or headword)
                    
                    # Create SEO-friendly URL with entry ID
                    f.write(f'  <url>\n')
                    f.write(f'    <loc>https://qamoos.org/search?q={url_word}&amp;entry={entry_id}</loc>\n')
                    f.write(f'    <lastmod>{today}</lastmod>\n')
                    f.write(f'    <changefreq>monthly</changefreq>\n')
                    f.write(f'    <priority>0.7</priority>\n')
                    f.write(f'  </url>\n')
                
                f.write('</urlset>\n')
            
            sitemap_files.append(filename)
            print(f"  ✅ Created {filename} ({len(chunk):,} entries)")
        
        print(f"\n📋 Creating sitemap index...")
        
        # Create sitemap index that points to all sitemaps
        index_filepath = os.path.join(output_dir, 'sitemap-index.xml')
        with open(index_filepath, 'w', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            f.write('<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            
            # Include the main static sitemap
            f.write(f'  <sitemap>\n')
            f.write(f'    <loc>https://qamoos.org/sitemap.xml</loc>\n')
            f.write(f'    <lastmod>{today}</lastmod>\n')
            f.write(f'  </sitemap>\n')
            
            # Include all entry sitemaps
            for filename in sitemap_files:
                f.write(f'  <sitemap>\n')
                f.write(f'    <loc>https://qamoos.org/{filename}</loc>\n')
                f.write(f'    <lastmod>{today}</lastmod>\n')
                f.write(f'  </sitemap>\n')
            
            f.write('</sitemapindex>\n')
        
        print(f"  ✅ Created sitemap-index.xml")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ SITEMAP GENERATION COMPLETE!")
        print("="*60)
        print(f"📊 Total entries indexed: {total_entries:,}")
        print(f"📄 Sitemap files created: {len(sitemap_files)}")
        print(f"📋 Main index: sitemap-index.xml")
        print("\n📍 Files created in: {output_dir}/")
        print("\n🚀 NEXT STEPS:")
        print("1. Update robots.txt to point to sitemap-index.xml")
        print("2. Deploy to Cloudflare Pages:")
        print(f"   cd {output_dir}")
        print("   npx wrangler pages deploy . --project-name qamoos-org --branch production")
        print("\n3. Submit to Google Search Console:")
        print("   https://search.google.com/search-console")
        print("   Submit: https://qamoos.org/sitemap-index.xml")
        print("\n4. Submit to Bing Webmaster Tools:")
        print("   https://www.bing.com/webmasters")
        print("   Submit: https://qamoos.org/sitemap-index.xml")
        print("="*60)
        
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    print("🚀 Dynamic Sitemap Generator for Qamoos.org")
    print("="*60)
    success = generate_entry_sitemaps()
    sys.exit(0 if success else 1)
