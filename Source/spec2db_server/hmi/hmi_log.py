# -*- coding: UTF-8 -*-
"""
Created on 2018-2-26

@author:
"""
from Source.spec2db_server.hmi.hmi_base import HMIBase
import time
import numpy as np
import copy
from Source.spec2db_server.arl.arl_table_manage import ArlTableMng

COMMIT_CLASSIFY = {"arl": 1, "hu": 2, "definition": 3, "analysis": 4,
                   "basic_req_hu": 5, "basic_req_definition": 6, "basic_req_analysis": 7,
                   "point_out": 8,
                   # ## HMI
                   "req": 10, "external_qa": 11, "hmi_screen": 12, "internal_qa": 13, "external_bug": 14,
                   "hmi_screen_it": 15, "it_screen_move": 16, "it_result_notify": 17,
                   "it_result_mode_transition": 18, "it_result_init_end": 19, "it_inside_move": 20

                   }
COMMIT_CLASSIFY_REVERSE = {1: "arl", 2: "hu", 3: "definition", 4: "analysis",
                           5: "basic_req_hu", 6: "basic_req_definition", 7: "basic_req_analysis",
                           8: "point_out",
                           # ## HMI
                           10: "req", 11: "external_qa", 12: "hmi_screen"
                           }
COMMIT_ACTION = {"add": 0, "change": 1, "delete": 2, "same": 3, "hide_change": 4}
COMMIT_ID_COL = {"arl": "arl_id", "hu": "hu_id", "definition": "definition_id", "analysis": "definition_id",
                 "basic_req_hu": "hu_id", "basic_req_definition": "definition_id", "basic_req_analysis": "definition_id",
                 # ## HMI
                 "req": "hu_id", "qa": "qa_no"}
HIDE_COLS = set(["user_id", "group_id", "lock_status", "job_status",
                 "complete_flag", "update_time", "major_ver", "small_ver",
                 "translation_flag", "agree_flag", "md5_key"])
MODEL_DEFAULT_VAL = '-'


class HmiLog(HMIBase):
    """
        This class provides the function of commit.Function:
            Add commit log: add_commit_log(data={})
            Get commit log by user: get_commit_log_by_user(user_id, str_time)
            Get commit log by group leader: get_commit_log_by_group(group_id, str_time)
            Get commit log by administrator: get_commit_log_by_admin(str_time)
    """
    def __init__(self,):
        HMIBase.__init__(self)
        self.schema = 'hmi'

    def _get_current_time(self, ):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def _handle_input_time(self, input_time=''):
        # 将时间字符串格式"2017-10-22"，转成:"XXXX-XX-XX XX:XX:XX"格式的时间字符串
        return input_time + ' ' + '00:00:00'

    def _create_commit_log_table(self, ):
        sqlcmd = '''
                -- DROP TABLE IF EXISTS {schema}.commit_log;
                CREATE TABLE {schema}.commit_log
                (
                    commit_id serial NOT NULL,-- the unique id of once commit
                    user_id BIGINT, --user_id
                    group_id BIGINT, -- group_id
                    commit_time character varying(24), -- commit time
                    CONSTRAINT commit_log_pkey PRIMARY KEY (commit_id)
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE {schema}.commit_log
                OWNER TO postgres;
    
                CREATE INDEX COMMIT_LOG_COMMIT_ID ON {schema}.commit_log(commit_id);
                CREATE INDEX COMMIT_LOG_USER_ID ON {schema}.commit_log(user_id);
                CREATE INDEX COMMIT_LOG_GROUP_ID ON {schema}.commit_log(group_id);
                CREATE INDEX COMMIT_LOG_COMMIT_TIME ON {schema}.commit_log(commit_time);
    
    
                -- DROP TABLE IF EXISTS {schema}.commit_log_ref;
                CREATE TABLE {schema}.commit_log_ref(
                    commit_log_ref_id serial NOT NULL,--using this id to get the commit detial info of one table
                    commit_id BIGINT NOT NULL, -- commit id
                    table_id INTEGER NOT NULL, --table_id
                    classify SMALLINT NOT NULL, --table class. 1:arl, 2:hu, 3:def
                    CONSTRAINT commit_log_ref_pkey PRIMARY KEY (commit_log_ref_id),
                    CONSTRAINT commit_log_commit_id_ref_fkey FOREIGN KEY (commit_id)
                      REFERENCES {schema}.commit_log (commit_id) MATCH SIMPLE
                      ON UPDATE RESTRICT ON DELETE RESTRICT
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE {schema}.commit_log_ref
                OWNER TO postgres;
                CREATE INDEX COMMIT_LOG_REF_commit_id ON {schema}.commit_log_ref(commit_id);
                CREATE INDEX COMMIT_LOG_REF_CLASSIFY ON {schema}.commit_log_ref(classify);
    
    
                -- DROP TABLE IF EXISTS {schema}.commit_log_info;
                CREATE TABLE {schema}.commit_log_info(
                    commit_log_info_id serial NOT NULL, --PK
                    commit_log_ref_id BIGINT NOT NULL, -- using this id to get the commit detial info of one table
                    record_id BIGINT NOT NULL,-- record id of the table 
                    action_type INTEGER NOT NULL, -- modify type. 0:add, 1:update, 2:delete
                    status_flag BIT varying(128) NOT NULL, -- the bit mask to get the flag whether one column is changed.
                    column_info TEXT[] NOT NULL, -- the column info after this commit
                    CONSTRAINT commit_log_info_pkey PRIMARY KEY (commit_log_info_id),
                    CONSTRAINT commit_log_commit_log_ref_id_ref_fkey FOREIGN KEY (commit_log_ref_id)
                      REFERENCES {schema}.commit_log_ref (commit_log_ref_id) MATCH SIMPLE
                      ON UPDATE RESTRICT ON DELETE RESTRICT
                )
                WITH (
                OIDS=FALSE
                );
                ALTER TABLE {schema}.commit_log_info
                OWNER TO postgres;
    
                CREATE INDEX COMMIT_LOG_INFO_COMMIT_LOG_REF_ID ON {schema}.commit_log_info(commit_log_ref_id);
                CREATE INDEX COMMIT_LOG_INFO_RECORD_ID ON {schema}.commit_log_info(record_id);
            '''.format(schema=self.schema)

    def _generate_commit_log_status_flags(self, last_column_info, new_column_info):
        """使用最近一次的commit log中的columns info 和 本次提交的columns info来生成status flags字段"""
        status_flag = ''
        last_column_len = len(last_column_info)
        new_column_len = len(new_column_info)
        # 这里只能处理增加列，不能处理减少列
        for index in xrange(last_column_len):
            if new_column_info[index] == last_column_info[index]:
                status_flag += '0'
            else:
                status_flag += '1'
        index += 1
        while index < new_column_len:
            status_flag += '1'
        return status_flag

    def _get_last_commit_by_record_id(self, pg, record_id):
        """Insert one new commit log"""
        sql_cmd = '''WITH r AS (
                  SELECT max(commit_log_info_id) AS commit_log_info_id FROM {schema}.commit_log_info WHERE record_id = %s
                )
                SELECT a.column_info FROM {schema}.commit_log_info AS a 
                JOIN r ON r.commit_log_info_id = a.commit_log_info_id;'''.format(schema=self.schema) % record_id
        pg.execute(sql_cmd)
        rows = pg.fetchall()
        if len(rows) == 0:
            # log...
            return None
        else:
            return rows[0][0]

    def _generate_status_flags(self, pg, column_info, record_id):
        last_commit_columns_info = self._get_last_commit_by_record_id(pg, record_id)
        if last_commit_columns_info is None:
            status_flag = ''
            for i in range(len(column_info)):
                status_flag += '1'
            return status_flag
        else:
            return self._generate_commit_log_status_flags(last_commit_columns_info, column_info)

    def add_commit_log(self, pg, data={}):
        commit_id = self._add_commit_log(pg, data)
        try:
            for table in data['commit_tables']:
                commit_log_ref_id = self._add_commit_log_ref(pg, data, commit_id)
                for record in table['records']:
                    record_id = record['record_id']
                    action_type = record['action_type']
                    column_info = record['column_info']
                    status_flag = self._generate_status_flags(pg, column_info, record_id)
                    if '1' not in status_flag and str(action_type) == '1':
                        continue
                    sql_cmd = '''INSERT INTO {schema}.commit_log_info(commit_log_ref_id, record_id, action_type, status_flag, column_info)
                                     VALUES(%s, %s, %s, b%s, %s);
                        '''.format(schema=self.schema)
                    fin_array = np.array([column_info])
                    pg.execute(sql_cmd, (commit_log_ref_id, record_id, action_type, status_flag, (list(fin_array[0]),)))
        except Exception as e:
            print(e)
            return False
        return True

    def _add_commit_log(self, pg, data, update_time):
        col_list = ["user_id", "group_id", "commit_time"]
        key_col = "commit_id"
        sqlcmd = self.list_2_insert_sql("commit_log", col_list, key_col)
        user_id = data.get('user_id')
        group_id = data.get("group_id")
        commit_time = update_time
        pg.execute(sqlcmd, [user_id, group_id, commit_time])
        commit_id = self.fetch_id(pg)
        return commit_id

    def _add_commit_log_ref(self, pg, data, commit_id):
        table_id = data['table_id']
        classify = data['classify']
        sql_cmd = '''
            INSERT INTO {schema}.commit_log_ref(commit_id, table_id, classify) 
                VALUES(%s, %s, %s) RETURNING commit_log_ref_id;
            '''.format(schema=self.schema)
        pg.execute(sql_cmd, (commit_id, table_id, classify))
        commit_log_ref_id = self.fetch_id(pg)
        return commit_log_ref_id

    def get_commit_log_by_user(self, user_id, s_time, e_time):
        start_time = s_time + " 00:00:00"
        end_time = e_time + " 23:59:59"
        result = {"result": "NG"}
        # classify:保存了本次修改设计到的所有的分类，如arl，hu，def。。。
        self._pg.connect()
        sql_cmd = '''SELECT commit_id, lower(b.user_name), lower(c.group_name), commit_time
                         FROM {schema}.commit_log AS a
                         JOIN {schema}.arl_user AS b ON a.user_id = b.user_id
                         JOIN {schema}.arl_group AS c ON a.group_id = c.group_id
                         WHERE a.user_id = %s AND commit_time >= '%s' AND commit_time <= '%s';
            '''.format(schema=self.schema)
        self._pg.execute(sql_cmd % (user_id, start_time, end_time))
        rows = self._pg.fetchall()
        content = []
        for row in rows:
            commit_info = dict()
            commit_info['commit_id'] = str(int(row[0]))
            commit_info['user_name'] = str(row[1])
            commit_info['group_name'] = str(row[2])
            commit_info['commit_time'] = str(row[3])
            commit_info['user_id'] = user_id
            sql_cmd = '''SELECT DISTINCT classify FROM {schema}.commit_log_ref 
                WHERE commit_id = %s;'''.format(schema=self.schema)
            self._pg.execute(sql_cmd % row[0])
            rows_tmp = self._pg.fetchall()
            classifies = []
            for row_tmp in rows_tmp:
                classifies.append(str(row_tmp[0]))
            commit_info['classify'] = classifies
            content.append(commit_info)
        if content:
            result["content"] = content
            result["result"] = "OK"
        self._pg.close()
        return result

        # get commit log info by group leader id

    def get_commit_log_by_group(self, group_id, s_time, e_time):
        start_time = s_time + " 00:00:00"
        end_time = e_time + " 23:59:59"
        result = {"result": "NG"}
        self._pg.connect()
        sql_cmd = '''SELECT commit_id, a.user_id, lower(b.user_name), lower(c.group_name), commit_time
                                 FROM {schema}.commit_log AS a
                                 JOIN {schema}.arl_user AS b ON a.user_id = b.user_id
                                 JOIN {schema}.arl_group AS c ON a.group_id = c.group_id
                                 WHERE a.group_id = %s AND commit_time >= '%s' AND commit_time <= '%s'
                                ORDER BY commit_id;
                    '''.format(schema=self.schema)
        self._pg.execute(sql_cmd % (group_id, start_time, end_time))
        rows = self._pg.fetchall()
        content = []
        for row in rows:
            commit_info = dict()
            commit_info['commit_id'] = str(int(row[0]))
            commit_info['user_id'] = str(int(row[1]))
            commit_info['user_name'] = str(row[2])
            commit_info['group_name'] = str(row[3])
            commit_info['commit_time'] = str(row[4])
            sql_cmd = '''SELECT DISTINCT classify FROM {schema}.commit_log_ref 
                WHERE commit_id = %s;'''.format(schema=self.schema)
            self._pg.execute(sql_cmd % row[0])
            rows_tmp = self._pg.fetchall()
            classifies = []
            for row_tmp in rows_tmp:
                # classify:保存了本次修改设计到的所有的分类，如arl，hu，def。。。
                classifies.append(str(row_tmp[0]))
            commit_info['classify'] = classifies
            content.append(commit_info)
        if content:
            result["content"] = content
            result["result"] = "OK"
        self._pg.close()
        return result

        # get commit log info by administrator

    def get_commit_log_by_admin(self, s_time, e_time):
        start_time = s_time + " 00:00:00"
        end_time = e_time + " 23:59:59"
        result = {"result": "NG"}
        self._pg.connect()
        sql_cmd = '''SELECT commit_id, a.user_id, lower(b.user_name), lower(c.group_name), commit_time
                         FROM {schema}.commit_log AS a
                         JOIN {schema}.arl_user AS b ON a.user_id = b.user_id
                         JOIN {schema}.arl_group AS c ON a.group_id = c.group_id
                         WHERE commit_time >= '%s' AND commit_time <= '%s';
            '''.format(schema=self.schema)
        self._pg.execute(sql_cmd % (start_time, end_time))
        rows = self._pg.fetchall()
        content = []
        for row in rows:
            commit_info = dict()
            commit_info['commit_id'] = row[0]
            commit_info['user_id'] = row[1]
            commit_info['user_name'] = row[2]
            commit_info['group_name'] = row[3]
            commit_info['commit_time'] = row[4]
            sql_cmd = '''SELECT DISTINCT classify FROM {schema}.commit_log_ref 
                WHERE commit_id = %s;'''.format(schema=self.schema)
            self._pg.execute(sql_cmd % row[0])
            rows_tmp = self._pg.fetchall()
            classifies = []
            for row_tmp in rows_tmp:
                classifies.append(str(row_tmp[0]))
            commit_info['classify'] = classifies
            content.append(commit_info)
        if content:
            result["content"] = content
            result["result"] = "OK"
        self._pg.close()
        return result

    def get_commit_log(self, s_time, e_time, group_id=0, user_id=0, size=0, page=0):
        start_time = s_time + " 00:00:00"
        end_time = e_time + " 23:59:59"
        result = {"result": "NG"}
        col_list, params = [], []
        condition_str = ''
        for col, param in zip(["a.group_id", "a.user_id"], [group_id, user_id]):
            if param:
                col_list.append(col)
                params.append(param)
        if col_list:
            condition_str = self.list_2_condition_str(col_list, where=False)
            if condition_str:
                condition_str += ' and '
        sql_cmd = '''
            SELECT commit_id, a.user_id,
                  lower(b.user_name) as user_name, 
                  lower(c.group_name) as group_name, commit_time
            FROM {schema}.commit_log AS a
            left JOIN {schema}.arl_user AS b
            ON a.user_id = b.user_id
            left JOIN {schema}.arl_group AS c
            ON a.group_id = c.group_id
            where {condition_str} commit_time >= %s AND commit_time <= %s
            ORDER BY commit_time DESC -- commit_id DESC
            '''.format(schema=self.schema, condition_str=condition_str)
        rows, content, rowcount = [], [], 0
        try:
            self._pg.connect()
            self._pg.execute(sql_cmd, params + [start_time, end_time])
            offset = size * (page - 1)
            rowcount = self._pg.pgcur.rowcount
            if rowcount > 0:
                if offset >= rowcount:
                    pass
                else:
                    self._pg.pgcur.scroll(offset)
                    rows = self._pg.pgcur.fetchmany(size)
            for row in rows:
                commit_info = dict()
                commit_info['commit_id'] = row[0]
                commit_info['user_id'] = row[1]
                commit_info['user_name'] = row[2]
                commit_info['group_name'] = row[3]
                commit_info['commit_time'] = row[4]
                sql_cmd = """
                    SELECT array_agg(classify) classifies
                      FROM (
                        SELECT DISTINCT commit_id, classify
                           FROM {schema}.commit_log_ref
                           WHERE commit_id = %s
                           order by classify
                      ) as a
                      group by commit_id;
                      """.format(schema=self.schema)
                self._pg.execute(sql_cmd % row[0])
                row_tmp = self._pg.fetchone()
                if row_tmp:
                    classifies = row_tmp[0]
                    classify_str_list = []
                    for classify in classifies:
                        classify_str_list.append(COMMIT_CLASSIFY_REVERSE.get(classify))
                    commit_info['classify'] = classify_str_list
                content.append(commit_info)
            if content:
                result["content"] = content
                result["total_count"] = rowcount
                result["result"] = "OK"
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return result

        # get detail commit info using commit id

    def get_commit_log_by_commit_id(self, commit_id):
        result = {"result": "NG"}
        self._pg.connect()
        sql_cmd = '''SELECT commit_log_ref_id, table_id, classify 
                           FROM {schema}.commit_log_ref
                           WHERE commit_id = %s;
                           '''.format(schema=self.schema)
        self._pg.execute(sql_cmd % commit_id)
        rows = self._pg.fetchall()
        self._pg.close()
        return result

    def get_commit_log_detail(self, commit_id, commit_log_ref_id=0):
        result = {"result": "NG"}
        self._pg.connect()
        min_id, max_id = self._get_commit_log_ref_id_range(self._pg, commit_id)
        if min_id:
            if not commit_log_ref_id:
                commit_log_ref_id = min_id
            else:
                if not (commit_log_ref_id >= min_id) and (commit_log_ref_id <= max_id):
                    self._pg.close()
                    return result
            table_name, action_type, log_data = self._get_log_data(self._pg, commit_log_ref_id)
            if log_data:
                result["classify"] = table_name  # 类别：hu, definition, analysis
                result["action_type"] = action_type  # "add": 0, "change": 1, "delete": 3, "same": 4
                result["content"] = log_data
                result["start_log_ref_id"] = min_id
                result["end_log_ref_id"] = max_id
                result["result"] = "OK"
        self._pg.close()
        return result

    def get_commit_log_brief(self, commit_id, size, page):
        result = {"result": "NG"}
        self._pg.connect()
        rowcount, brief_log_list = self._get_commit_log_brief(self._pg, commit_id, size, page)
        if brief_log_list:
            result["content"] = brief_log_list
            result["total_count"] = rowcount
            result["result"] = "OK"
        self._pg.close()
        return result

    def _get_commit_log_brief(self, pg, commit_id, size, page):
        sqlcmd = """
            SELECT t2.commit_log_ref_id, table_name, column_info
              FROM (
                SELECT commit_log_ref_id, commit_id, table_id, classify
                  FROM {schema}.commit_log_ref
                  where commit_id  = %s
              ) as t1
              left join {schema}.commit_log_info as t2
              ON t1.commit_log_ref_id = t2.commit_log_ref_id
              where table_name in ('arl', 'hu', 'definition', 'analysis', 
              'basic_req_hu', 'basic_req_definition', 'basic_req_analysis')
              order by t2.commit_log_ref_id
            """.format(schema=self.schema)
        brief_log_list = []
        offset = size * (page - 1)
        pg.execute(sqlcmd, [commit_id])
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                # offset = ((rowcount - 1) / size) * size
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        for row in rows:
            brief_log = dict()
            commit_log_ref_id = row[0]
            table_name = row[1]
            column_info = row[2]
            table_mng_obj = ArlTableMng.instance()
            col_info_list = table_mng_obj.get_col_list(table_name)
            id_col = COMMIT_ID_COL.get(table_name)
            if not id_col:
                print 'Error '
                continue
            for i, col_info in enumerate(col_info_list, 0):
                if id_col == col_info.get("col_name"):
                    _id = column_info[i]
                    brief_log["commit_log_ref_id"] = commit_log_ref_id
                    brief_log["classify"] = table_name
                    brief_log["id"] = _id
                    brief_log_list.append(brief_log)
                    break
        return rowcount, brief_log_list

    def _get_commit_log_ref_id_range(self, pg, commit_id):
        sqlcmd = """
            SELECT min(commit_log_ref_id), max(commit_log_ref_id)
              FROM {schema}.commit_log_ref
              where commit_id = %s
              group by commit_id
            """.format(schema=self.schema)
        pg.execute(sqlcmd, [commit_id])
        row = pg.fetchone()
        if row:
            min_id, max_id = row[0], row[1]
            return min_id, max_id
        return None, None

        # arl:0 hu:1 def:2

    def get_commit_log_by_classify_and_record_id(self, classify, r_id):
        result = {"result": "NG"}
        sql_cmd = '''
            SELECT t3.commit_id, t3.user_id, t4.user_name, 
                    t3.group_id, t5.group_name, t3.commit_time,
                    t1.commit_log_ref_id
              FROM {schema}.commit_log_info AS t1
              LEFT JOIN {schema}.commit_log_ref as t2
              on t1.commit_log_ref_id = t2.commit_log_ref_id
              LEFT JOIN {schema}.commit_log AS t3
              on t2.commit_id = t3.commit_id
              LEFT JOIN {schema}.arl_user AS t4
              ON t3.user_id = t4.user_id
              LEFT JOIN {schema}.arl_group AS t5
              ON t3.group_id = t5.group_id
              where record_id = %s and table_name = %s
              ORDER BY t3.commit_time DESC 
            '''.format(schema=self.schema)
        rows = []
        try:
            self._pg.connect()
            self._pg.execute(sql_cmd, (r_id, classify))
            rows = self._pg.fetchall()
        except Exception as e:
            print e
        finally:
            self._pg.close()
        content = []
        for row in rows:
            elem = dict()
            # 如果status_flag 全是0，则不需要返回这条record
            elem['commit_id'] = row[0]
            elem['user_id'] = row[1]
            elem['user_name'] = row[2]
            elem['group_name'] = row[4]
            elem['commit_time'] = row[5]
            elem['commit_log_ref_id'] = row[6]
            content.append(elem)
        if content:
            result['result'] = "OK"
            result['content'] = content
        return result

    def add_commit_log2(self, pg, log):
        table_mng_obj = ArlTableMng.instance()
        log_commit = log.get('commit_list')[0]
        log_commit_data = log_commit.get("data")
        update_time = log_commit_data.get("update_time")
        commit_id = self._add_commit_log(pg, log, update_time)
        try:
            for commit in log.get('commit_list'):
                table_name = commit.get("table_name")
                action = commit.get("action")
                table_id = table_mng_obj.get_table_id(table_name)
                col_list = table_mng_obj.get_cols_name(table_name)
                action_type = self._get_action_type(action, commit)
                record_id = commit.get("record_id")
                data = commit.get("data")
                col_change_list = commit.get("col_change_list")
                status_flag = self._generate_status_flags2(action, col_list, col_change_list)
                data_list = self._generate_data_list(data, col_list)
                commit_log_ref_id = self._add_commit_log_ref2(pg, commit_id, table_id, table_name)
                major_ver, small_ver, reason = data.get("major_ver"), data.get("small_ver"), data.get("reason")
                self._commit_log_info(pg, commit_log_ref_id, record_id,
                                      action_type, status_flag, data_list,
                                      table_name, major_ver, small_ver,
                                      reason)
                model_rels = commit.get("model_rel")
                if model_rels:
                    for model_rel in model_rels:
                        table_name = model_rel.get("table_name")
                        action = model_rel.get("action")
                        action_type = COMMIT_ACTION.get(action)
                        col_list = table_mng_obj.get_cols_name(table_name)
                        data = model_rel.get("data")
                        record_id = model_rel.get("record_id")
                        col_change_list = model_rel.get("col_change_list")
                        # major_ver, small_ver = data.get("major_ver"), data.get("small_ver")
                        major_ver, small_ver, reason = None, None, None
                        status_flag = self._generate_status_flags2(action, col_list, col_change_list)
                        data_list = self._generate_data_list(data, col_list)
                        self._commit_log_info(pg, commit_log_ref_id, record_id,
                                              action_type, status_flag, data_list,
                                              table_name, major_ver, small_ver,
                                              reason)
                point_dict = commit.get("point_dict")
                if point_dict:
                    table_name = point_dict.get("table_name")
                    action = point_dict.get("action")
                    action_type = COMMIT_ACTION.get(action)
                    col_list = table_mng_obj.get_cols_name(table_name)
                    data = point_dict.get("data")
                    record_id = point_dict.get("record_id")
                    col_change_list = point_dict.get("col_change_list")
                    major_ver, small_ver, reason = None, None, None
                    status_flag = self._generate_status_flags2(action, col_list, col_change_list)
                    data_list = self._generate_data_list(data, col_list)
                    self._commit_log_info(pg, commit_log_ref_id, record_id,
                                          action_type, status_flag, data_list,
                                          table_name, major_ver, small_ver,
                                          reason)

            return True, commit_id
        except Exception as e:
            print(e), commit
            return False, None

    def _get_action_type(self, action, commit):
        if action == "change":
            action_type = COMMIT_ACTION.get(action)
            col_change_list = commit.get("col_change_list")
            if set(col_change_list).issubset(HIDE_COLS):
                model_rels = commit.get("model_rel")
                for model_rel in model_rels:
                    model_action = model_rel.get("action")
                    if model_action != "same":
                        return action_type
                return COMMIT_ACTION.get("hide_change")
            return action_type
        else:
            return COMMIT_ACTION.get(action)

    def _commit_log_info(self, pg, commit_log_ref_id, record_id,
                         action_type, status_flag, data_list,
                         table_name, major_ver, small_ver,
                         reason):
        sql_cmd = '''
            INSERT INTO {schema}.commit_log_info(commit_log_ref_id, record_id, action_type,
                                             status_flag, column_info, table_name,
                                             major_ver, small_ver, reason)
               VALUES(%s, %s, %s,
                     b%s, %s, %s,
                     %s, %s, %s);
            '''.format(schema=self.schema)
        fin_array = np.array([data_list])
        pg.execute(sql_cmd, (commit_log_ref_id, record_id, action_type,
                             status_flag, (list(fin_array[0]),), table_name,
                             major_ver, small_ver, reason
                             )
                   )

    def _generate_status_flags2(self, action, col_list, col_change_list):
        if action in ("add", "delete"):
            status_list = ['1'] * len(col_list)
        elif action == "change":
            status_list = ['0'] * len(col_list)
            for col in col_change_list:
                status_list[col_list.index(col)] = '1'
        else:  # same
            status_list = ['0'] * len(col_list)
        return ''.join(status_list)

    def _generate_data_list(self, data, col_list):
        data_list = []
        for col in col_list:
            val = data.get(col)
            if val is None:
                data_list.append(val)
            else:
                data_list.append(unicode(val))
        return data_list

    def _add_commit_log_ref2(self, pg, commit_id, table_id, table_name):
        classify = COMMIT_CLASSIFY.get(table_name)
        sql_cmd = '''
            INSERT INTO {schema}.commit_log_ref(commit_id, table_id, classify) 
                VALUES(%s, %s, %s) RETURNING commit_log_ref_id;
            '''.format(schema=self.schema)
        pg.execute(sql_cmd, (commit_id, table_id, classify))
        commit_log_ref_id = self.fetch_id(pg)
        return commit_log_ref_id

    def _get_log_data(self, pg, commit_log_ref_id):
        """{"col_name": {"title": "表示Title名称", "new_val": "xxx", "old_val": "ooo", "changed": 1}}"""
        rows = self._get_log_info(pg, commit_log_ref_id)
        if not rows:
            return None, None, {}
        (commit_id, commit_log_ref_id, table_name, classify,
         record_id, action_type) = rows[0][0:6]  # 第0个是本体，后面是的Model_list
        from Source.spec2db_server.arl.arl_table_manage import ArlTableMng
        table_mng_obj = ArlTableMng.instance()
        col_info_list = table_mng_obj.get_col_list(table_name)
        model_type_dict = self._get_all_model_type_info(pg, table_name)  # 获取model的title, name, category
        curr_base_data, model_dict = self._convert_2_full_data(col_info_list, model_type_dict, rows)
        prev_rows = self._get_prev_log_info(pg, commit_log_ref_id, table_name, record_id)
        prev_base_data, prev_model_dict = self._convert_2_full_data(col_info_list, model_type_dict, prev_rows)
        # 合并前后两版基本数据
        for col_name in curr_base_data.iterkeys():
            col_data = curr_base_data.get(col_name)
            prev_col_data = prev_base_data.get(col_name)
            if prev_col_data:
                col_data["old_val"] = prev_col_data.get("val")
            else:
                col_data["old_val"] = None
            self._replace_character(col_data)  # \n替换行<br>
            col_data["changed"] = self._get_val_action_type(col_data.get("val"), col_data.get("old_val"))
        merged_model_list = self._merge_model_list(model_dict, prev_model_dict)
        if table_name in ("hu", "basic_req_hu"):
            # 按部品分类
            categoryed_model = self.category_model_list(merged_model_list, table_name)
            mm_model_list = categoryed_model.get(u"H/U以外のＭＭ部品")
            if mm_model_list:
                curr_base_data["mm_model_list"] = mm_model_list
            else:
                curr_base_data["mm_model_list"] = []
            other_model_list = categoryed_model.get(u"他部署設計部品(部品名は参考)")
            if other_model_list:
                curr_base_data["other_model_list"] = other_model_list
            else:
                curr_base_data["other_model_list"] = []
        if table_name in ("analysis", "basic_req_analysis"):
            categoryed_model = self.category_model_list(merged_model_list, table_name)
            curr_base_data["model_list"] = categoryed_model
        else:
            curr_base_data["model_list"] = merged_model_list
        return table_name, action_type, curr_base_data

    def _get_last_log_ref_id(self, pg, table_name, record_id, end_commit_time):
        sqlcmd = """
            SELECT max(t1.commit_log_ref_id)
              FROM {schema}.commit_log_info AS t1
              LEFT JOIN {schema}.commit_log_ref AS t2
              ON t1.commit_log_ref_id = t2.commit_log_ref_id
              left join {schema}.commit_log as t3
              on t2.commit_id = t3.commit_id
              WHERE t1.table_name = %s
                    and t1.record_id = %s
                    and commit_time < %s
            """.format(schema=self.schema)
        pg.execute(sqlcmd, [table_name, record_id, end_commit_time])
        row = pg.fetchone()
        if row:
            return row[0]
        return None

    def _diff_log_data(self, pg, prev_log_ref_id, curr_log_ref_id):
        from Source.spec2db_server.arl.arl_table_manage import ArlTableMng
        table_mng_obj = ArlTableMng.instance()
        diff_data = {}
        curr_rows = self._get_log_info(pg, curr_log_ref_id)
        if not curr_rows:
            return None, diff_data
        table_name, classify, record_id, action_type = curr_rows[0][2:6]  # 第0个是本体，后面是的Model_list
        col_info_list = table_mng_obj.get_col_list(table_name)
        model_type_dict = self._get_all_model_type_info(pg, table_name)  # 获取model的title, name, category
        if action_type == 2:  # 删除
            return 'delete', diff_data  # 删除
        prev_rows = self._get_log_info(pg, prev_log_ref_id)
        if prev_rows:
            prev_table_name, prev_classify = prev_rows[0][2:4]
            if table_name != prev_table_name or classify != prev_classify:
                print ('table_name or classify is error. curr_log_ref_id=%s, prev_log_ref_id = %s'
                       % (curr_log_ref_id, prev_log_ref_id))
                return None, diff_data
        else:
            curr_base_data, model_dict = self._convert_2_full_data(col_info_list, model_type_dict, curr_rows)
            if curr_base_data.get('hu_id'):
                diff_data['id'] = curr_base_data.get('hu_id')
            elif curr_base_data.get('definition_id'):
                diff_data['id'] = curr_base_data.get('definition_id')
            return 'add', diff_data  # 新增
        curr_base_data, model_dict = self._convert_2_full_data(col_info_list, model_type_dict, curr_rows)
        prev_base_data, prev_model_dict = self._convert_2_full_data(col_info_list, model_type_dict, prev_rows)
        # 合并前后两版基本数据
        for col_name in curr_base_data.iterkeys():
            if col_name in HIDE_COLS:
                continue
            col_data = curr_base_data.get(col_name)
            prev_col_data = prev_base_data.get(col_name)
            if col_name in ('hu_id', 'definition_id'):
                diff_data['id'] = col_data
            if prev_col_data:
                col_data["old_val"] = prev_col_data.get("val")
            else:
                col_data["old_val"] = None
            # self._replace_character(col_data)  # \n替换行<br>
            col_data["changed"] = self._get_val_action_type(col_data.get("val"), col_data.get("old_val"))
            if col_data["changed"] in ("add", "delete", "change"):
                diff_data[col_name] = col_data
        merged_model_list = self._merge_model_list_for_checklist(model_dict, prev_model_dict)
        if not merged_model_list and not diff_data:
            return "change", {}
        diff_data["model_list"] = merged_model_list
        return "change", diff_data

    def _replace_character(self, data):
        val = data.get("val")
        if val:
            data["val"] = self._replace_new_line_ch(val)
        old_val = data.get("old_val")
        if val:
            data["old_val"] = self._replace_new_line_ch(old_val)

    def _replace_new_line_ch(self, val):
        if val and type(val) in (str, unicode):
            return val.replace('\n', '<br>')
        return val

    def _merge_model_list(self, curr_model_dict, prev_model_dict):
        """合并前后两版Model_list"""
        merged_model_list = []
        model_id_list = list(sorted(set(curr_model_dict.keys() + prev_model_dict.keys())))
        for model_id in model_id_list:
            curr_model = curr_model_dict.get(model_id)
            prev_model = prev_model_dict.get(model_id)
            if curr_model:
                if prev_model:
                    curr_model["old_val"] = prev_model.get("val")
                else:
                    curr_model["old_val"] = MODEL_DEFAULT_VAL
                curr_model["changed"] = self._get_val_action_type(curr_model.get("val"), curr_model.get("old_val"))
                self._replace_character(curr_model)  # \n替换行<br>
                merged_model_list.append(curr_model)
            else:
                prev_model["old_val"] = prev_model.get("val")
                prev_model["val"] = MODEL_DEFAULT_VAL
                prev_model["changed"] = self._get_val_action_type(prev_model.get("val"), prev_model.get("old_val"))
                self._replace_character(prev_model)  # \n替换行<br>
                merged_model_list.append(prev_model)
        return merged_model_list

    def _merge_model_list_for_checklist(self, curr_model_dict, prev_model_dict):
        merged_model_list = []
        model_id_list = list(sorted(set(curr_model_dict.keys() + prev_model_dict.keys())))
        for model_id in model_id_list:
            curr_model = curr_model_dict.get(model_id)
            prev_model = prev_model_dict.get(model_id)
            if curr_model:
                if prev_model:
                    curr_model["old_val"] = prev_model.get("val")
                else:
                    curr_model["old_val"] = MODEL_DEFAULT_VAL
                curr_model["changed"] = self._get_val_action_type(curr_model.get("val"), curr_model.get("old_val"))
                if curr_model["changed"] in ("add", "delete", "change"):
                    merged_model_list.append(curr_model)
            else:
                prev_model["old_val"] = prev_model.get("val")
                prev_model["val"] = MODEL_DEFAULT_VAL
                prev_model["changed"] = self._get_val_action_type(prev_model.get("val"), prev_model.get("old_val"))
                if prev_model["changed"] in ("add", "delete", "change"):
                    merged_model_list.append(prev_model)
        return merged_model_list

    def _get_val_action_type(self, new_val, old_val):
        if new_val == old_val:
            return 'same'
        else:
            if not old_val and not new_val:  # 一个是None, 一个是空字符
                return 'same'
            elif not old_val:
                return 'add'
            elif not new_val:
                return 'delete'
            else:
                return 'change'

    def category_model_list(self, model_list, table_name):
        """按部品分类"""
        if table_name in ('hu', 'basic_req_hu'):
            from Source.spec2db_server.arl.hu_server import HuRecord
            obj = HuRecord()
            categoryed_model = obj.category_model_list(model_list)
            return categoryed_model
        elif table_name == 'definition':
            return model_list
        elif table_name in ('analysis', 'basic_req_analysis'):
            from Source.spec2db_server.arl.analysis_service import AnalysisRecord
            obj = AnalysisRecord()
            categoryed_model = obj.category_model_list(model_list)
            return categoryed_model

    def _get_all_model_type_info(self, pg, table_name):
        """获取model的title, name, category"""
        model_info_dict = dict()
        if table_name in ('hu', 'basic_req_hu'):
            from Source.spec2db_server.arl.hu_server import HuRecord
            obj = HuRecord()
            model_info_dict = obj.get_all_model_types(pg)
        elif table_name in ('definition', 'basic_req_definition'):
            from Source.spec2db_server.arl.def_server import DefRecord
            obj = DefRecord()
            model_info_dict = obj.get_all_model_types(pg)
        elif table_name in ('analysis', 'basic_req_analysis'):
            from Source.spec2db_server.arl.analysis_service import AnalysisRecord
            obj = AnalysisRecord()
            model_info_dict = obj.get_all_model_types(pg)
        return model_info_dict

    def _convert_2_full_data(self, col_info_list, model_type_dict, record_data_list):
        if not record_data_list:
            return dict(), dict()
        action_type, status_flag, column_info = record_data_list[0][-3], record_data_list[0][-2], record_data_list[0][-1]
        base_data = self._convert_2_base_data(col_info_list, action_type, status_flag, column_info)
        model_dict = self._convert_model_list(record_data_list[1:], model_type_dict)
        return base_data, model_dict

    def _convert_2_base_data(self, col_info_list, action_type, status_flag, column_info):
        if not column_info:
            return {}
        if action_type == COMMIT_ACTION.get("delete"):  # 删除
            return {}
        record_data = dict()
        min_len = min([len(column_info), len(col_info_list)])
        for i in xrange(0, min_len):
            col_data = dict()
            col_info = col_info_list[i]
            col_name = col_info.get("col_name")  # 字段名称
            col_data["title"] = col_info.get("col_disp_name")  # 表示Title名称
            col_data["changed"] = status_flag[i]
            col_data["val"] = column_info[i]
            record_data[col_name] = col_data
        return record_data

    def _convert_model_list(self, record_data_list, model_type_dict):
        model_dict = dict()
        for record in record_data_list:
            action_type = record[-3]
            if action_type == COMMIT_ACTION.get("delete"):  # 删除
                continue
            status_flag = record[-2]
            column_info = record[-1]
            if len(column_info) != 4:  # TODO: 后续要改
                break
            if column_info[-2]:
                model_id = int(column_info[-2])
            else:
                print 'Error Model_id = %s' % column_info[-2]
                continue
            val = column_info[-1]
            model_type = model_type_dict.get(model_id)
            if not model_type:
                print 'Error Model_id = %s' % model_id
                continue
                # return None
            temp_model_type = copy.deepcopy(model_type)
            temp_model_type["val"] = val
            temp_model_type["changed"] = status_flag[-1]
            model_dict[model_id] = temp_model_type
        return model_dict

    def _get_log_info(self, pg, commit_log_ref_id):
        sqlcmd = """
            SELECT commit_id, t1.commit_log_ref_id, t3.table_name, classify, 
                   record_id, action_type, status_flag, column_info
              FROM {schema}.commit_log_ref AS t1
              LEFT JOIN {schema}.commit_log_info AS t2
              ON t1.commit_log_ref_id = t2.commit_log_ref_id
              LEFT JOIN {schema}.log_table_map as t3
              ON t1.table_id = t3.table_id
              WHERE t1.commit_log_ref_id = %s
              ORDER BY commit_log_info_id
            """.format(schema=self.schema)
        pg.execute(sqlcmd, [commit_log_ref_id])
        rows = pg.fetchall()
        return rows

    def _get_prev_log_info(self, pg, commit_log_ref_id, table_name, record_id):
        sqlcmd = """
            SELECT commit_log_info_id, commit_log_ref_id, record_id,
                   action_type, status_flag, column_info
              FROM {schema}.commit_log_info
              WHERE commit_log_ref_id IN (
                  SELECT commit_log_ref_id
                    FROM {schema}.commit_log_info
                    WHERE commit_log_ref_id < %s
                    and record_id = %s
                    and table_name = %s
                   ORDER BY commit_log_info_id DESC
                   LIMIT 1
              )
              order by commit_log_info_id 
            """.format(schema=self.schema)
        pg.execute(sqlcmd, [commit_log_ref_id, record_id, table_name])
        rows = pg.fetchall()
        return rows

    def get_commit_log_by_id(self, classify, _id):
        result = {"result": "NG"}
        if classify == "arl":
            sql_cmd = '''
                SELECT  arl_record_id
                        FROM {schema}.arl
                        where arl_id = %s
                '''.format(schema=self.schema)
            r_id = None
            try:
                self._pg.connect()
                self._pg.execute(sql_cmd, (_id,))
                row = self._pg.fetchone()
                r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "hu":
            sql_cmd = '''
                SELECT  hu_record_id
                        FROM {schema}.hu
                        where hu_id = %s
                '''.format(schema=self.schema)
            r_id = None
            try:
                self._pg.connect()
                self._pg.execute(sql_cmd, (_id,))
                row = self._pg.fetchone()
                r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "definition":
            sql_cmd = '''
                SELECT  def_rc_id
                        FROM {schema}.definition
                        where definition_id = %s
                '''.format(schema=self.schema)
            r_id = None
            try:
                self._pg.connect()
                self._pg.execute(sql_cmd, (_id,))
                row = self._pg.fetchone()
                r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "analysis":
            sql_cmd = '''
                SELECT  analysis_rc_id
                        FROM {schema}.analysis
                        where analysis_id = %s
                '''.format(schema=self.schema)
            r_id = None
            try:
                self._pg.connect()
                self._pg.execute(sql_cmd, (_id,))
                row = self._pg.fetchone()
                r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "basic_req_hu":
            sql_cmd = '''
                SELECT  hu_record_id
                        FROM {schema}.hu
                        where hu_id = %s
                '''.format(schema=self.schema)
            sql_cmd2 = '''
                SELECT  hu_record_id
                        FROM {schema}.basic_req_hu
                        where hu_id = %s
                '''.format(schema=self.schema)
            r_id = None
            type_id = str(_id)
            try:
                self._pg.connect()
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    self._pg.execute(sql_cmd, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
                else:
                    self._pg.execute(sql_cmd2, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    type = "hu"
                    result = obj.get_commit_log_by_classify_and_record_id(type, r_id)
                else:
                    result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "basic_req_definition":
            sql_cmd = '''
                SELECT  def_rc_id
                        FROM {schema}.definition
                        where definition_id = %s
                '''.format(schema=self.schema)
            sql_cmd2 = '''
                SELECT  def_rc_id
                        FROM {schema}.basic_req_definition
                        where definition_id = %s
                '''.format(schema=self.schema)
            r_id = None
            type_id = str(_id)
            try:
                self._pg.connect()
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    self._pg.execute(sql_cmd, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
                else:
                    self._pg.execute(sql_cmd2, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    type = "definition"
                    result = obj.get_commit_log_by_classify_and_record_id(type, r_id)
                else:
                    result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        elif classify == "basic_req_analysis":
            sql_cmd = '''
                SELECT  analysis_rc_id
                        FROM {schema}.analysis
                        where analysis_id = %s
                '''.format(schema=self.schema)
            sql_cmd2 = '''
                SELECT  analysis_rc_id
                        FROM {schema}.basic_req_analysis
                        where analysis_id = %s
                '''.format(schema=self.schema)
            r_id = None
            type_id = str(_id)
            try:
                self._pg.connect()
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    self._pg.execute(sql_cmd, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
                else:
                    self._pg.execute(sql_cmd2, (_id,))
                    row = self._pg.fetchone()
                    if row:
                        r_id = row[0]
            except Exception as e:
                print e
            finally:
                self._pg.close()
            obj = HmiLog()
            if r_id:
                if type_id[0] != 'B' and type_id[0] != 'C' and type_id[0] != 'D':
                    type = "analysis"
                    result = obj.get_commit_log_by_classify_and_record_id(type, r_id)
                else:
                    result = obj.get_commit_log_by_classify_and_record_id(classify, r_id)
        return result

    def get_checklist_brief(self, pg, start_time, end_time):
        check_lists = []
        data_list = self._get_checklist_brief(pg, start_time, end_time)
        for (table_name, _id, commit_ids, commit_log_ref_ids,
             author_check_results, charger_check_results, record_id) in data_list:
            curr_log_ref_id = max(commit_log_ref_ids)
            prev_log_ref_id = self._get_last_log_ref_id(pg, table_name, record_id, start_time)
            action_type, diff_data = self._diff_log_data(pg, prev_log_ref_id, curr_log_ref_id)
            if action_type == "change" and not diff_data:  # 只是隐藏列内容更改
                continue
            check_brief = dict()
            check_brief["table_name"] = table_name
            if not _id:
                _id = diff_data['id'].get('val')
            check_brief["id"] = _id
            check_brief["commit_ids"] = commit_ids
            check_brief["author_check_results"] = author_check_results
            check_brief["charger_check_results"] = charger_check_results
            check_brief["action_type"] = action_type
            check_brief["diff_data"] = diff_data
            check_lists.append(check_brief)
        return check_lists

    def _get_checklist_brief(self, pg, start_time, end_time):
        table_infos = [{"table_name": "hu", "key_col": "hu_record_id", "id_col": "hu_id"},
                       {"table_name": "basic_req_hu", "key_col": "hu_record_id", "id_col": "hu_id"},
                       {"table_name": "definition", "key_col": "def_rc_id", "id_col": "definition_id"},
                       {"table_name": "basic_req_definition", "key_col": "def_rc_id", "id_col": "definition_id"},
                       {"table_name": "analysis", "key_col": "analysis_rc_id", "id_col": "definition_id"},
                       {"table_name": "basic_req_analysis", "key_col": "analysis_rc_id", "id_col": "definition_id"},
                       ]
        data_list = []
        for table_info in table_infos:
            sqlcmd = """
                SELECT table_name, {id_col}, 
                       array_agg(commit_id) as commit_ids,
                       array_agg(commit_log_ref_id) as commit_log_ref_ids, 
                       --array_agg(commit_time) as commit_time,
                       array_agg(author_check_result) as author_check_results,
                       array_agg(charger_check_result) as charger_check_results,
                       record_id
                  FROM (
                      SELECT table_name, {id_col}, t1.commit_id,
                             t3.commit_log_ref_id, commit_time, 
                             array_to_string(author_check_result, ',') author_check_result,
                             array_to_string(charger_check_result, ',') charger_check_result,
                             record_id
                      FROM (
                            SELECT commit_id, user_id, group_id, commit_time
                              FROM {schema}.commit_log
                              where commit_time >= %s
                                    and commit_time <= %s
                      ) as t1
                      left join {schema}.commit_log_ref as t2
                      on t1.commit_id = t2.commit_id
                      left join {schema}.commit_log_info as t3
                      on t2.commit_log_ref_id = t3.commit_log_ref_id
                      left join {schema}.{req_table} as t4
                      on t3.record_id = t4.{key_col}
                      left join (
                        SELECT commit_id, classfy, 
                            array_agg(author_check) as author_check_result, 
                            array_agg(charger_check) as charger_check_result
                          FROM {schema}.check_list
                          group by commit_id, classfy
                          order by commit_id
                      ) as t5
                      on t1.commit_id = t5.commit_id and table_name = classfy
                      where table_name in ('{req_table}') and action_type in (0, 1, 2) -- "add": 0, "change": 1, "delete": 2
                      ORDER BY table_name, record_id, commit_log_info_id DESC
                  ) as tt1
                  group by table_name, {id_col}, record_id
                  order by table_name, length({id_col}), {id_col}
                """.format(schema=self.schema,
                           req_table=table_info.get("table_name"),
                           key_col=table_info.get("key_col"),
                           id_col=table_info.get("id_col")
                           )
            pg.execute(sqlcmd, [start_time, end_time])
            rows = pg.fetchall()
            data_list += rows
        return data_list

    def get_cimmit_log_by_id(self, commit_id):
        sqlcmd = """
                SELECT user_name, group_name, commit_time
                FROM {schema}.commit_log AS t1 LEFT JOIN {schema}.arl_user AS t2 ON t1.user_id = t2.user_id
                LEFT JOIN {schema}.arl_group AS t3 ON t1.group_id = t3.group_id 
                WHERE commit_id = %s;
            """.format(schema=self.schema)
        self._pg.connect()
        self._pg.execute(sqlcmd, (commit_id,))
        row = self._pg.fetchone()
        self._pg.close()

        commit_data = {'user_name': row[0], 'group_name': row[1], 'commit_time': row[2]}
        return commit_data


def main():
    import os
    os.chdir('../')
    log = HmiLog()
    # result = log.get_commit_log_detail(96, commit_log_ref_id=0)
    start_time, end_time = '2018-01-08 23:59:59', '2018-01-15 23:59:59'
    log._pg.connect()
    data_list = log.get_checklist_brief(log._pg, start_time, end_time)
    log._pg.close()
    return data_list


if __name__ == '__main__':
    import sys

    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()