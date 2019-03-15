# -*- coding: UTF-8 -*-
import os
import datetime
from app.db.utility import Utillity
from app.db import db
from app.db.ds_attach import DSAttach
from app.db.ds_doc import DSDocAstahRel
from app.ctrl.ctrl_base import CtrlBase
from flask import current_app


class CtrlDSAttach(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSAttach.attach_id
        self.db_object = DSAttach
        self.col_list = [DSAttach.file_url.name, DSAttach.file_name.name,
                         DSAttach.file_type.name]

    def add(self, request_data, commit=True):
        if not request_data.files:
            return False, '没有上传文件!'
        file_upload = request_data.files['file']
        if not file_upload:
            return False, '没有指定上传的文件!'
        file_name = file_upload.filename
        curr_app = current_app._get_current_object()
        file_path = curr_app.config.get("ATTACH_PATH_ROOT")
        # file_path = os.path.join('data', 'Astah')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        only_id = Utillity().get_nextval()
        new_file_name = Utillity.get_new_file_name(file_name, only_id)
        fname, ext_name = Utillity.split_ext_name(file_name)
        fname = fname.rstrip('.')
        file_upload.save(os.path.join(file_path, new_file_name))
        file_url = os.path.join(file_path, new_file_name)
        file_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), file_url)
        update_time = datetime.datetime.now()
        commit_time = update_time
        attach_info = {DSAttach.file_name.name: file_name,
                       DSAttach.file_type.name: ext_name,
                       DSAttach.file_url.name: file_url,
                       DSAttach.update_time.name: update_time,
                       DSAttach.commit_time.name: commit_time
                       }
        attach = DSAttach(**attach_info)
        db.session.add(attach)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return True, attach.to_dict()

    def add2(self, attach_info, commit=True):
        ver = attach_info.get(DSAttach.ver.name)
        attach_info[DSAttach.ver.name] = Utillity.get_new_version(ver)
        attach_info = self.init_version(attach_info, type='section')
        # attach = DSAttach(**attach_info)
        # db.session.add(attach)
        log_dict = self.common_add(self.db_object, attach_info, None, self.col_list, self.key_col)
        if commit:
            db.session.commit()
        else:
            db.session.flush()
        return log_dict

    def update(self, attach_id, attach_info, commit=True):
        # attach = db.session.query(DSAttach.attach_id == attach_id).first()
        # new_ver = attach_info.get(DSAttach.ver.name)
        # attach.ver = Utillity.get_new_version(new_ver, attach.ver)
        # attach.micro_ver = self.update_version(attach.micro_ver)
        # attach.update(attach_info)
        attach = db.session.query(DSAttach.attach_id == attach_id).first()
        old_attach = attach.to_dict()
        new_ver = attach_info.get(DSAttach.ver.name)
        attach_info[DSAttach.ver.name] = Utillity.get_new_version(new_ver, old_attach.get(DSAttach.ver.name))
        attach_info[DSAttach.micro_ver.name] = self.update_version(old_attach.get(DSAttach.micro_ver.name))
        log_dict = self.common_add(self.db_object, attach_info, old_attach, self.col_list, self.key_col)
        if commit:
            db.session.commit()
        return log_dict, attach_info

    def get(self, attach_id):
        attach = (db.session.query(DSAttach)
                  .filter(DSAttach.attach_id == attach_id).first())
        return attach

    def delete(self, attach_id, commit=True):
        db.session.query(DSAttach).filter(
            DSAttach.attach_id == attach_id).delete()
        if commit:
            db.session.commit()


class CtrlDSAstah(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def add(self, request_data):
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        if not request_data.files:
            return False, '没有上传文件!'
        file_upload = request_data.files['file']
        if not file_upload:
            return False, '没有指定上传的文件!'
        doc_id = request_data.form.get('doc_id')
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        file_name = file_upload.filename
        curr_app = current_app._get_current_object()
        file_path = curr_app.config.get("ATTACH_PATH_ROOT")
        # file_path = os.path.join('data', 'Astah')
        if not os.path.exists(file_path):
            os.mkdir(file_path)
        fname, ext_name = Utillity.split_ext_name(file_name)
        # TODO@hcz: 所有都可以
        # if not ext_name or ext_name.lower() not in (".asta", ".jude"):
        #     return False, '文件扩展名不对，请上传".asta"或".jude文件"'
        fname = fname.rstrip('.')
        # 获取新的文件名称
        only_id = Utillity().get_nextval()
        new_file_name = Utillity.get_new_file_name(file_name, only_id)
        file_upload.save(os.path.join(file_path, new_file_name))
        file_url = os.path.join(file_path, new_file_name)
        file_url = Utillity.convert_url(curr_app.config.get('FILE_SRV_URL'), file_url)
        attach_id = request_data.form.get("attach_id")
        committer = request_data.form.get("committer")  # 提交者'
        ver = request_data.form.get("ver")
        update_time = datetime.datetime.now()
        commit_time = update_time
        attach_info = {DSAttach.attach_id.name: attach_id,
                       DSAttach.file_name.name: file_name,
                       DSAttach.file_type.name: ext_name,
                       DSAttach.file_url.name: file_url,
                       DSAttach.update_time.name: update_time,
                       DSAttach.committer.name: committer,
                       DSAttach.ver.name: ver
                       }
        commit_list = []
        if attach_id:  # 更新
            log_dict, attach_info = CtrlDSAttach().update(attach_id, attach_info, commit=False)
            if log_dict:
                commit_list.append(log_dict)
        else:  # 新增
            # 添加附件
            attach_info[DSAttach.commit_time.name] = commit_time
            attach_log = CtrlDSAttach().add2(attach_info, commit=False)
            attach_id = attach_log.get('key_id')
            attach_info[DSAttach.attach_id.name] = attach_id
            attach_info[DSAttach.commit_time.name] = self.time_to_str(commit_time)
            attach_info[DSAttach.update_time.name] = self.time_to_str(commit_time)
            astah_rel_info = {DSDocAstahRel.doc_id.name: doc_id,
                              DSDocAstahRel.attach_id.name: attach_id}
            astah_rel_log = self.common_add(DSDocAstahRel, astah_rel_info, None, [], DSDocAstahRel.gid)
            commit_list.append(attach_log)
            commit_list.append(astah_rel_log)
        if commit_list:
            log_doc = CtrlDsDoc().update_ver(doc_id, committer)
            commit_list.append(log_doc)
        self.commit_log(commit_list, committer, update_time)
        db.session.commit()
        return True, attach_info

    def get_astah(self, doc_id):
        result_astah = {'doc_id': doc_id, 'sec_type': 'ASTAH',
                        'astah_files': [], "sub": []
                        }
        astah_list = self.get_astah_by_doc_id(doc_id)
        result_astah['astah_files'] = astah_list
        return result_astah

    def get_db_for_journal(self, doc_id):
        q = (db.session.query(DSAttach)
             .outerjoin(DSDocAstahRel,
                        DSAttach.attach_id == DSDocAstahRel.attach_id)
             .filter(DSDocAstahRel.doc_id == doc_id)
             .order_by(DSAttach.update_time.desc())
             )
        q_rel = (db.session.query(DSDocAstahRel).
                 filter(DSDocAstahRel.doc_id == doc_id)
                 .order_by(DSDocAstahRel.gid))
        attachs = q.all() + q_rel.all()
        return attachs

    def get_astah_by_doc_id(self, doc_id):
        q = (db.session.query(DSAttach)
             .outerjoin(DSDocAstahRel,
                        DSAttach.attach_id == DSDocAstahRel.attach_id)
             .filter(DSDocAstahRel.doc_id == doc_id)
             .order_by(DSAttach.update_time.desc()))
        astah_list = []
        for astah in q:
            astah_list.append(astah.to_dict())
        return astah_list

    def delete_attach(self, doc_id, attach_id, commit_user):
        update_time = self.get_current_time()
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        commit_list = self.delete_by_doc_id(doc_id, attach_id)
        if commit_list:
            log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
            commit_list.append(log_doc)
        self.commit_log(commit_list, commit_user, update_time)
        db.session.commit()

    def delete_by_doc_id(self, doc_id, attach_id=None):
        """这里只删除关系，文档不删除Astah文件
        :param doc_id:
        :param attach_id:
        :return:
        """
        q = db.session.query(DSDocAstahRel)
        q = q.filter(DSDocAstahRel.doc_id == doc_id)
        if attach_id:
            q = q.filter(DSDocAstahRel.attach_id == attach_id)
        old_astah_rel = []
        for astah_rel in q:
            old_astah_rel.append(astah_rel.to_dict())
        commit_list = self.add_list(DSDocAstahRel, [], old_astah_rel, DSDocAstahRel.gid, [])
        return commit_list
