from flask import jsonify, request
from basic.exceptions.resource_not_found import ResourceNotFound
from basic.models.employee import Employee
from basic.services.employee_service import EmployeeService as ES


def route(app):

    @app.route("/empys", methods=['GET'])
    def get_all_employees():
        return jsonify(ES.all_employees()), 200

    @app.route("/empys/<empy_id>", methods=['GET'])
    def get_employee(empy_id):
        try:
            employee = ES.get_employee_by_id(int(empy_id))
            return jsonify(employee.json()), 200
        except ValueError as e:
            return "Not a valid employee ID.", 400
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/empys", methods=['POST'])
    def post_employee():
        employee = Employee.json_parse(request.json)
        employee = ES.create_employee(employee)
        return jsonify(employee.json()), 201


# Below code is useless to assignment:


"""

    @app.route("/clients/<client_id>", methods=['PUT'])
    def put_client(client_id):
        client = Client.json_parse(request.json)
        client.holder_id = int(client_id)

        try:
            client = ClientService.update_client(client)
            return jsonify(client.json()), 200

        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/clients/<client_id>", methods=['DELETE'])
    def del_client(client_id):
        try:
            ClientService.delete_client(int(client_id))
            return "", 205

        except ResourceNotFound as r:
            return r.message, 404
"""
