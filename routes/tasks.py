from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models.task import Task
from functools import wraps

tasks_bp = Blueprint('tasks', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@tasks_bp.route('/')
@login_required
def dashboard():
    status_filter = request.args.get('status', '')
    priority_filter = request.args.get('priority', '')
    
    try:
        tasks = Task.find_by_user(session['user_id'], status=status_filter, priority=priority_filter)
        return render_template('dashboard.html', tasks=tasks, current_status=status_filter, current_priority=priority_filter)
    except Exception as e:
        flash(f"Error loading tasks: {str(e)}", "error")
        return render_template('dashboard.html', tasks=[], current_status=status_filter, current_priority=priority_filter)

@tasks_bp.route('/task/new', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title').strip()
        description = request.form.get('description').strip()
        status = request.form.get('status')
        priority = request.form.get('priority')
        due_date = request.form.get('due_date') or None

        if not title:
            flash('Task title is required.', 'error')
            return render_template('task_form.html', task=None, action='Create')

        new_task = Task(title, description, status, priority, due_date, session['user_id'])
        try:
            new_task.save()
            flash('Task created successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except Exception as e:
            flash(f"Error saving task: {str(e)}", "error")
            
    return render_template('task_form.html', task=None, action='Create')

@tasks_bp.route('/task/<int:task_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(task_id):
    try:
        task = Task.find_by_id(task_id)
    except Exception as e:
        flash(f"Error retrieving task: {str(e)}", "error")
        return redirect(url_for('tasks.dashboard'))

    if not task or task.user_id != session['user_id']:
        flash('Task not found or access denied.', 'error')
        return redirect(url_for('tasks.dashboard'))

    if request.method == 'POST':
        task.title = request.form.get('title').strip()
        task.description = request.form.get('description').strip()
        task.status = request.form.get('status')
        task.priority = request.form.get('priority')
        task.due_date = request.form.get('due_date') or None

        if not task.title:
            flash('Task title is required.', 'error')
            return render_template('task_form.html', task=task, action='Edit')

        try:
            task.save()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('tasks.dashboard'))
        except Exception as e:
            flash(f"Error saving task: {str(e)}", "error")

    return render_template('task_form.html', task=task, action='Edit')

@tasks_bp.route('/task/<int:task_id>/delete', methods=['POST'])
@login_required
def delete(task_id):
    try:
        task = Task.find_by_id(task_id)
        if not task or task.user_id != session['user_id']:
            flash('Task not found or access denied.', 'error')
            return redirect(url_for('tasks.dashboard'))
        
        task.delete()
        flash('Task deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting task: {str(e)}", "error")
        
    return redirect(url_for('tasks.dashboard'))
