import unittest

from basic.exceptions.resource_not_found import ResourceNotFound
from basic.models.employee import Employee
from basic.models.reimbursement import Reimbursement
from basic.services.reimbursement_service import ReimbursementService


class Tests(unittest.TestCase):

    def test_employee_model(self):
        worker = Employee(
            name="Bob", job="Slob", phone="Bone"
        )
        self.assertEqual(
            isinstance(worker, Employee), True
        )

    def test_reimbursement_model(self):
        class_cash = Reimbursement(
            funds=3333.33
        )
        self.assertEqual(
            isinstance(class_cash, Reimbursement), True
        )

    def test_reimbursements_missing(self):
        try:
            rmbts = ReimbursementService.all_reimbursements(314159)
            raise AssertionError(
                "Reimbursements for employee 314159 shouldn't exist."
            )
        except ResourceNotFound as e:
            self.assertEqual(
                e.message,
                "Employee or reimbursement(s) not found."
            )


if __name__ == "__main__":

    unittest.main()
