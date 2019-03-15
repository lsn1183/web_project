from flask_restful import Resource
from flask import request
from token_manage import auth
from app.ctrl.ctrl_import_doc import CtrlImportDoc


class ApiWebImportDoc(Resource):
    # def get(self):
    #     """测试"""
    #     file_url = "import_root/DetailDesign_HwyView1.xlsx"
    #     proj_id = 10004
    #     model_id = 4
    #     doc_type = "DETAIL"
    #     creator = "Admin"
    #     flag, error = CtrlImportDoc().test_do_import(file_url, proj_id, model_id, doc_type, creator)
    #     print(flag, error)
    @auth.login_required
    def post(self):
        result = {"result": "NG", 'error': ''}
        rst, error = CtrlImportDoc().do_import(request)
        if not rst:
            result["error"] = error
        else:
            result["result"] = "OK"
        return result


