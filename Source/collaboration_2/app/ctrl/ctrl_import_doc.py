# -*- coding: UTF-8 -*-
import os
import json
import platform
import datetime
from app.db import db
from flask import current_app
from app.db.project import Project
from app.import_doc.import_doc_base import ImportDocBase
from app.ctrl.ctrl_base import CtrlBase
from app.db.utility import Utillity
from app.db.ds_doc import Ds_Doc
from app.db.model import Model
from data.doc.doxygenflie import Doxygen
from app.db.spec.specification import HeaderFile


class CtrlImportDoc(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.proj_name = ''

    def do_import(self, request_data):
        if not request_data.files:
            return False, '没有上传文件!'
        file_upload = request_data.files['file']
        if not file_upload:
            return False, '没有指定上传的文件!'
        file_name = file_upload.filename
        # if "&" in file_name:
        #     return False, '文件名不能含有&符号！'
        only_id = Utillity.get_nextval()
        new_file_name = Utillity.get_new_file_name(file_name, only_id)
        only_file_name = os.path.splitext(new_file_name)[0]
        path = os.path.join("import_root", only_file_name)
        if not os.path.exists(path):
            os.makedirs(path)
        file_url = os.path.join(path, file_name)
        file_upload.save(file_url)
        proj_id = request_data.form.get('proj_id')
        model_id = request_data.form.get('model_id')
        creator = request_data.form.get('creator')
        doc_type = request_data.form.get('doc_type')
        import_obj = ImportDocBase()
        try:
            json_url, error = import_obj.excel_to_json(file_url)
            if error:
                return False, error
            commit_list, error = import_obj.read_json(json_url, model_id, creator, doc_type, proj_id)
            if error:
                db.session.rollback()
                return False, error
            self.commit_log(commit_list, creator, self.get_current_time())
            db.session.commit()
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
            return True, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def test_do_import(self, file_url, proj_id, model_id, doc_type, creator):
        import_obj = ImportDocBase()
        json_url, error = import_obj.excel_to_json(file_url)
        if error:
            return False, error
        commit_list, error = import_obj.read_json(json_url, model_id, creator, doc_type, proj_id)
        if error:
            db.session.rollback()
            return False, error
        self.commit_log(commit_list, creator, self.get_current_time())
        db.session.commit()
        from app.db import cache
        cache.delete('get_model_tree')  # 删除缓存
        return True, None

    def batch_upload_h(self, request_data):
        if not request_data.files:
            return False, '没有上传文件!'
        uploaded_files = request_data.files.getlist("file")
        jsdata = json.loads(request_data.form.get('data'))
        doc_id = jsdata.get('doc_id')
        commter = jsdata.get('commit_user')
        proj_id = jsdata.get('proj_id')
        if db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).order_by(Ds_Doc.doc_id).all():
            doc = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
            module = db.session.query(Model).filter(Model.model_id == doc.model_id).first()
            proj = db.session.query(Project).filter(Project.proj_id == proj_id).all()
            uti = Utillity()
            only_id = uti.get_nextval()
            file_path = os.path.abspath(os.path.join(os.getcwd(), r'data', r'doxygen', str(only_id), module.title))
            for file in uploaded_files:
                if file:
                    filename = file.filename
                    if os.path.exists(os.path.join(file_path, filename)):
                        os.remove(os.path.join(file_path, filename))
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    file.save(os.path.join(file_path, filename))
            success, msg = self.add_one_by_batch(file_path, proj[0].proj_name, only_id, module.title)
            if success:
                # upgrade, h_id = self.have_hurl_by_doc(doc_id)
                # if upgrade:
                #     url = self.chang_header_file(msg, doc_id, h_id)
                # else:
                url = self.add_header_flie(msg, doc_id)
                return True, url
            else:
                return False, msg

    def add_one_by_batch(self, file_path, proj_name, only_id, title):
        try:
            curr_app = current_app._get_current_object()
            dox_path = os.path.join(curr_app.config.get("DOXYGEN_PATH"), proj_name, str(only_id), title)
            config_file = open(os.path.join(file_path, 'doxygenfile'), 'w+', encoding="utf8")
            config_file.write(Doxygen.DOXYGEN_STR % (dox_path, file_path))
            config_file.close()
            if not os.path.exists(dox_path):
                os.makedirs(dox_path)
            if not platform.system() == 'Windows':
                dx = 'cd %s; doxygen %s' % (file_path, os.path.join(file_path, 'doxygenfile'))
            else:
                dx = 'cd %s && %s %s' % (file_path, r'C:\Program Files\doxygen\bin\doxygen.exe', 'doxygenfile')
            print(dx)
            os.system(dx)
            dox_path = self.convert_url(dox_path)
            return True, dox_path
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def convert_url(self, file_url):
        expanduser = os.path.expanduser('~')
        if file_url.startswith(expanduser):
            expanduser = os.path.join(expanduser, 'data')
            file_url = file_url[len(expanduser):]
            file_url = file_url.strip(os.path.sep)
        else:
            _, file_url = os.path.splitdrive(file_url)  # 去掉盘符
            file_url = file_url.strip(os.path.sep)
            file_url = file_url.replace('\\', '/')
        return file_url

    def add_header_flie(self, path, doc_id):
        ver_info = {
            HeaderFile.html_url.name: os.path.join(path, r'html', r'index.html'),
            HeaderFile.doc_id.name: doc_id,
            HeaderFile.status.name: "新建",
            HeaderFile.create_time.name: datetime.datetime.now(),
        }
        attach = HeaderFile(**ver_info)
        db.session.add(attach)
        db.session.commit()
        return attach.html_url

    def chang_header_file(self, path, doc_id, h_id):
        header = db.session.query(HeaderFile).filter(HeaderFile.doc_id == doc_id,
                                                     HeaderFile.h_id == h_id).first()
        header.html_url = os.path.join(path, r'html', r'index.html')
        # header.create_time = datetime.datetime.now()
        db.session.commit()
        return header.html_url

    def have_hurl_by_doc(self, doc_id):
        q = db.session.query(HeaderFile).filter(HeaderFile.doc_id == doc_id).all()
        if q:
            return True, q[0].h_id
        else:
            return False, 0
