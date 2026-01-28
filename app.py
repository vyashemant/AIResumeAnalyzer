from flask import Flask
from config import Config
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.resume_routes import resume_bp
from datetime import datetime


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # Custom Jinja2 filters
    app.jinja_env.filters['strptime'] = lambda value, fmt: datetime.strptime(value, fmt)
    app.jinja_env.filters['strftime'] = lambda value, fmt: value.strftime(fmt)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(resume_bp)

    return app


# Expose app for Vercel
app = create_app()
