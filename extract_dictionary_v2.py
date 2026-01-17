#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
القاموس المحيط Dictionary Extraction System V2
============================================

Multi-dictionary extraction tool for converting HTML dictionaries
into a structured SQLite database for Flutter integration.

Author: Dictionary Extraction System
Date: November 2025
Version: 2.0.0 - Multi-Dictionary Support
"""

import sys
import os
import sqlite3
import re
import logging
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from bs4 import BeautifulSoup, Tag
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('extraction.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    """Represents a باب (chapter) in the dictionary"""
    name: str
    order: int
    dictionary_id: int
    chapter_id: Optional[int] = None


@dataclass
class Section:
    """Represents a فصل (section) within a chapter"""
    name: str
    chapter_id: int
    dictionary_id: int
    order: int
    section_id: Optional[int] = None


@dataclass
class Entry:
    """Represents a dictionary entry"""
    root: str
    headword: str
    headword_normalized: str
    pattern_ref: Optional[str]
    is_unique: bool
    page_number: int
    section_id: int
    dictionary_id: int
    entry_order: int
    full_text: str
    entry_id: Optional[int] = None


@dataclass
class Definition:
    """Represents a definition within an entry"""
    entry_id: int
    definition_text: str
    definition_order: int


class ArabicTextNormalizer:
    """Handles Arabic text normalization (removing diacritics)"""
    
    # Arabic diacritical marks (Tashkeel)
    DIACRITICS = [
        '\u064B',  # Tanween Fath
        '\u064C',  # Tanween Damm
        '\u064D',  # Tanween Kasr
        '\u064E',  # Fatha
        '\u064F',  # Damma
        '\u0650',  # Kasra
        '\u0651',  # Shadda
        '\u0652',  # Sukun
        '\u0653',  # Maddah
        '\u0654',  # Hamza Above
        '\u0655',  # Hamza Below
        '\u0656',  # Subscript Alef
        '\u0657',  # Inverted Damma
        '\u0658',  # Mark Noon Ghunna
        '\u0670',  # Superscript Alef
    ]
    
    @staticmethod
    def normalize(text: str) -> str:
        """Remove diacritics from Arabic text and normalize characters"""
        if not text:
            return ""
        
        # Remove diacritics
        for diacritic in ArabicTextNormalizer.DIACRITICS:
            text = text.replace(diacritic, '')
        
        # Normalize hamza variations
        text = text.replace('أ', 'ا').replace('إ', 'ا').replace('آ', 'ا')
        
        # Normalize taa marbuta and alef maksura
        text = text.replace('ة', 'ه').replace('ى', 'ي')
        
        return text.strip()


class HTMLParser:
    """Parses the HTML dictionary file"""
    
    def __init__(self, html_path: str):
        self.html_path = Path(html_path)
        self.soup: Optional[BeautifulSoup] = None
        self.raw_html: Optional[str] = None
    
    def load(self) -> BeautifulSoup:
        """Load and parse the HTML file"""
        logger.info(f"Loading HTML file: {self.html_path}")
        
        with open(self.html_path, 'r', encoding='utf-8') as f:
            self.raw_html = f.read()
        
        self.soup = BeautifulSoup(self.raw_html, 'lxml')
        logger.info(f"HTML file loaded: {len(self.raw_html):,} characters")
        
        return self.soup
    
    def extract_page_blocks(self) -> List[Tag]:
        """Extract all PageText div blocks"""
        if not self.soup:
            raise RuntimeError("HTML not loaded. Call load() first.")
        
        blocks = self.soup.find_all('div', class_='PageText')
        logger.info(f"Found {len(blocks)} page blocks")
        
        return blocks
    
    @staticmethod
    def extract_page_number(page_block: Tag) -> Optional[int]:
        """Extract page number from a page block"""
        page_head = page_block.find('div', class_='PageHead')
        if page_head:
            text = page_head.get_text()
            # Extract number from (ص: 123) format
            match = re.search(r'\(ص:\s*(\d+)\)', text)
            if match:
                return int(match.group(1))
        return None
    
    @staticmethod
    def find_chapters_and_sections(page_block: Tag) -> Tuple[List[str], List[str]]:
        """
        Find all chapter (باب) and section (فصل) markers in a page block
        Returns: (chapters, sections)
        """
        chapters = []
        sections = []
        
        # Find all red title spans
        # Use attrs instead of class_ to handle special cases
        title_spans = page_block.find_all('span', attrs={'class': 'title'})
        
        for span in title_spans:
            text = span.get_text().strip()
            # Remove zero-width characters (U+200C ZWNJ, U+200D ZWJ, etc.)
            text = text.replace('\u200c', '').replace('\u200d', '').replace('\u200b', '').replace('\ufeff', '').strip()
            
            # Normalize text for matching (remove diacritics)
            normalized = ArabicTextNormalizer.normalize(text)
            
            # More flexible matching - check if text contains the markers
            if 'باب' in normalized:
                chapters.append(text)
                logger.debug(f"Found chapter: {text}")
            elif 'فصل' in normalized:
                sections.append(text)
                logger.debug(f"Found section: {text}")
        
        return chapters, sections
    
    @staticmethod
    def extract_entries(page_block: Tag, current_section_id: int, page_number: int) -> List[str]:
        """
        Extract all entries from a page block
        Entries are separated by:
        - Bullet points (•) in القاموس المحيط
        - </p>( pattern in المعجم الوسيط (detected from raw HTML)
        """
        entries = []
        
        # Get text and check for bullet points (القاموس المحيط style)
        text = page_block.get_text()
        if '•' in text:
            parts = text.split('•')
            
            for part in parts:
                part = part.strip()
                
                # Skip empty parts
                if not part:
                    continue
                
                # Skip page headers
                if 'القاموس المحيط' in part or 'المعجم الوسيط' in part:
                    continue
                if part.startswith('(ص:'):  # Skip page numbers
                    continue
                    
                # Valid entry should have some content
                if len(part) > 10:
                    entries.append(part)
        
        return entries
    
    @staticmethod
    def extract_entries_from_raw_html(raw_html_block: str) -> List[str]:
        """
        Extract entries directly from raw HTML (for المعجم الوسيط)
        Entries are marked by </p>( pattern in the raw HTML
        """
        entries = []
        
        # Split by </p>( pattern
        parts = raw_html_block.split('</p>(')
        
        for i, part in enumerate(parts):
            if i == 0:
                # First part is page header
                continue
            
            # Add back the opening paren
            part_html = '(' + part
            
            # Extract text from HTML
            # Find the next </p> or end of part
            end_idx = part_html.find('</p>')
            if end_idx > 0:
                entry_html = part_html[:end_idx]
            else:
                entry_html = part_html
            
            # Clean HTML tags
            clean_text = BeautifulSoup(entry_html, 'lxml').get_text().strip()
            
            # Skip empty or invalid entries
            if not clean_text or len(clean_text) < 15:
                continue
            
            # Skip page numbers
            if clean_text.startswith('(ص:'):
                continue
            
            # Valid entry
            if clean_text.startswith('('):
                entries.append(clean_text)
        
        return entries


class EntryParser:
    """Parses individual dictionary entries"""
    
    # Pattern references regex
    PATTERN_REGEX = re.compile(r'ك(?:َ)?([^،\s]+)')
    
    # Plural marker regex
    PLURAL_REGEX = re.compile(r'ج:\s*([^،\.]+)')
    
    # Place markers
    PLACE_MARKERS = {
        'ع': 'place',
        'د': 'country',
        'ة': 'village',
        'م': 'famous'
    }
    
    @staticmethod
    def parse_headword(entry_text: str) -> Tuple[str, Optional[str]]:
        """
        Parse headword and pattern reference from entry text
        Returns: (headword, pattern_ref)
        """
        # Extract text within first set of parentheses
        match = re.match(r'\(([^\)]+)\)', entry_text)
        if not match:
            # No parentheses, take first word
            words = entry_text.split()
            return (words[0] if words else entry_text[:20], None)
        
        headword_part = match.group(1)
        
        # Check for pattern reference (ك + word)
        pattern_match = EntryParser.PATTERN_REGEX.search(headword_part)
        pattern_ref = pattern_match.group(1) if pattern_match else None
        
        # Clean headword (remove pattern reference)
        headword = re.sub(r'ك(?:َ)?[^،\s]+', '', headword_part).strip()
        headword = headword.replace(':', '').replace('،', '').strip()
        
        return (headword, pattern_ref)
    
    @staticmethod
    def extract_plurals(entry_text: str) -> List[str]:
        """Extract all plural forms from entry text"""
        plurals = []
        
        for match in EntryParser.PLURAL_REGEX.finditer(entry_text):
            plural_part = match.group(1)
            # Split by 'و' (and) to get multiple plurals
            for plural in plural_part.split('و'):
                plural = plural.strip()
                if plural:
                    plurals.append(plural)
        
        return plurals
    
    @staticmethod
    def extract_definitions(entry_text: str) -> List[str]:
        """
        Extract definitions from entry text
        This is simplified - real parsing would be more sophisticated
        """
        # Remove headword part (before first colon)
        parts = entry_text.split(':', 1)
        if len(parts) < 2:
            return [entry_text]
        
        definition_part = parts[1]
        
        # Split by common separators
        definitions = re.split(r'،\s*و', definition_part)
        
        return [d.strip() for d in definitions if d.strip()]
    
    @staticmethod
    def is_unique_entry(entry_text: str) -> bool:
        """
        Check if entry is marked as unique to this dictionary
        (entries in red that are not chapter/section headers)
        """
        # This would need access to the HTML tag
        # For now, return False - will be enhanced in integration
        return False
    
    @staticmethod
    def extract_markers(entry_text: str) -> Dict[str, List[str]]:
        """Extract place/type markers (ع، د، ة، م)"""
        markers = {marker_type: [] for marker_type in EntryParser.PLACE_MARKERS.values()}
        
        # Simple approach: look for marker symbols followed by text
        for symbol, marker_type in EntryParser.PLACE_MARKERS.items():
            # Find occurrences of the symbol
            if symbol in entry_text:
                # This is simplified - would need more sophisticated parsing
                markers[marker_type].append(f"Contains {symbol} marker")
        
        return markers


class DatabaseManager:
    """Manages SQLite database creation and operations"""
    
    def __init__(self, db_path: str):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None
    
    def connect(self):
        """Connect to database"""
        logger.info(f"Connecting to database: {self.db_path}")
        self.conn = sqlite3.connect(str(self.db_path))
        self.cursor = self.conn.cursor()
        
        # Enable foreign keys
        self.cursor.execute("PRAGMA foreign_keys = ON")
        
        logger.info("Database connection established")
    
    def insert_chapter(self, chapter: Chapter) -> int:
        """Insert a chapter and return its ID"""
        self.cursor.execute(
            "INSERT INTO chapters (name_arabic, chapter_order, dictionary_id) VALUES (?, ?, ?)",
            (chapter.name, chapter.order, chapter.dictionary_id)
        )
        return self.cursor.lastrowid
    
    def insert_section(self, section: Section) -> int:
        """Insert a section and return its ID"""
        self.cursor.execute(
            "INSERT INTO sections (chapter_id, name_arabic, section_order, dictionary_id) VALUES (?, ?, ?, ?)",
            (section.chapter_id, section.name, section.order, section.dictionary_id)
        )
        return self.cursor.lastrowid
    
    def insert_entry(self, entry: Entry) -> int:
        """Insert an entry and return its ID"""
        self.cursor.execute(
            """INSERT INTO entries 
               (section_id, root, headword, headword_normalized, pattern_ref, 
                is_unique, page_number, entry_order, full_text, dictionary_id)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (entry.section_id, entry.root, entry.headword, entry.headword_normalized,
             entry.pattern_ref, entry.is_unique, entry.page_number, entry.entry_order,
             entry.full_text, entry.dictionary_id)
        )
        return self.cursor.lastrowid
    
    def insert_definition(self, definition: Definition):
        """Insert a definition"""
        self.cursor.execute(
            "INSERT INTO definitions (entry_id, definition_text, definition_order) VALUES (?, ?, ?)",
            (definition.entry_id, definition.definition_text, definition.definition_order)
        )
    
    def insert_plural(self, entry_id: int, plural_form: str, order: int):
        """Insert a plural form"""
        self.cursor.execute(
            "INSERT INTO plurals (entry_id, plural_form, plural_order) VALUES (?, ?, ?)",
            (entry_id, plural_form, order)
        )
    
    def insert_marker(self, entry_id: int, marker_type: str, marker_text: str):
        """Insert a marker"""
        self.cursor.execute(
            "INSERT INTO markers (entry_id, marker_type, marker_text) VALUES (?, ?, ?)",
            (entry_id, marker_type, marker_text)
        )
    
    def set_metadata(self, key: str, value: str):
        """Set metadata value"""
        self.cursor.execute(
            "INSERT OR REPLACE INTO metadata (key, value, updated_at) VALUES (?, ?, ?)",
            (key, value, datetime.now().isoformat())
        )
    
    def commit(self):
        """Commit transaction"""
        self.conn.commit()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")


class DictionaryExtractor:
    """Main extraction orchestrator"""
    
    def __init__(self, db_path: str, dictionary_id: int):
        self.db_path = db_path
        self.dictionary_id = dictionary_id
        self.db = DatabaseManager(db_path)
        self.normalizer = ArabicTextNormalizer()
        
        # State tracking
        self.current_chapter_id: Optional[int] = None
        self.current_section_id: Optional[int] = None
        self.chapter_counter = 0
        self.section_counter = 0
        self.entry_counter = 0
        
        # Statistics
        self.stats = {
            'total_pages': 0,
            'total_chapters': 0,
            'total_sections': 0,
            'total_entries': 0,
            'total_definitions': 0,
            'total_plurals': 0,
            'errors': 0
        }
    
    def process_html_file(self, html_path: str):
        """Process a single HTML file"""
        logger.info(f"Processing HTML file: {html_path}")
        
        parser = HTMLParser(html_path)
        parser.load()
        
        # Extract all page blocks
        page_blocks = parser.extract_page_blocks()
        
        # Check if this is المعجم الوسيط (no bullet points)
        is_alwaseet = True
        for block in page_blocks[:5]:
            if '•' in block.get_text():
                is_alwaseet = False
                break
        
        # Process each page block
        if is_alwaseet and parser.raw_html:
            # For المعجم الوسيط, work with raw HTML blocks
            raw_blocks = parser.raw_html.split("<div class='PageText'>")
            
            for i, soup_block in enumerate(page_blocks):
                if i + 1 < len(raw_blocks):
                    raw_block = "<div class='PageText'>" + raw_blocks[i + 1]
                    self.process_page_block_raw(soup_block, raw_block, parser)
        else:
            # For القاموس المحيط, use normal processing
            for block in page_blocks:
                self.process_page_block(block, parser)
    
    def process_page_block(self, page_block: Tag, parser: HTMLParser):
        """Process a single page block (for القاموس المحيط with bullet points)"""
        self.stats['total_pages'] += 1
        
        # Extract page number
        page_number = parser.extract_page_number(page_block)
        
        # Find chapters and sections in this block
        chapters, sections = parser.find_chapters_and_sections(page_block)
        
        # Handle chapters
        for chapter_name in chapters:
            self.process_chapter(chapter_name)
        
        # Handle sections (explicit section markers override default)
        for section_name in sections:
            self.process_section(section_name)
        
        # If we have a current section, extract entries
        if self.current_section_id:
            entries = parser.extract_entries(page_block, self.current_section_id, page_number or 0)
            
            for order, entry_text in enumerate(entries, 1):
                try:
                    self.process_entry(entry_text, page_number or 0, order)
                except Exception as e:
                    logger.error(f"Error processing entry: {e}")
                    self.stats['errors'] += 1
    
    def process_page_block_raw(self, page_block: Tag, raw_html: str, parser: HTMLParser):
        """Process a single page block using raw HTML (for المعجم الوسيط)"""
        self.stats['total_pages'] += 1
        
        # Extract page number from parsed block
        page_number = parser.extract_page_number(page_block)
        
        # Find chapters and sections in this block
        chapters, sections = parser.find_chapters_and_sections(page_block)
        
        # Handle chapters
        for chapter_name in chapters:
            self.process_chapter(chapter_name)
        
        # Handle sections (explicit section markers override default)
        for section_name in sections:
            self.process_section(section_name)
        
        # If we have a current section, extract entries from raw HTML
        if self.current_section_id:
            entries = parser.extract_entries_from_raw_html(raw_html)
            
            for order, entry_text in enumerate(entries, 1):
                try:
                    self.process_entry(entry_text, page_number or 0, order)
                except Exception as e:
                    logger.error(f"Error processing entry: {e}")
                    self.stats['errors'] += 1
    
    def process_chapter(self, chapter_name: str):
        """Process a chapter marker"""
        self.chapter_counter += 1
        
        chapter = Chapter(
            name=chapter_name,
            order=self.chapter_counter,
            dictionary_id=self.dictionary_id
        )
        
        self.current_chapter_id = self.db.insert_chapter(chapter)
        self.stats['total_chapters'] += 1
        
        # Reset section tracking for new chapter
        self.current_section_id = None
        self.section_counter = 0
        
        logger.info(f"Chapter {self.chapter_counter}: {chapter_name}")
        
        # Auto-create a default section for this chapter
        # This handles dictionaries that don't have explicit section markers
        default_section_name = f"القسم الأول"  # "First Section"
        section = Section(
            chapter_id=self.current_chapter_id,
            name=default_section_name,
            order=1,
            dictionary_id=self.dictionary_id
        )
        self.current_section_id = self.db.insert_section(section)
        self.section_counter += 1
        self.stats['total_sections'] += 1
        logger.debug(f"Auto-created default section for chapter {self.chapter_counter}")
    
    def process_section(self, section_name: str):
        """Process a section marker"""
        if not self.current_chapter_id:
            logger.warning(f"Section '{section_name}' found without chapter, creating default")
            self.process_chapter("باب افتراضي")
        
        self.section_counter += 1
        
        section = Section(
            name=section_name,
            chapter_id=self.current_chapter_id,
            dictionary_id=self.dictionary_id,
            order=self.section_counter
        )
        
        self.current_section_id = self.db.insert_section(section)
        self.stats['total_sections'] += 1
        
        logger.debug(f"Section {self.section_counter}: {section_name}")
    
    def process_entry(self, entry_text: str, page_number: int, order: int):
        """Process a single entry text"""
        # Parse headword
        headword, pattern_ref = EntryParser.parse_headword(entry_text)
        
        # Determine root (simplified - use headword)
        root = headword
        
        # Normalize headword
        headword_normalized = self.normalizer.normalize(headword)
        
        # Create entry
        entry = Entry(
            root=root,
            headword=headword,
            headword_normalized=headword_normalized,
            pattern_ref=pattern_ref,
            is_unique=False,
            page_number=page_number,
            section_id=self.current_section_id,
            dictionary_id=self.dictionary_id,
            entry_order=order,
            full_text=entry_text
        )
        
        # Insert entry
        entry_id = self.db.insert_entry(entry)
        self.entry_counter += 1
        self.stats['total_entries'] += 1
        
        # Extract and insert definitions
        definitions = EntryParser.extract_definitions(entry_text)
        for def_order, def_text in enumerate(definitions, 1):
            definition = Definition(
                entry_id=entry_id,
                definition_text=def_text,
                definition_order=def_order
            )
            self.db.insert_definition(definition)
            self.stats['total_definitions'] += 1
        
        # Extract and insert plurals
        plurals = EntryParser.extract_plurals(entry_text)
        for plural_order, plural_form in enumerate(plurals, 1):
            self.db.insert_plural(entry_id, plural_form, plural_order)
            self.stats['total_plurals'] += 1
        
        # Extract and insert markers
        markers = EntryParser.extract_markers(entry_text)
        for marker_type, marker_texts in markers.items():
            for marker_text in marker_texts:
                self.db.insert_marker(entry_id, marker_type, marker_text)
    
    def save_metadata(self, source_files: List[str]):
        """Save extraction metadata"""
        self.db.set_metadata(f'extraction_date_dict_{self.dictionary_id}', datetime.now().isoformat())
        self.db.set_metadata(f'source_files_dict_{self.dictionary_id}', ','.join(source_files))
        self.db.set_metadata(f'total_pages_dict_{self.dictionary_id}', str(self.stats['total_pages']))
        self.db.set_metadata(f'total_chapters_dict_{self.dictionary_id}', str(self.stats['total_chapters']))
        self.db.set_metadata(f'total_sections_dict_{self.dictionary_id}', str(self.stats['total_sections']))
        self.db.set_metadata(f'total_entries_dict_{self.dictionary_id}', str(self.stats['total_entries']))
    
    def print_statistics(self):
        """Print extraction statistics"""
        print("\n" + "=" * 80)
        print(f"EXTRACTION STATISTICS - Dictionary ID: {self.dictionary_id}")
        print("=" * 80)
        print(f"Total Pages Processed:    {self.stats['total_pages']:,}")
        print(f"Total Chapters Created:   {self.stats['total_chapters']:,}")
        print(f"Total Sections Created:   {self.stats['total_sections']:,}")
        print(f"Total Entries Extracted:  {self.stats['total_entries']:,}")
        print(f"Total Definitions:        {self.stats['total_definitions']:,}")
        print(f"Total Plurals:            {self.stats['total_plurals']:,}")
        print(f"Errors Encountered:       {self.stats['errors']:,}")
        print("=" * 80)
        print(f"\nDatabase saved to: {self.db_path}")
        print("=" * 80 + "\n")
    
    def run(self, html_files: List[str]):
        """Execute the complete extraction process"""
        logger.info("=" * 80)
        logger.info(f"Starting Dictionary Extraction - Dictionary ID: {self.dictionary_id}")
        logger.info("=" * 80)
        
        try:
            # Step 1: Connect to database
            logger.info("Step 1: Connecting to database...")
            self.db.connect()
            
            # Step 2: Process all HTML files
            logger.info(f"Step 2: Processing {len(html_files)} HTML file(s)...")
            for html_file in html_files:
                self.process_html_file(html_file)
            
            # Step 3: Save metadata
            logger.info("Step 3: Saving metadata...")
            self.save_metadata(html_files)
            
            # Step 4: Commit and close
            logger.info("Step 4: Finalizing...")
            self.db.commit()
            self.db.close()
            
            # Step 5: Print statistics
            self.print_statistics()
            
            logger.info("=" * 80)
            logger.info("Extraction completed successfully!")
            logger.info("=" * 80)
            
        except Exception as e:
            logger.error(f"Extraction failed: {e}", exc_info=True)
            raise


def main():
    """Main entry point for extracting المعجم الوسيط (alwaseet)"""
    
    # Configuration for المعجم الوسيط
    HTML_FILES = [
        r"c:\python apps\arabic_qamoos\data\alwaseet1.htm",
        r"c:\python apps\arabic_qamoos\data\alwaseet2.htm"
    ]
    DB_FILE = r"c:\python apps\arabic_qamoos\qamoos_database.sqlite"
    DICTIONARY_ID = 2  # المعجم الوسيط
    
    # Verify HTML files exist
    for html_file in HTML_FILES:
        if not os.path.exists(html_file):
            print(f"Error: HTML file not found: {html_file}")
            sys.exit(1)
    
    # Verify database exists
    if not os.path.exists(DB_FILE):
        print(f"Error: Database not found: {DB_FILE}")
        print("Please run migration first: python migrate_to_multi_dictionary.py")
        sys.exit(1)
    
    print("\n" + "=" * 80)
    print("Al-Mu'jam Al-Waseet Extraction")
    print("=" * 80)
    print(f"\nFiles to process:")
    for i, html_file in enumerate(HTML_FILES, 1):
        print(f"   {i}. {Path(html_file).name}")
    print(f"\nDatabase: {Path(DB_FILE).name}")
    print(f"Dictionary ID: {DICTIONARY_ID}")
    print()
    
    response = input("Continue with extraction? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("\nExtraction cancelled")
        sys.exit(0)
    
    print()
    
    # Create extractor and run
    extractor = DictionaryExtractor(DB_FILE, DICTIONARY_ID)
    extractor.run(HTML_FILES)
    
    print("\nAl-Mu'jam Al-Waseet successfully extracted!")
    print(f"   Database now contains 2 dictionaries")
    print()


if __name__ == "__main__":
    main()
