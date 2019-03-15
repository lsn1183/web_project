# -*- coding: UTF-8 -*-
import copy
import datetime
import json
import os
import pandas as pd
from openpyxl import load_workbook

from app.db import db
from flask import current_app
from sqlalchemy import or_, and_
from app.db.ds_drbfm import DSDrbfm
from app.db.ds_failure import DSFailure
from app.db.ds_scene import DSScene
from app.db.ds_scene import DSRelScene
from app.db.ds_scene import DSRelTag
from app.db.model import DSRelModel
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_doc import CtrlFailureMode


class CtrlDsDrbfm(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSDrbfm.gid
        self.db_object = DSDrbfm
        self.col_list = [DSDrbfm.drbfm_content.name, ]

    def get_by_usecase_id(self, usecase_id):
        pass

    def get(self, usecase_id, sec_type=None, condition=None):
        # drbfm_list, status = self.get2(usecase_id, sec_type, condition)
        # if drbfm_list:
        #     return drbfm_list, status
        status = 'normal'
        drbfm_scene, status = self.get_drbfm_scene(usecase_id, status)
        failures_tree = CtrlDSFailure().get_failures_tree(usecase_id, condition)
        if condition == 'YES':
            if status != 'NO_SCENE':
                if not failures_tree:
                    status = 'NO_CONTENT'
        # print(1, datetime.datetime.now())
        # for item_id in drbfm_scene:
        #     scenes = drbfm_scene.get(item_id)
        #     self._get_sub(failures_tree, scenes, item_id)
        # print(2, datetime.datetime.now())
        self._merge_failures_drbfm(failures_tree, drbfm_scene)
        # print(3, datetime.datetime.now())
        return failures_tree, status

    def _get_sub(self, failures_tree, scenes, id):
        for failures in failures_tree:
            sub = failures.get('sub')
            item_id = failures.get('item_id')
            if id == item_id:
                failures['scenes'] = scenes
                return
            else:
                self._get_sub(sub, scenes, id)

    def get_db_for_journal(self, doc_id):
        # drbfms = (db.session.query(DSDrbfm)
        #           .filter(DSDrbfm.sec_id == sec_id)
        #           .order_by(DSDrbfm.gid).all())
        q = (db.session.query(DSRelModel)
             .outerjoin(DSRelTag, DSRelModel.change_id == DSRelTag.gid)
             .filter(DSRelTag.doc_id == doc_id)
             .order_by(DSRelModel.change_id, DSRelModel.change_type))
        drbfms = q.all()
        return drbfms

    def _merge_failures_drbfm(self, failures, drbfm_scene):
        for failure in failures:
            item_id = failure.get(DSFailure.item_id.name)
            if item_id:
                failure['scenes'] = drbfm_scene.get(item_id)
            else:
                sub_failures = failure.get("sub")
                self._merge_failures_drbfm(sub_failures, drbfm_scene)

    def get_drbfm_scene(self, usecase_id, status):
        scene_list = self.get_scenes_by_usecase_id(usecase_id)
        if not scene_list:
            status = 'NO_SCENE'
        failure_list = self.get_failure_list()
        drbfm_dict = self.get_drbfms_by_usecase_id(usecase_id)
        data_dict = dict()
        for item_id in failure_list:
            copy_scene = copy.deepcopy(scene_list)
            drbfm_list = drbfm_dict.get(item_id)
            if drbfm_list:
                for fm in drbfm_list:
                    scene_id = fm.get('scene_id')
                    drbfm_content = fm.get('drbfm_content')
                    for scene in copy_scene:
                        if scene_id == scene.get('scene_id'):
                            scene['content'] = drbfm_content
                            scene['gid'] = fm.get('gid')
            data_dict[item_id] = copy_scene
        return data_dict, status

    def delete_by_sec_id(self, sec_id):
        drbfm_q = db.session.query(DSDrbfm).filter(DSDrbfm.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for drbfm in drbfm_q:
            old_data_list.append(drbfm.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def get_scenes_by_usecase_id(self, usecase_id):
        scenes = db.session.query(DSScene) \
            .outerjoin(DSRelScene, DSScene.scene_id == DSRelScene.scene_id).filter(DSRelScene.sec_id == usecase_id)
        scene_list = []
        for sc in scenes:
            scene_dict = dict()
            scene_dict[DSScene.scene_id.name] = sc.scene_id
            scene_dict[DSScene.scene.name] = sc.scene
            scene_dict[DSScene.explain.name] = sc.explain
            scene_dict['content'] = ''
            scene_dict['showFlag'] = False
            scene_list.append(scene_dict)
        return scene_list

    def get_failure_list(self):
        failures = db.session.query(DSFailure).order_by(DSFailure.item_id).distinct()
        failure_list = []
        for failure in failures:
            failure_list.append(failure.item_id)
        return failure_list

    def get_drbfms_by_usecase_id(self, usecase_id):
        drbfm_dict = dict()
        drbfms = db.session.query(DSDrbfm).filter(DSDrbfm.sec_id == usecase_id)
        for drbfm in drbfms:
            if not drbfm_dict.get(drbfm.item_id):
                drbfm_dict[drbfm.item_id] = []
            sub_dict = dict()
            sub_dict[DSDrbfm.gid.name] = drbfm.gid
            sub_dict[DSDrbfm.scene_id.name] = drbfm.scene_id
            content = drbfm.drbfm_content
            if not content:
                content = ''
            sub_dict[DSDrbfm.drbfm_content.name] = content
            drbfm_dict[drbfm.item_id].append(sub_dict)
        return drbfm_dict

    def add(self, drbfm_data, commit_user):
        update_time = self.get_current_time()
        from app.ctrl.ctrl_ds_section import CtrlDSSection
        micro_ver = drbfm_data.get('micro_ver')
        doc_id = drbfm_data.get('doc_id')
        if not doc_id:
            return False, '未指定文档ID!'
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        content = drbfm_data.get('content')
        if content:
            sec_id = drbfm_data.get('content')[0].get('sec_id')
            if not sec_id:
                return False, '没有指定USECASE_ID！'
            old_data, error = CtrlDSSection().session_is_exist(sec_id)
            if error:
                return 0, error
            old_micro_ver = CtrlDSSection().get_sec_ver(sec_id)
            flag, error = self.diff_ver(micro_ver, old_micro_ver)
            if not flag:
                return False, error
        try:
            new_data_list = self.get_new_drbfm(content)
            old_data_list = self.get_old_data(self.db_object, DSDrbfm.sec_id, sec_id)
            commit_list = self.add_list(self.db_object, new_data_list, old_data_list, self.key_col, self.col_list)
            if commit_list:
                log_dict = CtrlDSSection().update_ver(sec_id)
                commit_list.append(log_dict)
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return sec_id, 'ok'
        except Exception as e:
            current_app.logger.error('%s' % e)
            db.session.rollback()
            return False, "服务异常！请联系管理员！"

    def get_new_drbfm(self, drbfm_content):
        drbfm_list = []
        for drbfm in drbfm_content:
            drbfm_dict = dict()
            drbfm_dict['gid'] = drbfm.get('gid')
            drbfm_dict['sec_id'] = drbfm.get('sec_id')
            drbfm_dict['item_id'] = drbfm.get('item_id')
            drbfm_dict['scene_id'] = drbfm.get('scene_id')
            drbfm_dict['drbfm_content'] = drbfm.get('drbfm_content')
            drbfm_list.append(drbfm_dict)
        return drbfm_list

    def get2(self, usecase_id, sec_type=None, condition=None):
        drbfm_list = []
        from app.ctrl.ctrl_ds_scene import CtrlDSScene
        drbfm_df = self.get_drbfm_df(usecase_id)
        if drbfm_df.empty:
            return drbfm_list, 'NO_SCENE'
        columns = {DSDrbfm.drbfm_content.name: "content"}
        drbfm_df.rename(columns=columns, inplace=True)
        drbfm_df.fillna('', inplace=True)
        if condition == 'YES':  # 过滤列
            drbfm_df2 = drbfm_df[~drbfm_df["content"].isin(['', '-'])]
            if drbfm_df2.empty:
                return drbfm_list, 'NO_CONTENT'
            scene_id_list = list(drbfm_df2["scene_id"].unique())
            drbfm_df = drbfm_df[drbfm_df["scene_id"].isin(scene_id_list)]
        if drbfm_df.empty:
            return drbfm_list, 'NO_CONTENT'
        failure_df = CtrlDSFailure().get_failure_df()
        scene_df = CtrlDSScene().get_scene_df()
        merge_df = pd.merge(failure_df, drbfm_df, how="left",
                            on=[DSFailure.item_id.name])
        print(merge_df)
        merge_df = pd.merge(merge_df, scene_df, how="left",
                            on=[DSScene.scene_id.name])
        merge_df["showFlag"] = [False] * len(merge_df)
        category_list = list(merge_df["category"].unique())
        for category in category_list:
            cat_dict = {"name": category, "sub": []}
            df1 = merge_df[merge_df["category"] == category]
            major_items = list(df1["major_item"].unique())
            for major_item in major_items:
                major_dict = {"name": major_item, "sub": []}
                df2 = df1[df1["major_item"] == major_item]
                failure_list = list(df2["failure"].unique())
                for failure in failure_list:
                    failure_dict = {"name": failure, "sub": []}
                    df3 = df2[df2["failure"] == failure]
                    if condition == 'YES':  # 过滤行
                        df4 = df3[~df3["content"].isin(['', '-'])]
                        if df4.empty:
                            continue
                    failure_dict["item_id"] = int(df3.iloc[0].item_id)
                    df3 = df3[["gid", "scene_id", "content",
                               "scene", "explain", "showFlag"]]
                    failure_dict["scenes"] = df3.to_dict(orient="record")
                    major_dict["sub"].append(failure_dict)
                if major_dict["sub"]:
                    cat_dict["sub"].append(major_dict)
            if cat_dict["sub"]:
                drbfm_list.append(cat_dict)
        return drbfm_list, 'normal'

    def get_drbfm_df(self, usecase_id):
        q = (db.session.query(DSDrbfm)
             .filter(DSDrbfm.sec_id == usecase_id)
             .order_by(DSDrbfm.item_id, DSDrbfm.scene_id))
        drbfm_df = pd.read_sql(q.statement, db.session.bind)
        return drbfm_df

    def get_drbfm_new(self, doc_id):
        drbfm = []
        df = self._get_drbfm_df(doc_id)
        if df.empty:
            return []
        change_id_list = df["change_id"].unique()
        model_name = self.get_curr_model_name(doc_id)
        for change_id in change_id_list:
            sub_df = df[df["change_id"] == change_id]
            change_types = ["change", "influence"]
            for change_type in change_types:
                change_info = dict()
                change_content = self._convert_change_content(sub_df,
                                                              change_type)
                if not change_content:
                    continue
                change_content = '\n'.join([u"【部品名】",
                                            model_name,
                                            "\n【目的】",
                                            change_content])
                change_info["change_content"] = change_content
                if change_type == "change":  # 修改点
                    change_df = sub_df[sub_df["change_type"] == change_type]
                else:  # 影响点
                    change_df = sub_df[sub_df["change_type"] == change_type]
                model_list, failuremode_num = self._convert_models(change_df)
                if not model_list:
                    continue
                change_info["model_list"] = model_list
                change_info["row_num"] = failuremode_num
                drbfm.append(change_info)
        return drbfm

    def _convert_change_content(self, df, change_type):
        change_content = u""
        s = df.iloc[0]
        if change_type == "change":  # 修改点
            change_content += '修改前:\n'
            before_change = s["before_change"]
            change = s["change"]
            if before_change == '同上' and change == '同上':
                return ''
            if not before_change:
                before_change = ''
            change_content += before_change + '\n'
            change_content += '\n修改后:\n'
            if not change:
                change = ''
            change_content += change
        else:
            change_content += '影响前:\n'
            before_change = s["before_influence"]
            change = s["influence"]
            if before_change == '同上' and change == '同上':
                return ''
            if not before_change:
                before_change = ''
            change_content += before_change + '\n'
            change_content += '\n影响后:\n'
            if not change:
                change = ''
            change_content += change
        return change_content

    def get_curr_model_name(self, doc_id):
        from app.db.ds_doc import Ds_Doc
        from app.db.model import Model
        q = (db.session.query(Model.title)
             .outerjoin(Ds_Doc, Model.model_id == Ds_Doc.model_id)
             .filter(Ds_Doc.doc_id == doc_id))
        model = q.first()
        model_name = model.title
        return model_name

    def _convert_models(self, df):
        df = df.dropna(subset=["model_id"])
        df = df[["model_id", "model_name", "failure_id_list"]]
        model_list = []
        mode_obj = CtrlFailureMode()
        failuremode_num = 0
        for model_info in df.to_dict(orient='records'):
            model_dict = dict()
            model_dict["model_name"] = model_info.get("model_name")
            failure_id_list = model_info["failure_id_list"]
            if failure_id_list:
                failure_id_list = json.loads(failure_id_list)
                doc_id_list = failure_id_list["havething_list"]
            else:
                doc_id_list = []
            failuremode_list = []
            if doc_id_list:
                for doc_id in doc_id_list:
                    fail_modes = mode_obj.get_failermode_by_doc_id(doc_id)
                    fail_modes = [m.get("failure_mode_name") for m in fail_modes]
                    failuremode_list += fail_modes
            failuremode_list = list(set(failuremode_list))
            if failuremode_list:
                model_dict["failuremode_list"] = failuremode_list
                model_list.append(model_dict)
            failuremode_num += len(failuremode_list)
        return model_list, failuremode_num

    def _get_drbfm_df(self, doc_id):
        sqlcmd = """
        SELECT doc_id, tag_id, a.gid as change_id, change_type,
               before_change, change, before_influence, influence,
               c.model_id, title as model_name, failure_id_list
          FROM ds.ds_rel_tag as a
          left join ds.ds_rel_model as b
          on a.gid = b.change_id
          left join ds.model as c
          on b.model_id = c.model_id
          where doc_id = {doc_id}
          order by tag_id, order_id
        """.format(doc_id=doc_id)
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        return df

    def export_drbfm(self, proj_id, doc_id):
        from app.ctrl.ctrl_project import CtrlProject
        from app.export_doc.export_factory import ExportDrbfmFactory
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        msg, file_path = '', ''
        _, proj_list = CtrlProject().get(proj_id)
        if proj_list:
            proj_name = proj_list[0].get("proj_name")
        else:
            msg = '指定的项目不存在!'
            return msg, file_path
        out_dir = os.path.join("export_root", "drbfm")
        drbfm_data = self.get_drbfm_new(doc_id)
        export_obj = ExportDrbfmFactory.create(proj_name)
        doc_data = CtrlDsDoc().get_doc(doc_id)
        if doc_data:
            doc_name = doc_data.get('title')
        else:
            msg = '该文档不存在!'
            return msg, file_path
        export_obj.drbfm_data = drbfm_data
        file_path = export_obj.write_drbfm_data(out_dir, doc_name)
        return msg, file_path

    def write_excel_cell(self, sheet, row, row_data):
        start_col = 1
        end_col = len(row_data) + 1
        while start_col < end_col:
            sheet.cell(row=row, column=start_col).value = row_data[start_col-1]
            start_col += 1


class CtrlDSFailure(object):
    def __init__(self):
        pass

    def get_failures(self):
        failure_list = []
        q = db.session.query(DSFailure).order_by(DSFailure.item_id).distinct()
        # print(q.statement)
        for failure in q:
            failure_list.append(failure.to_dict())
        return failure_list

    def get_failure_df(self):
        q = db.session.query(DSFailure).order_by(DSFailure.item_id).distinct()
        sqlcmd = q.statement
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        return df

    def get_failures2(self):
        failure_list = []
        q = db.session.query(DSFailure).order_by(DSFailure.category,
                                                 DSFailure.major_item,
                                                 DSFailure.item_id)

        # print(q.statement)
        for failure in q:
            failure_list.append(failure.to_dict())
        return failure_list

    def get_failures_tree(self, usecase_id, condition):
        failure_list = self.get_failures()
        failure_tree_list = []
        for fail in failure_list:
            item_id = fail.get('item_id')
            check_result = self.filter_failures_tree(usecase_id, item_id)
            if condition == 'YES':
                if not check_result:
                    continue
            elif condition == 'NO':
                if check_result:
                    continue
            category = fail.get('category')
            major_item = fail.get('major_item')
            failure = fail.get('failure')
            if not failure_tree_list:
                failure_dict = {'item_id': item_id, 'name': failure, 'sub': [], 'scenes': []}
                major_item_dict = {'name': major_item, 'sub': [failure_dict, ]}
                category_dict = {'name': category, 'sub': [major_item_dict, ]}
                failure_tree_list.append(category_dict)
                continue
            for failure_tree in failure_tree_list:
                n = failure_tree_list.index(failure_tree) + 1
                if category == failure_tree.get('name'):
                    major_item_list = failure_tree.get('sub')
                    for major in major_item_list:
                        i = major_item_list.index(major) + 1
                        if major_item == major.get('name'):
                            fail_list = major.get('sub')
                            fail_list.append({'item_id': item_id, 'name': failure, 'sub': [], 'scenes': []})
                            break
                        else:
                            if i == len(major_item_list):
                                failure_dict = {'item_id': item_id, 'name': failure, 'sub': [], 'scenes': []}
                                major_item_dict = {'name': major_item, 'sub': [failure_dict, ]}
                                major_item_list.append(major_item_dict)
                                break
                            else:
                                continue
                else:
                    if n == len(failure_tree_list):
                        failure_dict = {'item_id': item_id, 'name': failure, 'sub': [], 'scenes': []}
                        major_item_dict = {'name': major_item, 'sub': [failure_dict, ]}
                        category_dict = {'name': major_item, 'sub': [major_item_dict, ]}
                        failure_tree_list.append(category_dict)
                        break
                    else:
                        continue
        return failure_tree_list

    def get_failures_tree2(self):
        """只有叶子的model_id是正确的"""
        failure_list = self.get_failures()
        forest = []
        for failure in failure_list:
            sub_list = forest
            for col in [DSFailure.category.name,
                        DSFailure.major_item.name,
                        DSFailure.failure.name]:
                cat = failure.get(col)
                if cat:
                    found_failure_dict = dict()
                    for temp_model_dict in sub_list[::-1]:
                        if cat == temp_model_dict.get("name"):
                            found_failure_dict = temp_model_dict
                            break
                    if not found_failure_dict:
                        found_failure_dict = {"name": cat, "sub": []}
                        sub_list.append(found_failure_dict)
                    if col == DSFailure.failure.name:
                        found_failure_dict["item_id"] = failure.get("item_id")
                    sub_list = found_failure_dict.get("sub")
                else:  #
                    pass
        return forest

    def filter_failures_tree(self, usecase_id, item_id):
        q = db.session.query(DSDrbfm).filter(DSDrbfm.sec_id == usecase_id, DSDrbfm.item_id == item_id)
        check_result = False
        for drbfm in q:
            if drbfm.drbfm_content and drbfm.drbfm_content != '-':
                check_result = True
                break
        return check_result



