from db import get_db

def get_user_by_username(username):
    db = get_db()
    return db.execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()

def create_user(username, hashed_password):
    db = get_db()
    db.execute("INSERT INTO user (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()

def get_homework_by_user(user_id):
    db = get_db()
    return db.execute("SELECT * FROM homework WHERE user_id = ? ORDER BY due_date ASC", (user_id,)).fetchall()

def search_homework(user_id, query):
    db = get_db()
    return db.execute(
        "SELECT * FROM homework WHERE user_id = ? AND (title LIKE ? OR course LIKE ?) ORDER BY due_date ASC",
        (user_id, f'%{query}%', f'%{query}%')
    ).fetchall()

def add_homework(course, title, due_date, user_id):
    db = get_db()
    db.execute(
        "INSERT INTO homework (course, title, due_date, user_id) VALUES (?, ?, ?, ?)",
        (course, title, due_date, user_id)
    )
    db.commit()

def get_homework_by_id(homework_id):
    db = get_db()
    return db.execute("SELECT * FROM homework WHERE id = ?", (homework_id,)).fetchone()

def delete_homework(homework_id):
    db = get_db()
    db.execute("DELETE FROM homework WHERE id = ?", (homework_id,))
    db.commit()

