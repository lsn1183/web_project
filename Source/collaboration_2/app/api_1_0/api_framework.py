# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_framework import CtrlFramework
from app.ctrl.ctrl_framework import CtrlFwModel
from app.import_model.import_fw_model import ImportFwModel
from app.import_model.import_project_model import ImportProjectModel


class ApiFramework(Resource):
    @auth.login_required
    def get(self, type="FW", fw_id=None):
        """
        根据类型获取平台相关信息
        :param type:
        :param fw_id:
        :return:
        """
        result = {'result': 'NG'}
        if type == "FW":
            obj = CtrlFramework()
        elif type == "FW_MODEL":
            obj = CtrlFwModel()
        content = obj.get(fw_id)
        if content:
            result['result'] = 'OK'
            result['content'] = content
        return result

    def post(self):
        """
        新增或修改平台基本信息以及相关模块
        :return: 平台id
        """
        result = {"result": "NG"}
        data_json = request.get_json(force=True)
        type = data_json.get("type")
        if type == "FW":
            obj = CtrlFramework()
        elif type == "FW_MODEL":
            obj = CtrlFwModel()
        fw_id, error = obj.add(data_json)
        if fw_id:
            result = {"result": "OK", 'content': fw_id}
        else:
            result["error"] = error
        return result

    def delete(self, fw_id, commit_user):
        result = {"result": "NG", "error": ''}
        obj = CtrlFramework()
        flag, message = obj.delete(fw_id, commit_user)
        if flag:
            result = {"result": "OK"}
        else:
            result['error'] = message
        return result


class ApiGetCactusFw(Resource):
    @auth.login_required
    def post(self, ):
        data = request.get_json(force=True)
        accessToken = data.get('accessToken')
        manager = data.get('manager')
        result = {"result": "NG", "content": []}
        fw_list = CtrlFramework().get_cactus_fw(accessToken, manager)
        if fw_list:
            result['result'] = 'OK'
            result['content'] = fw_list
        return result


class ApiFwProject(Resource):
    @auth.login_required
    def get(self, fw_id=None):
        result = {'result': 'NG'}
        content = CtrlFramework().get_fw_project(fw_id)
        if content:
            result['result'] = 'OK'
            result['content'] = content
        return result


class ApiImportFWModel(Resource):
    @auth.login_required
    def get(self, fw_name=None):
        """测试用--平台模块导入
        :param fw_name:
        :return:
        """
        result = {'result': 'NG'}
        fw_name = "iAuto2.0"
        file = r"C:\Users\hcz\Desktop\iAuto_Architecture_MEUDCU_For17Cy_20150410.xlsx"
        sheet_names = ["MEU責務", "DCU責務"]
        content = ImportFwModel().import_model(fw_name, file, sheet_names)
        if content:
            result['result'] = 'OK'
            result['content'] = content
        return result


class ApiImportProjectModel(Resource):
    @auth.login_required
    def get(self, project_name='17cy'):
        """测试用--平台模块导入
        :param fw_name:
        :return:
        """
        result = {'result': 'NG'}
        rst, msg = ImportProjectModel().import_model(project_name)
        if rst:
            result['result'] = 'OK'
            result['content'] = ''  # TODO@hcz: 返回新的模块
        result['msg'] = msg
        return result
        # sqlcmd = """
        # SELECT a.tag_id, tag, c.doc_id, doc_type, doc_title, content, committer, summary, sub_cat
        #   FROM public.doc_tags as a
        #   inner join (
        #   SELECT tag_id, tag
        #       FROM public.doc_tag_category
        #       WHERE parent_tag_id = 6 -- '技术专题'
        #  ) as b
        #  on a.tag_id = b.tag_id
        #  left join public.docs as c
        #  on a.doc_id = c.doc_id
        #  --where tag = '应用程序'
        #  order by a.tag_id, doc_id
        # """
        # import pandas as pd
        # from app.db import db
        # df = pd.read_sql(sqlcmd, db.session.bind)
        # df.to_excel('doc.xls')