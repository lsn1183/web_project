# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import json
import re
from Source.spec2db_server.common import db
from Source.spec2db_server.arl.arl_base import ServiceBase
from Source.spec2db_server.arl.point_out import PointOut


class AnalysisRecord(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "analysis"
        self.model_table_name = "analysis_model_rel"
        self.model_type_table_name = "analysis_model_type"
        self.key_col = "analysis_rc_id"
        self.id_col = "analysis_id"
        self.parent_col_name = "definition_id"
        self.attr_list = ["analysis_rc_id", "author_name", "definition_id",
                          "unique_id", "exception", "seq_diagram",
                          # "application", "kernel", "systemd",  # 移到Model List.
                          "supple_spec", "uncheck", "remark",
                          "user_id", "update_time", "ana_1", "ana_2", "ana_3", "ana_4",
                          "translation_flag", "agree_flag", "has_problem",
                          "new_date", "reason", "complete_flag",
                          "major_ver", "md5_key", "small_ver",
                          "job_status", "asta_filename", "basic_req",
                          "rel_requirement", "lock_status", "analysis_id"
                          ]

    # def _assign_id(self, parent_id, data_list):
    #     for unique_id, data_dict in enumerate(data_list, 0):
    #         if self.parent_col_name:
    #             data_dict[self.parent_col_name] = parent_id
    #         data_dict["unique_id"] = unique_id
    #         data_dict[self.id_col] = parent_id
    #         # print self.id_col, data_dict.get(self.id_col)
    #         self._sequence_2_model_list(data_dict)

    def get_by_id_deep(self, pg, _id):
        """
        :param _id:  arl_id
        :return:
        """
        _, def_data_list = self.get_by_def_id(pg, _id)
        for def_data in def_data_list:
            point_obj = PointOut(self.table_name)
            point_list = point_obj.get_list_by_id(pg, _id)
            def_data["point_list"] = point_list
        return def_data_list

    def get_by_def_id(self, pg, def_id):
        """
        :param def_id:  definition id
        :return:
        """
        if not def_id:
            return []
        condition_col_list = [self.parent_col_name]
        order_cols = ["length(%s)" % self.id_col, self.id_col]
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, condition_col_list, order_cols)
        pg.execute(sqlcmd, (def_id,))
        rowcount = pg.pgcur.rowcount
        rows = pg.fetchall()
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(row):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            analysis_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件分析: ' + attr_dict.get(self.id_col)
            sequence_list = self._get_sequence(pg, analysis_rc_id)
            attr_dict["sequence_list"] = sequence_list
            attr_dict_list.append(attr_dict)
        return rowcount, attr_dict_list

    def _get_sequence(self, pg, analysis_rc_id):
        sequence_list, ref_base_list = [], []
        device_sequence_dict, ref_base_list = self._get_device_seq(pg, analysis_rc_id)   # 设备(model_list)
        seq_id_list = device_sequence_dict.keys()
        seq_id_list = sorted(set(seq_id_list))
        for seq_id in seq_id_list:
            sequence = device_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
        sequence_list += ref_base_list
        return sequence_list

    def _sequence_2_model_list(self, data_dict):
        sequence_list = data_dict.pop("sequence_list")
        model_list = self._parser_sequence_list(sequence_list)
        data_dict["model_list"] = model_list

    def _parser_sequence_list(self, sequence_list):
        device_sequence_dict = dict()
        for seq_id, seq_dict in enumerate(sequence_list, 1):
            _type = seq_dict.get("type")
            if _type == "DEVICE":
                device_sequence_dict[seq_id] = seq_dict
            else:
                print 'DEF sequence type error: %s' % _type
        model_list = self._merger_device_sequence(device_sequence_dict)
        return model_list

    def get_by_category2(self, category_id, size, page, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, arl_record["content"] = self.get_by_categorysql(cat_id_list, size, page, user_id)
        arl_record["total_count"] = count
        arl_record["result"] = "OK"
        return arl_record

    def get_by_categorysql(self, cat_id_list, page_size, page_number, user_id=None):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        sqlcmd = """
        SELECT analysis_rc_id, 
               t4.definition_id, t1.arl_id, t4.seq_diagram,
               t4.job_status, t5.user_name, t6.job_status as job_status_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
               %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        inner join spec.analysis as t4
        on t3.definition_id = t4.definition_id
        LEFT JOIN spec.arl_user t5
        on t1.user_id = t5.user_id
        left join spec.arl_job_status as t6
        on t4.job_status = t6.job_status_id
        ORDER BY length(t4."definition_id"), t4."definition_id"
        """ % condition
        def_list = ["analysis_rc_id", "definition_id", "arl_id", "seq_diagram",
                    "job_status", "user_name", "job_status_name", self.id_col]
        self._pg.connect()
        offset = page_size * (page_number - 1)
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(page_size)
        def_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(def_list):
                attr_dict[def_list[i]] = row[i]
                i += 1
            analysis_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件分析: '+ attr_dict.get(self.id_col)
            sequence_list = self._get_sequence(self._pg, analysis_rc_id)
            sequence_str = self._sequence_list_2_str(sequence_list)
            attr_dict["sequence_list"] = sequence_str
            def_dict_list.append(attr_dict)
        self._pg.close()
        return rowcount, def_dict_list

    def get_by_categorysql3(self, cat_id_list, filter_dict, user_id):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        filter_cond = self.get_filter_condition(filter_dict)
        if filter_cond:
            filter_cond = "WHERE t4.%s" % filter_cond
        sqlcmd = """
        SELECT analysis_rc_id, 
               t4.definition_id, t1.arl_id, t4.seq_diagram,
               t4.job_status, t5.user_name, t6.job_status as job_status_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
               %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        inner join spec.analysis as t4
        on t3.definition_id = t4.definition_id
        LEFT JOIN spec.arl_user t5
        on t1.user_id = t5.user_id
        left join spec.arl_job_status as t6
        on t4.job_status = t6.job_status_id
        %s
        ORDER BY length(t4."definition_id"), t4."definition_id"
        """ % (condition, filter_cond)
        def_list = ["analysis_rc_id", "definition_id", "arl_id", "seq_diagram",
                    "job_status", "user_name", "job_status_name"]
        self._pg.connect()
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        rows = self._pg.fetchall()
        def_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(def_list):
                attr_dict[def_list[i]] = row[i]
                i += 1
            analysis_rc_id = row[0]
            attr_dict['title'] = '要件分析: ' + attr_dict.get(self.id_col)
            sequence_list = self._get_sequence(self._pg, analysis_rc_id)
            sequence_str = self._sequence_list_2_str(sequence_list)
            attr_dict["sequence_list"] = sequence_str
            def_dict_list.append(attr_dict)
        self._pg.close()
        return rowcount, def_dict_list

    def _get_summary_data_list(self, condition_str, params, like_condition, complete_str, size, page):
        if like_condition:
            like_condition = "WHERE t4.%s" % like_condition
        if complete_str == '2':
            child_str = """
            inner join (
                select arl_id
                from spec.hu
                where job_status = 2
                union
                SELECT ARRAY_TO_STRING(a[1:ARRAY_UPPER(a, 1) - 2], '.') as arl_id
                from (
                    select definition_id, regexp_split_to_array(definition_id, E'\\.+') a
                    from spec.definition
                    where job_status = 2
                    ) as b
                union
                SELECT ARRAY_TO_STRING(a[1:ARRAY_UPPER(a, 1) - 2], '.') as arl_id
                from (
                    select definition_id, regexp_split_to_array(definition_id, E'\\.+') a
                    from spec.analysis
                    where job_status = 2
                ) as b
            ) as com
            on t1.arl_id = com.arl_id
            """
        else:
            child_str = ""
        sqlcmd = """
        SELECT analysis_rc_id, t4.definition_id, t1.arl_id, t4.seq_diagram,
               t4.job_status, t5.user_name, t6.job_status as job_status_name, t4.analysis_id
          FROM (
            SELECT arl_id, user_id, update_time
              FROM spec.arl 
               %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        inner join spec.analysis as t4
        on t3.definition_id = t4.definition_id
        LEFT JOIN spec.arl_user t5
        on t1.user_id = t5.user_id
        left join spec.arl_job_status as t6
        on t4.job_status = t6.job_status_id
        %s
        %s
        ORDER BY t4.update_time DESC
        """ % (condition_str, child_str, like_condition)
        self._pg.connect()
        rowcount, rows = self._fetch_many(self._pg, sqlcmd, params, size, page)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _rows_2_summay_data(self, rows):
        attr_dict_list = []
        def_list = ["analysis_rc_id", "definition_id", "arl_id", "seq_diagram",
                    "job_status", "user_name", "job_status_name", self.id_col]
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(def_list):
                attr_dict[def_list[i]] = row[i]
                i += 1
            analysis_rc_id = row[0]
            attr_dict['title'] = '要件分析: ' + attr_dict.get(self.id_col)
            sequence_list = self._get_sequence(self._pg, analysis_rc_id)
            sequence_str = self._sequence_list_2_str(sequence_list)
            attr_dict["sequence_list"] = sequence_str
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def _get_summary_user_list(self, condition_str, params, like_condition):
        if like_condition:
            like_condition = "WHERE t4.%s" % like_condition
        sqlcmd = """
        SELECT DISTINCT t1.user_id, t5.user_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
               %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        inner join spec.analysis as t4
        on t3.definition_id = t4.definition_id
        LEFT JOIN spec.arl_user t5
        on t1.user_id = t5.user_id
        left join spec.arl_job_status as t6
        on t4.job_status = t6.job_status_id
        %s
        ORDER BY t5.user_name
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

    def get_model_list(self, pg, record_id):
        model_list = []
        for model_id, model, val, order_no, analysis_rc_id in self._get_model_list(pg, record_id):
            model_dict = dict()
            model_dict["order_no"] = order_no
            model_dict["model_id"] = model_id
            model_dict["val"] = val
            model_dict["analysis_rc_id"] = analysis_rc_id
            model_list.append(model_dict)
        return model_list

    def _get_model_list(self, pg, _id):
        sqlcmd = """
        SELECT model, a.model_id, a.val, a.order_no, a.analysis_rc_id
          FROM spec.analysis_model_rel as a
          LEFT JOIN spec.analysis_model_type as b
          ON a.model_id = b.model_id
          WHERE analysis_rc_id = %s
          ORDER BY order_no
        """
        pg.connect()
        pg.execute(sqlcmd, (_id,))
        rows = pg.fetchall()
        for row in rows:
            model, model_id, val, orderno, analysis_rc_id = row[0], row[1], row[2], row[3], row[4]
            model = json.loads(model)
            i = len(model)
            while i:
                if not model[i - 1]:
                    i -= 1
                else:
                    break
            yield model_id, model[:i], val, orderno, analysis_rc_id

    def delete(self, pg, def_id):
        sqlcmd1 = """
        -- delete model list
        DELETE FROM spec.analysis_model_rel
          where analysis_rc_id in (
            select analysis_rc_id
              from spec.analysis
              where definition_id = %s
          );
        """
        sqlcmd2 = """
        -- delete content
        DELETE FROM spec.analysis
         WHERE definition_id = %s;
        """
        pg.execute(sqlcmd1, (def_id,))
        pg.execute(sqlcmd2, (def_id,))
        if pg.pgcur.rowcount > 0:
            return True
        return False

    def get_all_model_types(self, pg):
        return self._get_all_model_types(pg)

    def _get_all_model_types(self, pg):
        sqlcmd = """
        SELECT model_id, model
          FROM spec.analysis_model_type
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
            model_dict["model"] = model
            model_info_dict[model_id] = model_dict
        return model_info_dict

    def get_arl_by_id_for_diff(self, pg, arl_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

    def category_model_list(self, model_list):
        """model list分类"""
        forest_model = []
        for model_dict in model_list:
            sub_list = forest_model
            model = model_dict.get("model")
            changed = model_dict.get("changed")
            model_id = model_dict.get("model_id")
            old_val = model_dict.get("old_val")
            val = model_dict.get("val")
            while '' in model:
                model.remove('')
            while None in model:
                model.remove(None)
            for i in range(len(model)):
                found_model_dict = dict()
                for temp_model_dict in sub_list[::-1]:
                    if model[i] == temp_model_dict.get("name"):
                        found_model_dict = temp_model_dict
                        break
                if not found_model_dict:
                    found_model_dict = {"name": model[i], "sub_list": []}
                    if i == len(model) - 1:
                        found_model_dict["changed"] = changed
                        found_model_dict["model_id"] = model_id
                        found_model_dict["old_val"] = old_val
                        found_model_dict["val"] = val
                        found_model_dict.pop("sub_list")
                    sub_list.append(found_model_dict)
                sub_list = found_model_dict.get("sub_list")
        return forest_model

    def _add_sub(self, pg, data, update_time):
        point_out = PointOut(self.table_name)
        return point_out.add_list(pg, data.get(self.id_col), data.get("point_list"), update_time)

    def update_parent_lock_status(self, pg):
        from Source.spec2db_server.arl.def_server import DefRecord
        p = DefRecord()
        p.update_post_lock_status(pg)

    def check_seq_diagram(self, pg, seq_diagram, asta_filename):
        check_flag = False
        sqlcmd = """
            SELECT file_rc_id, seq_diagram FROM spec.arl_file_seq 
            WHERE file_rc_id in (SELECT record_id FROM spec.arl_file 
            WHERE file_name = %s 
            ORDER BY create_time DESC LIMIT 1)
            AND seq_diagram = %s
        """
        pg.execute(sqlcmd, (asta_filename, seq_diagram))
        rows = pg.fetchall()
        if rows:

            check_flag = True
        return check_flag

    def get_diagram_id(self, asta_filename):
        sqlcmd = """
                    SELECT record_id FROM spec.arl_file 
                    WHERE file_name = %s ORDER BY create_time DESC LIMIT 1
                """
        self._pg.connect()
        self._pg.execute(sqlcmd, (asta_filename,))
        row = self._pg.fetchone()
        return row[0]


