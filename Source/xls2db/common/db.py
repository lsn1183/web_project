# -*- coding: cp936 -*-
"""
Created on 2011-9-16
用来连接数据库
@author: hongchenzai
"""
import psycopg2
from Source.xls2db.common import config

BATCH_SIZE = 1024 * 10


class pg(object):
    __instance = None

    @staticmethod
    def instance():
        if pg.__instance is None:
            pg.__instance = pg()
        return pg.__instance

    def __init__(self, auto_connect=False):
        self.connected1 = False
        self.connected2 = False
        self.connected_base = False

        self.srv_path1 = config.CConfig.instance().getPara('db1')
        self.srv_path2 = config.CConfig.instance().getPara('db2')
        self.recordno = 0
        if auto_connect:
            self.connect2()
        self.conn1 = None
        self.pgcur1 = None

    def __del__(self):
        self.close1()
        self.close2()

    def connect1(self):
        """连接源数据库"""
        self.conn1 = psycopg2.connect(self.srv_path1)  # 源数据库
        self.pgcur1 = self.conn1.cursor()
        self.connected1 = True

    def connect2(self):
        """连接目标数据库"""
        self.conn2 = psycopg2.connect(self.srv_path2)   # 目标数据库
        self.pgcur2 = self.conn2.cursor()
        self.connected2 = True

    def deletetabledata(self, table_name):
        """删除目标数据库表中的数据"""
        sqlcmd = "delete from " + table_name
        try:
            self.pgcur2.execute(sqlcmd)
            self.conn2.commit()
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            # raise Exception, 'database operate wrong'
            raise

    def deletetabledata1(self, table_name):
        """删除目标数据库表中的数据"""
        sqlcmd = "delete from " + table_name
        try:
            self.pgcur1.execute(sqlcmd)
            self.conn1.commit()
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def query(self, sqlcmd):
        """在源数据库表查询数据"""
        try:
            self.pgcur1.execute(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def query_fromcur2(self, sqlcmd):
        """在源数据库表查询数据"""
        try:
            self.pgcur2.execute(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def execute1(self, sqlcmd, parameters=None):
        """往目标数据库表插入数据"""
        if not parameters:
            parameters = []
        try:
            self.pgcur1.execute(sqlcmd, parameters)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            # rdb_log.log('DataBase', 'SQL excute error:' + sqlcmd, 'info')
            raise

    def execute2(self, sqlcmd, parameters=None):
        """往目标数据库表插入数据"""
        if not parameters:
            parameters = []
        try:
            if parameters:
                self.pgcur2.execute(sqlcmd, parameters)
            else:
                self.pgcur2.execute(sqlcmd)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            # rdb_log.log('DataBase', 'SQL excute error:' + sqlcmd, 'info')
            raise

    def getcnt1(self):
        """往目标数据库表插入数据"""
        return self.pgcur1.rowcount

    def callproc(self, proc_name, parameters=None):
        """调用目标数据库的存储过程"""
        if not parameters:
            parameters = None
        try:
            self.pgcur2.callproc(proc_name, parameters)
            self.recordno += 1
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def fetchone(self):
        """读一条记录"""
        return self.pgcur1.fetchone()

    def fetchone2(self):
        """读一条记录"""
        return self.pgcur2.fetchone()

    def fetchone_fromcur2(self):
        """读一条记录"""
        return self.pgcur2.fetchone()

    def fetchall(self):
        return self.pgcur1.fetchall()

    def fetchall2(self):
        return self.pgcur2.fetchall()

    def commit1(self):
        self.conn1.commit()

    def commit2(self):
        self.conn2.commit()

    def close1(self):
        if self.connected1:
            self.pgcur1.close()
            self.conn1.close()
            self.connected1 = False

    def close2(self):
        self.recordno = 0
        if self.connected2:
            self.pgcur2.close()
            self.conn2.close()
            self.connected2 = False

    def closeall(self):
        # 关闭源数据库连接
        self.close1()
        # 关闭目标数据库连接
        self.close2()

    def analyze(self, table_name):
        sqlcmd = 'analyze %s;' % table_name
        self.pgcur2.execute(sqlcmd)
        self.conn2.commit()

    def copy_to(self, file_object, table, sep=r'\t', null=r'\N', columns=None):
        self.pgcur1.copy_to(file_object, table, sep, null, columns)

    def copy_from1(self, file_object, table, sep=r'\t',
                   null=r"", size=8192, columns=None):
        try:
            self.pgcur1.copy_from(file_object, table, sep, null, size, columns)
            return 0
        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def copy_from2(self, file_object, table, sep='\t',
                   null="", size=8192, columns=None):
        try:
            self.pgcur2.copy_from(file_object, table, sep, null, size, columns)
            return 0

        except Exception, ex:
            print '%s:%s' % (Exception, ex)
            raise

    def batch_query2(self, sql, parameters=(), batch_size=BATCH_SIZE):
        try:
            curs = self.conn2.cursor(name='batch2')
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

    def get_batch_data2(self, sqlcmd, parameters=(), batch_size=BATCH_SIZE):
        row_data = list()
        for rows in self.batch_query2(sqlcmd, parameters, batch_size):
            for row in rows:
                if not row:
                    break
                row_data = row
                yield row_data
