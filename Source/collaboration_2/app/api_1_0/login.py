# -*- coding: UTF-8 -*-
from flask_restful import Resource, request
# import ldap
from flask import current_app
from flask import g
from token_manage import serializer
from app.ctrl.ctrl_user import CtrlUser
from app.api_1_0.api_cactus import ApiCactus


class Root(Resource):
    def get(self):
        return "This is iDesign Server."


class Login(Resource):
    def get(self):
        from flask_restful import reqparse
        parser = reqparse.RequestParser()
        parser.add_argument('username')
        parser.add_argument('password')
        args = parser.parse_args()

        username = args.get('username')
        password = args.get('password')
        # result = self.login(username, password)
        db_password = self.get_password(username)
        if db_password:
            if db_password == password:
                user = CtrlUser().register(username=username)
                result = {'result': True, 'accessToken': ''}
                result.update(user)
            else:
                result = {'result': False, "error": u'登录失败，请输入正确的用户名或密码！'}
        else:
            result = self.login_from_cactus(username, password)

        return result

    def post(self):
        json_data = request.get_json(force=True)
        username = json_data.get('username')
        password = json_data.get('password')
        # result = self.login(username, password)
        db_password = self.get_password(username)
        if db_password:
            if db_password == password:
                user = CtrlUser().register(username=username)
                result = {'result': True, 'accessToken': ''}
                result.update(user)
            else:
                result = {'result': False, "error": u'登录失败，请输入正确的用户名或密码！'}
        else:
            result = self.login_from_cactus(username, password)
        if result.get('result'):
            g.username = username
            g.password = password
            token = serializer.dumps({'username': username})
            result['idesignToken'] = str(token, encoding='utf-8')
        return result

    def get_password(self, username):
        user = CtrlUser().get_user_by_name(username)
        if user:
            if user.user_type == 'TEST':
                return user.password
        return None

    # def login(self, username, password):
    #     try:
    #         conn = ldap.initialize(current_app.config["LDAP_PROVIDER_URL"])
    #         domain_username = current_app.config["LDAP_DOMAIN"] + '\\' + username
    #         conn.simple_bind_s(domain_username, password)
    #         user = CtrlUser().register(username=username)
    #         if user:
    #             result = {'result': True}
    #             result.update(user)
    #             return result
    #         else:
    #             current_app.logger.info("[注册用户失败], username=%s" % username)
    #             return {'result': False, "error": u'注册用户失败!'}
    #     except Exception as e:
    #         current_app.logger.info("[Login][exception]%s" % e)
    #         return {'result': False, "username": '', "error": str(e)}

    def login_from_cactus(self, work_id, password):
        """
        登录走cactus
        :param work_id:
        :param password:
        :return:
        """
        employ = {"employeeNo": work_id,
                  "password": password,
                  "clientType": 0
                  }
        user_dict = ApiCactus().cactus_login(employ)
        if user_dict:
            username = user_dict.get('username')
            accessToken = user_dict.get('accessToken')
            work_id = user_dict.get('work_id')
            user = CtrlUser().register(username=username, work_id=work_id)
            if user:
                result = {'result': True, 'accessToken': accessToken}
                result.update(user)
                return result
            else:
                current_app.logger.info("[注册用户失败], username=%s" % username)
                return {'result': False, "error": u'注册用户失败!'}
        else:
            return {'result': False, "error": u'登录失败，请输入正确的用户名或密码！'}




