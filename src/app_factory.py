from flask import Flask, session, request, redirect, url_for, render_template
from views.login import login_bp
from views.register import  register_bp
import json

def create_app():
    app = Flask(__name__)
    app.secret_key = "your_secret_key"  # Required for flash messages and session management
    SESSION_TIMEOUT = 60

    # Register the Blueprint for login
    app.register_blueprint(login_bp)
    app.register_blueprint(register_bp)

    EXCLUDED_ENDPOINTS = {'login.login', "login.verify_code", "register.register"}

    @app.before_request
    def before_request():
        print("Before each request")
        print("username", session.get("username"))
        print("user:", session.get("user"))
        print("sms:", session.get("sms"))
        print("mail:", session.get("mail"))

        #if user is logged in, redirect login to dashboard
        if request.endpoint == "login.login":
            if session.get("user") is not None:
                return redirect(url_for('login.dashboard'))

        #skip checking stuff when user goes to login or login.verify_code page
        if request.endpoint in EXCLUDED_ENDPOINTS:
            return  # Skip the logic for excluded endpoints
        #redirect depending on user state

        #if user does not have a session, redirect him to the login page
        if session.get("user") is None:
            return redirect(url_for('login.login'))

        #if sms or mail code is not verified, redirect him to the correct verify page
        if not session.get("sms")["verified"]:
            session["verify_type"] = "sms"
            return redirect(url_for('login.verify_code'))

        if not session.get("mail")["verified"]:
            session["verify_type"] = "mail"
            return redirect(url_for('login.verify_code'))

    return app