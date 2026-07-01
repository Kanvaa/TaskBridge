from models.base import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    def __init__(self, username, email, password_hash=None, user_id=None):
        self.id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            if self.id is None:
                query = "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)"
                cursor.execute(query, (self.username, self.email, self.password_hash))
                self.id = cursor.lastrowid
            else:
                query = "UPDATE users SET username = %s, email = %s, password_hash = %s WHERE id = %s"
                cursor.execute(query, (self.username, self.email, self.password_hash, self.id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.id is not None:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            try:
                query = "DELETE FROM users WHERE id = %s"
                cursor.execute(query, (self.id,))
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    @classmethod
    def find_by_id(cls, user_id):
        conn = cls.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE id = %s"
            cursor.execute(query, (user_id,))
            row = cursor.fetchone()
            if row:
                return cls(row['username'], row['email'], row['password_hash'], row['id'])
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def find_by_username(cls, username):
        conn = cls.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            row = cursor.fetchone()
            if row:
                return cls(row['username'], row['email'], row['password_hash'], row['id'])
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def find_by_email(cls, email):
        conn = cls.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            row = cursor.fetchone()
            if row:
                return cls(row['username'], row['email'], row['password_hash'], row['id'])
            return None
        finally:
            cursor.close()
            conn.close()
