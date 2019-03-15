# -*- coding: UTF-8 -*-
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_ds_drbfm import CtrlDSFailure


class ApiDSFailure(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        failures = CtrlDSFailure().get_failures()
        if failures:
            result["content"] = failures
            result["result"] = "OK"
        return result
