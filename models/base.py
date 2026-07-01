from database import DatabaseConnection

class BaseModel:
    db = DatabaseConnection()

    def save(self):
        raise NotImplementedError("Subclasses must implement save()")

    def delete(self):
        raise NotImplementedError("Subclasses must implement delete()")

    @classmethod
    def find_by_id(cls, model_id):
        raise NotImplementedError("Subclasses must implement find_by_id()")
