# -*- coding: UTF-8 -*-
from flask import request
from flask import current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_role import CtrlRole
from app.ctrl.ctrl_role import ROLE_CLS_SYS


class ApiRole(Resource):
    @auth.login_required
    def get(self, role_id=None, cls=ROLE_CLS_SYS):
        result = {"result": "NG", "content": []}
        obj = CtrlRole()
        role_list = obj.get_roles(role_id, cls)
        if role_list:
            result["content"] = role_list
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get Role Failed],"
                                    "role_id=%s, class=%s" % (role_id, cls))
        return result


class ApiRolePermission(Resource):
    @auth.login_required
    def get(self, role_id=None, cls=ROLE_CLS_SYS):
        result = {"result": "NG", "content": []}
        obj = CtrlRole()
        role_list = obj.get_role_permission(role_id, cls)
        if role_list:
            result["content"] = role_list
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get Role Permission Failed],"
                                    "role_id=%s, class=%s" % (role_id, cls))
        return result

    @auth.login_required
    def put(self):
        req_json = request.get_json(force=True)
        ctrl_tag = CtrlRole()
        return ctrl_tag.update_role_permissions(req_json)
