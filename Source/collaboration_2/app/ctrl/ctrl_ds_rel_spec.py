# -*- coding: UTF-8 -*-
from app.db import db
import json
from flask import current_app
from sqlalchemy import or_, and_
from app.db.ds_rel_specification import DSRelSpec
from app.db.spec.specification import Specification
from app.db.spec.specification import SpecVersion
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_ds_doc import CtrlDsDoc
from app.ctrl.ctrl_diff import CtrlDiff


class CtrlDSRelSpec(CtrlBase):
    """关系式样书
    """
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSRelSpec.gid
        self.db_object = DSRelSpec
        self.col_list = [DSRelSpec.func_id.name]

    def add(self, data_dict):
        update_time = self.get_current_time()
        micro_ver = data_dict.get('micro_ver')
        doc_id = data_dict.get(DSRelSpec.doc_id.name)
        commit_user = data_dict.get('commit_user')
        content = data_dict.get('content')
        if not doc_id:
            return False, '未指定文档ID!'
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        old_micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        flag, error = self.diff_ver(micro_ver, old_micro_ver)
        if not flag:
            return 0, error
        data_list = []
        old_spec_list = self.get_old_data(self.db_object, DSRelSpec.doc_id, doc_id)
        old_data_list = []
        for old_data in old_spec_list:
            if old_data.get('sec_id'):
                old_data_list.append(old_data)
        for data in content:
            sec_id = data.get(DSRelSpec.sec_id.name)
            if not sec_id:
                return 0, '没有指定USECASE_ID！'
            old_data, error = CtrlDSSection().session_is_exist(sec_id)
            if error:
                return 0, error
            specs = data.get('specs')
            if not specs:
                continue
            spec_info = dict()
            spec_info[DSRelSpec.gid.name] = specs.get('gid')
            spec_info[DSRelSpec.doc_id.name] = int(doc_id)
            spec_info[DSRelSpec.sec_id.name] = int(sec_id)
            spec_info[DSRelSpec.spec_id.name] = specs.get(DSRelSpec.spec_id.name)
            spec_info[DSRelSpec.func_id.name] = specs.get(DSRelSpec.func_id.name)
            data_list.append(spec_info)
            # if not spec_list:
            #     return 0, '无式样书!'
        try:
            commit_list = self.add_list(self.db_object, data_list, old_data_list,
                                        self.key_col, self.col_list)
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return doc_id, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def get(self, doc_id, sec_type=None, condition=None):
        uc_list = CtrlDSSection().get_session_by_doc_id(doc_id, "USERCASE")
        uc_spec_list = []
        i = 1
        for uc in uc_list:
            spec_dict = dict()
            spec_dict['sec_id'] = uc.get('sec_id')
            content = json.loads(uc.get('content'))
            spec_dict['number'] = 'UC' + str(i)
            spec_dict['title'] = content[0].get('title')
            spec_dict['val'] = content[0].get('val')
            spec_type_dict, status = self._get(uc.get('sec_id'))
            if not spec_type_dict:
                continue
            spec_dict['specs'] = spec_type_dict
            uc_spec_list.append(spec_dict)
            i += 1
        return uc_spec_list

    def get_by_sec_id(self, sec_id):
        spec_list, _ = self._get(sec_id)
        return spec_list

    def _get(self, sec_id, sec_type=None, condition=None):
        spec_list = []
        q = (db.session.query(
            DSRelSpec.gid,
            DSRelSpec.spec_id,
            DSRelSpec.func_id,
            Specification.spec_name,
            Specification.spec_type,
            Specification.spec_file_name,
            Specification.url,
                              )
             .filter(DSRelSpec.spec_id == Specification.spec_id)
             .filter(DSRelSpec.sec_id == sec_id)
             )
        q = q.order_by(Specification.spec_type.desc(), Specification.spec_name)
        for row in q:
            spec_dict = dict()
            spec_dict[DSRelSpec.gid.name] = row[0]
            spec_dict[DSRelSpec.spec_id.name] = row[1]
            spec_dict[DSRelSpec.func_id.name] = row[2]
            spec_dict[Specification.spec_name.name] = row[3]
            spec_dict[Specification.spec_type.name] = row[4]
            spec_dict[Specification.spec_file_name.name] = row[5]
            spec_dict[Specification.url.name] = row[6]
            spec_dict["title"] = '[%s]-%s-%s' % (row[4],
                                                 row[5],
                                                 row[3])
            spec_list.append(spec_dict)
        return spec_list, None

    def get_db_for_journal(self, doc_id):
        q = (db.session.query(DSRelSpec).filter(DSRelSpec.doc_id == doc_id))
        q = q.order_by(DSRelSpec.gid)
        spes = q.all()
        return spes

    # def get_detail(self, sec_id):
    #     q = db.session.query(DSRelSpec).filter(DSRelSpec.sec_id == sec_id)
    #     q = q.order_by(DSRelSpec.spec_type, DSRelSpec.spec_name)
    #     spec_list = []
    #     for spec in q:
    #         spec_dict = dict()
    #         spec_dict[DSRelSpec.spec_type.name] = spec.spec_type
    #         spec_dict[DSRelSpec.spec_name.name] = spec.spec_name
    #         spec_list.append(spec_dict)
    #     return spec_list

    def delete_by_key_id(self, key_id):
        db.session.query(DSRelSpec).filter(DSRelSpec.gid == key_id).delete()

    def delete_by_sec_id(self, sec_id):
        """
        删除usecase的式样书
        :param doc_id:
        :param sec_id:
        :return:
        """
        spec_q = db.session.query(DSRelSpec).filter(DSRelSpec.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for spec in spec_q:
            old_data_list.append(spec.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def delete_by_doc_id(self, doc_id):
        """
        删除文档的式样书
        :param doc_id:
        :return:
        """
        spec_q = db.session.query(DSRelSpec).filter(and_(DSRelSpec.doc_id == doc_id,
                                                    DSRelSpec.sec_id == None))
        old_data_list = []
        new_data_list = []
        for spec in spec_q:
            old_data_list.append(spec.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def delete_usecase_spec(self, doc_id, spec_id_list):
        """
        删除文档式样书时同时把usecase下相对应得式样书删掉
        :param doc_id:
        :param spec_list:
        :return:log信息
        """
        q_spec = (db.session.query(DSRelSpec).filter(and_(DSRelSpec.doc_id == doc_id,
                                                DSRelSpec.sec_id.isnot(None),
                                                DSRelSpec.spec_id.notin_(tuple(spec_id_list)))))
        delete_list = []
        new_data_list = []
        for q in q_spec:
            delete_list.append(q.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, delete_list, self.key_col, self.col_list)
        return commit_list

    def get_by_doc_id(self, doc_id, search_str):
        spec_list = []
        q = (db.session.query(
                              Specification.spec_name,
                              Specification.spec_type,
                              Specification.spec_file_name,
                              Specification.url,
                              DSRelSpec.spec_id,
                              DSRelSpec.gid
                              )
             .outerjoin(DSRelSpec, DSRelSpec.spec_id == Specification.spec_id)
             .filter(DSRelSpec.doc_id == doc_id)
             .filter(DSRelSpec.sec_id == None)
             )
        if search_str:
            q = q.filter(Specification.search_str
                         .ilike('%' + search_str + '%'))
        q = q.order_by(Specification.spec_type.desc(), Specification.spec_name)
        for row in q:
            spec_dict = dict()
            spec_dict[DSRelSpec.gid.name] = row[5]
            spec_dict[DSRelSpec.spec_id.name] = row[4]
            spec_dict[Specification.spec_name.name] = row[0]
            spec_dict[Specification.spec_type.name] = row[1]
            spec_dict[Specification.spec_file_name.name] = row[2]
            spec_dict[Specification.url.name] = row[3]
            spec_dict["title"] = '[%s]-%s-%s' % (row[1],
                                                 row[2],
                                                 row[0])
            spec_list.append(spec_dict)
        return spec_list, None

    def add_doc_spec(self, data_dict):
        update_time = self.get_current_time()
        commit_user = data_dict.get('commit_user')
        micro_ver = data_dict.get('micro_ver')
        doc_id = data_dict.get(DSRelSpec.doc_id.name)
        if not doc_id:
            return False, '未指定文档ID!'
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return 0, error
        spec_list = []
        for _, data_list in data_dict.items():
            if type(data_list) == list:
                for spec in data_list:
                    spec_info = dict()
                    spec_info[DSRelSpec.gid.name] = spec.get('gid')
                    spec_info[DSRelSpec.doc_id.name] = int(doc_id)
                    spec_info[DSRelSpec.spec_id.name] = spec.get('spec_id')
                    spec_info[DSRelSpec.sec_id.name] = None
                    spec_info[DSRelSpec.func_id.name] = None
                    spec_list.append(spec_info)
        # if not spec_list:
        #     return 0, '无式样书!'
        # sec_id = data_dict.get(DSRelSpec.sec_id.name)
        try:

            # if not sec_id:
            #     return 0, '没有指定USECASE_ID！'
            old_micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
            flag, error = self.diff_ver(micro_ver, old_micro_ver)
            if not flag:
                return 0, error
            spec_id_list = []
            old_data_list = self.get_old_data(self.db_object, [DSRelSpec.doc_id, DSRelSpec.sec_id],
                                              {'doc_id': doc_id, 'sec_id': None})
            for spec_info in spec_list:
                spec_id_list.append(spec_info.get(DSRelSpec.spec_id.name))
            commit_list = self.add_list(self.db_object, spec_list, old_data_list,
                                        self.key_col, self.col_list)
            commit_list += self.delete_usecase_spec(doc_id, spec_id_list)
            if commit_list:
                log_dict = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_dict)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return doc_id, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def get_project_spec(self, proj_id):
        spec_list = []
        specs = (db.session.query(Specification)
                 .filter(Specification.proj_id == proj_id)
                 .order_by(Specification.spec_file_name))
        for spec in specs:
            spec_dict = dict()
            spec_dict[Specification.spec_file_name.name] = spec.spec_file_name
            new_ver = self.get_new_ver(spec.spec_id)
            spec_dict['ver_id'] = new_ver.get('ver_id')
            spec_dict['html_url'] = new_ver.get('html_url')
            spec_list.append(spec_dict)
        return spec_list

    def get_new_ver(self, spec_id):
        spec = (db.session.query(SpecVersion)
                .filter(SpecVersion.spec_id == spec_id)
                .order_by(SpecVersion.ver_id.desc()).first())
        return spec.to_dict()
