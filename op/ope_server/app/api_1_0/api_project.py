from flask_restful import Resource, request
from flask import current_app
from flask import g
from token_manage import serializer
import json
import os
from token_manage import auth
from app.ctrl.ctrl_project import CtrlProject
from app.ctrl.ctrl_ope import CtrlOpe


class ApiProjectList(Resource):

    # @auth.login_required
    def get(self):
        result = {"result": "OK", "content": []}
        res = CtrlProject().get_proj_list()
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    # @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            res, message = CtrlProject().add_project(data)
            if res:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

class ApiProject(Resource):

    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "NG"}
        res, msg = CtrlProject().get_one_proj_by_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["content"] = msg
        return result

    # @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            proj_id, message = CtrlProject().change_proj_by_id(data)
            if proj_id:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    # @auth.login_required
    def delete(self, proj_id):
        result = {"result": "NG"}
        proj_id, message = CtrlProject().delete_proj_by_id(proj_id)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
        else:
            result["error"] = message
        return result

class ApiProjectOpe(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "NG"}
        res, msg = CtrlOpe().get_ope_list(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = msg
        else:
            result["content"] = msg
        return result