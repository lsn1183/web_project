# -*- coding: UTF-8 -*-
"""
Created on 2017-12-13

@author: hcz
"""
from Source.spec2db_server.arl.arl_base import ServiceBase


class ArlSrvStatus(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "arl_server_status"

    def set_srv_status(self, status=False):
        sqlcmd = """
        update spec.arl_server_status set lock_table = %s
        """
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, (status,))
            self._pg.commit()
        except Exception as e:
            print e
        finally:
            self._pg.close()

    def get_srv_status(self):
        sqlcmd = """
        SELECT lock_table
          FROM spec.arl_server_status
          limit 1
        """
        lock = False
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd)
            row = self._pg.fetchone()
            if row:
                if row[0]:
                    lock = True
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return lock
