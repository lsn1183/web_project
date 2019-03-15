# -*- coding: UTF-8 -*-

class HmiItScreenMoveV001():
    def __init__(self):
        self.doc_type = 'HMI_IT_SCREEN_MOVE'
        self.version = '0.01'
        self.doc_format_dict = {
            'it_no': {
                'xlsname': '番号',
                'xlspos': [(2, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'category': {
                'xlsname': '処理種類',
                'xlspos': [(3, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_unit_id': {
                'xlsname': '遷移元画面ID',
                'xlspos': [(4, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_first_id': {
                'xlsname': '遷移先画面ID',
                'xlspos': [(5, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_id': {
                'xlsname': '遷移イベント',
                'xlspos': [(6, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_unit_api': {
                'xlsname': '遷移元Exit処理API',
                'xlspos': [(7, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_unit_content': {
                'xlsname': '遷移元Exit処理内容',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_first_api': {
                'xlsname': '遷移先Entry処理API',
                'xlspos': [(9, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'move_first_content': {
                'xlsname': '遷移先Entry処理内容',
                'xlspos': [(10, 5)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'uac_stc': {
                'xlsname': 'インターフェース(STCからコール)',
                'xlspos': [(11, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(12, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_uac': {
                'xlsname': 'インターフェース(UACからコール)',
                'xlspos': [(13, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(14, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_uac_callback': {
                'xlsname': 'UACコールバック呼び出し',
                'xlspos': [(15, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'rel_service': {
                'xlsname': '関連Service',
                'xlspos': [(16, 4)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'test_item': {
                'xlsname': 'テスト項目',
                'xlspos': [(17, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'remark': {
                'xlsname': '備考欄',
                'xlspos': [(18, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'obstacle_id': {
                'xlsname': '障害ID',
                'xlspos': [(19, 4)],
                'datatype': 'STR',
                'needcheck': False,
            },
        }

        self.xls_sheet_name = '画面遷移'
        self.start_data_row = 6
        self.id_col = "it_no"