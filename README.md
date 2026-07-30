# TaskBridge — Task Management System

### Live Demo Website
You can access the live running application directly here: **[https://task-bridge-seven.vercel.app](https://task-bridge-seven.vercel.app)**

TaskBridge is a complete object-oriented Python-based task management web application built with **Flask**, **MySQL** (with automated **SQLite** fallback), and semantic **HTML/CSS**.

## OOP Design Principles & Architecture

This project is built using Object-Oriented Programming (OOP) paradigms in Python to structure models, routing logic, and database access:

- **`DatabaseConnection` (Singleton)**: Handled in `database.py`. Restricts instantiation of database connections to a single instance using `__new__` to manage resource optimization across routing handlers.
- **`BaseModel` (Abstraction)**: Located in `models/base.py`. Serves as the parent class for all entity models. Defines abstract interfaces like `save()`, `delete()`, and `find_by_id()` ensuring uniform behavior.
- **`User` (Model Inheritance & Encapsulation)**: Extends `BaseModel`. Encapsulates fields like `username`, `email`, and `password_hash` with secure password hashing helpers (`hash_password` and `check_password`) and static lookup operations.
- **`Task` (Model Inheritance)**: Extends `BaseModel`. Contains fields for `title`, `description`, `status`, `priority`, `due_date`, and `user_id`. Implements task persistence routines and filtering lookup metrics.

### OOP Relationships
- **Inheritance**: `User` &rarr; `BaseModel`, `Task` &rarr; `BaseModel`
- **Association (1-to-many)**: One `User` can own multiple `Task` instances.

---

## Database Schema Diagram

```
 +------------------+                +------------------+
 |      users       |                |      tasks       |
 +------------------+                +------------------+
 | id (PK)          | <------------+ | id (PK)          |
 | username (UQ)    |                | title            |
 | email (UQ)       |                | description      |
 | password_hash    |                | status           |
 | created_at       |                | priority         |
 +------------------+                | due_date         |
                                     | user_id (FK)     |
                                     | created_at       |
                                     +------------------+
```

---

## Setup Instructions

### 1. Prerequisite: MySQL Database
Make sure your local MySQL server is running (e.g., via XAMPP, Laragon, or standalone MySQL Service).
By default, the application is configured to connect to:
- **Host**: `localhost`
- **User**: `root`
- **Password**: *(empty)*
- **Database**: `taskbridge_db` (will be automatically created)

*To modify credentials, edit `config.py`.*

### 2. Configure Virtual Environment & Run
Run the following commands in your shell to run the app:

```bash
# Navigate to project root
cd TaskFlow

# Create a virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask development server
python app.py
```

Open your browser and navigate to: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Running Tests

This project includes a comprehensive unit and integration test suite built with `pytest` that validates models, user authentication flows, and task CRUD actions using an isolated temporary SQLite database connection (no database configuration required).

To run the tests:

```bash
# Make sure virtual environment is active, then run:
pytest
```
