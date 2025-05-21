from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .models import db, User
import sqlite3

login_manager = LoginManager()

# Function to create feedback table
def create_feedback_table():
    conn = sqlite3.connect('heart_disease.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedbacks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        message TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()
    print("✅ Table 'feedbacks' ensured to exist.")

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Ensure feedbacks table exists
    create_feedback_table()

    # Register Blueprints here
    from .routes import admin_routes, user_routes
    app.register_blueprint(admin_routes.bp)
    app.register_blueprint(user_routes.bp)

    return app
