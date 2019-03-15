# -*- coding: UTF-8 -*-
from flask_restful import Resource
from flask import request
import json
from search.spec_search import SpecSearch
from search.es_manager import EsManager
from search.es_anyplace import EsAnyplace
from app.ctrl.ctrl_anyplace import CtrlAnyplance


class ApiFunSearch(Resource):
    def get(self, proj_name, search):
        result = {"result": "NG", "content": ""}
        search_obj = SpecSearch.instance()
        content = search_obj.fun_search(proj_name, search)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result


class ApiBugSearch(Resource):
    def post(self):
        result = {"result": "NG", "content": []}
        # ad = request
        data = json.loads(request.data)
        content = CtrlAnyplance().search_field_by_user(data.get("value"), data.get("user"),
                                                       data.get("size"), data.get("page"))
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result


class ApiAnyPlaceInfo(Resource):
    def post(self):
        result = {"result": "NG", "content": ""}
        # ad = request
        data = json.loads(request.data)
        content = CtrlAnyplance().search_one_anyplace(data.get("value"))
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result


class ApiKeyList(Resource):
    # def get(self):
    #     result = {"result": "NG", "content": ""}
    #     es_manager = EsManager.instance()
    #     es = es_manager.get_curr_anyplace_index()
    #     content = es.find_key_name()
    #     # content = es.find_key_name_by_user(user)
    #     if content:
    #         result["result"] = "OK"
    #         result["content"] = content
    #     return result

    def get(self, user):
        result = {"result": "NG", "content": ""}
        content = CtrlAnyplance().find_key_name_by_user(user)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result
