# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import json
import re
from Source.spec2db_server.common import db
from Source.spec2db_server.arl.arl_base import ServiceBase
from Source.spec2db_server.arl.analysis_service import AnalysisRecord
from Source.spec2db_server.arl.point_out import PointOut


class DefRecord(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "definition"
        self.model_table_name = "definition_model_rel"
        self.model_type_table_name = "definition_model_type"
        self.key_col = "def_rc_id"
        self.id_col = "definition_id"
        self.sub_list_name = "analysis_list"
        self.parent_col_name = "hu_def_id"
        self.child_id_col = self.id_col
        self.attr_list = ["def_rc_id",
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
        self.lock_list = ["pf_status", "pf_trigger", "pf_action"]

    def get_by_category2(self, category_id, size, page, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, arl_record["content"] = self.get_by_categorysql(cat_id_list, size, page, user_id)
        if arl_record["content"]:
            arl_record["total_count"] = count
            arl_record["result"] = "OK"
        return arl_record

    def get_by_categorysql(self, cat_id_list, page_size, page_number, user_id=None):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        sqlcmd = """
        SELECT def_rc_id, t3."definition_id", t3."dcu_meu",
               t3."pf_status", t3."pf_trigger", t3."pf_action",
               t3.job_status, t4.user_name, t2.arl_id,
               t5.job_status as job_status_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        LEFT JOIN spec.arl_user t4
        on t1.user_id = t4.user_id
        left join spec.arl_job_status as t5
        on t3.job_status = t5.job_status_id
        ORDER BY length(t3."definition_id"), t3."definition_id"
        """ % condition
        self._pg.connect()
        offset = page_size * (page_number - 1)
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(page_size)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def get_by_categorysql3(self, cat_id_list, filter_dict, user_id):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        filter_cond = self.get_filter_condition(filter_dict)
        if filter_cond:
            filter_cond = "WHERE %s" % filter_cond
        sqlcmd = """
        SELECT def_rc_id, t3."definition_id", t3."dcu_meu",
               t3."pf_status", t3."pf_trigger", t3."pf_action",
               t3.job_status, t4.user_name, t2.arl_id,
               t5.job_status as job_status_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        LEFT JOIN spec.arl_user t4
        on t1.user_id = t4.user_id
        left join spec.arl_job_status as t5
        on t3.job_status = t5.job_status_id
        %s
        ORDER BY length(t3."definition_id"), t3."definition_id"
        """ % (condition, filter_cond)
        # def_list = ["def_rc_id", "definition_id", "dcu_meu",
        #             "pf_status", "pf_trigger", "pf_action"]
        self._pg.connect()
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        rows = self._pg.fetchall()
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _get_summary_data_list(self, condition_str, params, like_condition, complete_str, size, page):
        if like_condition:
            like_condition = "WHERE %s" % like_condition
        if complete_str == '2':
            child_str = """
            LEFT JOIN spec.arl_schedule as sdl
            ON t1.arl_id = sdl.arl_id
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
                ) as com
            on t1.arl_id = com.arl_id
            """
        elif complete_str:
            child_str = """
            LEFT JOIN spec.arl_schedule as sdl
            ON t1.arl_id = sdl.arl_id
            LEFT JOIN spec.analysis as child
            ON t3.definition_id = child.definition_id
            """
            if like_condition:
                like_condition += 'and ' + complete_str + " and analysis_date <> '-'"
            else:
                like_condition = 'where ' + complete_str + " and analysis_date <> '-'"
        else:
            child_str = ""
        sqlcmd = """
        SELECT distinct def_rc_id, t3."definition_id", t3."dcu_meu",
               t3."pf_status", t3."pf_trigger", t3."pf_action",
               t3.job_status, t4.user_name, t2.arl_id, t1.update_time,
               t5.job_status as job_status_name, length(t3."definition_id") as len
          FROM (
            SELECT arl_id, user_id, update_time
              FROM spec.arl 
              {condition_str}
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        LEFT JOIN spec.arl_user t4
        on t1.user_id = t4.user_id
        left join spec.arl_job_status as t5
        on t3.job_status = t5.job_status_id
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
            def_rc_id, definition_id = row[0:2]
            attr_dict['title'] = '要件定義: ' + definition_id
            attr_dict['definition_id'] = definition_id
            dcu_meu, pf_status, pf_trigger, pf_action = row[2:6]
            attr_dict['job_status'], attr_dict['user_name'] = row[6:8]
            attr_dict['arl_id'] = row[8]
            attr_dict['job_status_name'] = row[9]
            sequence_list = self._get_pf_sequence(self._pg, dcu_meu, pf_status, pf_trigger, pf_action, def_rc_id)
            sequence_str = self._sequence_list_2_str(sequence_list)
            attr_dict["sequence_list"] = sequence_str
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def _get_summary_user_list(self, condition_str, params, like_condition):
        if like_condition:
            like_condition = "WHERE %s" % like_condition
        sqlcmd = """
        SELECT DISTINCT t1.user_id, t4.user_name
          FROM (
            SELECT arl_id, user_id
              FROM spec.arl 
              %s
        ) as t1
        INNER JOIN spec.hu as t2
        ON t1.arl_id = t2.arl_id
        inner join spec.definition t3
        on t2.hu_id = t3.hu_def_id
        LEFT JOIN spec.arl_user t4
        on t1.user_id = t4.user_id
        left join spec.arl_job_status as t5
        on t3.job_status = t5.job_status_id
        %s
        ORDER BY t4.user_name
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

    def _get_parent_version(self, pg, data):
        hu_id = data.get(self.parent_col_name)
        from Source.spec2db_server.arl.hu_server import HuRecord
        hu_obj = HuRecord()
        parent_ver_dict = hu_obj.get_version(pg, hu_id)
        return parent_ver_dict

    def _get_model_list(self, pg, _id):
        sqlcmd = """
        SELECT model, a.model_id, a.val, a.order_no, a.def_rc_id
          FROM spec.definition_model_rel as a
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

    def get_by_id_deep(self, pg, _id):
        """
        :param _id:  arl_id
        :return:
        """
        if not _id:
            return []
        _, def_data_list = self.get_definition_by_hu_id_deep(pg, _id)
        from Source.spec2db_server.arl.analysis_service import AnalysisRecord
        analysis_obj = AnalysisRecord()
        for data_dict in def_data_list:
            def_id = data_dict.get(self.id_col)
            point_obj = PointOut("DEF")
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
        order_cols = ["length(%s)"%self.id_col, self.id_col]
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

    def get_by_id(self, definition_id):
        result = {"result": "NG"}
        self._pg.connect()
        data_dict = self._get_by_id(self._pg, definition_id)
        if data_dict:
            result["content"] = data_dict
            result["result"] = "OK"
        self._pg.close()
        return result

    def _get_by_id(self, pg, definition_id):
        """
        :param _id:  arl_id
        :return:
        """
        if not definition_id:
            return re
        condition_col_list = [self.id_col]
        # order_cols = [self.id_col]
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, condition_col_list)
        pg.execute(sqlcmd, (definition_id,))
        rowcount = pg.pgcur.rowcount
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            for i, col in enumerate(self.attr_list, 0):
                attr_dict[col] = row[i]
            def_rc_id = row[0]
            attr_dict['title'] = 'TAGL要件定義:' + attr_dict[self.id_col]
            pf_status = attr_dict.pop("pf_status")
            pf_trigger = attr_dict.pop("pf_trigger")
            pf_action = attr_dict.pop("pf_action")
            dcu_meu = attr_dict.get("dcu_meu")
            sequence_list = self._get_pf_sequence(pg, dcu_meu, pf_status, pf_trigger, pf_action, def_rc_id)
            attr_dict["sequence_list"] = sequence_list
        return attr_dict

    def _get_pf_sequence(self, pg, dcu_meu, pf_status, pf_trigger, pf_action, def_rc_id):
        sequence_list, ref_base_list = [], []
        pf_sequence_dict, ref_base_list = self._split_dcu_meu_seq(dcu_meu, pf_status, pf_trigger, pf_action)
        device_sequence_dict, dev_ref_base = self._get_device_seq(pg, def_rc_id)   # 设备(model_list)
        ref_base_list += dev_ref_base
        seq_id_list = pf_sequence_dict.keys() + device_sequence_dict.keys()
        seq_id_list = sorted(set(seq_id_list))
        for seq_id in seq_id_list:
            sequence = pf_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
            sequence = device_sequence_dict.get(seq_id)
            if sequence:
                sequence_list.append(sequence)
        sequence_list += ref_base_list
        return sequence_list

    def get_all_model_types(self, pg):
        return self._get_all_model_types(pg)

    def _get_all_model_types(self, pg):
        sqlcmd = """
        SELECT model_id, model
          FROM spec.definition_model_type
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
            model_dict["category"] = model[0]  # 抽象デバイス
            model_dict["name"] = model[-1]
            model_dict["title"] = model[-1]
            model_info_dict[model_id] = model_dict
        return model_info_dict

    def delete_by_parent(self, pg, parent_id, update_time):
        old_data_list = self._get_by_parent_id(pg, parent_id)
        new_data = None
        log_list = []
        for old_data in old_data_list:
            log_list = self._common_add(pg, new_data, old_data, update_time, check_md5=False)
            if log_list is None:
                return None
        return log_list

    def _add_sub(self, pg, data, update_time):
        def_id = data.get(self.id_col)
        def_data_list = data.get(self.sub_list_name)
        analysis_obj = AnalysisRecord()
        sub_log_list = analysis_obj.add_list(pg, def_id, def_data_list, update_time)
        if sub_log_list is None:
            return None
        point_out = PointOut("DEF")
        po_log_list = point_out.add_list(pg, data.get(self.id_col), data.get("point_list"), update_time)
        if po_log_list is None:
            return None
        return sub_log_list + po_log_list

    def _delete_sub(self, pg, hu_id, update_time):
        analysis_obj = AnalysisRecord()
        sub_log_list = analysis_obj.delete_by_parent(pg, hu_id, update_time)
        return sub_log_list

    def _sequence_2_model_list(self, data_dict):
        sequence_list = data_dict.pop("sequence_list")
        pf_dict, model_list = self._parser_sequence_list(sequence_list)
        data_dict.update(pf_dict)
        data_dict["model_list"] = model_list

    def _parser_sequence_list(self, sequence_list):
        pf_sequence_dict, device_sequence_dict = dict(), dict()
        dcu_meu = '-'
        for seq_id, seq_dict in enumerate(sequence_list, 1):
            _type = seq_dict.get("type")
            if _type in ('DCU', 'MEU', 'DCU/MEU'):
                pf_sequence_dict[seq_id] = seq_dict
                dcu_meu = _type
            elif _type == "DEVICE":
                device_sequence_dict[seq_id] = seq_dict
            else:
                print 'DEF sequence type error: %s' % _type
        pf_dict = self._merger_pf_sequence(pf_sequence_dict, 'PF')
        pf_dict["dcu_meu"] = dcu_meu
        model_list = self._merger_device_sequence(device_sequence_dict)
        return pf_dict, model_list

    def _merger_pf_sequence(self, sequence_dict, _type):
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
        return {"pf_status": status, "pf_trigger": trigger, "pf_action": action}

    def get_arl_by_id_for_diff(self, pg, arl_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

    def delete(self, pg, def_id):
        sqlcmd1 = """
        -- delete model list
        DELETE FROM spec.definition_model_rel
          where def_rc_id in (
            select def_rc_id
              from spec.definition
              where definition_id = %s
          );
        """
        sqlcmd2 = """
        -- delete content
        DELETE FROM spec.definition
         WHERE definition_id = %s;
        """
        pg.execute(sqlcmd1, (def_id,))
        pg.execute(sqlcmd2, (def_id,))
        if pg.pgcur.rowcount > 0:
            return True
        return False

    def update_post_lock_status(self, pg):
        sqlcmd = """
        -- 清空转记锁
        update spec.definition as t1 set lock_status = 0
          from (
            SELECT distinct a.definition_id
              FROM spec.definition as a
              left join spec.analysis as b
              on a.definition_id = b.definition_id and b.lock_status = 1
              where b.definition_id is null and a.lock_status = 2
          ) as t2
          where t1.definition_id = t2.definition_id
        """
        pg.execute(sqlcmd)

    def update_parent_lock_status(self, pg):
        from Source.spec2db_server.arl.hu_server import HuRecord
        p = HuRecord()
        p.update_post_lock_status(pg)


def main():
    obj = DefRecord()
    obj._pg.connect()
    result = obj.get_all_model_types(obj._pg)
    return result

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
