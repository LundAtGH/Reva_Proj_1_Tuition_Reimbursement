from basic.exceptions.resource_not_found import ResourceNotFound
from basic.exceptions.resource_unavailable import ResourceUnavailable
from basic.models.reimbursement import Reimbursement
from basic.util.db_connection import connection
import logging

log = logging.getLogger("application")
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)


class ReimbursementDAO:

    @staticmethod
    def proj_one_log(message):
        log.info("P1: " + str(message))

    def create_reimbursement(self, new_rbmt):

        self.proj_one_log("Attempting to create reimbursement...")

        sql = "insert into reimbursements values (" + \
              "DEFAULT, %s, %s, %s, %s, %s, %s, " + \
              "%s, %s, %s) returning *"  # Last 3 values are dates.

        cursor = connection.cursor()
        cursor.execute(sql, [
            new_rbmt.employee_id,
            new_rbmt.class_type,
            new_rbmt.funds,
            new_rbmt.approval_stage,
            new_rbmt.stage_reason,
            new_rbmt.grade_or_presentation,
            new_rbmt.date_of_last_escalation,
            new_rbmt.date_requested,
            new_rbmt.date_starting
        ])

        connection.commit()
        record = cursor.fetchone()

        return Reimbursement(
            record[0], record[1], record[2], float(str(record[3])),
            record[4], record[5], record[6], record[7],
            record[8], record[9]
        )

    def get_reimbursement(self, employee_id, reimbursement_id):

        self.proj_one_log("Attempting to get reimbursement...")

        sql = "select * from reimbursements where employee_id = %s and id = %s"

        cursor = connection.cursor()
        cursor.execute(sql, [
            employee_id, reimbursement_id
        ])

        record = cursor.fetchone()

        if record:
            return Reimbursement(
                record[0], record[1], record[2], float(str(record[3])),
                record[4], record[5], record[6], record[7],
                record[8], record[9]
            )
        else:
            raise ResourceNotFound("Reimbursement not found.")

    def all_reimbursements(self, employee_id):

        self.proj_one_log("Attempting to get all reimbursements...")

        sql = "select * from reimbursements where employee_id = %s"

        if employee_id == -1:
            sql = "select * from reimbursements"
            cursor = connection.cursor()
            cursor.execute(sql)
        else:
            cursor = connection.cursor()
            cursor.execute(sql, [
                employee_id
            ])

        records = cursor.fetchall()
        reimbursement_list = []

        for record in records:

            reimbursement = Reimbursement(
                record[0], record[1], record[2], float(str(record[3])),
                record[4], record[5], record[6], record[7],
                record[8], record[9]
            )
            reimbursement_list.append(reimbursement.json())

        if records:
            return reimbursement_list
        else:
            raise ResourceNotFound("Employee or reimbursement(s) not found.")

#########################################################

# R M B T S   R E Q .   U S E R   A T T E N T I O N . . .

#########################################################

    def rmbts_req_user_attn(self, user_id):

        self.proj_one_log("Getting user's pos. in company hierarchy...")

        boss_chain_length = 0
        employee_id = user_id

        while employee_id != -1:
            sql = "select supervisor_id from employees where id = %s"
            cursor = connection.cursor()
            cursor.execute(sql, [
                int(employee_id)
            ])
            record = cursor.fetchone()

            employee_id = record[0]
            if employee_id != -1:
                boss_chain_length += 1

    # # Boss chain length acquired: 0 = Dept. Head, 1 = Supervisor, 2 = Peon """

        self.proj_one_log("Getting all of user's underlings...")

        underlings = []
        underling_search_count = 0

        while underling_search_count < 2 - boss_chain_length:
            sql = "select id from employees where supervisor_id = %s"
            if underling_search_count > 0:
                sql = "select id from employees where not supervisor_id = %s "
                for underling in underlings:
                    sql += "and supervisor_id = " + str(int(underling))

            cursor = connection.cursor()
            cursor.execute(sql, [
                int(user_id)
            ])

            records = cursor.fetchall()
            for record in records:
                underlings.append(record[0])

            underling_search_count += 1

    # # All of user's underlings acquired.

        self.proj_one_log("Getting reimbursements req. user's attention...")

        rmbts_req_attn = []

        for underling in underlings:

            sql = "select * from reimbursements where " + \
                  "employee_id = %s and " + \
                  "approval_stage = %s"
            cursor = connection.cursor()
            cursor.execute(sql, [
                int(underling), int(3 - boss_chain_length)
            ])

            records = cursor.fetchall()
            for record in records:
                rmbt = Reimbursement(
                    record[0], record[1], record[2], float(str(record[3])),
                    record[4], record[5], record[6], record[7],
                    record[8], record[9]
                )
                rmbts_req_attn.append(rmbt.json())

        return rmbts_req_attn

# U P D A T E . . .

    def update_reimbursement(self, rmbt):

        self.proj_one_log("Attempting to update reimbursement...")

        sql = "update reimbursements set     " + \
              "class_type              = %s, " + \
              "funds                   = %s, " + \
              "approval_stage          = %s, " + \
              "stage_reason            = %s, " + \
              "grade_or_presentation   = %s, " + \
              "date_of_last_escalation = %s, " + \
              "date_requested          = %s, " + \
              "date_starting           = %s  " + \
              "where id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, [
            rmbt.class_type,
            rmbt.funds,
            rmbt.approval_stage,
            rmbt.stage_reason,
            rmbt.grade_or_presentation,
            rmbt.date_of_last_escalation,
            rmbt.date_requested,
            rmbt.date_starting,
            rmbt.id
        ])

        connection.commit()
        record = cursor.fetchone()

        if record:
            return Reimbursement(
                record[0], record[1], record[2], float(str(record[3])),
                record[4], record[5], record[6], record[7],
                record[8], record[9]
            )
        else:
            raise ResourceNotFound("Reimbursement not found.")


# Below code is useless to assignment:


"""

    def delete_reimbursement(self, client_id, reimbursement_id):

        self.proj_one_log("Attempting to delete reimbursement...")

        sql = "delete from reimbursements where holder_id = %s and id = %s returning *"

        cursor = connection.cursor()
        cursor.execute(sql, (int(client_id), int(reimbursement_id)))
        connection.commit()

        record = cursor.fetchone()

        if not record:
            raise ResourceNotFound("Client or account not found.")
"""
