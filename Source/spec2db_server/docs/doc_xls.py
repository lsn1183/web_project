# -*- coding: UTF-8 -*-
from base import DocBase
from openpyxl import load_workbook
from xls_util import XlsUtil
from hu_v017 import HuV017
from def_v012 import DefV012
from point_v001 import PointV001
from ana_v100 import AnalV100
from hmi_req_v001 import HMIReqV001
from hmi_req_v002 import HMIReqV002
from hmi_req_v003 import HMIReqV003
from hmi_req_v004 import HMIReqV004
from hmi_req_v005 import HMIReqV005
from hmi_internalQA_v001 import InternalQAV001
from hmi_externalQA_v001 import ExternalQAV001
from hmi_externalQA_v002 import ExternalQAV002
from hmi_externalBug_v002 import ExternalBug002
from hmi_screen_v001 import HmiScreenV001
from hmi_screen_it_v001 import HmiScreenItV001
from hmi_it_result_mode_transition_v001 import HimItResultModeTransitionV001
from it_result_init_end_v001 import ItResultInItEndV001
from hmi_it_screen_move_v001 import HmiItScreenMoveV001
from hmi_notify_v001 import HmiNotifV001
from hmi_interior_v001 import HmiIntertiorV001
from it_progress_report import ItProgressReport
from it_process_QA_v001 import ItProcessQaV001
from it_progress_report_v002 import ItProgressReportV002


class DocXls(DocBase):

    def __init__(self, doc_type, doc_ver):
        # super.__init__()
        self.doc_instance = None
        if doc_type == 'HU_DEF':
            if doc_ver == '0.40':
                self.doc_instance = HuV017()
        elif doc_type == 'TAGL_DEF':
            if doc_ver == '0.40':
                self.doc_instance = DefV012()
        elif doc_type == 'TAGL_ANA':
            if doc_ver == '0.40':
                self.doc_instance = AnalV100()
        elif doc_type == 'POINT_OUT':
            if doc_ver == '0.40':
                self.doc_instance = PointV001()
        elif doc_type == 'HMI_REQ':
            if doc_ver == '0.01':
                self.doc_instance = HMIReqV001()
            elif doc_ver == '0.02':
                self.doc_instance = HMIReqV002()
            elif doc_ver == '0.03':
                self.doc_instance = HMIReqV003()
            elif doc_ver == '0.04':
                self.doc_instance = HMIReqV004()
            elif doc_ver == '0.05':
                self.doc_instance = HMIReqV005()
        elif doc_type == 'HMI_INTERNALQA':
            if doc_ver == '0.01':
                self.doc_instance = InternalQAV001()
        elif doc_type == 'HMI_EXTERNALQA':
            if doc_ver == '0.01':
                self.doc_instance = ExternalQAV001()
            elif doc_ver == '0.02':
                self.doc_instance = ExternalQAV002()
        elif doc_type == 'HMI_EXTERNALBUG':
            if doc_ver == '0.02':
                self.doc_instance = ExternalBug002()
        elif doc_type == 'HMI_SCREEN':
            if doc_ver == '0.01':
                self.doc_instance = HmiScreenV001()
        elif doc_type == 'HMI_SCREEN_IT':
            if doc_ver == '0.01':
                self.doc_instance = HmiScreenItV001()
        elif doc_type == 'It_Result_InIt_End':
            if doc_ver == '0.01':
                self.doc_instance = ItResultInItEndV001()
        elif doc_type == 'HMI_IT_RESULT_MODE_TRANSITION':
            if doc_ver == '0.01':
                self.doc_instance = HimItResultModeTransitionV001()
        elif doc_type == 'HMI_IT_SCREEN_MOVE':
            if doc_ver == '0.01':
                self.doc_instance = HmiItScreenMoveV001()
        elif doc_type == 'HMI_NOTIFY':
            if doc_ver == '0.01':
                self.doc_instance = HmiNotifV001()
        elif doc_type == 'HMI_INTERIOR':
            if doc_ver == '0.01':
                self.doc_instance = HmiIntertiorV001()
        elif doc_type == 'HMI_IT_PROGRESS_REPORT':
            if doc_ver == '0.01':
                self.doc_instance = ItProgressReport()
            elif doc_ver == '0.02':
                self.doc_instance = ItProgressReportV002()
        elif doc_type == 'IT_PROCESS_QA':
            if doc_ver == '0.01':
                self.doc_instance = ItProcessQaV001()

    def load_data(self, xls_filename):
        # try:
        xls_wb = load_workbook(xls_filename)
        xls_sheet = xls_wb.get_sheet_by_name(self.doc_instance.xls_sheet_name.decode('utf8'))
            # except Exception:
            # raise Exception('file is error')
        xls_obj = XlsUtil(self.doc_instance.id_col)
        if not xls_obj.check_format(xls_sheet, self.doc_instance.doc_format_dict):
            raise Exception('file can not match the template')

        data_list = xls_obj.get_xls_data(xls_sheet, self.doc_instance.doc_format_dict,
                                         self.doc_instance.start_data_row)

        return data_list

    def get_doc_format_dict(self):
        if self.doc_instance is None:
            raise Exception('paramer is error')

        return self.doc_instance.doc_format_dict

    def get_doc_type(self):
        if self.doc_instance is None:
            raise Exception('paramer is error')

        return self.doc_instance.doc_type

    def get_doc_ver(self):
        if self.doc_instance is None:
            raise Exception('paramer is error')

        return self.doc_instance.version

if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    aaa = DocXls('HMI_REQ','0.01').load_data('/mnt/sharedoc/hmi/detailtemplate.xlsx')
    print len(aaa)

