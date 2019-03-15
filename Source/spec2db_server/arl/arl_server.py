# -*- coding: UTF-8 -*-
"""
Created on 2017-9-14

@author: hc
"""
import json
from Source.spec2db_server.arl.arl_base import ServiceBase
from Source.spec2db_server.arl.arl_group import ArlUser
from Source.spec2db_server.arl.arl_mail import ArlMail
from Source.spec2db_server.arl.commit_log import CommitLog
from Source.spec2db_server.arl.hu_server import HuRecord
from Source.spec2db_server.arl.def_server import DefRecord
from Source.spec2db_server.arl.analysis_service import AnalysisRecord
from Source.spec2db_server.arl.basic_hu import BasicHuRecord
from Source.spec2db_server.arl.basic_def import BasicDefRecord
from Source.spec2db_server.arl.basic_ana import BasicAnaRecord
from Source.spec2db_server.arl.whitelist_srv import WhitelistSrv


class ArlSpec(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)

    def get_category_tree(self, user_id=None):
        cat_tree = {"result": "OK/NG",
                    "content": [{"category_id": "",
                                 "category_name": "XXX",
                                 "sub_category_list": [{}]
                                }
                               ]
                    }
        cat_info_tree = self._get_category(user_id)
        cat_tree["content"] = self._trans_category(cat_info_tree)
        cat_tree["result"] = "OK"
        return cat_tree

    def get_group_category_tree(self, req_json):
        group_list = req_json.get("group_id")
        cat_tree = {"result": "OK/NG",
                    "content": [{"category_id": "",
                                 "category_name": "XXX",
                                 "sub_category_list": [{}]
                                }
                               ]
                    }
        cat_info_tree = self._get_group_category(group_list)
        cat_tree["content"] = self._trans_category(cat_info_tree)
        cat_tree["result"] = "OK"
        return cat_tree

    def get_hu_category_tree(self):
        cat_tree = {"result": "OK/NG",
                    "content": [{"category_id": "",
                                 "category_name": "XXX",
                                 "sub_category_list": [{}]
                                }
                               ]
                    }
        cat_info_tree = self._get_category()
        cat_tree["content"] = self._trans_category(cat_info_tree)
        cat_tree["result"] = "OK"
        return cat_tree

    def get_arl_by_id(self, arl_id):
        arl_record = {"result": "NG"}
        if not arl_id:
            return arl_record
        arl_rc = ArlRecord()
        arl_record["content"] = arl_rc.get_arl_by_id(arl_id)
        arl_record["result"] = "OK"
        return arl_record

    def get_by_category(self, data):
        result = {"result": "NG"}
        user_id = data.get("user_id")
        _type = data.get("type")
        category_id = data.get("category_id")
        filter_dict = data.get("condition")
        record_obj = None
        if _type == "arl":
            record_obj = ArlRecord()
        elif _type == "hu":
            record_obj = HuRecord()
        elif _type == "tagl_def":
            record_obj = DefRecord()
        elif _type == "tagl_ana":
            record_obj = AnalysisRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.get_by_category3(category_id, filter_dict, user_id)
            except:
                pass
        return result

    def summay_for_all(self, condition_data):
        result = {"result": "NG"}
        _type = condition_data.get("type")
        record_obj = None
        if _type == "arl":
            record_obj = ArlRecord()
        elif _type == "hu":
            record_obj = HuRecord()
        elif _type == "tagl_def":
            record_obj = DefRecord()
        elif _type == "tagl_ana":
            record_obj = AnalysisRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.summay_for_all(condition_data)
            except:
                pass
        return result

    def basic_summay_for_all(self, condition_data):
        result = {"result": "NG"}
        _type = condition_data.get("type")
        record_obj = None
        if _type == "arl":
            record_obj = BasicHuRecord()
        elif _type == "hu":
            record_obj = BasicHuRecord()
        elif _type == "tagl_def":
            record_obj = BasicDefRecord()
        elif _type == "tagl_ana":
            record_obj = BasicAnaRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.summay_for_all(condition_data)
            except:
                pass
        return result

    def summary_users(self, condition_data):
        result = {"result": "NG"}
        _type = condition_data.get("type")
        record_obj = None
        if _type == "arl":
            record_obj = ArlRecord()
        elif _type == "hu":
            record_obj = HuRecord()
        elif _type == "tagl_def":
            record_obj = DefRecord()
        elif _type == "tagl_ana":
            record_obj = AnalysisRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.summary_users(condition_data)
            except:
                pass
        return result

    def change_job_status(self, id, type, state):
        result = {"result": "NG"}
        _type = type
        record_obj = None
        if _type == "hu":
            record_obj = HuRecord()
        elif _type == "definition":
            record_obj = DefRecord()
        elif _type == "analysis":
            record_obj = AnalysisRecord()
        elif _type == "basic_req_hu":
            record_obj = BasicHuRecord()
        elif _type == "basic_req_definition":
            record_obj = BasicDefRecord()
        elif _type == "basic_req_analysis":
            record_obj = BasicAnaRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.update_job_status(id, state)
            except:
                pass
        return result

    def look_job_status(self, id, type):
        result = {"result": "NG"}
        _type = type
        record_obj = None
        if _type == "hu":
            record_obj = HuRecord()
        elif _type == "definition":
            record_obj = DefRecord()
        elif _type == "analysis":
            record_obj = AnalysisRecord()
        elif _type == "basic_req_hu":
            record_obj = BasicHuRecord()
        elif _type == "basic_req_definition":
            record_obj = BasicDefRecord()
        elif _type == "basic_req_analysis":
            record_obj = BasicAnaRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj._look_job_status(id)
            except:
                pass
        return result


    def get_block_white_list(self):
        api_data = dict()
        try:
            self._pg.connect()
            arl_obj = ArlRecord()
            block_data = arl_obj.get_lock_message(self._pg)
            api_data["hu_skiplist"] = block_data.get("hu_list")
            api_data["req_skiplist"] = block_data.get("def_list")
            api_data["ana_skiplist"] = block_data.get("ana_list")
            white_obj = WhitelistSrv()
            white_data = white_obj.get_white_list_by_classify(self._pg)
            if white_data.get("HU"):
                api_data["hu_exclude_whitelist"] = white_data.get("HU")
            else:
                api_data["hu_exclude_whitelist"] = []
            if white_data.get("DEF"):
                api_data["req_exclude_whitelist"] = white_data.get("DEF")
            else:
                api_data["req_exclude_whitelist"] = []
            if white_data.get("ANA"):
                api_data["ana_exclude_whitelist"] = white_data.get("ANA")
            else:
                api_data["ana_exclude_whitelist"] = []
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return api_data

    def get_user_by_category(self, data):
        result = {"result": "NG"}
        _type = data.get("type")
        category_id = data.get("category_id")
        filter_dict = data.get("condition")
        record_obj = None
        if _type == "arl":
            record_obj = ArlRecord()
        elif _type == "hu":
            record_obj = HuRecord()
        elif _type == "tagl_def":
            record_obj = DefRecord()
        elif _type == "tagl_ana":
            record_obj = AnalysisRecord()
        else:
            pass
        if record_obj:
            try:
                result = record_obj.get_user_by_category(category_id, filter_dict)
            except:
                pass
        return result

    def get_forest_model_type(self, _type):
        forest_model = []
        if _type == "arl":
            record_obj = ArlRecord()
            forest_model = record_obj.get_forest_model_type()
        elif _type == "hu":
            record_obj = HuRecord()
            forest_model = record_obj.get_forest_model_type()
        elif _type == "definition":
            record_obj = DefRecord()
            forest_model = record_obj.get_forest_model_type()
        elif _type == "analysis":
            record_obj = AnalysisRecord()
            forest_model = record_obj.get_forest_model_type()
        return forest_model

    def get_all_job_status(self):
        sqlcmd = """
        SELECT job_status_id, job_status
          FROM spec.arl_job_status
          order by job_status_id
        """
        job_status_list = list()
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd)
            rows = self._pg.fetchall()
            if rows:
                for row in rows:
                    job_status_dict = dict()
                    job_status_dict["job_status_id"], job_status_dict["job_status"] = row[0], row[1]
                    job_status_list.append(job_status_dict)
        finally:
            self._pg.close()
        return job_status_list

    def get_arl_by_category(self, category_id, size, page, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        if len(cat_id_list) != 5:
             return arl_record
        arl_rc = ArlRecord()
        count, arl_record["content"] = arl_rc.get_arl_by_category(cat_id_list,
                                                                  size,
                                                                  page,
                                                                  user_id)
        arl_record["total_count"] = count
        arl_record["result"] = "OK"
        return arl_record

    def new_get_arl_by_category(self, category_id, size, page, user_id=None):
        arl_record = {"result": "NG"}
        if not category_id:
            return arl_record
        cat_id_list = [int(n) for n in category_id.split('-')]
        arl_rc = ArlRecord()
        count, arl_record["content"] = arl_rc.new_get_by_category(cat_id_list,
                                                                  size,
                                                                  page,
                                                                  user_id)
        if arl_record["content"]:
            arl_record["total_count"] = count
            arl_record["result"] = "OK"
        return arl_record

    def get_by_id_deep(self, arl_id, user_id, group_id):
        data_list = []
        try:
            self._pg.connect()
            arl_obj = ArlRecord()
            data_list = arl_obj.get_by_id_deep(self._pg, arl_id, user_id, group_id)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return data_list

    def get_arl_by_user_id(self, user_id, size, page):
        arl_record = {"result": "NG"}
        if not user_id:
            return arl_record
        arl_rc = ArlRecord()
        count, arl_record["content"] = arl_rc.get_arl_by_category(user_id,
                                                                  size,
                                                                  page)
        if arl_record["content"]:
            arl_record["total_count"] = count
            arl_record["result"] = "OK"
        return arl_record

    def _trans_category(self, cat_info_tree, p_cat_id=None):
        # cat_dict = {"category_id": "", "category_name": "",
        #             "sub_category_list": [{}]}
        if not cat_info_tree:
            return []
        category_list = []
        for key in sorted(cat_info_tree.iterkeys(), key=lambda x: x[1]):
            sub_cat_tree = cat_info_tree.get(key)
            cat_dict = {}
            if p_cat_id:
                cat_dict["category_id"] = '-'.join([p_cat_id, str(key[0])])
            else:
                cat_dict["category_id"] = str(key[0])
            cat_dict["category_name"] = key[1]
            sub_category_list = self._trans_category(sub_cat_tree,
                                                     cat_dict.get("category_id")
                                                     )
            cat_dict["sub_category_list"] = sub_category_list
            category_list.append(cat_dict)
        return category_list

    def _get_category(self, user_id=None):
        if user_id:
            sqlcmd = """
            SELECT cat_id0, category,
                   cat_id1, major_category,
                   cat_id2, medium_catetory,
                   cat_id3, small_category,
                   cat_id4, detail
              FROM spec.arl
              where user_id = %s 
                    and exclude_flag = False
              ORDER BY cat_id0, cat_id1, cat_id2, cat_id3, cat_id4;
            """
        else:
            sqlcmd = """
            SELECT cat_id0, category,
                   cat_id1, major_category,
                   cat_id2, medium_catetory,
                   cat_id3, small_category,
                   cat_id4, detail
              FROM spec.arl
              where exclude_flag = False
              ORDER BY cat_id0, cat_id1, cat_id2, cat_id3, cat_id4;
            """
        self._pg.connect()
        if user_id:
            self._pg.execute(sqlcmd, (user_id,))
        else:
            self._pg.execute(sqlcmd)
        cat_info_tree = {}
        for row in self._pg.fetchall():
            j = 0
            cat = cat_info_tree
            while j < len(row):
                cat_id = row[j]
                cat_name = row[j + 1]
                key = (cat_id, cat_name)
                if key in cat:
                    cat = cat.get(key)
                else:
                    cat[key] = {}
                    cat = cat.get(key)
                j += 2
        self._pg.close()
        return cat_info_tree

    def _get_group_category(self, group_list):
        if group_list:
            str_group = str(group_list).replace("[", "(").replace("]", ")")
            condition_str = str_group

        sqlcmd = """
        SELECT cat_id0, category,
               cat_id1, major_category,
               cat_id2, medium_catetory,
               cat_id3, small_category,
               cat_id4, detail
          FROM spec.arl
          where group_id in {condition_str}
                and exclude_flag = False
          ORDER BY cat_id0, cat_id1, cat_id2, cat_id3, cat_id4;
        """.format(condition_str=condition_str)
        self._pg.connect()

        self._pg.execute(sqlcmd)
        cat_info_tree = {}
        for row in self._pg.fetchall():
            j = 0
            cat = cat_info_tree
            while j < len(row):
                cat_id = row[j]
                cat_name = row[j + 1]
                key = (cat_id, cat_name)
                if key in cat:
                    cat = cat.get(key)
                else:
                    cat[key] = {}
                    cat = cat.get(key)
                j += 2
        self._pg.close()
        return cat_info_tree


class ArlRecord(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "arl"
        self.model_table_name = "arl_model_rel"
        self.model_type_table_name = "arl_model_type"
        self.key_col = "arl_record_id"
        self.id_col = "arl_id"
        self.sub_list_name = "hu_list"
        self.child_id_col = "arl_id"
        self.attr_list = ["arl_record_id", "mm_new_num", "charge",
                          "mm_item", "tagl_exclude", "category",
                          "id1", "major_category", "level1",
                          "id2", "medium_catetory", "level2",
                          "id3", "small_category", "level3",
                          "id4", "detail", "level4",
                          "func_summary_jp", "func_summary_en", "supply",
                          "subid", "arl_id", "req_post",
                          "remark", "exception", "status",
                          "trigger", "action", "arl_user",
                          "dealer", "developer", "supplier",
                          "company_rule", "law", "old_bug",
                          "policy", "hmi_spec_no", "hmi_version",
                          "hmi_file_name", "hmi_chapter", "hmi_page",
                          "func_spec_no", "func_version", "func_file_name",
                          "func_chapter", "func_page", "if_spec",
                          "center_spec", "other_spec", "same_req",
                          "sys_conf_id", "author", "future_req",
                          "req_omission", "censure", "screen_id",
                          "job_status", "md5_key", "major_ver",
                          "user_id", "group_id", "exclude_flag",
                          "lock_status"
                          ]
        self._attr_list = ["arl_record_id", "category_name", "major_category",
                           "medium_category", "small_category", "id",
                           "detail", "dev_summary", "summary",
                           "extra_info", "sub_id", "arl_id",
                           "from_info", "memo", "except",
                           "status", "trigger", "action",
                           "IF_book", "center_book", "other_book",
                           "same_content", "system_id"]
        self._dest_category = ["user", "dealer", "developer",
                               "supplier", "company_rule", "law",
                               "history_problem", "dest_background"]
        self._hmi_book = ["book_no", "version",	"file_name",
                          "chapter", "page"]
        self._func_book = ["book_no", "version", "file_name",
                           "chapter", "page"]
        self._manage_memo = ["user", "no_analyze", "miss_content"]

    def basic_or_hu_content_post(self, data_list, update_time):
        self._pg.connect()
        data_dict = data_list[0]
        commit_user_id = data_dict.get("modify_user_id")
        result = {"result": "NG", "error": ''}
        if data_dict.get("hu_id"):  # HU
            _id = data_dict.get("hu_id")
            if self.is_basic(_id):
                record_obj = BasicHuRecord()
            else:
                record_obj = HuRecord()
        elif data_dict.get("hu_def_id"):  # DEF
            _id = data_dict.get("definition_id")
            if self.is_basic(_id):
                record_obj = BasicDefRecord()
            else:
                record_obj = DefRecord()
        else:  # ANA
            _id = data_dict.get("definition_id")
            if self.is_basic(_id):
                record_obj = BasicHuRecord()
            else:
                record_obj = HuRecord()
        try:
            old_arl_data = record_obj.get_by_id_for_diff(self._pg, _id, record_obj.attr_list)
            log_list = record_obj.common_add(self._pg, data_dict, old_arl_data, update_time, check_md5=True)
            if log_list is not None:
                if log_list:
                    # from Source.spec2db_server.arl.arl_func import ArlFunc
                    # check_obj = ArlFunc()
                    # TODO
                    # flag, e = check_obj.check_data_list(self._pg, data_list, commit_user_id)
                    flag = True
                    e = ''
                    if not flag:
                        self._pg.conn.rollback()
                        self._pg.close()
                        try:
                            result["error"] = str(e.collection[0].coord)
                        except Exception:
                            result["error"] = str(e)
                        return result
                    log_info = {'user_id': commit_user_id, "commit_list": log_list}
                    commit_log = CommitLog()
                    flag, commit_id = commit_log.add_commit_log2(self._pg, log_info)
                    if flag:
                        hu_check_list, def_check_list, ana_check_list = self.check_function(data_dict)
                        ojj = ServiceBase()
                        if hu_check_list:
                            ojj.insert_check_list(self._pg, commit_id, 'basic_req_hu', hu_check_list)
                        if def_check_list:
                            ojj.insert_check_list(self._pg, commit_id, 'basic_req_definition', def_check_list)
                        if ana_check_list:
                            ojj.insert_check_list(self._pg, commit_id, 'basic_req_analysis', ana_check_list)
                        self._pg.commit()
                result["result"] = "OK"
                result["content"] = data_list
            else:
                self._pg.conn.rollback()
        except Exception as e:
            print e
            result["error"] = str(e)
            if self._pg.connected:
                self._pg.conn.rollback()
        finally:
            self._pg.close()
        return result

    def is_basic(self, _id):
        if _id[0] in ('B', 'C', 'D'):
            return True
        else:
            return False

    def check_function(self, arl_data_dict):
        arl_tree_list = arl_data_dict
        hu_data = []
        def_data = []
        ana_data = []
        data_list = dict()
        if arl_tree_list.get("list1"):
            rows = arl_tree_list.get("list1")
            hu_list_rows = rows.get("hu")
            def_list_rows = rows.get("definition")
            ana_list_rows = rows.get("analysis")
            for hu_list_row in hu_list_rows:
                hu_check_list = {}
                hu_check_list["cl_item_id"] = hu_list_row.get("id")
                hu_check_list["author_check"] = hu_list_row.get("author_check")
                hu_data.append(hu_check_list)
            for def_list_row in def_list_rows:
                def_check_list = {}
                def_check_list["cl_item_id"] = def_list_row.get("id")
                def_check_list["author_check"] = def_list_row.get("author_check")
                def_data.append(def_check_list)
            for ana_list_row in ana_list_rows:
                ana_check_list = {}
                ana_check_list["cl_item_id"] = ana_list_row.get("id")
                ana_check_list["author_check"] = ana_list_row.get("author_check")
                ana_data.append(ana_check_list)
        elif arl_tree_list.get("list2"):
            rows = arl_tree_list.get("list2")
            hu_list_rows = rows.get("hu")
            def_list_rows = rows.get("definition")
            ana_list_rows = rows.get("analysis")
            for hu_list_row in hu_list_rows:
                hu_check_list = {}
                hu_check_list["cl_item_id"] = hu_list_row.get("id")
                hu_check_list["charger_check"] = hu_list_row.get("charger_check")
                hu_data.append(hu_check_list)

            for def_list_row in def_list_rows:
                def_check_list = {}
                def_check_list["cl_item_id"] = def_list_row.get("id")
                def_check_list["charger_check"] = def_list_row.get("charger_check")
                def_data.append(def_check_list)
            for ana_list_row in ana_list_rows:
                ana_check_list = {}
                ana_check_list["cl_item_id"] = ana_list_row.get("id")
                ana_check_list["charger_check"] = ana_list_row.get("charger_check")
                ana_data.append(ana_check_list)
        data_list["hu_check_list"] = hu_data
        data_list["def_check_list"] = def_data
        data_list["ana_check_list"] = ana_data
        return data_list["hu_check_list"], data_list["def_check_list"], data_list["ana_check_list"]

    def arl_full_content_post(self, data_list, update_time):
        result = {"result": "NG", "error": ''}
        if not data_list:
            result["error"] = u'无数据。'
            return result
        arl_data_dict = data_list[0]
        arl_id = arl_data_dict.get(self.id_col)
        commit_user_id = arl_data_dict.get("modify_user_id")
        if not commit_user_id:
            print 'Modify User Id is None.'
            result["error"] = u'未指定提交者.'
            return result
        if arl_id:
            try:
                self._pg.connect()
                old_arl_data = self._get_arl_by_id_for_diff(self._pg, arl_id)
                if old_arl_data:
                    self.recovery_unkown_ch(arl_data_dict, old_arl_data)
                    log_list = self._common_add(self._pg, arl_data_dict, old_arl_data, update_time, check_md5=True)
                    if log_list is not None:
                        if log_list:
                            from Source.spec2db_server.arl.arl_func import ArlFunc
                            check_obj = ArlFunc()
                            flag, e = check_obj.check_data_list(self._pg, data_list, commit_user_id)
                            if not flag:
                                self._pg.conn.rollback()
                                self._pg.close()
                                try:
                                    result["error"] = str(e.collection[0].coord)
                                except Exception:
                                    result["error"] = str(e)
                                return result
                            log_info = {'user_id': commit_user_id, "commit_list": log_list}
                            commit_log = CommitLog()
                            flag, commit_id = commit_log.add_commit_log2(self._pg, log_info)
                            if flag:
                                hu_check_list, def_check_list, ana_check_list = self.check_function(arl_data_dict)
                                ojj = ServiceBase()
                                if hu_check_list:
                                    ojj.insert_check_list(self._pg, commit_id, 'hu', hu_check_list)
                                if def_check_list:
                                    ojj.insert_check_list(self._pg, commit_id, 'definition', def_check_list)
                                if ana_check_list:
                                    ojj.insert_check_list(self._pg, commit_id, 'analysis', ana_check_list)
                                self._pg.commit()
                        result["result"] = "OK"
                        result["content"] = data_list
                    else:
                        self._pg.conn.rollback()
            except Exception as e:
                print e
                result["error"] = str(e)
                if self._pg.connected:
                    self._pg.conn.rollback()
            finally:
                self._pg.close()
        return result

    def _update_new_date(self, data, old_data, update_time):
        """ARL不更新new_date"""
        return

    def _add_sub(self, pg, data, update_time):
        arl_id = data.get(self.id_col)
        hu_data_list = data.get(self.sub_list_name)
        hu_obj = HuRecord()
        sub_log_list = hu_obj.add_list(pg, arl_id, hu_data_list, update_time)
        return sub_log_list

    def get_new_version(self, pg, data, old_data):
        major_ver, small_ver = old_data.get("major_ver"), old_data.get("small_ver")
        return major_ver, small_ver

    def get_arl_by_id(self, arl_id):
        sqlcmd = """
        SELECT arl_record_id, category, major_category,
               medium_catetory, small_category, id4,
               detail, func_summary_jp, func_summary_en,
               supply, subid, arl_id,
               req_post, remark, exception,
               status, trigger, action,
               if_spec, center_spec, other_spec,
               same_req, sys_conf_id,
               ---- dest_category-------------
               arl_user, dealer, developer,
               supplier, company_rule, law,
               old_bug, policy,
               ----- hmi_book ----------------
               hmi_spec_no, hmi_version, hmi_file_name,
               hmi_chapter, hmi_page,
               ----- func book ---------------
               func_spec_no, func_version, func_file_name,
               func_chapter, func_page,
               ----- manage_memo ------------
               author, future_req, req_omission,
               user_id, group_id
               md5_key, major_ver, small_ver
          FROM spec.arl as tt1
          where arl_id = %s
          ORDER BY arl_record_id
          limit 1
        """
        attr_dict = {}
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            attr_dict = self.get_arl_dict(row)
            arl_rc_id = row[0]
            attr_dict["model_list"] = self.get_model_list2(arl_rc_id)
        self._pg.close()
        return attr_dict

    def _get_arl_by_id_for_diff(self, pg, arl_id):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        data_dict = dict()
        pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            for i, attr in enumerate(self.attr_list, 0):
                data_dict[self.attr_list[i]] = row[i]
        return data_dict

    def get_by_id_deep(self, pg, _id, user_id, group_id):
        """
        :param pg: 
        :param _id: 
        :param user_id: 
        :param group_id: 
        :return: 
        """""
        if not _id:
            return []
        info_list = []
        arl_dict = self.get_by_id(pg, _id, self.attr_list)
        self.del_unkown_ch(arl_dict)
        if arl_dict:
            hu_obj = HuRecord()
            arl_dict["hu_list"] = hu_obj.get_by_id_deep(pg, _id)
            arl_user_id = arl_dict.get("user_id")
            # 设置权限控制
            control_list = self._get_procudure_control(pg, arl_user_id, user_id)
            self._set_procudure_control(arl_dict, control_list)
        info_list.append(arl_dict)
        return info_list

    def del_unkown_ch(self, data):
        for key, val in data.iteritems():
            if type(val) in (str, unicode):
                data[key] = val.replace(u'_x000D_', u'')

    def recovery_unkown_ch(self, data, old_data):
        for key, val in data.iteritems():
            if key in ("user_id", "group_id"):
                continue
            old_val = old_data.get(key)
            if old_val and val:
                if type(val) in (str, unicode):
                    data[key] = old_val

    def _set_procudure_control(self, arl_dict, control_list):
        arl_dict["control_list"] = control_list
        for hu_info in arl_dict.get("hu_list"):
            hu_info["control_list"] = control_list
            for def_info in hu_info.get("definition_list"):
                def_info["control_list"] = control_list
                for analysis_info in def_info.get("analysis_list"):
                    analysis_info["control_list"] = control_list

    def _get_procudure_control(self, pg, arl_user_id, curr_user_id):
        """取得流程控制权限
        :param arl_user_id:
        :param curr_user_id:
        :return: []
        """
        sqlcmd = """
        SELECT role, array_agg(job_status_id)
          FROM (
            SELECT DISTINCT t2.role, job_status_id
              FROM (
                SELECT group_id, user_id, role, role_id
                  FROM spec.arl_group_member
                  where user_id = %s
                  ORDER BY user_id
              ) as t1
              left join spec.arl_role_power as t2
              on t1.role_id = t2.role_id
              LEFT JOIN spec.arl_procudure_control as t3
              ON t2.role_id = t3.role_id
              ORDER BY t2.role, job_status_id
          ) as tt1
          group by role
        """
        pg.execute(sqlcmd, [curr_user_id])
        rows = pg.fetchall()
        role_set = set()
        control_set = set()
        if rows:
            for row in rows:
                role, job_status_ids = row[0], row[1]
                role_set.add(role)
                control_set.update(job_status_ids)
        if role_set:
            if role_set == set(["Member"]):
                if arl_user_id != curr_user_id:
                    return []
        return sorted(control_set)

    def get_by_id(self, pg, _id, col_list):
        sqlcmd = self.list_2_select_sql(self.table_name, self.attr_list, [self.id_col])
        pg.execute(sqlcmd, [_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
            record_id = row[0]
            attr_dict["title"] = 'ARL: ' + attr_dict[self.id_col]
            # model_list = self.get_model_list(pg, record_id)
            # attr_dict["model_list"] = model_list
        return attr_dict

    def get_by_user_id(self, user_id, size, page):
        arl_record = {"result": "NG"}
        if not user_id:
            return arl_record
        arl_rc = ArlRecord()
        count, arl_record["content"] = arl_rc._get_by_user_id(user_id, size,
                                                              page)
        if count > 0:
            arl_record["total_count"] = count
            arl_record["result"] = "OK"
        return arl_record

    def get_by_group_id(self, user_id, size, page):
        arl_record = {"result": "NG"}
        if not user_id:
            return arl_record
        arl_rc = ArlRecord()
        count, arl_record["content"] = arl_rc._get_by_user_id(user_id, size,
                                                              page)
        if count > 0:
            arl_record["total_count"] = count
            arl_record["result"] = "OK"
        return arl_record

    def _get_by_user_id(self, user_id, size, page):
        sqlcmd = """
                SELECT detail, subid, arl_id,
                       req_post, remark, exception,
                       status, trigger, action,
                       job_status
                  FROM spec.arl as tt1
                  where user_id = %s
                  ORDER BY arl_record_id;
                """
        attr_list = ["detail", "sub_id", "arl_id", "from_info", "memo",
                     "except", "status", "trigger", "action", "job_status"]
        self._pg.connect()
        offset = size * (page - 1)
        self._pg.execute(sqlcmd, user_id)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(attr_list):
                attr_dict[attr_list[i]] = row[i]
                i += 1
            attr_dict_list.append(attr_dict)
        self._pg.close()
        return rowcount, attr_dict_list

    def new_get_by_category(self, cat_id_list, size, page, user_id=None):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        condition = condition.replace('user_id', 'tt1.user_id')
        sqlcmd = """
        SELECT tt1.detail, subid, tt1.arl_id,
               tt1.req_post, remark, exception,
               status, trigger, action,
               job_status, user_name, hu_date,
               def_date, analysis_date    
          FROM spec.arl as tt1
          LEFT JOIN spec.arl_user as tt2
          ON tt1.user_id = tt2.user_id
          LEFT JOIN spec.arl_schedule as tt3
          ON tt1.arl_id = tt3.arl_id
          %s  -- condition
          ORDER BY length(tt1.arl_id), tt1.arl_id;
        """ % condition
        attr_list = ["detail", "sub_id", "arl_id",
                     "from_info", "memo", "except",
                     "status", "trigger", "action",
                     "job_status", "user_name"
                     ]
        self._pg.connect()
        offset = size * (page - 1)
        self._pg.execute(sqlcmd, params)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def get_by_categorysql3(self, cat_id_list, filter_list, user_id):
        condition, params = self.get_category_condition(cat_id_list, user_id)
        filter_cond = self.get_filter_condition(filter_list)
        if filter_cond:
            condition += ' and ' + 'tt1.'+filter_cond
            print "arl:", filter_cond
        sqlcmd = """
        SELECT tt1.detail, subid, tt1.arl_id,
               tt1.req_post, remark, exception,
               status, trigger, action,
               job_status, user_name, hu_date,
               def_date, analysis_date    
          FROM spec.arl as tt1
          LEFT JOIN spec.arl_user as tt2
          ON tt1.user_id = tt2.user_id
          LEFT JOIN spec.arl_schedule as tt3
          ON tt1.arl_id = tt3.arl_id
          %s  -- condition
          ORDER BY length(tt1.arl_id), tt1.arl_id;
        """ % condition
        self._pg.connect()
        self._pg.execute(sqlcmd, params)
        rows = self._pg.fetchall()
        rowcount = self._pg.pgcur.rowcount
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _get_summary_data_list(self, condition_str, params, like_condition, complete_str, size, page):
        condition_str = condition_str.replace('user_id', 'tt1.user_id')
        like_condition = like_condition.replace('arl_id', 'tt1.arl_id')
        if condition_str:
            if like_condition:
                condition_str += 'and ' + like_condition
        else:
            condition_str = 'where ' + like_condition
        if complete_str == '2':
            child_str = """
            inner join (
                select arl_id
                from spec.hu
                where job_status = 2
                union
                SELECT ARRAY_TO_STRING(a[1:ARRAY_UPPER(a, 1) - 2], '.') as arl_id
                from (
                    select definition_id, regexp_split_to_array(definition_id, E'\\.+') a
                    from spec.definition
                    where job_status = 2
                    ) as b
                union
                SELECT ARRAY_TO_STRING(a[1:ARRAY_UPPER(a, 1) - 2], '.') as arl_id
                from (
                    select definition_id, regexp_split_to_array(definition_id, E'\\.+') a
                    from spec.analysis
                    where job_status = 2
                    ) as b
                ) as com
            on tt1.arl_id = com.arl_id
            """
            if condition_str:
                condition_str += 'and ' + " hu_date <> '-'"
            else:
                condition_str = 'where ' + " hu_date <> '-'"
        elif complete_str:
            child_str = """
            LEFT JOIN spec.hu as child
            ON tt1.arl_id = child.arl_id
            """
            if condition_str:
                condition_str += 'and ' + complete_str + " and hu_date <> '-'"
            else:
                condition_str = 'where ' + complete_str + " and hu_date <> '-'"
        else:
            child_str = ""
        sqlcmd = """
        SELECT distinct tt1.detail, subid, tt1.arl_id,
               tt1.req_post, tt1.remark, tt1.exception,
               tt1.status, tt1.trigger, tt1.action,
               tt1.job_status, user_name, hu_date,
               def_date, analysis_date, tt1.update_time, length(tt1.arl_id) as len
          FROM spec.arl as tt1
          LEFT JOIN spec.arl_user as tt2
          ON tt1.user_id = tt2.user_id
          LEFT JOIN spec.arl_schedule as tt3
          ON tt1.arl_id = tt3.arl_id
          {child_str}
          {condition_str}
          ORDER BY tt1.update_time DESC;
        """.format(child_str=child_str,
                   condition_str=condition_str)
        self._pg.connect()
        rowcount, rows = self._fetch_many(self._pg, sqlcmd, params, size, page)
        attr_dict_list = self._rows_2_summay_data(rows)
        self._pg.close()
        return rowcount, attr_dict_list

    def _rows_2_summay_data(self, rows):
        attr_list = ["detail", "sub_id", "arl_id",
                     "from_info", "memo", "except",
                     "status", "trigger", "action",
                     "job_status", "user_name", "hu_date",
                     "def_date", "analysis_date"
                     ]
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(attr_list):
                attr_dict[attr_list[i]] = row[i]
                i += 1
            attr_dict['title'] = 'ARL: ' + attr_dict['arl_id']
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def _get_summary_user_list(self, condition_str, params, like_condition):
        condition_str = condition_str.replace('user_id', 'tt1.user_id')
        if like_condition:
            condition_str += ' and ' + like_condition
        sqlcmd = """
        SELECT DISTINCT tt1.user_id, tt2.user_name
          FROM spec.arl as tt1
          LEFT JOIN spec.arl_user as tt2
          ON tt1.user_id = tt2.user_id
          {condition_str}
          ORDER BY user_name;
        """.format(condition_str=condition_str)
        user_list = []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, params)
            rows = self._pg.fetchall()
            self._pg.close()
            for row in rows:
                user_id = row[0]
                user_name = row[1]
                user_list.append({"user_id": user_id, "user_name": user_name})
        except Exception as e:
            print e
        finally:
            self._pg.close()
        return user_list

    def _get_user_by_category(self, cat_id_list, filter_list):
        condition, params = self.get_category_condition(cat_id_list, user_id=None)
        filter_cond = self.get_filter_condition(filter_list)
        if filter_cond:
            condition += ' and ' + filter_cond
        sqlcmd = """
        SELECT distinct tt1.user_id, user_name
          FROM spec.arl as tt1
          LEFT JOIN spec.arl_user as tt2
          ON tt1.user_id = tt2.user_id
          %s  -- condition
          ORDER BY user_name;
        """ % condition
        # attr_list = ["user_id", "user_name"]
        self._pg.connect()
        self._pg.execute(sqlcmd, params)
        rows = self._pg.fetchall()
        rowcount = self._pg.pgcur.rowcount
        self._pg.close()
        user_dict_list = []
        for row in rows:
            attr_dict = dict()
            attr_dict["user_id"], attr_dict["user_name"] = row[:2]
            user_dict_list.append(attr_dict)
        return rowcount, user_dict_list

    def get_arl_by_category(self, cat_id_list, size, page, user_id=None):
        sqlcmd = """
        SELECT detail, subid, arl_id,
               req_post, remark, exception,
               status, trigger, action
          FROM spec.arl as tt1
          where cat_id0 = %s and cat_id1 = %s and
                    cat_id2 = %s and cat_id3 = %s and cat_id4 = %s
          ORDER BY arl_record_id;
        """
        if user_id:
            sqlcmd = """
            SELECT detail, subid, arl_id,
                   req_post, remark, exception,
                   status, trigger, action
              FROM spec.arl as tt1
              where user_id = %s and
                    cat_id0 = %s and cat_id1 = %s and
                    cat_id2 = %s and cat_id3 = %s and
                    cat_id4 = %s
              ORDER BY arl_record_id;
            """
        attr_list = ["detail", "sub_id", "arl_id",
                     "from_info", "memo", "except",
                     "status", "trigger", "action"
                     ]
        self._pg.connect()
        offset = size * (page - 1)
        if user_id:
            self._pg.execute(sqlcmd, [user_id] + cat_id_list)
        else:
            self._pg.execute(sqlcmd, cat_id_list)
        rowcount = self._pg.pgcur.rowcount
        if rowcount > 0:
            if offset >= rowcount - 1:
                return rowcount, []
            self._pg.pgcur.scroll(offset)
        rows = self._pg.pgcur.fetchmany(size)
        attr_dict_list = []
        for row in rows:
            attr_dict = {}
            i = 0
            while i < len(attr_list):
                attr_dict[attr_list[i]] = row[i]
                i += 1
            attr_dict["HU_num"] = ''
            attr_dict["func_def_num"] = ''
            attr_dict["func_anaylize_num"] = ''
            attr_dict['title'] = 'ARL: '+attr_dict['arl_id']
            attr_dict_list.append(attr_dict)
        self._pg.close()
        return rowcount, attr_dict_list

    def get_model_list(self, arl_rc_id):
        """树型结构"""
        model_list = []
        # model_dict = {"content": "", "sub_content":[{},]}
        for model, val in self._get_model_list(arl_rc_id):
            sub_mode_list = model_list
            for model_element in model + [val]:
                matched_flag = False
                for sub_model in sub_mode_list:
                    if model_element == sub_model.get('content'):
                        sub_mode_list = sub_model.get('sub_content')
                        matched_flag = True
                        break
                if matched_flag:
                    continue
                new_model_dict = {"content": model_element,
                                  "sub_content": []}
                sub_mode_list.append(new_model_dict)
                sub_mode_list = new_model_dict.get('sub_content')
        return model_list

    def get_model_list2(self, arl_rc_id):
        model_list = []
        # model_dict = {"content": "", "sub_content":[{},]}
        for model, val in self._get_model_list(arl_rc_id):
            model_list.append(val)
        return model_list

    def get_arl_dict(self, row):
        attr_dict = {}
        i = 0
        while i < len(self._attr_list):
            attr_dict[self._attr_list[i]] = row[i]
            i += 1
        dest_category = {}
        for j in range(0, len(self._dest_category)):
            dest_category[self._dest_category[j]] = row[i]
            i += 1
        attr_dict["dest_category"] = dest_category
        for key in ["IF_book", "center_book", "other_book", "same_content"]:
            # TODO
            attr_dict[key] = attr_dict.get(key)
        hmi_book = self._split_attr(row[i: i + len(self._hmi_book)],
                                    self._hmi_book)
        attr_dict["HMI_book"] = hmi_book
        i += len(self._hmi_book)
        func_book = self._split_attr(row[i: i + len(self._func_book)],
                                     self._func_book)
        attr_dict["func_book"] = func_book
        i += len(self._func_book)
        manage_memo = {}
        for j in range(0, len(self._manage_memo)):
            manage_memo[self._manage_memo[j]] = row[i]
            i += 1
        attr_dict["manage_memo"] = manage_memo
        return attr_dict

    def get_arl_post_info(self, arl_id):
        post_list = ["arl_id", "major_categor", "medium_catetory",
                     "small_category", "detail", "base",
                     "req_post", "remark", "status",
                     "trigger", "action"]
        sqlcmd = """
        SELECT arl_id, major_category, medium_catetory,
               small_category,  detail, '' as base,
               req_post, remark, status,
               trigger, action
          FROM spec.arl
          where arl_id = %s
          limit 1
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        data = {"result": "NG"}
        content = {}
        if row:
            for i in range(0, len(row)):
                attr = post_list[i]
                content[attr] = row[i]
        if content:
            data["content"] = content
            data["result"] = "OK"
        self._pg.close()
        return data

    def _split_attr(self, infos, attr_list):
        split_list = []
        max_count = 1
        for info in infos:
            if info:
                if type(info) in (str, unicode):
                    temp_splited = info.split('\n')
                    if max_count < len(temp_splited):
                        max_count = len(temp_splited)
                    split_list.append(temp_splited)
                else:
                    split_list.append(info)
            else:
                split_list.append([''])
        i = 0
        while i < len(split_list):
            split_list[i] = split_list[i] + [''] * (max_count - len(split_list[i]))
            i += 1
        attr_dict_list = []
        for temp_list in zip(*split_list):
            attr_dict = {}
            i = 0
            while i < len(temp_list):
                attr_dict[attr_list[i]] = temp_list[i]
                i += 1
            attr_dict_list.append(attr_dict)
        return attr_dict_list

    def _get_model_list(self, _id):
        sqlcmd = """
        SELECT model, val
          FROM spec.arl_model_rel as a
          LEFT JOIN spec.arl_model_type as b
          ON a.model_id = b.model_id
          WHERE arl_record_id = %s
          ORDER BY order_no
        """
        self._pg.execute(sqlcmd, (_id,))
        rows = self._pg.fetchall()
        for row in rows:
            model, val = row[0], row[1]
            model = json.loads(model)
            yield model, val

    def get_category(self, arl_id):
        sqlcmd = """
        SELECT cat_id0, cat_id1, cat_id2, cat_id3, cat_id4
          FROM spec.arl
          where arl_id = %s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        if row:
            return list(row)
        self._pg.close()
        return []

    def assign_user(self, data):
        result = {"result": "NG"}
        arl_ids = data.get("arl")
        user_id = data.get("user_id")
        group_id = data.get("group_id")
        if not arl_ids:
            result["error"] = 'Doset not indicate arl_id.'
            return result
        if not user_id:
            result["error"] = 'Doset not indicate user_id.'
            return result
        if not group_id:
            result["error"] = 'Doset not indicate group_id.'
            return result
        sqlcmd = """
        UPDATE spec.arl set user_id = %s, group_id = %s
           WHERE arl_id = %s;
        """
        try:
            self._pg.connect()
            for arl_id in arl_ids:
                self._pg.execute(sqlcmd, (user_id, group_id, arl_id))
            self._pg.commit()
            self._send_mail(user_id, arl_ids)
            result["result"] = "OK"
            self._pg.close()
        finally:
            pass
        return result

    def _send_mail(self, user_id, arl_ids):
        usr_obj = ArlUser()
        email = usr_obj.get_email(user_id)
        if email:
            mail_obj = ArlMail(to_list=[email])
            mail_obj.send_tranfer(arl_ids)

    def get_graph(self, arl_id):
        from Source.spec2db_server.arl.hu_server import HuRecord
        g = {"ARL": arl_id}
        hu_obj = HuRecord()
        g["children"] = hu_obj.get_graph(arl_id)
        return g

    def get_group_id(self, hu_id):
        sqlcmd = """
            SELECT group_id from spec.arl as a left join
            spec.hu as h on a.arl_id = h.arl_id where h.hu_id = %s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (hu_id,))
        row = self._pg.fetchone()
        group_id = row[0]
        self._pg.close()
        return group_id

    def add(self, pg, data, col_list, update_time, check_md5=False, excel_import=True, major_ver='0.40'):
        arl_id = data.get(self.id_col)
        old_data = self.get_by_arl_id(pg, arl_id, self.attr_list)
        if check_md5 and not self.check_md5_key(data, old_data):
            return
        if old_data:
            data["arl_record_id"] = old_data.get("arl_record_id")
            data["major_ver"] = old_data.get("major_ver")
            data["md5_key"] = old_data.get("md5_key")
            data["user_id"] = old_data.get("user_id")
            data["group_id"] = old_data.get("group_id")
            if data.get("exclude_flag") and not old_data.get("exclude_flag"):
                print data.get("arl_id"), "exclude_flag=True"
                return
        ignore_col_list = [self.sub_list_name]
        from Source.spec2db_server.arl.arl_diff import ArlDiff
        diff_obj = ArlDiff("arl_record_id", "arl_id", self.attr_list, ignore_col_list)
        diff_result = diff_obj.diff(old_data, data)
        action = diff_result.get("action")
        if action == "same":
            return
        md5_key = self.generate_md5_key(data)
        data["md5_key"] = md5_key
        data["major_ver"] = major_ver
        data["update_time"] = update_time
        if action == "add":
            rc_id, model_list_change = self._add_one2(pg, data, self.attr_list[1:])
            data[self.key_col] = rc_id
            diff_result["arl_record_id"] = rc_id
            model_list = diff_result.get("model_list")
            for i in range(len(model_list)):
                model_list[i]["data"] = model_list_change[i]
                model_list[i]["record_id"] = model_list_change[i].get("order_no")

        elif action == "change":
            col_change_list = diff_result.get("col_change_list")
            col_change_list.append("major_ver")
            col_change_list.append("md5_key")
            col_change_list.append("update_time")
            arl_record_id = diff_result.get("arl_record_id")
            if col_change_list:
                if self.update_col_change_list(pg, arl_record_id, data, col_change_list):
                    model_diff_list = diff_result.get("model_list")
            if not self.update_model_diff_list(pg, arl_record_id, model_diff_list):
                return
            # self.get_by_id_deep(arl_id, user_id=7, group_id=)

            # from hu_server import HuRecord
            # hu_obj = HuRecord()
            # old_hu = hu_obj._get_by_parent_id(pg, arl_id)
            # status_change_list = ["job_status"]
            # if old_hu:
            #     old_hu_dict = old_hu[0]
            #     old_hu_dict["job_status"] = "init"
            #     hu_record_id = old_hu_dict.get("hu_record_id")
            #     hu_id = old_hu_dict.get("hu_id")
            #     if old_hu.update_col_change_list(pg, hu_record_id, old_hu_dict, status_change_list):
            #         hu_dict = dict()
            #         hu_dict["table_name"] = hu_obj.table_name
            #         hu_dict["action"] = "change"
            #         hu_dict["record_id"] = hu_record_id
            #         hu_dict["col_change_list"] = ["job_status"]
            #         hu_dict["data"] = old_hu
            #         log_list["hu"] = hu_dict
            #     from def_server import DefRecord
            #     def_obj = DefRecord()
            #     old_def = def_obj._get_by_parent_id(pg, hu_id)
            #     if old_def:
            #         old_def_dict = old_def[0]
            #         old_def_dict["job_status"] = "init"
            #         def_rc_id = old_def_dict.get("def_rc_id")
            #         definition_id = old_def_dict.get("definition_id")
            #         if old_def.update_col_change_list(pg, def_rc_id, old_def_dict, status_change_list):
            #             def_dict = dict()
            #             def_dict["table_name"] = def_obj.table_name
            #             def_dict["action"] = "change"
            #             def_dict["record_id"] = def_rc_id
            #             def_dict["col_change_list"] = ["job_status"]
            #             def_dict["data"] = old_def
            #             log_list["definition"] = def_dict
            #         from analysis_service import AnalysisRecord
            #         ana_obj = AnalysisRecord()
            #         old_analysis = ana_obj._get_by_parent_id(pg, definition_id)
            #         if old_analysis:
            #             old_analysis_dict = old_analysis[0]
            #             old_analysis_dict["job_status"] = "init"
            #             analysis_rc_id = old_analysis_dict.get("analysis_rc_id")
            #             if ana_obj.update_col_change_list(pg, analysis_rc_id, old_analysis_dict, status_change_list):
            #                 analysis_dict = dict()
            #                 analysis_dict["table_name"] = ana_obj.table_name
            #                 analysis_dict["action"] = "change"
            #                 analysis_dict["record_id"] = analysis_rc_id
            #                 analysis_dict["col_change_list"] = ["job_status"]
            #                 analysis_dict["data"] = old_analysis
            #                 log_list["definition"] = def_dict
        else:
            self.delete(arl_id)
        log_list = self.convert2log([diff_result])

        return log_list

    def get_by_arl_id(self, pg, arl_id, col_list):
        sqlcmd = self.list_2_select_sql("arl", col_list, ["arl_id"])
        pg.execute(sqlcmd, [arl_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
            arl_record_id = row[0]
            model_list = self.get_arl_model_list(pg, arl_record_id)
            attr_dict["model_list"] = model_list
        return attr_dict

    def get_arl_model_list(self, pg, arl_record_id):
        category_dict = {}
        model_list = []
        for model_id, model, val, order_no, arl_record_id in self._get_arl_model_list(pg, arl_record_id):
            model_dict = dict()
            model_dict["order_no"] = order_no
            model_dict["model_id"] = model_id
            model_dict["val"] = val
            model_dict["arl_record_id"] = arl_record_id
            model_list.append(model_dict)
        return model_list

    def _get_arl_model_list(self, pg, _id):
        sqlcmd = """
        SELECT a.model_id, model, a.val, a.order_no, a.arl_record_id
          FROM spec.arl_model_rel as a
          LEFT JOIN spec.arl_model_type as b
          ON a.model_id = b.model_id
          WHERE arl_record_id = %s
          ORDER BY a.model_id
        """
        pg.execute(sqlcmd, (_id,))
        rows = pg.fetchall()
        for row in rows:
            model_id, model, val, order_no, arl_record_id = row
            model = json.loads(model)
            yield model_id, model, val, order_no, arl_record_id

    def get_user_by_arl_id(self, arl_id):
        sqlcmd = """
        SELECT user_id FROM spec.arl WHERE arl_id = %s
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (arl_id,))
        row = self._pg.fetchone()
        return row

    def get_lock_message(self, pg=None):
        data = dict()
        if pg:
            temp_pg = pg
        else:
            temp_pg = self._pg
            temp_pg.connect()
        sqlcmd = """
            SELECT hu_id
            FROM (
                select hu_id
                from spec.hu
                where lock_status = 1
                union
                
                select hu_id
                from spec.basic_req_hu
                where lock_status = 1
            ) as t1
            ORDER BY length(hu_id), hu_id;
         """
        temp_pg.execute(sqlcmd)
        rows = temp_pg.fetchall()
        hu_list = []
        for row in rows:
            hu_list.append(row[0])
        sqlcmd2 = """
            SELECT definition_id
            FROM (
                select definition_id
                from spec.definition
                where lock_status = 1
                union
    
                select definition_id
                from spec.basic_req_definition
                where lock_status = 1
            ) as t1
            ORDER BY length(definition_id), definition_id;
            """
        temp_pg.execute(sqlcmd2)
        rows = temp_pg.fetchall()
        def_list = []
        for row in rows:
            def_list.append(row[0])
        sqlcmd3 = """
            SELECT definition_id
            FROM (
                select definition_id
                from spec.analysis
                where lock_status = 1
                union
                select definition_id
                from spec.basic_req_definition
                where lock_status = 1
            ) as t1
            ORDER BY length(definition_id), definition_id;
        """
        temp_pg.execute(sqlcmd3)
        rows = temp_pg.fetchall()
        ana_list = []
        for row in rows:
            ana_list.append(row[0])
        if not pg:
            temp_pg.close()
        data["hu_list"] = hu_list
        data["def_list"] = def_list
        data["ana_list"] = ana_list
        return data

    def get_req_content(self, type):
        self._pg.connect()
        data = []
        if type == "HU":
            sqlcmd = """
                SELECT distinct basic_req
                FROM spec.basic_req_hu where basic_req <> '' and  basic_req is not null
                union
                SELECT distinct basic_req
                FROM spec.hu where basic_req <> '' and  basic_req is not null
            """
        elif type == "DEF":
            sqlcmd = """
                select distinct t1.basic_req from(SELECT basic_req
                FROM spec.basic_req_hu
                union
                SELECT basic_req
                FROM spec.hu
                union
                SELECT basic_req
                FROM spec.definition
                union
                SELECT basic_req
                FROM spec.basic_req_definition
                )as t1 where t1.basic_req <> '' and t1.basic_req is not null
            """
        else:
            sqlcmd = """
                select distinct t1.basic_req from(SELECT basic_req
                FROM spec.basic_req_hu
                union
                SELECT basic_req
                FROM spec.hu
                union
                SELECT basic_req
                FROM spec.definition
                union
                SELECT basic_req
                FROM spec.basic_req_definition
                union
                SELECT basic_req
                FROM spec.basic_req_analysis
                union
                SELECT basic_req
                FROM spec.analysis
                )as t1 where t1.basic_req <> '' and t1.basic_req is not null
                        """
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        self._pg.close()
        req_list = []

        for row in rows:
            req_list.append(row[0])
        data = dict()
        data["req_list"] = req_list
        return data

    def get_check_content(self, type):
        self._pg.connect()
        type_data = dict()
        sqlcmd = """   
          SELECT check_item_id,  check_project, check_subject, check_methord
          FROM spec.check_list_item where check_type = %s
          ORDER BY check_item_id
        """
        self._pg.execute(sqlcmd, (type,))
        rows = self._pg.fetchall()
        self._pg.close()
        data = []
        for row in rows:
            chick_list = {}
            chick_list["id"] = row[0]
            chick_list["check_project"] = row[1]
            chick_list["check_subject"] = row[2]
            chick_list["check_methord"] = row[3]
            data.append(chick_list)
        type_data = dict()
        if type == 'hu':
            type_data["hu_check_list"] = data
        elif type == 'definition':
            type_data["definition_check_list"] = data
        elif type == 'analysis':
            type_data["analysis_check_list"] = data
        elif type == 'basic_req_hu':
            type_data["basic_req_hu_check_list"] = data
        elif type == 'basic_req_definition':
            type_data["basic_req_definition_check_list"] = data
        elif type == 'basic_req_analysis':
            type_data["basic_req_analysis_check_list"] = data

        return type_data


def main():
    # spec_obj = ArlSpec()
    # arl_id = '10.1.9.9.4.11'
    # data_list = spec_obj.get_by_id_deep(arl_id, user_id=0, group_id=0)
    # hu_list = data_list[0]["hu_list"]
    # import copy
    # hu_list.append(copy.deepcopy(hu_list[0]))
    # obj = ArlRecord()
    # import time
    # update_time = time.strftime("%Y-%m-%d %H:%M:%S")
    # result = obj.arl_full_content_post(data_list, update_time)
    spec_obj = ArlSpec()
    data = spec_obj.get_block_white_list()
    return 0
    # data = {"user_id": 0,
    #         "type": "tagl_ana",  # arl / hu / tagl_def / tagl_ana,
    #         "category_id": "1-35",
    #         "condition": {"definition_id": "2"}
    #         }
    # result = spec_obj.get_by_category(data)
    data = {
        "type": "arl",  # arl / hu / tagl_def / tagl_ana,
        "condition": {"user_id": 0, "group_id": 230,
                      # "complete": 'incomplete',  # complete: 已完成， incomplete：未完成，空：不设过滤条件
                      },
        # "like_condition": {'arl_id': '10'},
        "page": 1,
        "size": 100
    }
    result = spec_obj.summay_for_all(data)
    # result = spec_obj.summary_users(data)
    return result


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

