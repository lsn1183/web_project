# -*- coding: UTF-8 -*-
import json
from Source.spec2db_server.arl.arl_base import ServiceBase

class TmcPointInfo(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "tmc_point_info"
        self.key_col = "rc_id"
        self.attr_list = ["rc_id",  "classify", "point_date",
                          "folder_info", "file_info", "id",
                          "small_category", "basic_req", "review_result",
                          "pointout_no", "pointout_status", "pointout_comment",
                          "reader_check", "reader2_check", "final_check",
                          "pointout_charger","pointout_priority","pointout_date",
                          "suntec_status","fixed","suntec_remark","arl_rel",
                          "suntec_cannot_modify"
                          ]

    def delete_info(self, classify, point_date):
        self._pg.connect()

        del_sqlcmd = """
                        DELETE FROM spec.tmc_point_info WHERE classify = %s and point_date = %s
                        """
        self._pg.execute(del_sqlcmd, (classify, point_date))

        self._pg.close()

    def store_json(self, header_json, data_json):
        tile_to_dbcol = {
            u"小分類":("small_category","STR"),
            u"基本要件":("basic_req", "STR"),
            u"H/U要件定義ID":("id", "STR"),
            u"レビュー結果":("review_result", "RICHSTR"),
            u"指摘No.":("pointout_no", "RICHSTR"),
            u"ステータス": ("pointout_status", "RICHSTR"),
            u"コメント": ("pointout_comment", "RICHSTR"),
            u"リーダチェック": ("reader_check", "RICHSTR"),
            u"リーダ２チェック": ("reader2_check", "RICHSTR"),
            u"最終チェック": ("final_check", "RICHSTR"),
            u"担当": ("pointout_charger", "RICHSTR"),
            u"優先度": ("pointout_priority", "RICHSTR"),
            u"指摘提出日": ("pointout_date", "RICHSTR"),
            u"Suntecステータス": ("suntec_status", "STR"),
            u"修正済み": ("fixed", "STR"),
            u"Suntec備考": ("suntec_remark", "STR"),
            u"ARL関連指摘": ("arl_rel", "STR"),
            u"Suntec修正不可": ("suntec_cannot_modify", "STR"),
            u"TAGL要件定義ID":("id", "STR"),
        }
        self._pg.connect()

        for one_data in data_json:
            new_point_data = dict(zip(self.attr_list[1:], ['']*len(self.attr_list[1:])))
            for header_key, header_data in header_json.iteritems():
                new_point_data[header_key]= header_data
            for col_data in one_data:
                db_key, db_type = tile_to_dbcol[col_data['titleInfo']]
                if db_type == "STR":
                    new_point_data[db_key] = col_data["richVal"]["strVal"]
                else :
                    new_point_data[db_key] = json.dumps(col_data["richVal"])

            sqlcmd = self.list_2_insert_sql(self.table_name, self.attr_list[1:], self.key_col)
            params = self.get_params(new_point_data, self.attr_list[1:])

            self._pg.execute(sqlcmd, params)

        self._pg.commit()
        self._pg.close()

    def find_folder_by_indexdict(self, index_dict, data_type):
        sqlcmd="""
            SELECT distinct(folder_info) FROM spec.tmc_point_info WHERE point_date=%s and classify=%s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (index_dict['point_date'],data_type))
        foler_info_list = [_row[0] for _row in self._pg.fetchall()]
        self._pg.close()

        if index_dict['folder'] in foler_info_list:
            return index_dict['folder']

        import re
        folder_match = re.match("^\d.*\d", index_dict['folder'])
        if folder_match:
            if folder_match.group(0) in foler_info_list:
                return folder_match.group(0)

        return None

    def get_info_list_by_folder(self, index_dict, data_type):

        ret_dict_keys = ["classify", "id",
                         "small_category", "basic_req", "review_result",
                         "pointout_no", "pointout_status", "pointout_comment",
                         "reader_check", "reader2_check", "final_check",
                         "pointout_charger", "pointout_priority", "pointout_date",
                         "suntec_status", "fixed", "suntec_remark", "arl_rel",
                         "suntec_cannot_modify"]

        folder_info = self.find_folder_by_indexdict(index_dict, data_type)
        if not folder_info:
            print "error folder info:",index_dict["folder"]
            return []

        self._pg.connect()

        sql_match_all = """
            SELECT classify, id,
                small_category, basic_req, review_result,
                pointout_no, pointout_status, pointout_comment,
                reader_check, reader2_check, final_check,
                pointout_charger, pointout_priority, pointout_date,
                suntec_status, fixed, suntec_remark, arl_rel,
                suntec_cannot_modify
            FROM spec.tmc_point_info
            WHERE point_date=%s and classify=%s and folder_info=%s and 
                    small_category=%s and basic_req=%s
        """

        self._pg.execute(sql_match_all, (index_dict['point_date'],
                                         data_type,
                                         folder_info,
                                         index_dict['small_category'],
                                         index_dict['basic_req']))
        tmc_info_list = [dict(zip(ret_dict_keys, _row)) for _row in self._pg.fetchall()]
        if len(tmc_info_list) > 0:
            self._pg.close()
            return tmc_info_list

        sql_match_small_category = """
                    SELECT classify, id,
                        small_category, basic_req, review_result,
                        pointout_no, pointout_status, pointout_comment,
                        reader_check, reader2_check, final_check,
                        pointout_charger, pointout_priority, pointout_date,
                        suntec_status, fixed, suntec_remark, arl_rel,
                        suntec_cannot_modify
                    FROM spec.tmc_point_info
                    WHERE point_date=%s and classify=%s and folder_info=%s and small_category=%s
                """

        self._pg.execute(sql_match_small_category, (index_dict['point_date'],
                                                    data_type,
                                                    folder_info,
                                                    index_dict['small_category']))
        tmc_info_list = [dict(zip(ret_dict_keys, _row)) for _row in self._pg.fetchall()]
        if len(tmc_info_list) > 0:
            self._pg.close()
            return tmc_info_list

        sql_match_basic_req = """
                            SELECT classify, id,
                                small_category, basic_req, review_result,
                                pointout_no, pointout_status, pointout_comment,
                                reader_check, reader2_check, final_check,
                                pointout_charger,pointout_priority,pointout_date,
                                suntec_status,fixed,suntec_remark, arl_rel,
                                suntec_cannot_modify
                            FROM spec.tmc_point_info
                            WHERE point_date=%s and classify=%s and folder_info=%s and basic_req=%s
                        """

        self._pg.execute(sql_match_basic_req, (index_dict['point_date'],
                                                    data_type,
                                                    folder_info,
                                                    index_dict['basic_req']))
        tmc_info_list = [dict(zip(ret_dict_keys, _row)) for _row in self._pg.fetchall()]
        if len(tmc_info_list) > 0:
            self._pg.close()
            return tmc_info_list

        self._pg.close()
        return []

    def get_info_list_bydate(self, point_date, data_type):
        self._pg.connect()
        ret_dict_keys = ["classify", "id",
                         "small_category", "basic_req", "review_result",
                         "pointout_no", "pointout_status", "pointout_comment",
                         "reader_check", "reader2_check", "final_check",
                         "pointout_charger", "pointout_priority", "pointout_date",
                         "suntec_status", "fixed", "suntec_remark", "arl_rel",
                         "suntec_cannot_modify"]

        sql_match_all = """
                        SELECT classify, id,
                            small_category, basic_req, review_result,
                            pointout_no, pointout_status, pointout_comment,
                            reader_check, reader2_check, final_check,
                            pointout_charger, pointout_priority, pointout_date,
                            suntec_status, fixed, suntec_remark, arl_rel,
                            suntec_cannot_modify
                        FROM spec.tmc_point_info
                        WHERE point_date=%s and classify=%s
                        """
        self._pg.execute(sql_match_all, (point_date, data_type))
        tmc_info_list = [dict(zip(ret_dict_keys, _row)) for _row in self._pg.fetchall()]
        self._pg.close()
        return tmc_info_list
