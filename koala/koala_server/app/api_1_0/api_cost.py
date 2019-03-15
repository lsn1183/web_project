from flask_restful import Resource, request
from token_manage import auth
from flask import current_app
from app.ctrl.ctrl_cost import CtrlCost


class ApiCost(Resource):
    @auth.login_required
    def get(self, quotation_id, user_id, myself=None):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_quotations_cost(quotation_id, user_id, myself)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data_json = request.get_json(force=True)
        res, msg = CtrlCost().update_cost(data_json)
        if res:
            result["result"] = "OK"
        else:
            result["error"] = msg
        return result


class ApiTaskCostHistiry(Resource):
    @auth.login_required
    def get(self, task_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_task_cost_history(task_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result


class ApiCostSummary(Resource):
    @auth.login_required
    def get(self, quotation_id, user_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().summary_cost(quotation_id, user_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        else:
            result["error"] = msg
        return result


class ApiCostDetail(Resource):
    @auth.login_required
    def get(self, func_id):
        result = {"result": "NG", "content": []}
        res, msg = CtrlCost().get_detail_cost(func_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["error"] = msg
        return result