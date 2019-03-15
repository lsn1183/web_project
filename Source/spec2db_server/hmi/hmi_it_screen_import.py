# -*- coding: UTF-8 -*-

from Source.spec2db_server.hmi.hmi_base import HMIBase
from Source.spec2db_server.hmi.hmi_log import HmiLog
from Source.spec2db_server.docs.do_import import DoImport
from Source.spec2db_server.hmi.hmi_it_result_mode_transition_import import HimItResultModeTransitionImport
from Source.spec2db_server.hmi.hmi_it_screen_move_import import HmiItScreenMoveImport
from Source.spec2db_server.hmi.hmi_notify_import import HmiNotifyImport
from Source.spec2db_server.hmi.hmi_interior_import import HmiInteriorImport
from Source.spec2db_server.hmi.it_result_init_end_import import ItResultInitEndImport


class HmiItScreenImport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def do_imports(self, file_name, file_path, user_id, time):
        result = {"result": "NG", "error": ''}
        obj = DoImport()
        sheet_name_list = obj.each_sheet_name(file_path)
        self._pg.connect()
        if u"モード遷移"in sheet_name_list:
            obj1 = HimItResultModeTransitionImport()
            ret_data1 = obj1.do_import(self._pg, file_name, file_path, user_id, time)
            if ret_data1.get("result") != "OK":
                result["error"] = "モード遷移:" + ret_data1.get("error")
                self._pg.close()
                return result
        if u"画面遷移"in sheet_name_list:
            obj2 = HmiItScreenMoveImport()
            ret_data2 = obj2.do_import(self._pg, file_name, file_path, user_id, time)
            if ret_data2.get("result") != "OK":
                result["error"] = "画面遷移:" + ret_data2.get("error")
                self._pg.close()
                return result
        if u"Notify"in sheet_name_list:
            obj3 = HmiNotifyImport()
            ret_data3 = obj3.do_import(self._pg, file_name, file_path, user_id, time)
            if ret_data3.get("result") != "OK":
                result["error"] = "Notify:" + ret_data3.get("error")
                self._pg.close()
                return result
        if u"内部遷移"in sheet_name_list:
            obj4 = HmiInteriorImport()
            ret_data4 = obj4.do_import(self._pg, file_name, file_path, user_id, time)
            if ret_data4.get("result") != "OK":
                result["error"] = "内部遷移:" + ret_data4.get("error")
                self._pg.close()
                return result
        if u"アプリ初期化・終了処理"in sheet_name_list:
            obj5 = ItResultInitEndImport()
            ret_data5 = obj5.do_import(self._pg, file_name, file_path, user_id, time)
            if ret_data5.get("result") != "OK":
                result["error"] = "アプリ初期化・終了処理:" + ret_data5.get("error")
                self._pg.close()
                return result
        self._pg.commit()
        result["result"] = "OK"
        self._pg.close()
        return result


if __name__ == '__main__':
    import sys
    import time
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    obj = HmiItScreenImport()
    obj.do_imports('TAGL_r.xlsx', r'C:\SpiderInput\20180330\TAGL_d.xlsx', 341, obj.get_current_time())
