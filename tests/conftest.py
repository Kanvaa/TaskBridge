import os
import tempfile
import pytest
import sys

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app import create_app, init_db
from database import DatabaseConnection

@pytest.fixture(scope='session', autouse=True)
def setup_test_database():
    # Force database handler to use SQLite fallback for test runner simplicity
    db = DatabaseConnection()
    db.use_sqlite = True
    
    # Configure temporary DB path
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    
    # Patch DatabaseConnection database path retrieval
    original_get_connection = db.get_connection
    def patched_get_connection(include_db=True):
        from database import SQLiteConnectionAdapter
        return SQLiteConnectionAdapter(db_path)
    
    db.get_connection = patched_get_connection
    
    # Initialize the temporary database structure
    init_db()
    
    yield db_path
    
    # Cleanup
    os.close(db_fd)
    try:
        os.unlink(db_path)
    except OSError:
        pass

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SECRET_KEY": "test_secret_key"
    })
    return app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()
