# -*- coding: UTF-8 -*-


class ItProgressReportV002():
    def __init__(self):
        self.doc_type = 'HMI_IT_PROGRESS_REPORT'
        self.version = '0.02'
        self.doc_format_dict = {
            'step': {
                'xlsname': 'SP',
                'xlspos': [(1, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'remark': {
                'xlsname': '備考',
                'xlspos': [(2, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'it_group': {
                'xlsname': 'Group',
                'xlspos': [(3, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'gl': {
                'xlsname': 'GL',
                'xlspos': [(4, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'author': {
                'xlsname': '担当者',
                'xlspos': [(5, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'plan_date': {
                'xlsname': '完了予定日',
                'xlspos': [(6, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'progress_code': {
                'xlsname': 'code分析',
                'xlspos': [(7, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'progress_ut': {
                'xlsname': 'UT',
                'xlspos': [(8, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'progress_it': {
                'xlsname': 'IT',
                'xlspos': [(9, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'progress_risk': {
                'xlsname': 'Risk状況',
                'xlspos': [(10, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'comment': {
                'xlsname': '备注',
                'xlspos': [(11, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'cate_alias': {
                'xlsname': 'カテゴリ読み替え',
                'xlspos': [(12, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'represent_req': {
                'xlsname': '代表要件',
                'xlspos': [(13, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'req_id': {
                'xlsname': '要件ID',
                'xlspos': [(14, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'jira_id': {
                'xlsname': 'JIRA ID',
                'xlspos': [(15, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'qa_id': {
                'xlsname': 'QA ID',
                'xlspos': [(16, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'release_ver': {
                'xlsname': 'Release Ver',
                'xlspos': [(17, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'major_category': {
                'xlsname': '大分类',
                'xlspos': [(18, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'medium_category': {
                'xlsname': '中分類',
                'xlspos': [(19, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'small_category': {
                'xlsname': '小分类',
                'xlspos': [(20, 3)],
                'datatype': 'STR',
                'needcheck': False,
            },
            'major': {
                'xlsname': '大分类',
                'xlspos': [(21, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'small': {
                'xlsname': '小分类',
                'xlspos': [(22, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'status': {
                'xlsname': '状態',
                'xlspos': [(23, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trigger': {
                'xlsname': 'トリガー',
                'xlspos': [(24, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'action': {
                'xlsname': '動作',
                'xlspos': [(25, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'check_status': {
                'xlsname': '待确认',
                'xlspos': [(26, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trans_status': {
                'xlsname': '状态',
                'xlspos': [(27, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trans_trigger': {
                'xlsname': 'Trigger',
                'xlspos': [(28, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trans_action': {
                'xlsname': '动作',
                'xlspos': [(29, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'trans_explain': {
                'xlsname': '说明（陈杨Comment 2018/3/19）',
                'xlspos': [(30, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'progress_status': {
                'xlsname': '状态',
                'xlspos': [(31, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'author_is_me': {
                'xlsname': '1）是否属于自己担当（如果知道是谁担当，请写出）',
                'xlspos': [(32, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'is_same_it': {
                'xlsname': '2）是否是同件（是的话，写出同件ID）',
                'xlspos': [(33, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'is_make': {
                'xlsname': '3)判断该要件是否能做（如果能判断的话）',
                'xlspos': [(34, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'is_have_qa': {
                'xlsname': '4)有QA的话，写出QA ID。',
                'xlspos': [(35, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_update_date': {
                'xlsname': '更新日期',
                'xlspos': [(36, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_represent': {
                'xlsname': '代表要件',
                'xlspos': [(37, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_fw16_status': {
                'xlsname': '①与FW16一起分析要件',
                'xlspos': [(38, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dev_s_date1': {
                'xlsname': '开始日期',
                'xlspos': [(39, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_model_status': {
                'xlsname': '②要件->具体模块分析\n(结合代码得出Astah图)',
                'xlspos': [(40, 3)],
                'datatype': 'INT',
                'needcheck': False,
            },
            'dev_s_date2': {
                'xlsname': '开始日期',
                'xlspos': [(41, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_ut_status': {
                'xlsname': '③完成自己模块的UT',
                'xlspos': [(42, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dev_s_date3': {
                'xlsname': '开始日期',
                'xlspos': [(43, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_it_status': {
                'xlsname': '④完成自己模块+1的IT',
                'xlspos': [(44, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dev_s_date4': {
                'xlsname': '开始日期',
                'xlspos': [(45, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_itn_status': {
                'xlsname': '⑤完成自己模块+N的IT',
                'xlspos': [(46, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dev_s_date5': {
                'xlsname': '开始日期',
                'xlspos': [(47, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'dev_commit_id': {
                'xlsname': '⑥提交CommitID',
                'xlspos': [(48, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_s_date6': {
                'xlsname': '提交日期',
                'xlspos': [(49, 3)],
                'datatype': 'DATETIME',
                'needcheck': True,
            },
            'atsah_path': {
                'xlsname': '成果物（atsah图)\n填写成果路完整路径',
                'xlspos': [(50, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_path': {
                'xlsname': '成果物(UT设计书)\n填写成果路完整路径',
                'xlspos': [(51, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'it_path': {
                'xlsname': '成果物(IT设计书)\n填写成果路完整路径',
                'xlspos': [(52, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'analysis_path': {
                'xlsname': '问题分析(文档/备注)\n填写成果路完整路径',
                'xlspos': [(53, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_status': {
                'xlsname': '开发状态',
                'xlspos': [(54, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'dev_remark': {
                'xlsname': '备注',
                'xlspos': [(55, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_qaid': {
                'xlsname': 'QAID',
                'xlspos': [(56, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'dev_qa_status': {
                'xlsname': 'QA状态',
                'xlspos': [(57, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            # 'author': {
            #     'xlsname': 'QA指派者',
            #     'xlspos': [(58, 3)],
            #     'datatype': 'STR',
            #     'needcheck': True,
            # },
            # 'qa_id': {
            #     'xlsname': 'QAIDCheck（系统关联）',
            #     'xlspos': [(59, 3)],
            #     'datatype': 'STR',
            #     'needcheck': True,
            # },
            'unit1': {
                'xlsname': 'Unit',
                'xlspos': [(60, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase1': {
                'xlsname': 'UseCase',
                'xlspos': [(61, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase1': {
                'xlsname': 'TestCase',
                'xlspos': [(62, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status1': {
                'xlsname': '开发状态',
                'xlspos': [(63, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no1': {
                'xlsname': '票号',
                'xlspos': [(64, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit2': {
                'xlsname': 'Unit',
                'xlspos': [(65, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase2': {
                'xlsname': 'UseCase',
                'xlspos': [(66, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase2': {
                'xlsname': 'TestCase',
                'xlspos': [(67, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status2': {
                'xlsname': '开发状态',
                'xlspos': [(68, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no2': {
                'xlsname': '票号',
                'xlspos': [(69, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit3': {
                'xlsname': 'Unit',
                'xlspos': [(70, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase3': {
                'xlsname': 'UseCase',
                'xlspos': [(71, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase3': {
                'xlsname': 'TestCase',
                'xlspos': [(72, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status3': {
                'xlsname': '开发状态',
                'xlspos': [(73, 3)],
                'datatype': 'ITN',
                'needcheck': True,
            },
            'ut_no3': {
                'xlsname': '票号',
                'xlspos': [(74, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit4': {
                'xlsname': 'Unit',
                'xlspos': [(75, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase4': {
                'xlsname': 'UseCase',
                'xlspos': [(76, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase4': {
                'xlsname': 'TestCase',
                'xlspos': [(77, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status4': {
                'xlsname': '开发状态',
                'xlspos': [(78, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no4': {
                'xlsname': '票号',
                'xlspos': [(79, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit5': {
                'xlsname': 'Unit',
                'xlspos': [(80, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase5': {
                'xlsname': 'UseCase',
                'xlspos': [(81, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase5': {
                'xlsname': 'TestCase',
                'xlspos': [(82, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status5': {
                'xlsname': '开发状态',
                'xlspos': [(83, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no5': {
                'xlsname': '票号',
                'xlspos': [(84, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit6': {
                'xlsname': 'Unit',
                'xlspos': [(85, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase6': {
                'xlsname': 'UseCase',
                'xlspos': [(86, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase6': {
                'xlsname': 'TestCase',
                'xlspos': [(87, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status6': {
                'xlsname': '开发状态',
                'xlspos': [(88, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no6': {
                'xlsname': '票号',
                'xlspos': [(89, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit7': {
                'xlsname': 'Unit',
                'xlspos': [(90, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase7': {
                'xlsname': 'UseCase',
                'xlspos': [(91, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase7': {
                'xlsname': 'TestCase',
                'xlspos': [(92, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status7': {
                'xlsname': '开发状态',
                'xlspos': [(93, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no7': {
                'xlsname': '票号',
                'xlspos': [(94, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit8': {
                'xlsname': 'Unit',
                'xlspos': [(95, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase8': {
                'xlsname': 'UseCase',
                'xlspos': [(96, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase8': {
                'xlsname': 'TestCase',
                'xlspos': [(97, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status8': {
                'xlsname': '开发状态',
                'xlspos': [(98, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no8': {
                'xlsname': '票号',
                'xlspos': [(99, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit9': {
                'xlsname': 'Unit',
                'xlspos': [(100, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase9': {
                'xlsname': 'UseCase',
                'xlspos': [(101, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase9': {
                'xlsname': 'TestCase',
                'xlspos': [(102, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status9': {
                'xlsname': '开发状态',
                'xlspos': [(103, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no9': {
                'xlsname': '票号',
                'xlspos': [(104, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'unit10': {
                'xlsname': 'Unit',
                'xlspos': [(105, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'usercase10': {
                'xlsname': 'UseCase',
                'xlspos': [(106, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'testcase10': {
                'xlsname': 'TestCase',
                'xlspos': [(107, 3)],
                'datatype': 'STR',
                'needcheck': True,
            },
            'ut_status10': {
                'xlsname': '开发状态',
                'xlspos': [(108, 3)],
                'datatype': 'INT',
                'needcheck': True,
            },
            'ut_no10': {
                'xlsname': '票号',
                'xlspos': [(109, 3)],
                'datatype': 'STR',
                'needcheck': True,
            }

        }

        self.xls_sheet_name = 'SP30SP31对象进度'
        self.start_data_row = 4
        self.id_col = "req_id"