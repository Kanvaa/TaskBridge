import os
from flask import Flask, redirect, url_for
from config import Config
from database import DatabaseConnection
from routes.auth import auth_bp
from routes.tasks import tasks_bp

def init_db():
    db = DatabaseConnection()
    try:
        if db.use_sqlite:
            conn = db.get_connection()
            cursor = conn.cursor()
            schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                statements = schema_sql.split(';')
                for statement in statements:
                    clean_stmt = statement.strip()
                    if not clean_stmt:
                        continue
                    if "CREATE DATABASE" in clean_stmt or "USE " in clean_stmt:
                        continue
                    clean_stmt = clean_stmt.replace("INT AUTO_INCREMENT PRIMARY KEY", "INTEGER PRIMARY KEY AUTOINCREMENT")
                    cursor.execute(clean_stmt)
                conn.commit()
            cursor.close()
            conn.close()
            print("SQLite Database initialized successfully.")
            return

        # Connect without specifying database to create it if missing
        conn = db.get_connection(include_db=False)
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Config.DB_NAME}")
        conn.commit()
        cursor.close()
        conn.close()
        
        # Connect to specific database to load tables
        conn = db.get_connection(include_db=True)
        cursor = conn.cursor()
        
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r') as f:
                schema_sql = f.read()
            
            # Simple SQL execution by splitting semicolon
            statements = schema_sql.split(';')
            for statement in statements:
                clean_stmt = statement.strip()
                if clean_stmt:
                    cursor.execute(clean_stmt)
            conn.commit()
        cursor.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Warning: Database initialization skipped/failed: {str(e)}")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Boot Database
    init_db()

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect(url_for('tasks.dashboard'))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
