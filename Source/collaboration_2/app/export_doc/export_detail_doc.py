# -*- coding: UTF-8 -*-
from app.export_doc.export_doc_base import ExportDocBase


class ExportDetailDoc(ExportDocBase):
    """详细设计
    """
    def __init__(self, doc_id=None, doc_type='DETAIL', export_format=".xlsx"):
        ExportDocBase.__init__(self, doc_id, doc_type, export_format)
