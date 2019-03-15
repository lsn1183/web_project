# -*- coding: UTF-8 -*-

class HMIReqV001():
    def __init__(self):
        self.doc_type = 'HMIREQ'
        self.version = '0.01'
        self.doc_format_dict = {
            'represent_req': {
                'xlsname': 'H/U要件定義書から転記->NEDL代表要件',
                'xlspos': [(1, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'arl_id': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->ARLID',
                'xlspos': [(2, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'big_category': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->大分類',
                'xlspos': [(3, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'mid_category': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->中分類',
                'xlspos': [(4, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'small_category': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->小分類',
                'xlspos': [(5, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_category': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->詳細',
                'xlspos': [(6, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_basicreq': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->基本要件',
                'xlspos': [(7, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_req': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->要件',
                'xlspos': [(8, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_status': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->状態',
                'xlspos': [(9, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_trigger': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->トリガ',
                'xlspos': [(10, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_action': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->動作',
                'xlspos': [(11, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_remark': {
                'xlsname': 'H/U要件定義書から転記->ARLから転記->備考',
                'xlspos': [(12, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmino': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->仕様書番号',
                'xlspos': [(13, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmiversion': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->バージョン',
                'xlspos': [(14, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmifile': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->ファイル名',
                'xlspos': [(15, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmichapter': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->章',
                'xlspos': [(16, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmipage': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->Page',
                'xlspos': [(17, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_hmiscr': {
                'xlsname': 'H/U要件定義書から転記->HMI仕様書->画面ID',
                'xlspos': [(18, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_funcno': {
                'xlsname': 'H/U要件定義書から転記->機能仕様書->仕様書番号',
                'xlspos': [(19, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_funcversion': {
                'xlsname': 'H/U要件定義書から転記->機能仕様書->バージョン',
                'xlspos': [(20, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_funcfile': {
                'xlsname': 'H/U要件定義書から転記->機能仕様書->ファイル名',
                'xlspos': [(21, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_funcchapter': {
                'xlsname': 'H/U要件定義書から転記->機能仕様書->章',
                'xlspos': [(22, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_arl_funcpage': {
                'xlsname': 'H/U要件定義書から転記->機能仕様書->Page',
                'xlspos': [(23, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_id': {
                'xlsname': 'H/U要件定義書から転記->H/U要件定義ID',
                'xlspos': [(24, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_unique_id': {
                'xlsname': 'H/U要件定義書から転記->ユニークID',
                'xlspos': [(25, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_amp': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->AMP',
                'xlspos': [(26, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_dsrc': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->DSRC',
                'xlspos': [(27, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_dcm': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->DCM',
                'xlspos': [(28, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_rse': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->RSE',
                'xlspos': [(29, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_touchpad': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->TouchPad',
                'xlspos': [(30, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_opt_sepdisp': {
                'xlsname': 'H/U要件定義書から転記->オプション項目->SeparateDisp',
                'xlspos': [(31, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_system_conf': {
                'xlsname': 'H/U要件定義書から転記->システム構成',
                'xlspos': [(32, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_rel_req': {
                'xlsname': 'H/U要件定義書から転記->関連基本要件',
                'xlspos': [(33, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_exception': {
                'xlsname': 'H/U要件定義書から転記->除外',
                'xlspos': [(34, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_dcu_status': {
                'xlsname': 'H/U要件定義書から転記->H/U->DCU->状態',
                'xlspos': [(35, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_dcu_trigger': {
                'xlsname': 'H/U要件定義書から転記->H/U->DCU->トリガー',
                'xlspos': [(36, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_dcu_action': {
                'xlsname': 'H/U要件定義書から転記->H/U->DCU->動作',
                'xlspos': [(37, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_meu_status': {
                'xlsname': 'H/U要件定義書から転記->H/U->MEU->状態',
                'xlspos': [(38, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_meu_trigger': {
                'xlsname': 'H/U要件定義書から転記->H/U->MEU->トリガー',
                'xlspos': [(39, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_meu_action': {
                'xlsname': 'H/U要件定義書から転記->H/U->MEU->動作',
                'xlspos': [(40, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'hu_cat_id': {
                'xlsname': 'H/U要件定義書から転記->H/U分類ID',
                'xlspos': [(41, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_action_flow': {
                'xlsname': '設計内容紐付け->処理フロー',
                'xlspos': [(42, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_hmi_scrID': {
                'xlsname': '設計内容紐付け->HMI設計->画面ID',
                'xlspos': [(43, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_hmi_device_no': {
                'xlsname': '設計内容紐付け->HMI設計->部品番号',
                'xlspos': [(44, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_hmi_remark': {
                'xlsname': '設計内容紐付け->HMI設計->備考',
                'xlspos': [(45, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_IFNo': {
                'xlsname': '設計内容紐付け->アプリ設計->I/F番号',
                'xlspos': [(46, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_seviceIF': {
                'xlsname': '設計内容紐付け->アプリ設計->Service I/F',
                'xlspos': [(47, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_except_obj': {
                'xlsname': '設計内容紐付け->アプリ設計->除外対象',
                'xlspos': [(48, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_obj': {
                'xlsname': '設計内容紐付け->アプリ設計->対象アプリ',
                'xlspos': [(49, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_devstep': {
                'xlsname': '設計内容紐付け->アプリ設計->開発Step',
                'xlspos': [(50, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_app_remark': {
                'xlsname': '設計内容紐付け->アプリ設計->備考',
                'xlspos': [(51, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_system_file': {
                'xlsname': '設計内容紐付け->システム設計書名',
                'xlspos': [(52, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_decompose_id': {
                'xlsname': '設計内容紐付け->分解ID',
                'xlspos': [(53, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_decompose_content': {
                'xlsname': '設計内容紐付け->分解内容',
                'xlspos': [(54, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_operation': {
                'xlsname': '設計内容紐付け->操作',
                'xlspos': [(55, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_dest_name': {
                'xlsname': '設計内容紐付け->テスト\n項目',
                'xlspos': [(56, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_testcase_num': {
                'xlsname': '設計内容紐付け->テストケース件数',
                'xlspos': [(57, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'design_sys_remark': {
                'xlsname': '設計内容紐付け->備考',
                'xlspos': [(58, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'apl_status': {
                'xlsname': 'アプリ作成状態',
                'xlspos': [(59, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sys_test_status': {
                'xlsname': 'システムテスト作成状態',
                'xlspos': [(60, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sp29': {
                'xlsname': 'SP29',
                'xlspos': [(62, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sp30': {
                'xlsname': 'SP30',
                'xlspos': [(63, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'sp31': {
                'xlsname': 'SP31',
                'xlspos': [(64, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'iauto_complete': {
                'xlsname': 'iAuto担当（SP29）',
                'xlspos': [(65, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_step': {
                'xlsname': 'Step',
                'xlspos': [(66, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_def_id': {
                'xlsname': 'tagl要件定義ID',
                'xlspos': [(67, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_unique_id': {
                'xlsname': 'uniqueID',
                'xlspos': [(68, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_seq_file': {
                'xlsname': '時序図文件',
                'xlspos': [(69, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_seq_no': {
                'xlsname': '時序図番号',
                'xlspos': [(70, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_application': {
                'xlsname': 'Application',
                'xlspos': [(71, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_except': {
                'xlsname': 'TAGL除外',
                'xlspos': [(72, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_screenID': {
                'xlsname': 'ScreenID',
                'xlspos': [(73, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_is_represent_req': {
                'xlsname': '是否代表要件',
                'xlspos': [(74, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_parent_rep_req': {
                'xlsname': '親代表要件',
                'xlspos': [(75, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_new_date': {
                'xlsname': '新建日期',
                'xlspos': [(76, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ana_is_dalian': {
                'xlsname': 'APL是否为大连对应',
                'xlspos': [(77, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_charger': {
                'xlsname': '负责人',
                'xlspos': [(78, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_author': {
                'xlsname': '担当',
                'xlspos': [(79, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_apl_schedule': {
                'xlsname': 'APL日程',
                'xlspos': [(80, 5)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'detail_it_schedule': {
                'xlsname': '结合日程',
                'xlspos': [(81, 5)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'detail_apl_progress': {
                'xlsname': 'APL进度',
                'xlspos': [(82, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_it_progress': {
                'xlsname': '结合测试结果',
                'xlspos': [(83, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_it_release_ver': {
                'xlsname': '结合测试Release版本',
                'xlspos': [(84, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_dev_status': {
                'xlsname': '开发状态',
                'xlspos': [(85, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_dev_remark': {
                'xlsname': '备考',
                'xlspos': [(86, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_external_qa': {
                'xlsname': '外部QA番号',
                'xlspos': [(87, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_internal_qa': {
                'xlsname': '内部QA番号',
                'xlspos': [(88, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'detail_ng_num': {
                'xlsname': 'NG次数',
                'xlspos': [(89, 5)],
                'datatype': 'STR',
                'needcheck': True,
            },
        }
        self.xls_sheet_name = '要件详细'
        self.start_data_row = 6
        self.id_col = "hu_id"