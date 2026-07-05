from flask import Blueprint, render_template, redirect, url_for, request, session, flash
from models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('tasks.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username').strip()
        email = request.form.get('email').strip()
        password = request.form.get('password')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        try:
            # Check existing user
            if User.find_by_username(username):
                flash('Username already exists.', 'error')
                return render_template('register.html')
            
            if User.find_by_email(email):
                flash('Email already registered.', 'error')
                return render_template('register.html')

            password_hash = User.hash_password(password)
            new_user = User(username, email, password_hash)
            new_user.save()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('tasks.dashboard'))
    if request.method == 'POST':
        username = request.form.get('username').strip()
        password = request.form.get('password')

        try:
            user = User.find_by_username(username)
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Logged in successfully.', 'success')
                return redirect(url_for('tasks.dashboard'))
            else:
                flash('Invalid username or password.', 'error')
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login'))
