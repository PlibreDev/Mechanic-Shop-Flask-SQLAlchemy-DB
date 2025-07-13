from app import create_app
from app.models import db

app = create_app('ProductionConfig')

try:
    with app.app_context():
        # db.drop_all()
        db.create_all()
except Exception as e:
    print(f"Warning: Could not create database tables: {e}")