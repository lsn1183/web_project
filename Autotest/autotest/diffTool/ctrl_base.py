# -*- coding: UTF-8 -*-
import time
import datetime
from django.db import transaction
from django.forms.models import model_to_dict
from diffTool.ctrl_diff import CtrlDiff


class CtrlBase(object):

    def __init__(self):
        self.major_ver = 0
        self.minor_ver = 1
        self.micro_ver = 1

    def init_version(self, datainfo, type):
        if type == 'doc':
            datainfo['major_ver'] = self.major_ver
            datainfo['minor_ver'] = self.minor_ver
            datainfo['micro_ver'] = self.micro_ver
        elif type == 'section':
            datainfo['micro_ver'] = self.micro_ver
        return datainfo

    def update_version(self, ver):
        if ver:
            ver += 1
        else:
            ver = 1
        return ver

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def time_to_str(self, date_time):
        if type(date_time) in (datetime.datetime, datetime.time):
            date_time = date_time.strftime("%Y-%m-%d %H:%M:%S")
        return date_time

    def diff_ver(self, new_ver, old_ver):
        # return True, ''
        if new_ver == old_ver:
            return True, ''
        else:
            error = '已有人更新，请重新刷新页面！'
            return False, error

    def add_list(self, db_object, data_list, old_data_list, key_col, col_list):
        """
        :param db_object: model
        :param data_list: 新数据list
        :param old_data_list: 旧数据list
        :param key_col: 主键id('id')
        :param col_list: 比较的字段list
        :return:
        """
        diff_obj = CtrlDiff()
        match_list = diff_obj.match_list(old_data_list, data_list, key_col)
        log_list = []
        for match_dict in match_list:
            new_data = match_dict.get("new_data")
            old_data = match_dict.get("old_data")
            log_dict = self.common_add(db_object, new_data, old_data, col_list, key_col)
            if log_dict:
                log_list.append(log_dict)
        return log_list

    def common_add(self, db_object, new_data, old_data, col_list, key_col, diff_required=True):
        log_dict = dict()
        log_dict['table_name'] = db_object._meta.db_table
        diff_obj = CtrlDiff()
        if diff_required:
            action = diff_obj.diff_col(col_list, old_data, new_data)
        else:
            action = 'change'
        if action == 'same':
            return None
        elif action == 'add':
            if key_col in new_data:
                if not new_data[key_col]:
                    new_data.pop(key_col)
            new_obj = db_object.objects.create(**new_data)
            obj_dict = model_to_dict(new_obj)
            log_dict['action'] = action
            log_dict['key_id'] = obj_dict.get(key_col)
            log_dict['data'] = new_data
        elif action == 'change':
            key_id = new_data.get(key_col)
            db_object.objects.filter(pk=key_id).update(**new_data)
            log_dict['action'] = action
            log_dict['key_id'] = key_id
            log_dict['data'] = new_data
        elif action == 'delete':
            key_id = old_data.get(key_col)
            db_object.objects.filter(pk=key_id).delete()
            log_dict['action'] = action
            log_dict['key_id'] = key_id
            log_dict['data'] = old_data
        return log_dict

    def case_common_add(self, db_object, new_data, old_data, col_list, key_col):
        """
        testcase的diff更新
        :param db_object:
        :param new_data:
        :param old_data:
        :param col_list:
        :param key_col:
        :return:
        """
        log_dict = dict()
        diff_obj = CtrlDiff()
        action, change_col_list = diff_obj.diff_case_change(col_list, old_data, new_data)
        if action == 'same':
            return None
        with transaction.atomic():
            if action == 'add':
                if key_col in new_data:
                    if not new_data[key_col]:
                        new_data.pop(key_col)
                new_obj = db_object.objects.create(**new_data)
                obj_dict = model_to_dict(new_obj)
                log_dict['action'] = action
                log_dict['key_id'] = obj_dict.get(key_col)
                log_dict['data'] = obj_dict
            elif action == 'change':
                key_id = new_data.get(key_col)
                update_dict = dict()
                for col in change_col_list:
                    update_dict[col] = new_data.get(col)
                db_object.objects.filter(pk=key_id).update(**update_dict)
                log_dict['action'] = action
                log_dict['key_id'] = key_id
                log_dict['change_col_list'] = change_col_list
                log_dict['data'] = new_data
            elif action == 'delete':
                key_id = old_data.get(key_col)
                db_object.objects.filter(pk=key_id).delete()
                log_dict['action'] = action
                log_dict['key_id'] = key_id
                log_dict['data'] = old_data
        return log_dict

    def commit_log(self, commit_list, commit_user, update_time):
        """
        把变更履历存进数据库
        :param commit_list:
        :param commit_user:
        :param update_time:
        :return: True:有变更/False:无变更
        """
        if commit_list:
            commit_log = dict()
            commit_log['commit_user'] = commit_user
            commit_log['update_time'] = update_time
            commit_log['commit_list'] = commit_list
            # from app.ctrl.ctrl_journal import CtrlJournal
            # CtrlJournal().add_journals(commit_log)

    def get_old_data(self, db_object, key_id):
        if type(key_id) == dict:
            q = db_object.objects.filter(**key_id)
        else:
            q = db_object.objects.filter(pk=key_id)
        data_list = []
        for data in q:
            data_list.append(model_to_dict(data))
        return data_list

    def get_verbose_name(self, db_object, exclude_fields):
        """
        获取model的备注信息
        :param db_object:
        :param exclude_fields:
        :return:
        """
        verbose_name_dict = dict()
        params = [f for f in db_object._meta.fields if f.name not in exclude_fields]
        for msg in params:
            verbose_name_dict[msg.name] = msg.verbose_name
        verbose_name_dict['case_keyword_list'] = '关键字'
        verbose_name_dict['case_dest_list'] = '仕向地'
        verbose_name_dict['case_step_list'] = '测试步骤'
        verbose_name_dict['case_field_value_list'] = '自定义字段的值'
        return verbose_name_dict





