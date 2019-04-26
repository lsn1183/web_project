from flask_restful import Resource, request
from app.ctrl.ctrl_import_json import CtrlImportJson
from app.ctrl.ctrl_export import CtrlExport

class ApiScreenJsonImport(Resource):
    # def get(self):
    #     ImportJson().import_json()

    def post(self):
        result = {'result': 'NG', 'error': ''}
        res, message = CtrlImportJson().save_import_file(request)
        if res:
            result['result'] = 'OK'
        else:
            result['error'] = message
        return result

class ApiScreenJsonExport(Resource):
    def get(self, screen_gid):
        CtrlExport().get_chapter1_info_to_df(screen_gid)
        return