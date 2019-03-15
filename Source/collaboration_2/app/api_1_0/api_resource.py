# -*- coding: UTF-8 -*-
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_ds_section import CtrlDSResource


class ApiResource(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        content = CtrlDSResource().get_resource()
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result