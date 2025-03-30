
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///homework.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this to a secure secret key

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    homeworks = db.relationship('Homework', backref='user', lazy=True)

class Homework(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    due_date = db.Column(db.DateTime, nullable=False)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    search_query = request.form.get('search_query', '')

    if search_query:
        homeworks = Homework.query.filter(
            (Homework.user_id == session['user_id']) &
            ((Homework.title.contains(search_query)) | (Homework.course.contains(search_query)))
        ).order_by(Homework.due_date.asc()).all()
    else:
        homeworks = Homework.query.filter_by(user_id=session['user_id']).order_by(Homework.due_date.asc()).all()

    return render_template('index.html', homeworks=homeworks, search_query=search_query)
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))
        
        user = User(username=username, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! You can now log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Login successful!", "success")
            return redirect(url_for('index'))
        else:
            flash("Invalid username or password", "danger")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        course = request.form['course']
        title = request.form['title']
        due_date = datetime.strptime(request.form['due_date'], '%Y-%m-%d')

        homework = Homework(course=course, title=title, due_date=due_date, user_id=session['user_id'])
        db.session.add(homework)
        db.session.commit()
        flash("Homework added successfully.", "success")
        return redirect(url_for('index'))

    return render_template('add.html')

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    homework = Homework.query.get_or_404(id)
    if homework.user_id != session['user_id']:
        flash("You do not have permission to delete this homework.", "danger")
        return redirect(url_for('index'))
    
    db.session.delete(homework)
    db.session.commit()
    flash("Homework deleted successfully.", "success")
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
