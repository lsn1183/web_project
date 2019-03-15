# -*- coding: UTF-8 -*-
from app.db import db
from app.db.ds_doc_checklist_item import DSChecklistItem as CLI
from app.ctrl.ctrl_ds_section import CtrlDSSection
from app.db.ds_failure import DSFailure


class CtrlDSCheckListItem(object):
    def add(self, data_dict):
        doc_id = int(data_dict.get(CLI.doc_id.name))
        if not doc_id:
            return False, '未指定文档ID!'
        sec_id = data_dict.get(CLI.sec_id.name)
        if not sec_id:
            sec_id = CtrlDSSection().add_usercase(doc_id)
            if not sec_id:
                return 0, 'UserCase生成失败!'
        else:
            self.delete(sec_id)
        checklist = data_dict.get("checklist")
        if checklist:
            for cl in checklist:
                check = dict()
                check[CLI.doc_id.name] = doc_id
                check[CLI.sec_id.name] = int(sec_id)
                check[CLI.item_id.name] = cl.get('item_id')
                check[CLI.content.name] = cl.get('content')
                # checks.append(CLI(**check))
                db.session.add(CLI(**check))
        try:
            db.session.commit()
            return sec_id, 'OK'
        except Exception as e:
            db.session.rollback()
            return 0, str(e)

    def delete(self, sec_id):
        if sec_id:
            db.session.query(CLI).filter(CLI.sec_id == sec_id).delete()

    def get(self, sec_id, sec_type=None):
        q = db.session.query(CLI.doc_id, CLI.item_id, CLI.content, DSFailure.failure)\
            .outerjoin(DSFailure, CLI.item_id == DSFailure.item_id)\
            .filter(CLI.sec_id == sec_id).all()
        check_list = dict()
        if len(q):
            check_list = {'doc_id': q[0][0], 'sec_id': sec_id, 'sec_type': 'CHECKLIST'}
            checklist = []
            for check in q:
                check_dict = dict()
                check_dict['item_id'] = check[1]
                check_dict['content'] = check[2]
                check_dict['failure'] = check[3]
                checklist.append(check_dict)
            check_list['checklist'] = checklist
        return check_list

