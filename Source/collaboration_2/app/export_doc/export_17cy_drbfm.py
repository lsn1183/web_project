from app.export_doc.export_drbfm_base import ExportDrbfmBase


class Export17cyDrbfm(ExportDrbfmBase):
    """17cy
    """
    def __init__(self, start_row=9, sheet_name='DRBFMSheet',
                 templet_file=r'./data/doc/Data_DRBFM帳票_模板.xlsx',
                 export_format=".xlsx"):
        ExportDrbfmBase.__init__(self, start_row, sheet_name, templet_file, export_format)