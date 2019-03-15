# -*- coding: UTF-8 -*-
"""
Created on 2017-9-21

@author: zj
"""
from Source.spec2db_server.common import db
import json


hu = {
    "result": "OK",
    "content": {
        "arl_id": "",  # 要件ID
        "hu_id":  "H/U要件定義ID",
        "unique_id": "ユニークID",
        "system_conf": "システム構成(System configuration)",
        "rel_requirement": "関連基本要件(Related Basic Requirements)",
        "exception": "除外",
        "dcu_status": "DCU-状態",
        "dcu_trigger": "DCU-トリガー",
        "dcu_action": "DCU-動作",
        "meu_status": "MEU-状態",
        "meu_trigger": "MEU-トリガー",
        "meu_action": "MEU-動作",
        "hu_category_id": "H/U分類ID",
        "remark": "備考",
        "sys_spec_chapter": "001 システム仕様書--章Chapter/Section or ページ番号 Page No",
        "common_chapter": "003 共通アプリ?AVC-LAN仕様書--章　Chapter/Section or ページ番号 Page No",
        "common_seq_spec": "シーケンス仕様 Sequence spec.",
        "common_seq_no": "シーケンス番号Sequence No.",
        "common_cmd_guide": "コマンドガイドCommand guide",
        "common_opc": "OPC",
        "inter_loc_spec": "318 DCU-MEU間連携仕様書DCU-MEU interaction spec.--機能配置?機能仕様 Function location and spec.",
        "inter_chapter": "章Chapter/Section or ページ番号 Page No",
        "other_chapter": "ドキュメント名 ※トヨタ仕様の場合は仕様番号も記載する事",
        "other_doc": "その他資料Other document",
        "amp": "AMP",
        "dsrc": "DSRC",
        "dcm": "DCM",
        "rse": "RSE",
        "touch_pad": "ToutchPad",
        "separate_disp": "SepareteDisp",
        "test_results": "テスト結果",
        "future_req": "未要件分析",
        "model_list": [
        ]
    }
}


definition = {
    "result": "OK",
    "content": {
        "def_rc_id": "",  # 记录ID
        "author_name": "担当",
        "hu_def_id": "H/U要件定義ID",
        "definition_id": "要件定義ID",
        "unique_id": "ユニークID",
        # "rel_requiremant": "関連基本要件",
        # "major_category": "大分類",
        # "medium_catetory": "中分類",
        # "small_category": "小分類",
        # "detail": "詳細",
        # "base": "基本要件",
        "exception": "",
        # "dcu_status": "DCU-状態",
        # "dcu_trigger": "DCU トリガー",
        # "dcu_action": "DCU 動作",
        # "meu_status": "MEU 状態",
        # "meu_trigger": "MEU-トリガー",
        # "meu_action": " MEU-動作",
        # "hu_req_remark": "備考(HU要件定義)",
        "dcu_meu": "DCU/MEUどちらの想定か",
        "pf_status": "状態",
        "pf_trigger": "リガー",
        "pf_action": "動作",
        "remark": "備考",
        "notice": "責務分担の特記事項",
        "rel_hal_design": "参考HAL設計書",
        "rel_flow_diagram": "参考ウォークスルー図",
        "other_spec": "その他仕様（リファハード仕様等）",
        "implementation": "リファレンスハード上での実現可否",
        "analysis": "詳細分析可否",
        "unrequire": "未要件分析",
        "new_date": "日付",
        "reason": "変更理由",
        "translation_flag": "翻译",
        "agree_flag": "承认",
        "has_problem": "指摘",
        "complete_flag": "是否完成",
        "model_list": []
    }
}


analysis = {
    "result": "OK/NG",
    "content": {
        "analysis_rc_id": "",  # 记录ID
        "author_name": "担当者",
        "definition_id": "TAGL要件定義ID",
        "unique_id": "ユニークID",
        # "major_category": "大分類",
        # "medium_catetory": "中分類",
        # "small_category": "小分類",
        # "detail": "詳細",
        # "base": "基本要件",
        # "dcu_meu": "DCU/MEUどちらの想定か",
        # "pf_status": "状態",
        # "fp_trigger": "トリガー",
        # "pf_action": "動作",
        "seq_diagram": "シーケンス図",
        # "application": "アプリケーション",
        # "kernel": "kernel",
        # "systemd": "systemd",
        "supple_spec": "補足参照仕様書",
        "uncheck": "未検証",
        "remark": "備考",
        "new_date": "日付",
        "reason": "変更理由",
        "translation_flag": "翻译",
        "agree_flag": "承认",
        "has_problem": "指摘",
        "complete_flag": "是否完成",
        "model_list": []
    }
}


class Cdb_operate(object):
    def __init__(self):
        self.pg = db.pg(True)
        self.table = ''
        self.primary_key = ''
        self.serial_col = ''
        self.base_dict = {}
        self.column_list = []

    def fetch_id(self):
        _id = 0
        row = self.pg.fetchone()
        if row:
            _id = row[0]
        return _id

    def init_column_list(self):
        self.column_list = [key for key in self.base_dict['content'].keys() if key != 'model_list']
          
    def get_result_dict(self):
        result_dict = self.base_dict.copy()
        result_dict['result'] = 'OK'
        result_dict['total_count'] = 0
        
        return result_dict
        
    def get_column_type(self, column):
        sqlcmd = '''
                select data_type, udt_name
                from   information_schema.columns
                where table_name = '{table}' and column_name= '{column}'; 
                '''.format(table=self.table, column=column)
        self.pg.query(sqlcmd)
        row = self.pg.fetchone()
        if row:
            return row[0]
        else:
            print self.table, column
            return None

    def get_record_key_value(self, key_value):
        return self.get_record((key_value.keys())[0], (key_value.values())[0])
    
    def get_record(self, column, column_value, sheet_idx=1, limit=20, list_flag = False):
        result_dict = self.get_result_dict()
        if not list_flag:
            column = [column]
            column_value = [column_value]
            
        num = 0
        content_dict_list = None
        row_all_num, rows = self.get_record_sql(column, column_value, sheet_idx, limit)
        if not rows:
            result_dict['content'] = {}
            result_dict['result'] = 'NG'
            return result_dict
        for row in rows:
            content_dict = {}
            for i in range(len(self.column_list)):
                content_dict[self.column_list[i]] = row[i]
            rc_id = content_dict.get(self.serial_col)
            if rc_id:
                model_list = self.get_model_list2(rc_id)
                content_dict['model_list'] = model_list
            if num == 0:
                content_dict_list = content_dict
            elif num == 1:
                content_dict_list = [content_dict_list]
                content_dict_list.append(content_dict)
            else:
                content_dict_list.append(content_dict)
            num += 1
        result_dict['total_count'] = row_all_num
        if content_dict_list:
            result_dict['content'] = content_dict_list
        return result_dict

    def dict_2_list_comtent(self, data_dict, insert_flag=False):
        data_dict_content = data_dict
        key_list = []
        value_list = []
        for key in self.base_dict.get("content").keys():
            if key == 'model_list':
                continue
            if key == self.serial_col:
                continue
            key_list.append(key)
            value_list.append(data_dict_content.get(key))
        return key_list, value_list

    def insert_record_list(self, data_list):
        if not data_list:
            return 0
        try:
            hu_id = data_list[0].get("hu_def_id")
            if hu_id:
                self.delete_by_hu_id(self.pg, hu_id)
            for unique_id, content in enumerate(data_list, 0):
                if hu_id:
                    content["definition_id"] = '.'.join([hu_id, str(unique_id)])
                    content["unique_id"] = unique_id
                key_list, value_list = self.dict_2_list_comtent(content,
                                                                insert_flag=True
                                                                )
                rc_id = self.insert_record_sql(key_list, value_list)
                if content:
                    model_list = content.get("model_list")
                    self._add_model_list(rc_id, model_list)
            self.pg.commit()
            return 1
        except:
            self.pg.conn.rollback()
            return 0

    def insert_record(self, data):
        if not data:
            return 0
        content = data['content']
        key_list, value_list = self.dict_2_list_comtent(content,
                                                        insert_flag=True)
        try:
            rc_id = self.insert_record_sql(key_list, value_list)
            if content:
                model_list = content.get("model_list")
                self._add_model_list(rc_id, model_list)
            self.pg.commit()
        except:
            self.pg.conn.rollback()

    def update_record(self, key_value, data_dict):
        if not (data_dict and key_value):
            return 0
        content = data_dict.get("content")
        key_list, value_list = self.dict_2_list_comtent(content)
        try:
            self.update_record_sql(key_list, value_list,
                                   [self.primary_key], [key_value])
            if content:
                rc_id = content.get(self.serial_col)
                model_list = content.get("model_list")
                self._update_model_list(rc_id, model_list)
            self.pg.commit()
        except:
            self.pg.conn.rollback()

    def lists_2_str(self, key_list, values_list, connect_key):
        strlist = ''
        for i in range(len(key_list)):
            if strlist:
                strlist += ' ' + connect_key + ' '
            if self.get_column_type(key_list[i]) == 'integer':
                strlist += key_list[i] + ' = ' + str(values_list[i])
            else:
                strlist += key_list[i] + ' = \'' + str(values_list[i]) + '\''
        return strlist

    def lists_2_condition_str(self, key_list):
        strlist = ' '
        new_keys = []
        for key in key_list:
            new_keys.append(key + ' = %s')
        strlist += ' and '.join(new_keys)
        strlist += " "
        return strlist

    def lists_2_update_str(self, key_list):
        strlist = ' '
        new_keys = []
        for key in key_list:
            new_keys.append(key + ' = %s')
        strlist += ', '.join(new_keys)
        strlist += ' '
        return strlist

    def list_2_str(self, key_list, values_list, connect_key):
        strlist = ''
        for i in range(len(key_list)):
            if strlist:
                strlist += ' ' + connect_key + ' '
            if self.get_column_type(key_list[i]) == 'integer':
                strlist += str(values_list[i])
            else:
                strlist += '\'' + str(values_list[i]) + '\''
        return strlist

    def get_record_sql(self, key_column_list, key_value_list, sheet_idx, limit):
        strcolumns = ', '.join(self.column_list)
        # key_column = self.lists_2_str(key_column_list, key_value_list, 'and')
        key_column = self.lists_2_condition_str(key_column_list)
        sqlcmd = '''
                select {columns}
                from spec.{table}
                where {key_column}
                order by unique_id;
                '''.format(columns=strcolumns, table=self.table, key_column=key_column)
        
        offset = (sheet_idx - 1) * limit
        self.pg.execute(sqlcmd, key_value_list)
        rowcount = self.pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self.pg.pgcur.scroll(offset)
            rows = self.pg.pgcur.fetchmany(limit)
            return rowcount, rows
        return 0, []

    def insert_record_sql(self, column_list, column_value_list):
        strcolumn = ','.join(column_list)
        pecent_list = ', '.join(['%s'] * len(column_list))
        sqlcmd = '''
                insert into spec.{table}({strcolumn})
                values({pecent_list}) 
                returning {serial_col}
                '''.format(table=self.table,
                           strcolumn=strcolumn,
                           pecent_list=pecent_list,
                           serial_col=self.serial_col)
        rc_id = None
        try:
            self.pg.execute(sqlcmd, column_value_list)
            rc_id = self.fetch_id()
            return rc_id
        finally:
                pass
        return rc_id
    
    def update_record_sql(self, column_list, column_value_list,
                          key_list, key_value_list):
        strcolumn = self.lists_2_update_str(column_list)
        strkey = self.lists_2_condition_str(key_list)
        sqlcmd = '''
                update spec.{table}
                set {strcolumn}
                where {strkey}
                '''.format(table=self.table, strcolumn=strcolumn, strkey=strkey)
        try:
            self.pg.execute(sqlcmd, column_value_list + key_value_list)
            if self.pg.pgcur.rowcount:
                return 1
        finally:
            pass
        return 0

    def get_model_list2(self, arl_rc_id):
        model_list = []
        # model_dict = {"content": "", "sub_content":[{},]}
        for model, val in self._get_model_list(arl_rc_id):
            model_list.append(val)
        return model_list


class Cdb_definition(Cdb_operate):
    def __init__(self):
        super(Cdb_definition, self).__init__()
        self.table = 'definition'
        self.primary_key = 'definition_id'
        self.base_dict = definition
        self.serial_col = 'def_rc_id'
        self.init_column_list()

    def get_all_model_list(self):
        result = {"reslut": "NG"}
        sqlcmd = """
        SELECT model_id, model
          FROM spec.definition_model_type
          order by model_id;
         """
        model_list = []
        try:
            self.pg.execute(sqlcmd)
            rows = self.pg.fetchall()
            for row in rows:
                model_dict = dict()
                model_id, model = row[0:2]
                model = json.loads(model)
                model_dict["model_id"] = model_id
                model_dict["title"] = model[-1]
                model_list.append(model_dict)
        except:
            self.pg.close()
        if model_list:
            result["reslut"] = "OK"
            result["content"] = model_list
        return result

    def add_by_hu(self, pg, hu_data):
        hu_def_id = hu_data.get("hu_id")
        if not hu_def_id:
            return
        def_data_base = {
            "hu_def_id": hu_def_id,
            "definition_id": "",
            "unique_id": "",
            "dcu_meu": "",
            "pf_status": "",
            "pf_trigger": "",
            "pf_action": "",
        }
        def_data_list = []
        hu_category_id = hu_data.get("hu_category_id")
        if hu_category_id in (0, '0'):  # 2个: 要件をDCU-MEUに跨って実現
            def_dict = def_data_base.copy()
            # DCU
            def_dict["dcu_meu"] = 'DCU'
            def_dict["pf_status"] = hu_data.get("dcu_status")
            def_dict["pf_trigger"] = hu_data.get("dcu_trigger")
            def_dict["pf_action"] = hu_data.get("dcu_action")
            def_data_list.append(def_dict)
            # MEU
            def_dict = def_data_base.copy()
            def_dict["dcu_meu"] = 'MEU'
            def_dict["pf_status"] = hu_data.get("meu_status")
            def_dict["pf_trigger"] = hu_data.get("meu_trigger")
            def_dict["pf_action"] = hu_data.get("meu_action")
            def_data_list.append(def_dict)
        elif hu_category_id in (1, '1'):  # 1个DCU: 要件をDCUのみで実現：
            def_dict = def_data_base.copy()
            def_dict["dcu_meu"] = 'DCU'
            def_dict["pf_status"] = hu_data.get("dcu_status")
            def_dict["pf_trigger"] = hu_data.get("dcu_trigger")
            def_dict["pf_action"] = hu_data.get("dcu_action")
            def_data_list.append(def_dict)
        elif hu_category_id in (2, '2'):  # 1个MEU: 要件をMEUのみで実現
            # MEU
            def_dict = def_data_base.copy()
            def_dict["dcu_meu"] = 'MEU'
            def_dict["pf_status"] = hu_data.get("meu_status")
            def_dict["pf_trigger"] = hu_data.get("meu_trigger")
            def_dict["pf_action"] = hu_data.get("meu_action")
            def_data_list.append(def_dict)
        elif hu_category_id in (3, '3'):  # 要件をDCU/MEU各々で実現（同じ機能をDCUもMEUも持つケース）
            def_dict = def_data_base.copy()
            def_dict["dcu_meu"] = 'DCU/MEU'
            # status = [hu_data.get("dcu_status"), hu_data.get("meu_status")]
            # trigger = [hu_data.get("dcu_trigger"), hu_data.get("meu_trigger")]
            # action = [hu_data.get("dcu_action"), hu_data.get("meu_action")]
            def_dict["pf_status"] = hu_data.get("dcu_status")
            def_dict["pf_trigger"] = hu_data.get("dcu_trigger")
            def_dict["pf_action"] = hu_data.get("dcu_action")
            def_data_list.append(def_dict)
        if not def_data_list:
            raise 'Error HU Category ID' 
            return
        old_defs = self._get_by_hu(pg, hu_def_id)
        matched_defs = []
        matched_def_ids = {}
        for def_data in def_data_list:
            dcu_meu = def_data["dcu_meu"]
            temp_defs = []
            for (old_dcu_meu, definition_id, unique_id) in old_defs:
                if dcu_meu == old_dcu_meu:
                    temp_defs.append((definition_id, def_data))
                    matched_def_ids[definition_id] = None
            if temp_defs:
                matched_defs += temp_defs
            else:
                matched_defs.append((None, def_data))
        # 删除
        for _, definition_id, _ in old_defs:
            if definition_id not in matched_def_ids:
                self.delete(definition_id, pg)
        # 先更新旧的
        for i in range(0, len(matched_defs)):
            old_def_id, def_data = matched_defs[i]
            if old_def_id:  # 旧的
                new_def_id = '.'.join([hu_def_id, str(i)])
                def_data["definition_id"] = new_def_id
                def_data["unique_id"] = i
                self._update(pg, old_def_id, def_data)
        # 最后添加新的
        for i in range(0, len(matched_defs)):
            old_def_id, def_data = matched_defs[i]
            if not old_def_id:  # 旧的
                new_def_id = '.'.join([hu_def_id, str(i)])
                def_data["definition_id"] = new_def_id
                def_data["unique_id"] = i
                self._insert(pg, def_data)

    def _update(self, pg, old_def_id, def_data):
        attr_list = ["hu_def_id", "definition_id", "unique_id",
                     "dcu_meu", "pf_status", "pf_trigger",
                     "pf_action"]
        params = []
        for attr in attr_list:
            val = def_data.get(attr)
            params.append(val)
        sqlcmd = """
        UPDATE spec.definition
           SET "hu_def_id" = %s, definition_id=%s, unique_id=%s,
                dcu_meu=%s, pf_status=%s, pf_trigger=%s,
                pf_action=%s
         WHERE definition_id = %s;
        """
        pg.execute(sqlcmd, params + [old_def_id])

    def _insert(self, pg, def_data):
        attr_list = ["hu_def_id", "definition_id", "unique_id",
                     "dcu_meu", "pf_status", "pf_trigger", "pf_action"]
        params = []
        for attr in attr_list:
            val = def_data.get(attr)
            params.append(val)
        sqlcmd = """
        INSERT INTO spec.definition(
                    hu_def_id, definition_id, unique_id, 
                    dcu_meu, pf_status, pf_trigger, pf_action)
            VALUES (%s, %s, %s,
                    %s, %s, %s, %s) returning def_rc_id;
        """
        pg.execute(sqlcmd, params)

    def _get_by_hu(self, pg, hu_id):
        sqlcmd = """
        SELECT dcu_meu, definition_id, unique_id
          FROM spec.definition
          where hu_def_id = %s
          ORDER BY unique_id
        """
        pg.execute(sqlcmd, (hu_id, ))
        rows = pg.fetchall()
        if rows:
            return list(rows)
        return []

    def get_record_author_name(self, value):
        return self.get_record('author_name', value)

    def get_record_hu_def_id(self, value):
        data = self.get_record('hu_def_id', value)
        total_count = data.get("total_count")
        if total_count == 1:
            content = data.get("content")
            if type(content) != list:
                data["content"] = [content]
        elif total_count < 1:
            data["content"] = []
        content = data.get("content")
        for def_data in content:
            def_data["title"] = "TAGL要件定義: " + def_data.get("definition_id")
        return data
    
    def get_record_definition_id(self, value):
        data = self.get_record('definition_id', value, sheet_idx=1, limit=1)
        if data:
            data.pop('total_count')
            content = data.get("content")
            if 'definition_id' in content.keys():
                data['content']['title'] = 'TAGL要件定義：'+content['definition_id']
            # if content:
            #     rc_id = content.get("def_rc_id")
            #     if rc_id:
            #         model_list = self.get_model_list2(rc_id)
            #         content["model_list"] = model_list
        return data

    def get_by_category2(self, category_id, page_size, page_number, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, arl_record["content"] = self.get_by_categorysql(cat_id_list, page_size, page_number, user_id)
        arl_record["total_count"] = count
        arl_record["result"] = "OK"
        return arl_record

    def get_by_categorysql(self, cat_id_list, page_size, page_number, user_id=None):
        from Source.spec2db_server.arl.arl_server import ArlRecord
        arl_obj = ArlRecord()
        condition, params = arl_obj.get_category_condition(cat_id_list, user_id)
        sqlcmd = """
        select d."definition_id", "arl_id", "dcu_meu",
               "pf_status", "pf_trigger", "pf_action"
            from spec.definition d
            INNER JOIN (
                SELECT h.hu_id, h.arl_id
                FROM spec.hu h
                WHERE h.arl_id in (
                    SELECT a.arl_id 
                      FROM spec.arl a
                      %s
                )
            ) AS hu
            on d.hu_def_id = hu.hu_id
            ORDER BY length(d."definition_id"), d."definition_id"
        """ % condition
        def_list = ["definition_id", "arl_id", "dcu_meu",
                    "pf_status", "pf_trigger", "pf_action"]
        self.pg.connect()
        offset = page_size * (page_number - 1)
        self.pg.execute(sqlcmd, params)
        rowcount = self.pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount - 1:
                return rowcount, []
            self.pg.pgcur.scroll(offset)
        rows = self.pg.pgcur.fetchmany(page_size)
        def_dict_list = []
        for row in rows:
            def_dict = {}
            i = 0
            while i < len(def_list):
                def_dict[def_list[i]] = row[i]
                i += 1
            def_dict['title'] = '要件定义: '+def_dict['definition_id']
            def_dict_list.append(def_dict)
        return rowcount, def_dict_list

    def get_by_category(self, category_id, size, page):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        if len(cat_id_list) != 5:
            return arl_record
        data = self.get_record_cat_id0_4(cat_id_list, page, size)
        content = data.get("content")
        if content and type(content) != list:
            data['content'] = [content]
        return data

    def get_record_cat_id0_4(self, value_list, sheet_idx=1, num=20):
        return self.get_record(['cat_id0', 'cat_id1', 'cat_id2', 'cat_id3', 'cat_id4'], 
                               value_list, sheet_idx, num, True)

    def get_new_id(self, hu_id):
        sqlcmd = """
        SELECT max("unique_id"::int)
          FROM spec.definition
          where hu_def_id = %s
          group by "hu_def_id";
        """
        data = {"result": "OK"}
        self.pg.connect()
        self.pg.execute(sqlcmd, (hu_id, ))
        row = self.pg.fetchone()
        if row:
            unique_id = row[0] + 1
        else:
            unique_id = 0
        definition_id = '.'.join([hu_id, str(unique_id)])
        content = {"unique_id": unique_id,
                   "definition_id": definition_id}
        data[u"content"] = content
        self.pg.close()
        return data

    def get_post_info(self, def_id):
        data = {"result": "NG"}
        def_post_info = self._get_post_info(def_id)
        if not def_post_info:
            return data
        post_list = ["major_categor", "medium_catetory", "small_category",
                     "detail", "base", "rel_requirement"]
        from Source.spec2db_server.arl.hu_server import HuRecord
        hu = HuRecord()
        hu_id = '.'.join(def_id.split('.')[:-1])
        hu_post_info = hu.get_post_info(hu_id)
        if hu_post_info:
            hu_content = hu_post_info.get("content")
            for attr in post_list:
                def_post_info[attr] = hu_content.get(attr)
            data["content"] = def_post_info
            data["result"] = "OK"
        return data

    def _get_post_info(self, def_id):
        post_list = ["definition_id", "unique_id", "dcu_meu",
                     "pf_status", "pf_trigger", "pf_action"]
        sqlcmd = """
        SELECT "definition_id", "unique_id", "dcu_meu",
               "pf_status", "pf_trigger", "pf_action"
          FROM spec.definition
          WHERE "definition_id" = %s
          limit 1
        """
        self.pg.connect()
        self.pg.execute(sqlcmd, (def_id,))
        row = self.pg.fetchone()
        content = {}
        if row:
            for i in range(0, len(row)):
                attr = post_list[i]
                content[attr] = row[i]
        return content

    def delete(self, def_id, pg=None):
        sqlcmd = """
        -- delete model list
        DELETE FROM spec.definition_model_rel
          where def_rc_id in (
            select def_rc_id
              from spec.definition
              where definition_id = %s
          );
        -- delete content
        DELETE FROM spec.definition
         WHERE definition_id = %s;
        """
        if not pg:
            try:
                self.pg.connect ()
                self.pg.execute(sqlcmd, (def_id, def_id))
                obj = Cdb_analysis()
                obj.delete(def_id, False)
                self.pg.commit()
            except:
                self.pg.conn.rollback()
        else:
            pg.execute(sqlcmd, (def_id, def_id))
            obj = Cdb_analysis()
            obj.delete(def_id, pg)
        return 'OK'

    def delete_by_hu_id(self, pg, hu_id):
        sqlcmd = """
        -- delete model list
        DELETE FROM spec.definition_model_rel
          where def_rc_id in (
            select def_rc_id
              from spec.definition
              where hu_def_id = %s
          );
        -- delete content
        DELETE FROM spec.definition
         WHERE hu_def_id = %s;
        """
        pg.execute(sqlcmd, (hu_id, hu_id))
        analysis = Cdb_analysis()
        analysis.delete_by_hu_id(pg, hu_id)
        return 'OK'

    def get_model_list2(self, arl_rc_id):
        model_list = []
        # model_dict = {"content": "", "sub_content":[{},]}
        for model, model_id, val in self._get_model_list(arl_rc_id):
            model = json.loads(model)
            md = {"model_id": model_id, "title": model[-1], "val": val}
            model_list.append(md)
        return model_list

    def _get_model_list(self, _id):
        sqlcmd = """
        SELECT model, a.model_id, val
          FROM spec.definition_model_rel as a
          LEFT JOIN spec.definition_model_type as b
          ON a.model_id = b.model_id
          WHERE def_rc_id = %s
          ORDER BY order_no
        """
        self.pg.connect()
        self.pg.execute(sqlcmd, (_id,))
        rows = self.pg.fetchall()
        for row in rows:
            model, model_id, val = row[0], row[1], row[2]
            yield model, model_id, val

    def _add_model_list(self, rc_id, model_list):
        if not rc_id or not model_list:
            return
        for d in model_list:
            model_id = d.get("model_id")
            val = d.get("val")
            self._insert_model(rc_id, model_id, val)
        # for i in range(0, len(model_list)):
        #     #model_id = i + 1
        #     model_id = model_list[i].get("model_id")
        #     val = model_list[i].get("val")
        #     self._insert_model(rc_id, model_id, val)

    def _insert_model(self, rc_id, model_id, val):
        sqlcmd = """
        INSERT INTO spec.definition_model_rel(
                    def_rc_id, model_id, val)
            VALUES (%s, %s, %s);
        """
        self.pg.execute(sqlcmd, (rc_id, model_id, val))

    def _update_model_list(self, rc_id, model_list):
        if not rc_id:
            return
        if not model_list:
            sqlcmd = """
            DELETE FROM spec.definition_model_rel
            where def_rc_id = %s
            """
            self.pg.execute(sqlcmd, (rc_id,))
            return
        sqlcmd = """
        UPDATE spec.definition_model_rel SET val = %s
            where def_rc_id = %s and model_id = %s
        """
        for i in range(0, len(model_list)):
            model_id = i + 1
            val = model_list[i]
            self.pg.execute(sqlcmd, (val, rc_id, model_id))
            if self.pg.pgcur.rowcount == 0:
                self._insert_model(rc_id, model_id, val)

    def get_graph(self, hu_id):
        sqlcmd = """
        SELECT definition_id
          FROM spec.definition
          where hu_def_id = %s
          ORDER BY unique_id
        """
        self.pg.connect()
        self.pg.execute(sqlcmd, (hu_id, ))
        rows = self.pg.fetchall()
        def_list = []
        analysis_obj = Cdb_analysis()
        for row in rows:
            def_dict = dict()
            definition_id = row[0]
            def_dict["DEF"] = definition_id
            def_dict["children"] = analysis_obj.get_graph(definition_id)
            def_list.append(def_dict)
        return def_list


class Cdb_analysis(Cdb_operate):
    def __init__(self):
        super(Cdb_analysis, self).__init__()
        self.table = 'analysis'
        self.primary_key = 'definition_id'        
        self.base_dict = analysis
        self.serial_col = 'analysis_rc_id'
        self.init_column_list()

    def get_record_author_name(self, value):
        return self.get_record('author_name', value) 
    
    def get_record_definition_id(self, value):
        data = self.get_record('definition_id', value, sheet_idx=1, limit=1)
        if data:
            data.pop('total_count')
            content = data.get("content")
            if 'definition_id' in content.keys():
                data['content']['title'] = 'TAGL要件分析：'+content['definition_id']
            # if content:
            #     rc_id = content.get("analysis_rc_id")
            #     if rc_id:
            #         model_list = self.get_model_list2(rc_id)
            #         content["model_list"] = model_list
        return data

    def _exist_analysis(self, definition_id):
        sqlcmd = """
        SELECT definition_id
          FROM spec.analysis
          where definition_id = %s;
        """
        self.pg.execute(sqlcmd, (definition_id,))
        if self.pg.pgcur.rowcount > 0:
            return True
        return False

    def insert_record(self, data_dict):
        content = data_dict.get("content")
        if not content:
            return
        definition_id = content.get("definition_id")
        if not definition_id:
            return
        if self._exist_analysis(definition_id):
            return self.update_record(definition_id, data_dict)
        else:
            return Cdb_operate.insert_record(self, data_dict)

    def get_record_unique_id(self, value):
        return self.get_record('unique_id', value) 
    
    def get_record_major_category(self, value):
        return self.get_record('major_category', value) 
    
    def get_record_medium_catetory(self, value):
        return self.get_record('medium_catetory', value) 
    
    def get_record_small_category(self, value):
        return self.get_record('small_category', value) 
    
    def get_record_detail(self, value):
        return self.get_record('detail', value) 
    
    def get_record_base(self, value):
        return self.get_record('base', value) 
    
    def get_record_dcu_meu(self, value):
        return self.get_record('dcu_meu', value) 
    
    def get_record_pf_status(self, value):
        return self.get_record('pf_status', value) 
    
    def get_record_fp_trigger(self, value):
        return self.get_record('fp_trigger', value) 
    
    def get_record_pf_action(self, value):
        return self.get_record('pf_action', value) 
    
    def get_record_seq_diagram(self, value):
        return self.get_record('seq_diagram', value)
    
    def get_record_supple_spec(self, value):
        return self.get_record('supple_spec', value) 
    
    def get_record_uncheck(self, value):
        return self.get_record('uncheck', value) 
    
    def get_record_remark(self, value):
        return self.get_record('remark', value) 
    
    def get_record_model_list(self, value):
        return None

    def get_by_category(self, category_id, size, page):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        if len(cat_id_list) != 5:
            return arl_record
        return self.get_record_cat_id0_4(cat_id_list, page, size)

    def get_by_category2(self, category_id, size, page, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        count, arl_record["content"] = self.get_by_categorysql(cat_id_list, size, page, user_id)
        arl_record["total_count"] = count
        arl_record["result"] = "OK"
        return arl_record

    def get_by_categorysql(self, cat_id_list, page_size, page_number, user_id=None):
        from Source.spec2db_server.arl.arl_server import ArlRecord
        arl_obj = ArlRecord()
        condition, params = arl_obj.get_category_condition(cat_id_list, user_id)
        sqlcmd = """
        SELECT a.definition_id, arl_id, seq_diagram
          FROM spec.analysis as a
          INNER JOIN (
                select d.definition_id, arl_id
                    from spec.definition d
                    INNER JOIN (
                        SELECT h.hu_id, h.arl_id
                        FROM spec.hu h
                        WHERE h.arl_id in (
                            SELECT a.arl_id 
                            FROM spec.arl a
                            %s
                        )
                    ) AS hu
                    on d.hu_def_id = hu.hu_id
          ) AS def
          ON a.definition_id = def.definition_id
          ORDER BY length(a.definition_id), a.definition_id
        """ % condition
        def_list = ["definition_id", "arl_id", "seq_diagram"]
        self.pg.connect()
        offset = page_size * (page_number - 1)
        self.pg.execute(sqlcmd, params)
        rowcount = self.pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self.pg.pgcur.scroll(offset)
        rows = self.pg.pgcur.fetchmany(page_size)
        def_dict_list = []
        for row in rows:
            def_dict = {}
            i = 0
            while i < len(def_list):
                def_dict[def_list[i]] = row[i]
                i += 1
            def_dict['title'] = '要件分析: '+def_dict['definition_id']
            def_dict_list.append(def_dict)
        return rowcount, def_dict_list

    def get_record_cat_id0_4(self, value_list, sheet_idx=1, num=20):
        return self.get_record(['cat_id0', 'cat_id1', 'cat_id2', 'cat_id3', 'cat_id4'],
                               value_list, sheet_idx, num, True)

    def delete(self, def_id, pg=None):
        sqlcmd = """
        DELETE FROM spec.analysis_model_rel
          where analysis_rc_id in (
            select analysis_rc_id
              from spec.analysis
              where definition_id = %s
          );
        DELETE FROM spec.analysis
        WHERE definition_id = %s;
        """
        if not pg:
            self.pg.connect()
            self.pg.execute(sqlcmd, (def_id, def_id))
            self.pg.commit()
        else:
            pg.execute(sqlcmd, (def_id, def_id))
        return 'OK'

    def delete_by_hu_id(self, pg, hu_id):
        sqlcmd = """
          DELETE FROM spec.analysis_model_rel
          where analysis_rc_id in (
            select analysis_rc_id
              from spec.analysis
              where definition_id in (
                SELECT definition_id
                from spec.definition
                where hu_def_id = %s
              )
          );
        DELETE FROM spec.analysis
        where definition_id in (
            SELECT definition_id
            from spec.definition
            where hu_def_id = %s
        )
        """
        pg.connect()
        pg.execute(sqlcmd, (hu_id, hu_id))
        return 'OK'

    def _get_model_list(self, _id):
        sqlcmd = """
        SELECT model, val
          FROM spec.analysis_model_rel as a
          LEFT JOIN spec.analysis_model_type as b
          ON a.model_id = b.model_id
          WHERE analysis_rc_id = %s
          ORDER BY order_no
        """
        self.pg.connect()
        self.pg.execute(sqlcmd, (_id,))
        rows = self.pg.fetchall()
        for row in rows:
            model, val = row[0], row[1]
            yield model, val

    def _add_model_list(self, rc_id, model_list):
        if not rc_id or not model_list:
            return
        self.pg.connect()
        for i in range(0, len(model_list)):
            model_id = i + 1
            val = model_list[i]
            self._insert_model(rc_id, model_id, val)

    def _insert_model(self, rc_id, model_id, val):
        sqlcmd = """
        INSERT INTO spec.analysis_model_rel(
                    analysis_rc_id, model_id, val)
            VALUES (%s, %s, %s);
        """
        self.pg.execute(sqlcmd, (rc_id, model_id, val))

    def _update_model_list(self, rc_id, model_list):
        if not rc_id:
            return
        if not model_list:
            sqlcmd = """
            DELETE FROM spec.analysis_model_rel
            where analysis_rc_id = %s
            """
            self.pg.execute(sqlcmd, (rc_id,))
            return
        sqlcmd = """
        UPDATE spec.analysis_model_rel SET val = %s
            where analysis_rc_id = %s and model_id = %s
        """
        self.pg.connect()
        for i in range(0, len(model_list)):
            model_id = i + 1
            val = model_list[i]
            self.pg.execute(sqlcmd, (val, rc_id, model_id))
            if self.pg.pgcur.rowcount == 0:
                self._insert_model(rc_id, model_id, val)

    def get_graph(self, def_id):
        sqlcmd = """
        SELECT definition_id
          FROM spec.analysis
          where definition_id = %s
          ORDER BY unique_id
        """
        self.pg.connect()
        self.pg.execute(sqlcmd, (def_id,))
        rows = self.pg.fetchall()
        als_list = []
        for row in rows:
            als_dict = dict()
            definition_id = row[0]
            als_dict["ALS"] = definition_id
            als_list.append(als_dict)
        return als_list


def main():
    def_obj = Cdb_definition()
    data = def_obj.get_record_definition_id('50.1.3.1.3.273.0')
    content = data.get("content")
    model_list0 = content.get("model_list")
    content["hu_def_id"] = '10.1.1.5.1.3.0'
    content["unique_id"] = 0
    content["definition_id"] = '10.1.1.5.1.3.0.0'
    data_list = [content]
    def_obj.insert_record_list(data_list)
    return
    data = def_obj.get_record_definition_id('10.1.1.5.1.3.0.1')
    content = data.get("content")
    model_list0[0] = 'x'
    model_list0[1] = 'x'
    content["model_list"] = model_list0
    def_obj.update_record('10.1.1.5.1.3.0.1', data)
    return 0


    obj = Cdb_analysis()
    data = obj.get_record_definition_id('01.1.1.1.0.0.0.0')
    # content = data.get("content")
    # content["definition_id"] = '01.1.1.1.0.0.0.1'
    # content["unique_id"] = 1
    # obj.insert_record(data)
    data = obj.get_record_definition_id('01.1.1.1.0.0.0.1')
    content = data.get("content")
    model_list = content.get("model_list")
    model_list = ['o', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-', '-',
                   '-', '-', '-', '-', '-', '-', '-', '-']
    content["model_list"] = model_list
    if model_list:
        model_list[0] = 'O'
        model_list[1] = 'X'
    obj.update_record('01.1.1.1.0.0.0.1', data)

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
