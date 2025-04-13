from flask import Flask, render_template
from app.models import db
from flask_migrate import Migrate
import os

migrate = Migrate()

def create_app(config_name='default'):
    """Factory function to create Flask application instance."""
    from config.config import config
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Create instance directory if it doesn't exist
    os.makedirs(app.instance_path, exist_ok=True)
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Add main route
    @app.route('/')
    def index():
        return render_template('index.html')
    
    return app 