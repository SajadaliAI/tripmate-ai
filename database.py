import sqlite3
import os

DB_FILE = "tripmate.db"

def get_db_connection():
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ SQLite Connection Error: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                user_query TEXT NOT NULL,
                flight_data TEXT,
                hotel_data TEXT,
                itinerary_data TEXT,
                final_response TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()
        print("✅ Local SQLite Database Initialized Successfully!")
    except Exception as e:
        print(f"❌ Table Creation Error: {e}")
    finally:
        conn.close()

def save_conversation(session_id: str, user_query: str, flight_data: str, hotel_data: str, itinerary_data: str, final_response: str):
    conn = get_db_connection()
    if not conn:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO conversations 
            (session_id, user_query, flight_data, hotel_data, itinerary_data, final_response)
            VALUES (?, ?, ?, ?, ?, ?);
        """, (session_id, user_query, flight_data, hotel_data, itinerary_data, final_response))
        
        inserted_id = cursor.lastrowid
        conn.commit()
        print(f"💾 Conversation Saved (ID: {inserted_id})")
        return inserted_id
    except Exception as e:
        print(f"❌ Save Conversation Error: {e}")
        return None
    finally:
        conn.close()

def get_conversation_history(session_id: str, limit: int = 10):
    conn = get_db_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_query, final_response, created_at 
            FROM conversations 
            WHERE session_id = ? 
            ORDER BY created_at DESC 
            LIMIT ?;
        """, (session_id, limit))
        
        records = [dict(row) for row in cursor.fetchall()]
        return records
    except Exception as e:
        print(f"❌ History Fetch Error: {e}")
        return []
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()