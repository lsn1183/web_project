# -*- coding: UTF-8 -*-
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_ds_doc_template import CtrlDSDocTemplate


class ApiDSDocTemplate(Resource):
    @auth.login_required
    def get(self, doc_type=''):
        result = {"result": "NG"}
        doc_templates = CtrlDSDocTemplate().get_doc_template(doc_type)
        if doc_templates:
            result["content"] = doc_templates
            result["result"] = "OK"
        return result
