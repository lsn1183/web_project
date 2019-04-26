from flask_restful import Resource, request
from flask import current_app
from flask import g
from token_manage import serializer
import json
import os
from token_manage import auth
from app.ctrl.ctrl_ope import CtrlOpe


class ApiOpe(Resource):
    # @auth.login_required
    def get(self, screen_gid):
        """获取单本ope基本信息"""
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_ope_info(screen_gid)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    # @auth.login_required
    def post(self):
        """ope上锁"""
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            proj_id, message = CtrlOpe().lock_ope(data)
            if proj_id:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

    # @auth.login_required
    def delete(self, user_id, screen_gid):
        """删除ope"""
        result = {"result": "NG"}
        proj_id, message = CtrlOpe().delete_ope_by_id(user_id, screen_gid)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
        else:
            result["error"] = message
        return result


class ApiOpeStatus(Resource):
    # @auth.login_required
    def get(self, screen_gid):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_ope_status(screen_gid)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    # @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            proj_id, message = CtrlOpe().unlock_ope(data)
            if proj_id:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result

class ApiDisplay(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_displays_by_proj_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

class ApiCondition(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_conditions_by_proj_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

class ApiProperty(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_properties_by_proj_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

class ApiOpeType(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_opetypes_by_proj_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

class ApiEvent(Resource):
    # @auth.login_required
    def get(self, proj_id):
        result = {"result": "OK", "content": []}
        res = CtrlOpe().get_events_by_proj_id(proj_id)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result
