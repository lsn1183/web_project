# -*- coding: UTF-8 -*-
from flask import request
from flask_restful import Resource
from app.ctrl.ctrl_model import CtrlModel
from app.ctrl.ctrl_doc_tag import CtrlDocTag
from token_manage import auth
from app.db import cache


class ApiModel(Resource):
    @auth.login_required
    def get(self, page=None, size=None, model_id=None, condition=None):
        """
        获取模块
        :param model_id:
        :return:
        """
        result = {"result": "NG"}
        count, content = CtrlModel().get(page, size, model_id, condition)
        if content:
            result['result'] = 'OK'
            result['content'] = content
            if count:
                result['count'] = count
        return result

    @auth.login_required
    def post(self):
        """
        新增或修改模块
        :return:
        """
        result = {"result": "NG"}
        data_json = request.get_json(force=True)
        obj = CtrlModel()
        flag, error = obj.add(data_json)
        if flag:
            result = {"result": "OK", 'content': flag}
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
        else:
            result["error"] = error
        return result

    @auth.login_required
    def delete(self, model_id):
        """
        删除模块
        :return:
        """
        result = {"result": "NG", "error": ''}
        obj = CtrlModel()
        flag, message = obj.delete(model_id)
        if flag:
            result = {"result": "OK", "error": message}
        else:
            result["error"] = message
        return result


class ApiModelDSDoc(Resource):
    @auth.login_required
    def get(self, page, size, fw_id = None, proj_id=None, model_id=None, user='', doc_type="ALL", condition=None):
        """
        :param user:
        :param doc_type:
        :return:基本设计或详细设计下的文档
        """
        result = {"result": "NG"}
        ctrl_model = CtrlModel()
        count, docs = ctrl_model.get_doc_by_type(user, fw_id, model_id, proj_id, doc_type, page, size, condition)
        if docs:
            # model_doc_tree = ctrl_model.model_doc_tree(docs)
            result["result"] = "OK"
            result["content"] = docs
            result["count"] = count
        return result

#
# class ApiModelTag(Resource):
#     def get(self, model_id):
#         """
#         :param model_id:
#         :return:获取Model下的所有TAG
#         """
#         result = {"result": "NG"}
#         ctrl_model = CtrlModel()
#         tags = ctrl_model.get_tag_by_model(model_id)
#         if tags:
#             result["result"] = "OK"
#             result["content"] = tags
#         # tags = [{"tag_id": 106, "tag": "NativeAPP"},
#         #         {"tag_id": 107, "tag": "Html5APP"},
#         #        ]
#         return result


class ApiModelTags(Resource):
    @auth.login_required
    def get(self, model_id, doc_type=None):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        tag_tree = ctrl_tag.get_tag_tree(model_id=model_id, doc_type=doc_type)
        if tag_tree:
            result["result"] = "OK"
            result["content"] = tag_tree
        return result


class ApiSectionTags(Resource):
    @auth.login_required
    def get(self, sec_id):
        result = {"result": "NG", "content": []}
        ctrl_tag = CtrlDocTag()
        tag_tree = ctrl_tag.get_tag_tree(sec_id=sec_id)
        if tag_tree:
            result["result"] = "OK"
            result["content"] = tag_tree
        return result


class ApiModelTree(Resource):
    @auth.login_required
    def get(self, user_id=None):
        result = {"result": "NG", "content": []}
        ctrl_model = CtrlModel()
        model_tree = ctrl_model.get_model_tree(user_id=user_id)
        if model_tree:
            result["result"] = "OK"
            result["content"] = model_tree
        return result


class ApiDesignTop(Resource):
    # @auth.login_required
    def get(self, proj_id, type="ALL"):
        result = {"result": "NG", "content": []}
        # ctrl_model = CtrlModel()
        # print(id(ctrl_model))
        # result_data = ctrl_model.get_model_top(proj_id, type)
        result_data = get_model_top(proj_id, type)
        if result_data:
            result["content"] = result_data
            result["result"] = "OK"
        return result


@cache.memoize(timeout=3600 * 12)  # 12 hours
def get_model_top(proj_id, type):
    ctrl_model = CtrlModel()
    result_data = ctrl_model.get_model_top(proj_id, type)
    return result_data


def del_cache_model_top(proj_id):
    print('delete_memoized: get_model_top, proj_id=%s' % proj_id)
    # get_model_top之后的参数要么写全，要么都不写。不写参数，就见删除所有的。
    cache.delete_memoized(get_model_top, proj_id, 'ALL')
    cache.delete_memoized(get_model_top, proj_id, 'PART')


class ApiTestDelCache(Resource):
    def get(self, proj_id):
        del_cache_model_top(proj_id)
        return {'result': 'OK'}


class ApiModelAuthor(Resource):
    @auth.login_required
    def get(self, proj_id, model_id):
        result = {"result": "NG", "content": []}
        ctrl_model = CtrlModel()
        model_authors = ctrl_model.get_authors(proj_id, model_id)
        if model_authors:
            result["result"] = "OK"
            result["result"] = "OK"
            result["content"] = model_authors
        return result


class ApiSubModel(Resource):
    @auth.login_required
    def get(self, proj_id):
        result = {"result": "NG", "content": []}
        ctrl_model = CtrlModel()
        data_list = ctrl_model.get_sub_model(proj_id)
        if data_list:
            result["result"] = "OK"
            result["content"] = data_list
        return data_list


class ApiModelRefGet(Resource):
    """
    获取项目指定人的关联模块
    :return:
    """

    @auth.login_required
    def post(self):
        result = {"result": "NG", "content": [], "error": ''}
        data_json = request.get_json(force=True)
        ctrl_model = CtrlModel()
        data_list, error = ctrl_model.get_model_ref_model(data_json)
        if not error:
            result["result"] = "OK"
            result["content"] = data_list
        else:
            result['error'] = error
        return result

    def get(self, doc_id):
        """获取该设计书所属模块的关联模块
        :param doc_id:
        :return:
        """
        result = {"result": "NG", "content": [], "error": ''}
        ctrl_model = CtrlModel()
        model_list, error = ctrl_model.get_model_ref_by_doc_id(doc_id)
        if model_list:
            result["result"] = "OK"
            result["content"] = model_list
        result["error"] = error
        return result


class ApiModelRefPost(Resource):
    @auth.login_required
    def post(self):
        """
        编辑项目模块关系
        :return:
        """
        result = {"result": "NG"}
        data_json = request.get_json(force=True)
        obj = CtrlModel()
        flag, error = obj.update_model_ref_model(data_json)
        if flag:
            result = {"result": "OK", 'content': flag}
        else:
            result["error"] = error
        return result
