from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session, abort
import time
import model_dto
import tools
import jwt
from forms import LoginForm, VerifyCodeForm, ResetPasswordForm

login_bp = Blueprint("login", __name__)  # Create a Blueprint for login-related routes

@login_bp.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        login_dto = model_dto.LoginDto(username=username, password=password)
        login_result = current_app.model.login(login_dto)

        if login_result == "True" or login_result == "verify_sms" or login_result == "verify_mail":
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

    return render_template("login.html", form=form)

@login_bp.route("/dashboard")
def dashboard():
    username = session.get("username")
    return render_template("dashboard.html", username=username)

@login_bp.route("/logout")
def logout():
    session.clear()
    return redirect('/')

@login_bp.route("/admin")
def admin():
    if session.get("user")["role"] == "admin":
        return render_template("admin.html")
    else:
        session.clear()
        return redirect('/')

@login_bp.route("/reset", methods=["GET", "POST"])
def reset():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        #check if user exists
        print("fetching user via mail:", form.mail.data)
        current_app.model.send_reset_mail(form.mail.data)
        flash("Reset mail sent!", "success")
        return redirect('/')
        pass
    return render_template("reset.html", form = form)

@login_bp.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        #get user input
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        #get user
        user = current_app.model.get_user(username)

        if user.email != session.get("email"):
            print("invalid mail")
            flash(f"something went wrong", "danger")
            return redirect('/')

        if user:
            if password1 != password2:
                print("passwords do not match")
                flash("passwords do not match")
                return render_template("reset_password.html")
            #save new password
            user.password = password1
            current_app.model.update_user(user)
            return redirect('/')
        else:
            flash(f"something went wrong", "danger")

    #verify token
    token = request.args.get("token")
    if not token:
        abort(400, "Missing token")
    try:
        decoded_token = jwt.decode(token, "secret_key", algorithms=['HS256'])
        session["token"] = token
        session["email"] = decoded_token.get("email")
        return render_template("reset_password.html")
        print(decoded_token)
    except jwt.ExpiredSignatureError:
        flash("Token has expired")
        print("Token has expired")
        return redirect('/')
    except jwt.InvalidTokenError:
        print("Invalid token")
        flash("Invalid token")
        return redirect('/')

    return redirect('/')

@login_bp.route("/verify_code", methods=["GET", "POST"])
def verify_code():
    form = VerifyCodeForm()
    print(session.get("username"))
    verify_type = session.get("verify_type")
    label_text = f"{verify_type.capitalize()} code"  # 'sms code' or 'mail code'
    form.code.label.text = label_text

    if request.method == "POST" and form.validate_on_submit():
        user = session.get("user")
        code_under_under_test = model_dto.RegistrationCodeDto(code=form.code.data,
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

    return render_template("verify_code.html", session = session, form = form)

