"""
Create Poetry Tables in Existing Database
Integrates seamlessly with dictionary structure
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def create_poetry_tables():
    """Create all poetry-related tables"""
    conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    cursor = conn.cursor()
    
    print("🎭 Creating Poetry Tables in Existing Database...")
    
    # Drop existing tables if they exist (for clean setup)
    print("  📋 Dropping existing poetry tables (if any)...")
    cursor.execute("""
        DROP TABLE IF EXISTS poetry_favorites CASCADE;
        DROP TABLE IF EXISTS verses CASCADE;
        DROP TABLE IF EXISTS poems CASCADE;
        DROP TABLE IF EXISTS poets CASCADE;
        DROP TABLE IF EXISTS poetry_topics CASCADE;
        DROP TABLE IF EXISTS poetry_meters CASCADE;
        DROP TABLE IF EXISTS poetry_eras CASCADE;
        DROP TABLE IF EXISTS poetry_countries CASCADE;
    """)
    
    # 1. Poetry Eras (العصور)
    print("  ✅ Creating poetry_eras table...")
    cursor.execute("""
        CREATE TABLE poetry_eras (
            era_id SERIAL PRIMARY KEY,
            name_arabic VARCHAR(100) UNIQUE NOT NULL,
            name_english VARCHAR(100),
            description TEXT,
            start_year INTEGER,
            end_year INTEGER,
            poets_count INTEGER DEFAULT 0,
            poems_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert common eras
    cursor.execute("""
        INSERT INTO poetry_eras (name_arabic, name_english, start_year, end_year, description) VALUES
        ('العصر الجاهلي', 'Pre-Islamic Era', -500, 610, 'The era before Islam'),
        ('العصر الإسلامي', 'Islamic Era', 610, 661, 'Early Islamic period'),
        ('العصر الأموي', 'Umayyad Era', 661, 750, 'Umayyad Caliphate'),
        ('العصر العباسي', 'Abbasid Era', 750, 1258, 'Abbasid Caliphate'),
        ('العصر الأندلسي', 'Andalusian Era', 711, 1492, 'Islamic Spain'),
        ('العصر المملوكي', 'Mamluk Era', 1250, 1517, 'Mamluk Sultanate'),
        ('العصر العثماني', 'Ottoman Era', 1517, 1918, 'Ottoman Empire'),
        ('العصر الحديث', 'Modern Era', 1800, 2000, 'Modern poetry'),
        ('العصر المعاصر', 'Contemporary Era', 2000, NULL, 'Contemporary poetry')
    """)
    
    # 2. Poetry Countries (الدول)
    print("  ✅ Creating poetry_countries table...")
    cursor.execute("""
        CREATE TABLE poetry_countries (
            country_id SERIAL PRIMARY KEY,
            name_arabic VARCHAR(100) UNIQUE NOT NULL,
            name_english VARCHAR(100),
            region VARCHAR(100),  -- الخليج، المشرق، المغرب العربي، etc.
            poets_count INTEGER DEFAULT 0,
            poems_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert Arab countries
    cursor.execute("""
        INSERT INTO poetry_countries (name_arabic, name_english, region) VALUES
        ('السعودية', 'Saudi Arabia', 'الخليج'),
        ('مصر', 'Egypt', 'المشرق'),
        ('العراق', 'Iraq', 'المشرق'),
        ('سوريا', 'Syria', 'المشرق'),
        ('لبنان', 'Lebanon', 'المشرق'),
        ('الأردن', 'Jordan', 'المشرق'),
        ('فلسطين', 'Palestine', 'المشرق'),
        ('اليمن', 'Yemen', 'الجزيرة العربية'),
        ('الإمارات', 'UAE', 'الخليج'),
        ('الكويت', 'Kuwait', 'الخليج'),
        ('قطر', 'Qatar', 'الخليج'),
        ('البحرين', 'Bahrain', 'الخليج'),
        ('عمان', 'Oman', 'الخليج'),
        ('المغرب', 'Morocco', 'المغرب العربي'),
        ('الجزائر', 'Algeria', 'المغرب العربي'),
        ('تونس', 'Tunisia', 'المغرب العربي'),
        ('ليبيا', 'Libya', 'المغرب العربي'),
        ('السودان', 'Sudan', 'أفريقيا'),
        ('الصومال', 'Somalia', 'أفريقيا'),
        ('جيبوتي', 'Djibouti', 'أفريقيا'),
        ('موريتانيا', 'Mauritania', 'المغرب العربي')
    """)
    
    # 3. Poetry Topics (موضوعات القصيدة)
    print("  ✅ Creating poetry_topics table...")
    cursor.execute("""
        CREATE TABLE poetry_topics (
            topic_id SERIAL PRIMARY KEY,
            name_arabic VARCHAR(100) UNIQUE NOT NULL,
            name_english VARCHAR(100),
            description TEXT,
            poems_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert common poetry topics
    cursor.execute("""
        INSERT INTO poetry_topics (name_arabic, name_english, description) VALUES
        ('غزل', 'Love Poetry', 'Poetry about love and romance'),
        ('مدح', 'Praise', 'Poetry praising people or virtues'),
        ('رثاء', 'Elegy', 'Poetry mourning the dead'),
        ('هجاء', 'Satire', 'Satirical poetry'),
        ('وصف', 'Description', 'Descriptive poetry'),
        ('حكمة', 'Wisdom', 'Poetry containing wisdom'),
        ('فخر', 'Boasting', 'Poetry about pride and glory'),
        ('شكوى', 'Complaint', 'Poetry expressing grievances'),
        ('اعتذار', 'Apology', 'Apologetic poetry'),
        ('حماسة', 'Enthusiasm', 'Poetry about bravery and war'),
        ('وطنية', 'Patriotic', 'Patriotic poetry'),
        ('دينية', 'Religious', 'Religious poetry'),
        ('فلسفية', 'Philosophical', 'Philosophical poetry'),
        ('اجتماعية', 'Social', 'Poetry about social issues'),
        ('رومانسية', 'Romantic', 'Romantic poetry'),
        ('طبيعة', 'Nature', 'Poetry about nature'),
        ('قومية', 'Nationalist', 'Nationalist poetry')
    """)
    
    # 4. Poetry Meters (البحور الشعرية)
    print("  ✅ Creating poetry_meters table...")
    cursor.execute("""
        CREATE TABLE poetry_meters (
            meter_id SERIAL PRIMARY KEY,
            name_arabic VARCHAR(100) UNIQUE NOT NULL,
            name_english VARCHAR(100),
            pattern VARCHAR(255),  -- التفعيلة
            description TEXT,
            example_verse TEXT,
            poems_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Insert the 16 classical Arabic poetry meters
    cursor.execute("""
        INSERT INTO poetry_meters (name_arabic, name_english, pattern, description) VALUES
        ('الطويل', 'Al-Tawil', 'فعولن مفاعيلن فعولن مفاعيلن', 'The longest meter, often used for serious subjects'),
        ('الوافر', 'Al-Wafir', 'مفاعلتن مفاعلتن فعولن', 'Abundant meter, used for various subjects'),
        ('الكامل', 'Al-Kamil', 'متفاعلن متفاعلن متفاعلن', 'Complete meter, very popular'),
        ('البسيط', 'Al-Basit', 'مستفعلن فاعلن مستفعلن فعلن', 'Simple meter, versatile'),
        ('الرجز', 'Al-Rajaz', 'مستفعلن مستفعلن مستفعلن', 'Rajaz meter, easy and flowing'),
        ('الخفيف', 'Al-Khafif', 'فاعلاتن مستفعلن فاعلاتن', 'Light meter'),
        ('المتقارب', 'Al-Mutaqarib', 'فعولن فعولن فعولن فعولن', 'Approaching meter'),
        ('المتدارك', 'Al-Mutadarik', 'فاعلن فاعلن فاعلن فاعلن', 'Catching up meter'),
        ('الهزج', 'Al-Hazaj', 'مفاعيلن مفاعيلن', 'Playful meter'),
        ('الرمل', 'Al-Ramal', 'فاعلاتن فاعلاتن فاعلاتن', 'Sand meter, smooth flow'),
        ('السريع', 'Al-Sari', 'مستفعلن مستفعلن مفعولات', 'Fast meter'),
        ('المنسرح', 'Al-Munsarih', 'مستفعلن مفعولات مستفعلن', 'Flowing meter'),
        ('المضارع', 'Al-Mudari', 'مفاعيل فاعلاتن', 'Similar meter'),
        ('المقتضب', 'Al-Muqtadab', 'مفعولات مستفعلن', 'Brief meter'),
        ('المجتث', 'Al-Mujtath', 'مستفعلن فاعلاتن', 'Uprooted meter'),
        ('المديد', 'Al-Madid', 'فاعلاتن فاعلن فاعلاتن', 'Extended meter')
    """)
    
    # 5. Poets Table
    print("  ✅ Creating poets table...")
    cursor.execute("""
        CREATE TABLE poets (
            poet_id SERIAL PRIMARY KEY,
            name_arabic VARCHAR(255) NOT NULL,
            name_english VARCHAR(255),
            nickname VARCHAR(255),  -- اللقب (e.g., المتنبي، أبو الطيب)
            bio_arabic TEXT,
            bio_english TEXT,
            birth_year INTEGER,
            death_year INTEGER,
            era_id INTEGER REFERENCES poetry_eras(era_id),
            country_id INTEGER REFERENCES poetry_countries(country_id),
            image_url VARCHAR(500),
            wikipedia_url VARCHAR(500),
            poems_count INTEGER DEFAULT 0,
            verses_count INTEGER DEFAULT 0,
            views_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for poets
    cursor.execute("""
        CREATE INDEX idx_poets_era ON poets(era_id);
        CREATE INDEX idx_poets_country ON poets(country_id);
        CREATE INDEX idx_poets_name ON poets USING gin(to_tsvector('arabic', name_arabic));
    """)
    
    # 6. Poems Table
    print("  ✅ Creating poems table...")
    cursor.execute("""
        CREATE TABLE poems (
            poem_id SERIAL PRIMARY KEY,
            poet_id INTEGER REFERENCES poets(poet_id) ON DELETE CASCADE,
            title_arabic VARCHAR(500),
            title_english VARCHAR(500),
            full_text TEXT,  -- Full poem text (all verses concatenated)
            verses_count INTEGER DEFAULT 0,
            meter_id INTEGER REFERENCES poetry_meters(meter_id),
            rhyme_letter VARCHAR(10),  -- حرف القافية
            topic_id INTEGER REFERENCES poetry_topics(topic_id),
            occasion VARCHAR(255),  -- المناسبة
            year_written INTEGER,
            source VARCHAR(255),  -- المصدر (e.g., 'AlDiwan.net', 'GitHub', etc.)
            audio_url VARCHAR(500),
            video_url VARCHAR(500),
            explanation TEXT,  -- شرح القصيدة
            views_count INTEGER DEFAULT 0,
            favorites_count INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for poems
    cursor.execute("""
        CREATE INDEX idx_poems_poet ON poems(poet_id);
        CREATE INDEX idx_poems_meter ON poems(meter_id);
        CREATE INDEX idx_poems_topic ON poems(topic_id);
        CREATE INDEX idx_poems_rhyme ON poems(rhyme_letter);
        CREATE INDEX idx_poems_fulltext ON poems USING gin(to_tsvector('arabic', full_text));
        CREATE INDEX idx_poems_title ON poems USING gin(to_tsvector('arabic', title_arabic));
    """)
    
    # 7. Verses Table (Individual verses/lines)
    print("  ✅ Creating verses table...")
    cursor.execute("""
        CREATE TABLE verses (
            verse_id SERIAL PRIMARY KEY,
            poem_id INTEGER REFERENCES poems(poem_id) ON DELETE CASCADE,
            verse_number INTEGER NOT NULL,  -- Order in poem (1, 2, 3...)
            first_hemistich TEXT,  -- الشطر الأول (first half of verse)
            second_hemistich TEXT,  -- الشطر الثاني (second half)
            full_verse TEXT NOT NULL,  -- Complete verse (both hemistichs)
            explanation TEXT,  -- شرح البيت (explanation of this verse)
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create indexes for verses
    cursor.execute("""
        CREATE INDEX idx_verses_poem ON verses(poem_id);
        CREATE INDEX idx_verses_number ON verses(verse_number);
        CREATE INDEX idx_verses_fulltext ON verses USING gin(to_tsvector('arabic', full_verse));
    """)
    
    # 8. Poetry Favorites (User favorites - optional for future)
    print("  ✅ Creating poetry_favorites table...")
    cursor.execute("""
        CREATE TABLE poetry_favorites (
            favorite_id SERIAL PRIMARY KEY,
            user_id INTEGER,  -- For future user system
            poem_id INTEGER REFERENCES poems(poem_id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    cursor.execute("""
        CREATE INDEX idx_favorites_poem ON poetry_favorites(poem_id);
        CREATE INDEX idx_favorites_user ON poetry_favorites(user_id);
    """)
    
    # Commit all changes
    conn.commit()
    
    print("\n✅ All poetry tables created successfully!")
    print("\n📊 Database Structure:")
    print("  ├── poetry_eras (9 eras)")
    print("  ├── poetry_countries (21 countries)")
    print("  ├── poetry_topics (17 topics)")
    print("  ├── poetry_meters (16 meters)")
    print("  ├── poets (empty - ready for data)")
    print("  ├── poems (empty - ready for data)")
    print("  ├── verses (empty - ready for data)")
    print("  └── poetry_favorites (empty - for future)")
    
    print("\n🔗 Integration with Dictionary:")
    print("  ✅ Same database as dictionary")
    print("  ✅ Can link words in poems to dictionary definitions")
    print("  ✅ Shared infrastructure")
    
    # Verify tables exist
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' AND table_name LIKE 'poet%'
        ORDER BY table_name
    """)
    poetry_tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n✅ Verified {len(poetry_tables)} poetry tables created:")
    for table in poetry_tables:
        print(f"  ✅ {table}")
    
    conn.close()
    return True

if __name__ == '__main__':
    try:
        create_poetry_tables()
        print("\n🎉 Poetry database setup complete!")
        print("📝 Next: Run data extraction script to import poems")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
