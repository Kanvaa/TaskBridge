import os
from urllib.parse import urlparse

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'taskbridge_super_secret_session_key_12345'
    
    db_url = os.environ.get('DATABASE_URL') or os.environ.get('JAWSDB_URL') or os.environ.get('CLEARDB_DATABASE_URL')
    
    if db_url:
        parsed = urlparse(db_url)
        DB_HOST = parsed.hostname
        DB_USER = parsed.username
        DB_PASSWORD = parsed.password
        DB_NAME = parsed.path.lstrip('/')
        DB_PORT = parsed.port or 3306
    else:
        DB_HOST = os.environ.get('DB_HOST') or 'localhost'
        DB_USER = os.environ.get('DB_USER') or 'root'
        DB_PASSWORD = os.environ.get('DB_PASSWORD') or ''
        DB_NAME = os.environ.get('DB_NAME') or 'taskbridge_db'
        DB_PORT = 3306
