from basic.exceptions.resource_not_found import ResourceNotFound
from basic.models.employee import Employee
from basic.util.db_connection import connection
import logging

log = logging.getLogger("application")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class EmployeeDAO:

    @staticmethod
    def proj_one_log(message):
        log.info("P1: " + str(message))

    def create_employee(self, new_hire):

        self.proj_one_log("Attempting to create employee...")

        sql = "insert into employees values (" + \
              "DEFAULT, %s, %s, %s, %s, %s, %s) returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [
            new_hire.supervisor_id,
            new_hire.job,
            new_hire.name,
            new_hire.password,
            new_hire.email,
            new_hire.phone
        ])

        connection.commit()
        record = cursor.fetchone()

        return Employee(
            record[0], record[1], record[2], record[3],
            record[4], record[5], record[6]
        )

    def get_employee(self, employee_id):

        self.proj_one_log("Attempting to get employee...")

        sql = "select * from employees where id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [
            int(employee_id)
        ])

        record = cursor.fetchone()

        if record:
            return Employee(
                record[0], record[1], record[2], record[3],
                record[4], record[5], record[6]
            )
        else:
            raise ResourceNotFound("Employee not found.")

    def all_employees(self):

        self.proj_one_log("Attempting to get all employees...")

        sql = "select * from employees"

        cursor = connection.cursor()
        cursor.execute(sql)

        records = cursor.fetchall()
        employee_list = []

        for record in records:

            employee = Employee(
                record[0], record[1], record[2], record[3],
                record[4], record[5], record[6]
            )
            employee_list.append(employee.json())

        return employee_list


# Below code is useless to assignment.

"""
    def update_employee(self, new):

        self.proj_one_log("Attempting to update employee...")

        sql = "update employees set name = %s where id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [new.name, new.holder_id])

        connection.commit()
        record = cursor.fetchone()

        if record:
            return Employee(record[0], record[1])
        else:
            raise ResourceNotFound("Employee not found.")

    def delete_employee(self, employee_id):

        self.proj_one_log("Attempting to delete employee...")

        sql = "delete from employees where id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [employee_id])

        record = cursor.fetchone()
        connection.commit()

        if record:
            return Employee(record[0], record[1])
        else:
            raise ResourceNotFound("Employee not found.")
"""
