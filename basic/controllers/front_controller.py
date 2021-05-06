from flask import request, flash
from flask_login import LoginManager
from werkzeug.utils import redirect

from basic.controllers import \
    employee_controller as empy, \
    reimbursement_controller as rmbt, \
    login_controller

from basic.services.employee_service import EmployeeService as ES


def route(app):

    login_manager = LoginManager()
    login_manager.login_view = "login.html"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return ES.get_employee_by_id(int(user_id))

    @login_manager.unauthorized_handler
    def unauthorized():
        flash('You must be logged in to view that page.')
        return redirect('/login?next=' + request.path)

    login_controller.route(app)

    empy.route(app)
    rmbt.route(app)
