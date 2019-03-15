# -*- coding: UTF-8 -*-
from import_base import ImportBase
from Source.spec2db_server.arl.pointout_server import PointOut
from Source.spec2db_server.arl.hu_server import HuRecord
from Source.spec2db_server.arl.def_server import DefRecord
from Source.spec2db_server.arl.analysis_service import AnalysisRecord
from Source.spec2db_server.arl.basic_hu import BasicHuRecord
from Source.spec2db_server.arl.basic_def import BasicDefRecord
from Source.spec2db_server.arl.basic_ana import BasicAnaRecord
import re
class SpecPointout(ImportBase):
    def __init__(self):
        ImportBase.__init__(self)
        self.file_name = ''
        self._point_col_list = []
        self._from = []
        self.covert_dict = {}
        self._point_col_list = ["review_result", "pointout_no", "pointout_status", "pointout_comment",
                                "reader_check", "reader2_check", "final_check", "pointout_charger",
                                "pointout_priority", "pointout_date", "suntec_status", "fixed", "suntec_remark",
                                "arl_rel", "suntec_cannot_modify"
                                ]

    def set_file(self, file_name):
        self.file_name = file_name

    def store(self, point_data_list, new_date):
        import_record = dict()
        self._pg.connect()
        for point_data in point_data_list:
            new_data = self.convert_data(point_data)
            new_data["new_date"] = new_date
            new_data.pop("model_list")
            point_obj = PointOut()
            try:
                point_obj.delete_all(new_date)
                point_obj.add_point_out(self._pg, new_data)

            except Exception as e:
                import_record['result'] = 1
                import_record["error_list"] = e.message
                return import_record
        import_record['result'] = "OK"
        self._pg.commit()
        self._pg.close()
        return import_record

    def point_store(self, data_list, update_time, classify):
        if classify == "HU_DEF":
            record_obj = HuRecord()
            classify = 'hu'
        elif classify == "TAGL_DEF":
            record_obj = DefRecord()
            classify = 'definition'
        elif classify == "TAGL_ANA":
            record_obj = AnalysisRecord()
            classify = 'analysis'
        self._pg.connect()
        # import_record = dict()
        for _data in data_list:
            point_dict = self.get_point_data(_data)
            if point_dict:
                point_dict["classify"] = classify
                point_dict["update_time"] = update_time
                id = point_dict.get("id")
                if re.match("^[B|C|D].*", id):
                    if classify == "hu":
                        record_obj = BasicHuRecord()
                    elif classify == "definition":
                        record_obj = BasicDefRecord()
                    elif classify == "analysis":
                        record_obj = BasicAnaRecord()
                old_data = record_obj.get_by_id_for_diff(self._pg, id, record_obj.attr_list)
                record_id = old_data.get(record_obj.key_col)
                point_dict["record_id"] = record_id
                from Source.spec2db_server.arl.point_out import PointOut
                point_obj = PointOut(classify)
                point_obj.add_point_out(self._pg, point_dict)
        self._pg.commit()
        self._pg.close()

    def get_point_data(self, data_list):
        point_dict = dict()
        for key in data_list:
            datavalue = data_list[key].get("datavalue")
            if key in self._point_col_list:
                point_dict[key] = datavalue
            if key in ("hu_id", "definition_id", "analysis_id"):
                point_dict["id"] = datavalue
        for key in self._point_col_list:
            if point_dict[key]:
                return point_dict
        return None







