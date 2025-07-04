class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:pj627129@localhost:3306/mechanic_db'
    DEBUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass

