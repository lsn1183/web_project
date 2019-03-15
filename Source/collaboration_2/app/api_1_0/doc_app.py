# -*- coding: UTF-8 -*-
import os
from flask import request
from flask_restful import Resource
from token_manage import auth
from flask import current_app
from app.db.doc import Doc
from app.ctrl.ctrl_doc import CtrlDoc
from app.ctrl.ctrl_knowledge import CtrlKnowledge


class DocAppUpdate(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ''}
        obj = CtrlDoc()
        rst, message = obj.update(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result


class DocApp(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ''}
        obj = CtrlDoc()
        rst, message = obj.add(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result

    def get(self, doc_id):
        result = {"result": "NG", "content": ''}
        obj = CtrlDoc()
        doc_info = obj.get_by_key_id(doc_id)
        if doc_info:
            doc_info['path'] = ''
            doc_info['file'] = ''
            if doc_info.get("doc_type") == 'url':
                doc_info['path'] = doc_info.get("content")
                doc_info["content"] = ''
            elif doc_info.get("doc_type") == 'file':
                doc_info['file'] = doc_info.get("content")
                doc_info["content"] = ''
            result["result"] = "OK"
            result["content"] = doc_info
        return result

    def put(self):
        """update"""
        result = {"result": "NG", "error": ''}
        obj = CtrlDoc()
        rst, message = obj.update(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result

    def delete(self, doc_id):
        result = {"result": "NG", "error": ''}
        obj = CtrlDoc()
        rst, message = obj.delete(doc_id)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result


class DocApp2(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG", "error": ''}
        obj = CtrlDoc()
        rst, message = obj.add2(request)
        if not rst:
            result["error"] = message
        else:
            result["result"] = "OK"
        return result


class DocByTag(Resource):
    @auth.login_required
    def get(self, page, size, condition=None, username=None, tag_id=None):
        result = {"result": "NG", "content": [], "count": 0}
        obj = CtrlDoc()
        count, doc_list = obj.get_by_tag(condition, tag_id, username, page, size)
        if doc_list:
            result["result"] = "OK"
            result["content"] = doc_list
            result["count"] = count
        return result


class FailureModeByTag(Resource):
    @auth.login_required
    def get(self, tag_id=None):
        result = {"result": "NG", "content": [], "count": 0}
        obj = CtrlDoc()
        failuremode_list = obj.get_failuremode_by_tag(tag_id)
        if failuremode_list:
            result["result"] = "OK"
            result["content"] = failuremode_list
        return result


class DocByFailureMode(Resource):
    @auth.login_required
    def get(self, page, size, failure_mode=None):
        result = {"result": "NG", "content": [], "count": 0}
        obj = CtrlDoc()
        condition = None
        username = None
        count, doc_list = obj.get_by_failure_mode(condition, failure_mode,
                                                  username, page, size)
        if doc_list:
            result["result"] = "OK"
            result["content"] = doc_list
            result["count"] = count
        return result


class DocGroupUser(Resource):
    @auth.login_required
    def get(self, create_time=None):
        result = {"result": "NG", "content": ''}
        obj = CtrlDoc()
        content = obj.get_group_users(create_time)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result


class ApiKnowledgeClassify(Resource):
    @auth.login_required
    def get(self, knowledge_only='right', knowledge=''):
        result = {"result": "NG", "content": ''}
        obj = CtrlKnowledge()
        content = obj.get_knowledge_classify(knowledge_only=knowledge_only,
                                             knowledge=knowledge)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result

    @auth.login_required
    def post(self):
        """
        KnowledgeClassify导入，暂时不上线。
        :return:
        """
        result = {"result": "NG", "error": ''}
        file_upload = request.files['file']
        fileName = file_upload.filename
        file_path = os.path.join('data', 'KnowledgeClassify')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        file_url = os.path.join(file_path, fileName)
        file_upload.save(file_url)  # 保存上传的文件
        obj = CtrlKnowledge()
        flag, message = obj.import_excel(file_url)
        if flag:
            result["result"] = "OK"
        else:
            result["error"] = message
        return result





