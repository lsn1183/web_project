# -*- coding: UTF-8 -*-
"""
Created on 2017-10-27

@author: hc
"""
import copy
import re

class ArlDiff(object):
    def __init__(self, key_col, id_col, col_list, ignore_col_list=None):
        self._key_col = key_col
        self._id_col = id_col
        self._col_list = col_list
        self._ignore_col = dict()
        if ignore_col_list:
            for col in ignore_col_list:
                self._ignore_col[col] = None

    def diff_list(self, old_datas, new_datas):
        """
        :param from_datas:
        :param to_datas:
        :return:
        """
        if not old_datas:
            old_datas = []
        if not new_datas:
            new_datas = []
        diff_dict = dict()
        # 先比较主键相同的
        compared = dict()
        for i, new_data in enumerate(new_datas, 0):
            diff_result = self._compare_by_id(new_data, old_datas, self._key_col, compared)
            if diff_result:
                diff_dict[i] = diff_result
        # 再比较id相同的
        for i, new_data in enumerate(new_datas, 0):
            if i in diff_dict:
                continue
            diff_result = self._compare_by_id(new_data, old_datas, self._id_col, compared)
            if diff_result:
                diff_dict[i] = diff_result
            else:
                diff_result = self.diff(None, new_data)
                diff_dict[i] = diff_result
        diff_list = []
        for i in diff_dict.keys():
            diff_list.append(diff_dict.get(i))
        for i, old_data in enumerate(old_datas, 0):
            if i not in compared:
                diff_result = self.diff(old_data, None)
                diff_list.append(diff_result)
        return diff_list

    def match_list(self, old_datas, new_datas):
        """
        :param from_datas:
        :param to_datas:
        :return:
        """
        if not old_datas:
            old_datas = []
        if not new_datas:
            new_datas = []
        match_list = []
        # 先比较主键相同的
        new_compared, old_compared = dict(), dict()
        for i, new_data in enumerate(new_datas, 0):
            old_data = self._match_by_id(new_data, old_datas, self._key_col, old_compared)
            if old_data:
                match_list.append({"new_data": new_data, "old_data": old_data})
                new_compared[i] = None
        # 再比较id相同的
        for i, new_data in enumerate(new_datas, 0):
            if i in new_compared:
                continue
            match_list.append({"new_data": new_data, "old_data": None})
            # old_data = self._match_by_id(new_data, old_datas, self._id_col, old_compared)
            # if old_data:
            #     match_list.append({"new_data": new_data, "old_data": old_data})
            # else:
            #     match_list.append({"new_data": new_data, "old_data": None})
        for i, old_data in enumerate(old_datas, 0):
            if i not in old_compared:
                match_list.append({"new_data": None, "old_data": old_data})
        return match_list

    def _match_by_id(self, new_data, old_datas, id_col, compared):
        new_id = new_data.get(id_col)
        if new_id:
            for j, old_data in enumerate(old_datas, 0):
                if j in compared:
                    continue
                if new_id == old_data.get(id_col):
                    compared[j] = None
                    return old_data
        return None

    def _compare_by_id(self, new_data, old_datas, id_col, compared):
        key_id = new_data.get(self._key_col)
        diff_result = None
        if key_id:
            for j, old_data in enumerate(old_datas, 0):
                if j not in compared:
                    continue
                if key_id == old_data.get(id_col):
                    diff_result = self.diff(old_data, new_data)
                    compared[j] = None
                    break
        return diff_result

    def diff(self, old_data, new_data):
        """
        :param old_data:
        :param new_data:
        :return: "delete"、"new"、“update"、"same"
        """
        diff_result = {"action": "same", "data": new_data,
                       "col_change_list": [], "model_list": [], "point_dict": {}}
        col_change_list, old_model_list, new_model_list = [], [], []
        if old_data:
            key_id = old_data.get(self._key_col)
            diff_result[self._key_col] = key_id
            old_model_list = old_data.get("model_list")
            old_point_dict = old_data.get("point_dict")
            if not new_data:
                diff_result["action"] = "delete"
                change_flag, model_list_changes = self._diff_model_list(old_model_list, [])
                diff_result["col_change_list"] = col_change_list
                diff_result["model_list"] = model_list_changes
                diff_result["point_list"] = {}
                return diff_result
        elif new_data:
            diff_result["action"] = "add"
            new_model_list = new_data.get("model_list")
            new_point_dict = new_data.get("point_dict")
            change_flag, model_change_list = self._diff_model_list([], new_model_list)
            change_flag1, point_dict = self.diff_point(None, new_point_dict)
            diff_result["col_change_list"] = col_change_list
            diff_result["model_list"] = model_change_list
            diff_result["point_dict"] = point_dict
            return diff_result
        else:
            return {}
        col_change_list = self._diff_col_list(old_data, new_data)
        new_model_list = new_data.get("model_list")
        new_point_dict = new_data.get("point_dict")
        change_flag, model_change_list = self._diff_model_list(old_model_list, new_model_list)
        change_flag1, point_dict = self.diff_point(old_point_dict, new_point_dict)
        if col_change_list or change_flag or change_flag1:
            diff_result["action"] = "change"
        else:
            diff_result["action"] = "same"
        diff_result["col_change_list"] = col_change_list
        diff_result["model_list"] = model_change_list
        diff_result["point_dict"] = point_dict
        return diff_result

    def _diff_col_list(self, old_data, new_data):
        if not old_data:
            old_data = dict()
        if not new_data:
            new_data = dict()
        col_change_list = []
        for i, col_name in enumerate(self._col_list, 0):
            if col_name == self._key_col:  # 主键不比较
                continue
            if col_name in self._ignore_col:
                continue
            new_val = new_data.get(col_name)
            if new_val is None:
                new_val = ''
            old_val = old_data.get(col_name)
            if old_val is None:
                old_val = ''
            if new_val != old_val:
                try:
                    if unicode(new_val) != unicode(old_val):
                        col_change_list.append(col_name)
                except:
                    col_change_list.append(col_name)
        return col_change_list

    def _diff_model_list(self, old_model_list=None, new_model_list=None):
        change_flag = False
        new_dict, old_dict = dict(), dict()
        if not old_model_list:
            old_model_list = []
        if not new_model_list:
            new_model_list = []
        for old_model_dict in old_model_list:
            model_id = old_model_dict.get("model_id")
            old_dict[model_id] = old_model_dict
        for new_model_dict in new_model_list:
            model_id = new_model_dict.get("model_id")
            new_dict[model_id] = new_model_dict
        model_id_set = set(old_dict.keys() + new_dict.keys())
        model_change_list = []
        for model_id in sorted(model_id_set):
            diff_result = dict()
            new_model_data = new_dict.get(model_id)
            old_model_data = old_dict.get(model_id)
            if old_model_data:
                if not new_model_data:
                    diff_result["action"] = "delete"
                    diff_result["data"] = old_model_data
                    model_change_list.append(diff_result)
                    change_flag = True
                else:
                    old_val = old_model_data.get("val")
                    new_val = new_model_data.get("val")
                    if old_val != new_val:
                        diff_result["action"] = "change"
                        temp = copy.deepcopy(old_model_data)
                        temp["val"] = new_val
                        diff_result["data"] = temp
                        diff_result["col_change_list"] = ["val"]
                        model_change_list.append(diff_result)
                        change_flag = True
                    else:  # same
                        diff_result["action"] = "same"
                        diff_result["col_change_list"] = []
                        diff_result["data"] = old_model_data
                        diff_result["record_id"] = old_model_data.get("order_no")
                        model_change_list.append(diff_result)
            else:
                diff_result["action"] = "add"
                diff_result["col_change_list"] = []  # All
                diff_result["data"] = new_model_data
                model_change_list.append(diff_result)
                change_flag = True
        return change_flag, model_change_list

    def diff_point(self, old_point_dict, new_point_dict):
        tmc_point = ["review_result", "pointout_no", "pointout_status", "pointout_comment",
                    "reader_check", "reader2_check", "final_check", "pointout_charger",
                    "pointout_priority", "pointout_date"]
        suntec_point = ["suntec_status", "fixed", "suntec_remark",
                        "arl_rel", "suntec_cannot_modify"]
        diff_result = dict()
        col_change_list = []
        change_flag = False
        if not old_point_dict:
            if not new_point_dict:
                return change_flag, diff_result
            else:
                change_flag = True
                diff_result["action"] = "add"
                diff_result["col_change_list"] = []
                diff_result["data"] = new_point_dict
                return change_flag, diff_result
        else:
            if not new_point_dict:
                return change_flag, diff_result
            else:
                for point in tmc_point:
                    old_val = old_point_dict.get(point)
                    new_val = new_point_dict.get(point)
                    if new_val is None:
                        new_val = ''
                    if old_val is None:
                        old_val = ''
                    if new_val != old_val:
                        change_flag = True
                        diff_result["action"] = "add"
                        diff_result["col_change_list"] = []
                        diff_result["data"] = new_point_dict
                        return change_flag, diff_result
                for point in suntec_point:
                    old_val = old_point_dict.get(point)
                    new_val = new_point_dict.get(point)
                    if new_val is None:
                        new_val = ''
                    if old_val is None:
                        old_val = ''
                    if new_val != old_val:
                        col_change_list.append(point)
                if col_change_list:
                    change_flag = True
                    diff_result["action"] = "change"
                    diff_result["col_change_list"] = col_change_list
                    diff_result["data"] = new_point_dict
                return change_flag, diff_result











    def diff_reason(self, data, old_data, update_time):
        new_reason = str(data.get("reason"))
        old_reason = str(old_data.get("reason"))
        # diff_old_reason = old_reason.replace('\n', '')
        new_reason1 = str(self.reason_norm(new_reason, old_reason, update_time))
        # diff_new_reason = new_reason1.replace('\n', '')
        # old_reason1 = str(self.reason_norm(old_reason, update_time))
        # if re.findall(diff_old_reason, diff_new_reason):
        #     return new_reason1
        # elif re.findall(diff_new_reason, diff_old_reason):
        #     return old_reason
        # else:
        if old_reason[-1] == '\n':
            return old_reason+new_reason1
        return old_reason+'\n'+new_reason1

    def reason_norm(self, reason, old_reason, update_time):
        # mat = re.search(r"(\d{4}[-/]\d{1,2}[-/]\d{1,2})", reason)
        date_list = re.findall(r"(\d{4}[/-]\d{1,2}[/-]\d{1,2})", reason)
        new_date_list = []
        for date in date_list:
            new_date = date.replace('-', '/')
            reason = reason.replace(date, new_date)
            new_date_list.append(new_date)
        # print date_list
        if new_date_list:
            index_list = []
            for date in new_date_list:
                # m.replace("\\", r"\")
                index = re.search(date, reason).span()
                index_list.append(index)
            # print index_list
            reason_list = []
            for i in range(0, len(index_list)):
                if i == len(index_list)-1:
                    start = index_list[i][1]
                    rs = reason[start:]
                    reason_list.append(rs)
                else:
                    start = index_list[i][1]
                    end = index_list[i+1][0]
                    rs = reason[start:end]
                    reason_list.append(rs)
            norm_reason = ''
            if index_list[0][0] != 0:
                norm_reason = reason[0:index_list[0][0]]
                if norm_reason[-1] != '\n':
                    norm_reason = norm_reason+'\n'
            for i in range(0, len(reason_list)):
                reason_list[i] = reason_list[i].replace('\n', '')
                norm_reason = norm_reason + new_date_list[i]+'\n'+reason_list[i]+'\n'

            # print norm_reason
        else:
            # update_time = time.strftime("%Y-%m-%d %H:%M:%S")
            update_time = update_time.split(' ')[0]
            update_time = update_time.replace('-', '/')
            # reason1 = reason.replace('\n', '')
            # old_reason1 = old_reason.replace('\n', '')
            # if re.findall(old_reason1, reason1):
            #     reason2 = reason.replace(old_reason1, '')
            #     reason = update_time + reason2
            #     if old_reason[-1] == '\n':
            #         norm_reason = old_reason + reason
            #     else:
            #         norm_reason = old_reason + '\n' + reason
            # else:
            norm_reason = update_time + '\n' + reason
        return norm_reason
