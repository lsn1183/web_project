# -*- coding: UTF-8 -*-
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_export_doc import CtrlExportDoc


class ApiExportDoc(Resource):
    @auth.login_required
    def get(self, proj_id, model_id=None, doc_type=None, doc_id=None):
        result = {"result": "NG", "msg": '', "file_path": ''}
        rst, msg, file_path = CtrlExportDoc().do_export(proj_id, model_id,
                                                        doc_type, doc_id)
        if rst:
            result["result"] = "OK"
            result["file_path"] = file_path
        else:
            result["msg"] = msg
        return result

    def post(self):
        pass

