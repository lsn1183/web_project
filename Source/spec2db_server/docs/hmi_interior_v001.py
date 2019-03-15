# -*- coding: UTF-8 -*-

class HmiIntertiorV001():
    def __init__(self):
        self.doc_type = 'HMI_Interior'
        self.version = '0.01'
        self.doc_format_dict = {
            'it_no': {
                'xlsname': '番号',
                'xlspos': [(2, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'category': {
                'xlsname': '処理種類',
                'xlspos': [(3, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'screen_id': {
                'xlsname': '画面ID',
                'xlspos': [(4, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'classify': {
                'xlsname': '種別',
                'xlspos': [(5, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'component_id': {
                'xlsname': '部品ID',
                'xlspos': [(6, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'length': {
                'xlsname': 'イベント',
                'xlspos': [(7, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'stc_apfw': {
                'xlsname': '押下イベントの処理関数(APFWからコール)',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'stc_process_content': {
                'xlsname': '処理内容',
                'xlspos': [(9, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_stc': {
                'xlsname': 'インターフェース(STCからコール)',
                'xlspos': [(10, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(11, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_uac': {
                'xlsname': 'インターフェース(UACからコール)',
                'xlspos': [(12, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(13, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_uac_callback': {
                'xlsname': 'UACコールバック呼び出し',
                'xlspos': [(14, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'rel_service': {
                'xlsname': '関連Service',
                'xlspos': [(15, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'test_item': {
                'xlsname': 'テスト項目',
                'xlspos': [(16, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'remark': {
                'xlsname': '備考欄',
                'xlspos': [(17, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'obstacle_id': {
                'xlsname': '障害ID',
                'xlspos': [(18, 4)],
                'datatype': 'STR',
                'needcheck': False,
            }

        }

        self.xls_sheet_name = '内部遷移'
        self.start_data_row = 6
        self.id_col = "it_no"