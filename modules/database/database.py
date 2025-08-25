import sqlite3
import os
from datetime import datetime
from ..models import SaleItem
from typing import List, Dict, Optional

class Database:
    def __init__(self, db_path: str = 'sale_tracker.db'):
        """Initialize database connection"""
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self) -> None:
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Table to store sale items
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            item_id INTEGER,
            site TEXT,
            item_name TEXT,
            item_description TEXT,
            item_price REAL,
            item_discounted_price REAL,
            item_url TEXT,
            first_seen TIMESTAMP,
            last_seen TIMESTAMP,
            is_active INTEGER DEFAULT 1,
            PRIMARY KEY (item_id, site)
        )
        ''')
        
        # Table to store historical price data
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER,
            site TEXT,
            price REAL,
            discounted_price REAL,
            timestamp TIMESTAMP,
            FOREIGN KEY (item_id, site) REFERENCES sale_items(item_id, site)
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def compare_against_db(self, sale_items: List[SaleItem], site: str) -> List[SaleItem]:
        """
        Compare new sale items against existing items in the database.
        Return only new or price-changed items.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        new_items = []
        
        # Update all items as inactive initially
        cursor.execute(
            "UPDATE sale_items SET is_active = 0 WHERE site = ?",
            (site,)
        )
        
        for item in sale_items:
            cursor.execute(
                "SELECT item_id, item_price, item_discounted_price FROM sale_items WHERE item_id = ? AND site = ?",
                (item['item_id'], site)
            )
            result = cursor.fetchone()
            if result:
                old_discounted_price = result[2]
                old_price = result[1]
                cursor.execute(
                    "UPDATE sale_items SET is_active = 1, last_seen = ? WHERE item_id = ? AND site = ?",
                    (now, item['item_id'], site)
                )

                if item['item_discounted_price'] < old_discounted_price:
                    new_items.append(item)
                
                if item['item_discounted_price'] != old_discounted_price or item['item_price'] != old_price:
                    cursor.execute(
                        "INSERT INTO price_history (item_id, site, price, discounted_price, timestamp) VALUES (?, ?, ?, ?, ?)",
                        (item['item_id'], site, item['item_price'], item['item_discounted_price'], now)
                    )
                    cursor.execute(
                        "UPDATE sale_items SET item_price = ?, item_discounted_price = ? WHERE item_id = ? AND site = ?",
                        (item['item_price'], item['item_discounted_price'], item['item_id'], site)
                    )
            else:
                cursor.execute(
                    """
                    INSERT INTO sale_items (item_id, site, item_name, item_description, item_price, item_discounted_price, item_url, first_seen, last_seen, is_active)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1)
                    """,
                    (item['item_id'], site, item['item_name'], item['item_description'], item['item_price'], item['item_discounted_price'], item['item_url'], now, now)
                )
                cursor.execute(
                    "INSERT INTO price_history (item_id, site, price, discounted_price, timestamp) VALUES (?, ?, ?, ?, ?)",
                    (item['item_id'], site, item['item_price'], item['item_discounted_price'], now)
                )
                new_items.append(item)

        for item in new_items:
            # Ensure metadata dictionary exists
            if not hasattr(item, 'metadata'):
                item['metadata'] = {}
            elif item['metadata'] is None:
                item['metadata'] = {}
                
            cursor.execute(
                """
                SELECT price, discounted_price, timestamp FROM price_history 
                WHERE item_id = ? AND site = ? 
                ORDER BY timestamp DESC
                """,
                (item['item_id'], site)
            )
            
            price_history = [
                {'item_price': row[0], 'item_discounted_price': row[1], 'timestamp': row[2]} 
                for row in cursor.fetchall()
            ]
            
            item['metadata']['price_history'] = price_history
    
        conn.commit()
        conn.close()
            
        return new_items