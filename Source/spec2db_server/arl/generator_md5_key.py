# -*- coding: UTF-8 -*-
"""
Created on 2017-10-24

@author:
"""
import time

from Source.spec2db_server.arl.arl_base import ServiceBase

class GeneratorMd5Key(ServiceBase):
    """

    """
    def __init__(self,):
        ServiceBase.__init__(self)
        self._pg.connect()

    def add_md5_column(self, table_name):
        sql_cmd = '''ALTER TABLE spec.%s ADD md5_key varchar;'''
        self._pg.execute(sql_cmd % table_name)
        self._pg.commit()

    def get_table_column_names(self, table_name):
        # 获取hu表的所有字段名
        self._pg.connect()
        sql_cmd = '''SELECT col_name FROM spec.log_col_map AS a 
                            JOIN spec.log_table_map AS b ON a.table_id = b.table_id
                            WHERE b.table_name = '%s' ORDER BY col_id;'''
        self._pg.execute(sql_cmd % table_name)
        rows = self._pg.fetchall()
        columns_name = []
        for row in rows:
            columns_name.append(row[0])
        self._pg.close()
        return ','.join(columns_name[1:])

    def join_md5_parm(self, table, columns_name):
        print('table_name:%s' % table['table_name'])
        self._pg.connect()
        sql_cmd = '''SELECT %s, %s FROM spec.%s;'''
        self._pg.execute(sql_cmd % (table['pk_column_name'], columns_name, table['table_name']))
        rows = self._pg.fetchall()
        for row in rows:
            pk_id = row[0]
            # print("table_name:%s, record_id:%s, " % (table['table_name'], pk_id))
            column_num = len(row) - 1
            val_str = ""
            i = 1
            while i < column_num:
                val_str += str(row[i]) + ','
                i += 1
            sql_cmd = '''SELECT %s FROM spec.%s AS a JOIN spec.%s AS b ON a.%s = b.%s where b.%s = %s ORDER BY a.%s;'''
            self._pg.execute(sql_cmd % (','.join(table['relation_table_columns']), table['relation_table_name'],
                                        table['table_name'], table['condition_column_name'],
                                        table['rel_condition_column_name'], table['pk_column_name'], pk_id,
                                        table['order_by_condition']))
            rrs = self._pg.fetchall()
            if rrs:
                for rr in rrs:
                    for r in rr:
                        val_str += str(r) + ','
            val_str = val_str[0:-1]
            sql_cmd = '''UPDATE spec.%s
                         SET md5_key = md5($$%s$$)
                         WHERE %s = %s;
            '''
            try:
                self._pg.execute(sql_cmd % (table['table_name'], val_str, table['pk_column_name'], pk_id))
            except Exception as e:
                print e
                return None
        self._pg.commit()
        self._pg.close()
        return 'OK'

    def generator_hu_md5_key(self, table):
        self._pg.connect()
        self.add_md5_column(table['table_name'])
        columns_name = self.get_table_column_names(table['table_name'])
        if columns_name:
            if self.join_md5_parm(table, columns_name):
                print('Successfully generator md5 key of table:%s' % table['table_name'])
        else:
            print('table:%s 没有字段.' % table['table_name'])
        self._pg.close()


if __name__ == "__main__":
    tables = [
              {'table_name': 'hu', 'pk_column_name': 'hu_record_id', 'relation_table_name': 'hu_model_rel',
               'condition_column_name': 'hu_record_id', 'rel_condition_column_name': 'hu_record_id',
               'relation_table_columns':['model_id', 'val'], 'order_by_condition':'model_id'},
              {'table_name': 'definition', 'pk_column_name': 'def_rc_id', 'relation_table_name': 'definition_model_rel',
               'condition_column_name': 'def_rc_id', 'rel_condition_column_name': 'def_rc_id',
               'relation_table_columns': ['model_id', 'val'], 'order_by_condition':'model_id'},
              {'table_name': 'arl', 'pk_column_name': 'arl_record_id', 'relation_table_name': 'arl_model_rel',
               'condition_column_name': 'arl_record_id', 'rel_condition_column_name': 'arl_record_id',
               'relation_table_columns': ['model_id', 'val'], 'order_by_condition':'model_id'}
              ]
    for table in tables:
        gen_md5_key = GeneratorMd5Key()
        gen_md5_key.generator_hu_md5_key(table)


