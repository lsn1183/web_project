# -*- coding: UTF-8 -*-'
from flask import request
from flask import current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_group import CtrlGroup


class ApiGroup(Resource):
    @auth.login_required
    def get(self, group_name=None):
        """
        获取组的信息
        :param group_name:
        :return:
        """
        result = {"result": "NG"}
        ctrl_obj = CtrlGroup()
        content = ctrl_obj.get_groups(group_name)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result

    def post(self):
        """
        新增组
        :return:
        """
        json_data = request.get_json(force=True)
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.add_group(json_data)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result

    def put(self):
        """
        修改组信息
        :return:
        """
        json_data = request.get_json(force=True)
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.update_group(json_data)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result

    def delete(self, group_id):
        """
        删除组
        :param group_id:
        :return:
        """
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.delete_group(group_id)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result


class ApiGroupMembers(Resource):
    @auth.login_required
    def get(self, group_id=None):
        """
        获取组成员信息
        :param group_id:
        :return:
        """
        result = {"result": "NG"}
        ctrl_obj = CtrlGroup()
        content = ctrl_obj.get_group_members(group_id)
        if content:
            result["result"] = "OK"
            result["content"] = content
        return result

    def post(self):
        """
        添加组成员
        :return:
        """
        json_data = request.get_json(force=True)
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.add_group_members(json_data)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result

    def put(self):
        """
        编辑组成员角色
        :return:
        """
        json_data = request.get_json(force=True)
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.update_member_role(json_data)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result

    def delete(self, group_id, user_id):
        """
        删除组成员
        :param group_id:
        :param user_id:
        :return:
        """
        ctrl_obj = CtrlGroup()
        result = {'result': 'NG', 'error': ''}
        try:
            ctrl_obj.delete_member(group_id, user_id)
            result['result'] = "OK"
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            result['error'] = str(e)
        return result


class ApiCactusGroups(Resource):
    @auth.login_required
    def post(self):
        """
        从cactus上拿项目的组信息
        :return:
        """
        result = {"result": "NG"}
        from app.ctrl.ctrl_group import CtrlGroup
        data_json = request.get_json(force=True)
        accessToken = data_json.get('accessToken')
        proj_id = data_json.get('proj_id')
        group_list = CtrlGroup().get_project_group(accessToken, proj_id)
        if group_list:
            result["result"] = "OK"
            result['content'] = group_list
        return result


class ApiModelGroupMessage(Resource):
    """
    从cactus上拿模块关联组的信息
    :return:
    """

    @auth.login_required
    def post(self):
        result = {"result": "NG"}
        from app.ctrl.ctrl_group import CtrlGroup
        data_json = request.get_json(force=True)
        proj_id = data_json.get('proj_id')
        model_id = data_json.get('model_id')
        accessToken = data_json.get('accessToken')
        group_message, model_name = CtrlGroup().get_cactus_group_mesage(proj_id, model_id, accessToken)
        if group_message:
            result["result"] = "OK"
            result['content'] = group_message
            result['model_name'] = model_name
        return result