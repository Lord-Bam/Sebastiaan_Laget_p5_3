from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from pydantic import BaseModel, constr, EmailStr, ValidationError

import model_dto
from model_dto import UserDto

register_bp = Blueprint("register", __name__)  # Create a Blueprint for registration-related routes

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get form data
        form_data = {
            "username": request.form.get("username"),
            "password": request.form.get("password"),
            "email": request.form.get("email"),
            "mobile_nr": request.form.get("mobile_nr"),
        }

        try:
            # Validate form data with Pydantic
            user = model_dto.UserDto.model_validate(form_data)
            user = current_app.model.register(user)
            # If valid, flash success and redirect (e.g., to a login page)
            flash("Registration successful!", "success")
            return redirect(url_for("login.login"))
        except ValidationError as e:
            # If validation fails, flash errors
            for error in e.errors():
                flash(f"{error['loc'][0]}: {error['msg']}", "danger")

    return render_template("register.html")