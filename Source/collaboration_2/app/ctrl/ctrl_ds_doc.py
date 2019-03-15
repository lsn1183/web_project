# -*- coding: UTF-8 -*-
import time
from app.db import db
import copy
import re
from flask import current_app
from app.db.ds_doc import Ds_Doc
from app.db.ds_doc import DSDocDetailRel
from app.db.ds_doc import DSDocType
from app.db.ds_doc import DSDocStatus
from app.db.model import Model
from app.db.ds_section import DSSection, DSSectionTag
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.ctrl.ctrl_doc_tag import CtrlDocTag
from app.ctrl.ctrl_attach import CtrlDSAstah
from app.ctrl.ctrl_ds_if import CtrlDsIf
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_ds_drbfm import CtrlDsDrbfm
WORK_START_STATUS = 1  # 初始状态，待作业
WORK_FINISH_STATUS = 2  # 作业完了，待确认
WORK_CONFIRM_STATUS = 3  # 确认完了
WORK_LOCK_STATUS = 4  # 入库，锁定


class CtrlDsDoc(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Ds_Doc.doc_id
        self.db_object = Ds_Doc
        self.col_list = [Ds_Doc.title.name, Ds_Doc.summary.name]
        self.ds_col_list = []
        for column in Ds_Doc.__table__.columns:
            self.ds_col_list.append(column.name)
        self.sec_type_list = []
        for sec_type in CtrlDSSection().get_section_type():
            self.sec_type_list.append(sec_type.get('sec_type'))
        # self.ds_col_list = ['doc_type', 'title', 'ver', 'model_id',
        #                     'create_time', 'update_time', 'creator', 'editor', 'locked']
        # self.sec_type_list = ['SUMMARY', 'USERCASE', 'SEQUENCE', 'CLASS',
        #                       'BLOCK', 'RESOURCE', 'IF', 'STD']

    def get_ds_doc(self, doc_id):
        doc_data = dict()
        q = (db.session.query(Ds_Doc.doc_id, Model.title, DSDocType.describe,
                              Ds_Doc.creator, Ds_Doc.create_time, Ds_Doc.editor,
                              Ds_Doc.update_time, Ds_Doc.ver, Ds_Doc.model_id)
             .outerjoin(Model, Ds_Doc.model_id == Model.model_id)
             .outerjoin(DSDocType, Ds_Doc.doc_type == DSDocType.doc_type)
             .filter(Ds_Doc.doc_id == doc_id)).all()
        if len(q):
            ds_doc = q[0]
            model_name = ds_doc[1]
            doc_type = ds_doc[2]
            doc_data['title'] = "%s_v%s(%s)" % (doc_type, ds_doc[7], model_name)
            doc_data['doc_type'] = doc_type
            doc_data['creator'] = ds_doc[3]
            doc_data['create_time'] = self.time_to_str(ds_doc[4])
            doc_data['editor'] = ds_doc[5]
            doc_data['update_time'] = self.time_to_str(ds_doc[6])
            doc_data['ver'] = ds_doc[7]
            doc_data['model_id'] = ds_doc[8]
            doc_data['Block'] = CtrlDSSection().get_section_by_type(doc_id, sec_type="BLOCK")
            doc_data['Class'] = CtrlDSSection().get_section_by_type(doc_id, sec_type="CLASS")
            doc_data['Usecase'] = CtrlDSSection().get_section_by_type(doc_id, sec_type="COMMON")
            doc_data['UsecaseTable'] = CtrlDSSection().get_uc_table2(doc_id)
            doc_data['Statemachine'] = CtrlDSSection().get_section_by_type(doc_id, sec_type="STD")
        return doc_data

    def get_latest_doc(self, model_id, doc_type=None):
        """
        根据模块id获取最新的基本设计/详细设计/IF式样书
        :param model_id:
        :param doc_type:BASIC/DETAIl
        :return:
        """
        doc_dict = {"doc_id": 0, "ver": "TODO"}
        q = (db.session.query(Ds_Doc)
             .filter(Ds_Doc.model_id == model_id))
        if doc_type:
            q = q.filter(Ds_Doc.doc_type == doc_type)
        q = q.order_by(Ds_Doc.ver.desc()).all()
        if len(q):
            doc_dict["doc_id"] = q[0].doc_id
            doc_dict["ver"] = q[0].ver
        return doc_dict

    def add_new_doc(self, doc_type, proj_id, model_id, commit_user):
        type_dict = {"basic_design": "BASIC", "detail_design": "DETAIL",
                     "IF_stylebook": "IF", "unit_test": "UNIT",
                     "interface_test": "INTERFACE", "function_test": "FUNCTION"}
        doc_type = type_dict.get(doc_type)
        now_datetime = self.get_current_time()
        new_doc = {"doc_type": doc_type, "ver": "0.001",
                   "model_id": model_id, "proj_id": proj_id,
                   "creator": commit_user, "create_time": now_datetime,
                   "editor": commit_user, "update_time": now_datetime,
                   "major_ver": 0, "minor_ver": 1, "micro_ver": 1,
                   "status": 1}
        try:
            log_dict = self.common_add(self.db_object, new_doc, None, self.key_col, self.key_col)
            db.session.commit()
            doc_id = log_dict.get("key_id")
            return doc_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return None,  "服务异常！请联系管理员！"

    def up_doc_ver(self, data_json):
        """
        升级文档版本
        :param doc_id:
        :param ver:
        :return:
        """
        doc_id = data_json.get("doc_id")
        ver = data_json.get("ver")
        username = data_json.get("commit_user")
        update_time = self.get_current_time()
        error = ""
        try:
            q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).all()
            if q:
                old_ver = q[0].ver
                if ver != old_ver:
                    result = self.write_db_journal(doc_id, username, update_time)
                    if not result:
                        error = "备份文档失败！"
                        db.session.rollback()
            else:
                error = "该文档ID不存在！"
            if not error:
                q[0].ver = ver
                db.session.commit()
            return error
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return "服务异常！请联系管理员！"

    ####################################################################################################################

    def get_doc(self, doc_id, detail=None):
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id)
        q = q.order_by(Ds_Doc.doc_id).all()
        ds_doc = dict()
        if len(q):
            ds_doc = q[0].to_dict()
            ds_doc['create_time'] = self.time_to_str(ds_doc.get('create_time'))
            ds_doc['update_time'] = self.time_to_str(ds_doc.get('update_time'))
            ds_doc['copy_on'] = False
            parent_doc = self.get_parent_doc(doc_id)
            ds_doc['parent_doc'] = parent_doc
            if parent_doc:
                ds_doc['copy_on'] = True
        if not detail:
            return ds_doc
        else:
            if ds_doc.get(Ds_Doc.summary.name):
                ds_doc[Ds_Doc.summary.name] = ds_doc[Ds_Doc.summary.name].replace('\n', '<br>')
            ds_doc['sub'] = []
            astah_dict = CtrlDSAstah().get_astah(doc_id)
            public_usecase_list = CtrlDSSection().get_session_by_doc_id(doc_id, 'COMMON')
            block_list = CtrlDSSection().get_session_by_doc_id(doc_id, "BLOCK")
            class_list = CtrlDSSection().get_session_by_doc_id(doc_id, "CLASS")
            seq_list = CtrlDSSection().get_sequence2(doc_id)
            std_list = CtrlDSSection().get_session_by_doc_id(doc_id, 'STD')
            if_list = CtrlDsIf().get_if_detail(doc_id)
            usercase_dict = CtrlDSSection().get_usecase_tree2(doc_id)
            drbfm_list = CtrlDsDrbfm().get_drbfm_new(doc_id)
            drbfm_dict = {'sec_type': 'DRBFM', 'drbfm_list': drbfm_list, 'sub': []}
            ds_doc['sub'].append(astah_dict)
            ds_doc['sub'] += if_list
            ds_doc['sub'] += public_usecase_list
            ds_doc['sub'] += block_list
            ds_doc['sub'] += class_list
            ds_doc['sub'].append(usercase_dict)
            ds_doc['sub'] += seq_list
            ds_doc['sub'] += std_list
            ds_doc['sub'].append(drbfm_dict)
            return ds_doc

    def get_parent_doc(self, doc_id):
        parent_doc = None
        q = (db.session.query(Ds_Doc).outerjoin(DSDocDetailRel,
             Ds_Doc.doc_id == DSDocDetailRel.parent_doc_id
                                                )
             .filter(DSDocDetailRel.doc_id == doc_id).first())
        if q:
            parent_doc = {'doc_id': q.doc_id, 'title': q.title}
        return parent_doc

    def update_ds_doc(self, doc_info):
        result = {'result': 'OK', 'doc_id': None}
        update_time = self.get_current_time()
        commit_user = doc_info.get('editor')
        basic_doc_id = doc_info.get('basic_doc_id')
        copy_on = doc_info.get('copy_on')
        try:
            ds_doc = dict()
            for col in self.ds_col_list:
                ds_doc[col] = doc_info.get(col)
            ds_doc['update_time'] = update_time
            doc_id = ds_doc.get('doc_id')
            if not doc_id:
                ds_doc['create_time'] = update_time
                ds_doc['status'] = WORK_START_STATUS
                ds_doc = self.init_version(ds_doc, 'doc')
                if copy_on and basic_doc_id:
                    doc_id, commit_list = self.copy_basic_to_detail(basic_doc_id, commit_user, ds_doc)
                else:
                    old_data = []
                    commit_list = self.add_list(self.db_object, [ds_doc], old_data, self.key_col, self.col_list)
                    doc_id = commit_list[0].get('key_id')
                from app.db import cache
                cache.delete('get_model_tree')  # 删除缓存
            else:
                old_data, error = self.ds_doc_exist(doc_id)
                if error:
                    result["result"] = 'NG'
                    result["error"] = error
                    return result
                old_micro_ver = self.get_doc_ver(doc_id)
                flag, error = self.diff_ver(ds_doc.get('micro_ver'), old_micro_ver)
                old_title = old_data[0].get('title')
                if ds_doc.get('title') != old_title:
                    from app.db import cache
                    cache.delete('get_model_tree')  # 删除缓存
                if not flag:
                    result["result"] = 'NG'
                    result["error"] = error
                    return result
                else:
                    ds_doc['micro_ver'] = self.update_version(ds_doc.get('micro_ver'))
                    commit_list = self.add_list(self.db_object, [ds_doc], old_data, self.key_col, self.col_list)
            self.commit_log(commit_list, commit_user, update_time)
            result['doc_id'] = doc_id
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            result["result"] = 'NG'
            result["error"] = "服务异常！请联系管理员！"
        return result

    def ds_doc_exist(self, doc_id):
        """
        检查文档是否存在
        :param doc_id:
        :return:
        """
        error = None
        old_data = self.get_old_data(self.db_object, self.key_col, doc_id)
        if doc_id and not old_data:
            error = "该文档已被删除！"
        else:
            if old_data[0].get('status') == WORK_LOCK_STATUS:
                error = '请先解锁该文档！'
        return old_data, error

    def _update_sub_section(self, sub_sec, sec_id, doc_id):
        ctrl_sec = CtrlDSSection()
        for sec_type in sub_sec:
            contents = sub_sec.get(sec_type)
            for content in contents:
                pass
        # for sec_type in usercase:
        #     if sec_type not in self.sec_type_list:
        #         continue
        #     order_id = 1
        #     for sec_dict in usercase[sec_type]:
        #         sec_id = sec_dict.get('sec_id')
        #         content = sec_dict.get('content')
        #         tags = sec_dict.get('tags')
        #         if content:
        #             section = {"doc_id": doc_id, "sec_type": sec_type, 'content': content,
        #                        'ver': None, 'order_id': order_id}
        #             if sec_id:
        #                 ctrl_sec.update_sec(section, sec_id)
        #                 ctrl_sec.delete_sec_tags(sec_id)
        #             else:
        #                 section['parent_sec_id'] = parent_sec_id
        #                 sec_id = ctrl_sec.add_section(section)
        #             for tag in tags:
        #                 ctrl_sec.add_sec_tag_rel({'sec_id': sec_id, 'tag_id': tag})
        #             order_id += 1

    def _add_ds_doc(self, ds_doc):
        doc = Ds_Doc(**ds_doc)
        db.session.add(doc)
        db.session.flush()
        doc_id = doc.doc_id
        return doc_id

    def _update_ds_doc(self, ds_doc):
        doc_id = ds_doc.get('doc_id')
        db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).update(ds_doc)
        return doc_id

    def get_doc_type(self, doc_type='', orient='list'):
        """
        :param doc_type:
        :param orient: 'list', 'dict'
        :return:
        """
        q = db.session.query(DSDocType)
        if doc_type:
            q = q.filiter(DSDocType.doc_type == doc_type)
        # q = q.order_by(DSDocType.doc_type_id)
        if orient.lower() == 'dict':
            doc_types = dict()
        else:
            doc_types = []
        for doc_type_info in q:
            if orient.lower() == 'dict':
                doc_types[doc_type_info.doc_type] = doc_type_info.to_dict()
            else:
                doc_types.append(doc_type_info.to_dict())
        return doc_types

    def get_doc_status(self):
        q = db.session.query(DSDocStatus).order_by(DSDocStatus.status_id)
        status_list = []
        for status in q:
            status_list.append(status.to_dict())
        return status_list

    def get_ds_doc_by_tag(self, model_id, tag_id, doc_type):
        doc_tag_obj = CtrlDocTag()
        desc_list = doc_tag_obj.get_descendant_tags(tag_id)
        tag_id_list = [tag_id] + desc_list
        q = db.session.query(Ds_Doc).outerjoin(DSSection, Ds_Doc.doc_id == DSSection.doc_id)\
            .outerjoin(DSSectionTag, DSSection.sec_id == DSSectionTag.sec_id)\
            .filter(Ds_Doc.model_id == model_id)
        q = q.filter(Ds_Doc.doc_type == doc_type)
        q = q.filter(DSSectionTag.tag_id.in_(tag_id_list))
        ds_docs = q.order_by(Ds_Doc.doc_id).distinct()
        ds_docs_list = []
        for ds_doc in ds_docs:
            ds_doc = ds_doc.to_dict()
            ds_doc['create_time'] = ds_doc.get('create_time').strftime("%Y-%m-%d %H:%M:%S")
            ds_doc['update_time'] = ds_doc.get('update_time').strftime("%Y-%m-%d %H:%M:%S")
            ds_docs_list.append(ds_doc)
        return ds_docs_list

    def delete(self, doc_id, commit_user, commit=True):
        """
        #删除整个文档
        :param doc_id:
        :return:
        """
        update_time = self.get_current_time()
        commit_list = []
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        commit_list += CtrlDSAstah().delete_by_doc_id(doc_id)
        commit_list += CtrlDSRelSpec().delete_by_doc_id(doc_id)
        commit_list += CtrlDsIf().delete_by_doc_id(doc_id)
        commit_list += CtrlDSSection().delete_section(doc_id, commit_user)
        commit_list += CtrlDSScene().del_rel_tag(doc_id)
        doc_log_list, error = self.delete_ds_doc(doc_id)
        if error:
            return error
        commit_list += doc_log_list
        if not commit:
            return commit_list
        self.commit_log(commit_list, commit_user, update_time)
        db.session.commit()
        from app.db import cache
        cache.delete('get_model_tree')  # 删除缓存
        return None

    def delete_ds_doc(self, doc_id):
        doc_rel_q = db.session.query(DSDocDetailRel).filter(DSDocDetailRel.doc_id == doc_id)
        doc_rel_list = []
        for doc_rel in doc_rel_q:
            doc_rel_list.append(doc_rel.to_dict())
        commit_list = self.add_list(DSDocDetailRel, [], doc_rel_list, DSDocDetailRel.gid, [])
        parent_doc_q = (db.session.query(Ds_Doc)
                        .outerjoin(DSDocDetailRel, Ds_Doc.doc_id == DSDocDetailRel.doc_id)
                        .filter(DSDocDetailRel.parent_doc_id == doc_id).first())
        if parent_doc_q:
            parent_doc_title = parent_doc_q.title
            return commit_list, '请先删除详细设计：%s' % (parent_doc_title, )
        ds_doc_q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id)
        old_data_list = []
        new_data_list = []
        for ds_doc in ds_doc_q:
            old_data_list.append(ds_doc.to_dict())
        commit_list += self.add_list(self.db_object, new_data_list, old_data_list,
                                     self.key_col, self.col_list)
        return commit_list, None

    def get_doc_ver(self, doc_id):
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
        if q:
            return q.micro_ver
        return None

    def update_doc_ver(self, doc_id, editor):
        """
        更新文档版本(旧的)
        :param doc_id:
        :param editor:
        :return:
        """
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
        if q:
            q.micro_ver = self.update_version(q.micro_ver)
            q.editor = editor
            q.update_time = self.get_current_time()
            db.session.commit()

    def update_ver(self, doc_id, commit_user):
        """
        更新文档版本
        :param sec_id:
        :return:返回log信息
        """
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
        old_doc = q.to_dict()
        new_doc = copy.deepcopy(old_doc)
        new_doc['micro_ver'] = self.update_version(old_doc['micro_ver'])
        new_doc[Ds_Doc.editor.name] = commit_user
        log_dict = self.common_add(self.db_object, new_doc, old_doc,
                                   self.col_list, self.key_col, diff_required=False)
        return log_dict

    def write_db_journal(self, doc_id, username, update_time):
        """
        备份整个设计文档
        :param doc_id:
        :param username:
        :param update_time:
        :return:
        """
        from app.ctrl.ctrl_journal import CtrlJournal
        db_objs = self.get_db_for_journal2(doc_id)
        result = CtrlJournal().write(db_objs, username=username, update_time=update_time)
        return result

    def get_db_for_journal(self, doc_id):
        """设计方档整体备份使用
        :param doc_id:
        :return:
        """
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        db_objs = []
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
        ds_doc = q
        astahs = CtrlDSAstah().get_db_for_journal(doc_id)
        if astahs:
            db_objs += astahs
        ifs = CtrlDsIf().get_db_for_journal(doc_id)
        if ifs:
            db_objs += ifs
        specs = CtrlDSRelSpec().get_db_for_journal(doc_id)
        if specs:
            db_objs += specs
        drbfms = CtrlDSScene().get_db_for_journal(doc_id)
        if drbfms:
            db_objs += drbfms
        sections = CtrlDSSection().get_db_for_journal(doc_id)
        if sections:
            db_objs += sections
        if ds_doc:
            db_objs.append(ds_doc)
        return db_objs

    def get_db_for_journal2(self, doc_id):
        """设计方档整体备份使用
        :param doc_id:
        :return:
        """
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        db_objs = []
        q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
        ds_doc = q
        # astahs = CtrlDSAstah().get_db_for_journal(doc_id)
        # if astahs:
        #     db_objs += astahs
        # ifs = CtrlDsIf().get_db_for_journal(doc_id)
        # if ifs:
        #     db_objs += ifs
        # specs = CtrlDSRelSpec().get_db_for_journal(doc_id)
        # if specs:
        #     db_objs += specs
        # drbfms = CtrlDSScene().get_db_for_journal(doc_id)
        # if drbfms:
        #     db_objs += drbfms

        sections = CtrlDSSection().get_db_for_journal(doc_id)
        if sections:
            db_objs += sections
        if ds_doc:
            db_objs.append(ds_doc)
        return db_objs

    def update_doc_status(self, data_info):
        doc_id = data_info.get('doc_id')
        status = data_info.get('status')
        commit_user = data_info.get('commit_user')
        update_time = self.get_current_time()
        try:
            q_status = db.session.query(DSDocStatus).filter(DSDocStatus.status_name == status).first()
            if not q_status:
                return False, '该状态不存在！'
            status_id = q_status.status_id
            doc_q = db.session.query(Ds_Doc).filter(Ds_Doc.doc_id == doc_id).first()
            old_doc = doc_q.to_dict()
            if status_id != old_doc.get(Ds_Doc.status.name):
                new_doc = copy.deepcopy(old_doc)
                new_doc[Ds_Doc.status.name] = status_id
                new_doc[Ds_Doc.update_time.name] = update_time
                new_doc[Ds_Doc.editor.name] = commit_user
                new_doc['micro_ver'] = self.update_version(old_doc.get('micro_ver'))
                log_dict = self.common_add(self.db_object, new_doc, old_doc, self.col_list,
                                           self.key_col, diff_required=False)
                self.commit_log([log_dict], commit_user, update_time)
                if status_id == WORK_LOCK_STATUS:
                    result = self.write_db_journal(doc_id, commit_user, update_time)
                    if not result:
                        return False, '备份文档失败！'
            db.session.commit()
            return True, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def get_basic_doc_for_detail(self, proj_id, model_id):
        q = (db.session.query(Ds_Doc.doc_id, Ds_Doc.title, Ds_Doc.summary)
             .filter(Ds_Doc.proj_id == proj_id)
             .filter(Ds_Doc.model_id == model_id)
             .filter(Ds_Doc.doc_type == 'BASIC'))
        doc_list = []
        for doc in q:
            doc_dict = dict()
            doc_dict['doc_id'] = doc[0]
            doc_dict['title'] = doc[1]
            doc_dict['summary'] = doc[2]
            doc_list.append(doc_dict)
        return doc_list

    def copy_basic_to_detail(self, basic_doc_id, commit_user, ds_doc):
        """
        把基本设计的内容拷贝到详细设计
        :param doc_id:
        :return:
        """
        update_time = ds_doc.get('update_time')
        commit_log_list = []
        doc_log = self.common_add(self.db_object, ds_doc, None, self.col_list, self.key_col)
        detail_doc_id = doc_log.get('key_id')
        self.add_detail_doc_rel(basic_doc_id, detail_doc_id, commit_log_list)
        basic_doc_data = self.get_doc(basic_doc_id, detail='detail')
        sub_list = basic_doc_data.get('sub')
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        doc_spec_list, status = CtrlDSRelSpec().get_by_doc_id(basic_doc_id, None)
        self.copy_ds_spec(detail_doc_id, None, doc_spec_list, commit_log_list)
        commit_log_list += self.copy_doc_sub(sub_list, detail_doc_id, commit_user, update_time)
        self.commit_log(commit_log_list, commit_user, update_time)
        return detail_doc_id, commit_log_list

    def copy_doc_sub(self, sub_list, doc_id, commit_user, update_time, parent_sec_id=0):
        commit_list = []
        for doc_sub in sub_list:
            doc_sub.pop('sub')
            sec_type = doc_sub.get('sec_type')
            if sec_type == 'ASTAH':  # 成果物文件
                astah_files = doc_sub.get('astah_files')
                self.copy_ds_astah(astah_files, doc_id, commit_user, update_time, commit_list)
            elif sec_type in ('BLOCK', 'CLASS', 'COMMON'):
                self.copy_ds_session(doc_sub, doc_id, commit_list, parent_sec_id)
            elif sec_type == 'USERCASE':
                self.copy_ds_usecase(doc_sub, doc_id, commit_list)
            elif sec_type == 'IF':  # IF接口
                self.copy_ds_if(doc_id, doc_sub, commit_list)
            # elif sec_type == 'SPEC':  # 式样书
            #     spec_list = doc_sub.get('specs')
            #     self.copy_ds_spec(doc_id, parent_sec_id, spec_list, commit_list)
            # elif sec_type == 'SCENE':  # 场景
            #     scene_list = doc_sub.get('scenes')
            #     self.copy_ds_scene(doc_id, parent_sec_id, scene_list, commit_list)
            # elif sec_type == 'RESOURCE':  # 资源
            #     self.copy_ds_resource(doc_sub, parent_sec_id, commit_list)
            # elif sec_type == 'CONSIDER':  # 考虑点
            #     considers = doc_sub.get('considers')
            #     self.copy_ds_consider(parent_sec_id, considers, commit_list)
        return commit_list

    def copy_ds_usecase(self, usecas_data, doc_id, commit_list):
        table_list = usecas_data.get('table_list')
        old_new_dict = {}
        if table_list:
            for usecase in table_list:
                sec_id = usecase.get('sec_id')
                basic_usecase = self.get_old_data(DSSection, DSSection.sec_id, sec_id)
                usecase_id = self.copy_ds_session(basic_usecase[0], doc_id, commit_list)
                seq_list = usecase.get('seq_list')
                std_list = usecase.get('std_list')
                self.copy_usecase_rel(usecase_id, seq_list+std_list, doc_id, commit_list, old_new_dict)
                spec_list = usecase.get('spec_list')
                self.copy_ds_spec(doc_id, usecase_id, spec_list, commit_list)

    def copy_usecase_rel(self, usecase_id, data_list, doc_id, commit_list, old_new_dict):
        from app.db.ds_section import DSSectionRel
        for data in data_list:
            sec_id = data.get('sec_id')
            sec_type = data.get('sec_type')
            if sec_id not in old_new_dict:
                basic_data = self.get_old_data(DSSection, DSSection.sec_id, sec_id)
                new_sec_id = self.copy_ds_session(basic_data[0], doc_id, commit_list)
                if sec_type == 'SEQUENCE':
                    # basic_activity = self.get_old_data(DSSection, DSSection.parent_sec_id, basic_id)
                    resource_list = CtrlDSSection()._get_resource(sec_id)
                    for resource in resource_list:
                        self.copy_ds_resource(resource, new_sec_id, commit_list)
                    # for activity in basic_activity:
                    #     self.copy_ds_session(activity, doc_id, commit_list, basic_id)
                    old_new_dict[sec_id] = new_sec_id
            seq_rel = {'sec_id': old_new_dict.get(sec_id), 'sec_rel_id': usecase_id}
            rel_log = self.common_add(DSSectionRel, seq_rel, None, [], DSSectionRel.gid)
            commit_list.append(rel_log)

    def add_detail_doc_rel(self, basic_doc_id, detail_doc_id, commit_list):
        rel_data = {'doc_id': detail_doc_id, 'parent_doc_id': basic_doc_id}
        rel_data_log = self.common_add(DSDocDetailRel, rel_data, None, [], DSDocDetailRel.gid)
        commit_list.append(rel_data_log)

    def copy_ds_astah(self, astah_files, doc_id, commit_user, update_time, commit_list):
        from app.db.ds_doc import DSDocAstahRel
        from app.ctrl.ctrl_attach import CtrlDSAttach
        for file in astah_files:
            file['attach_id'] = None
            file['committer'] = commit_user
            file['update_time'] = update_time
            file['commit_time'] = update_time
            file['micro_ver'] = 1
            attach_log = CtrlDSAttach().add2(file, commit=False)
            attach_id = attach_log.get('key_id')
            astah_rel_info = {'doc_id': doc_id,
                              'attach_id': attach_id}
            astah_rel_log = self.common_add(DSDocAstahRel, astah_rel_info, None, [], DSDocAstahRel.gid)
            commit_list.append(attach_log)
            commit_list.append(astah_rel_log)

    def copy_ds_session(self, section_info, doc_id, commit_list, parent_sec_id=0):
        from app.db.ds_section import DSSection
        section_info['sec_id'] = None
        section_info['doc_id'] = doc_id
        section_info['parent_sec_id'] = parent_sec_id
        section_info['micro_ver'] = 1
        if section_info[DSSection.content.name]:
            section_info[DSSection.content.name] = section_info[DSSection.content.name].replace('<br>', '\\n')
        section_log = self.common_add(DSSection, section_info, None, [], DSSection.sec_id)
        sec_id = section_log.get('key_id')
        commit_list.append(section_log)
        return sec_id

    def copy_ds_if(self, doc_id, if_info, commit_list):
        from app.db.ds_doc_if import DSDocIf
        if 'sec_type' in if_info:
            if_info.pop('sec_type')
        if_info['if_id'] = None
        if_info['doc_id'] = doc_id
        if_info['micro_ver'] = 1
        if_log = self.common_add(DSDocIf, if_info, None, [], DSDocIf.if_id)
        commit_list.append(if_log)

    def copy_ds_spec(self, doc_id, sec_id, spec_list, commit_list):
        from app.db.ds_rel_specification import DSRelSpec
        for spec_info in spec_list:
            new_spec = dict()
            new_spec['gid'] = None
            new_spec['doc_id'] = doc_id
            new_spec['sec_id'] = sec_id
            new_spec['spec_id'] = spec_info.get('spec_id')
            new_spec['func_id'] = spec_info.get('func_id')
            spec_log = self.common_add(DSRelSpec, new_spec, None, [], DSRelSpec.gid)
            commit_list.append(spec_log)

    def copy_ds_scene(self, doc_id, sec_id, scene_list, commit_list):
        from app.db.ds_scene import DSRelScene
        for scene_info in scene_list:
            new_scene = dict()
            new_scene['gid'] = None
            new_scene['doc_id'] = doc_id
            new_scene['sec_id'] = sec_id
            new_scene['scene_id'] = scene_info.get('scene_id')
            new_scene['change'] = scene_info.get('change')
            new_scene['alter'] = scene_info.get('alter')
            scene_log = self.common_add(DSRelScene, new_scene, None, [], DSRelScene.gid)
            commit_list.append(scene_log)

    def copy_ds_resource(self, resource_info, sec_id, commit_list):
        from app.db.ds_section import DSSectionResource
        resource = dict()
        resource['sec_id'] = sec_id
        resource['resource_id'] = resource_info.get('resource_id')
        resource['content'] = resource_info.get('val')
        resource['operator'] = resource_info.get('operator')
        resource['unit'] = resource_info.get('unit')
        resource['value'] = resource_info.get('value')
        if type(resource['value']) == str:
            resource['value'] = None
        resource_log = self.common_add(DSSectionResource, resource, None, [], DSSectionResource.gid)
        commit_list.append(resource_log)

    def copy_ds_consider(self, parent_sec_id, considers, commit_list):
        """
        复制基本设计的考虑点
        :return:
        """
        from app.db.ds_doc import DSDocConsider
        for consider in considers:
            csd = dict()
            csd['sec_id'] = parent_sec_id
            csd['consider_id'] = consider.get('consider_id')
            csd['consider_content'] = consider.get('consider_content')
            csd['checked'] = consider.get('checked')
            csd_log = self.common_add(DSDocConsider, csd, None, [], DSDocConsider.gid)
            commit_list.append(csd_log)

    def _get_new_tilte(self, title):
        new_title = title.replace('基本设计', '详细设计')
        new_title = new_title.replace('BasicDesign', 'DetailDesign')
        return new_title






