# -*- coding: UTF-8 -*-
from flask import request
from token_manage import auth
from flask_restful import Resource
from app.ctrl.ctrl_doc_tag import CtrlDocTag, TAG_RATE_ALL


class ApiDocTagCat(Resource):
    @auth.login_required
    def post(self):
        req_json = request.get_json(force=True)
        ctrl_tag = CtrlDocTag()
        result = ctrl_tag.add(req_json)
        return result

    @auth.login_required
    def put(self, tag_id=0):
        req_json = request.get_json(force=True)
        ctrl_tag = CtrlDocTag()
        return ctrl_tag.update(tag_id, req_json)

    @auth.login_required
    def get(self, rate=TAG_RATE_ALL, username=''):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        tag_tree = ctrl_tag.get_tag_tree(rate=rate, username=username)
        if tag_tree:
            result["result"] = "OK"
            result["content"] = tag_tree
        return result

    @auth.login_required
    def delete(self, tag_id):
        obj = CtrlDocTag()
        result = obj.delete(tag_id)
        return result


class ApiDocTagIncludeNumber(Resource):
    @auth.login_required
    def get(self, user_id=1, rate=TAG_RATE_ALL, username=''):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        tag_tree = ctrl_tag.get_tag_tree_include_head(user_id, rate=rate, username=username)
        if tag_tree:
            result["result"] = "OK"
            result["content"] = tag_tree
        return result


class ApiDocTagRequiredGroups(Resource):
    @auth.login_required
    def get(self):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        required_groups = ctrl_tag.get_required_tags()
        if required_groups:
            result["result"] = "OK"
            result["content"] = required_groups
        return result


class ApiDocTagProject(Resource):
    @auth.login_required
    def get(self, classify):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        content = ctrl_tag.get_tag_for_proj(classify)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result