# -*- coding: UTF-8 -*-
from flask import request, current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_specification import CtrlSpecification
from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
from app.ctrl.ctrl_ds_doc import CtrlDsDoc


class ApiSpecification(Resource):
    @auth.login_required
    def get(self, proj_id=None, search_str=''):
        result = {"result": "NG", "content": [], "error": ''}
        try:
            spec = CtrlSpecification()
            spec_list = spec.get(proj_id, search_str)
            if spec_list:
                result = {"result": "OK", "content": spec_list}
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result["error"] = str(e)
        return result
    

class ApiDSDocSpec(Resource):
    @auth.login_required
    def get(self, doc_id, search_str=''):
        """
        获取文档下的式样书
        :param doc_id:
        :param search_str:
        :return:
        """
        result = {"result": "NG", "content": []}
        spec, status = CtrlDSRelSpec().get_by_doc_id(doc_id, search_str)
        micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        if spec:
            result["result"] = "OK"
            result["content"] = spec
        result["micro_ver"] = micro_ver
        return result

    @auth.login_required
    def post(self):
        """
        编辑文档下的式样书
        :return:
        """
        result = {"result": "NG", "doc_id": 0, 'error': ''}
        data_json = request.get_json()
        doc_id, error = CtrlDSRelSpec().add_doc_spec(data_json)
        if doc_id:
            micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
            result['result'] = "OK"
            result['doc_id'] = doc_id
            result["micro_ver"] = micro_ver
        else:
            result['error'] = error
        return result

#####################################################################################################################


class ApiUsecaseSpec(Resource):
    @auth.login_required
    def get(self, proj_id):
        """
        usecase选择式样书的接口
        :return:
        """
        result = {"result": "NG", "content": []}
        spec_list = CtrlDSRelSpec().get_project_spec(proj_id)
        if spec_list:
            result["result"] = "OK"
            result["content"] = spec_list
        return result




