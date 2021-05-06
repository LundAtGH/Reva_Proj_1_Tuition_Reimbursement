from flask_login import UserMixin


class Employee(UserMixin):

    def __init__(
            self, id=0, supervisor_id=0, job="", name="",
            password="", email="", phone=""
    ):
        self.id = id
        self.supervisor_id = supervisor_id
        self.job = job
        self.name = name
        self.password = password
        self.email = email
        self.phone = phone

    def json(self):
        return {
            "id":           self.id,
            "supervisorId": self.supervisor_id,
            "job":          self.job,
            "name":         self.name,
            "password":     self.password,
            "email":        self.email,
            "phone":        self.phone
        }

    @staticmethod
    def json_parse(json):
        employee = Employee()
        employee.id = json["id"] if "id" in json else 0
        employee.supervisor_id = json[
            "supervisorId"] if \
            "supervisorId" in json else 0
        employee.job = json["job"]
        employee.name = json["name"]
        employee.password = json["password"]
        employee.email = json["email"]
        employee.phone = json["phone"]
        return employee

    def __repr__(self):
        return str(self.json())
