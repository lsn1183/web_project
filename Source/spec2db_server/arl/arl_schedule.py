# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
from Source.spec2db_server.arl.arl_base import ServiceBase
from Source.spec2db_server.arl.arl_diff import ArlDiff


class ArlSchedule(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "arl_schedule"
        self.key_col = "arl_sch_id"
        self.id_col = "arl_id"
        self.attr_list = ["arl_sch_id",
                          "arl_id", "major_category", "medium_catetory",
                          "small_category", "detail", "req_post",
                          "change_type", "group", "author",
                          "charger", "hu_date", "hu_remark",
                          "def_date", "def_remark", "analysis_date",
                          "analysis_remark", "update_time", "update_user_id"
                          ]
        # 固定列
        self.fixed_list = ["arl_id", "major_category", "medium_catetory",
                           "small_category", "detail", "req_post",
                           "change_type", "group", "author",
                           "charger"]

    def add(self, pg, data, col_list, update_time, role=None, excel_import=True):
        _id = data.get(self.id_col)  # hu_id/definition_id
        old_data = self.get_by_id_for_diff(pg, _id, self.attr_list)
        if old_data:
            data[self.key_col] = old_data.get(self.key_col)
        ignore_col_list = ["update_time", "update_user_id"] + self.fixed_list
        diff_obj = ArlDiff(self.key_col, self.id_col, self.attr_list, ignore_col_list)
        diff_result = diff_obj.diff(old_data, data)
        action = diff_result.get("action")
        if action == "same":
            return []
        data["update_time"] = update_time
        if action == "add":
            # data["new_date"] = update_time.split(' ')[0]  # 日付赋值为更新时间
            rc_id, model_list_change = self._add_one2(pg, data, self.attr_list[1:])
            data[self.key_col] = rc_id
            diff_result[self.key_col] = rc_id
        elif action == "change":
            col_change_list = diff_result.get("col_change_list")
            col_change_list.append("update_time")
            col_change_list.append("update_user_id")
            record_id = diff_result.get(self.key_col)
            if col_change_list:
                if not self.update_col_change_list(pg, record_id, data, col_change_list):
                    return None
        else:
            # 不删除
            pass
        log_list = self.convert2log([diff_result])
        return log_list

    def get_by_id_for_diff(self, pg, _id, col_list):
        sqlcmd = self.list_2_select_sql(self.table_name, col_list, [self.id_col])
        pg.execute(sqlcmd, [_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
        return attr_dict
