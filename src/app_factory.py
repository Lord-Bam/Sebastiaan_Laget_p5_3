from flask import Flask
from views.login import login_bp
from views.register import  register_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Required for flash messages and session management

    # Register the Blueprint for login
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    return app