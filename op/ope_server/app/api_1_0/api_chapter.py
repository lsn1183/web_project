from flask_restful import Resource, request
from flask import current_app
from flask import g
from token_manage import serializer
import json
import os
from token_manage import auth
from app.ctrl.ctrl_ope import CtrlOpe
from app.ctrl.ctrl_chapter import CtrlChapter


class ApiChapter(Resource):
    # @auth.login_required
    def get(self, screen_gid, _type):
        """获取chapter表格信息"""
        result = {"result": "OK", "content": []}
        res = CtrlChapter().get_chapter(screen_gid, _type)
        if res:
            result["result"] = "OK"
            result["content"] = res
        return result

    # @auth.login_required
    def post(self, _type):
        """更新表格"""
        result = {"result": "NG"}
        data = request.get_json(force=True)
        if data:
            res, message = CtrlChapter().update_chapter(_type, data)
            if res:
                result = {"result": "OK", 'content': message}
            else:
                result["error"] = message
        else:
            result["error"] = "请不要传空数据"
        return result