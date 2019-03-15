# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_ds_scene import CtrlDSScene
from app.ctrl.ctrl_ds_doc import CtrlDsDoc


class ApiDSScene(Resource):
    @auth.login_required
    def get(self, doc_id=0, type='change'):
        result = {"result": "NG"}
        if not doc_id:  # 取所有场景(TAG)
            # scenes = CtrlDSScene().get_scene()
            scenes = CtrlDSScene().get_scene3()
        else:
            # scenes = CtrlDSScene().get_scene_by_sec(doc_id)
            if type == 'change':  # 修改点、影响点
                scenes = CtrlDSScene().get_scene_by_doc2(doc_id)
            else:  # 已选择
                scenes = CtrlDSScene().get_scene_by_doc(doc_id)
        micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        result["micro_ver"] = micro_ver
        if scenes:
            result['result'] = "OK"
            result['content'] = scenes
        return result

    def post(self):
        result = {"result": "NG", "doc_id": 0, 'error': ''}
        data_json = request.get_json()
        type = data_json.get('type')
        if type == "SCENE":
            doc_id, error = CtrlDSScene().add_scene(data_json)
        elif type == "CHANGE":
            doc_id, error = CtrlDSScene().add2(data_json)
        if doc_id:
            # micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
            result['result'] = "OK"
            result['doc_id'] = doc_id
            # result["micro_ver"] = micro_ver
        else:
            result['error'] = error
        return result


class ApiDSTag(Resource):
    @auth.login_required
    def get(self, doc_id=0):
        """获取设计文档关系的场景(场景的考虑点使用)"""
        result = {"result": "NG", 'content': []}
        if doc_id:  # 取所有场景(TAG)
            # scenes = CtrlDSScene().get_scene()
            tags = CtrlDSScene().get_tags_by_doc_id(doc_id)
            if tags:
                result['result'] = "OK"
                result['content'] = tags
            micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
            result["micro_ver"] = micro_ver
        return result

    def post(self):
        """
        保存場景的模快下的考慮點
        :return:
        """
        result = {"result": "NG", "doc_id": 0, 'error': ''}
        data_json = request.get_json()
        doc_id, error = CtrlDSScene().add_tag_considers(data_json)
        if doc_id:
            result['result'] = "OK"
            result['doc_id'] = doc_id
        else:
            result['error'] = error
        return result