# -*- coding: UTF-8 -*-
from flask import request
from flask import current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_permission import CtrlPermission


class ApiPermission(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        obj = CtrlPermission()
        perm_list = obj.get_perms()
        if perm_list:
            result["content"] = perm_list
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get Permission Failed]")
        return result
