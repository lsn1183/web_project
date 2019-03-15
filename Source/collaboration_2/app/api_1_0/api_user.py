# -*- coding: UTF-8 -*-'
from flask import request
from flask import current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_user import CtrlUser
from app.ctrl.ctrl_role import ROLE_CLS_SYS


class ApiUser(Resource):
    @auth.login_required
    def get(self, user_id=None):
        result = {"result": "NG", "content": []}
        obj = CtrlUser()
        count, user_list = obj.get_user(user_id)
        if user_list:
            result["content"] = user_list
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get user Failed],"
                                    "user_id=%s" % user_id)
        return result


class ApiUserRole(Resource):
    @auth.login_required
    def get(self, page, size, user_id=None, condition=None, cls=ROLE_CLS_SYS):
        result = {"result": "NG", "content": []}
        obj = CtrlUser()
        # import time
        # print(time.strftime("%Y-%m-%d %H:%M:%S"))
        count, user_role_list = obj.get_user_role(page, size, user_id, cls, condition)
        # print(time.strftime("%Y-%m-%d %H:%M:%S"))
        if user_role_list:
            result["content"] = user_role_list
            result["count"] = count
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get User Role Failed],"
                                    "user_id=%s, class=%s" % (user_id, cls))
        return result

    @auth.login_required
    def put(self):
        req_json = request.get_json(force=True)
        ctrl_user = CtrlUser()
        return ctrl_user.update_user_role(req_json)


class ApiUserPermission(Resource):
    @auth.login_required
    def get(self, user_id):
        result = {"result": "NG", "content": []}
        obj = CtrlUser()
        permission_list = obj.get_user_permission(user_id)
        if permission_list:
            result["content"] = permission_list
            result["result"] = "OK"
        else:
            current_app.logger.info("[Get User Permission Failed],"
                                    "user_id=%s," % (user_id,))
        return result


class ApiUserRoleCactus(Resource):
    @auth.login_required
    def post(self):
        result = {'result': 'NG', 'error': ''}
        json_data = request.get_json(force=True)
        from app.ctrl.ctrl_user import CtrlUser
        perm_list, error = CtrlUser().get_role_by_cactus(json_data)
        if error:
            result['error'] = error
        else:
            result['result'] = 'OK'
            result['content'] = perm_list
        return result
