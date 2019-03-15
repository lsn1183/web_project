# -*- coding: UTF-8 -*-
from flask import current_app
from app.db import db
from app.db.ds_doc_if import DSDocIf
from app.ctrl.ctrl_base import CtrlBase
from app.db.spec.specification import HeaderFile


class CtrlDsIf(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSDocIf.if_id
        self.db_object = DSDocIf
        self.col_list = [DSDocIf.if_name.name, DSDocIf.description.name,
                         DSDocIf.parameter.name, DSDocIf.return_val.name]

    def get_if_detail(self, doc_id):
        ds_if_list = self.get_by_doc_id(doc_id)
        if_result = []
        for ds_if in ds_if_list:
            if_dict = dict()
            if_dict[DSDocIf.if_id.name] = ds_if.get(DSDocIf.if_id.name)
            if_dict['sec_type'] = 'IF'
            if_dict[DSDocIf.if_name.name] = ds_if.get(DSDocIf.if_name.name)
            if_dict[DSDocIf.parameter.name] = ds_if.get(DSDocIf.parameter.name)
            if_dict[DSDocIf.return_val.name] = ds_if.get(DSDocIf.return_val.name)
            if_dict[DSDocIf.description.name] = ds_if.get(DSDocIf.description.name)
            if_dict[DSDocIf.micro_ver.name] = ds_if.get(DSDocIf.micro_ver.name)
            if_dict['sub'] = []
            if_result.append(if_dict)
        return if_result

    def get_by_doc_id(self, doc_id):
        q = db.session.query(DSDocIf).filter(DSDocIf.doc_id == doc_id).order_by(DSDocIf.if_id)
        ds_if_list = []
        for ds_if in q:
            ds_if_list.append(ds_if.to_dict())
        return ds_if_list

    def get_db_for_journal(self, doc_id):
        q = db.session.query(DSDocIf).filter(DSDocIf.doc_id == doc_id).order_by(
            DSDocIf.if_id)
        ifs = q.all()
        return ifs

    def add_if(self, if_data):
        try:
            for if_dict in if_data:
                db.session.add(DSDocIf(**if_dict))
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def update_if(self, data_info):
        try:
            update_time = self.get_current_time()
            doc_id = data_info.get(DSDocIf.doc_id.name)
            if not doc_id:
                return False, '没有指定文档ID！'
            from app.ctrl.ctrl_ds_doc import CtrlDsDoc
            doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
            if error:
                return 0, error
            commit_user = data_info.get('commit_user')
            if_data = data_info.get('if_data')
            error = self.diff_if_ver(if_data)
            if error:
                return False, error
            new_if_data = self.get_new_if_list(if_data, doc_id)
            old_if_data = self.get_old_data(self.db_object, DSDocIf.doc_id, doc_id)
            commit_list = self.add_list(self.db_object, new_if_data, old_if_data,
                                        self.key_col, self.col_list)
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def get_new_if_list(self, if_data, doc_id):
        new_if_data = []
        for data in if_data:
            new_data = dict()
            for column in DSDocIf.__table__.columns:
                new_data[column.name] = data.get(column.name)
            new_data['doc_id'] = doc_id
            new_if_data.append(new_data)
        return new_if_data

    def diff_if_ver(self, if_data):
        for if_dict in if_data:
            if_id = if_dict.get(DSDocIf.if_id.name)
            micro_ver = if_dict.get(DSDocIf.micro_ver.name)
            if if_id:
                old_micro_ver = self.get_if_ver(if_id)
                flag, error = self.diff_ver(micro_ver, old_micro_ver)
                if not flag:
                    return error
            if_dict['micro_ver'] = self.update_version(micro_ver)
        return None

    def delete_by_doc_id(self, doc_id):
        ds_if_q = db.session.query(DSDocIf).filter(DSDocIf.doc_id == doc_id)
        old_data_list = []
        new_data_list = []
        for ds_if in ds_if_q:
            old_data_list.append(ds_if.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def delete_by_if_id(self, if_id, commit_user):
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        try:
            q = db.session.query(DSDocIf).filter(DSDocIf.if_id == if_id)
            doc_id = q.doc_id
            q.delete()
            CtrlDsDoc().update_doc_ver(doc_id, commit_user)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def get_if_ver(self, if_id):
        q = db.session.query(DSDocIf).filter(DSDocIf.if_id == if_id).first()
        return q.micro_ver

    def get_if_url(self, doc_id):
        curr_app = current_app._get_current_object()
        url_list = []
        res = {"url": ""}
        q = db.session.query(HeaderFile).filter(HeaderFile.doc_id == doc_id).filter(HeaderFile.status == "新建").all()
        if q:
            for i_url in q:
                res["url"] = "".join([curr_app.config.get('FILE_SRV_URL'), i_url.html_url])
                res["h_id"] = i_url.h_id
                res["name"] = "详细地址"
                url_list.append(res)
        return url_list

    def delete_by_h_id(self, h_id):
        try:
            q = db.session.query(HeaderFile).filter(HeaderFile.h_id == h_id).filter(HeaderFile.status == "新建").all()
            if q:
                q[0].status = "已删除"
                db.session.commit()
                return True, ''
            else:
                return False, "此IF文件未找到或已删除"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"
