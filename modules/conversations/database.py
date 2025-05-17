# modules/conversations/database.py
import sqlite3
import json
from datetime import datetime
import os

class MessageDatabase:
    def __init__(self, db_path="data/conversations.db"):
        # Ensure directory exists
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Create database tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone_number TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            referenced_items TEXT
        )
        ''')
        
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_phone ON messages(phone_number)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp, phone_number)')
        
        conn.commit()
        conn.close()
    
    def store_message(self, phone_number, role, content, referenced_items=None):
        """Store a message in the database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        timestamp = datetime.now().isoformat()
        ref_items_json = json.dumps(referenced_items) if referenced_items else None
        
        cursor.execute(
            "INSERT INTO messages (phone_number, timestamp, role, content, referenced_items) VALUES (?, ?, ?, ?, ?)",
            (phone_number, timestamp, role, content, ref_items_json)
        )
        
        conn.commit()
        conn.close()
    
    def get_conversation_history(self, phone_number, limit=10):
        """Get the most recent messages for a user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp, referenced_items FROM messages WHERE phone_number = ? ORDER BY timestamp DESC LIMIT ?",
            (phone_number, limit)
        )
        
        # Convert to list of dicts and reverse to get chronological order
        rows = [dict(row) for row in cursor.fetchall()]
        messages = list(reversed(rows))
        
        conn.close()
        return messages
    
    def get_last_system_message(self, phone_number):
        """Get the most recent system message for a user"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT role, content, timestamp, referenced_items FROM messages WHERE phone_number = ? AND role = 'system' ORDER BY timestamp DESC LIMIT 1",
            (phone_number,)
        )
        
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None