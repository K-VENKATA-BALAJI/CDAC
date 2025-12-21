import sqlite3
import json
import os
from datetime import datetime

class Database:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), 'pcb_data.db')
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                file_name TEXT,
                file_description TEXT,
                specifications TEXT,
                vendors TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def save_user_data(self, email, file_name, file_description, specifications, vendors):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO user_files (email, file_name, file_description, specifications, vendors)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            email,
            file_name,
            file_description,
            json.dumps(specifications),
            json.dumps(vendors)
        ))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_user_data(self, email):
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT file_name, file_description, specifications, vendors, created_at
            FROM user_files
            WHERE email = ?
            ORDER BY created_at DESC
        ''', (email,))
        
        rows = cursor.fetchall()
        if not rows:
            return None
        
        # Return all files for the email
        files = []
        for row in rows:
            files.append({
                "file_name": row[0],
                "file_description": row[1],
                "specifications": json.loads(row[2]) if row[2] else {},
                "vendors": json.loads(row[3]) if row[3] else [],
                "created_at": row[4]
            })
        
        return files


