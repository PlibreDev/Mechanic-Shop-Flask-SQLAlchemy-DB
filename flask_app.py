from app import create_app
from app.extensions import db

app = create_app('ProductionConfig')

