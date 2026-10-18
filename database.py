import sqlite3
from datetime import datetime

DB_PATH = "tickets.db"

def init_db():
    """Creates the tickets table if it doesn't exist yet."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            sender     TEXT NOT NULL,
            subject    TEXT,
            body       TEXT NOT NULL,
            category   TEXT,
            urgency    TEXT,
            reasoning  TEXT,
            draft      TEXT,
            approved   INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

def save_ticket(sender, subject, body):
    """Saves a new incoming ticket and returns its ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tickets (sender, subject, body) VALUES (?, ?, ?)",
        (sender, subject, body)
    )
    ticket_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return ticket_id

def update_classification(ticket_id, category, urgency, reasoning):
    """Saves the classifier agent's output."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET category=?, urgency=?, reasoning=? WHERE id=?",
        (category, urgency, reasoning, ticket_id)
    )
    conn.commit()
    conn.close()

def update_draft(ticket_id, draft):
    """Saves the specialist agent's draft response."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET draft=? WHERE id=?",
        (draft, ticket_id)
    )
    conn.commit()
    conn.close()

def approve_ticket(ticket_id):
    """Marks a ticket as approved by the human."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tickets SET approved=1 WHERE id=?",
        (ticket_id,)
    )
    conn.commit()
    conn.close()

def get_all_tickets():
    """Returns all tickets, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # lets us use ticket["column"] syntax
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_ticket(ticket_id):
    """Returns a single ticket by its ID."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tickets WHERE id=?", (ticket_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None