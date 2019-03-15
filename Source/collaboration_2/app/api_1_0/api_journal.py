# -*- coding: UTF-8 -*-'
from flask import request
from flask import current_app
from flask_restful import Resource
from token_manage import auth
from app.ctrl.ctrl_journal import CtrlDSDocJournal


class ApiJournal(Resource):
    @auth.login_required
    def get(self, key_id, left_version='', right_version='', log_type='DSDOC'):
        """
        :param key_id: 如doc_id
        :param log_type: 类别(DSDOC:设计文档)
        :param left_version: 左边版本号(Old)
        :param right_version: 右边版本号(New)
        :return:
        """
        result = {"result": "NG"}
        if log_type == 'DSDOC':
            ds_joournal = CtrlDSDocJournal()
            left_doc, right_doc, msg = ds_joournal.get_journal_diff(key_id,
                                                                    left_version,
                                                                    right_version)
            if left_doc or right_doc:
                result["content"] = {"left": left_doc,
                                     "right": right_doc,
                                     }
                result["result"] = "OK"
            else:
                result["message"] = msg
        return result

    def post(self):
        """
        获取组的信息
        :param group_name:
        :return:
        """
        result = {"result": "NG"}
        return result


class ApiJournalVersion(Resource):
    @auth.login_required
    def get(self, key_id, log_type='DSDOC'):
        """
        :param key_id: 如doc_id
        :param log_type: 类别(DSDOC:设计文档)
        :param left_version: 左边版本号(Old)
        :param right_version: 右边版本号(New)
        :return:
        """
        result = {"result": "NG"}
        if log_type == 'DSDOC':
            ds_joournal = CtrlDSDocJournal()
            version_list = ds_joournal.get_journalized_versions(key_id)
            result["content"] = version_list
            result["result"] = "OK"
        return result
