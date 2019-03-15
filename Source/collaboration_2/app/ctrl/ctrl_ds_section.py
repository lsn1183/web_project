# -*- coding: UTF-8 -*-
import json
import copy
import pandas as pd
from sqlalchemy import or_, and_
from app.db import db
from app.db.ds_section import DSSectionRel
from app.db.ds_rel_specification import DSRelFun
from app.db.ds_section import DSSection, DSSectionTag, DSSectionType, DSSectionResource
from app.ctrl.ctrl_doc_tag import CtrlDocTag
from flask import current_app
from app.db.doc import Consider
from app.db.ds_doc import DSDocConsider
from app.db.ds_resource import DsResource
from app.db.ds_drbfm import DSDrbfm
from app.ctrl.ctrl_base import CtrlBase


class CtrlDSSection(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSSection.sec_id
        self.db_object = DSSection
        self.col_list = [DSSection.content.name, DSSection.explain.name,
                         DSSection.complement.name, DSSection.sec_title.name]

    def get_section_detail(self, doc_id, sec_type):
        section_list = self.get_section_by_type(doc_id, sec_type)
        if sec_type == "COMMON":
            table_list = self.get_uc_table(doc_id)
            return {"doc_id": doc_id, "sec_type": sec_type,
                    "section_list": section_list, "table_list": table_list}
        return {"doc_id": doc_id, "sec_type": sec_type, "section_list": section_list}

    def get_section_by_type(self, doc_id, sec_type, parent_sec_id=0):
        """
        根据类型和doc_id获取所有章节
        :param doc_id:
        :param sec_type:BLOCK/CLASS/COMMON/STD
        :return:
        """
        q = (db.session.query(DSSection)
             .filter(and_(DSSection.doc_id == doc_id,
                     DSSection.sec_type == sec_type,
                          DSSection.parent_sec_id == parent_sec_id))
             .order_by(DSSection.sec_id))
        section_list = []
        for sec in q:
            section_list.append(self.section_to_dict(sec))
        return section_list

    def get_usecase_detail(self, usecase_id):
        from app.db.model import Model
        from app.db.ds_doc import Ds_Doc
        usecase_dict = dict()
        q = (db.session.query(DSSection.sec_id, DSSection.sec_title, Model.title,
                              Ds_Doc.doc_type, DSSection.doc_id)
             .outerjoin(Ds_Doc, DSSection.doc_id == Ds_Doc.doc_id)
             .outerjoin(Model, Ds_Doc.model_id == Model.model_id)
             .filter(DSSection.sec_id == usecase_id).all())
        if len(q):
            usecase = q[0]
            usecae_title = usecase[1]
            model_title = usecase[2]
            if not usecae_title:
                usecae_title = ""
            usecase_dict['usecase_id'] = usecase[0]
            usecase_dict['doc_type'] = usecase[3]
            usecase_dict['doc_id'] = usecase[4]
            usecase_dict['title'] = "%s(%s)" % (usecae_title, model_title)
            usecase_dict['UsecaseTable'] = self.get_uc_fun2(usecase_id)
            usecase_dict['Block'] = self.get_sub_by_usecase(usecase_id, sec_type="BLOCK")
            usecase_dict['Class'] = self.get_sub_by_usecase(usecase_id, sec_type="CLASS")
            usecase_dict['Usecase'] = self.get_sub_by_usecase(usecase_id, sec_type='COMMON')
            usecase_dict['Sequence'] = self.get_sub_by_usecase(usecase_id)
            usecase_dict['Statemachine'] = self.get_sub_by_usecase(usecase_id, sec_type="STD")
            usecase_dict['Other'] = self.get_sub_by_usecase(usecase_id, sec_type="OTHER")
            usecase_dict['DRBFM'] = []  # TODO@yuyin
        return usecase_dict

    # def get_sequence(self, usecase_id):
    #     old_data_list, error = self.session_is_exist(usecase_id)
    #     if error:
    #         return [], error
    #     doc_id = old_data_list[0].get('doc_id')

    def get_sub_by_usecase(self, usecase_id, sec_type="SEQUENCE"):
        """
        获取usecase下的sequence, block, class, common, std
        :param usecase_id:
        :return:
        """
        q = (db.session.query(DSSection)
             .filter(DSSection.parent_sec_id == usecase_id)
             .filter(DSSection.sec_type == sec_type)
             .order_by(DSSection.sec_id))
        sec_list = []
        for sec in q:
            sec_dict = self.section_to_dict(sec)
            if sec_type == "SEQUENCE":
                sec_dict['Resource'] = self._get_resource(sec.sec_id)
                sec_dict['Activity'] = self.get_activitys(sec.sec_id)
            sec_list.append(sec_dict)
        return sec_list

    def get_activitys(self, sequence_id, sec_type='Activity'):
        """
        获取Activity图
        :param sequence_id:
        :return:
        """
        q = db.session.query(DSSection).filter(and_(DSSection.parent_sec_id == sequence_id,
                                                    DSSection.sec_type == sec_type))
        activity_list = []
        for section in q:
            sec_dict = self.section_to_dict(section)
            activity_list.append(sec_dict)
        return activity_list

    def get_uc_table(self, doc_id):
        i = 1
        table_list = []
        usecase_list = self.get_section_by_type(doc_id, "USERCASE")
        for usecase in usecase_list:
            uc_dict = dict()
            uc_section_id = usecase.get('sec_id')
            uc_dict['sec_id'] = uc_section_id
            uc_dict['number'] = 'UC' + str(i)
            uc_dict['sec_title'] = usecase.get('sec_title')
            uc_dict['explain'] = usecase.get('explain')
            # uc_dict['func_id'] = self.get_uc_fun(uc_section_id)
            uc_dict['micro_ver'] = usecase.get('micro_ver')
            i += 1
            table_list.append(uc_dict)
        return table_list

    def get_uc_fun(self, usecase_id):
        """
        取usecase的机能点
        :param usecase_id:
        :return:
        """
        func_id = ""
        q = db.session.query(DSRelFun).filter(DSRelFun.sec_id == usecase_id).all()
        if len(q):
            func_id = q[0].func_id
        return func_id

    def get_uc_table2(self, doc_id):
        table_list = []
        usecase_list = self.get_section_by_type(doc_id, "USERCASE")
        for usecase in usecase_list:
            uc_section_id = usecase.get('sec_id')
            table_list += self.get_uc_fun2(uc_section_id)
        return table_list

    def get_uc_fun2(self, usecase_id):
        table_list = []
        parent_uc = self.get_by_sec_id(usecase_id)
        doc_id = parent_uc.get('doc_id')
        sub_uc_list = self.get_section_by_type(doc_id, "USERCASE", parent_sec_id=usecase_id)
        if not sub_uc_list:
            uc_dict = dict()
            uc_dict['level1_sec_id'] = usecase_id
            uc_dict['sec_level1'] = parent_uc.get('sec_title')
            uc_dict['level2_sec_id'] = 0
            uc_dict['sec_level2'] = ""
            uc_dict['explain'] = parent_uc.get('explain')
            uc_dict['func_list'] = self._get_uc_fun(usecase_id)
            table_list.append(uc_dict)
        else:
            for sub_uc in sub_uc_list:
                uc_dict = dict()
                uc_dict['level1_sec_id'] = usecase_id
                uc_dict['sec_level1'] = ""
                if sub_uc_list.index(sub_uc) == 0:
                    uc_dict['level1_sec_id'] = usecase_id
                    uc_dict['sec_level1'] = parent_uc.get('sec_title')
                uc_dict['level2_sec_id'] = sub_uc.get('sec_id')
                uc_dict['sec_level2'] = sub_uc.get('sec_title')
                uc_dict['explain'] = sub_uc.get('explain')
                uc_dict['func_list'] = self._get_uc_fun(sub_uc.get('sec_id'))
                table_list.append(uc_dict)
        return table_list

    def _get_uc_fun(self, usecase_id):
        """
        取usecase的机能信息
        :param usecase_id:
        :return:
        """
        from app.db.spec.specification import Specification
        from app.db.spec.specification import SpecVersion
        func_list = []
        q = (db.session.query(DSRelFun.gid, DSRelFun.ver_id, DSRelFun.func_name,
             DSRelFun.func_id, SpecVersion.html_url, Specification.spec_file_name)
             .outerjoin(SpecVersion, DSRelFun.ver_id == SpecVersion.ver_id)
             .outerjoin(Specification, SpecVersion.spec_id == Specification.spec_id)
             .filter(DSRelFun.sec_id == usecase_id).all())
        for fun in q:
            fun_dict = dict()
            fun_dict['gid'] = fun[0]
            fun_dict['ver_id'] = fun[1]
            fun_dict['func_name'] = fun[2]
            fun_dict['func_id'] = fun[3]
            fun_dict['html_url'] = fun[4]
            fun_dict['spec_file_name'] = fun[5]
            func_list.append(fun_dict)
        return func_list

    def get_level2_usecase(self, usecase_id):
        """"获取一个usecase下的二级usecase"""
        level2_list = []
        parent_uc = self.get_by_sec_id(usecase_id)
        doc_id = parent_uc.get('doc_id')
        sub_uc_list = self.get_section_by_type(doc_id, "USERCASE", parent_sec_id=usecase_id)
        uc_dict = dict()
        uc_dict['sec_id'] = usecase_id
        uc_dict['sec_title'] = parent_uc.get('sec_title')
        uc_dict['micro_ver'] = parent_uc.get('micro_ver')
        uc_dict['explain'] = parent_uc.get('explain')
        uc_dict['func_list'] = self._get_uc_fun(usecase_id)
        for sub_uc in sub_uc_list:
            sub_dict = dict()
            sub_dict['sec_id'] = sub_uc.get('sec_id')
            sub_dict['sec_title'] = sub_uc.get('sec_title')
            sub_dict['micro_ver'] = sub_uc.get('micro_ver')
            sub_dict['explain'] = sub_uc.get('explain')
            sub_dict['func_list'] = self._get_uc_fun(sub_uc.get('sec_id'))
            level2_list.append(sub_dict)
        uc_dict['level2_list'] = level2_list
        return uc_dict

    def update_usecase_level2(self, data_json):
        commit_user = data_json.get("commit_user")
        level2_list = data_json.get("level2_list")
        parent_sec_id = data_json.get("sec_id")
        parent_uc = self.get_by_sec_id(parent_sec_id)
        update_time = self.get_current_time()
        doc_id = parent_uc.get('doc_id')
        if not doc_id:
            return False, '没有指定文档！'
        commit_list = []
        try:
            if not level2_list:
                level2_list = [{'sec_id': parent_sec_id, 'sec_title': data_json.get('sec_title'),
                                'explain': data_json.get('explain'), 'micro_ver': data_json.get('micro_ver'),
                                'func_list': data_json.get('func_list')}]
                commit_list += self.delete_excess(doc_id, level2_list, "USERCASE", parent_sec_id)
                log_list, error = self._section_commont(doc_id, "USERCASE", level2_list, parent_sec_id=0)
            else:
                commit_list += self.delete_excess(doc_id, level2_list, "USERCASE", parent_sec_id)
                log_list, error = self._section_commont(doc_id, "USERCASE", level2_list, parent_sec_id)
            if error:
                return False, error
            commit_list += log_list
            if commit_list:
                from app.ctrl.ctrl_ds_doc import CtrlDsDoc
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def update_func_rel(self, sec_id, func_list):
        old_data_list = self.get_old_data(DSRelFun, DSRelFun.sec_id, sec_id)
        new_data_list = []
        for func in func_list:
            new_data = {DSRelFun.gid.name: func.get("gid"),
                        DSRelFun.sec_id.name: sec_id,
                        DSRelFun.ver_id.name: func.get("ver_id"),
                        DSRelFun.func_name.name: func.get("func_name"),
                        DSRelFun.func_id.name: func.get("func_id")}
            new_data_list.append(new_data)
        log_list = self.add_list(DSRelFun, new_data_list, old_data_list, DSRelFun.gid,
                                 [DSRelFun.func_id.name, DSRelFun.func_name.name, DSRelFun.ver_id])
        return log_list

    def section_to_dict(self, section):
        sec_dict = dict()
        sec_dict['sec_id'] = section.sec_id
        sec_dict['sec_title'] = section.sec_title
        sec_dict['content'] = self.join_ip_message(section.content)
        sec_dict['explain'] = section.explain
        sec_dict['complement'] = section.complement
        sec_dict['micro_ver'] = section.micro_ver
        for key in sec_dict:
            if not sec_dict[key]:
                sec_dict[key] = ""
        return sec_dict

    def section_commont(self, data_json):
        """
        BLOCK/CLASS/COMMON/STD图的编辑
        :param data_json:
        :return:
        """
        try:
            doc_id = data_json.get("doc_id")
            sec_type = data_json.get("sec_type")
            commit_user = data_json.get("commit_user")
            update_time = self.get_current_time()
            if not doc_id:
                return False, '没有指定文档！'
            from app.ctrl.ctrl_ds_doc import CtrlDsDoc
            doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
            if error:
                return False, error
            section_list = data_json.get("section_list")
            table_list = data_json.get("table_list")
            commit_list = self.delete_excess(doc_id, section_list, sec_type)
            log_list, error = self._section_commont(doc_id, sec_type, section_list)
            if error:
                return False, error
            commit_list += log_list
            if table_list:
                commit_list += self.delete_excess(doc_id, table_list, "USERCASE")
                log_list, error = self._section_commont(doc_id, "USERCASE", table_list)
                if error:
                    return False, error
                commit_list += log_list
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def _section_commont(self, doc_id, sec_type, section_list, parent_sec_id=0):
        commit_list = []
        for section in section_list:
            sec_id = section.get('sec_id')
            if sec_id:
                sec_id = int(sec_id)
            else:
                sec_id = 0
            micro_ver = section.get('micro_ver')
            image_url = []
            if section.get('content'):
                image_url = section.get('content')
            image_url = self.remove_ip_message(image_url)
            image_url = json.dumps(image_url, ensure_ascii=False)
            old_data_list, error = self.session_is_exist(sec_id)
            if error:
                return [], error
            new_data = self.built_new_section(section, sec_id, doc_id, content=image_url,
                                              parent_sec_id=parent_sec_id, sec_type=sec_type)
            if old_data_list:
                old_data = old_data_list[0]
                old_micro_ver = old_data.get('micro_ver')
                flag, error = self.diff_ver(micro_ver, old_micro_ver)
                if not flag:
                    return [], error
            else:
                old_data = None
            new_data['micro_ver'] = self.update_version(micro_ver)
            log_dict = self.common_add(self.db_object, new_data, old_data,
                                       self.col_list, self.key_col)
            if log_dict:
                sec_id = log_dict.get('key_id')
                commit_list.append(log_dict)
            if sec_type == "SEQUENCE":
                resource_list = section.get('Resource')
                activity_list = section.get('Activity')
                activity_log, error = self._section_commont(doc_id, "Activity", activity_list,
                                                            parent_sec_id=sec_id)
                if error:
                    return 0, error
                commit_list += activity_log
                if resource_list:
                    commit_list += self.add_sec_resource(sec_id, resource_list)
            if sec_type == "USERCASE":
                func_list = section.get('func_list')
                if func_list is not None:
                    commit_list += self.update_func_rel(sec_id, func_list)
        return commit_list, None

    def delete_excess(self, doc_id, section_list, sec_type, parent_sec_id=0):
        """
        新旧section对比，挑出要删除的section进行删除
        :param parent_sec_id:
        :param sequence_list:
        :param sec_type:
        :return:
        """
        commit_list = []
        seq_list = self.get_old_data(DSSection, [DSSection.doc_id, DSSection.sec_type, DSSection.parent_sec_id],
                                     {'doc_id': doc_id, 'sec_type': sec_type, 'parent_sec_id': parent_sec_id})
        old_sec_id_list = self._to_sec_id_list(seq_list)
        new_sec_id_list = self._to_sec_id_list(section_list)
        for sec_id in old_sec_id_list:
            if sec_id not in new_sec_id_list:
                commit_list += self.delete_usecase_sub(sec_id)
        return commit_list

    def built_new_section(self, section, sec_id, doc_id, content=None, parent_sec_id=0, sec_type='USERCASE'):
        new_section = {DSSection.sec_id.name: sec_id,
                       DSSection.doc_id.name: doc_id,
                       DSSection.parent_sec_id.name: parent_sec_id,
                       DSSection.sec_type.name: sec_type,
                       DSSection.content.name: content,
                       DSSection.sec_title.name: section.get('sec_title'),
                       DSSection.explain.name: section.get('explain'),
                       DSSection.complement.name: section.get('complement'),
                       DSSection.ver.name: None,
                       DSSection.order_id.name: None,
                       DSSection.required.name: None}
        return new_section

    def update_uc_sub(self, data_json):
        try:
            usecase_id = data_json.get("sec_id")
            commit_user = data_json.get("commit_user")
            update_time = self.get_current_time()
            if not usecase_id:
                return False, '没有指定USECASE！'
            old_data_list, error = self.session_is_exist(usecase_id)
            if error:
                return [], error
            doc_id = old_data_list[0].get('doc_id')
            from app.ctrl.ctrl_ds_doc import CtrlDsDoc
            doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
            if error:
                return False, error
            section_list = data_json.get('section_list')
            sec_type = data_json.get('sec_type')
            commit_list = self.delete_excess(doc_id, section_list, sec_type, usecase_id)
            log_list, error = self._section_commont(doc_id, sec_type, section_list, parent_sec_id=usecase_id)
            if error:
                return False, error
            commit_list += log_list
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"


#################################################################################################################
    def get_usecase_tree(self, doc_id):
        """
        :param doc_id:
        :return: 返回章节树
        """
        usercase_q = db.session.query(DSSection)\
            .filter(DSSection.doc_id == doc_id, DSSection.sec_type == 'USERCASE')\
            .order_by(DSSection.sec_id)
        # block_q = db.session.query(DSSection) \
        #     .filter(DSSection.doc_id == doc_id, DSSection.sec_type == 'BLOCK')
        usercase_list = self.to_sec_list(usercase_q)
        # block_list = self.to_sec_list(block_q)
        usercase_list = self.get_usercase_sub(usercase_list)
        # block_list = self.get_usercase_sub(block_list)
        return usercase_list

    def get_usecase_tree2(self, doc_id):
        q = (db.session.query(DSSection)
             .filter(DSSection.doc_id == doc_id, DSSection.sec_type == "USERCASE")
             .order_by(DSSection.sec_id))
        usecase_list = []
        for uc in q:
            usecase_list.append(uc.to_dict())
        usecase_priview = dict()
        usecase_priview['sec_type'] = 'USERCASE'
        seq_list = self.get_sequence2(doc_id)
        seqNo_dict = {}
        for seq in seq_list:
            seqNo_dict[seq.get('sec_id')] = 'Sequence%s' % str(seq_list.index(seq)+1)
        usecase_priview['table_list'] = self.get_usecase_table(usecase_list, seqNo_dict)
        # from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        # usecase_priview['spec_list'] = CtrlDSRelSpec().get(doc_id)
        usecase_priview['sub'] = []
        return usecase_priview

    def get_sec_ver(self, sec_id):
        """
        获取章节版本号
        :param sec_id:
        :return:
        """
        ver = 0
        section = db.session.query(DSSection).filter(DSSection.sec_id == sec_id).first()
        if section:
            ver = section.micro_ver
        return ver

    def get_usecase_by_doc_id(self, doc_id, sec_type='USERCASE'):
        usecase_dict = dict()
        usecase_list = []
        public_sec_id = None
        public_usecase_content = None
        public_micro_ver = None
        public_usecase = self.get_session_by_doc_id(doc_id, 'COMMON')
        if public_usecase:
            public_sec_id = public_usecase[0].get('sec_id')
            public_usecase_content = public_usecase[0].get('content')
            public_micro_ver = public_usecase[0].get('micro_ver')
        sec_list = self.get_session_by_doc_id(doc_id, sec_type)
        for sec in sec_list:
            content = sec.get("content")
            content = content.replace('<br>', '\\n')
            usecase_list.append({
                                 "sec_id": sec.get("sec_id"),
                                 "content": content,
                                 "micro_ver": sec.get("micro_ver")
                                 })
        usecase_dict['doc_id'] = doc_id
        usecase_dict['public_sec_id'] = public_sec_id
        usecase_dict['public_usecase_content'] = public_usecase_content
        usecase_dict['public_micro_ver'] = public_micro_ver
        usecase_dict['commit_user'] = None
        usecase_dict['usecase_list'] = usecase_list
        return usecase_dict

    def get_session_by_doc_id(self, doc_id, sec_type):
        q = (db.session.query(DSSection)
             .filter(DSSection.doc_id == doc_id, DSSection.sec_type == sec_type)
             .order_by(DSSection.sec_id))
        sec_list = self.to_sec_list(q)
        return sec_list

    def get_session_by_doc(self, doc_id, sec_type):
        q = (db.session.query(DSSection)
             .filter(DSSection.doc_id == doc_id, DSSection.sec_type == sec_type)
             .order_by(DSSection.sec_id))
        sec_list = []
        for sec in q:
            sec_list.append(sec.to_dict())
        return sec_list

    def get_all_usecase_tille(self, doc_id, sec_type='USERCASE'):
        q = (db.session.query(DSSection)
             .filter(DSSection.doc_id == doc_id, DSSection.sec_type == sec_type)
             .order_by(DSSection.sec_id))
        usecase_list = []
        i = 1
        for uc in q:
            usecase = dict()
            usecase['sec_id'] = uc.sec_id
            content = json.loads(uc.content)
            usecase['number'] = 'UC'+str(i)
            usecase['title'] = content[0].get('title')
            usecase['val'] = content[0].get('val')
            usecase_list.append(usecase)
            i += 1
        return usecase_list

    def get_usecase_table(self, usecase_list, seqNo_dict):
        i = 1
        table_list = []
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        spec_obj = CtrlDSRelSpec()
        for uc in usecase_list:
            usecase = dict()
            uc_section_id = uc.get('sec_id')
            usecase['sec_id'] = uc_section_id
            content = json.loads(uc.get('content'))
            usecase['number'] = 'UC'+str(i)
            usecase['title'] = content[0].get('title')
            usecase['val'] = content[0].get('val')
            sec_list = self.get_usecase_rel_section(uc_section_id)
            seq_list, std_list = [], []
            for sec in sec_list:
                sub_dict = dict()
                if sec.get('sec_type') == 'SEQUENCE':
                    sub_dict['sec_type'] = sec.get('sec_type')
                    sub_dict['sec_id'] = sec.get('sec_id')
                    sub_dict['number'] = seqNo_dict.get(sec.get('sec_id'))
                    sub_dict['title'] = sec.get('title')
                    sub_dict['val'] = sec.get('val')
                    seq_list.append(sub_dict)
                # elif sec.get('sec_type') == 'STD':
                #     sub_dict['sec_type'] = sec.get('sec_type')
                #     sub_dict['sec_id'] = sec.get('sec_id')
                #     sub_dict['number'] = 'Statemachine'+str(n)
                #     sub_dict['title'] = sec.get('title')
                #     sub_dict['val'] = sec.get('val')
                #     std_list.append(sub_dict)
                #     n += 1
            usecase['seq_list'] = seq_list
            # usecase['std_list'] = std_list
            # 获取spec_list
            usecase['spec_list'] = spec_obj.get_by_sec_id(uc_section_id)
            i += 1
            table_list.append(usecase)
        return table_list

    def get_usecase_rel_section(self, usecase_id):
        q = (db.session.query(DSSection)
             .outerjoin(DSSectionRel, DSSection.sec_id == DSSectionRel.sec_id)
             .filter(DSSectionRel.sec_rel_id == usecase_id)
             .order_by(DSSection.sec_id))
        sec_list = []
        for sec in q:
            sec_list.append(sec.to_dict())
        return sec_list

    def get_db_for_journal(self, doc_id):
        q = (db.session.query(DSSection)
             .filter(DSSection.doc_id == doc_id)
             .order_by(DSSection.sec_id))
        sections = q.all()
        db_objs = []
        for section in sections:
            sec_id = section.sec_id
            db_objs.append(section)
            if section.sec_type == 'SEQUENCE':
                # 资源
                resources = CtrlDSResource().get_db_for_journal(sec_id)
                db_objs += resources
            # UseCase与Sequence关系
            if section.sec_type == 'USERCASE':
                q = (db.session.query(DSSectionRel).
                     filter(DSSectionRel.sec_rel_id == sec_id))
                rel_objs = q.all()
                q_fun = (db.session.query(DSRelFun).
                         filter(DSRelFun.sec_id == sec_id).all())
                db_objs += q_fun
                db_objs += rel_objs
        return db_objs

    def to_sec_list(self, q_result):
        sec_list = []
        for q in q_result:
            sec = q.to_dict()
            if sec[DSSection.content.name]:
                sec[DSSection.content.name] = sec[DSSection.content.name].replace('\\n', '<br>')
            sec['sub'] = []
            sec_list.append(sec)
        return sec_list

    def get_usercase_sub(self, usercase_list):
        for usercase in usercase_list:
            usercase['sub'] = []
            sec_id = usercase.get('sec_id')
            spec_dict = self._get_spec(sec_id)
            scene_dict = self._get_scene(sec_id)
            seq_list = self._get_sequence(sec_id)
            consider_dict = self._get_consider(sec_id)
            std_list = self._get_std(sec_id)
            drbfm_dict = self._get_drbfm(sec_id)
            usercase['sub'].append(spec_dict)
            usercase['sub'].append(scene_dict)
            usercase['sub'] += seq_list
            usercase['sub'].append(consider_dict)
            usercase['sub'] += std_list
            usercase['sub'].append(drbfm_dict)
        return usercase_list

    def _get_spec(self, usecase_id):
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        spec_dict = dict()
        spec_type_dict, status = CtrlDSRelSpec().get(usecase_id)
        spec_dict['sec_type'] = 'SPEC'
        spec_dict['sec_id'] = usecase_id
        spec_dict['specs'] = spec_type_dict
        spec_dict['sub'] = []
        return spec_dict

    def _get_spec2(self, usecase_list):
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        uc_spec_list = []
        for uc in usecase_list:
            spec_dict = dict()
            spec_dict['sec_id'] = uc.get('sec_id')
            spec_type_dict, status = CtrlDSRelSpec().get(uc.get('sec_id'))
            spec_dict['specs'] = spec_type_dict
            uc_spec_list.append(spec_dict)
        return uc_spec_list

    def _get_scene(self, usecase_id):
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        scene_dict = dict()
        scene_list = CtrlDSScene().get_scene_by_sec(usecase_id)
        scene_dict['sec_id'] = usecase_id
        scene_dict['sec_type'] = 'SCENE'
        scene_dict['scenes'] = scene_list
        scene_dict['sub'] = []
        return scene_dict

    def _get_sequence(self, usecase_id):
        seqs = db.session.query(DSSection)\
            .filter(and_(DSSection.parent_sec_id == usecase_id, DSSection.sec_type == 'SEQUENCE'))\
            .order_by(DSSection.sec_id)
        seq_list = []
        for seq in seqs:
            seq_dict = seq.to_dict()
            if seq_dict[DSSection.content.name]:
                seq_dict[DSSection.content.name] = seq_dict[DSSection.content.name].replace('\\n', '<br>')
            seq_id = seq_dict.get('sec_id')
            resource_list = self._get_resource(seq_id)
            activity_list = self._get_activity(seq_id)
            seq_dict['sub'] = []
            seq_dict['sub'] += resource_list
            seq_dict['sub'] += activity_list
            seq_list.append(seq_dict)
        return seq_list

    def get_sequence2(self, doc_id):
        seqs = db.session.query(DSSection)\
            .filter(and_(DSSection.doc_id == doc_id, DSSection.sec_type == 'SEQUENCE'))\
            .order_by(DSSection.sec_id)
        seq_list = []
        for seq in seqs:
            seq_dict = seq.to_dict()
            if seq_dict[DSSection.content.name]:
                seq_dict[DSSection.content.name] = seq_dict[DSSection.content.name].replace('\\n', '<br>')
            seq_id = seq_dict.get('sec_id')
            resource_list = self._get_resource(seq_id)
            activity_list = self._get_activity(seq_id)
            seq_dict['sub'] = []
            seq_dict['sub'] += resource_list
            seq_dict['sub'] += activity_list
            seq_list.append(seq_dict)
        return seq_list

    def _get_activity(self, seq_id):
        activity_list = self.get_activity_list(seq_id)
        for resource in activity_list:
            resource["sub"] = []
        return activity_list

    def _get_resource(self, seq_id):
        resource_list = CtrlDSResource().get_resource_by_sec_id(seq_id)
        for resource in resource_list:
            resource['sec_id'] = seq_id
            resource['sec_type'] = "RESOURCE"
            resource["sub"] = []
        return resource_list

    def _get_consider(self, usecase_id):
        consider_dict = {'sec_id': usecase_id,
                         'sec_type': 'CONSIDER',
                         'considers': [], 'sub': []}
        consider_dict['considers'] = CtrlDSConsider().get(usecase_id)
        return consider_dict

    def _get_std(self, usecase_id):
        stds = db.session.query(DSSection) \
            .filter(and_(DSSection.parent_sec_id == usecase_id, DSSection.sec_type == 'STD')) \
            .order_by(DSSection.sec_id)
        std_list = []
        for std in stds:
            std_dict = std.to_dict()
            if std_dict[DSSection.content.name]:
                std_dict[DSSection.content.name] = std_dict[DSSection.content.name].replace('\\n', '<br>')
            std_dict['sub'] = []
            std_list.append(std_dict)
        return std_list

    def _get_drbfm(self, usecase_id):
        drbfm_dict = dict()
        from app.ctrl.ctrl_ds_drbfm import CtrlDsDrbfm
        failures_tree, status = CtrlDsDrbfm().get(usecase_id)
        drbfm_dict['sec_id'] = usecase_id
        drbfm_dict['sec_type'] = 'DRBFM'
        drbfm_dict['status'] = status
        drbfm_dict['checklist'] = failures_tree
        drbfm_dict['sub'] = []
        return drbfm_dict

    def get_sections(self, doc_id):
        q = db.session.query(DSSection).filter(DSSection.doc_id == doc_id)
        q = q.order_by(DSSection.sec_type, DSSection.order_id)
        # q.statement
        df = pd.read_sql(q.statement,
                         con=db.session.bind,
                         # index_col=[DSSection.sec_type.name]
                         )
        sections = {}
        records = df.to_dict(orient="records")
        if records:
            all_tags = CtrlDocTag().get_all_tag()
        for sec in records:
            # 获取章节关联的TAG
            sec_id = sec.get(DSSection.sec_id.name)
            tag_list = self.get_tags(sec_id, all_tags)
            sec["tags"] = tag_list
            sec_type = sec.get(DSSection.sec_type.name)
            if sec_type in sections:
                sections[sec_type].append(sec)
            else:
                sections[sec_type] = [sec]
        return sections

    def get_tags(self, sec_id, all_tags=None):
        q = db.session.query(DSSectionTag.tag_id)
        q = q.filter(DSSectionTag.sec_id == sec_id)
        q = q.order_by(DSSectionTag.tag_id)
        tag_list = []
        for tag_rel in q:
            if all_tags:
                tag_id = tag_rel.tag_id
                tag_info = all_tags.get(tag_id)
                tag_list.append(tag_info)
            else:
                tag_list.append({DSSectionTag.tag_id.name: tag_rel[0]})
        return tag_list

    def get_section_type(self, sec_type='', orient='list'):
        q = db.session.query(DSSectionType)
        if sec_type:
            q = q.filter(DSSectionType.doc_type == sec_type)
        if orient.lower() == 'dict':
            sec_types = dict()
        else:
            sec_types = []
        for type_info in q:
            if orient.lower() == 'dict':
                sec_types[type_info.doc_type] = type_info.to_dict()
            else:
                sec_types.append(type_info.to_dict())
        return sec_types

    def get_section_by_doc_id(self, doc_id, sec_type='USERCASE'):
        q = db.session.query(DSSection)\
            .filter(DSSection.doc_id == doc_id, DSSection.sec_type == sec_type).first()
        if q:
            return q.sec_id, q.micro_ver
        return None, None

    def add_section(self, section):
        section = DSSection(**section)
        db.session.add(section)
        db.session.flush()
        sec_id = section.sec_id
        return sec_id

    def add_sec_tag_rel(self, sec_tag):
        sec_tag = DSSectionTag(**sec_tag)
        db.session.add(sec_tag)

    def update_sec(self, section, sec_id):
        section = DSSection(**section)
        db.session.query(DSSection).filter(DSSection.sec_id == sec_id).update(section)

    def delete_section(self, doc_id, commit_user):
        """
        # 删除一个文档下所有的章节
        :param doc_id:
        :return:
        """
        commit_list = []
        # db.session.query(DSSection).filter(DSSection.doc_id == doc_id).delete()
        q = db.session.query(DSSection).filter(DSSection.doc_id == doc_id)
        for sec_info in q:
            sec_id = sec_info.sec_id
            commit_list += self._delete(sec_id, commit_user, delete='ds_doc')
        return commit_list

    def delete_sec_tags(self, sec_id):
        """
        # 删除一个章节的tags
        :param sec_id:
        :return:
        """
        db.session.query(DSSectionTag).filter(DSSectionTag.sec_id == sec_id).delete()

    def delete_sequence_by_usecase_id(self, usecase_id):
        db.session.query(DSSection).filter(and_(DSSection.parent_sec_id == usecase_id,
                                                DSSection.sec_type == 'SEQUENCE')).delete()

    def delete(self, sec_id, commit_user):
        self._delete(sec_id, commit_user)
        db.session.commit()
        return None

    def _delete(self, sec_id, commit_user, delete='session'):
        """
        #删除一个usercase
        :param sec_id:
        :return:
        """
        from app.ctrl.ctrl_ds_rel_spec import CtrlDSRelSpec
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        from app.ctrl.ctrl_ds_drbfm import CtrlDsDrbfm
        commit_list = []
        update_time = self.get_current_time()
        commit_list += CtrlDSRelSpec().delete_by_sec_id(sec_id)
        # commit_list += CtrlDSScene().delete_by_sec_id(sec_id)
        # commit_list += CtrlDSConsider().delete_by_sec_id(sec_id)
        # commit_list += CtrlDsDrbfm().delete_by_sec_id(sec_id)
        commit_list += self.delete_usecase_sub(sec_id)
        if delete == 'session':
            self.commit_log(commit_list, commit_user, update_time)
        else:
            return commit_list

    def delete_usecase_sub(self, sec_id):
        """
        删除usecase或其他章节
        :param sec_id:
        :return:
        """
        commit_list = []
        sub_q = db.session.query(DSSection).filter(or_(DSSection.parent_sec_id == sec_id,
                                                   DSSection.sec_id == sec_id))
        old_data_list = []
        for sub in sub_q:
            old_data_list.append(sub.to_dict())
        for old_data in old_data_list:
            new_data = None
            if old_data.get('sec_type') == 'SEQUENCE':
                commit_list += self.delete_resource(old_data.get('sec_id'))
            commit_list += self.delete_sec_rel(old_data.get('sec_id'))
            commit_list += self.delete_func_rel(old_data.get('sec_id'))
            log_dict = self.common_add(self.db_object, new_data, old_data,
                                       self.col_list, self.key_col)
            commit_list.append(log_dict)
        return commit_list

    def delete_func_rel(self, sec_id):
        q = db.session.query(DSRelFun).filter(DSRelFun.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for func in q:
            old_data_list.append(func.to_dict())
        commit_list = self.add_list(DSRelFun, new_data_list, old_data_list,
                                    DSRelFun.gid, [])
        return commit_list

    def delete_sec_rel(self, sec_id):
        sr_q = db.session.query(DSSectionRel).filter(or_(DSSectionRel.sec_id == sec_id,
                                                         DSSectionRel.sec_rel_id == sec_id))
        old_data_list = []
        new_data_list = []
        for sr in sr_q:
            old_data_list.append(sr.to_dict())
        commit_list = self.add_list(DSSectionRel, new_data_list, old_data_list,
                                    DSSectionRel.gid, [])
        return commit_list

    def delete_resource(self, sec_id):
        col_list = ['content', 'operator', 'unit', 'value']
        rs_q = db.session.query(DSSectionResource).filter(DSSectionResource.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for rs in rs_q:
            old_data_list.append(rs.to_dict())
        commit_list = self.add_list(DSSectionResource, new_data_list, old_data_list,
                                    DSSectionResource.gid, col_list)
        return commit_list

    def usecase_add(self, data_json):
        update_time = self.get_current_time()
        commit_user = data_json.get('commit_user')
        doc_id = data_json.get('doc_id')
        if not doc_id:
            return False, '没有指定文档！'
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        public_sec_id = data_json.get('public_sec_id')
        public_usecase_content = data_json.get('public_usecase_content')
        public_micro_ver = data_json.get('public_micro_ver')
        public_usecase_content = json.dumps(public_usecase_content, ensure_ascii=False)
        try:
            old_pubuse_list, error = self.session_is_exist(public_sec_id)
            if error:
                return False, error
            new_pubuse = self.get_new_section(public_sec_id, doc_id, content=public_usecase_content,
                                              sec_type='COMMON')
            if old_pubuse_list:
                old_pubuse = old_pubuse_list[0]
                old_micro_ver = old_pubuse.get('micro_ver')
                flag, error = self.diff_ver(public_micro_ver, old_micro_ver)
                if not flag:
                    return False, error
            else:
                old_pubuse = None
            new_pubuse['micro_ver'] = self.update_version(public_micro_ver)
            pubuse_log = self.common_add(self.db_object, new_pubuse, old_pubuse, self.col_list, self.key_col)
            commit_list = []
            if pubuse_log:
                commit_list.append(pubuse_log)
            usecase_list = data_json.get('usecase_list')
            for data in usecase_list:
                sec_id = data.get("sec_id")
                content = data.get("content")
                str_content = json.dumps(content, ensure_ascii=False)
                micro_ver = data.get("micro_ver")
                new_data = self.get_new_section(sec_id, doc_id, content=str_content)
                old_data_list, error = self.session_is_exist(sec_id)
                if error:
                    return False, error
                if old_data_list:
                    old_data = old_data_list[0]
                    old_micro_ver = old_data.get('micro_ver')
                    flag, error = self.diff_ver(micro_ver, old_micro_ver)
                    if not flag:
                        return False, error
                else:
                    old_data = None
                new_data['micro_ver'] = self.update_version(micro_ver)
                log_dict = self.common_add(self.db_object, new_data, old_data,
                                           self.col_list, self.key_col)
                if log_dict:
                    commit_list.append(log_dict)
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

    def session_is_exist(self, sec_id):
        """
        判断章节是否存在
        :param sec_id:
        :return:
        """
        error = None
        session_data = self.get_old_data(self.db_object, self.key_col, sec_id)
        if sec_id and not session_data:
            error = '该章节已被删除！'
        return session_data, error

    def add_usercase(self, doc_id, usercase_con=None,
                     parent_sec_id=0, sec_type='USERCASE'):
        """
        USERCASE还未生成时新增一个usercase并返回sec_id,也可以指定类型添加别的章节
        :param doc_id:
        :param usercase_con:
        :param parent_sec_id:
        :param sec_type:
        :return:sec_id #章节id
        """
        usercase_sec = {"doc_id": doc_id, "parent_sec_id": parent_sec_id,
                        "sec_type": sec_type, "content": usercase_con}
        usercase_sec = self.init_version(usercase_sec, 'section')
        sec_id = self.add_section(usercase_sec)
        return sec_id

    def add(self, section_data, commit_user):
        return self.update_section(section_data, commit_user)

    def get_by_sec_id(self, sec_id):
        q = db.session.query(DSSection).filter(DSSection.sec_id == sec_id).first()
        if q:
            return q.to_dict()
        return dict()

    def get_usecase_sub(self, usecase_id, type):
        """
        :param usecase_id:
        :param type:
        :return:
        """
        q = db.session.query(DSSection).filter(and_(DSSection.parent_sec_id == usecase_id,
                                                DSSection.sec_type == type))
        sub_list = []
        for sub in q:
            sub_list.append(sub.to_dict())
        return sub_list

    def _to_sec_id_list(self, sec_list):
        id_list = []
        for sec in sec_list:
            id_list.append(sec.get(DSSection.sec_id.name))
        return id_list

    def delete_sequence(self, sec_id):
        db.session.query(DSSectionResource).filter(DSSectionResource.sec_id == sec_id).delete()
        db.session.query(DSSection).filter(DSSection.sec_id == sec_id).delete()

    def update(self, new_data_list, old_data_list):
        log_list = self.add_list(self.db_object, new_data_list, old_data_list, self.key_col, self.col_list)
        return log_list

    def update_section(self, section_data, commit_user):
        """ 新增或修改章节
        :param section_data:
        :return:
        """
        try:
            update_time = self.get_current_time()
            doc_id = int(section_data.get("doc_id"))
            from app.ctrl.ctrl_ds_doc import CtrlDsDoc
            doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
            if error:
                return False, error
            # micro_ver = section_data.get('micro_ver')
            contents = section_data.get("content")
            sec_type = section_data.get("sec_type")
            # csd_list = section_data.get("considers")
            commit_list = []
            if sec_type == 'SEQUENCE':
                commit_list += self.update_sequence(doc_id, contents, sec_type)
                # if csd_list:
                #     commit_list += CtrlDSConsider().update_content(parent_sec_id, csd_list)
            for content in contents:
                sec_id = content.get('sec_id')
                if sec_id:
                    sec_id = int(sec_id)
                micro_ver = content.get('micro_ver')
                str_content = content.get('content')
                str_content = json.dumps(str_content, ensure_ascii=False)
                rel_id_list = content.get('rel_id_list')
                resource_list = content.get('resource_list')
                activity_list = content.get('activity_list')
                if sec_type in ('BLOCK', 'CLASS', 'STD'):
                    old_sec_id, old_ver = self.get_section_by_doc_id(doc_id, sec_type)
                    if old_sec_id:  # 判断BLOCK/CLASS/STD是否已存在
                        sec_id = old_sec_id
                        micro_ver = old_ver
                old_data_list, error = self.session_is_exist(sec_id)
                if error:
                    return 0, error
                new_data = self.get_new_section(sec_id, doc_id, content=str_content,
                                                sec_type=sec_type)
                if old_data_list:
                    old_data = old_data_list[0]
                    old_micro_ver = old_data.get('micro_ver')
                    flag, error = self.diff_ver(micro_ver, old_micro_ver)
                    if not flag:
                        return 0, error
                else:
                    old_data = None
                new_data['micro_ver'] = self.update_version(micro_ver)
                if sec_type in ('BLOCK', 'CLASS', 'STD'):  # content只能有一个
                    log_dict = self.common_add(self.db_object, new_data, old_data,
                                               self.col_list, self.key_col)
                    if log_dict:
                        commit_list.append(log_dict)
                else:
                    # if not rel_id_list:
                    #     return 0, '没有指定关联的USECASE！'
                    log_dict = self.common_add(self.db_object, new_data, old_data,
                                               self.col_list, self.key_col)
                    if log_dict:
                        sec_id = log_dict.get('key_id')
                        commit_list.append(log_dict)
                    commit_list += self.update_sec_rel(sec_id, rel_id_list)  # 添加关联usecase信息
                    if sec_type == "SEQUENCE":
                        activity_log, error = self.add_activity_list(activity_list, sec_id, doc_id)
                        if error:
                            return 0, error
                        commit_list += activity_log
                        if resource_list:
                            commit_list += self.add_sec_resource(sec_id, resource_list)
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, ''
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def update_sec_rel(self, sec_id, rel_id_list):
        old_rel_list = self.get_old_data(DSSectionRel, DSSectionRel.sec_id, sec_id)
        new_rel_list = []
        for rel_id in rel_id_list:
            new_rel = {'sec_id': sec_id, 'sec_rel_id': rel_id}
            for old_rel in old_rel_list:
                if sec_id == old_rel['sec_id'] and rel_id == old_rel['sec_rel_id']:
                    new_rel['gid'] = old_rel['gid']
            new_rel_list.append(new_rel)
        commit_list = self.add_list(DSSectionRel, new_rel_list, old_rel_list, DSSectionRel.gid, [])
        return commit_list

    def add_activity_list(self, activity_list, parent_sec_id, doc_id):
        """
        更新Activity图
        :param activity_list:
        :param parent_sec_id:
        :return:
        """
        commit_list = []
        if not parent_sec_id:
            return commit_list, '没有指定SEQUENCE！'
        commit_list += self.update_activity(parent_sec_id, activity_list, sec_type="Activity")
        for activity in activity_list:
            sec_id = activity.get('sec_id')
            micro_ver = activity.get('micro_ver')
            sec_type = activity.get('sec_type')
            content = activity.get('content')
            str_content = json.dumps(content, ensure_ascii=False)
            old_data_list, error = self.session_is_exist(sec_id)
            if error:
                return commit_list, error
            new_data = self.get_new_section(sec_id, doc_id, content=str_content,
                                            parent_sec_id=parent_sec_id,
                                            sec_type=sec_type)
            if old_data_list:
                old_data = old_data_list[0]
                old_micro_ver = old_data.get('micro_ver')
                flag, error = self.diff_ver(micro_ver, old_micro_ver)
                if not flag:
                    return 0, error
            else:
                old_data = None
            new_data['micro_ver'] = self.update_version(micro_ver)
            log_dict = self.common_add(self.db_object, new_data, old_data,
                                       self.col_list, self.key_col)
            if log_dict:
                commit_list.append(log_dict)
        return commit_list, None

    def update_activity(self, parent_sec_id, activity_list, sec_type):
        """
        新旧activity对比，挑出要删除的activity进行删除
        :param parent_sec_id:
        :param sequence_list:
        :param sec_type:
        :return:
        """
        old_activity_list = self.get_old_data(DSSection, [DSSection.parent_sec_id, DSSection.sec_type],
                                              {'parent_sec_id': parent_sec_id, 'sec_type': sec_type})
        old_list = self._to_sec_id_list(old_activity_list)
        new_list = self._to_sec_id_list(activity_list)
        commit_list = []
        for sec_id in old_list:
            if sec_id not in new_list:
                commit_list += self.delete_usecase_sub(sec_id)
        return commit_list

    def get_activity_list(self, sequence_id, sec_type='Activity'):
        """
        获取Activity图
        :param sequence_id:
        :return:
        """
        q = db.session.query(DSSection).filter(and_(DSSection.parent_sec_id == sequence_id,
                                                    DSSection.sec_type == sec_type))
        activity_list = []
        for section in q:
            content_dict = dict()
            content_dict[DSSection.sec_id.name] = section.sec_id
            content_dict[DSSection.sec_type.name] = section.sec_type
            content_dict[DSSection.micro_ver.name] = section.micro_ver
            content_dict[DSSection.content.name] = section.content
            activity_list.append(content_dict)
        return activity_list

    def update_sequence(self, doc_id, sequence_list, sec_type):
        """
        新旧时序图对比，挑出要删除的时序图进行删除
        :param parent_sec_id:
        :param sequence_list:
        :param sec_type:
        :return:
        """
        seq_list = self.get_old_data(DSSection, [DSSection.doc_id, DSSection.sec_type],
                                     {'doc_id': doc_id, 'sec_type': sec_type})
        old_seq_id_list = self._to_sec_id_list(seq_list)
        new_seq_id_list = self._to_sec_id_list(sequence_list)
        commit_list = []
        for seq_id in old_seq_id_list:
            if seq_id not in new_seq_id_list:
                commit_list += self.delete_usecase_sub(seq_id)
        return commit_list

    def get_new_section(self, sec_id, doc_id, content=None, parent_sec_id=0, sec_type='USERCASE'):
        new_section = {DSSection.sec_id.name: sec_id,
                       DSSection.doc_id.name: doc_id,
                       DSSection.parent_sec_id.name: parent_sec_id,
                       DSSection.sec_type.name: sec_type,
                       DSSection.content.name: content,
                       DSSection.ver.name: None,
                       DSSection.order_id.name: None,
                       DSSection.required.name: None}
        return new_section

    def update_ver(self, sec_id):
        """
        更新章节版本
        :param sec_id:
        :return:
        """
        q = db.session.query(DSSection).filter(DSSection.sec_id == sec_id).first()
        old_section = q.to_dict()
        new_section = copy.deepcopy(old_section)
        new_section['micro_ver'] = self.update_version(old_section['micro_ver'])
        log_dict = self.common_add(self.db_object, new_section, old_section,
                                   self.col_list, self.key_col, diff_required=False)
        return log_dict

    def add_sec_check_lit(self, doc_id, sec_id, checklist):
        from app.ctrl.ctrl_ds_checklist_item import CtrlDSCheckListItem
        check_dict = {"doc_id": doc_id, "sec_id": sec_id, "checklist": checklist}
        sec_id, error = CtrlDSCheckListItem().add(check_dict)
        return sec_id, error

    def add_sec_resource(self, sec_id, resourcelist):
        q = db.session.query(DSSectionResource).filter(DSSectionResource.sec_id == sec_id)
        old_data_list = []
        for resource in q:
            old_data_list.append(resource.to_dict())
        new_data_list = []
        for resource in resourcelist:
            value = resource.get('value')
            if type(value) == str:
                value = None
            sec_res = {'sec_id': sec_id,
                       'gid': resource.get('gid'),
                       'resource_id': resource.get('resource_id'),
                       'content': resource.get('val'),
                       'operator': resource.get('operator'),
                       'unit': resource.get('unit'),
                       'value': value}
            new_data_list.append(sec_res)
        col_list = ['content', 'operator', 'unit', 'value']
        resource_log = self.add_list(DSSectionResource, new_data_list, old_data_list,
                                     DSSectionResource.gid, col_list)
        return resource_log
        # db.session.add(DSSectionResource(**sec_res))

    def get_sec_rel_list(self, sec_id):
        q = db.session.query(DSSectionRel).filter(DSSectionRel.sec_id == sec_id)
        rel_id_list = []
        for sec_rel in q:
            rel_id_list.append(sec_rel.sec_rel_id)
        return rel_id_list

    def get(self, doc_id, sec_type=None, condition=None):
        q = db.session.query(DSSection)
        q = q.filter(DSSection.doc_id == doc_id)
        q = q.filter(DSSection.sec_type == sec_type)
        q = q.order_by(DSSection.sec_id)
        sec_dict = dict()
        content_list = []
        for section in q:
            resource_list = []
            activity_list = []
            content_dict = dict()
            content_dict[DSSection.sec_id.name] = section.sec_id
            content_dict[DSSection.micro_ver.name] = section.micro_ver
            content = section.content
            content_dict[DSSection.content.name] = content
            content_dict['rel_id_list'] = self.get_sec_rel_list(section.sec_id)
            if sec_type == 'SEQUENCE':
                # check_list = CDL().get(section.sec_id)
                activity_list = self.get_activity_list(section.sec_id)
                resource_list = CtrlDSResource().get_resource_by_sec_id(section.sec_id)
            content_dict['resource_list'] = resource_list
            content_dict['activity_list'] = activity_list
            content_list.append(content_dict)
        sec_dict['content'] = content_list
        # sec_dict['considers'] = CtrlDSConsider().get(sec_id, 'ALL')
        if sec_dict.get("content"):
            sec_dict.update({'doc_id': q[0].doc_id,
                             'sec_type': q[0].sec_type})
            return sec_dict, None
        return None, None

    def get_knowledge_doc(self, sec_id):
        """
        取关联的技术文档
        :param sec_id:
        :return:
        """
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        from app.ctrl.ctrl_project import CtrlProject
        from app.ctrl.ctrl_doc import CtrlDoc
        scene_tag_list = CtrlDSScene().get_scene_tag(sec_id)  # 场景
        proj_tag_list = CtrlProject().get_proj_tags(sec_id)  # Project
        inter_tags = set(scene_tag_list).intersection(proj_tag_list)
        knowledge_docs, bug_list = CtrlDoc().get_by_tags(inter_tags)
        result = {'knowledge_docs': knowledge_docs,
                  'bug_list': bug_list}
        return result


class CtrlDSConsider(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSDocConsider.gid
        self.db_object = DSDocConsider
        self.col_list = [DSDocConsider.consider_content.name]

    def create_considers(self, sec_id):
        """
        :param sec_id:
        :return:
        """
        scene_csd_list = self._get_scene_considers(sec_id)  # 场景
        # model_csd_list = self._get_model_considers(sec_id)  # Model
        proj_csd_list = self._get_project_considers(sec_id)  # Project
        inter_considers = set(scene_csd_list).intersection(proj_csd_list)
        # inter_considers = inter_considers.intersection(proj_csd_list)
        old_considers = self.get_old_data(self.db_object, DSDocConsider.sec_id, sec_id)
        new_conciders = []
        for consider_id in inter_considers:
            csd_info = {
                        DSDocConsider.gid.name: None,
                        DSDocConsider.sec_id.name: sec_id,
                        DSDocConsider.consider_id.name: consider_id,
                        DSDocConsider.checked.name: None,
                        DSDocConsider.consider_content.name: None}
            for old in old_considers:
                if consider_id == old.get('consider_id'):
                    csd_info[DSDocConsider.gid.name] = old.get(DSDocConsider.gid.name)
            new_conciders.append(csd_info)
        log_list = self.add_list(self.db_object, new_conciders, old_considers, self.key_col, [])
        return log_list

    def get(self, sec_id, csd_range='ALL'):
        if not csd_range or csd_range == 'ALL':
            consider_list = self.get_considers(sec_id, checked=None)
        else:
            consider_list = self.get_considers(sec_id, checked=True)
        # if consider_list:
            # return {"sec_id": sec_id,  # USERCASE，0：USERCASE还未生成
            #         "sec_type": "CONSIDERS",
            #         "considers": consider_list}
        return consider_list

    def get_considers(self, sec_id, checked=None):
        q = (db.session.query(DSDocConsider.gid,
                              DSDocConsider.sec_id,
                              DSDocConsider.consider_id,
                              DSDocConsider.consider_content,
                              DSDocConsider.checked,
                              Consider.consider_name)
             .filter(DSDocConsider.sec_id == sec_id,
                     DSDocConsider.consider_id == Consider.consider_id)
             )
        if checked:
            q = q.filter(DSDocConsider.checked==True)
        q = q.order_by(DSDocConsider.consider_id)
        consider_list = []
        col_names = [DSDocConsider.gid.name,
                     DSDocConsider.sec_id.name,
                     DSDocConsider.consider_id.name,
                     DSDocConsider.consider_content.name,
                     DSDocConsider.checked.name,
                     Consider.consider_name.name]
        for row in q:
            csd_info = dict(zip(col_names, row))
            if not csd_info.get(DSDocConsider.consider_content.name):
                csd_info[DSDocConsider.consider_content.name] = ''
            consider_list.append(csd_info)
        return consider_list

    def get_db_for_journal(self, sec_id):
        """
        :param sec_id:
        :return: DSDocConsider object list
        """
        q = (db.session.query(DSDocConsider)
             .filter(DSDocConsider.sec_id == sec_id)
             ).order_by(DSDocConsider.gid)
        return q.all()

    def update_content(self, sec_id, csd_list):
        # for csd in csd_list:
        #     csd[DSDocConsider.consider_content.name] = csd["consider_val"]
        old_condsiders = self.get_old_data(self.db_object, DSDocConsider.sec_id, sec_id)
        new_condsiders = []
        for csd in csd_list:
            csd_info = dict()
            csd_info[DSDocConsider.gid.name] = csd.get(DSDocConsider.gid.name)
            csd_info[DSDocConsider.sec_id.name] = csd.get(DSDocConsider.sec_id.name)
            csd_info[DSDocConsider.consider_id.name] = csd.get(DSDocConsider.consider_id.name)
            csd_info[DSDocConsider.consider_content.name] = csd.get(DSDocConsider.consider_content.name)
            csd_info[DSDocConsider.checked.name] = csd.get(DSDocConsider.checked.name)
            new_condsiders.append(csd_info)
        log_list = self.add_list(self.db_object, new_condsiders, old_condsiders, self.key_col, self.col_list)
        return log_list

    def update_condsiders(self, data):
        try:
            sec_id = data.get("sec_id")
            if not sec_id:
                return True, 'UserCase ID未指定!'
            considers = data.get("considers")
            update_range = data.get("update_range")
            if update_range == 'CHECKED':  # 更新check项
                update_cols = [DSDocConsider.checked.name]
            elif update_range == 'CONTENT':  # # 更新内容项
                update_cols = [DSDocConsider.consider_content.name]
            else:
                return False, '更新项(%s)指定错误' % update_range
            self._update_condsiders(sec_id, considers,
                                    update_cols=update_cols)
            db.session.commit()
            return True, 'OK'
        except Exception as e:
            return False, "服务异常！请联系管理员！"

    def _update_condsiders(self, sec_id, considers,
                           update_cols=[DSDocConsider.checked.name]):
        old_condsiders = self.get_considers(sec_id)
        old_csd_dict = self.considers_to_dict(old_condsiders)
        for csd in considers:
            csd[DSDocConsider.sec_id.name] = sec_id
            self.update(csd, update_cols)
            old_csd_dict.pop(csd.get(DSDocConsider.consider_id.name))
        # 清空其他的
        for old_csd in old_csd_dict.values():
            for col in update_cols:
                old_csd[col] = None
                self.update(old_csd, update_cols)

    def delete_by_sec_id(self, sec_id):
        """
        删除usecase的考虑点
        :param doc_id:
        :param sec_id:
        :return:
        """
        consider_q = db.session.query(DSDocConsider).filter(DSDocConsider.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for consider in consider_q:
            old_data_list.append(consider.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def update(self, consider_info, update_cols=[DSDocConsider.checked.name]):
        sec_id = consider_info.get(DSDocConsider.sec_id.name)
        consider_id = consider_info.get(DSDocConsider.consider_id.name)
        new_data = dict()
        for col in update_cols:
            new_data[col] = consider_info.get(col)
        db.session.query(DSDocConsider).filter(
            DSDocConsider.sec_id == sec_id,
            DSDocConsider.consider_id == consider_id).update(new_data)

    def add(self, consider_info):
        csd_obj = DSDocConsider(**consider_info)
        db.session.add(csd_obj)

    def delete(self, sec_id, consider_id=None):
        if consider_id:
            db.session.query(DSDocConsider).filter(
                DSDocConsider.sec_id == sec_id,
                DSDocConsider.consider_id == consider_id).delete()
        else:
            db.session.query(DSDocConsider).filter(
                DSDocConsider.sec_id == sec_id).delete()

    def considers_to_dict(self, condsiders):
        consider_dict = dict()
        for consider in condsiders:
            key = consider.get(DSDocConsider.consider_id.name)
            consider_dict[key] = consider
        return consider_dict

    def _get_scene_considers(self, sec_id):
        """获取场景关联的考虑点
        :param sec_id: UserCase ID
        :return:
        """
        sqlcmd = """
        SELECT DISTINCT consider_id, consider_name
          FROM ds.ds_rel_scene as a
          left join ds.ds_scene_tag_rel as b
          on a.scene_id = b.scene_id
          left join public.doc_tags as c
          on b.tag_id = c.tag_id
          inner join public.consider as d
          on c.doc_id = d.doc_id
          where a.sec_id = :sec_id
          ORDER BY consider_id
        """
        consider_list = []
        s = db.session
        query = s.execute(sqlcmd, {'sec_id': sec_id})
        rows = query.fetchall()
        for row in rows:
            consider_list.append(row[0])
        return consider_list

    def _get_model_considers(self, sec_id):
        """获取模块关联的考虑点
        :param sec_id: UserCase ID
        :return:
        """
        sqlcmd = """
        SELECT DISTINCT consider_id
          FROM ds.ds_section as a
          left join ds.ds_doc as b
          on a.doc_id = b.doc_id
          left join ds.ds_model_tag_rel as c
          on b.model_id = c.model_id
          left join public.doc_tags as d
          on c.tag_id = d.tag_id
          inner join public.consider as e
          on d.doc_id = e.doc_id
          where a.sec_id = :sec_id
          ORDER BY consider_id
        """
        consider_list = []
        s = db.session
        query = s.execute(sqlcmd, {'sec_id': sec_id})
        rows = query.fetchall()
        for row in rows:
            consider_list.append(row[0])
        return consider_list

    def _get_project_considers(self, sec_id):
        """获取项目关联的考虑点
        :param sec_id: UserCase ID
        :return:
        """
        sqlcmd = """
        SELECT DISTINCT consider_id, consider_name
          FROM ds.ds_section as a
          left join ds.ds_doc as b
          on a.doc_id = b.doc_id
          left join ds.project_tags as c
          on b.proj_id = c.proj_id
          left join public.doc_tags as d
          on c.tag_id = d.tag_id
          inner join public.consider as e
          on d.doc_id = e.doc_id
          where a.sec_id = :sec_id
          ORDER BY consider_id
        """
        consider_list = []
        s = db.session
        query = s.execute(sqlcmd, {'sec_id': sec_id})
        rows = query.fetchall()
        for row in rows:
            consider_list.append(row[0])
        return consider_list


class CtrlDSResource(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def get_resource(self):
        resource_list = []
        q = db.session.query(DsResource).order_by(DsResource.resource_id)
        # print(q.statement)
        for resource in q:
            resource_list.append(resource.to_dict())
        return resource_list

    def get_resource_by_sec_id(self, sec_id):
        resource_list = []
        q = db.session.query(DSSectionResource.gid, DSSectionResource.resource_id, DsResource.rsc_name,
                             DSSectionResource.content,
                             DSSectionResource.operator, DSSectionResource.unit,
                             DSSectionResource.value, DsResource.type)\
            .outerjoin(DsResource, DSSectionResource.resource_id == DsResource.resource_id)\
            .filter(DSSectionResource.sec_id == sec_id)\
            .order_by(DSSectionResource.resource_id).all()
        for sec_res in q:
            resource_dict = dict()
            resource_dict['gid'] = sec_res[0]
            resource_dict['resource_id'] = sec_res[1]
            resource_dict['rsc_name'] = sec_res[2]
            resource_dict['val'] = sec_res[3]
            resource_dict['operator'] = sec_res[4]
            resource_dict['unit'] = sec_res[5]
            resource_dict['value'] = sec_res[6]
            resource_dict['type'] = sec_res[7]
            if resource_dict['type'] == "text":
                resource_dict['value'] = sec_res[3]
            resource_list.append(resource_dict)
        return resource_list

    def get_db_for_journal(self, sec_id):
        resources = (db.session.query(DSSectionResource).
                     filter(DSSectionResource.sec_id == sec_id).all())
        return resources
