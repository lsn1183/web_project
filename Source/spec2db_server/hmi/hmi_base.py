# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import time
import re
import json
import copy
from Source.spec2db_server.arl.arl_diff import ArlDiff
from Source.spec2db_server.common.db_access_base import DBAccessBase
from Source.spec2db_server.common import db
HMI_DEV_STATUS_NG = 16


class HMIBase(DBAccessBase):
    """
    """
    def __init__(self):
        DBAccessBase.__init__(self)
        self.table_name = ""
        self.model_table_name = ""
        self.model_type_table_name = ""
        self.key_col = ""
        self.id_col = ""
        self.attr_list = []
        self.sub_list_name = ""
        self.parent_col_name = ""
        self.child_id_col = ""
        self.db_schema = 'hmi'

    def fetch_id(self, pg=None):
        Id = 0
        if pg:
            row = pg.fetchone()
        else:
            row = self._pg.fetchone()
        if row:
            Id = row[0]
        return Id

    def list_2_select_sql(self, table_name, col_list, condition_col_list, order_col_list=None):
        strcolumn = self.list_2_col_str(col_list)
        condition_str = self.list_2_condition_str(condition_col_list)
        order_str = self.list_2_order_str(order_col_list)
        sqlcmd = """
        SELECT {strcolumn} \n FROM {db_schema}.{table} \n {condition_str} \n{order_str}
        """.format(table=table_name,
                   strcolumn=strcolumn,
                   condition_str=condition_str,
                   order_str=order_str,
                   db_schema=self.db_schema)
        return sqlcmd

    def list_2_insert_sql(self, table_name, col_list, key_col):
        strcolumn = self.list_2_col_str(col_list)
        pecent_str = self.percent_str(len(col_list))
        sqlcmd = """
        insert into {db_schema}.{table} ({strcolumn}) \n values({pecent_str}) returning {key_col};
        """.format(table=table_name,
                   strcolumn=strcolumn,
                   pecent_str=pecent_str,
                   key_col=key_col,
                   db_schema=self.db_schema)
        return sqlcmd

    def list_2_update_sql(self, table_name, update_col_list, condition_col_list, key_col):
        update_str = self.list_2_update_str(update_col_list)
        condition_str = self.list_2_condition_str(condition_col_list)
        sqlcmd = """
        update {db_schema}.{table} set {update_str} \n {condition_str} \nreturning {key_col};
        """.format(table=table_name,
                   update_str=update_str,
                   condition_str=condition_str,
                   key_col=key_col,
                   db_schema=self.db_schema)
        return sqlcmd

    def list_2_delete_sql(self, table_name, condition_col_list):
        condition_str = self.list_2_condition_str(condition_col_list)
        sqlcmd = """
        delete from {db_schema}.{table} {condition_str};
        """.format(table=table_name,
                   condition_str=condition_str,
                   db_schema=self.db_schema)
        return sqlcmd

    def list_2_col_str(self, col_list):
        strcolumn = ''
        new_keys = []
        for i, key in enumerate(col_list, 1):
            if key == "group":
                key = '"group"'
            if (i % 4) == 0:
                new_keys.append(key + '\n')
            else:
                new_keys.append(key)
        strcolumn = ', '.join(new_keys)
        strcolumn += " "
        return strcolumn

    def percent_str(self, col_num):
        pecent_list = []
        for i in range(1, col_num + 1):
            if i % 4 == 0:
                pecent_list.append('%s\n')
            else:
                pecent_list.append('%s')
        pecent_str = ', '.join(pecent_list)
        return pecent_str

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

    def list_2_update_str(self, col_list):
        strlist = ' '
        new_keys = []
        for i, key in enumerate(col_list, 1):
            if (i % 4) == 0:
                new_keys.append(key + ' = %s\n')
            else:
                new_keys.append(key + ' = %s')
        strlist += ', '.join(new_keys)
        strlist += ' '
        return strlist

    def get_category_condition(self, cat_id_list, user_id=None):
        cat_list = []
        for i in range(0, len(cat_id_list)):
            cat = "cat_id%s" % i
            cat = cat + ' = %s'
            cat_list.append(cat)
        condition = ' and '.join(cat_list)
        if user_id:
            condition = ' user_id = %s and ' + condition
            params = [user_id] + cat_id_list
        else:
            params = cat_id_list
        condition = ' WHERE ' + condition + ' and exclude_flag = False '
        return condition, params

    def get_filter_condition(self, filter_dict):
        cond_list = []
        if filter_dict:
            for key, val in filter_dict.iteritems():
                if key and val:
                    val = val.replace('.', '\\.')
                    s = key + """ like '%%""" + val + """%%'"""
                    cond_list.append(s)
        return ' and '.join(cond_list)

    def get_params(self, data, cols):
        params = []
        for col in cols:
            val = data.get(col)
            params.append(val)
        return params

    def convert2log(self, diff_result_list):
        log_list = []
        for diff_result in diff_result_list:
            log_dict = dict()
            record_id = diff_result.get(self.key_col)
            # log_dict["group_id"] = group_id
            log_dict["table_name"] = self.table_name
            log_dict["action"] = diff_result.get("action")
            log_dict["data"] = diff_result.get("data")
            log_dict["record_id"] = record_id
            log_dict["col_change_list"] = diff_result.get("col_change_list")
            # model_rel = []
            # for model_diff in diff_result.get("model_list"):
            #     model_dict = dict()
            #     model_dict["table_name"] = self.model_table_name
            #     model_dict["action"] = model_diff.get("action")
            #     model_dict["data"] = model_diff.get("data")
            #     record_id = model_diff.get("record_id")
            #     if record_id:
            #         model_dict["record_id"] = record_id
            #     else:
            #         model_dict["record_id"] = model_diff.get("data").get("order_no")
            #     model_dict["col_change_list"] = model_diff.get("col_change_list")
            #     model_rel.append(model_dict)
            # point_dict = diff_result.get("point_dict")
            # if point_dict:
            #     point_dict["table_name"] = "point_out"
            #     data = point_dict.get("data")
            #     point_dict["record_id"] = data.get("pointout_rc_id")
            #     log_dict["point_dict"] = point_dict
            # log_dict["model_rel"] = model_rel
            log_list.append(log_dict)
        return log_list

    def get_version(self, pg, _id):
        version = dict()
        col_list = ["major_ver", "small_ver"]
        sqlcmd = self.list_2_select_sql(self.table_name, col_list, [self.id_col])
        pg.execute(sqlcmd, (_id,))
        row = pg.fetchone()
        if row:
            for i, col in enumerate(col_list, 0):
                version[col] = row[i]
        else:
            for col in col_list:
                version[col] = None
        return version

    def update_version(self, data):
        return

    def check_md5_key(self, new_data, old_data):
        if not old_data:
            return True
        elif not new_data:
            return True
        else:
            old_md5 = old_data.get("md5_key")
            if old_md5 is None:
                old_md5 = ''
            curr_md5 = new_data.get("md5_key")
            if curr_md5 is None:
                curr_md5 = ''
            if old_md5 == curr_md5:
                return True
        return False

    def generate_md5_key(self, data):
        import hashlib
        m = hashlib.md5(str(data))
        return m.hexdigest()

    def get_by_category3(self, category_id, filter_dict, user_id):
        record = {"result": "NG"}
        if not category_id:
            return record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, record["content"] = self.get_by_categorysql3(cat_id_list, filter_dict, user_id)
        if record["content"]:
            record["total_count"] = count
            record["result"] = "OK"
        return record

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
        condition_str, params, like_condition, complete_str = self._get_summay_condition_str(condition_data)
        return self._get_summary_data_list(condition_str, params, like_condition, complete_str, size, page)

    def _get_summary_data_list(self, condition_str, params, like_condition, complete_str, size, page):
        return 0, []

    def summary_users(self, condition_data):
        record = {"result": "NG"}
        condition_str, params, like_condition, complete_str = self._get_summay_condition_str(condition_data)
        user_list = self._get_summary_user_list(condition_str, params, like_condition)
        if user_list:
            record["content"] = user_list
            record["result"] = "OK"
        return record

    def _get_summary_user_list(self, condition_str, params, like_condition):
        return 0, []

    def _get_summay_condition_str(self, condition_data):
        condition_dict = condition_data.get("condition")
        condition, params = '', []
        if "category_id" in condition_dict:
            category_id = condition_dict.pop("category_id")
            cat_id_list = [int(n) for n in category_id.split('-')]
            condition, params = self.get_category_condition(cat_id_list)
        if not condition:
            condition = ' WHERE exclude_flag = False '
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
        if other_cols:
            if condition:
                condition += ' and ' + self.list_2_condition_str(other_cols, False)
            else:
                condition = self.list_2_condition_str(other_cols, True)
        like_condition_dict = condition_data.get("like_condition")
        like_condition = self.get_filter_condition(like_condition_dict)
        return condition, params + other_vals, like_condition, complete_str

    def _complete_condition_2_str(self, complete):
        condition_2_str = ''
        if complete == "complete":
            condition_2_str = 'child.%s IS NOT NULL' % self.child_id_col
        elif complete == "incomplete":
            condition_2_str = 'child.%s IS NULL' % self.child_id_col
        elif complete == "work_complete":
            condition_2_str = '2'
        return condition_2_str

    def _date_condition_2_str(self, condition_dict, date_col='update_time'):
        condition_2_str = ''
        params = []
        start_time = condition_dict.get("start_date")
        end_time = condition_dict.get("end_date")
        if start_time:
            start_time += " 00:00:00"
            condition_2_str = date_col + ' >= %s'
            params.append(start_time)
        if end_time:
            end_time = end_time + " 23:59:59"
            if condition_2_str:
                condition_2_str += ' and '
            condition_2_str += date_col + ' <= %s'
            params.append(end_time)
        return condition_2_str, params

    def _fetch_many(self, pg, sqlcmd, params, size, page):
        offset = size * (page - 1)
        pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            pg.pgcur.scroll(offset)
        rows = pg.pgcur.fetchmany(size)
        return rowcount, rows

    def get_user_by_category(self, category_id, filter_dict):
        record = {"result": "NG"}
        if not category_id:
            return record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, record["content"] = self._get_user_by_category(cat_id_list, filter_dict)
        if record["content"]:
            record["total_count"] = count
            record["result"] = "OK"
        return record

    def _get_user_by_category(cat_id_list, filter_dict):
        return None, None

    def get_by_categorysql3(self, cat_id_list, filter_dict, user_id):
        return None, None

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
            record_id = row[0]
            model_list = self.get_model_list(pg, record_id)
            attr_dict["model_list"] = model_list
        return attr_dict

    def _get_parent_version(self, pg, data):
        return {}

    def update_col_change_list(self, pg, record_id, data, col_change_list):
        params = self.get_params(data, col_change_list)
        condition_col_list, key_col = [self.key_col], self.key_col
        sqlcmd = self.list_2_update_sql(self.table_name, col_change_list, condition_col_list, key_col)
        pg.execute(sqlcmd, params + [record_id])
        if pg.pgcur.rowcount:
            return True
        return False

    def update_model_diff_list(self, pg, record_id, model_diff_list):
        if model_diff_list:
            update_sql = self.list_2_update_sql(self.model_table_name, ["val"], ["order_no"], "order_no")
            insert_sql = self.list_2_insert_sql(self.model_table_name, [self.key_col, "model_id", "val"], "order_no")
            delete_sql = self.list_2_delete_sql(self.model_table_name, ["order_no"])
            for change_dict in model_diff_list:
                action = change_dict.get("action")
                data = change_dict.get("data")
                if action == 'change':
                    val = data.get("val")
                    order_no = data.get("order_no")
                    pg.execute(update_sql, [val, order_no])
                    if pg.pgcur.rowcount <= 0:
                        return False
                    data[self.key_col] = record_id
                    change_dict["record_id"] = order_no
                elif action == 'add':
                    model_id = data.get("model_id")
                    val = data.get("val")
                    params = [record_id, model_id, val]
                    pg.execute(insert_sql, params)
                    if pg.pgcur.rowcount <= 0:
                        return False
                    order_no = self.fetch_id(pg)
                    data[self.key_col] = record_id
                    data["order_no"] = order_no
                    change_dict["data"] = data
                    change_dict["record_id"] = order_no
                elif action == 'delete':
                    order_no = data.get("order_no")
                    change_dict["record_id"] = order_no
                    params = [order_no]
                    pg.execute(delete_sql, params)
                    if pg.pgcur.rowcount <= 0:
                        return False
                else:  # same
                    pass
                if not change_dict.get("record_id"):
                    pass
        return True

    def update_point_diff_dict(self, pg, point_diff_dict):
        if point_diff_dict:
            action = point_diff_dict.get("action")
            if action == "change":
                data = point_diff_dict.get("data")
                point_rc_id = data.get("pointout_rc_id")
                col_change_list = point_diff_dict.get("col_change_list")
                col_change_list.append("update_time")
                params = self.get_params(data, col_change_list)
                update_sql = self.list_2_update_sql("point_out", col_change_list, ["pointout_rc_id"], "pointout_rc_id")
                pg.execute(update_sql, params + [point_rc_id])
                if pg.pgcur.rowcount <= 0:
                    return False
            if action == "add":
                data = point_diff_dict.get("data")
                from Source.spec2db_server.arl.point_out import PointOut
                point_obj = PointOut(None)
                insert_sql = self.list_2_insert_sql("point_out", point_obj.attr_list[1:],
                                                    "pointout_rc_id")
                params = self.get_params(data, point_obj.attr_list[1:])
                pg.execute(insert_sql, params)
                if pg.pgcur.rowcount <= 0:
                    return False
                rc_id = self.fetch_id(pg)
                data["pointout_rc_id"] = rc_id
                point_diff_dict["record_id"] = rc_id
        return True

    def get_model_list(self, pg, record_id):
        model_list = []
        for model_id, model, val, order_no, def_rc_id in self._get_model_list(pg, record_id):
            model_dict = dict()
            model_dict["order_no"] = order_no
            model_dict["model_id"] = model_id
            model_dict["val"] = val
            model_dict[self.key_col] = def_rc_id
            model_list.append(model_dict)
        return model_list

    def _add_one2(self, pg, data, col_list):
        """from excel."""
        # print "table:%s, hu_id:%s, hu_def_id:%s,definition_id=%s" % (self.table_name, data.get("hu_id"),
        #                                                              data.get("hu_def_id"), data.get("definition_id"))
        sqlcmd = self.list_2_insert_sql(self.table_name, col_list, self.key_col)
        params = self.get_params(data, col_list)
        pg.execute(sqlcmd, params)
        rc_id = self.fetch_id(pg)
        # model_list = data.get("model_list")
        # model_list_change = self._add_model_list(pg, rc_id, model_list)
        return rc_id

    def _add_sub(self, pg, data, update_time):
        return []

    def _delete_sub(self, pg, _id, update_time):
        return []

    def add_point_out(self, pg, point_dict):
        sqlcmd = self.list_2_insert_sql(self.table_name, self.attr_list[1:], self.key_col)
        params = self.get_params(point_dict, self.attr_list[1:])
        pg.execute(sqlcmd, params)

    def _add_model_list(self, pg, rc_id, model_list):
        if not rc_id or not model_list:
            return
        model_list_change = []
        for d in model_list:
            model_id = d.get("model_id")
            val = d.get("val")
            order_no = self._insert_model(pg, rc_id, model_id, val)
            d["order_no"] = order_no
            d[self.key_col] = rc_id
            model_list_change.append(d)
        return model_list_change

    def _insert_model(self, pg, rc_id, model_id, val):
        sqlcmd = """
        INSERT INTO hmi.{table_name}(
                    {record_col}, model_id, val)
            VALUES (%s, %s, %s) returning order_no;
        """.format(table_name=self.model_table_name,
                   record_col=self.key_col)
        pg.execute(sqlcmd, (rc_id, model_id, val))
        return self.fetch_id(pg)

    def _sequence_list_2_str(self, sequence_list):
        temp_action_list = []
        for i, sequence_dict in enumerate(sequence_list, 1):
            action = sequence_dict.get("action")
            # temp_action_list.append('(%s)%s' % (i, action))
            if action:
                temp_action_list.append(action)
        return '\n'.join(temp_action_list)

    def _get_by_parent_id(self, pg, parent_id):
        condition_col_list = [self.parent_col_name]
        order_cols = [self.id_col]
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, condition_col_list, order_cols)
        pg.execute(sqlcmd, (parent_id,))
        rows = pg.fetchall()
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(row):
                attr_dict[self.attr_list[i]] = row[i]
                i += 1
            record_id = attr_dict.get(self.key_col)
            attr_dict["model_list"] = self.get_model_list(pg, record_id)
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def delete_by_parent(self, pg, parent_id, update_time):
        old_data_list = self._get_by_parent_id(pg, parent_id)
        new_data = None
        log_list = []
        for old_data in old_data_list:
            log_list = self._common_add(pg, new_data, old_data, update_time, check_md5=False)
            if log_list is None:
                return None
        return log_list

    def _split_dcu_meu_seq(self, _type, _status, _trigger, _action):
        sequence_dict, ref_base_list = dict(), list()
        trigger_seq = self._split_sequence(_trigger)
        action_seq = self._split_sequence(_action)
        seq_id_list = trigger_seq.keys() + action_seq.keys()
        if seq_id_list:
            seq_id_list = sorted(set(seq_id_list))
            for seq_id in seq_id_list:
                sequence_dict[seq_id] = {"type": _type,
                                         "status": _status,
                                         "trigger": trigger_seq.get(seq_id),
                                         "action": action_seq.get(seq_id),
                                         "id": "",
                                         "category": "",
                                         "name":  _type,
                                         "info": "",
                                         }
        elif self._is_ref_base(_action):
            ref_base_dict = {"type": _type,
                             "status": _status,
                             "trigger": _trigger,
                             "action": _action,
                             "id": "",
                             "category": "",
                             "name": _type,
                             "info": "",
                             }
            ref_base_list.append(ref_base_dict)
        return sequence_dict, ref_base_list

    def _split_sequence(self, s):
        seq_dict = dict()
        if s:
            seq_list = self.parse_action(s)
            if seq_list:
                for seq_id, contents in seq_list:
                    p = re.compile("^\(\d+")
                    m_group = p.match(seq_id).group(0)
                    _id = int(m_group[1:])  # (数字)去掉头尾的括号
                    if _id in seq_dict:
                        idx = s.find(contents)
                        if s[idx - 1] == '\n':
                            seq_dict[_id] = '%s\n%s' % (seq_dict.get(_id), contents)
                        else:
                            seq_dict[_id] = '%s%s' % (seq_dict.get(_id), contents)
                    else:
                        seq_dict[_id] = contents
            #
            # p1 = re.compile(r'[(^\(\d+\))|(\n\(\d+\))].*')
            # p2 = re.compile(r'\(\d+\)')
            # seq_list = p1.findall(s)
            #
            # for seq in seq_list:
            #     seq = seq.lstrip('\n')
            #     m = p2.match(seq)
            #     if m:
            #         seq_id = m.group(0)
            #         seq_id = int(seq_id[1:-1])  # (数字)去掉头尾的括号
            #         #  hcz(2017-11-08): (数字)不删除了
            #         seq_content = seq
            #         seq_dict[seq_id] = seq_content
        return seq_dict

    def parse_action(self, v):
        """parse an action cell

        return a list of (id, content) if there's concrete content
        return as-is if the content is empty
        """
        if v is None:
            return None
        # v = v.strip()
        if not v:  # empty, lets deal with this later
            return None
        if v in {'-', '※', '-※'}:
            return None
        offsets = list((m.groupdict()['id'], m.start(), m.end())
                       for m in re.finditer(r'^\s*(?P<id>\(\d+(\[(par|alt)\])?\))', v, re.MULTILINE))
        if not offsets:
            print 'Sequence:', v
            return None
        ids, starts, ends = zip(*offsets)
        if starts[0] != 0:
            return None
        starts = list(starts)
        ends = []
        for i, i_id in enumerate(ids[1:], start=1):
            starts[i] = v.find(i_id, starts[i])
            end_pos = starts[i] - 1
            if v[end_pos] in ('\n',):
                ends.append(end_pos)
            else:
                ends[i].append(starts[i-1])
        ends.append(len(v))
        contents = [v[start:end] for start, end in zip(starts, ends)]
        # cleanup = lambda x: '\n'.join(filter(None, (line.strip() for line in x.splitlines())))
        # contents = list(map(cleanup, contents))
        return list(zip(ids, contents))

    def _is_ref_base(self, val):
        """引用基本要件
        :param val:
        :return:
        """
        if val == '-※':
            return True
        else:
            return False

    def _get_device_seq(self, pg, _id):
        sequence_dict, ref_base_list = dict(), list()
        next_step = 0.001
        for model_id, model, val, _, _ in self._get_model_list(pg, _id):
            if self._is_ref_base(val):
                ref_base_dict = {"type": "DEVICE",
                                 "id": model_id,
                                 "name": model[-1],
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
                                             "name": model[-1],
                                             "info": model[-1],
                                             "status": "",
                                             "trigger": "",
                                             "action": seq_content,
                                             }
        return sequence_dict, ref_base_list

    def _merger_device_sequence(self, sequence_dict):
        if not sequence_dict:
            return []
        seq_id_list = sequence_dict.keys()
        model_list_dict = dict()
        for seq_id in sorted(seq_id_list):
            device_dict = sequence_dict.get(seq_id)
            model_id = device_dict.get("id")
            temp_val = device_dict.get("action")
            val = model_list_dict.get(model_id)
            if val:
                # model_list_dict[model_id] = '%s\n(%s)%s' % (val, seq_id, temp_val)
                model_list_dict[model_id] = '%s\n%s' % (val, temp_val)
            else:
                # model_list_dict[model_id] = '(%s)%s' % (seq_id, temp_val)
                model_list_dict[model_id] = temp_val
        model_id_list = model_list_dict.keys()
        model_list = []
        for model_id in model_id_list:
            model_list.append({"model_id": model_id, "val": model_list_dict.get(model_id)})
        return model_list

    def get_forest_model_type(self):
        self._pg.connect()
        model_list = self._get_all_model_types2(self._pg)
        forest_model = self._model_type_2_tree(model_list)
        self._pg.close()
        return forest_model

    def _model_type_2_tree(self, model_list):
        """只有叶子的model_id是正确的"""
        forest_model = []
        for model_id, model in model_list:
            sub_list = forest_model
            for model_name in model:
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
                    sub_list = found_model_dict.get("sub_list")
                else:  #
                    pass
        return forest_model

    def _get_all_model_types2(self, pg):
        if not self.model_type_table_name:
            return []
        sqlcmd = """
        SELECT model_id, model
          FROM hmi.{model_type}
          order by model_id;
        """.format(model_type=self.model_type_table_name)
        model_list = []
        pg.connect()
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        for row in rows:
            model_id, model = row[0:2]
            model = json.loads(model)
            model_list.append((model_id, model))
        return model_list

    def change_lock_status(self, lock, _type, _id):
        if _type == "hu":
            table_name = "hmi.hu"
            type_id = "hu_id"
        elif _type == "definition":
            table_name = "hmi.definition"
            type_id = "definition_id"
        elif _type == "analysis":
            table_name = "hmi.analysis"
            type_id = "definition_id"
        result = self._change_lock_status(table_name, _id, lock, type_id)
        return result

    def _change_lock_status(self, table_name, _id, lock, type_id):
        result = {"result": "NG"}
        self._pg.connect()
        sqlcmd = """
            update {table_name} set lock_status = %s where {type_id} = %s
        """.format(table_name=table_name,
                   type_id=type_id)
        try:
            self._pg.execute(sqlcmd, (lock, _id))
            self._pg.commit()
            self._pg.close()
            result["result"] = "OK"
            return result
        except Exception as e:
            return result

    def import_file(self, user_id, group_id, fileName, file_url, create_time):
        sqlcmd = """
            INSERT INTO hmi.arl_file(user_id, group_id, file_name, file_url, create_time) values(%s, %s, %s, %s, %s)
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (user_id, group_id, fileName, file_url, create_time))
        self._pg.commit()
        self._pg.close()

    def get_file_list(self, group_id):
        result = {"result": "OK"}
        sqlcmd = """
            SELECT record_id, user_name, group_name, file_name, file_url, create_time
            FROM hmi.arl_file as t1 left join hmi.arl_user as t2 on t1.user_id = t2.user_id
            left join hmi.arl_group as t3 on t1.group_id = t3.group_id
            where t1.group_id = %s order by create_time desc
        """
        col_list = ['record_id', 'user_name', 'group_name', 'file_name', 'file_url', 'create_time']
        self._pg.connect()
        self._pg.execute(sqlcmd, (group_id,))
        rows = self._pg.fetchall()
        file_list = []
        if rows:
            for row in rows:
                file_dict = dict()
                for i in range(len(row)):
                    file_dict[col_list[i]] = row[i]
                file_list.append(file_dict)
        result["data"] = file_list
        return result

    def get_file_url(self, record_id):
        sqlcmd = """
                   SELECT file_name, file_url
                   FROM hmi.arl_file where record_id = %s
               """
        self._pg.connect()
        self._pg.execute(sqlcmd, (record_id,))
        row = self._pg.fetchone()
        file_name = row[0]
        file_url = row[1]
        return file_name, file_url

    def update_post_lock_status(self, pg):
        pass

    def update_parent_lock_status(self, pg):
        pass

    def update_job_status(self, id, state):
        sqlcmd = """
         UPDATE hmi.{table_name}
         SET job_status = %s
         WHERE {table_col} = %s
        """.format(table_name=self.table_name, table_col=self.id_col)
        if id:
            self._pg.connect()
            self._pg.execute(sqlcmd, (state, id))
            self._pg.commit()
            self._pg.close()
            result = {"result": "OK"}
        else:
            result = {"result": "NG"}
        return result

    def _look_job_status(self, _id):
        result = {"result": "OK"}
        sqlcmd = """
         SELECT job_status
         FROM hmi.{table_name}
         WHERE {table_col} = %s
        """.format(table_name=self.table_name, table_col=self.id_col)

        self._pg.connect()
        self._pg.execute(sqlcmd, (_id,))
        row = self._pg.fetchone()
        if row:
            result["job_status"] = row[0]
        else:
            result = {"result": "NG"}
        self._pg.close()
        return result

    def insert_check_list(self, pg, commit_id, type, check_list):
        for row in check_list:
            self.insert_check_one(pg, commit_id, type, row)

    def insert_check_one(self, pg, commit_id, type, check_list):
        _check_list = check_list
        item_id = _check_list.get("cl_item_id")
        author = _check_list.get("author_check")
        charger = _check_list.get("charger_check")
        sqlcmd = """
        INSERT INTO hmi.check_list
            (cl_item_id, commit_id, classfy, author_check, charger_check)
        VALUES (%s, %s, %s, %s, %s)
        """
        pg.execute(sqlcmd, (item_id, commit_id, type, author, charger))

    def get_old_data(self, pg, hu_id):
        pass

    def parse_screen_id(self, hmi_screen_id):
        pass

    def delete_scree_by_hu_id(self, pg, hu_id):
        pass

    def insert_screen(self, pg, hu_id, screen_id_list):
        pass

    def select_hmi_screen(self, pg, screen_id):
        pass

    def insert_hmi_screen(self, pg, screen_id):
        pass

    def add(self, pg, data, update_cols=None):
        log_list = self._common_add(pg, data, update_cols)
        return log_list

    def _common_add(self, pg, data, update_time='2018-01-01 00:00:00', update_cols=None):
        if not update_cols:
            update_cols = []
        hu_id = data.get(self.id_col)
        old_datas = self.get_old_data(pg, hu_id)
        if old_datas:
            old_data = old_datas[0]
        else:
            old_data = None
        ignore_col_list = []
        diff_obj = ArlDiff(self.key_col, self.id_col, self.attr_list, ignore_col_list)
        diff_result = diff_obj.diff(old_data, data)
        action = diff_result.get("action")
        if action == "same":
            return None
        if action == "add":
            self._count_ng_num(old_data, data)
            rc_id = self._add_one2(pg, data, self.attr_list[1:])
            col_change_list = diff_result.get("col_change_list")
            self.update_screen_rel(pg, data, col_change_list, action)
            data[self.key_col] = rc_id
            diff_result[self.key_col] = rc_id
            # ## 记录状态变化
            old_status = ''
            new_status = data.get('dev_status')
            self._status_log(self._pg, hu_id, old_status, new_status, update_time)
        elif action == "change":
            data[self.key_col] = old_data.get(self.key_col)
            col_change_list = diff_result.get("col_change_list")
            if update_cols:
                update_cols_list = [i_data for i_data in col_change_list if i_data in update_cols]
            else:
                update_cols_list = col_change_list
            if 'dev_status' in update_cols_list:
                self._count_ng_num(old_data, data)
                if data.get('dev_status') == HMI_DEV_STATUS_NG:
                    update_cols_list.append('ng_num')
                # ## 记录状态变化
                old_status = old_data.get('dev_status')
                new_status = data.get('dev_status')
                self._status_log(self._pg, hu_id, old_status, new_status, update_time)
            self.update_screen_rel(pg, data, col_change_list, action)
            record_id = diff_result.get(self.key_col)
            if update_cols_list:
                if not self.update_col_change_list(pg, record_id, data, update_cols_list):
                    return None
        else:
            pass
        log_list = self.convert2log([diff_result])
        return log_list

    def delete(self, pg, id_val):
        delete_sql = self.list_2_delete_sql(self.model_table_name, [self.id_col])
        pg.execute(delete_sql)

    def update_screen_rel(self, pg, data, col_change_list, action):
        pass

    def _status_log(self, pg, _id, old_status, new_status, update_time):
        pass

    def _count_ng_num(self, old_data, new_data):
        if old_data:
            if new_data.get('dev_status') != old_data.get('dev_status'):
                ng_num = old_data.get('ng_num')
                if not ng_num:
                    ng_num = 0
                if new_data['dev_status'] == HMI_DEV_STATUS_NG:  # NG
                        new_data['ng_num'] = ng_num + 1
                else:
                    new_data['ng_num'] = ng_num
        else:
            if new_data.get('dev_status') == HMI_DEV_STATUS_NG:
                new_data['ng_num'] = 1
            else:
                new_data['ng_num'] = 0


