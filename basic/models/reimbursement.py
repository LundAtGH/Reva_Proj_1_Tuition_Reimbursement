class Reimbursement:

    def __init__(self,
                 id=0,
                 employee_id=0,
                 class_type="",
                 funds=0,
                 approval_stage=0,
                 stage_reason="",
                 grade_or_presentation="",
                 date_of_last_escalation=0,
                 date_requested=0,
                 date_starting=0):

        self.id = id
        self.employee_id = employee_id
        self.class_type = class_type
        self.funds = funds
        self.approval_stage = approval_stage
        self.stage_reason = stage_reason
        self.grade_or_presentation = grade_or_presentation
        self.date_of_last_escalation = date_of_last_escalation
        self.date_requested = date_requested
        self.date_starting = date_starting

    def json(self):
        return {
            "id":                   self.id,
            "employeeId":           self.employee_id,
            "classType":            self.class_type,
            "funds":                self.funds,
            "approvalStage":        self.approval_stage,
            "stageReason":          self.stage_reason,
            "gradeOrPresentation":  self.grade_or_presentation,
            "dateOfLastEscalation": self.date_of_last_escalation,
            "dateRequested":        self.date_requested,
            "dateStarting":         self.date_starting
        }

    @staticmethod
    def json_parse(json):
        reimbursement = Reimbursement()
        reimbursement.id = json["id"] if "id" in json else 0
        reimbursement.employee_id = json[
            "employeeId"] if \
            "employeeId" in json else 0
        reimbursement.class_type = json["classType"]
        reimbursement.funds = json["funds"]
        reimbursement.approval_stage = json["approvalStage"]
        reimbursement.stage_reason = json["stageReason"]
        reimbursement.grade_or_presentation = json[
            "gradeOrPresentation"]
        reimbursement.date_of_last_escalation = json[
            "dateOfLastEscalation"]
        reimbursement.date_requested = json["dateRequested"]
        reimbursement.date_starting = json["dateStarting"]
        return reimbursement

    def __repr__(self):
        return str(self.json())
