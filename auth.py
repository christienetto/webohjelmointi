from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from models import get_user_by_username, create_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if get_user_by_username(username):
            flash("Username already exists!", "danger")
            return redirect(url_for('auth.register'))
        hashed = generate_password_hash(password)
        create_user(username, hashed)
        flash("Account created! You can now log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = get_user_by_username(request.form['username'])
        if user and check_password_hash(user['password'], request.form['password']):
            session['user_id'] = user['id']
            flash("Login successful!", "success")
            return redirect(url_for('home.index'))
        flash("Invalid credentials", "danger")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('auth.login'))

