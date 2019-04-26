from flask_restful import Resource
from app.api_1_0.login import Login
from app.api_1_0.api_project import ApiProjectList, ApiProject, ApiProjectOpe
from app.api_1_0.api_ope import *
from app.api_1_0.api_chapter import ApiChapter
from app.api_1_0.api_import import ApiScreenJsonImport, ApiScreenJsonExport

class Root(Resource):
    def get(self):
        return "This is OPE Server."

class Api_1_0():
    def __init__(self, api):
        # Home
        api.add_resource(Root, '/')
        # 登录
        api.add_resource(Login, '/login')
        # 项目
        api.add_resource(ApiProjectList,
                         '/Project/List',                   # 获取项目列表
                         '/Project/add')                    # 添加项目
        api.add_resource(ApiProject,
                         '/Project/<int:proj_id>',          # 获取某个项目信息
                         '/Project/delete/<int:proj_id>',   # 删除某个项目信息
                         '/Project/update')                 # 添加项目
        api.add_resource(ApiProjectOpe,
                         '/Project/ope/<int:proj_id>')      # 获取项目下的ope列表
        # ope(screen)
        api.add_resource(ApiOpe,
                         '/Ope/lock',                       # 锁定某本Ope
                         '/Ope/delete/<int:user_id>/<int:screen_gid>',    # 删除某本Ope
                         '/Ope/<int:screen_gid>')           # 获取单本Ope的基本信息
        api.add_resource(ApiOpeStatus,
                         '/Ope/unlock',                     # 解锁某本Ope
                         '/Ope/status/<int:screen_gid>')    # 获取单本Ope的锁状态
        api.add_resource(ApiDisplay,
                         '/Ope/Display/<int:proj_id>')      # 获取项目下所有Display的对应关系
        api.add_resource(ApiCondition,
                         '/Ope/Condition/<int:proj_id>')    # 获取项目下所有Condition的对应关系
        api.add_resource(ApiProperty,
                         '/Ope/Property/<int:proj_id>')     # 获取项目下所有Property的对应关系
        api.add_resource(ApiOpeType,
                         '/Ope/OpeType/<int:proj_id>')      # 获取项目下所有OpeType的对应关系
        api.add_resource(ApiEvent,
                         '/Ope/Event/<int:proj_id>')        # 获取项目下所有Event的对应关系
        # chapter
        api.add_resource(ApiChapter,
                         '/Chapter/<int:screen_gid>/<int:_type>',  # 获取某本Ope下的chapter
                         '/Chapter/update/<int:_type>')     # 更新某本Ope的chapter
        # import
        api.add_resource(ApiScreenJsonImport, '/screen/json/import')
        # export
        api.add_resource(ApiScreenJsonExport,
                         '/screen/json/export/<int:screen_gid>')
