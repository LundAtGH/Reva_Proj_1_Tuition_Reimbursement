from flask import render_template, request, flash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.utils import redirect

from basic.exceptions.resource_not_found import ResourceNotFound
from basic.services.employee_service import EmployeeService as ES


def route(app):
    @app.route('/')
    def index():
        return render_template("index.html")

    @app.route('/login')
    def login():
        return render_template("login.html")

    @app.route('/login', methods=['POST'])
    def login_post():
        try:
            employee_id = request.form.get('employeeId')
            password = request.form.get('password')

            user = ES.get_employee_by_id(int(employee_id))

            if not user or not user.password == password:
                flash('Employee id or password incorrect. Please try again.')
                return redirect("login")  # Reloads page.

            login_user(user)
            return redirect("/")

        except ValueError as e:
            return "Employee id or password invalid.", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")
