# coding: utf-8
import os
from Source.spec2db_server.arl.arl_group import ArlUser
import ldap
ldapServer = 'LDAP://apolo.storm'
domain = 'storm'


def login(username, password):
    try:
        conn = ldap.initialize(ldapServer)
        domainUserName = domain + '\\' + username
        conn.simple_bind_s(domainUserName, password)
        return {'result': True}
    except:
        return {'result': False}


def login2(user_name, pass_word):
    user_obj = ArlUser()
    user_data = user_obj.login(user_name, pass_word)
    if user_data:
        return {'result': True, 'content': user_data}
    else:
        return {'result': False}


def register(user_name, pass_word, email):
    obj = ArlUser()
    user_info = obj.register(user_name, pass_word, email)
    if user_info:
        return {'result': True, 'content': user_info}
    else:
        return {'result': False}


if __name__ == "__main__":
    username = "hongcz"  # ldap中用户名
    password = "fhMH99Jo"  # ldap中密码
    print login(username, password)
