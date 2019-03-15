# -*- coding: UTF-8 -*-
'''
Created on 2017-7-18

@author: hcz
'''
import datetime
import json
import sys

from Source.xls2db.common import log
from Source.xls2db.common import cache_file, rdb_log
from Source.xls2db.json2db import deal_spec, spec, req, definition, arl, hu


def main():

    print 'UpLoad:', datetime.datetime.now()
    log.common_log.instance().init()
    rdb_log.init()
    # 导入机能式样书
    spec_image = spec.SpecImage.instance()
    # in_file_dir = r'C:\workspace\Spec2db\Spec2DB\Source\xls2db\json'
    in_file_dir = r'C:\Users\hcz\Desktop\projdoc\659B\func_json'
    spec_image.set_in_dir(in_file_dir)
    deal_spec.parsers(in_file_dir)
    # 导入要求式样书
    # in_file_dir = r'C:\Users\hcz\Desktop\func_json'
    # obj_chapter = req.ReqChapter.instance()
    # obj_chapter.load()
    # deal_spec.req_parsers(in_file_dir)
    # 导入要求式样书的.
    # deal_spec.parse_arl_func_file()

    # ###### Operation
    # path = r'C:\Users\hcz\Desktop\ope_dump'
    # deal_spec.ope_parsers(path)

#     file_name = new_spec.get_file_name()
#     spec1 = deal_spec.load(file_name)
#     spec2 = deal_spec.load(new_spec.get_id())
#     diff = deal_spec.spec_cmp(spec1, spec2)
#     if diff:
#         if not deal_spec.same(diff):
#             deal_spec.history(spec1, spec2)
    # os.system('rm tt.json;')
    #############
    # fp = open(r'C:\workspace\Spec2db\Spec2DB\Source\xls2db\json\func_3_12_USB.json')
    # d = json.load(fp)
    # jstr = json.dumps(d, ensure_ascii=False, encoding='utf8',
    #                   sort_keys=True, indent=2)
    # path = r'func_3_12_USB.json'
    # out_fp = cache_file.open(path)
    # out_fp.write(jstr)
    # cache_file.close(out_fp, False)
    # ##
    #
    # out_dir = r'C:\workspace\Spec2db\Spec2DB\Source\xls2db\out_json'
    # name = '第2.1章'
    # spec2 = deal_spec.load(name)
    # deal_spec.write_spec(spec2, out_dir)
    # deal_spec.parse_func_content()
    ##############
    # ARL
    # obj_arl = arl.SpecArl()
    # path = r'C:\Users\hcz\Desktop\TAGL\ARL.xlsx'
    # obj_arl.set_path(path)
    # obj_arl.store()
    # # HU
    # obj_hu = hu.SpecHU()
    # path = r'C:\Users\hcz\Desktop\TAGL\0926\HU.xlsx'
    # obj_hu.set_path(path)
    # obj_hu.store()
    # # 要件定义
    # ojb_def = definition.DefinitionSpec ()
    # path = r'C:\Users\hcz\Desktop\TAGL\0926\TAGL_RequirementDefinitionVer.xlsx'
    # ojb_def.set_path (path)
    # ojb_def.store ()
    # # 分析
    # path = r'C:\Users\hcz\Desktop\TAGL\0926\TAGL_RequirementAnalysis.xlsx'
    # analysis = definition.AnalysisSpec ()
    # analysis.set_path (path)
    # analysis.store ()
    # ###### HU ###########################
    # hu_dir = r'C:\SpiderInput\HU\1012\1'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\2'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\3'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\4'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\5'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\6'
    # deal_spec.load_hu(hu_dir)
    # hu_dir = r'C:\SpiderInput\HU\1012\7'
    # deal_spec.load_hu(hu_dir)
    # ###### DEF ###########################
    # def_dir = r'C:\SpiderInput\TAGL\definition\1012\1'
    # deal_spec.load_def(def_dir)
    # def_dir = r'C:\SpiderInput\TAGL\definition\1012\2'
    # deal_spec.load_def(def_dir)
    # def_dir = r'C:\SpiderInput\TAGL\definition\1012\3'
    # deal_spec.load_def(def_dir)
    # def_dir = r'C:\SpiderInput\TAGL\definition\1012\4'
    # deal_spec.load_def(def_dir)
    log.common_log.instance().end()
    rdb_log.end()
    print datetime.datetime.now()
    return 0


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()

