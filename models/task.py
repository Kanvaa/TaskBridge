from models.base import BaseModel

class Task(BaseModel):
    def __init__(self, title, description, status='Pending', priority='Medium', due_date=None, user_id=None, task_id=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.user_id = user_id

    @property
    def due_date_str(self):
        if self.due_date:
            try:
                return self.due_date.strftime('%Y-%m-%d')
            except AttributeError:
                return str(self.due_date)
        return ''

    def save(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            # Handle empty string or null due_date
            due = self.due_date if self.due_date else None
            if self.id is None:
                query = """
                    INSERT INTO tasks (title, description, status, priority, due_date, user_id) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, (self.title, self.description, self.status, self.priority, due, self.user_id))
                self.id = cursor.lastrowid
            else:
                query = """
                    UPDATE tasks 
                    SET title = %s, description = %s, status = %s, priority = %s, due_date = %s, user_id = %s 
                    WHERE id = %s
                """
                cursor.execute(query, (self.title, self.description, self.status, self.priority, due, self.user_id, self.id))
            conn.commit()
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        if self.id is not None:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            try:
                query = "DELETE FROM tasks WHERE id = %s"
                cursor.execute(query, (self.id,))
                conn.commit()
            finally:
                cursor.close()
                conn.close()

    @classmethod
    def find_by_id(cls, task_id):
        conn = cls.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM tasks WHERE id = %s"
            cursor.execute(query, (task_id,))
            row = cursor.fetchone()
            if row:
                return cls(
                    row['title'], row['description'], row['status'], 
                    row['priority'], row['due_date'], row['user_id'], row['id']
                )
            return None
        finally:
            cursor.close()
            conn.close()

    @classmethod
    def find_by_user(cls, user_id, status=None, priority=None):
        conn = cls.db.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            query = "SELECT * FROM tasks WHERE user_id = %s"
            params = [user_id]
            if status:
                query += " AND status = %s"
                params.append(status)
            if priority:
                query += " AND priority = %s"
                params.append(priority)
            query += " ORDER BY due_date ASC, id DESC"
            cursor.execute(query, tuple(params))
            rows = cursor.fetchall()
            tasks = []
            for row in rows:
                tasks.append(cls(
                    row['title'], row['description'], row['status'], 
                    row['priority'], row['due_date'], row['user_id'], row['id']
                ))
            return tasks
        finally:
            cursor.close()
            conn.close()
