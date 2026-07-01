import mysql.connector
import sqlite3
import os
from config import Config

class SQLiteCursorAdapter:
    def __init__(self, sqlite_cursor):
        self.cursor = sqlite_cursor

    def execute(self, query, params=None):
        # Convert %s query placeholders to sqlite ? placeholders
        query = query.replace('%s', '?')
        if params is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, params)
        return self

    @property
    def lastrowid(self):
        return self.cursor.lastrowid

    def fetchone(self):
        row = self.cursor.fetchone()
        if row:
            return dict(row)
        return None

    def fetchall(self):
        rows = self.cursor.fetchall()
        return [dict(r) for r in rows]

    def close(self):
        self.cursor.close()

class SQLiteConnectionAdapter:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.conn.row_factory = sqlite3.Row

    def cursor(self, dictionary=False):
        return SQLiteCursorAdapter(self.conn.cursor())

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()

class DatabaseConnection:
    _instance = None
    use_sqlite = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.config = Config
            # Check if MySQL service is running
            try:
                conn = mysql.connector.connect(
                    host=Config.DB_HOST,
                    user=Config.DB_USER,
                    password=Config.DB_PASSWORD,
                    port=Config.DB_PORT,
                    connect_timeout=2
                )
                conn.close()
                cls._instance.use_sqlite = False
                print("MySQL Service detected. Using MySQL.")
            except Exception:
                cls._instance.use_sqlite = True
                print("MySQL Service not detected. Falling back to local SQLite database (taskbridge.db) for zero-config run.")
        return cls._instance

    def get_connection(self, include_db=True):
        if self.use_sqlite:
            if os.environ.get('VERCEL') == '1' or os.environ.get('NOW_REGION'):
                db_path = '/tmp/taskbridge.db'
            else:
                db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'taskbridge.db')
            return SQLiteConnectionAdapter(db_path)
            
        params = {
            'host': self.config.DB_HOST,
            'user': self.config.DB_USER,
            'password': self.config.DB_PASSWORD,
            'port': self.config.DB_PORT
        }
        if include_db:
            params['database'] = self.config.DB_NAME
        return mysql.connector.connect(**params)
