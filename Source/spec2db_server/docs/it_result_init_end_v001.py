# -*- coding: UTF-8 -*-

class ItResultInItEndV001():
    def __init__(self):
        self.doc_type = 'It_Result_InIt_End'
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
            'inteface': {
                'xlsname': 'インタフェース(APFWからコール)',
                'xlspos': [(4, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'if_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(5, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'mc_process_content': {
                'xlsname': 'MC処理内容',
                'xlspos': [(6, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_interface': {
                'xlsname': 'インターフェース(MC/STCからコール)',
                'xlspos': [(7, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'uac_nofity_no': {
                'xlsname': '関連Nofity番号',
                'xlspos': [(9, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_inteface': {
                'xlsname': 'インターフェース(UACからコール)',
                'xlspos': [(10, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_process_content': {
                'xlsname': 'インターフェース処理内容',
                'xlspos': [(11, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_nofity_no': {
                'xlsname': '関連Nofity番号',
                'xlspos': [(12, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sb_uac_callback': {
                'xlsname': 'UACコールバック呼び出し',
                'xlspos': [(13, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'rel_service': {
                'xlsname': '関連Service',
                'xlspos': [(14, 5)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'test_item': {
                'xlsname': 'D/G/J列に記載している関数名のLOGがターミナルで順番に出力されることを確認する',
                'xlspos': [(15, 5)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'remark': {
                'xlsname': '備考欄',
                'xlspos': [(16, 5)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'obstacle_id': {
                'xlsname': '障害ID',
                'xlspos': [(17, 5)],
                'datatype': 'STR',
                'needcheck': False,
            },
        }

        self.xls_sheet_name = 'アプリ初期化・終了処理'
        self.start_data_row = 6
        self.id_col = "it_no"