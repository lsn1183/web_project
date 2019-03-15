# -*- coding: UTF-8 -*-
from app.export_doc.export_doc_base import ExportDocBase


class ExportBasicDoc(ExportDocBase):
    """基本设计
    """
    def __init__(self, doc_id=None, doc_type='BASIC', export_format=".xlsx"):
        ExportDocBase.__init__(self, doc_id, doc_type, export_format)
