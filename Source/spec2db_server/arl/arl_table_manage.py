# -*- coding: UTF-8 -*-
"""
Created on 2017-10-27

@author: hc
"""
from Source.spec2db_server.arl.arl_base import ServiceBase


class ArlTableMng(ServiceBase):
    __instance = None

    @staticmethod
    def instance():
        """create a instance"""
        if ArlTableMng.__instance is None:
            ArlTableMng.__instance = ArlTableMng()
        return ArlTableMng.__instance

    def __init__(self):
        ServiceBase.__init__(self)
        self.table_dict = dict()

    def get_table_id(self, table_name):
        if not self.table_dict:
            self.load_table()
        table_info = self.table_dict.get(table_name)
        if table_info:
            return table_info.get("table_id")
        return None

    def get_cols_name(self, table_name):
        cols_name = []
        if not self.table_dict:
            self.load_table()
        table_info = self.table_dict.get(table_name)
        if table_info:
            col_list = table_info.get("col_list")
            if col_list:
                for col in col_list:
                    cols_name.append(col.get("col_name"))
        return cols_name

    def get_col_list(self, table_name):
        if not self.table_dict:
            self.load_table()
        table_info = self.table_dict.get(table_name)
        if table_info:
            col_list = table_info.get("col_list")
            if col_list:
                return col_list
        return []

    def load_table(self):
        sqlcmd = """
        SELECT table_name, tt1.table_id, col_ids,
               col_names, col_disp_names
          FROM spec.log_table_map as tt1
          INNER JOIN (
            SELECT table_id, array_agg(col_id) as col_ids,
                   array_agg(col_name) as col_names, array_agg(col_disp_name) as col_disp_names
              FROM (
                SELECT table_id, col_id, col_name, col_disp_name
                  FROM spec.log_col_map
                  order by table_id, col_id
              ) AS t1
              group by table_id
          ) as tt2
          on tt1.table_id = tt2.table_id
          ORDER BY tt1.table_id
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        self._pg.close()
        for row in rows:
            table_info = dict()
            table_name, table_id = row[0:2]
            col_ids, col_names, col_disp_names = row[2:]
            col_list = []
            for col_id, col_name, col_disp_name in zip(col_ids, col_names, col_disp_names):
                col_info = dict()
                col_info["col_id"] = col_id
                col_info["col_name"] = col_name
                col_info["col_disp_name"] = col_disp_name
                col_list.append(col_info)
            table_info["table_id"] = table_id
            table_info["col_list"] = col_list
            self.table_dict[table_name] = table_info
