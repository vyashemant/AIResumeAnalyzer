from flask import Flask
from config import Config
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.resume_routes import resume_bp

app = Flask(__name__)
app.config.from_object(Config)

# register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(resume_bp)

if __name__ == "__main__":
    app.run(debug=True)
