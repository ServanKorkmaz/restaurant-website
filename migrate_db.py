#!/usr/bin/env python
"""
Database migration script to add new fields to existing tables.
This script safely adds new columns without losing existing data.
"""

import os
import sqlite3
import shutil
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def backup_database(db_path):
    """Create a backup before migration."""
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    logging.info(f"Database backed up to: {backup_path}")
    return backup_path

def migrate_database(db_path='instance/restaurant.db'):
    """Add new columns to existing tables."""
    
    # Check if database exists
    if not os.path.exists(db_path):
        logging.warning(f"Database not found at {db_path}. Migration not needed for new database.")
        return
    
    # Create backup
    backup_path = backup_database(db_path)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check existing columns in menu_items table
        cursor.execute("PRAGMA table_info(menu_items)")
        existing_columns = [col[1] for col in cursor.fetchall()]
        
        # Add new columns to menu_items if they don't exist
        new_columns = [
            ("webp_filename", "VARCHAR(100)"),
            ("thumbnail_filename", "VARCHAR(100)"),
            ("alt_text", "VARCHAR(200)"),
            ("is_published", "BOOLEAN DEFAULT 1"),
            ("is_featured", "BOOLEAN DEFAULT 0"),
            ("position", "INTEGER"),
            ("allergens", "VARCHAR(100)"),
            ("min_pax", "INTEGER"),
            ("features", "JSON")
        ]
        
        for col_name, col_type in new_columns:
            if col_name not in existing_columns:
                try:
                    cursor.execute(f"ALTER TABLE menu_items ADD COLUMN {col_name} {col_type}")
                    logging.info(f"Added column {col_name} to menu_items table")
                except sqlite3.OperationalError as e:
                    if "duplicate column" not in str(e).lower():
                        logging.warning(f"Could not add column {col_name}: {e}")
        
        # Create media table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS media (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_path VARCHAR(255) NOT NULL,
                webp_path VARCHAR(255),
                thumbnail_path VARCHAR(255),
                width INTEGER,
                height INTEGER,
                alt_text VARCHAR(200),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        logging.info("Media table created or verified")
        
        # Create catering_inquiries table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS catering_inquiries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                firma VARCHAR(200) NOT NULL,
                email VARCHAR(120) NOT NULL,
                phone VARCHAR(20) NOT NULL,
                antall_personer INTEGER NOT NULL,
                dato DATE NOT NULL,
                pakke VARCHAR(50),
                leveringsadresse VARCHAR(300),
                kommentar TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                status VARCHAR(20) DEFAULT 'new'
            )
        """)
        logging.info("Catering inquiries table created or verified")
        
        # Update existing menu items with allergen data if description contains it
        cursor.execute("SELECT id, description FROM menu_items WHERE description LIKE '%Allergener:%'")
        items_with_allergens = cursor.fetchall()
        
        for item_id, description in items_with_allergens:
            # Extract allergens from description
            import re
            allergen_match = re.search(r'Allergener?:\s*([0-9,\s]+)', description, re.IGNORECASE)
            if allergen_match:
                allergens = allergen_match.group(1).strip()
                # Update allergens column
                cursor.execute("UPDATE menu_items SET allergens = ? WHERE id = ?", (allergens, item_id))
                logging.info(f"Updated allergens for item {item_id}")
        
        # Commit changes
        conn.commit()
        logging.info("Migration completed successfully!")
        
    except Exception as e:
        logging.error(f"Migration failed: {e}")
        logging.info(f"Restoring from backup: {backup_path}")
        shutil.copy2(backup_path, db_path)
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    # Run migration
    migrate_database()
    
    # Also create backup directory if it doesn't exist
    os.makedirs('backups', exist_ok=True)
    logging.info("Backup directory created/verified")