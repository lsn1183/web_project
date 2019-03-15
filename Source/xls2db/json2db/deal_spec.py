# -*- coding: UTF-8 -*-
'''
Created on 2017-7-18

@author: hcz
'''
import os
import json
#from differ import compare_objects
from spec import SpecSpecification, SpecImage, SPEC_CHAPTER_LIST
from spec import SPEC_CHAPTER_NUM, SPEC_CHAPTER_TITLE
from spec import H_OLD_CONTENT, H_NEW_CONTENT
from req import ReqSpec
from Source.xls2db.common import cache_file
from Source.xls2db.json2db.hu import SpecHU
from Source.xls2db.json2db.definition import DefinitionSpec

DIFF_CHANGED = 'changed'  # 修改
DIFF_ADDED = 'added'  # 添加
DIFF_REMOVED = 'removed'  # 删除
DIFF_CHANGES = 'changes'  # 变更项
DIFF_DIFF = 'diff'
DIFF_DIST = 'distance'
DIFF_RIGHT = 'right'
DIFF_LEFT = 'left'


def load_hu(file_dir):
    if not os.path.isdir(file_dir):
        pass
    hu_obj = SpecHU()
    for f in sorted(os.listdir(file_dir)):
        path = os.path.join(file_dir, f)
        print path
        # continue
        if os.path.isfile(path):
            base_name, ext_name = os.path.splitext(path)
            if ext_name.lower() in ('.xlsx', '.xls'):
                hu_obj.set_path(path)
                hu_obj.store()


def load_def(file_dir):
    """TAGL定义"""
    if not os.path.isdir(file_dir):
        pass
    def_obj = DefinitionSpec()
    for f in sorted(os.listdir(file_dir)):
        path = os.path.join(file_dir, f)
        print path
        # continue
        if os.path.isfile(path):
            base_name, ext_name = os.path.splitext(path)
            if ext_name.lower() in ('.xlsx', '.xls'):
                def_obj.set_path(path)
                def_obj.store()


def parsers(file_dir):
    if not os.path.isdir(file_dir):
        pass
    spec_image = SpecImage.instance()
    for f in sorted(os.listdir(file_dir)):
        spec_image.set_in_dir(file_dir)
        path = os.path.join(file_dir, f)
        # print path
        # continue
        if os.path.isfile(path):
            base_name, ext_name = os.path.splitext(path)
            if ext_name.upper() == '.JSON':
                print base_name
                fp = open(path)
                obj_spec = parser(fp)
                obj_spec.store()


def parser(fp):
    d = json.load(fp)
    spec = SpecSpecification()
    spec.parser(d)
    return spec


def req_parsers(file_dir):
    """要求式样书"""
    if not os.path.isdir(file_dir):
        pass
    for f in sorted(os.listdir(file_dir)):
        path = os.path.join(file_dir, f)
        if os.path.isfile(path):
            base_name, ext_name = os.path.splitext(path)
            if ext_name.upper() == '.JSON':
                # print base_name
                if base_name.find('016_18') >= 0:
                    pass
                fp = open(path)
                obj_spec = req_parser(fp)
                obj_spec.store()


def req_parser(fp):
    """要求式样书"""
    d = json.load(fp)
    req_spec = ReqSpec()
    req_spec.parser(d)
    return req_spec


def load(p):
    spec = SpecSpecification()
    if type(p) == int:
        if spec.load(p):
            return spec
    else:
        if spec.load_by_name(p):
            return spec
    return None


def write_spec(spec, out_dir):
    """

    :type spec: object
    """
    if not spec:
        return
    file_name = spec.get_file_name()
    file_name = '.'.join([file_name, 'json'])
    path = os.path.join(out_dir, file_name)
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    else:
        if os.path.isfile(path):
            os.remove(path)
    attr_dict = spec.dump_attr(load_flag=True)
    # 写到在JSON文件
    jstr = json.dumps(attr_dict, ensure_ascii=False, encoding='utf8',
                      sort_keys=True, indent=2)
    out_fp = cache_file.open(path)
    out_fp.write(jstr)
    cache_file.close(out_fp, False)
    spec_image = SpecImage.instance ()
    spec_image.set_out_dir(out_dir)
    spec.download_images()


def spec_cmp(old, new):
    """
    diff: update
    """
    if not old and new:
        # 新规做成
        return None
    attr_dict1 = old.dump_attr(load_flag=False)
    attr_dict2 = new.dump_attr(load_flag=False)
    return None
    # if not attr_dict1:
    #     return None
    # diff = compare_objects(attr_dict1, attr_dict2)
    # return diff


def same(diff):
    if diff and diff.get(DIFF_DIST):
        if(not diff.get(DIFF_CHANGED) and
           not diff.get(DIFF_ADDED) and
           not diff.get(DIFF_REMOVED) and
           not diff.get(DIFF_CHANGES)):
            return True
    return False


def history(old, new):
    diff = spec_cmp(old, new)
    history_log = {'modify_reason': r"新規作成",  # 項番
                   'chapter': None,
                   'right': None,  # 更新前内容
                   'left': None,  # 更新后内容
                   }
    if diff is None:
        # 新规做成
        print history_log
    else:
        chapter_changes = parser_diff(diff)
    chapters = new.get_chapters()
    spec_id = new.get_id()
    for chapter_idx, diff_list in chapter_changes.iteritems():
        attr = chapters[chapter_idx].get_attr()
        chapter_num = attr.get(SPEC_CHAPTER_NUM)  # 章号
        chapter_title = attr.get(SPEC_CHAPTER_TITLE)  # 标题
        chapter_num += chapter_title
        for diff_info in diff_list:
            for func_type, diff in diff_info.iteritems():
                old_content = {func_type: json.loads(diff.get(DIFF_LEFT))}
                new_content = {func_type: json.loads(diff.get(DIFF_RIGHT))}
                history_log = {'modify_reason': '仕様変更',
                               SPEC_CHAPTER_NUM: chapter_num,
                               H_OLD_CONTENT: old_content,
                               H_NEW_CONTENT: new_content
                               }
                store_history(spec_id, history_log)


def parser_diff(diff):
    chapter_changes = {}
    changed_list = diff.get(DIFF_CHANGED)
    changes = diff.get(DIFF_CHANGES)
    if not changed_list:
        return chapter_changes
    for changed_key in changed_list:
        if changed_key == SPEC_CHAPTER_LIST:  # 章节
            chapter_diff_list = changes.get(SPEC_CHAPTER_LIST)
            sub_changed_list = chapter_diff_list.get(DIFF_CHANGED)
            sub_changes = chapter_diff_list.get(DIFF_CHANGES)
            for chapter_idx in sub_changed_list:
                chapter_diff = sub_changes.get(chapter_idx)
                content_list = parser_chapter_diff(chapter_diff)
                chapter_changes[chapter_idx] = content_list
    return chapter_changes


def parser_chapter_diff(diff):
    '''章节号，变更关键字，变更内容'''
    change_content_list = []

    sub_diff = diff.get(DIFF_DIFF)
    if sub_diff:
        temp = parser_chapter_diff(sub_diff)
        change_content_list += temp
    else:
        changed_list = diff.get(DIFF_CHANGED)
        changes = diff.get(DIFF_CHANGES)
        for changed_key in changed_list:
            sub_diff = changes.get(changed_key)
            if is_leaf(sub_diff):
                change_content_list.append({changed_key: sub_diff})
                return change_content_list
            else:
                temp = parser_chapter_diff(sub_diff)
                change_content_list += temp
    return change_content_list


def is_leaf(diff):
    if(not diff.get(DIFF_CHANGED) and
       not diff.get(DIFF_ADDED) and
       not diff.get(DIFF_REMOVED) and
       not diff.get(DIFF_DIFF)):
        return True
    else:
        return False


def store_history(spec_id, history_log):
    from Source.xls2db.common.db import pg
    sqlcmd = """
    INSERT INTO spec.spec_history(
                spec_id, modify_reason, chapter,
                old_content, new_content, modify_date)
        VALUES (%s, %s, %s,
                %s, %s, now());
    """
    my_pg = pg.instance()
    my_pg.connect2()
    my_pg.execute2(sqlcmd, (spec_id,
                            history_log.get('modify_reason'),
                            history_log.get(SPEC_CHAPTER_NUM),
                            json.dumps(history_log.get(H_OLD_CONTENT),
                                       ensure_ascii=False,
                                       encoding='utf8'),
                            json.dumps(history_log.get(H_NEW_CONTENT),
                                       ensure_ascii=False,
                                       encoding='utf8')
                            )
                   )
    my_pg.commit2()
