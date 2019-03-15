# -*- coding: UTF-8 -*-
import platform
import os.path


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.25.99/collaboration'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DOC_PATH_ROOT = os.path.join('data', 'doc')
    IMG_PATH_ROOT = os.path.join('data', 'Image')
    LDAP_PROVIDER_URL = 'LDAP://apolo.storm'
    LDAP_DOMAIN = 'storm'
    ARCHITECTURE_SRV = 'http://192.168.8.152/'  # 框架服务器地址
    FILE_SRV_URL = 'http://192.168.25.99:8081'
    CACHE_TYPE = 'filesystem'
    CACHE_DIR = 'cache_root'
    JOBS = [
        {
            'id': 'job1',
            'func': 'update_index:update_anyplace_bugs',
            'args': '',
            'trigger': {
                'type': 'cron',
                # 'day_of_week': "mon-fri",
                'hour': 0,
                'minute': 1,
                # 'second': '*/5'
            }
        }
    ]
    SCHEDULER_API_ENABLED = True
    ES_SERVER_IP = '192.168.25.99'
    ES_SERVER_PORT = 9200
    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.25.99/collaboration_1123'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    HOST = "http://192.168.3.126:8080/"
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    if platform.system() == 'Windows':
        # Z盘映射地址：\\192.168.64.128\data
        DOC_PATH_ROOT = os.path.join(r'Y:\doc')
        IMG_PATH_ROOT = os.path.join(r'Y:\Image')
        ATTACH_PATH_ROOT = os.path.join(r'Y:\Attach')
        SPEC_PATH_ROOT = os.path.join(r'Y:\Spec')
        SPEC_PATH_TEMP = os.path.join(r'Y:\Spec\temp')
        DOXYGEN_PATH = os.path.join(r'Y:\Doxygen')
        TEMP_HTML_PATH_ROOT = os.path.join(r'Y:\temp\spec_html')
        FILE_SRV_URL = 'http://192.168.25.99:8081/'
        SPEC_CHANGE_URL = os.path.join(r'Y:')
        EXCEL_TO_HTM_URL = 'http://192.168.25.120:5000/ExcelToHtm'
        LASTEST_HISTORY_DIR = r'Y:'  # \\192.168.32.97\latest_history
    else:
        DOC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'doc')
        IMG_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Image')
        ATTACH_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data',
                                        'Attach')
        SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Spec')
        SPEC_PATH_TEMP = os.path.join(os.path.expanduser('~'), 'data', 'Spec', 'temp')
        DOXYGEN_PATH = os.path.join(os.path.expanduser('~'), 'data', 'Doxygen')
        FILE_SRV_URL = 'http://192.168.25.99:8081/'
        SPEC_CHANGE_URL = os.path.join(os.path.expanduser('~'), 'data')
        LASTEST_HISTORY_DIR = os.path.join(os.path.expanduser('~'), 'latest_history')  # \\192.168.32.97\latest_history
        EXCEL_TO_HTM_URL = 'http://192.168.25.120:5000/ExcelToHtm'


class ReleaseConfig(Config):
    HOST = "http://192.168.3.126:8080/"
    LOGIN_URL = HOST + "cactuswebapi/auth/login"
    PROJ_URL = HOST + "cactuswebapi/project/list"
    PROJECTGROUP_URL = HOST + "cactuswebapi/projectgroup/list"
    if platform.system() == 'Windows':
        # R盘映射地址：\\192.168.64.127\data
        DOC_PATH_ROOT = os.path.join(r'R:\doc')
        IMG_PATH_ROOT = os.path.join(r'R:\Image')
        ATTACH_PATH_ROOT = os.path.join(r'R:\Attach')
        SPEC_PATH_ROOT = os.path.join(r'R:\Spec')
        FILE_SRV_URL = 'http://192.168.64.127'
    else:
        DOC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'doc')
        IMG_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Image')
        ATTACH_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data',
                                        'Attach')
        SPEC_PATH_ROOT = os.path.join(os.path.expanduser('~'), 'data', 'Spec')
        FILE_SRV_URL = 'http://192.168.64.127'
    EXCEL_TO_HTM_URL = 'http://192.168.25.120:5000/ExcelToHtm'  # TODO@hcY: 到时要填上release机器的址址


config = {
    'development': DevelopConfig,
    'release': ReleaseConfig,
    'default': DevelopConfig
}
