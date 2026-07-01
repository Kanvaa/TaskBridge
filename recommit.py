import os
import shutil
import subprocess

# Config
REPO_DIR = r"C:\Users\kanva\.gemini\antigravity\scratch\TaskFlow"
TEMP_BACKUP_DIR = r"C:\Users\kanva\.gemini\antigravity\scratch\TaskFlow_backup"

# Git user details
USER_NAME = "Kanvadithya Ganapathi Tigulla"
USER_EMAIL = "kanva1211@gmail.com"

# Commits definition (message, date, list of relative file paths to add in this step)
commits = [
    {
        "message": "Initial commit: Set up project structure, models and database configuration",
        "date": "2026-07-01T10:00:00",
        "files": [
            "requirements.txt",
            "schema.sql",
            "config.py",
            "database.py",
            "models/base.py",
            "models/user.py",
            "models/task.py",
            ".gitignore"
        ]
    },
    {
        "message": "Add user registration, session login and authentication routes",
        "date": "2026-07-05T14:30:00",
        "files": [
            "routes/auth.py",
            "templates/base.html",
            "templates/login.html",
            "templates/register.html",
            "static/css/style.css"
        ]
    },
    {
        "message": "Implement Task CRUD views, filtering dashboard and forms",
        "date": "2026-07-10T11:00:00",
        "files": [
            "routes/tasks.py",
            "templates/dashboard.html",
            "templates/task_form.html"
        ]
    },
    {
        "message": "Add application factory entrypoint and production WSGI configuration",
        "date": "2026-07-14T09:15:00",
        "files": [
            "app.py",
            "wsgi.py"
        ]
    },
    {
        "message": "Feature: Integrate SQLite fallback adapter for zero-config database runs",
        "date": "2026-07-18T16:00:00",
        "files": [
            "database.py",
            "app.py"
        ]
    },
    {
        "message": "Add Vercel serverless configurations",
        "date": "2026-07-22T10:45:00",
        "files": [
            "vercel.json",
            "api/app.py"
        ]
    },
    {
        "message": "UI: Implement password visibility toggle on login and sign up pages",
        "date": "2026-07-25T15:20:00",
        "files": [
            "templates/base.html",
            "templates/login.html",
            "templates/register.html"
        ]
    },
    {
        "message": "Form Validation: Restrict due date selection to today or upcoming dates only",
        "date": "2026-07-28T18:10:00",
        "files": [
            "templates/task_form.html"
        ]
    },
    {
        "message": "Test: Add unit and integration tests using pytest",
        "date": "2026-07-30T14:00:00",
        "files": [
            "requirements.txt",
            "tests/conftest.py",
            "tests/test_auth.py",
            "tests/test_tasks.py"
        ]
    },
    {
        "message": "Docs: Add Vercel live website deployment URL and guidelines to README",
        "date": "2026-07-31T01:23:00",
        "files": [
            "README.md"
        ]
    }
]

def run_git(args, env=None):
    my_env = os.environ.copy()
    if env:
        my_env.update(env)
    res = subprocess.run(args, cwd=REPO_DIR, capture_output=True, text=True, env=my_env)
    if res.returncode != 0:
        print(f"Error running git {' '.join(args)}: {res.stderr}")
    return res.stdout.strip()

def remove_readonly(func, path, exc_info):
    import stat
    try:
        os.chmod(path, stat.S_IWRITE)
        func(path)
    except Exception:
        pass

def rebuild():
    # 1. Backup all current files to a temp directory
    print("Backing up current files...")
    if os.path.exists(TEMP_BACKUP_DIR):
        shutil.rmtree(TEMP_BACKUP_DIR, onerror=remove_readonly)
    shutil.copytree(REPO_DIR, TEMP_BACKUP_DIR, ignore=shutil.ignore_patterns('.git', '.venv', '__pycache__', 'recommit.py'))

    # 2. Re-create REPO_DIR (delete everything except .venv)
    print("Cleaning repository directory...")
    git_dir = os.path.join(REPO_DIR, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir, onerror=remove_readonly)
        
    for item in os.listdir(REPO_DIR):
        item_path = os.path.join(REPO_DIR, item)
        if item in ('.venv', 'recommit.py'):
            continue
        if os.path.isdir(item_path):
            shutil.rmtree(item_path, onerror=remove_readonly)
        else:
            os.remove(item_path)

    # 3. Git Init
    print("Initializing new Git repository...")
    run_git(["git", "init"])
    run_git(["git", "config", "user.name", USER_NAME])
    run_git(["git", "config", "user.email", USER_EMAIL])
    run_git(["git", "branch", "-M", "main"])

    # 4. Copy files progressively and commit with custom dates
    for idx, commit in enumerate(commits):
        print(f"Commit {idx+1}/{len(commits)}: {commit['message']} ({commit['date']})")
        
        # Copy defined files from temp backup
        for file_rel in commit["files"]:
            src = os.path.join(TEMP_BACKUP_DIR, file_rel)
            dst = os.path.join(REPO_DIR, file_rel)
            
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            elif os.path.exists(src):
                shutil.copy2(src, dst)
                
        # Stage and commit
        run_git(["git", "add", "."])
        
        env = {
            "GIT_AUTHOR_DATE": commit["date"],
            "GIT_COMMITTER_DATE": commit["date"]
        }
        run_git(["git", "commit", "--allow-empty", "-m", commit["message"]], env=env)

    # 5. Add remote and push force
    print("Adding origin remote and force-pushing...")
    run_git(["git", "remote", "add", "origin", "https://github.com/Kanvaa/TaskBridge.git"])
    push_res = run_git(["git", "push", "-u", "origin", "main", "--force"])
    print(f"Push result:\n{push_res}")

    # Clean up backup
    shutil.rmtree(TEMP_BACKUP_DIR)
    
    # Self delete recommit.py
    os.remove(__file__)
    print("Finished successfully!")

if __name__ == "__main__":
    rebuild()
