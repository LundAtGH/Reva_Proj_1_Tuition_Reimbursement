from flask import jsonify, request, render_template
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from basic.exceptions.resource_not_found \
    import ResourceNotFound

from basic.exceptions.resource_unavailable \
    import ResourceUnavailable

from basic.models.reimbursement \
    import Reimbursement

from basic.services.reimbursement_service \
    import ReimbursementService as RS


def route(app):

    @app.route('/request_tuition_reimbursement')
    @login_required
    def rqst_tutn_reimbursement():
        return render_template("request_tuition_reimbursement.html")

    @app.route('/rmbts')
    @login_required
    def reimbursements():
        if current_user.id == 1:
            return render_template("reimbursements.html", name=current_user.name)
        else:
            return redirect("rmbts/" + str(current_user.id))

    @app.route("/rmbts/<empy_id>", methods=['GET'])
    @login_required
    def reimbursements_for_employee(empy_id):
        if \
                current_user.id == int(empy_id) or \
                current_user.id == 1:
            try:
                return render_template(
                    "rmbts_for_empy.html",
                    data=RS.all_reimbursements(int(empy_id))
                ), \
                    200
            except ResourceNotFound as r:
                return r.message, 404
        else:
            return "You lack the required user id to access this data.", 403  # Forbidden!

    @app.route("/rmbts/<empy_id>", methods=['POST'])
    @login_required
    def post_reimbursement(empy_id):

        reimbursement = Reimbursement()

        reimbursement.employee_id = \
            int(empy_id)
        reimbursement.class_type = \
            request.form.get('classType')
        reimbursement.funds = \
            float(str(request.form.get('funds')))
        reimbursement.stage_reason = \
            "0 (Req. by " + request.form.get('name') + \
            "):(br)" + request.form.get('eventInfo')
        reimbursement.grade_or_presentation = \
            request.form.get('gradeOrPresentation')

        reimbursement.date_of_last_escalation = \
            int(str(request.form.get('dateRequested')).replace("-", ""))
        reimbursement.date_requested = \
            int(str(request.form.get('dateRequested')).replace("-", ""))
        reimbursement.date_starting = \
            int(str(request.form.get('dateStarting')).replace("-", ""))
        
        reimbursement = RS.create_reimbursement(reimbursement)

        return jsonify(reimbursement.json()), 201

    @app.route("/rmbts_req_attn", methods=['GET'])
    @login_required
    def reimbursements_req_attn():
        try:
            if current_user.id != 1:
                return render_template(
                    "rmbts_req_attn.html",
                    data=RS.rmbts_req_user_attn(int(current_user.id))
                ), \
                    200
            else:
                return render_template(
                    "rmbts_req_attn.html",
                    data=RS.all_reimbursements(-1)
                ), \
                    200
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/rmbts_req_attn", methods=['POST'])
    @login_required
    def update_reimbursement():
        try:
            reimbursement = Reimbursement()

            reimbursement.id = \
                int(request.form.get('id'))
            reimbursement.employee_id = \
                int(current_user.id)
            reimbursement.class_type = \
                request.form.get('classType')
            reimbursement.funds = \
                float(str(request.form.get('funds')))

            # Build approval stage:

            reimbursement.approval_stage = int(request.form.get('approvalStage'))

            if request.form.get('approvalCheck'):
                reimbursement.approval_stage += 1
                if reimbursement.approval_stage < 0:
                    reimbursement.approval_stage = 0
                if reimbursement.approval_stage > 5:
                    reimbursement.approval_stage = 5

            if not request.form.get('approvalCheck'):
                if 0 <= reimbursement.approval_stage < 5:
                    reimbursement.approval_stage += 1
                    reimbursement.approval_stage *= -1

            # Build new stage reason:

            reimbursement.stage_reason = request.form.get('stageReason')

            if not reimbursement.approval_stage \
                   == int(request.form.get('approvalStage')):

                prefix = str(reimbursement.approval_stage) + " ("

                if reimbursement.approval_stage ==  0: prefix += "Requested"
                if reimbursement.approval_stage ==  1: prefix += "Approved, Req. Grading"
                if reimbursement.approval_stage ==  2: prefix += "Approval Email Provided"
                if reimbursement.approval_stage ==  3: prefix += "Approved By Supervisor"
                if reimbursement.approval_stage == -3: prefix += "Rejected By Supervisor"
                if reimbursement.approval_stage ==  4: prefix += "Approved By Dept. Head"
                if reimbursement.approval_stage == -4: prefix += "Rejected By Dept. Head"
                if reimbursement.approval_stage ==  5: prefix += "Approved, Awarded"
                if reimbursement.approval_stage == -5: prefix += "Rejected By BenCo"
                prefix += "):(br)" + str(request.form.get('approvalText')) + "(br)(br)"

                reimbursement.stage_reason = prefix + reimbursement.stage_reason

                if len(reimbursement.stage_reason) > 500:
                    reimbursement.stage_reason = reimbursement.stage_reason[0: 497] + "..."

            # End

            reimbursement.grade_or_presentation = \
                request.form.get('gradeOrPresentation')

            reimbursement.date_of_last_escalation = \
                int(str(request.form.get('dateRequested')).replace("-", ""))
            reimbursement.date_requested = \
                int(str(request.form.get('dateRequested')).replace("-", ""))
            reimbursement.date_starting = \
                int(str(request.form.get('dateStarting')).replace("-", ""))

            RS.update_reimbursement(reimbursement)

            return jsonify(reimbursement.json()), 200

        except ResourceNotFound as r:
            return r.message, 404


# Incomplete:


"""

    @app.route("/empys/<empy_id>/rmbts?<conditions>", methods=['GET'])
    def get_some_reimbursements(empy_id, conditions):
        try:
            return jsonify(RS.some_reimbursements(int(empy_id), conditions)), 200
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/empys/<empy_id>/rmbts/<reimbursement_id>", methods=['GET'])
    def get_reimbursement(empy_id, reimbursement_id):
        try:
            reimbursement = RS.get_reimbursement_by_id(int(empy_id), int(reimbursement_id))
            return jsonify(reimbursement.json()), 200
        except ValueError as e:
            return "Employee or reimbursement ID invalid.", 400
            # Bad request
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/empys/<empy_id>/rmbts/<reimbursement_id>", methods=['PUT'])
    def put_reimbursement(empy_id, reimbursement_id):
        try:
            reimbursement = BankAcct.json_parse(request.json)
            reimbursement.reimbursement_id = int(reimbursement_id)
            reimbursement.holder_id = int(empy_id)
            RS.update_reimbursement(reimbursement)

            return jsonify(reimbursement.json()), 200
        except ResourceNotFound as r:
            return r.message, 404

"""


# Below Code is useless to assignment:


"""

    @app.route("/empys/<empy_id>/rmbts/<reimbursement_id>", methods=['DELETE'])
    def del_reimbursement(empy_id, reimbursement_id):
        try:
            RS.delete_reimbursement(int(empy_id), int(reimbursement_id))
            return "", 204
        except ResourceNotFound as r:
            return r.message, 404

    @app.route("/empys/<empy_id>/rmbts/<reimbursement_id>", methods=['PATCH'])
    def patch_reimbursement(empy_id, reimbursement_id):

        depo_req = float(request.json['deposit'])
        with_req = float(request.json['withdraw'])

        if depo_req > 0:
            try:
                reimbursement = RS.deposit_funds(int(empy_id), int(reimbursement_id), depo_req)
                return jsonify(reimbursement.json()), 200
            except ResourceNotFound as r:
                return r.message, 404

        elif with_req > 0:
            try:
                reimbursement = RS.withdraw_funds(int(empy_id), int(reimbursement_id), with_req)
                return jsonify(reimbursement.json()), 200
            except ResourceUnavailable as e:
                return e.message, 422
            except ResourceNotFound as r:
                return r.message, 404

    @app.route("/empys/<empy_id>/rmbts/<id_of_BA_taken_from>/transfer/<id_of_BA_depos_into>",
               methods=['PATCH'])
    def tran_betw_reimbursements(empy_id, id_of_BA_taken_from, id_of_BA_depos_into):

        amount = float(request.json['amount'])

        try:
            reimbursement = RS.transfer_funds(
                int(empy_id), int(id_of_BA_taken_from), int(id_of_BA_depos_into), amount
            )
            return jsonify(reimbursement.json()), 200
        except ResourceUnavailable as e:
            return e.message, 422
        except ResourceNotFound as r:
            return r.message, 404
"""
