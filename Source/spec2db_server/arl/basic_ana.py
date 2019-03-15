# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.analysis_service import AnalysisRecord
from Source.spec2db_server.arl.point_out import PointOut
import json
class BasicAnaRecord(AnalysisRecord):
    def __init__(self):
        AnalysisRecord.__init__(self)
        self.table_name = "basic_req_analysis"
        self.model_table_name = "basic_req_analysis_model_rel"
        self.key_col = "analysis_rc_id"
        self.id_col = "analysis_id"
        self.other_table_name = "analysis"
        self.parent_col_name = "definition_id"
        self.attr_list = ["analysis_rc_id", "author_name", "definition_id",
                          "major_category", "medium_category", "small_category", "detail",
                          "dcu_meu", "pf_status", "pf_trigger", "pf_action",
                          "unique_id", "exception", "seq_diagram",
                          "supple_spec", "uncheck", "remark",
                          "user_id", "update_time", "ana_1", "ana_2", "ana_3", "ana_4",
                          "translation_flag", "agree_flag", "has_problem",
                          "new_date", "reason", "complete_flag",
                          "major_ver", "md5_key", "small_ver",
                          "job_status", "asta_filename", "basic_req",
                          "rel_requirement", "lock_status", "group_id",
                          "analysis_id"
                          ]
        self.other_attr_list = ["analysis_rc_id", "author_name", "definition_id",
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
    def _get_model_list(self, pg, _id):
        sqlcmd = """
        SELECT model, a.model_id, a.val, a.order_no, a.analysis_rc_id
          FROM spec.basic_req_analysis_model_rel as a
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

    def _get_summary_data_list(self, condition_str, params, like_condition, size, page, condition_basic_req):
        condition_str = condition_str.replace('user_id', 't2.user_id')
        str = condition_str
        sqlcmd = """ 
           SELECT t2.analysis_rc_id, t2.definition_id, t2.author_name, t2.rel_requirement,
                  t2.basic_req, t2.user_id, t1.user_name, t2.analysis_id
           FROM  spec.basic_req_analysis as t2
           left join spec.arl_user as t1 on t1.user_id = t2.user_id  
                {condition_str}
                {like_condition}
            UNION
            SELECT  t2.analysis_rc_id, t2.definition_id, t2.author_name, t2.rel_requirement,
                    t2.basic_req, t5.user_id, t1.user_name, t2.analysis_id
              FROM  spec.analysis as t2
             left join spec.definition as t3 on t2.definition_id = t3.definition_id
             left join spec.hu as t4 on t3.hu_def_id = t4.hu_id
             left join spec.arl as t5 on t4.arl_id = t5.arl_id
             left join spec.arl_user as t1 on t5.user_id = t1.user_id
             {condition_str}
             {like_condition}
             {condition_basic_req}
             ORDER BY definition_id
        """.format(condition_str=str, condition_basic_req=condition_basic_req, like_condition=like_condition)
        self._pg.connect()
        rowcount, rows = self._basic_fetch_many(self._pg, sqlcmd, params, size, page)
        attr_dict_list = self._rows_basic_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    # def _get_basic_summay_condition_str(self, condition_data):
    #     condition_dict = condition_data.get("condition")
    #     other_cols, other_vals = [], []
    #
    #     for col, val in condition_dict.items():
    #         if val:
    #             other_cols.append(col)
    #             other_vals.append(val)
    #
    #     like_condition_dict = condition_data.get("like_condition")
    #     like_condition = self.get_filter_condition(like_condition_dict)
    #     return condition, params + other_vals, like_condition


    def summay_for_all(self, condition_data):
        record = {"result": "NG"}
        count, record["content"] = self._summay_for_all(condition_data)
        if record["content"]:
            record["total_count"] = count
            record["result"] = "OK"
        return record

    def _summay_for_all(self, condition_data):
        size = condition_data.get("size")
        page = condition_data.get("page")
        condition_str, params, like_condition, complete_str, condition_basic_req = self._get_summay_basic_condition_str(
            condition_data)
        return self._get_summary_data_list(condition_str, params, like_condition, size, page, condition_basic_req)

    def _get_summay_basic_condition_str(self, condition_data):
        condition_dict = condition_data.get("condition")
        condition, params = '', []
        if "category_id" in condition_dict:
            category_id = condition_dict.pop("category_id")
            cat_id_list = [int(n) for n in category_id.split('-')]
            condition, params = self.get_category_condition(cat_id_list)
        other_cols, other_vals = [], []
        date_condition, date_params = self._date_condition_2_str(condition_dict, 'update_time')
        params += date_params
        if date_condition:
            if condition:
                condition += ' and ' + date_condition
            else:
                condition += 'WHERE ' + date_condition
        complete_str = self._complete_condition_2_str(condition_dict.get("complete"))
        for col, val in condition_dict.items():
            if col in ("category_id", "start_date", "end_date", "complete"):
                continue
            if val:
                other_cols.append(col)
                other_vals.append(val)
        like_condition_dict = condition_data.get("like_condition")
        if other_cols:
            if condition:
                condition += ' and ' + self.list_2_condition_str(other_cols, False)
            else:
                condition = self.list_2_condition_str(other_cols, True)
        if len(other_cols) != 0:
            condition_basic_req = self.get__basic_condition_basic_req()
            like_condition = self.get__basic_filter_condition(like_condition_dict)
        else:
            if like_condition_dict:
                like_condition = self.get__basic_2_filter_condition(like_condition_dict)
                condition_basic_req = self.get__basic_condition_basic_req()
            else:
                like_condition = ''
                condition_basic_req = self.get__basic_condition_2_basic_req()

        return condition, params + other_vals, like_condition, complete_str, condition_basic_req

    def get__basic_condition_basic_req(self):
        cond_list = []
        s = "and t2.basic_req <>''"
        cond_list.append(s)
        return ' and '.join(cond_list)

    def get__basic_condition_2_basic_req(self):
        cond_list = []
        s = "WHERE t2.basic_req <>''"
        cond_list.append(s)
        return ' and '.join(cond_list)

    def get__basic_filter_condition(self, filter_dict):
        cond_list = []
        if filter_dict:
            for key, val in filter_dict.iteritems():
                if key and val:
                    val = val.replace('.', '\\.')
                    s = "and t2." + key + """ like '%%""" + val + """%%'"""
                    cond_list.append(s)
        return ' and '.join(cond_list)

    def get__basic_2_filter_condition(self, filter_dict):
        cond_list = []
        if filter_dict:
            for key, val in filter_dict.iteritems():
                if key and val:
                    val = val.replace('.', '\\.')
                    s = "where t2." + key + """ like '%%""" + val + """%%'"""
                    cond_list.append(s)
        return ' and '.join(cond_list)

    def _basic_fetch_many(self, pg, sqlcmd, params, size, page):
        offset = size * (page - 1)
        pg.execute(sqlcmd, params+params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            pg.pgcur.scroll(offset)
        rows = pg.pgcur.fetchmany(size)
        return rowcount, rows

    def _rows_basic_summay_data(self, rows):
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            attr_dict["analysis_rc_id"], attr_dict["definition_id"] = row[0:2]
            attr_dict["title"] = row[4]  # Basic REQ
            attr_dict["user_id"] = row[5]
            attr_dict["info"] = row[3]  # rel_requirement关联要件
            attr_dict["author_name"] = row[2]
            attr_dict["user_name"] = row[6]
            attr_dict["analysis_id"] = row[7]
            attr_dict_list.append(attr_dict)
        return attr_dict_list

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

    def _get_by_basic_id_deep(self, pg, _id, user_id, group_id):
        """
        :param pg: 
        :param _id: 
        :return: 
        """""
        if not _id:
            return []
        info_list = []
        arl_dict = self.get_by_id(pg, _id, self.attr_list)
        if arl_dict:
            if not arl_dict.get("user_id"):
                arl_dict["user_id"] = self.get_user_id_by_arl_id(arl_dict["definition_id"])
            self.del_unkown_ch(arl_dict)
            if arl_dict:
                type_id = str(_id)
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    point_obj = PointOut("analysis")
                    point_list = point_obj.get_list_by_id(pg, _id)
                    arl_dict["point_list"] = point_list
                    arl_user_id = arl_dict.get("user_id")
                    # # 设置权限控制
                    control_list = self._get_procudure_control(pg, arl_user_id, user_id)
                    arl_dict["control_list"] = control_list
                    # self._set_procudure_control(arl_dict, control_list)
                else:
                    point_obj = PointOut(self.table_name)
                    point_list = point_obj.get_list_by_id(pg, _id)
                    arl_dict["point_list"] = point_list
                    arl_user_id = arl_dict.get("user_id")
                    # # 设置权限控制
                    control_list = self._get_procudure_control(pg, arl_user_id, user_id)
                    arl_dict["control_list"] = control_list
                    # self._set_procudure_control(arl_dict, control_list)
            info_list.append(arl_dict)
        return info_list

    def get_user_id_by_arl_id(self, id):
        sqlcmd = """ 
                 SELECT  t3.user_id
                 FROM    spec.hu as t2
                left join spec.arl_user as t1 on t1.user_id = t2.user_id
                left join spec.arl as t3 on t2.arl_id = t3.arl_id
                left join spec.definition as t4 on t4.hu_def_id = t2.hu_id
                where  definition_id = %s
                ORDER BY definition_id

                """
        self._pg.connect()
        self._pg.execute(sqlcmd, (id,))
        row = self._pg.fetchone()
        return row[0]

    def get_by_def_id(self, pg, def_id):
        """
        :param def_id:  definition id
        :return:
        """
        if not def_id:
            return []
        condition_col_list = [self.parent_col_name]
        order_cols = [self.id_col]
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

    def get_arl_by_id_for_diff(self, pg, _id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

    def del_unkown_ch(self, data):
        for key, val in data.iteritems():
            if type(val) in (str, unicode):
                data[key] = val.replace(u'_x000D_', u'')

    def get_by_id(self, pg, _id, col_list):
        type_id = str(_id)
        if type_id[0] not in ('B', 'C', 'D'):
            sqlcmd = self.list_2_select_sql(self.other_table_name, self.other_attr_list, [self.id_col])
        else:
            sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, [_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            if type_id[0] not in ('B', 'C', 'D'):
                while i < len(self.other_attr_list):
                    attr_dict[self.other_attr_list[i]] = row[i]
                    i += 1
            else:
                while i < len(col_list):
                    attr_dict[col_list[i]] = row[i]
                    i += 1
            analysis_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件分析: ' + attr_dict.get(self.id_col)
            sequence_list = self._get_sequence(pg, analysis_rc_id)
            attr_dict["sequence_list"] = sequence_list
        return attr_dict

    def list_2_select_sql(self, table_name, col_list, condition_col_list, order_col_list=None):
        strcolumn = self.list_2_col_str(col_list)
        condition_str = self.list_2_condition_str(condition_col_list)
        order_str = self.list_2_order_str(order_col_list)
        sqlcmd = """
           SELECT {strcolumn} \n FROM spec.{table} \n {condition_str} \n{order_str};
           """.format(table=table_name,
                      strcolumn=strcolumn,
                      condition_str=condition_str,
                      order_str=order_str)
        return sqlcmd

    def list_2_col_str(self, col_list):
        strcolumn = ''
        new_keys = []
        for i, key in enumerate(col_list, 1):
            if (i % 4) == 0:
                new_keys.append(key + '\n')
            else:
                new_keys.append(key)
        strcolumn = ', '.join(new_keys)
        strcolumn += " "
        return strcolumn

    def list_2_condition_str(self, col_list, where=True):
        strlist = ''
        if col_list:
            if where:
                strlist += 'WHERE '
        new_keys = []
        for i, key in enumerate(col_list, 1):
            if (i % 4) == 0:
                new_keys.append(key + ' = %s\n')
            else:
                new_keys.append(key + ' = %s')
        strlist += ' and '.join(new_keys)
        strlist += " "
        return strlist

    def list_2_order_str(self, col_list):
        order_str = ''
        if col_list:
            order_str = ', '.join(col_list)
            order_str = 'ORDER BY ' + order_str
        return order_str

    def _set_procudure_control(self, arl_dict, control_list):
        arl_dict["control_list"] = control_list
        # for hu_info in arl_dict.get("hu_list"):
        #     hu_info["control_list"] = control_list
        #     for def_info in hu_info.get("definition_list"):
        #         def_info["control_list"] = control_list
        # for analysis_info in arl_dict.get("analysis_list"):
        # arl_dict["control_list"] = control_list

    def _get_procudure_control(self, pg, arl_user_id, curr_user_id):
        """取得流程控制权限
        :param arl_user_id:
        :param curr_user_id:
        :return: []
        """
        sqlcmd = """
           SELECT role, array_agg(job_status_id)
             FROM (
               SELECT DISTINCT t2.role, job_status_id
                 FROM (
                   SELECT group_id, user_id, role, role_id
                     FROM spec.arl_group_member
                     where user_id = %s
                     ORDER BY user_id
                 ) as t1
                 left join spec.arl_role_power as t2
                 on t1.role_id = t2.role_id
                 LEFT JOIN spec.arl_procudure_control as t3
                 ON t2.role_id = t3.role_id
                 ORDER BY t2.role, job_status_id
             ) as tt1
             group by role
           """
        pg.execute(sqlcmd, [curr_user_id])
        rows = pg.fetchall()
        role_set = set()
        control_set = set()
        if rows:
            for row in rows:
                role, job_status_ids = row[0], row[1]
                role_set.add(role)
                control_set.update(job_status_ids)
        if role_set:
            if role_set == set(["Member"]):
                if arl_user_id != curr_user_id:
                    return []
        return sorted(control_set)

    def _sequence_2_model_list(self, data_dict):
        sequence_list = data_dict.pop("sequence_list")
        model_list = self._parser_sequence_list(sequence_list)
        data_dict["model_list"] = model_list

    def delete(self, pg, def_id):
        sqlcmd1 = """
        -- delete model list
        DELETE FROM spec.basic_req_analysis_model_rel
          where analysis_rc_id in (
            select analysis_rc_id
              from spec.basic_req_analysis
              where definition_id = %s
          );
        """
        sqlcmd2 = """
        -- delete content
        DELETE FROM spec.basic_req_analysis
         WHERE definition_id = %s;
        """
        pg.execute(sqlcmd1, (def_id,))
        pg.execute(sqlcmd2, (def_id,))
        if pg.pgcur.rowcount > 0:
            return True
        return False
