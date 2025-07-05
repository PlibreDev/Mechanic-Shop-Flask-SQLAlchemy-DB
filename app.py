from app import create_app
from app.extensions import db

app = create_app('DevelopmentConfig')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print(app.url_map)
    app.run()

