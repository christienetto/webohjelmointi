
import sqlite3

DATABASE = 'homework.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS homework (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        course TEXT NOT NULL,
        title TEXT NOT NULL,
        due_date TEXT NOT NULL,
        user_id INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES user (id)
    )''')

    c.execute('''CREATE TABLE IF NOT EXISTS collaborations (
        owner_id INTEGER NOT NULL,
        collaborator_id INTEGER NOT NULL,
        FOREIGN KEY (owner_id) REFERENCES user (id),
        FOREIGN KEY (collaborator_id) REFERENCES user (id),
        UNIQUE (owner_id, collaborator_id)
    )''')

    conn.commit()
    conn.close()



def add_collaborator(owner_id, collaborator_username):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM user WHERE username = ?', (collaborator_username,))
    row = c.fetchone()
    if not row:
        return False
    collaborator_id = row['id']
    try:
        c.execute('INSERT INTO collaborations (owner_id, collaborator_id) VALUES (?, ?)', (owner_id, collaborator_id))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def get_all_accessible_homework(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT owner_id FROM collaborations WHERE collaborator_id = ?', (user_id,))
    owners = [row['owner_id'] for row in c.fetchall()]
    owners.append(user_id)
    placeholders = ','.join('?' for _ in owners)
    query = f'SELECT * FROM homework WHERE user_id IN ({placeholders})'
    c.execute(query, owners)
    result = c.fetchall()
    conn.close()
    return result

