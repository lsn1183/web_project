# -*- coding: UTF-8 -*-
"""
Created on 2011-9-16
用来连接数据库
@author: HCZ
"""
import psycopg2
import psycopg2.extensions
import psycopg2.extras
from Source.spec2db_server.common import config

BATCH_SIZE = 1024 * 10


class pg(object):
    # __instance = None
    #
    # @staticmethod
    # def instance():
    #     if pg.__instance is None:
    #         pg.__instance = pg()
    #     return pg.__instance

    def __init__(self, auto_connect=False):
        #psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
        self.connected = False
        self.srv_path = config.CConfig.instance().getPara('db')
        self.recordno = 0
        self.conn = None
        self.pgcur = None
        if auto_connect:
            self.connect()

    def __del__(self):
        self.close()
        # self.close2()

    def connect(self, cursor_type=None):
        """连接源数据库"""
        if not self.connected:
            self.conn = psycopg2.connect(self.srv_path)  # 源数据库
            if not cursor_type:
                self.pgcur = self.conn.cursor()
            else:
                self.pgcur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.connected = True

    def deletetabledata(self, table_name):
        """删除目标数据库表中的数据"""
        sqlcmd = "delete from " + table_name
        try:
            self.pgcur.execute(sqlcmd)
            self.conn.commit()
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            # raise Exception, 'database operate wrong'
            raise

    def query(self, sqlcmd):
        """在源数据库表查询数据"""
        try:
            self.pgcur.execute(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def query_fromcur(self, sqlcmd):
        """在源数据库表查询数据"""
        try:
            self.pgcur.execute(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def execute(self, sqlcmd, parameters=None):
        """往目标数据库表插入数据"""
        if not parameters:
            parameters = []
        try:
            if parameters:
                self.pgcur.execute(sqlcmd, parameters)
                # print self.pgcur.mogrify(sqlcmd, parameters)
            else:
                self.pgcur.execute(sqlcmd)
                # print self.pgcur.mogrify(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            # rdb_log.log('DataBase', 'SQL excute error:' + sqlcmd, 'info')
            raise

    def fetchone(self):
        """读一条记录"""
        return self.pgcur.fetchone()

    def fetchall(self):
        return self.pgcur.fetchall()

    def commit(self):
        self.conn.commit()

    def close(self):
        if self.connected:
            self.pgcur.close()
            self.conn.close()
            self.connected = False

    def closeall(self):
        # 关闭源数据库连接
        self.close1()
        # 关闭目标数据库连接
        # self.close2()

    def analyze(self, table_name):
        sqlcmd = 'analyze %s;' % table_name
        self.pgcur.execute(sqlcmd)
        self.conn.commit()

    def copy_to(self, file_object, table, sep=r'\t', null=r'\N', columns=None):
        self.pgcur.copy_to(file_object, table, sep, null, columns)

    def copy_from(self, file_object, table, sep=r'\t',
                  null=r"", size=8192, columns=None):
        try:
            self.pgcur.copy_from(file_object, table, sep, null, size, columns)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def batch_query(self, sql, parameters=(), batch_size=BATCH_SIZE):
        try:
            curs = self.conn.cursor(name='batch')
            curs.arraysize = batch_size
            # print curs.mogrify(sql, parameters)
            curs.execute(sql, parameters)
            while True:
                rows = curs.fetchmany()
                if not rows:
                    break
                yield rows

        except psycopg2.DatabaseError as e:
            raise

        finally:
            curs.close()

    def get_batch_data(self, sqlcmd, parameters=(), batch_size=BATCH_SIZE):
        row_data = list()
        for rows in self.batch_query2(sqlcmd, parameters, batch_size):
            for row in rows:
                if not row:
                    break
                row_data = row
                yield row_data

    def get_curr_db(self):
        if self.srv_path:
            e_dict = {}
            for e in self.srv_path.split(' '):
                e = e.strip()
                key, val = e.split('=')
                e_dict[key.strip()] = val.strip()[1:-1]
            return e_dict.get("dbname")
        return None

    def get_columns_info(self, table_name):
        sqlcmd = """
        -------------------------------------------------------
        SELECT attname,
               col_description(a.attrelid, a.attnum) as comment, -- 注释
               format_type(a.atttypid, a.atttypmod) as type -- 类型       
          FROM pg_attribute as a
          --where attname = 'bug_type'
          where attrelid in (
            SELECT oid
              FROM pg_class
              where relname = '%s'
          ) and attnum > 0
          order by attrelid, attnum
        -------------------------------------------------------
        """
        self.pgcur.execute(sqlcmd, [table_name])
        rows = self.pgcur.fetchall()
        return rows
