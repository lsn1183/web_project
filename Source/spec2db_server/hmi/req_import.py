# -*- coding: UTF-8 -*-
from Source.spec2db_server.hmi.hmi_req import HmiReq
from Source.spec2db_server.docs.doc_xls import DocXls
from Source.spec2db_server.hmi.hmi_log import HmiLog


class ReqImport(HmiReq):
    def __init__(self):
        HmiReq.__init__(self)
        self.dev_status_dict = {}
        self._pg.connect()
        self._pg.execute('select status, dev_status_id from hmi.dev_status')
        for db_data in self._pg.fetchall():
            self.dev_status_dict[db_data[0]] = db_data[1]
        self._pg.close()

    def do_import(self, xls_file_name, update_cols, commit_user_id, update_time):
        result = {"result": "NG", "error": ''}
        try:
            xls_list = DocXls('HMI_REQ', '0.05').load_data(xls_file_name)
        except Exception as e:
            result["error"] = str(e)
            return result
        self._pg.connect()
        commit_list = []
        try:
            for i, xls_data in enumerate(xls_list, 0):
                print i
                new_data_dict = {}
                for db_col, xls_data_dict in xls_data.iteritems():
                    xls_value = xls_data_dict.get('datavalue')
                    # delete unicode _x000D_
                    if xls_value and type(xls_value) in (str, unicode):
                        xls_value = xls_value.replace('_x000D_', '\n')
                    if db_col in ('apl_progress', 'ng_num', ):
                        try:
                            xls_value = str(int(xls_value))
                        except:
                            xls_value = None
                    if db_col in ('dev_status',):
                        xls_value = self.dev_status_dict[xls_value] if xls_value in self.dev_status_dict else None
                    new_data_dict[db_col] = xls_value
                # ## 去掉空白和\n
                val = new_data_dict.get("it_file_name")
                if val:
                    new_data_dict["it_file_name"] = val.strip()
                # ## APL设计书番号: APL设计书名称有，APL设计书番号无，那么 APL设计书番号 = 结合测试书番号.
                if new_data_dict.get("apl_test_files"):  # APL设计书名称
                    if not new_data_dict.get("apl_test_nos"):
                        new_data_dict["apl_test_nos"] = new_data_dict.get("it_nos")  # 结合测试书番号
                curr_commit_list = self._common_add(self._pg, new_data_dict, update_time, update_cols)
                if curr_commit_list:
                    commit_list += curr_commit_list
            if commit_list:
                log_info = {'user_id': commit_user_id, "commit_list": commit_list}
                commit_log = HmiLog()
                log_commit_data = commit_list[0].get("data")
                log_commit_data["update_time"] = update_time
                flag, commit_id = commit_log.add_commit_log2(self._pg, log_info)
                if flag:
                    self._pg.commit()
                    result["result"] = "OK"
            else:
                # self._pg.commit()
                result["result"] = "OK"
        except Exception as e:
            print e
            self._pg.conn.rollback()
            result["error"] = "%s %s" % (new_data_dict.get('hu_id'), str(e))
        finally:
            self._pg.close()
            return result


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    obj = ReqImport()
    obj.do_import(r'C:\SpiderInput\20180312\HMI_Detail_template_v004_02.xlsx', [], 341,
                  obj.get_current_time())
