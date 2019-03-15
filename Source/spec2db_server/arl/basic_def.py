# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.def_server import DefRecord
from Source.spec2db_server.arl.point_out import PointOut
import json
from Source.spec2db_server.arl.basic_ana import BasicAnaRecord


class BasicDefRecord(DefRecord):
    def __init__(self):
        DefRecord.__init__(self)
        self.table_name = "basic_req_definition"
        self.key_col = "def_rc_id"
        self.id_col = "definition_id"
        self.other_table_name = "definition"
        self.sub_list_name = "analysis_list"
        self.parent_col_name = "hu_def_id"
        self.model_table_name = "basic_req_definition_model_rel"
        self.attr_list = ["def_rc_id",
                          "author_name", "hu_def_id", "definition_id",
                          "major_category", "medium_category", "small_category", "detail",
                          "unique_id", "exception", "dcu_meu",
                          "dcu_status", "dcu_trigger", "dcu_action", "meu_status", "meu_trigger", "meu_action",
                          "hu_remark",
                          "pf_status", "pf_trigger", "pf_action",
                          "remark", "notice", "rel_hal_design",
                          "rel_flow_diagram", "other_spec", "implementation",
                          "analysis", "unrequire", "new_date",
                          "reason", "translation_flag", "agree_flag",
                          "has_problem", "complete_flag", "md5_key",
                          "major_ver", "small_ver", "job_status", "update_time",
                          "basic_req", "rel_requirement", "lock_status", "user_id", "group_id"
                          ]
        self.other_attr_list = ["def_rc_id",
                          "author_name", "hu_def_id", "definition_id",
                          "unique_id", "exception", "dcu_meu",
                          "pf_status", "pf_trigger", "pf_action",
                          "remark", "notice", "rel_hal_design",
                          "rel_flow_diagram", "other_spec", "implementation",
                          "analysis", "unrequire", "new_date",
                          "reason", "translation_flag", "agree_flag",
                          "has_problem", "complete_flag", "md5_key",
                          "major_ver", "small_ver", "job_status", "update_time",
                          "basic_req", "rel_requirement", "lock_status"
                         ]
    def _get_model_list(self, pg, _id):
        sqlcmd = """
        SELECT model, a.model_id, a.val, a.order_no, a.def_rc_id
          FROM spec.basic_req_definition_model_rel as a
          LEFT JOIN spec.definition_model_type as b
          ON a.model_id = b.model_id
          WHERE def_rc_id = %s
          ORDER BY order_no
        """
        pg.connect()
        pg.execute(sqlcmd, (_id,))
        rows = pg.fetchall()
        for row in rows:
            model, model_id, val, order_no, def_rc_id = row[0], row[1], row[2], row[3], row[4]
            model = json.loads(model)
            yield model_id, model, val, order_no, def_rc_id

    def _get_summary_data_list(self, condition_str, params, like_condition, size, page, condition_basic_req):
        condition_str = condition_str.replace('user_id', 't2.user_id')
        str = condition_str
        sqlcmd = """ 

        SELECT t2.def_rc_id, t2.definition_id, t2.hu_def_id, t2.author_name,t2.rel_requirement,
            t2.basic_req,t2.user_id, t1.user_name
       FROM  spec.basic_req_definition as t2 
       left join spec.arl_user as t1 on t1.user_id = t2.user_id  
            {condition_str}
            {like_condition}
        UNION
           SELECT  t2.def_rc_id, t2.definition_id, t2.hu_def_id, t2.author_name, t2.rel_requirement,
                  t2.basic_req, t4.user_id, t1.user_name
           FROM    spec.definition as t2
          left join spec.hu as t3 on t2.hu_def_id = t3.hu_id
          left join spec.arl as t4 on t3.arl_id = t4.arl_id
          left join spec.arl_user as t1 on t4.user_id = t1.user_id
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
        s = "and  t2.basic_req <>''"
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
            attr_dict["def_rc_id"], attr_dict["definition_id"], attr_dict["hu_def_id"] = row[0:3]
            attr_dict["title"] = row[5]
            attr_dict["user_id"] = row[6]
            attr_dict["info"] = row[4]
            attr_dict["author_name"] = row[3]
            attr_dict["user_name"] = row[7]
            attr_dict_list.append(attr_dict)
        return attr_dict_list

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
        if not arl_dict.get("user_id"):
            arl_dict["user_id"] = self.get_user_id_by_arl_id(arl_dict["definition_id"])
        self.del_unkown_ch(arl_dict)
        if arl_dict:
            type_id = str(_id)
            if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                def_id = arl_dict.get("definition_id")
                point_obj = PointOut("def")
                point_list = point_obj.get_list_by_id(pg, def_id)
                arl_dict["point_list"] = point_list
                from Source.spec2db_server.arl.analysis_service import AnalysisRecord
                ana_obj = AnalysisRecord()
                arl_dict[self.sub_list_name] = ana_obj.get_by_id_deep(pg, _id)
                arl_user_id = arl_dict.get("user_id")
                # 设置权限控制
                control_list = self._get_procudure_control(pg, arl_user_id, user_id)
                self._set_procudure_control(arl_dict, control_list)
            else:
                def_id = arl_dict.get(self.id_col)
                point_obj = PointOut("def")
                point_list = point_obj.get_list_by_id(pg, def_id)
                arl_dict["point_list"] = point_list
                from Source.spec2db_server.arl.basic_ana import BasicAnaRecord
                ana_obj = BasicAnaRecord()
                arl_dict[self.sub_list_name] = ana_obj.get_by_id_deep(pg, _id)
                arl_user_id = arl_dict.get("user_id")
                # 设置权限控制
                control_list = self._get_procudure_control(pg, arl_user_id, user_id)
                self._set_procudure_control(arl_dict, control_list)
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

    def get_by_id_deep(self, pg, _id):
        """
        :param _id:  arl_id
        :return:
        """
        if not _id:
            return []
        _, def_data_list = self.get_definition_by_hu_id_deep(pg, _id)
        from Source.spec2db_server.arl.basic_ana import BasicAnaRecord
        analysis_obj = BasicAnaRecord()
        for data_dict in def_data_list:
            def_id = data_dict.get(self.id_col)
            point_obj = PointOut(self.table_name)
            point_list = point_obj.get_list_by_id(pg, def_id)
            data_dict["point_list"] = point_list
            data_dict[self.sub_list_name] = analysis_obj.get_by_id_deep(pg, def_id)
        return def_data_list

    def get_definition_by_hu_id_deep(self, pg, hu_id):
        """
        :param _id:  arl_id
        :return:
        """
        if not hu_id:
            return []
        condition_col_list = ["hu_def_id"]
        order_cols = [self.id_col]
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, condition_col_list, order_cols)
        # offset = size * (page - 1)
        pg.execute(sqlcmd, (hu_id,))
        rowcount = pg.pgcur.rowcount
        rows = pg.fetchall()
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(row):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            def_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件定義: ' + attr_dict[self.id_col]
            pf_status = attr_dict.pop("pf_status")
            pf_trigger = attr_dict.pop("pf_trigger")
            pf_action = attr_dict.pop("pf_action")
            dcu_meu = attr_dict.get("dcu_meu")
            sequence_list = self._get_pf_sequence(pg, dcu_meu, pf_status, pf_trigger, pf_action, def_rc_id)
            attr_dict["sequence_list"] = sequence_list
            attr_dict_list.append(attr_dict)
        return rowcount, attr_dict_list

    def del_unkown_ch(self, data):
        for key, val in data.iteritems():
            if type(val) in (str, unicode):
                data[key] = val.replace(u'_x000D_', u'')

    def get_by_id(self, pg, _id, col_list):
        type_id = str(_id)
        if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
            sqlcmd = self.list_2_select_sql(self.other_table_name, self.other_attr_list, [self.id_col])
        else:
            sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, [_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            if type_id[0]!='B' and type_id[0]!='C' and type_id[0]!='D':
                while i < len(self.other_attr_list):
                    attr_dict[self.other_attr_list[i]] = row[i]
                    i += 1
            else:
                while i < len(col_list):
                    attr_dict[col_list[i]] = row[i]
                    i += 1
            def_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件定義: ' + attr_dict[self.id_col]
            pf_status = attr_dict.pop("pf_status")
            pf_trigger = attr_dict.pop("pf_trigger")
            pf_action = attr_dict.pop("pf_action")
            dcu_meu = attr_dict.get("dcu_meu")
            sequence_list = self._get_pf_sequence(pg, dcu_meu, pf_status, pf_trigger, pf_action, def_rc_id)
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
        # hu_info["control_list"] = control_list
        # for def_info in arl_dict.get("definition_list"):
        #     def_info["control_list"] = control_list
        for analysis_info in arl_dict.get("analysis_list"):
            analysis_info["control_list"] = control_list

    def get_arl_by_id_for_diff(self, pg, arl_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

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

    def _add_sub(self, pg, data, update_time):
        def_id = data.get(self.id_col)
        ana_data_list = data.get(self.sub_list_name)
        ana_obj = BasicAnaRecord()
        sub_log_list = ana_obj.add_list(pg, def_id, ana_data_list, update_time)
        if sub_log_list is None:
            return None
        point_out = PointOut(self.table_name)
        po_log_list = point_out.add_list(pg, data.get(self.id_col), data.get("point_list"), update_time)
        if po_log_list is None:
            return None
        return sub_log_list + po_log_list

    def _delete_sub(self, pg, hu_id, update_time):
        analysis_obj = BasicAnaRecord()
        sub_log_list = analysis_obj.delete_by_parent(pg, hu_id, update_time)
        return sub_log_list

    def delete_by_parent(self, pg, parent_id, update_time):
        old_data_list = self._get_by_parent_id(pg, parent_id)
        new_data = None
        log_list = []
        for old_data in old_data_list:
            log_list = self.common_add(pg, new_data, old_data, update_time, check_md5=False)
            if log_list is None:
                return None
        return log_list

    def _sequence_2_model_list(self, data_dict):
        sequence_list = data_dict.pop("sequence_list")
        pf_dict, model_list = self._parser_sequence_list(sequence_list)
        data_dict.update(pf_dict)
        data_dict["model_list"] = model_list

    def delete(self, pg, def_id):
        sqlcmd1 = """
        -- delete model list
        DELETE FROM spec.basic_req_definition_model_rel
          where def_rc_id in (
            select def_rc_id
              from spec.basic_req_definition
              where definition_id = %s
          );
        """
        sqlcmd2 = """
        -- delete content
        DELETE FROM spec.basic_req_definition
         WHERE definition_id = %s;
        """
        pg.execute(sqlcmd1, (def_id,))
        pg.execute(sqlcmd2, (def_id,))
        if pg.pgcur.rowcount > 0:
            return True
        return False
