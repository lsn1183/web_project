# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_it_screen_move import HmiItScreenMove
from Source.spec2db_server.docs.doc_xls import DocXls
from Source.spec2db_server.hmi.hmi_log import HmiLog


class HmiItScreenMoveImport(HmiItScreenMove):
    def __init__(self):
        HmiItScreenMove.__init__(self)

    def do_import(self, pg, file_name, xls_file_name, commit_user_id, update_time):
        result = {"result": "NG", "error": ''}
        try:
            xls_list = DocXls('HMI_IT_SCREEN_MOVE', '0.01').load_data(xls_file_name)
        except Exception as e:
            result["error"] = str(e)
            return result
        commit_list = []
        try:
            for i, xls_data in enumerate(xls_list, 0):
                print i
                if not xls_data['it_no']['datavalue']:
                    continue
                new_data_dict = {}
                update_cols = []
                for db_col, xls_data_dict in xls_data.iteritems():
                    update_cols.append(db_col)
                    xls_value = xls_data_dict.get('datavalue')
                    # delete unicode _x000D_
                    if xls_value and type(xls_value) in (str, unicode):
                        xls_value = xls_value.replace('_x000D_', '\n')
                    new_data_dict[db_col] = xls_value
                new_data_dict['file_name'] = file_name
                new_data_dict['it_key'] = ', '.join([file_name, new_data_dict['it_no']])
                curr_commit_list = self._common_add(pg, new_data_dict, update_time, update_cols)
                if curr_commit_list:
                    commit_list += curr_commit_list
            if commit_list:
                log_info = {'user_id': commit_user_id, "commit_list": commit_list}
                commit_log = HmiLog()
                log_commit_data = commit_list[0].get("data")
                log_commit_data["update_time"] = update_time
                flag, commit_id = commit_log.add_commit_log2(pg, log_info)
                if flag:
                    result["result"] = "OK"
            else:
                result["result"] = "OK"
        except Exception as e:
            print str(e)
            pg.conn.rollback()
            result["error"] = "%s%s" % (new_data_dict.get('it_no'), str(e))
        finally:
            return result


if __name__ == '__main__':
    import sys
    import time
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    HmiItScreenMoveImport().do_import(r'/mnt/sharedoc/HMI_ScreenImport_v001.xlsx', 341,
                          time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))