from app.export_doc.export_17cy_drbfm import Export17cyDrbfm
from .export_basic_doc import ExportBasicDoc
from .export_detail_doc import ExportDetailDoc


class ExportFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def create(project='17Cy', doc_type='BASIC'):
        if project == '17Cy':
            if doc_type == 'BASIC':
                return ExportBasicDoc()
            else:
                return ExportDetailDoc()
        else:
            if doc_type == 'BASIC':
                return ExportBasicDoc()
            else:
                return ExportDetailDoc()


class ExportDrbfmFactory(object):
    def __init__(self):
        pass

    @staticmethod
    def create(project='17Cy'):
        if project == '17Cy':
            return Export17cyDrbfm()

        else:
            return Export17cyDrbfm()


