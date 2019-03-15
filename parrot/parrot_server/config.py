# -*- coding: UTF-8 -*-
import platform
import os.path


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.64.174/quotation_0114'
    SQLALCHEMY_POOL_SIZE = 100
    SQLALCHEMY_MAX_OVERFLOW = -1
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOC_PATH_ROOT = os.path.join('data', 'doc')
    IMG_PATH_ROOT = os.path.join('data', 'Image')
    LDAP_PROVIDER_URL = 'LDAP://apolo.storm'
    LDAP_DOMAIN = 'storm'
    ARCHITECTURE_SRV = 'http://192.168.8.152/'  # 框架服务器地址
    FILE_SRV_URL = 'http://192.168.64.128:8081'
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = 'cache_root'
    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.64.128/quotation_0114'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "http://192.168.3.126:8080/"
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    if platform.system() == 'Windows':
        # Z盘映射地址：\\192.168.64.128\data
        SPEC_PATH_ROOT = os.path.join(r'Z:\Input')
        SPEC_PATH_TEMP = os.path.join(r'Z:\Input\temp')
        FILE_SRV_URL = 'http://192.168.64.128:8081'
        SPEC_CHANGE_URL = os.path.join(r'Z:')
    else:
        SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Input')
        SPEC_PATH_TEMP = os.path.join(os.path.expanduser('~'), 'data', 'Input', 'temp')
        FILE_SRV_URL = 'http://192.168.64.128:8081'
        SPEC_CHANGE_URL = os.path.join(os.path.expanduser('~'), 'data')


class ReleaseConfig(Config):
    HOST = "http://192.168.3.126:8080/"
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    if platform.system() == 'Windows':
        # R盘映射地址：\\192.168.64.127\data
        SPEC_PATH_TEMP = os.path.join(r'R:\Input\temp')
        SPEC_PATH_ROOT = os.path.join(r'R:\Input')
        FILE_SRV_URL = 'http://192.168.64.127'
        SPEC_CHANGE_URL = os.path.join(r'Z:')
    else:
        SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Input')
        SPEC_PATH_TEMP = os.path.join(os.path.expanduser('~'), 'data', 'Input', 'temp')
        FILE_SRV_URL = 'http://192.168.64.127'
        SPEC_CHANGE_URL = os.path.join(os.path.expanduser('~'), 'data')


config = {
    'development': DevelopConfig,
    'release': ReleaseConfig,
    'default': DevelopConfig
}
