from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
import time
import model_dto

login_bp = Blueprint("login", __name__)  # Create a Blueprint for login-related routes

@login_bp.route("/", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        login_dto = model_dto.LoginDto(username=username, password=password)

        login_result = current_app.model.login(login_dto)
        if login_result == "True":
            flash("Login successful!", "success")
            #create session
            return redirect(url_for("login.dashboard", username=request.form.get("username")))
        if login_result == "verify_sms":
            return redirect(url_for("login.verify_sms", username=request.form.get("username")))
        if login_result == "verify_mail":
            return redirect(url_for("login.verify_mail", username=request.form.get("username")))
        else:
            flash(f"{login_result}", "danger")

    return render_template("login.html")

@login_bp.route("/dashboard/<username>")
def dashboard(username):
    return render_template("dashboard.html", username=username)

@login_bp.route("/verify_sms/<username>")
def verify_sms(username):
    return render_template("verify_sms.html", username=username)

@login_bp.route("/verify_mail/<username>")
def verify_mail(username):
    return render_template("verify_mail.html", username=username)