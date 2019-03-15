# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.it_progress_qa import ItProgressQA
from Source.spec2db_server.docs.doc_xls import DocXls
from Source.spec2db_server.hmi.hmi_log import HmiLog
import re


class ItProgressImport(ItProgressQA):
    def __init__(self):
        ItProgressQA.__init__(self)

    def do_import(self, xls_file_name, commit_user_id, update_time):
        result = {"result": "NG", "error": ''}
        try:
            xls_list = DocXls('IT_PROCESS_QA', '0.01').load_data(xls_file_name)
        except Exception as e:
            result["error"] = str(e)
            return result
        self._pg.connect()
        commit_list = []
        try:
            for i, xls_data in enumerate(xls_list, 0):
                new_data_dict = {}
                update_cols = []
                for db_col, xls_data_dict in xls_data.iteritems():
                    update_cols.append(db_col)
                    xls_value = xls_data_dict.get('datavalue')
                    # delete unicode _x000D_
                    if xls_value and type(xls_value) in (str, unicode):
                        xls_value = xls_value.replace('_x000D_', '\n')
                    new_data_dict[db_col] = xls_value
                subject = new_data_dict.get('subject')
                req_id, jira_id_list = self.get_req_id(subject)  # 正则解要件id, jira_id
                if '.' not in req_id:
                    req_id = ''
                if not jira_id_list:
                    jira_id = ''
                else:
                    jira_id = '\n'.join(jira_id_list)
                new_data_dict['req_id'] = req_id
                new_data_dict['jira_id'] = jira_id
                update_cols.append('req_id')
                update_cols.append('jira_id')
                curr_commit_list = self._common_add(self._pg, new_data_dict, update_time, update_cols)
                if curr_commit_list:
                    commit_list += curr_commit_list
            # self._pg.commit()
            # if commit_list:
            #     log_info = {'user_id': commit_user_id, "commit_list": commit_list}
            #     commit_log = HmiLog()
            #     log_commit_data = commit_list[0].get("data")
            #     log_commit_data["update_time"] = update_time
            #     flag, commit_id = commit_log.add_commit_log2(self._pg, log_info)
            #     if flag:
            #         self._pg.commit()
            #         result["result"] = "OK"
            # else:
            #     result["result"] = "OK"
            self._pg.commit()
            result["result"] = "OK"

        except Exception as e:
            print e
            self._pg.conn.rollback()
            result["error"] = "%s%s" % (new_data_dict.get('qa_id'), str(e))
        finally:
            self._pg.close()
            return result


if __name__ == '__main__':
    import sys
    import time
    import os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    ItProgressImport().do_import(r'C:\Users\yuyin\Desktop\ITQA.xlsx', 341,
                                 time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))