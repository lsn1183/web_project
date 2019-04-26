import zipfile
import os
from flask import current_app
from app.db import db
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_project import CtrlProject
from app.json_import.import_json import ImportJson


class CtrlImportJson(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def save_import_file(self, request_data):
        if not request_data.files:
            return False, '没有上传文件!'
        upload_file = request_data.files["file"]
        param = request_data.form
        proj_id = param.get("proj_id")
        filename = upload_file.filename
        zip_name, zip_extension = os.path.splitext(filename)
        if zip_extension != ".zip":
            return False, '请上传zip文件！'
        res, msg = CtrlProject().get_one_proj_by_id(proj_id)
        if not res:
            return res, msg
        proj_name = msg.get("proj_name")
        only_file_id = self.get_next_seq()
        unzip_path = os.path.join('static', proj_name, str(only_file_id))
        if not os.path.exists(os.path.join(current_app.root_path, unzip_path)):
            os.makedirs(os.path.join(current_app.root_path, unzip_path))
        local_file_path = os.path.join(current_app.root_path, unzip_path, filename)
        upload_file.save(local_file_path)
        z = zipfile.ZipFile(local_file_path, 'r')
        z.extractall(path=os.path.join(current_app.root_path, unzip_path))
        z.close()
        json_file_list = self.find_json_file_path(os.path.join(unzip_path, zip_name))
        try:
            for json_file in json_file_list:
                ImportJson().import_json(proj_id, json_file)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def find_json_file_path(self, unzip_path):
        """
        找到json文件路径
        :param unzip_path:
        :return:
        """
        json_file_list = []
        for i in os.walk(os.path.join(current_app.root_path, unzip_path)):
            file_list = i[2]
            for file in file_list:
                extension = os.path.splitext(file)[1]
                if extension == ".json":
                    json_file_list.append(os.path.join(unzip_path, file))
        return json_file_list
