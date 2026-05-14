import sqlite3
from config import Config

class Database:
    def __init__(self):
        self.db_name = Config.DB_NAME
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Initializes database tables for students, sessions, and events."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    student_id TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Create sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER,
                    start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                    end_time DATETIME,
                    FOREIGN KEY (student_id) REFERENCES students (id)
                )
            ''')
            
            # Create events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    event_type TEXT,
                    description TEXT,
                    evidence_path TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            ''')
            conn.commit()

    def register_student(self, name, student_id):
        """Registers a student or fetches their ID if they already exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('INSERT INTO students (name, student_id) VALUES (?, ?)', (name, student_id))
                conn.commit()
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM students WHERE student_id = ?', (student_id,))
                return cursor.fetchone()[0]

    def create_session(self, student_internal_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO sessions (student_id) VALUES (?)', (student_internal_id,))
            conn.commit()
            return cursor.lastrowid

    def end_session(self, session_id):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE sessions SET end_time = CURRENT_TIMESTAMP WHERE session_id = ?', (session_id,))
            conn.commit()

    def log_event(self, session_id, event_type, description, evidence_path=None):
        """Logs a suspicious event to the database."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO events (session_id, event_type, description, evidence_path)
                VALUES (?, ?, ?, ?)
            ''', (session_id, event_type, description, evidence_path))
            conn.commit()
            
    def get_session_events(self, session_id):
        """Retrieves all events for a specific session."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT timestamp, event_type, description, evidence_path FROM events WHERE session_id = ?', (session_id,))
            return cursor.fetchall()
