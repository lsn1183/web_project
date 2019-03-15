# -*- coding: UTF-8 -*-
import os
import re
import datetime
import requests
import json
import platform
import shutil
from app.db.utility import Utillity
from app.db import db
from app.db.spec.specification import Specification, SpecVersion
from search.spec_search import SpecSearch
from app.db.ds_rel_specification import DSRelFun
from app.db.project import Project
from app.db.ds_doc import DSDocAstahRel
from app.ctrl.ctrl_base import CtrlBase
from flask import current_app


class CtrlDSInput(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Specification.spec_id
        self.db_object = Specification
        self.col_list = [Specification.spec_id.name, Specification.spec_name.name,
                         Specification.spec_type.name]

    def add(self, request_data, commit=True):
        if not request_data.files:
            return False, '没有上传文件!'
        file_upload = request_data.files['file']
        proj_id = request_data.form.get('proj_id')
        spec_name = request_data.form.get('spec_name')
        spec_type = request_data.form.get('spec_type')
        spec_num = request_data.form.get('spec_num')
        spec_ver = str(request_data.form.get('spec_ver'))
        spec_id = request_data.form.get('spec_id')
        if request_data.form.get('replace') == 'true':
            replace = True
        else:
            replace = False
        if not file_upload:
            return False, '没有指定上传的文件!'
        file_name = file_upload.filename
        file_name = file_name.replace(' ', '').replace('(', '').replace(')', '')
        curr_app = current_app._get_current_object()
        file_path = curr_app.config.get("SPEC_PATH_TEMP")
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        fname, ext_name = Utillity.split_ext_name(file_name)
        fname = fname.rstrip('.')
        if os.path.exists(os.path.join(file_path, file_name)):
            os.remove(os.path.join(file_path, file_name))
        file_upload.save(os.path.join(file_path, file_name))
        proj = db.session.query(Project).filter(Project.proj_id == proj_id).all()
        files = {'file': open(os.path.join(file_path, file_name), 'rb')}
        html_data = requests.post(curr_app.config.get('EXCEL_TO_HTM_URL'), files=files)
        if not html_data.status_code == 200:
            return False, 'EXCEL转换HTM调用失败'
        dd = json.loads(html_data.text)
        if dd.get("result") == "ok":
            html_url = dd.get("content")
            if not platform.system() == 'Windows':
                html_url = html_url.replace('\\', '/')
                html_url = html_url.lstrip('/')
            html_url = os.path.join(curr_app.config.get('SPEC_CHANGE_URL'), html_url)
            new_htm_url = os.path.join(curr_app.config.get('SPEC_PATH_ROOT'), proj[0].proj_name,
                                       spec_type, spec_ver, 'html')
            if not os.path.exists(new_htm_url):
                os.makedirs(new_htm_url)
            mv = 'mv %s %s' % (html_url, new_htm_url)
            os.system(mv)
            new_htm_url = self.convert_url(new_htm_url)
            # SpecSearch
            new_excel_url = os.path.join(curr_app.config.get('SPEC_PATH_ROOT'), proj[0].proj_name,
                                         spec_type, spec_ver, 'excel')
            file_url = os.path.join(file_path, file_name)
            if not os.path.exists(new_excel_url):
                os.makedirs(new_excel_url)
            cmd = 'cp -f %s %s' % (file_url, new_excel_url)
            os.system(cmd)
            pk_excel_url = os.path.join(new_excel_url, file_name)

            new_excel_url = self.convert_url(new_excel_url)
            update_time = datetime.datetime.now()
            # commit_time = update_time
            search_str = "[%s]-%s-%s" % (spec_type, fname, spec_name)
            data = {}
            inputs = db.session.query(Specification).filter(Specification.spec_id == spec_id).order_by(
                                                            Specification.spec_id).all()
            search_obj = SpecSearch.instance()
            if not inputs:
                spec_info = {Specification.proj_id.name: proj_id,
                             Specification.spec_name.name: spec_name,
                             Specification.spec_file_name.name: file_name,
                             Specification.spec_type.name: spec_type,
                             Specification.spec_num.name: spec_num,
                             Specification.search_str.name: search_str,
                             }
                attach = Specification(**spec_info)
                db.session.add(attach)
                db.session.flush()
                ver_info = {
                    SpecVersion.excel_url.name: os.path.join(new_excel_url, file_name),
                    SpecVersion.html_url.name: os.path.join(new_htm_url, fname, fname+'.htm'),
                    SpecVersion.spec_id.name: attach.spec_id,
                    SpecVersion.spec_ver.name: spec_ver,
                    SpecVersion.create_time.name: update_time,
                }
                attach2 = SpecVersion(**ver_info)
                db.session.add(attach2)
                data = attach2.to_dict()
                data['create_time'] = self.time_to_str(data.get('create_time'))
                db.session.commit()
                search_obj.add_document4excel(proj[0].proj_name, pk_excel_url, attach.spec_id, attach2.html_url)
                return True, data
            else:
                height_ver = self.search_height_version(spec_id, spec_ver)
                if not replace:
                    version = db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id,
                                                                   SpecVersion.spec_ver == spec_ver).order_by(
                        SpecVersion.spec_id).all()
                    if not version:
                        ver_info = {
                                     SpecVersion.excel_url.name: os.path.join(new_excel_url, file_name),
                                     SpecVersion.html_url.name: os.path.join(new_htm_url, fname, fname+'.htm'),
                                     SpecVersion.spec_id.name: spec_id,
                                     SpecVersion.spec_ver.name: spec_ver,
                                     SpecVersion.create_time.name: update_time,
                                     }
                        attach = SpecVersion(**ver_info)
                        db.session.add(attach)
                        data = attach.to_dict()
                        data['create_time'] = self.time_to_str(data.get('create_time'))
                        db.session.commit()
                        if height_ver:
                            search_obj.add_document4excel(proj[0].proj_name, pk_excel_url, spec_id,
                                                          attach.html_url)
                        return True, data
                    else:
                        return False, '已存在相同版本'
                else:
                    if db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id,
                                                            SpecVersion.spec_ver == spec_ver).order_by(
                                SpecVersion.create_time.desc()).all():
                        attach = db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id,
                                                                      SpecVersion.spec_ver == spec_ver).order_by(
                            SpecVersion.create_time.desc()).first()
                        attach.excel_url = os.path.join(new_excel_url, file_name),
                        attach.html_url = os.path.join(new_htm_url, fname, fname+'.htm'),
                        attach.create_time = update_time,
                        data = attach.to_dict()
                        data['create_time'] = self.time_to_str(data.get('create_time')[0])
                        db.session.commit()
                        if height_ver:
                            search_obj.add_document4excel(proj[0].proj_name, pk_excel_url, spec_id,
                                                          attach.html_url)
                        return True, data
                    else:
                        return False, '没有此版本信息，无法更新'
        else:
            return False, dd.get("error")

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
        # url = '/'.join([srv_url, file_url])
        return file_url

    def search_height_version(self, spec_id, spec_ver):
        q = db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id).order_by(
                                SpecVersion.spec_ver.desc()).all()
        flag = False
        if q:
            if not q[0].spec_ver > spec_ver:
                flag = True
        else:
            flag = True
        return flag

    def batch_add(self, request_data):
        if not request_data.files:
            return False, '没有上传文件!'
        uploaded_files = request_data.files.getlist("file")
        jsdata = json.loads(request_data.form.get('data'))
        proj_id = jsdata.get('proj_id')
        spec_ver = str(jsdata.get('spec_ver'))
        spec_type = jsdata.get('spec_type')
        curr_app = current_app._get_current_object()
        file_path = curr_app.config.get("SPEC_PATH_TEMP")
        res = {"success": [], "error": []}
        for file in uploaded_files:
            if file:
                filename = file.filename
                filename = filename.replace(' ', '').replace('(', '').replace(')', '')
                if os.path.exists(os.path.join(file_path, filename)):
                    os.remove(os.path.join(file_path, filename))
                file.save(os.path.join(file_path, filename))
                error, name, msg = self.add_one_by_batch(curr_app, file_path, filename, proj_id, spec_type, spec_ver)
                if error:
                    res["success"].append(filename)
                else:
                    res["error"].append({"filename": name, "msg": msg})
        return True, res

    def add_one_by_batch(self, curr_app, file_path, file_name, proj_id, spec_type, spec_ver):
        fname, ext_name = Utillity.split_ext_name(file_name)
        fname = fname.rstrip('.')
        spec_name = fname
        spec_num = re.search(r'(_[0-9]+_([0-9]+_)*)', fname, flags=0).group().strip("_")
        proj = db.session.query(Project).filter(Project.proj_id == proj_id).all()
        files = {'file': open(os.path.join(file_path, file_name), 'rb')}
        html_data = requests.post(curr_app.config.get('EXCEL_TO_HTM_URL'), files=files)
        if not html_data.status_code == 200:
            return False, file_name, 'EXCEL转换HTM调用失败'
        dd = json.loads(html_data.text)
        if dd.get("result") == "ok":
            html_url = dd.get("content")
            if not platform.system() == 'Windows':
                html_url = html_url.replace('\\', '/')
                html_url = html_url.lstrip('/')
            html_url = os.path.join(curr_app.config.get('SPEC_CHANGE_URL'), html_url)
            new_htm_url = os.path.join(curr_app.config.get('SPEC_PATH_ROOT'), proj[0].proj_name,
                                       spec_type, spec_ver, 'html')
            if not os.path.exists(new_htm_url):
                os.makedirs(new_htm_url)
            mv = 'mv %s %s' % (html_url, new_htm_url)
            os.system(mv)
            new_htm_url = self.convert_url(new_htm_url)
            new_excel_url = os.path.join(curr_app.config.get('SPEC_PATH_ROOT'), proj[0].proj_name,
                                         spec_type, spec_ver, 'excel')
            file_url = os.path.join(file_path, file_name)
            if not os.path.exists(new_excel_url):
                os.makedirs(new_excel_url)
            cmd = 'cp -f %s %s' % (file_url, new_excel_url)
            os.system(cmd)
            pk_excel_url = os.path.join(new_excel_url, file_name)
            new_excel_url = self.convert_url(new_excel_url)
            update_time = datetime.datetime.now()
            # commit_time = update_time
            search_str = "[%s]-%s-%s" % (spec_type, fname, spec_name)
            inputs = db.session.query(Specification).filter(Specification.proj_id == proj_id,
                                                            Specification.spec_name == spec_name).order_by(
                Specification.spec_id).all()
            search_obj = SpecSearch.instance()
            if not inputs:
                spec_info = {Specification.proj_id.name: proj_id,
                             Specification.spec_name.name: spec_name,
                             Specification.spec_file_name.name: file_name,
                             Specification.spec_type.name: spec_type,
                             Specification.spec_num.name: spec_num,
                             Specification.search_str.name: search_str,
                             }
                attach = Specification(**spec_info)
                db.session.add(attach)
                db.session.flush()
                ver_info = {
                    SpecVersion.excel_url.name: os.path.join(new_excel_url, file_name),
                    SpecVersion.html_url.name: os.path.join(new_htm_url, fname, fname + '.htm'),
                    SpecVersion.spec_id.name: attach.spec_id,
                    SpecVersion.spec_ver.name: spec_ver,
                    SpecVersion.create_time.name: update_time,
                }
                attach2 = SpecVersion(**ver_info)
                db.session.add(attach2)
                db.session.commit()
                search_obj.add_document4excel(proj[0].proj_name, pk_excel_url, attach.spec_id, attach2.html_url)
                return True, file_name, ''
            else:
                height_ver = self.search_height_version(inputs[0].spec_id, spec_ver)
                version = db.session.query(SpecVersion).filter(SpecVersion.spec_id == inputs[0].spec_id,
                                                               SpecVersion.spec_ver == spec_ver).order_by(
                    SpecVersion.spec_id).all()
                if not version:
                    ver_info = {
                        SpecVersion.excel_url.name: os.path.join(new_excel_url, file_name),
                        SpecVersion.html_url.name: os.path.join(new_htm_url, fname, fname + '.htm'),
                        SpecVersion.spec_id.name: inputs[0].spec_id,
                        SpecVersion.spec_ver.name: spec_ver,
                        SpecVersion.create_time.name: update_time,
                    }
                    attach = SpecVersion(**ver_info)
                    db.session.add(attach)
                    db.session.commit()
                    if height_ver:
                        search_obj.add_document4excel(proj[0].proj_name, pk_excel_url, inputs[0].spec_id, attach.html_url)
                    return True, file_name, ''
                else:
                    return False, file_name, '已存在相同版本'
        else:
            return False, file_name, 'EXCEL转换HTM调用失败'

    def get_db_for_journal(self, doc_id):
        q = (db.session.query(Specification)
             .outerjoin(DSDocAstahRel,
                        Specification.spec_id == DSDocAstahRel.attach_id)
             .filter(DSDocAstahRel.doc_id == doc_id)
             # .order_by(Specification.update_time.desc())
             )
        q_rel = (db.session.query(DSDocAstahRel).
                 filter(DSDocAstahRel.doc_id == doc_id)
                 .order_by(DSDocAstahRel.gid))
        attachs = q.all() + q_rel.all()
        return attachs

    def get_astah_by_type(self, proj_id, _type):
        curr_app = current_app._get_current_object()
        q = (db.session.query(Specification).filter(Specification.spec_type == _type, Specification.proj_id == proj_id)
             .order_by(Specification.spec_file_name)).all()
        astah_list = []
        for astah in q:
            ver_list = []
            q2 = db.session.query(SpecVersion).filter(SpecVersion.spec_id == astah.spec_id)\
                .order_by(SpecVersion.spec_ver).all()
            q2 = self.up_sper_ver(q2)
            if q2:
                for ver in q2:
                    ver_list.append({
                        "ver_id": ver.ver_id,
                        "spec_ver": ver.spec_ver,
                        "spec_id": ver.spec_id,
                        "url": "".join([curr_app.config.get('FILE_SRV_URL'), ver.html_url]),
                    })
            astah_list.append({
                "spec_id": astah.spec_id,
                "proj_id": astah.proj_id,
                "spec_num": astah.spec_num,
                "spec_name": astah.spec_name,
                "spec_file_name": astah.spec_file_name,
                "spec_type": astah.spec_type,
                "search_str": astah.search_str,
                "ver_list": ver_list
            })
        return astah_list

    def get_astah_by_proj_id(self, proj_id):
        curr_app = current_app._get_current_object()
        q = (db.session.query(Specification).filter(Specification.proj_id == proj_id)
             .order_by(Specification.spec_num)).all()
        astah_list = []
        for astah in q:
            ver_list = []
            q2 = db.session.query(SpecVersion).filter(SpecVersion.spec_id == astah.spec_id) \
                .order_by(SpecVersion.spec_ver).all()
            q2 = self.up_sper_ver(q2)
            if q2:
                for ver in q2:
                    ver_list.append({
                        "ver_id": ver.ver_id,
                        "spec_ver": ver.spec_ver,
                        "spec_id": ver.spec_id,
                        "url": "".join([curr_app.config.get('FILE_SRV_URL'), ver.html_url]),
                    })
            astah_list.append({
                "spec_id": astah.spec_id,
                "proj_id": astah.proj_id,
                "spec_num": astah.spec_num,
                "spec_name": astah.spec_name,
                "spec_file_name": astah.spec_file_name,
                "spec_type": astah.spec_type,
                "search_str": astah.search_str,
                "ver_list": ver_list
            })
        return astah_list

    def get_spec_num_by_proj_id(self, proj_id, _type):
        q = (db.session.query(Specification).filter(Specification.spec_type == _type, Specification.proj_id == proj_id)
             .order_by(Specification.spec_num)).all()
        astah_list = []
        filter_list = []
        for astah in q:
            ver_list = []
            q2 = (db.session.query(SpecVersion).filter(SpecVersion.spec_id == astah.spec_id)
                  .order_by(SpecVersion.create_time)).all()
            if astah.spec_num in filter_list:
                pass
            else:
                if q2:
                    for ver in q2:
                        ver_list.append({
                            "ver_id": ver.ver_id,
                            "spec_ver": ver.spec_ver,
                        })
                astah_list.append({
                    "spec_id": astah.spec_id,
                    "proj_id": astah.proj_id,
                    "spec_num": astah.spec_num,
                    "spec_name": astah.spec_name,
                    "ver_list": ver_list
                })
                filter_list.append(astah.spec_num)
        return astah_list

    def get_ver_list_by_spec_id(self, spec_id):
        q = (db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id)
             .order_by(SpecVersion.create_time.desc())).all()
        ver_list = []
        if q:
            for ver in q:
                ver_list.append({
                    "ver_id": ver.ver_id,
                    "spec_ver": ver.spec_ver,
                })
        return ver_list

    def delete_attach(self, spec_id, ver_id, commit_user):
        update_time = self.get_current_time()
        if ver_id == 0:
            commit_list2 = self.delete_by_spec_id(spec_id)
            self.commit_log(commit_list2, commit_user, update_time)
        else:
            self.update_spec_search_or_del(spec_id, ver_id)
            commit_list, error = self.delete_by_ver_id(spec_id, ver_id)
            if error:
                return error
            self.commit_log(commit_list, commit_user, update_time)
        db.session.commit()
        return ""


    def update_spec_search_or_del(self, spec_id, ver_id):
        Specobj = SpecSearch.instance()
        spec = db.session.query(Specification).filter(Specification.spec_id == spec_id).first()
        if db.session.query(Project).filter(Project.proj_id == spec.proj_id).all():
            pro = db.session.query(Project).filter(Project.proj_id == spec.proj_id).first()
            versions = (db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id)
                        .order_by(SpecVersion.spec_ver.desc())).all()
            versions = self.desc_sper_ver(versions)
            ver = (db.session.query(SpecVersion).filter(SpecVersion.spec_id == spec_id,
                                                        SpecVersion.ver_id == ver_id)
                   .order_by(SpecVersion.spec_ver.desc())).first()
            height_ver = self.search_height_version(spec_id, ver.spec_ver)
            if height_ver:
                if len(versions) < 2:
                    if Specobj.get_index4proj(pro.proj_name):
                        Specobj.delete_document(pro.proj_name, spec_id)
                else:
                    excel_url = versions[1].excel_url
                    if not platform.system() == 'Windows':
                        excel_url = excel_url.replace('\\', '/')
                        excel_url = excel_url.lstrip('/')
                    curr_app = current_app._get_current_object()
                    pk_excel_url = os.path.join(curr_app.config.get('SPEC_CHANGE_URL'), excel_url)
                    Specobj.add_document4excel(pro.proj_name, pk_excel_url, spec_id, versions[1].html_url)

    def desc_sper_ver(self, ver_list):
        count = len(ver_list)
        for i in range(0, count):
            for j in range(i+1, count):
                num_i = re.search(r'([0-9]+(\W[0-9]+)*)', ver_list[i].spec_ver, flags=0).group()
                num_j = re.search(r'([0-9]+(\W[0-9]+)*)', ver_list[j].spec_ver, flags=0).group()
                if float(num_i) < float(num_j):
                    ver_list[i], ver_list[j] = ver_list[j], ver_list[i]
        return ver_list

    def up_sper_ver(self, ver_list):
        count = len(ver_list)
        for i in range(0, count):
            for j in range(i+1, count):
                num_i = re.search(r'([0-9]+(\W[0-9]+)*)', ver_list[i].spec_ver, flags=0).group()
                num_j = re.search(r'([0-9]+(\W[0-9]+)*)', ver_list[j].spec_ver, flags=0).group()
                if float(num_i) > float(num_j):
                    ver_list[i], ver_list[j] = ver_list[j], ver_list[i]
        return ver_list

    def get_num_by_str(self):
        pass

    def delete_by_spec_id(self, spec_id=None):
        """这里只删除关系，不删除文件
        :return:
        """
        q = db.session.query(Specification)
        if spec_id:
            q = q.filter(Specification.spec_id == spec_id)
        old_astah_rel = []
        for astah_rel in q:
            old_astah_rel.append(astah_rel.to_dict())
        commit_list = self.add_list(Specification, [], old_astah_rel, Specification.spec_id, [])
        return commit_list

    def delete_by_ver_id(self, spec_id=None, ver_id=None):
        """这里只删除关系，不删除文件
        :return:
        """
        q = db.session.query(SpecVersion)
        b = db.session.query(DSRelFun)
        if ver_id:
            q = q.filter(SpecVersion.ver_id == ver_id, SpecVersion.spec_id == spec_id)
            b = b.filter(DSRelFun.ver_id == ver_id)
        old_astah_rel = []
        if not b:
            for astah_rel in q:
                old_astah_rel.append(astah_rel.to_dict())
            commit_list = self.add_list(SpecVersion, [], old_astah_rel, SpecVersion.ver_id, [])
            error = ""
        else:
            commit_list = []
            error = "此式样书版本有关联usecase无法删除"
        return commit_list, error
