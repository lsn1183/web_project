# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_project import CtrlProject


class ApiProject(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.add(data)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
        else:
            result["error"] = message
        return result

    def put(self, proj_id):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.update(proj_id, data)
        if proj_id:
            result = {"result": "OK", "error": message}
        else:
            result["error"] = message
        return result

    def get(self, page=None, size=None, proj_id=None, condition=None, manager=None):
        result = {"result": "NG", "content": []}
        project = CtrlProject()
        count, proj_info_list = project.get(proj_id, page, size, condition, manager)
        if proj_info_list:
            if page and size:
                result = {"result": "OK", "content": proj_info_list, "count": count}
            else:
                result = {"result": "OK", "content": proj_info_list}
        return result

    def delete(self, proj_id, commit_user):
        result = {"result": "NG", "error": ''}
        project = CtrlProject()
        flag, message = project.delete(proj_id, commit_user)
        if flag:
            result = {"result": "OK"}
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
        else:
            result["error"] = message
        return result


class ApiMergeCactusProject(Resource):
    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        accessToken = data.get('accessToken')
        proj_id = data.get('proj_id')
        page = data.get('page')
        size = data.get('size')
        condition = data.get('condition')
        manager = data.get('manager')
        result = {"result": "NG", "content": [], "error": ''}
        project = CtrlProject()
        error = project.synchronize_project(accessToken)
        if error:
            result['error'] = error
            return result
        count, proj_info_list = project.get(proj_id, manager, page, size, condition)
        if proj_info_list:
            if page and size:
                result = {"result": "OK", "content": proj_info_list, "count": count}
            else:
                result = {"result": "OK", "content": proj_info_list}
        return result


class ApiGetCactusProject(Resource):
    @auth.login_required
    def post(self):
        data = request.get_json(force=True)
        accessToken = data.get('accessToken')
        manager = data.get('manager')
        project = CtrlProject()
        result = {"result": "NG", "content": []}
        project_list = project.get_cactus_project(accessToken, manager)
        if project_list:
            result["result"] = 'OK'
            result["content"] = project_list
        return result


class ApiProjectFW(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.add_proj_fw(data)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
        else:
            result["error"] = message
        return result

    def get(self, proj_id):
        result = {"result": "NG"}
        project = CtrlProject()
        content = project.get_proj_fw(proj_id)
        if content:
            result = {"result": "OK", "content": content}
        return result


class ApiProjectTag(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.add_proj_tag(data)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
        else:
            result["error"] = message
        return result

    def get(self, proj_id):
        result = {"result": "NG"}
        project = CtrlProject()
        content = project.get_proj_tag(proj_id)
        if content:
            result = {"result": "OK", 'content': content}
        return result


class ApiProjectModel(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.add_proj_model(data)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
        else:
            result["error"] = message
        return result

    def get(self, proj_id):
        result = {"result": "NG"}
        project = CtrlProject()
        content = project.get_proj_model(proj_id)
        if content:
            result = {"result": "OK", 'content': content}
        return result


class ApiProjectGroup(Resource):
    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        data = request.get_json(force=True)
        project = CtrlProject()
        proj_id, message = project.add_proj_group(data)
        if proj_id:
            result = {"result": "OK", 'content': proj_id}
        else:
            result["error"] = message
        return result

    @auth.login_required
    def get(self, proj_id):
        result = {"result": "NG"}
        project = CtrlProject()
        content = project.get_proj_group(proj_id)
        if content:
            result = {"result": "OK", 'content': content}
        return result





