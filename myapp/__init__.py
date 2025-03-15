# myapp/__init__.py
from flask import Flask
from .models import db

def create_app():
    """Application Factory: creates and configures the Flask app."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register blueprints or routes if needed
    # from .routes import main_bp
    # app.register_blueprint(main_bp)

    return app
