# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import json
from Source.spec2db_server.arl.arl_base import ServiceBase
from Source.spec2db_server.arl.db_operate import Cdb_definition
from Source.spec2db_server.arl.def_server import DefRecord
from Source.spec2db_server.arl.arl_base import JOB_STATUS_ASSURED
from Source.spec2db_server.arl.point_out import PointOut


class HuRecord(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "hu"
        self.model_table_name = "hu_model_rel"
        self.model_type_table_name = "hu_model_type"
        self.key_col = "hu_record_id"
        self.id_col = "hu_id"
        self.sub_list_name = "definition_list"
        self.parent_col_name = "arl_id"
        self.child_id_col = "hu_def_id"
        self.attr_list = ["hu_record_id", "author",
                          "arl_id", "hu_id", "unique_id",
                          "system_conf", "rel_requirement", "exception",
                          "dcu_status", "dcu_trigger", "dcu_action",
                          "meu_status", "meu_trigger",  "meu_action",
                          "hu_category_id", "remark", "sys_spec_chapter",
                          "common_chapter", "common_seq_spec", "common_seq_no",
                          "common_cmd_guide", "common_opc", "inter_loc_spec",
                          "inter_chapter", "other_chapter", "other_doc",
                          "amp", "dsrc", "dcm",
                          "rse", "touch_pad", "separate_disp",
                          "test_results", "future_req", "remark1",
                          "remark2", "leak_check", "last_modifier",
                          "new_date", "reason", "translation_flag",
                          "agree_flag", "has_problem", "user_id",
                          "complete_flag", "job_status", "md5_key", "major_ver",
                          "small_ver", "update_time", "basic_req",
                          "lock_status"
                          ]
        self.lock_list = ["dcu_status", "dcu_trigger", "dcu_action", "meu_status", "meu_trigger", "meu_action"]

    def get_new_hu_id(self, arl_id):
        sqlcmd = """
        SELECT max("unique_id"::int)
          FROM spec.hu
          where arl_id = %s
          group by "arl_id";
        """
        hu_record = {"result": "OK"}
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id, ))
        row = self._pg.fetchone()
        if row:
            unique_id = row[0] + 1
        else:
            unique_id = 0
        hu_id = '.'.join([arl_id, str(unique_id)])
        content = {u"unique_id": unique_id,
                   u"hu_id": hu_id}
        hu_record[u"content"] = content
        self._pg.close()
        return hu_record

    def get_info(self, hu_id):
        table_name, condition_col_list = "hu", ["hu_id"]
        sqlcmd = self.list_2_select_sql(table_name, self.attr_list, condition_col_list)
        hu_record = {"result": "NG"}
        self._pg.connect()
        self._pg.execute(sqlcmd, (hu_id,))
        row = self._pg.fetchone()
        if row:
            i = 0
            attr_dict = {}
            while i < len(self.attr_list):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            hu_rc_id = row[0]
            dcu_status = attr_dict.pop("dcu_status")
            dcu_trigger = attr_dict.pop("dcu_trigger")
            dcu_action = attr_dict.pop("dcu_action")
            meu_status = attr_dict.pop("meu_status")
            meu_trigger = attr_dict.pop("meu_trigger")
            meu_action = attr_dict.pop("meu_action")
            hu_category_id = attr_dict.pop("hu_category_id")
            sequence_list = self._get_sequence_list(self._pg, hu_category_id, dcu_status,
                                                    dcu_trigger, dcu_action, meu_status,
                                                    meu_trigger, meu_action, hu_rc_id)
            attr_dict["sequence_list"] = sequence_list
            hu_record["content"] = attr_dict
            hu_record["result"] = "OK"
        self._pg.close()
        return hu_record

    def get_by_hu_id(self, pg, hu_id, col_list):
        sqlcmd = self.list_2_select_sql("hu", col_list, ["hu_id"])
        pg.execute(sqlcmd, [hu_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
            hu_rc_id = row[0]
            model_list = self.get_model_list(pg, hu_rc_id)
            attr_dict["model_list"] = model_list
        return attr_dict

    def get_by_arl_id(self, arl_id):
        hu_record = {u"result": "NG"}
        if not arl_id:
            return hu_record
        self._pg.connect()
        try:
            count, hu_record[u"content"] = self._get_by_arl_id(self._pg, arl_id)
            hu_record[u"total_count"] = count
            hu_record[u"result"] = "OK"
        except:
            pass
        self._pg.close()
        return hu_record

    def get_by_id_deep(self, pg, _id):
        """
        :param _id:  arl_id
        :return:
        """
        if not _id:
            return []
        count, hu_data_list = self._get_by_arl_id(pg, _id)
        from Source.spec2db_server.arl.def_server import DefRecord
        def_obj = DefRecord()
        for data_dict in hu_data_list:
            hu_id = data_dict.get('hu_id')
            point_obj = PointOut(self.table_name)
            point_list = point_obj.get_list_by_id(pg, hu_id)
            data_dict["point_list"] = point_list
            data_dict[self.sub_list_name] = def_obj.get_by_id_deep(pg, hu_id)
        return hu_data_list

    # def get_model_list(self, pg, hu_rc_id):
    #     category_dict = {}
    #     model_list = []
    #     for model_id, model, val, order_no, hu_record_id in self._get_model_list(pg, hu_rc_id):
    #         model_dict = dict()
    #         model_dict["order_no"] = order_no
    #         model_dict["model_id"] = model_id
    #         model_dict["val"] = val
    #         model_dict["hu_record_id"] = hu_record_id
    #         model_list.append(model_dict)
    #     return model_list
        # category_list = []
        # for model_id, model, val, _ in self._get_model_list(hu_rc_id):
        #     category = model[0]
        #     model_dict = dict()
        #     model_dict["model_id"] = model_id
        #     model_dict["name"] = model[1]
        #     model_dict["title"] = model[2]
        #     model_dict["val"] = val
        #     if category not in category_dict:
        #         category_dict[category] = [model_dict]
        #         category_list.append(category)
        #     else:
        #         category_dict[category].append(model_dict)
        # rst_model_list = []
        # for category in category_list:
        #     models = category_dict.get(category)
        #     rst_model_list.append({"category": category,
        #                            "models": models})
        #
        # return rst_model_list

    def get_post_info(self, hu_id):
        from Source.spec2db_server.arl.arl_server import ArlRecord
        arl_post_list = ["major_categor", "medium_catetory",
                         "small_category", "detail", "base"]
        data = {"result": "NG"}
        hu_content = self._get_post_info(hu_id)
        if hu_content:
            arl_id = '.'.join(hu_id.split('.')[:-1])
            arl_obj = ArlRecord()
            arl_post = arl_obj.get_arl_post_info(arl_id)
            if arl_post:
                arl_content = arl_post.get("content")
                for attr in arl_post_list:
                    hu_content[attr] = arl_content.get(attr)
            data["content"] = hu_content
            data["result"] = "OK"
        return data

    def _get_post_info(self, hu_id):
        post_list = ["hu_id", "rel_requirement",
                     "dcu_status", "dcu_trigger", "dcu_action",
                     "meu_status", "meu_trigger", "meu_action"]
        table_name, condition_col_list = "hu", ["hu_id"]
        sqlcmd = self.list_2_select_sql(table_name, post_list, condition_col_list)
        self._pg.connect()
        self._pg.execute(sqlcmd, (hu_id,))
        row = self._pg.fetchone()
        content = {}
        if row:
            for i in range(0, len(row)):
                attr = post_list[i]
                content[attr] = row[i]
        self._pg.close()
        return content

    def get_by_category(self, category_id, size, page):
        hu_record = {"result": "NG"}
        if not category_id:
            return hu_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        if len(cat_id_list) != 5:
            return hu_record
        hu = HuRecord()
        count, hu_record[u"content"] = self._get_by_category(cat_id_list,
                                                             size,
                                                             page)
        if hu_record[u"content"]:
            hu_record[u"total_count"] = count
            hu_record[u"result"] = "OK"
        return hu_record

    def get_by_category2(self, category_id, size, page, user_id=None):
        hu_record = {"result": "NG"}
        if not category_id:
            return hu_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, hu_record["content"] = self.get_by_categorysql(cat_id_list, size, page, user_id)
        hu_record["total_count"] = count
        hu_record["result"] = "OK"
        return hu_record

    def get_by_categorysql3(self, cat_id_list, filter_dict, user_id):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        filter_cond = self.get_filter_condition(filter_dict)
        if filter_cond:
            filter_cond = " where %s" % filter_cond
            # print "hu:", filter_cond
        sqlcmd = """ 
        SELECT hu_record_id, hu_id, t2.arl_id,
               dcu_status, dcu_trigger, dcu_action,
               meu_status, meu_trigger, meu_action,
               hu_category_id, t2.job_status, t3.user_name,
               t4.job_status as job_status_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        LEFT JOIN spec.arl_user t3
        on t1.user_id = t3.user_id
        left join spec.arl_job_status as t4
        on t2.job_status = t4.job_status_id
        %s
        ORDER BY length(hu_id), hu_id
        """ % (condition, filter_cond)
        self._pg.connect()
        self._pg.execute(sqlcmd, params)
        rows = self._pg.fetchall()
        rowcount = self._pg.pgcur.rowcount
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _get_summary_data_list(self, condition_str, params, like_condition, complete_str, size, page):
        if like_condition:
            like_condition = 'where ' + like_condition
        if complete_str == '2':
            child_str = """
            LEFT JOIN spec.arl_schedule as sdl
            ON t1.arl_id = sdl.arl_id
            inner join (
                select arl_id
                from spec.hu
                where job_status = 2
                ) as com
            on t1.arl_id = com.arl_id
            """
        elif complete_str:
            child_str = """
            LEFT JOIN spec.arl_schedule as sdl
            ON t1.arl_id = sdl.arl_id
            LEFT JOIN spec.definition as child
            ON t2.hu_id = child.hu_def_id
            """
            if like_condition:
                like_condition += 'and ' + complete_str + " and def_date <> '-'"
            else:
                like_condition = 'where ' + complete_str + " and def_date <> '-'"
        else:
            child_str = ""
        sqlcmd = """ 
        SELECT distinct hu_record_id, hu_id, t2.arl_id,
               dcu_status, dcu_trigger, dcu_action,
               meu_status, meu_trigger, meu_action,
               hu_category_id, t2.job_status, t3.user_name,
               t4.job_status as job_status_name, t1.update_time, length(hu_id) as len
          FROM (
            SELECT arl_id, user_id, update_time
              FROM spec.arl 
              {condition_str}
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        LEFT JOIN spec.arl_user t3
        on t1.user_id = t3.user_id
        left join spec.arl_job_status as t4
        on t2.job_status = t4.job_status_id
        {child_str}
        {like_condition}
        ORDER BY t1.update_time DESC
        """.format(condition_str=condition_str, child_str=child_str, like_condition=like_condition)
        self._pg.connect()
        rowcount, rows = self._fetch_many(self._pg, sqlcmd, params, size, page)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _rows_2_summay_data(self, rows):
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            hu_record_id, attr_dict["hu_id"], attr_dict["arl_id"] = row[0:3]
            attr_dict["title"] = 'HU: ' + row[1]
            dcu_status, dcu_trigger, dcu_action = row[3:6]
            meu_status, meu_trigger, meu_action = row[6:9]
            hu_category_id = row[9]
            attr_dict["job_status"], attr_dict["user_name"], attr_dict["job_status_name"] = row[10: 13]
            sequence_list = self._get_sequence_list(self._pg, hu_category_id, dcu_status,
                                                    dcu_trigger, dcu_action, meu_status,
                                                    meu_trigger, meu_action, hu_record_id)
            sequence_str = self._sequence_list_2_str(sequence_list)
            attr_dict["sequence_list"] = sequence_str
            attr_dict_list.append(attr_dict)
            attr_dict["title"] = 'HU: ' + attr_dict['hu_id']
        return attr_dict_list

    def _get_summary_user_list(self, condition_str, params, like_condition):
        sqlcmd = """ 
        SELECT DISTINCT t1.user_id, t3.user_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        LEFT JOIN spec.arl_user t3
        on t1.user_id = t3.user_id
        left join spec.arl_job_status as t4
        on t2.job_status = t4.job_status_id
        %s
        ORDER BY t3.user_name
        """ % (condition_str, like_condition)
        user_list = []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, params)
            rows = self._pg.fetchall()
            self._pg.close()
            for row in rows:
                user_id = row[0]
                user_name = row[1]
                user_list.append({"user_id": user_id, "user_name": user_name})
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return user_list

    def get_by_categorysql(self, cat_id_list, size, page, user_id):
        from Source.spec2db_server.arl.arl_server import ArlRecord
        arl_obj = ArlRecord()
        condition, params = arl_obj.get_category_condition(cat_id_list, user_id)
        sqlcmd = """ 
        SELECT hu_record_id, hu_id, t2.arl_id,
               dcu_status, dcu_trigger, dcu_action,
               meu_status, meu_trigger, meu_action,
               hu_category_id, t2.job_status, t3.user_name,
               t4.job_status as job_status_name
        FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        LEFT JOIN spec.arl_user t3
        on t1.user_id = t3.user_id
        left join spec.arl_job_status as t4
        on t2.job_status = t4.job_status_id
        ORDER BY length(hu_id), hu_id
        """ % condition
        self._pg.connect()
        offset = size * (page - 1)
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _get_by_category(self, cat_id_list, size, page):
        table_name = "hu"
        condition_col_list = ["cat_id0", "cat_id1", "cat_id2", "cat_id3", "cat_id4"]
        sqlcmd = self.list_2_select_sql(table_name, self.attr_list, condition_col_list)
        self._pg.connect()
        offset = size * (page - 1)
        self._pg.execute(sqlcmd, cat_id_list)

        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount - 1:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(row):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            attr_dict_list.append(attr_dict)
        self._pg.close()
        return rowcount, attr_dict_list

    def _get_by_arl_id(self, pg, arl_id):
        table_name = "hu"
        condition_col_list = ["arl_id"]
        order_cols = ["length(%s)"%self.id_col, self.id_col]
        sqlcmd = self.list_2_select_sql(table_name, self.attr_list, condition_col_list, order_cols)
        pg.connect()
        # offset = size * (page - 1)
        pg.execute(sqlcmd, (arl_id,))
        rowcount = pg.pgcur.rowcount
        rows = pg.fetchall()
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(row):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            hu_rc_id = row[0]
            attr_dict['title'] = 'HU要件定義: ' + attr_dict['hu_id']
            dcu_status = attr_dict.pop("dcu_status")
            dcu_trigger = attr_dict.pop("dcu_trigger")
            dcu_action = attr_dict.pop("dcu_action")
            meu_status = attr_dict.pop("meu_status")
            meu_trigger = attr_dict.pop("meu_trigger")
            meu_action = attr_dict.pop("meu_action")
            hu_category_id = attr_dict.pop("hu_category_id")
            sequence_list = self._get_sequence_list(pg, hu_category_id, dcu_status,
                                                    dcu_trigger, dcu_action, meu_status,
                                                    meu_trigger, meu_action, hu_rc_id)
            attr_dict["sequence_list"] = sequence_list
            attr_dict_list.append(attr_dict)
        return rowcount, attr_dict_list

    def _sequence_2_model_list(self, data_dict):
        sequence_list = data_dict.pop("sequence_list")
        hu_category_id, dcu_dict, meu_dict, model_list = self._parser_equence_list(sequence_list)
        data_dict["hu_category_id"] = hu_category_id
        data_dict.update(dcu_dict)
        data_dict.update(meu_dict)
        data_dict["model_list"] = model_list

    def _delete_by_arl_id(self, pg, arl_id):
        sqlcmd = """
        DELETE FROM spec.hu_model_rel
          where hu_record_id in (
            select hu_record_id
              from spec.hu
              where arl_id = %s
          ); 
        DELETE FROM spec.hu
         WHERE arl_id = %s;
        """
        pg.execute(sqlcmd, (arl_id, arl_id))

    # def add(self, pg, data, col_list, update_time, excel_import=True):
    #     if excel_import:  # input from excel
    #         data["job_status"] = JOB_STATUS_ASSUREDED
    #     hu_id = data.get("hu_id")
    #     old_data = self.get_by_hu_id(pg, hu_id, self.attr_list)
    #     # md5_check = True
    #     if self.check_md5_key(data, old_data):
    #         md5_check = True
    #     else:
    #         md5_check = False
    #         return md5_check, []
    #     if old_data:
    #         data["hu_record_id"] = old_data.get("hu_record_id")
    #         data["small_ver"] = old_data.get("small_ver")
    #         data["update_time"] = old_data.get("update_time")
    #         # data["md5_key"] = old_data.get("md5_key")
    #     # Generate New md5
    #     major_ver, small_ver = self.get_new_version(pg, data, old_data)
    #     data["major_ver"] = major_ver
    #     # compare
    #     from Source.spec2db_server.arl.arl_diff import ArlDiff
    #     ignore_col_list = [self.sub_list_name]
    #     diff_obj = ArlDiff("hu_record_id", "hu_id", self.attr_list, ignore_col_list)
    #     diff_result = diff_obj.diff(old_data, data)
    #     action = diff_result.get("action")
    #     if action == "same":
    #         return md5_check, []
    #     md5_key = self.generate_md5_key(data)
    #     data["md5_key"] = md5_key
    #     data["small_ver"] = small_ver
    #     data["update_time"] = update_time
    #     if action == "add":
    #         rc_id, model_list_change = self._add_one2(pg, data, self.attr_list[1:])
    #         data[self.key_col] = rc_id
    #         diff_result["hu_record_id"] = rc_id
    #         model_list = diff_result.get("model_list")
    #         for i in range(len(model_list)):
    #             model_list[i]["data"] = model_list_change[i]
    #             model_list[i]["record_id"] = model_list_change[i].get("order_no")
    #     elif action == "change":
    #         col_change_list = diff_result.get("col_change_list")
    #         col_change_list.append("small_ver")
    #         col_change_list.append("md5_key")
    #         col_change_list.append("update_time")
    #         hu_record_id = diff_result.get("hu_record_id")
    #         if col_change_list:
    #             if self.update_col_change_list(pg, hu_record_id, data, col_change_list):
    #                 model_diff_list = diff_result.get("model_list")
    #         if not self.update_model_diff_list(pg, hu_record_id, model_diff_list):
    #             return md5_check, None
    #     else:
    #         self.delete(hu_id)
    #         # delete TAGL Definition
    #     log_list = self.convert2log([diff_result])
    #     return md5_check, log_list

    def _add_sub(self, pg, data, update_time):
        hu_id = data.get(self.id_col)
        def_data_list = data.get(self.sub_list_name)
        def_obj = DefRecord()
        sub_log_list = def_obj.add_list(pg, hu_id, def_data_list, update_time)
        if sub_log_list is None:
            return None
        point_out = PointOut(self.table_name)
        po_log_list = point_out.add_list(pg, data.get(self.id_col), data.get("point_list"), update_time)
        if po_log_list is None:
            return None
        return sub_log_list + po_log_list

    def _delete_sub(self, pg, hu_id, update_time):
        def_obj = DefRecord()
        sub_log_list = def_obj.delete_by_parent(pg, hu_id, update_time)
        return sub_log_list

    def _get_parent_version(self, pg, data):
        arl_id = data.get("arl_id")
        from Source.spec2db_server.arl.arl_server import ArlRecord
        arl_obj = ArlRecord()
        parent_ver_dict = arl_obj.get_version(pg, arl_id)
        return parent_ver_dict

    def _add_one(self, data_dict):
        """from web."""
        params = []
        sequence_list = data_dict.get("sequence_list")
        hu_category_id, dcu_dict, meu_dict, model_list = self._parser_equence_list(sequence_list)
        data_dict["hu_category_id"] = hu_category_id
        data_dict.update(dcu_dict)
        data_dict.update(meu_dict)
        data_dict["model_list"] = model_list
        col_list = []
        for attr in self.attr_list:
            if attr != "hu_record_id":
                val = data_dict.get(attr)
                params.append(val)
                col_list.append(attr)
        sqlcmd = self.list_2_insert_sql("hu", col_list, "hu_record_id")
        self._pg.execute(sqlcmd, params[1:])
        rc_id = self.fetch_id(self._pg)
        self._add_model_list(self._pg, rc_id, model_list)
        return rc_id

    def _add_model_list(self, pg, rc_id, model_list):
        if not rc_id or not model_list:
            return
        model_list_changes = []
        for model_dict in model_list:
            if "models" in model_dict:
                models = model_dict.get("models")
                for model in models:
                    model_id = model.get("model_id")
                    val = model.get("val")
                    order_no = self._insert_model(pg, rc_id, model_id, val)
                    model_dict["order_no"] = order_no
                    model_dict["hu_record_id"] = rc_id
                    model_list_changes.append(model_dict)
            else:
                model_id = model_dict.get("model_id")
                val = model_dict.get("val")
                order_no = self._insert_model(pg, rc_id, model_id, val)
                model_dict["order_no"] = order_no
                model_dict["hu_record_id"] = rc_id
                model_list_changes.append(model_dict)
        return model_list_changes

    def _update_model_list(self, rc_id, model_list):
        if not rc_id:
            return
        sqlcmd = """
        DELETE FROM spec.hu_model_rel
        where hu_record_id = %s
        """
        self._pg.execute(sqlcmd, (rc_id,))
        sqlcmd = """
        UPDATE spec.hu_model_rel SET val = %s
            where hu_record_id = %s and model_id = %s
        """
        for i in range(0, len(model_list)):
            model_id = i + 1
            val = model_list[i]
            self._pg.execute(sqlcmd, (val, rc_id, model_id))
            if self._pg.pgcur.rowcount == 0:
                self._insert_model(rc_id, model_id, val)

    # def update_col_change_list(self, pg, hu_record_id, data, col_change_list):
    #     params = self.get_params(data, col_change_list)
    #     condition_col_list, key_col = ["hu_record_id"], "hu_record_id"
    #     sqlcmd = self.list_2_update_sql("hu", col_change_list, condition_col_list, key_col)
    #     pg.execute(sqlcmd, params + [hu_record_id])
    #     if pg.pgcur.rowcount:
    #         return True
    #     return False

    # def update_model_diff_list(self, pg, hu_record_id, model_diff_list):
    #     if model_diff_list:
    #         update_sql = self.list_2_update_sql("hu_model_rel", ["val"], ["order_no"], "order_no")
    #         insert_sql = self.list_2_insert_sql("hu_model_rel", ["hu_record_id", "model_id", "val"], "order_no")
    #         delete_sql = self.list_2_delete_sql("hu_model_rel", ["order_no"])
    #         for change_dict in model_diff_list:
    #             change_dict.get("data")["hu_record_id"] = hu_record_id
    #             action = change_dict.get("action")
    #             data = change_dict.get("data")
    #             if action == 'change':
    #                 val = data.get("val")
    #                 order_no = data.get("order_no")
    #                 pg.execute(update_sql, [val, order_no])
    #                 if pg.pgcur.rowcount <= 0:
    #                     return False
    #                 data["def_rc_id"] = hu_record_id
    #                 change_dict["record_id"] = order_no
    #             elif action == 'add':
    #                 data = change_dict.get("data")
    #                 model_id = data.get("model_id")
    #                 val = data.get("val")
    #                 params = [hu_record_id, model_id, val]
    #                 pg.execute(insert_sql, params)
    #                 if pg.pgcur.rowcount <= 0:
    #                     return False
    #                 order_no = self.fetch_id(pg)
    #                 data["order_no"] = order_no
    #                 change_dict["data"] = data
    #                 change_dict["record_id"] = order_no
    #             elif action == 'delete':
    #                 params = [data.get("order_no")]
    #                 pg.execute(delete_sql, params)
    #                 if pg.pgcur.rowcount <= 0:
    #                     return False
    #             else:  # same
    #                 pass
    #     return True

    def delete(self, pg, hu_id):
        sqlcmd = """
        DELETE FROM spec.hu_model_rel
          where hu_record_id in (
            select hu_record_id
              from spec.hu
              where hu_id = %s
          );
        """
        sqlcmd2 = """DELETE FROM spec.hu WHERE "hu_id" = %s;"""
        pg.execute(sqlcmd, (hu_id, ))
        pg.execute(sqlcmd2, (hu_id,))
        if pg.pgcur.rowcount > 0:
            return True
        return False

    def get_category_tree(self, user_id):
        cat_tree = {"result": "OK/NG",
                    "content": [{"category_id": "",
                                 "category_name": "XXX",
                                 "sub_category_list": [{}]
                                }
                               ]
                    }
        cat_info_tree = self._get_category()
        cat_tree[u"content"] = self._trans_category(cat_info_tree)
        cat_tree[u"result"] = "OK"
        return cat_tree

    def _get_category(self):
        sqlcmd = """
                SELECT distinct cat_id0, category,
                       cat_id1, major_category,
                       cat_id2, medium_catetory,
                       cat_id3, small_category,
                       cat_id4, detail
                  FROM spec.hu
                  ORDER BY cat_id0, cat_id1, cat_id2, cat_id3, cat_id4;
                """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        cat_info_tree = {}
        for row in self._pg.fetchall():
            j = 0
            cat = cat_info_tree
            while j < len(row):
                cat_id = row[j]
                cat_name = row[j + 1]
                key = (cat_id, cat_name)
                if key in cat:
                    cat = cat.get(key)
                else:
                    cat[key] = {}
                    cat = cat.get(key)
                j += 2
        self._pg.close()
        return cat_info_tree

    def _get_model_list(self, pg, _id):
        sqlcmd = """
        SELECT a.model_id, model, a.val, a.order_no, a.hu_record_id
          FROM spec.hu_model_rel as a
          LEFT JOIN spec.hu_model_type as b
          ON a.model_id = b.model_id
          WHERE hu_record_id = %s
          ORDER BY a.model_id
        """
        pg.execute(sqlcmd, (_id,))
        rows = pg.fetchall()
        for row in rows:
            model_id, model, val, order_no, hu_record_id = row
            model = json.loads(model)
            yield model_id, model, val, order_no, hu_record_id

    def get_all_model_list(self):
        result = {"reslut": "NG"}
        sqlcmd = """
        SELECT model_id, model
          FROM spec.hu_model_type
          order by model_id;
        """
        model_list = []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd)
            rows = self._pg.fetchall()
            for row in rows:
                model_dict = dict()
                model_id, model = row[0:2]
                model = json.loads(model)
                model_dict["model_id"] = model_id
                model_dict["category"] = model[0]
                model_dict["name"] = model[1]
                model_dict["title"] = model[2]
                model_list.append(model_dict)
            self._pg.close()
        except:
            self._pg.close()
        if model_list:
            result["reslut"] = "OK"
            result["content"] = model_list
        return result

    def get_all_model_types(self, pg):
        return self._get_all_model_types(pg)

    def _get_all_model_types(self, pg):
        sqlcmd = """
        SELECT model_id, model
          FROM spec.hu_model_type
          order by model_id;
        """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        model_info_dict = dict()
        for row in rows:
            model_dict = dict()
            model_id, model = row[0:2]
            model = json.loads(model)
            model_dict["model_id"] = model_id
            model_dict["category"] = model[0]
            model_dict["name"] = model[1]
            model_dict["title"] = model[2]
            model_info_dict[model_id] = model_dict
        return model_info_dict

    def get_graph(self, arl_id):
        sqlcmd = """
        SELECT hu_id
          FROM spec.hu
          where arl_id = %s
          ORDER BY unique_id
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        rows = self._pg.fetchall()
        hu_list = []
        for row in rows:
            hu_dict = dict()
            hu_id = row[0]
            hu_dict["HU"] = hu_id
            def_obj = Cdb_definition()
            hu_dict["children"] = def_obj.get_graph(hu_id)
            hu_list.append(hu_dict)
        self._pg.close()
        return hu_list

    def get_option(self):
        sqlcmd = """
        SELECT amp, dsrc, dcm, rse, touch_pad, separate_disp,
           (array_agg(system_conf))[1] as system_conf
           FROM (
           SELECT id, amp, dsrc, dcm, 
           rse, touch_pad, separate_disp, system_conf
           FROM spec.hu_option_item
           order by id
           ) as a
           group by amp, dsrc, dcm, rse, touch_pad, separate_disp
          """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        option_dict = dict()
        for row in rows:
            key = ','.join(row[0:6])
            val = row[6]
            option_dict[key] = val
        self._pg.close()
        return option_dict

    def _get_sequence_list(self, pg, hu_category_id, dcu_status, dcu_trigger, dcu_action,
                           meu_status, meu_trigger, meu_action, _id):
        sequence_list, ref_base_list = [], []
        dcu_sequence_dict, meu_sequence_dict = dict(), dict()
        if hu_category_id in (3, '3'):  # DCU/MEU
            dcu_sequence_dict, dcu_ref_base = self._split_dcu_meu_seq('DCU/MEU', dcu_status, dcu_trigger, dcu_action)
            ref_base_list += dcu_ref_base
        else:
            dcu_sequence_dict, dcu_ref_base = self._split_dcu_meu_seq('DCU', dcu_status, dcu_trigger, dcu_action)
            meu_sequence_dict, men_ref_base = self._split_dcu_meu_seq('MEU', meu_status, meu_trigger, meu_action)
            ref_base_list += dcu_ref_base + men_ref_base
        device_sequence_dict, device_ref_base = self._get_device_seq(pg, _id)   # 设备
        ref_base_list += device_ref_base
        seq_id_list = dcu_sequence_dict.keys() + meu_sequence_dict.keys() + device_sequence_dict.keys()
        seq_id_list = sorted(set(seq_id_list))
        for seq_id in seq_id_list:
            sequence = dcu_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
            sequence = meu_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
            sequence = device_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
        sequence_list += ref_base_list  # 引用基本要件 放最后
        return sequence_list

    def _get_device_seq(self, pg, _id):
        sequence_dict, ref_base_list = dict(), list()
        next_step = 0.001
        for model_id, model, val, _, _ in self._get_model_list(pg, _id):
            if self._is_ref_base(val):
                ref_base_dict = {"type": "DEVICE",
                                 "id": model_id,
                                 "category": model[0],
                                 "name": model[1],
                                 "info": model[-1],
                                 "status": "",
                                 "trigger": "",
                                 "action": val}
                ref_base_list.append(ref_base_dict)
            else:
                seq_dict = self._split_sequence(val)
                for seq_id, seq_content in seq_dict.iteritems():
                    seq_id = float(seq_id)
                    if seq_id in sequence_dict:
                        seq_id += next_step
                        next_step += 0.001
                    sequence_dict[seq_id] = {"type": "DEVICE",
                                             "id": model_id,
                                             "category": model[0],
                                             "name": model[1],
                                             "info": model[-1],
                                             "status": "",
                                             "trigger": "",
                                             "action": seq_content,
                                             }
        return sequence_dict, ref_base_list

    def _parser_equence_list(self, sequence_list):
        hu_category_id = '-'
        dcu_sequence_dict, meu_sequence_dict, device_sequence_dict = dict(), dict(), dict()
        for seq_id, seq_dict in enumerate(sequence_list, 1):
            _type = seq_dict.get("type")
            if _type == 'DCU':
                dcu_sequence_dict[seq_id] = seq_dict
            elif _type == "MEU":
                meu_sequence_dict[seq_id] = seq_dict
            elif _type == "DCU/MEU":
                dcu_sequence_dict[seq_id] = seq_dict
                hu_category_id = '3'
            elif _type == "DEVICE":
                device_sequence_dict[seq_id] = seq_dict
        if hu_category_id != '3':
            if dcu_sequence_dict and meu_sequence_dict:
                hu_category_id = '0'
            if dcu_sequence_dict and not meu_sequence_dict:
                hu_category_id = '1'
            if not dcu_sequence_dict and meu_sequence_dict:
                hu_category_id = '2'
        dcu_dict = self._merger_dcu_meu_sequence(dcu_sequence_dict, "DCU")
        if hu_category_id == '3':
            same = "(DCUと同様)"
            meu_dict = {"meu_status": same, "meu_trigger": same, "meu_action": same}
        else:
            meu_dict = self._merger_dcu_meu_sequence(meu_sequence_dict, "MEU")
        model_list = self._merger_device_sequence(device_sequence_dict)
        return hu_category_id, dcu_dict, meu_dict, model_list

    def _merger_dcu_meu_sequence(self, sequence_dict, _type):
        if sequence_dict:
            seq_id_list = sequence_dict.keys()
            status, trigger, action = '', '', ''
            for seq_id in sorted(seq_id_list):
                status = sequence_dict.get(seq_id).get("status")
                temp_trigger = sequence_dict.get(seq_id).get("trigger")
                temp_action = sequence_dict.get(seq_id).get("action")
                if temp_trigger:
                    if not trigger:
                        # trigger = "(%s)%s" % (seq_id, temp_trigger)
                        trigger = temp_trigger
                    else:
                        # trigger = "%s\n(%s)%s" % (trigger, seq_id, temp_trigger)
                        trigger = "%s\n%s" % (trigger, temp_trigger)
                if temp_action:
                    if not action:
                        # action = "(%s)%s" % (seq_id, temp_action)
                        action = temp_action
                    else:
                        # action = "%s\n(%s)%s" % (action, seq_id, temp_action)
                        action = "%s\n%s" % (action, temp_action)
        else:
            status, trigger, action = '-', '-', '-'
        if _type in ("DCU",):
            return {"dcu_status": status, "dcu_trigger": trigger, "dcu_action": action}
        else:
            return {"meu_status": status, "meu_trigger": trigger, "meu_action": action}

    def category_model_list(self, model_list):
        """model list按部品分类"""
        category_dict = dict()
        for model_dict in model_list:
            category = model_dict.get("category")
            if category not in category_dict:
                category_dict[category] = [model_dict]
            else:
                category_dict[category].append(model_dict)
        return category_dict
        # rst_model_list = []
        # for category in category_dict.keys():
        #     models = category_dict.get(category)
        #     rst_model_list.append({"category": category,
        #                            "models": models})
        # return rst_model_list

    def get_arl_by_id_for_diff(self, pg, arl_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

    def _model_type_2_tree(self, model_list):
        """只有叶子的model_id是正确的"""
        forest_model = []
        for model_id, model in model_list:
            sub_list = forest_model
            for model_name in model[:-1]:
                if model_name:
                    found_model_dict = dict()
                    for temp_model_dict in sub_list[::-1]:
                        if model_name == temp_model_dict.get("name"):
                            found_model_dict = temp_model_dict
                            break
                    if not found_model_dict:
                        found_model_dict = {"name": model_name, "sub_list": []}
                        sub_list.append(found_model_dict)
                    found_model_dict["model_id"] = model_id
                    found_model_dict["info"] = model[-1]
                    sub_list = found_model_dict.get("sub_list")
                else:  #
                    pass
        return forest_model

    def update_post_lock_status(self, pg):
        sqlcmd = """
        -- 清空转记锁
        update spec.hu as t1 set lock_status = 0
          from (
            SELECT distinct hu_id
              FROM spec.hu as a
              left join spec.definition as b
              on a.hu_id = b.hu_def_id and b.lock_status = 1
              where hu_def_id is null and a.lock_status = 2
          ) as t2
          where t1.hu_id = t2.hu_id
        """
        pg.execute(sqlcmd)


def main():
    hu = HuRecord()
    # data = hu.get_info("30.9.9.2.6.7.0")  # 2个DCU,2个MEU
    # data = hu.get_info("50.1.3.1.3.833.0")  # 带device?
    # data2 = [data.get("content")]
    # hu.add_list(data2)
    # r = hu.get_forest_model_type()
    # print r
    # return
    from Source.spec2db_server.arl.arl_server import ArlSpec
    spec_obj = ArlSpec()
    data = {"user_id": 0,
            "type": "tagl_ana",  # arl / hu / tagl_def / tagl_ana,
            "category_id": "1-35-157",
            "condition": {"definition_id": "2"}
            }
    result = spec_obj.get_by_category(data)
    return result

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
