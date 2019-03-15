# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_it_progress_report import HmiItProgressReport
from Source.spec2db_server.docs.doc_xls import DocXls
from Source.spec2db_server.hmi.hmi_log import HmiLog


class HmiItProgressReportImport(HmiItProgressReport):
    def __init__(self):
        HmiItProgressReport.__init__(self)
        self.dev_status_dict = {}
        self.dev_status_dict2 = {}
        self._pg.connect()
        self._pg.execute('select process_status, process_status_id from hmi.it_process_status')
        for db_data in self._pg.fetchall():
            self.dev_status_dict[db_data[0]] = db_data[1]
        self._pg.execute('select dev_status, dev_status_id from hmi.it_dev_status')
        for db_data in self._pg.fetchall():
            self.dev_status_dict2[db_data[0]] = db_data[1]
        # self._pg.close()

    def do_import(self, xls_file_name, update_cols, commit_user_id, update_time):
        result = {"result": "NG", "error": ''}
        try:
            xls_list = DocXls('HMI_IT_PROGRESS_REPORT', '0.02').load_data(xls_file_name)
        except Exception as e:
            result["error"] = str(e)
            return result
        commit_list = []
        try:
            for i, xls_data in enumerate(xls_list, 0):
                print i
                # if not xls_data['it_no']['datavalue']:
                #     continue
                new_data_dict = {}
                for db_col, xls_data_dict in xls_data.iteritems():
                    xls_value = xls_data_dict.get('datavalue')
                    # delete unicode _x000D_
                    if xls_value and type(xls_value) in (str, unicode):
                        xls_value = xls_value.replace('_x000D_', '\n')
                    new_data_dict[db_col] = xls_value
                    if db_col in ('dev_fw16_status', 'dev_model_status', 'dev_ut_status', 'dev_it_status', 'dev_itn_status',):
                        xls_value = self.dev_status_dict[xls_value] if xls_value in self.dev_status_dict else None
                    new_data_dict[db_col] = xls_value
                    if db_col in ('dev_status', 'ut_status1', 'ut_status2', 'ut_status3', 'ut_status4',
                                  'ut_status5', 'ut_status6', 'ut_status7', 'ut_status8', 'ut_status9', 'ut_status10',):
                        xls_value = self.dev_status_dict2[xls_value] if xls_value in self.dev_status_dict2 else None
                    new_data_dict[db_col] = xls_value
                # new_data_dict['file_name'] = file_name
                # new_data_dict['it_key'] = ', '.join([file_name, new_data_dict['req_id']])
                curr_commit_list = self._common_add(self._pg, new_data_dict, update_time, update_cols)
                if curr_commit_list:
                    commit_list += curr_commit_list
            # if commit_list:
            #     log_info = {'user_id': commit_user_id, "commit_list": commit_list}
            #     commit_log = HmiLog()
            #     log_commit_data = commit_list[0].get("data")
            #     log_commit_data["update_time"] = update_time
            #     flag, commit_id = commit_log.add_commit_log2(pg, log_info)
            #     if flag:
            #         result["result"] = "OK"
            # else:
            self._pg.commit()
            result["result"] = "OK"

        except Exception as e:
            print str(e)
            self._pg.conn.rollback()
            result["error"] = "%s%s" % (new_data_dict.get('req_id'), str(e))
        finally:
            return result


if __name__ == '__main__':
    import sys
    import time
    import os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    HmiItProgressReportImport().do_import(r'C:\Users\yuyin\Desktop\IT_Progress_Report_20180328201140.xlsx', ['gl'], 341,
                          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))