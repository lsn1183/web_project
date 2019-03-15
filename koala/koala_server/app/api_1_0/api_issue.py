from flask_restful import Resource, request
from token_manage import auth
from app.ctrl.ctrl_issue import CtrlIssue


class ApiIssueList(Resource):
    @auth.login_required
    def get(self, base_id):
        result = {"result": "NG", "content": []}
        res = CtrlIssue().get_issue_list(base_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data = request.get_json(force=True)
        if data:
            res, message = CtrlIssue().add_issue(data)
            if res:
                result = {"result": "OK"}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result


class ApiUpdateIssueStatus(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ""}
        data = request.get_json(force=True)
        if data:
            res, message = CtrlIssue().add_issue(data)
            if res:
                result = {"result": "OK"}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result


class ApiReplayList(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        res = CtrlIssue().get_replay_list()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            replay_id, message = CtrlIssue().add_replay(data)
            if replay_id:
                result = {"result": "OK", 'content': replay_id}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result
