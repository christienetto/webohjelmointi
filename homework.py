from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from models import get_homework_by_user, add_homework, get_homework_by_id, delete_homework, search_homework

from db import add_collaborator
home_bp = Blueprint('home', __name__)

@home_bp.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    query = request.form.get('search_query', '')
    if query:
        homeworks = search_homework(session['user_id'], query)
    else:
        homeworks = get_homework_by_user(session['user_id'])

    homework_list = []
    for hw in homeworks:
        hw_dict = dict(hw)
        if isinstance(hw_dict['due_date'], str):
            hw_dict['due_date'] = datetime.strptime(hw_dict['due_date'], '%Y-%m-%d')
        homework_list.append(hw_dict)

    return render_template('index.html', homeworks=homework_list, search_query=query)

@home_bp.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        course = request.form['course']
        title = request.form['title']
        due = datetime.strptime(request.form['due_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
        add_homework(course, title, due, session['user_id'])
        flash("Homework added successfully.", "success")
        return redirect(url_for('home.index'))
    return render_template('add.html')

@home_bp.route('/delete/<int:id>')
def delete(id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    hw = get_homework_by_id(id)
    if hw and hw['user_id'] == session['user_id']:
        delete_homework(id)
        flash("Homework deleted.", "success")
    else:
        flash("Permission denied.", "danger")
    return redirect(url_for('home.index'))


@home_bp.route('/add_collaborator', methods=['GET', 'POST'])
def add_collaborator_route():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        username = request.form['collaborator_username']
        success = add_collaborator(session['user_id'], username)
        if success:
            flash('Collaborator added.', 'success')
        else:
            flash('Failed to add collaborator.', 'danger')
        return redirect(url_for('home.index'))

    return render_template('add_collaborator.html')

