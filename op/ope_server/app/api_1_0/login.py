from flask_restful import Resource, request
from flask import current_app
from flask import g
from token_manage import serializer
import json
from requests import post
from app.ctrl.ctrl_user import CtrlUser



class Root(Resource):
    def get(self):
        return "This is Koala Server."


class Login(Resource):

    def post(self):
        json_data = request.get_json(force=True)
        username = json_data.get('username')
        password = json_data.get('password')
        result = self.login_from_cactus(username, password)
        if result.get('result') == "OK":
            g.username = username
            g.password = password
            token = serializer.dumps({'username': username})
            result['LoginToken'] = str(token, encoding='utf-8')
        return result


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
        user_dict = self.cactus_login(employ)
        if user_dict:
            username = user_dict.get('username')
            work_id = user_dict.get("work_id")
            user = CtrlUser().register(username=username, work_id=work_id)
            if user:
                result = {'result': "OK"}
                result.update(user)
                return result
            else:
                current_app.logger.info("[注册用户失败], username=%s" % username)
                return {'result': "NG", "error": u'注册用户失败!'}
        else:
            return {'result': "NG", "error": u'登录失败，请输入正确的用户名或密码！'}

    def cactus_login(self, employ):
        login_post = current_app.config["LOGIN_URL"]
        r = post(login_post, employ)
        user_dict = dict()
        if r.status_code == 200:  # 成功
            result = json.loads(r.content)
            if result.get("code") == 0:  # 表示成功
                accessToken = result.get("info").get("accessToken")
                refreshToken = result.get("info").get("refreshToken")
                username = result.get("info").get("userName")
                work_id = result.get("info").get("employeeNo")
                user_dict = {'username': username, "accessToken": accessToken, "work_id": work_id}
        return user_dict

