# -*- coding: UTF-8 -*-
"""
Created on 2017-8-23

@author: hcz
"""
import os
import re
from openpyxl import load_workbook
import datetime
from ..spec_import.import_base import ImportBase

PROJ_NAME = 'proj_name'
SPEC_NAME = 'spec_name'
SPEC_VERSION = 'version'
SPEC_FILE_NAME = 'file_name'
RECORD_START_ROW = 5  # 记录开始行号


class DefinitionTemplate(ImportBase):
    """
    """
    def __init__(self):
        ImportBase.__init__(self)

    def _import_model_list(self, start_col=16, ):
        pass


class DefModel(ImportBase):
    # __instance = None
    # @staticmethod
    # def instance():
    #     """create a instance"""
    #     if AnalysisModel.__instance is None:
    #         AnalysisModel.__instance = AnalysisModel()
    #     return AnalysisModel.__instance

    def __init__(self):
        ImportBase.__init__(self)
        self._attr_dict = dict()

    def get_model_id_dict(self, modelList):
        for model_dict in modelList:
            for model in model_dict.iterkeys():
                model_id = self._attr_dict.get(model)
                if not model_id:
                    model_id = self._get_model_id(model)
                    self._attr_dict[model] = model_id
        return self._attr_dict

    def get_model_id(self, model):
        model_id = self._attr_dict.get(model)
        if not model_id:
            model_id = self._get_model_id(model)
            self._attr_dict[model] = model_id
        return model_id

    def _get_model_id(self, model):
        sqlcmd = """
        SELECT model_id
          FROM spec.definition_model_type
          WHERE model = %s;
        """
        self._pg.connect()
        self._pg.execute(sqlcmd, (model,))
        row = self._pg.fetchone()
        if row and row[0]:
            return row[0]
        sqlcmd = """
        INSERT INTO spec.definition_model_type(model)
            VALUES (%s) RETURNING model_id;
        """
        self._pg.execute(sqlcmd, (model,))
        model_id = self.fetch_id()
        self._pg.commit()
        return model_id


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    def_obj = DefinitionTemplate()
    def_obj.set_file(r'C:\Users\pset\Desktop\TAGL_RequirementDefinitionVer0.10_template_20171106.xlsx')
    book = load_workbook(def_obj.xls_file_name, data_only=True)
    sheet = book.get_sheet_by_name(r'TAGL要件定義')
    def_obj.store(sheet, user_id = 6)
    # sqlcmd = "select hu_id from spec.hu"
    # hu_obj._pg.query_fromcur(sqlcmd)
    # row = hu_obj._pg.fetchone()
    # print row
