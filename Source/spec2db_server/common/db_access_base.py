# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hcz
"""
import time
from Source.spec2db_server.common import db


class DBAccessBase(object):
    """
    """
    def __init__(self):
        self._pg = db.pg()

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
        SELECT {strcolumn} \n FROM spec.{table} \n {condition_str} \n{order_str};
        """.format(table=table_name,
                   strcolumn=strcolumn,
                   condition_str=condition_str,
                   order_str=order_str)
        return sqlcmd

    def list_2_insert_sql(self, table_name, col_list, key_col):
        strcolumn = self.list_2_col_str(col_list)
        pecent_str = self.percent_str(len(col_list))
        sqlcmd = """
        insert into spec.{table} ({strcolumn}) \n values({pecent_str}) returning {key_col};
        """.format(table=table_name,
                   strcolumn=strcolumn,
                   pecent_str=pecent_str,
                   key_col=key_col)
        return sqlcmd

    def list_2_update_sql(self, table_name, update_col_list, condition_col_list, key_col):
        update_str = self.list_2_update_str(update_col_list)
        condition_str = self.list_2_condition_str(condition_col_list)
        sqlcmd = """
        update spec.{table} set {update_str} \n {condition_str} \nreturning {key_col};
        """.format(table=table_name,
                   update_str=update_str,
                   condition_str=condition_str,
                   key_col=key_col)
        return sqlcmd

    def list_2_delete_sql(self, table_name, condition_col_list):
        condition_str = self.list_2_condition_str(condition_col_list)
        sqlcmd = """
        delete from spec.{table} {condition_str};
        """.format(table=table_name,
                   condition_str=condition_str)
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

    def get_filter_condition(self, filter_dict):
        cond_list = []
        if filter_dict:
            for key, val in filter_dict.iteritems():
                if key and val:
                    val = val.replace('.', '\\.')
                    s = key + """ like '%%""" + val + """%%'"""
                    cond_list.append(s)
        return ' and '.join(cond_list)

    def generate_md5_key(self, data):
        import hashlib
        m = hashlib.md5(str(data))
        return m.hexdigest()

    def get_current_time(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def get_current_date(self):
        return time.strftime("%Y-%m-%d")
