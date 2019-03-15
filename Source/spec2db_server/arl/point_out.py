# -*- coding: UTF-8 -*-
"""
Created on 2017-11-22

@author: hcz
"""
from Source.spec2db_server.arl.arl_base import ServiceBase


class PointOut(ServiceBase):
    """
    """
    def __init__(self, classify):
        ServiceBase.__init__(self)
        self.table_name = "point_out"
        self.key_col = "pointout_rc_id"
        self.classify = classify  # Hu / def / analysis
        if self.classify == 'basic_req_hu':
            self.classify = 'hu'
        if self.classify in ('definition', 'basic_req_definition'):
            self.classify = 'DEF'
        if self.classify == 'basic_req_analysis':
            self.classify = 'analysis'
        self.attr_list = ["pointout_rc_id", "record_id", "classify",
                          "id", "review_result", "pointout_no",
                          "pointout_status", "pointout_comment", "reader_check",
                          "reader2_check", "final_check", "pointout_charger",
                          "pointout_priority", "pointout_date", "fixed",
                          "suntec_remark", "arl_rel", "update_time","suntec_status",
                          "suntec_cannot_modify", "point_date"
                          ]
        self.type_list = ["STR", "STR", "STR",
                          "STR", "STR", "STR",
                          "STR", "STR", "STR",
                          "STR", "STR", "STR",
                          "STR", "STR", "STR",
                          "STR", "STR", "STR",
                          "STR", "STR", "STR"
                          ]

    def check_md5_key(self, new_data, old_data):
        return True

    def get_one_point_by_id(self, pg, _id):
        col_str = self.list_2_col_str(self.attr_list)
        sqlcmd = """
                SELECT {col_str}
                  FROM spec.point_out
                  where id = %s and classify = %s
                  ORDER BY update_time DESC limit 1
                """.format(col_str=col_str)
        if self.classify == "DEF":
            self.classify = "definition"
        pg.execute(sqlcmd, [_id, self.classify])
        row = pg.fetchone()
        point_dict = dict()
        if row:
            for i, col in enumerate(self.attr_list, 0):
                point_dict[col] = row[i]
        return point_dict

    def get_list_by_id(self, pg, _id):
        col_str = self.list_2_col_str(self.attr_list)
        sqlcmd = """
        SELECT {col_str}
          FROM spec.point_out
          where id = %s and classify = %s
          ORDER BY pointout_rc_id DESC
        """.format(col_str=col_str)
        pg.execute(sqlcmd, [_id, self.classify])
        rows = pg.fetchall()
        point_out_list = []
        for row in rows:
            point_out_data = dict()
            for i, col in enumerate(self.attr_list, 0):
                if self.type_list[i] == "JSON":
                    point_out_data[col] = self.json_to_html(row[i])
                else:
                    point_out_data[col] = row[i]
            point_out_list.append(point_out_data)
        return point_out_list

    def add_list(self, pg, parent_id, data_list, update_time):
        if not parent_id:
            return None
        return self._update_point_out_list(pg, data_list, update_time)

    def _update_point_out_list(self, pg, data_list, update_time):
        update_col_list = ["suntec_status", "fixed", "suntec_remark", "arl_rel","suntec_cannot_modify", "update_time"]
        condition_col_list = [self.key_col]
        sqlcmd = self.list_2_update_sql(self.table_name, update_col_list, condition_col_list, self.key_col)
        for data in data_list:
            pointout_rc_id = data.get(self.key_col)
            params = [data.get("suntec_status"),
                      data.get("fixed"), data.get("suntec_remark"),
                      data.get("arl_rel"), data.get("suntec_cannot_modify"),
                      update_time, pointout_rc_id]
            pg.execute(sqlcmd, params)
            if pg.pgcur.rowcount <= 0:
                return None
        return []

    def do_point_info_update(self, point_info_list, point_date):
        self._pg.connect()

        for one_point_info in point_info_list:
            check_exist_sql = """
                SELECT * FROM spec.point_out WHERE classify=%s AND id=%s AND review_result=%s AND pointout_no=%s
                    AND pointout_status=%s AND pointout_comment=%s AND reader_check=%s
                    AND reader2_check=%s AND final_check=%s AND pointout_charger=%s
                    AND pointout_priority=%s AND pointout_date=%s
            """
            self._pg.execute(check_exist_sql, (one_point_info['classify'], one_point_info['id'], one_point_info['review_result'],
                                               one_point_info['pointout_no'], one_point_info['pointout_status'],
                                               one_point_info['pointout_comment'], one_point_info['reader_check'],
                                               one_point_info['reader2_check'], one_point_info['final_check'],
                                               one_point_info['pointout_charger'], one_point_info['pointout_priority'],
                                               one_point_info['pointout_date']
                                               ))
            check_data = self._pg.fetchall()
            if len(check_data) > 0:
                continue
            #insert data into db
            insert_sql = self.list_2_insert_sql(self.table_name, self.attr_list[2:], self.key_col)
            self._pg.execute(insert_sql, [one_point_info['classify'], one_point_info['id'], one_point_info['review_result'],
                                        one_point_info['pointout_no'], one_point_info['pointout_status'],
                                        one_point_info['pointout_comment'], one_point_info['reader_check'],
                                        one_point_info['reader2_check'], one_point_info['final_check'],
                                        one_point_info['pointout_charger'], one_point_info['pointout_priority'],
                                        one_point_info['pointout_date'], one_point_info['fixed'],
                                        one_point_info['suntec_remark'], one_point_info['arl_rel'],
                                        self.get_current_time(), one_point_info['suntec_status'],
                                        one_point_info["suntec_cannot_modify"], point_date])

        self._pg.commit()
        self._pg.close()

    def update_by_tmc_point(self, point_date, data_type):
        from pointout_server import PointOut as TmcPointIndex
        from arl_tmc_pointinfo import TmcPointInfo

        if data_type=="hu":
            tmc_point_index = TmcPointIndex().get_date_info(point_date)

            for one_index_info in tmc_point_index:
                point_info_list = TmcPointInfo().get_info_list_by_folder(one_index_info, data_type)
                self.do_point_info_update(point_info_list, point_date)
        else:
            point_info_list = TmcPointInfo().get_info_list_bydate(point_date, data_type)
            self.do_point_info_update(point_info_list, point_date)

    def json_to_html(self, json_str):
        if not json_str:
            return ""

        import json
        from ctypes import c_uint8

        try:
            json_val = json.loads(json_str)
        except:
            return json_str

        str_val = json_val["strVal"]
        ret_html_list = []
        for style_info in json_val["styleInfoList"]:
            html_info = """<font color="#%02X%02X%02X">"""%(c_uint8(style_info["fontColorRGB"][0]).value,
                                                            c_uint8(style_info["fontColorRGB"][1]).value,
                                                            c_uint8(style_info["fontColorRGB"][2]).value)
            if style_info["isItalic"]:
                html_info+="<i>"
            if style_info["isBold"]:
                html_info+="<b>"
            if style_info["isStrike"]:
                html_info+="<s>"
            html_info+=str_val[style_info["startIndex"]:style_info["startIndex"]+style_info["strLength"]]
            if style_info["isItalic"]:
                html_info+="</i>"
            if style_info["isBold"]:
                html_info+="</b>"
            if style_info["isStrike"]:
                html_info+="</s>"

            html_info+="</font>"
            ret_html_list.append(html_info)

        return "".join(ret_html_list)
