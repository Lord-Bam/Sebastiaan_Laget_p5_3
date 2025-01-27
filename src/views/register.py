from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from pydantic import BaseModel, constr, EmailStr, ValidationError
import model_dto
from model_dto import UserDto
from forms import RegisterForm

register_bp = Blueprint("register", __name__)  # Create a Blueprint for registration-related routes

@register_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Get form data
        form_data = {
            "username": form.username.data,
            "password": form.password.data,
            "email": form.email.data,
            "mobile_nr": form.mobile_nr.data
        }

        try:
            # Validate form data with Pydantic
            user = model_dto.UserDto.model_validate(form_data)
            result = current_app.model.register(user)
            # If valid, flash success and redirect (e.g., to a login page)
            if result:
               flash("Registration successful!", "success")
            else:
                flash("Registration failed!", "danger")
            return redirect('/')
        except ValidationError as e:
            # If validation fails, flash errors
            for error in e.errors():
                flash(f"{error['loc'][0]}: {error['msg']}", "danger")

    return render_template("register.html", form=form)