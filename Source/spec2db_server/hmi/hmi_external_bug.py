# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_base import HMIBase
import time

class HmiExternalBug(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)
        self.table_name = 'external_bug'
        self.key_col = 'bug_rc_id'
        self.id_col = 'bug_id'
        self.attr_list = [
            'bug_rc_id', 'bug_type', 'bug_keyword', 'bug_id', 'summary',
            'charger', 'reporter', 'priority', 'status', 'result',
            'create_date', 'update_date', 'arrive_date', 'detail'
        ]

    def get_old_data(self, pg, id_val):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, (str(id_val),))
        row = pg.fetchone()

        detail_data_list = []
        if row:
            detail_data_list.append(dict(zip(self.attr_list, row)))

        return detail_data_list

    def get_by_id(self, qa_no):
        detail_data = self._get_by_id(qa_no)
        return detail_data

    def _get_by_id(self, qa_no):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        self._pg.connect()
        self._pg.execute(sqlcmd, (qa_no,))
        row = self._pg.fetchone()
        detail_data = dict()
        for i in range(0, len(self.attr_list)):
            detail_data[self.attr_list[i]] = row[i]
        self._pg.close()
        return detail_data

    def get_qa_list(self, page, size):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [])
        sqlcmd += "ORDER BY bug_rc_id DESC"
        qa_list = []
        try:
            self._pg.connect()
            rowcount, rows = self._fetch_many(self._pg, sqlcmd, [], size, page)
            # rowcount = self._pg.pgcur.rowcount
            for row in rows:
                detail_data = dict()
                for i in range(0, len(self.attr_list)):
                    detail_data[self.attr_list[i]] = row[i]
                qa_list.append(detail_data)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return rowcount, qa_list

    def update_datalist(self, data_list):
        result = {'result': 'OK'}
        self._pg.connect()
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        for data_dict in data_list:
            self._common_add(self._pg, data_dict, update_time, self.attr_list)

        self._pg.commit()
        self._pg.close()

        return result

    def delete_by_dbid(self, db_id):
        result = {'result': 'OK'}
        self._pg.connect()
        del_sql = self.list_2_delete_sql(self.table_name, [self.key_col])
        self._pg.execute(del_sql, (db_id, ))
        self._pg.close()

        return result

    def delete_by_idlist(self, db_id_list):
        result = {'result': 'OK'}
        self._pg.connect()
        del_sql = self.list_2_delete_sql(self.table_name, [self.key_col])
        for db_id in db_id_list:
            self._pg.execute(del_sql, (db_id,))
        self._pg.close()

        return result
