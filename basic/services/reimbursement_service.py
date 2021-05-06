from basic.daos.reimbursement_dao import ReimbursementDAO


class ReimbursementService:

    rmbt_dao = ReimbursementDAO()

    @classmethod
    def create_reimbursement(cls, reimbursement):
        return cls.rmbt_dao.create_reimbursement(
            reimbursement
        )

    @classmethod
    def get_reimbursement_by_id(cls, empy_id, rmbt_id):
        return cls.rmbt_dao.get_reimbursement(
            empy_id, rmbt_id
        )

    @classmethod
    def all_reimbursements(cls, empy_id):
        return cls.rmbt_dao.all_reimbursements(
            empy_id
        )

    @classmethod
    def rmbts_req_user_attn(cls, empy_id):
        return cls.rmbt_dao.rmbts_req_user_attn(
            empy_id
        )

    @classmethod
    def update_reimbursement(cls, reimbursement):
        return cls.rmbt_dao.update_reimbursement(
            reimbursement
        )
