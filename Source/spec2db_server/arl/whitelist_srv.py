
# -*- coding: UTF-8 -*-
"""
Created on 2017-11-22

@author: hcz
"""
from Source.spec2db_server.arl.arl_base import ServiceBase


class WhitelistSrv(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "white_list"
        self.key_col = "wl_rc_id"
        self.attr_list = ["wl_rc_id", "classify", "id", "agree",
                          "import_user_id", "import_time", "agree_time",
                          "agree_user_id"
                          ]

    def get_white_list(self, condition=None):
        sqlcmd = """
        SELECT classify, id, agree, t2.user_name as import_user, import_time, 
               agree_time, t3.user_name as agree_name
          FROM spec.white_list as t1
          LEFT JOIN spec.arl_user as t2
          on t1.import_user_id = t2.user_id
          left join spec.arl_user as t3
          on t1.agree_user_id = t3.user_id
          ORDER BY import_time desc
        """
        white_list = []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd)
            rows = self._pg.fetchall()
            attr_list = ["classify", "id", "agree", "import_user",
                         "import_time", "agree_time", "agree_user"]
            for row in rows:
                data = dict()
                for i, attr in enumerate(attr_list, 0):
                    data[attr] = row[i]
                white_list.append(data)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return white_list

    def agree(self, white_list, user_id):
        agree_time = self.get_current_time()
        try:
            self._pg.connect()
            for data in white_list:
                classify = data.get("classify")
                agree = data.get("agree")
                _id = data.get("id")
                params = [agree, agree_time, user_id, classify, _id]
                self._agree(self._pg, params)
            self._pg.commit()
            return True
        except Exception as e:
            print e
            if self._pg.connected:
                self._pg.conn.rollback()
                self._pg.close()
            return False

    def _agree(self, pg, params):
        sqlcmd = """
        UPDATE spec.white_list
           SET agree=%s, agree_time=%s, agree_user_id=%s
         WHERE classify = %s and id = %s;
        """
        pg.execute(sqlcmd, params)

    def get_white_list_by_classify(self, pg=None):
        sqlcmd = """
        SELECT classify, array_agg(id)
          FROM (
            select classify, id
              from spec.white_list
              where agree = 1
          ) AS a
          group by classify
        """
        white_list = dict()
        if not pg:
            pg = self._pg.connect()
            pg.execute(sqlcmd)
            rows = pg.fetchall()
            pg.close()
        else:
            pg.execute(sqlcmd)
            rows = pg.fetchall()
        for row in rows:
            classify = row[0]
            white_list[classify] = row[1]
        return white_list
