from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
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



        if login_result == "True" or "verify_sms" or "verify_mail":
            flash("Login successful!", "success")
            #create session
            session["username"] = username
            user = current_app.model.get_user(username=username)
            session["user"] = user.dict()
            session["sms"] = current_app.model.get_registration_sms_code_from_user(user).dict()
            session["mail"] = current_app.model.get_registration_mail_code_from_user(user).dict()
            return redirect(url_for("login.dashboard"))
        else:
            flash(f"{login_result}", "danger")

    return render_template("login.html")

@login_bp.route("/dashboard")
def dashboard():
    username = session.get("username")
    return render_template("dashboard.html", username=username)

@login_bp.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    print(session.get("username"))
    verify_type = session.get("verify_type")
    if request.method == "POST":
        user = session.get("user")
        code_under_under_test = model_dto.RegistrationCodeDto(code=request.form.get("code"),
                                                              type=model_dto.CodeTypeEnum(verify_type),
                                                              user=model_dto.UserDto.model_validate(session.get("user"))
                                                              )
        print(code_under_under_test)
        if current_app.model.verify_registration_code(code_under_under_test) == True:
            username = session.get("username")
            user = current_app.model.get_user(username=username)
            session["user"] = user.dict()
            session["sms"] = current_app.model.get_registration_sms_code_from_user(user).dict()
            session["mail"] = current_app.model.get_registration_mail_code_from_user(user).dict()
            return redirect(url_for("login.dashboard"))
        else:
            flash("code incorrect", "danger")

    return render_template("verify_code.html", session = session)