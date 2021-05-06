from basic.daos.employee_dao import EmployeeDAO


class EmployeeService:

    employee_dao = EmployeeDAO()

    @classmethod
    def create_employee(cls, employee):
        return cls.employee_dao.create_employee(employee)

    @classmethod
    def all_employees(cls):
        return cls.employee_dao.all_employees()

    @classmethod
    def get_employee_by_id(cls, employee_id):
        return cls.employee_dao.get_employee(employee_id)
