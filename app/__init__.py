from flask import Flask, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
from .extensions import ma, limiter, cache
from .models import db
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(f"config.{config_name}")

    #initialize extensions
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    # Set up Swagger UI
    SWAGGER_URL = '/api/docs'
    API_URL = '/static/swagger.yaml'  # This will serve from app/static/swagger.yaml
    
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "Mechanic Shop API"
        }
    )
    app.register_blueprint(swaggerui_blueprint)

    # Add a simple index route
    @app.route('/')
    def index():
        return {
            "message": "Welcome to Mechanic Shop API",
            "documentation": "/api/docs",
            "endpoints": {
                "customers": "/customers/",
                "mechanics": "/mechanics/",
                "service_tickets": "/service_tickets/",
                "inventory": "/inventory/"
            }
        }

    # Register blueprints
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
        
    
    return app