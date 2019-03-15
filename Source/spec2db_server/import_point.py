# -*- coding: UTF-8 -*-
import os
import re

from spec_import.new_import import ArlImport
from arl.arl_tmc_pointinfo import TmcPointInfo
from arl.point_out import PointOut

point_index_file = '元ファイル/HU要件定義/要件定義・分析レビュー計画詳細HU要件定義用.xlsx'
hu_file_folder = '元ファイル/HU要件定義'
def_file_folder = '元ファイル/TAGL要件定義書'
ana_file_folder = '元ファイル/TAGL要件分析書'

def check_point_path(root_path):
    if not os.path.exists(os.path.join(root_path, point_index_file)):
        print "point index file does not exist"
        return False
    if not os.path.exists(os.path.join(root_path, hu_file_folder)):
        print "HU file folder is not exits"
        return False
    if not os.path.exists(os.path.join(root_path, def_file_folder)):
        print "Def file folder is not exits"
        return False
    if not os.path.exists(os.path.join(root_path, ana_file_folder)):
        print "Ana file folder is not exits"
        return False
    return True

def do_point_xls_path(point_date_info, xls_path, data_type):
    extra_info_dict = {}
    extra_info_dict['point_date'] = point_date_info

    if data_type == "HU":
        extra_info_dict['classify'] = "hu"
        xls_file_regx = "^HU_RequirementDefinition.*"
        xls_data_folder = hu_file_folder
    elif data_type == "DEF":
        extra_info_dict['classify'] = "def"
        xls_file_regx = "^TAGL_RequirementDefinition.*"
        xls_data_folder = def_file_folder
    elif data_type == "ANA":
        extra_info_dict['classify'] = "analysis"
        xls_file_regx = "^TAGL_RequirementAnalysis.*"
        xls_data_folder = ana_file_folder

    TmcPointInfo().delete_info(extra_info_dict['classify'], extra_info_dict['point_date'])

    for root, _, files in os.walk(os.path.join(xls_path, xls_data_folder)):
        if files:
            for file in files:
                if re.match(xls_file_regx, file):
                    try:
                        dest_file_name = file.decode("utf8").encode("utf8")
                    except:
                        dest_file_name = file.decode("gbk").encode("utf8")
                    dest_file_name = dest_file_name.replace(' ', r'\ ')

                    if data_type == "HU":
                        extra_info_dict['folder_info'] = root.split("/")[-1]
                    else:
                        extra_info_dict['folder_info'] = "-"
                    extra_info_dict['file_info'] = dest_file_name

                    dump_cmd = '''java -Xms4g -Xmx16g -jar tools/export/jar/DumpPointInfo.jar %s %s %s''' % (
                        os.path.join(root, dest_file_name),
                        data_type,
                        './dump_temp.json'
                    )
                    print dump_cmd
                    if os.system(dump_cmd) !=0:
                        continue
                    import json
                    with open("./dump_temp.json","r") as f:
                        try:
                            json_data = json.load(f)
                            if len(json_data) > 0:
                                TmcPointInfo().store_json(extra_info_dict, json_data)
                        except Exception as e:
                            print e.message
                            continue


if __name__ == '__main__':
    point_path = "/mnt/sharedoc/point/20171221"

    if check_point_path(point_path) == False:
        exit(1)

    point_date_info = point_path.split("/")[-1]

    full_index_file = os.path.join(point_path, point_index_file)
    retDict = ArlImport(None, None,None).point_import(file_path=full_index_file,
                                                      new_date=point_date_info)
    if retDict['result'] != 'OK':
        print "index file import error"
        exit(1)

    do_point_xls_path(point_date_info, point_path, "HU")
    do_point_xls_path(point_date_info, point_path, "DEF")
    do_point_xls_path(point_date_info, point_path, "ANA")

    PointOut('hu').update_by_tmc_point(point_date_info, 'hu')
    PointOut('def').update_by_tmc_point(point_date_info, 'def')
    PointOut('analysis').update_by_tmc_point(point_date_info, 'analysis')

    print "finish"

