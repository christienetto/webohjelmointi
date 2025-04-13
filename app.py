from flask import Flask
from db import init_db
from auth import auth_bp
from homework import home_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.register_blueprint(auth_bp)
app.register_blueprint(home_bp)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

