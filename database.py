import sqlite3
import os
import datetime

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "aegis_flow.db")

def get_connection():
    return sqlite3.connect(DB_FILE)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decisions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        summary TEXT NOT NULL,
        rationale TEXT,
        tags TEXT,
        timestamp TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_symbols (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        type TEXT NOT NULL, -- 'file', 'class', 'function'
        filepath TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS decision_symbol_links (
        decision_id INTEGER,
        symbol_id INTEGER,
        PRIMARY KEY (decision_id, symbol_id),
        FOREIGN KEY (decision_id) REFERENCES decisions(id) ON DELETE CASCADE,
        FOREIGN KEY (symbol_id) REFERENCES code_symbols(id) ON DELETE CASCADE
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hash TEXT NOT NULL UNIQUE,
        author TEXT NOT NULL,
        message TEXT,
        diff_content TEXT NOT NULL,
        timestamp TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS commit_symbol_links (
        commit_id INTEGER,
        symbol_id INTEGER,
        PRIMARY KEY (commit_id, symbol_id),
        FOREIGN KEY (commit_id) REFERENCES commits(id) ON DELETE CASCADE,
        FOREIGN KEY (symbol_id) REFERENCES code_symbols(id) ON DELETE CASCADE
    )
    """)
    
    conn.commit()
    conn.close()

def log_decision(summary, rationale, tags, linked_symbols):
    """Logs an architectural decision and links it to specific code symbols."""
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()
    cursor.execute(
        "INSERT INTO decisions (summary, rationale, tags, timestamp) VALUES (?, ?, ?, ?)",
        (summary, rationale, tags, timestamp)
    )
    decision_id = cursor.lastrowid
    
    for symbol_name, symbol_type, filepath in linked_symbols:
        # Get or create symbol
        cursor.execute("SELECT id FROM code_symbols WHERE name = ?", (symbol_name,))
        row = cursor.fetchone()
        if row:
            symbol_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO code_symbols (name, type, filepath) VALUES (?, ?, ?)",
                (symbol_name, symbol_type, filepath)
            )
            symbol_id = cursor.lastrowid
        
        # Link decision and symbol
        cursor.execute(
            "INSERT OR IGNORE INTO decision_symbol_links (decision_id, symbol_id) VALUES (?, ?)",
            (decision_id, symbol_id)
        )
        
    conn.commit()
    conn.close()
    return decision_id

def log_commit(commit_hash, author, message, diff_content, modified_symbols):
    """Logs a simulated commit and links it to modified symbols."""
    conn = get_connection()
    cursor = conn.cursor()
    
    timestamp = datetime.datetime.now().isoformat()
    try:
        cursor.execute(
            "INSERT INTO commits (hash, author, message, diff_content, timestamp) VALUES (?, ?, ?, ?, ?)",
            (commit_hash, author, message, diff_content, timestamp)
        )
        commit_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Commit already exists
        cursor.execute("SELECT id FROM commits WHERE hash = ?", (commit_hash,))
        commit_id = cursor.fetchone()[0]
        
    for symbol_name, symbol_type, filepath in modified_symbols:
        # Get or create symbol
        cursor.execute("SELECT id FROM code_symbols WHERE name = ?", (symbol_name,))
        row = cursor.fetchone()
        if row:
            symbol_id = row[0]
        else:
            cursor.execute(
                "INSERT INTO code_symbols (name, type, filepath) VALUES (?, ?, ?)",
                (symbol_name, symbol_type, filepath)
            )
            symbol_id = cursor.lastrowid
            
        # Link commit and symbol
        cursor.execute(
            "INSERT OR IGNORE INTO commit_symbol_links (commit_id, symbol_id) VALUES (?, ?)",
            (commit_id, symbol_id)
        )
        
    conn.commit()
    conn.close()
    return commit_id

def clear_db():
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    init_db()
