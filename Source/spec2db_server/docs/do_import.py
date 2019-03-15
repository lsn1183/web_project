# -*- coding: UTF-8 -*-
from base import DocBase
from openpyxl import load_workbook
from xls_util import XlsUtil

class DoImport(DocBase):
    def __init__(self):
        DocBase.__init__(self)

    def each_sheet_name(self, xls_filename):
        xls_wb = load_workbook(xls_filename)
        sheetNames = xls_wb.get_sheet_names()
        return sheetNames