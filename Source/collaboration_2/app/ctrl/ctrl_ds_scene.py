# -*- coding: UTF-8 -*-
import pandas as pd
import json
from app.db import db
from flask import current_app
from app.db.ds_scene import DSScene, DSSceneType
from app.db.ds_scene import DSRelScene, DSSceneTag
from app.db.ds_scene import DSRelTag
from app.db.model import DSRelModel
from sqlalchemy import or_, and_
from app.ctrl.ctrl_ds_section import CtrlDSSection, CtrlDSConsider
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_doc_tag import CtrlDocTag
import pandas as pd


class CtrlDSScene(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = DSRelScene.gid
        self.db_object = DSRelScene
        self.col_list = [DSRelScene.change.name, DSRelScene.alter.name]

    def get_scene(self):
        q = db.session.query(DSScene).order_by(DSScene.order_no,
                                               DSScene.scene_id)
        scene_df = pd.read_sql(q.statement, db.session.bind)
        q = db.session.query(DSSceneType).order_by(DSSceneType.scene_type_id)
        scene_type_df = pd.read_sql(q.statement, db.session.bind)
        merge_df = pd.merge(scene_df, scene_type_df, how='inner',
                            on=[DSSceneType.scene_type_id.name])
        scene_types = list(merge_df[DSSceneType.scene_type.name].unique())
        scene_list = []
        i = 0
        for scene_type in scene_types:
            s_dict = dict()
            sub_df = merge_df[merge_df[DSSceneType.scene_type.name] == scene_type]
            sub_scene_list = sub_df.to_dict(orient='record')
            s_dict["scene"] = scene_type
            s_dict["scenes"] = sub_scene_list
            s_dict["scene_type_org"] = sub_scene_list[0].get("scene_type_org")
            s_dict["scene_id"] = i
            i -= 1
            scene_list.append(s_dict)
        return scene_list

    def get_scene_by_sec(self, sec_id):
        """
        #根据sec_id获取场景
        :param sec_id:
        :return:
        """
        scene_list = []
        q = (db.session.query(DSScene.scene_id, DSScene.scene, DSScene.explain,
             DSRelScene.change, DSRelScene.alter, DSRelScene.gid, DSScene.scene_type_id)
             .outerjoin(DSRelScene, DSScene.scene_id == DSRelScene.scene_id)
             .filter(DSRelScene.sec_id == sec_id).order_by(DSScene.scene_id))
        scene_df = pd.read_sql(q.statement, db.session.bind)
        q = db.session.query(DSSceneType).order_by(DSSceneType.scene_type_id)
        scene_type_df = pd.read_sql(q.statement, db.session.bind)
        merge_df = pd.merge(scene_df, scene_type_df, how='inner',
                            on=[DSSceneType.scene_type_id.name])
        scene_list = merge_df.to_dict(orient='record')
        return scene_list
        # for s in q:
        #     scene_dict = dict()
        #     scene_dict['scene_id'] = s[0]
        #     scene_dict['scene'] = s[1]
        #     scene_dict['explain'] = s[2]
        #     scene_dict['change'] = s[3]
        #     scene_dict['alter'] = s[4]
        #     scene_dict['gid'] = s[5]
        #     scene_list.append(scene_dict)
        # return scene_list

    def get_scene_by_doc(self, doc_id):
        """
        #根据sec_id获取场景(场景画面)
        :param sec_id:
        :return:
        """
        sqlcmd = """
                SELECT a.gid, p.tag as parent_tag,
                       a.tag_id, b.tag,
                       before_change, change,
                       before_influence, influence
                  FROM ds.ds_rel_tag as a
                  LEFT JOIN public.doc_tag_category as b
                  on a.tag_id = b.tag_id
                  left join public.doc_tag_category as p
                  on b.parent_tag_id = p.tag_id
                  where doc_id = {doc_id}
                  order by b.parent_tag_id, a.tag_id, order_id, gid
                """.format(doc_id=doc_id)
        df = pd.read_sql(sqlcmd, db.session.bind)
        scene_list = df.to_dict(orient='records')
        return scene_list

    def get_scene_by_doc2(self, doc_id):
        """
        #根据doc_id获取场景(修改点、影响点)
        :param sec_id:
        :return:
        """
        sqlcmd = """
        SELECT a.gid, p.tag as parent_tag,
               a.tag_id, b.tag,
               before_change, change,
               before_influence, influence
          FROM ds.ds_rel_tag as a
          LEFT JOIN public.doc_tag_category as b
          on a.tag_id = b.tag_id
          left join public.doc_tag_category as p
          on b.parent_tag_id = p.tag_id
          where doc_id = {doc_id}
          order by b.parent_tag_id, a.tag_id, order_id, gid
        """.format(doc_id=doc_id)
        rel_tags = []
        df = pd.read_sql(sqlcmd, db.session.bind)
        tag_ids = df["tag_id"].unique()
        for tag_id in tag_ids:
            sub_df = df[df["tag_id"] == tag_id]
            s = sub_df.iloc[0]
            tag_info = {"parent_tag": s["parent_tag"],
                        "tag_id": int(s["tag_id"]),
                        "tag": s["tag"]}
            columns = ["gid", "before_change", "change",
                       "before_influence", "influence"]
            changes = sub_df[columns].to_dict(orient='records')
            tag_info["changes"] = changes
            rel_tags.append(tag_info)
        return rel_tags

    # def get_db_for_journal(self, sec_id):
    #     """
    #     #根据sec_id获取场景
    #     :param sec_id:
    #     :return: DSScene object list
    #     """
    #     q = (db.session.query(DSRelScene).filter(DSRelScene.sec_id == sec_id)
    #          .order_by(DSRelScene.gid))
    #     scene_list = q.all()
    #     return scene_list

    def add(self, data_dict, commit_user):
        update_time = self.get_current_time()
        micro_ver = data_dict.get('micro_ver')
        doc_id = data_dict.get(DSRelScene.doc_id.name)
        if not doc_id:
            return False, '未指定文档ID!'
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        sec_id = data_dict.get(DSRelScene.sec_id.name)
        if not sec_id:
            return False, '没有指定USECASE_ID！'
        old_data, error = CtrlDSSection().session_is_exist(sec_id)
        if error:
            return 0, error
        old_micro_ver = CtrlDSSection().get_sec_ver(sec_id)
        flag, error = self.diff_ver(micro_ver, old_micro_ver)
        if not flag:
            return False, error
        old_scenes_data = self.get_old_data(self.db_object, DSRelScene.sec_id, sec_id)
        scenes = data_dict.get("scenes")
        try:
            drbfm_log_list = self.delete_scene_drbfm(sec_id, scenes, old_scenes_data)
            new_scene_list = self.get_new_scene_list(scenes, doc_id, sec_id)
            scene_log_list = self.add_list(self.db_object, new_scene_list, old_scenes_data,
                                           self.key_col, self.col_list)
            db.session.flush()
            consider_log_list = CtrlDSConsider().create_considers(sec_id)
            commit_list = drbfm_log_list + scene_log_list + consider_log_list
            if commit_list:
                log_dict = CtrlDSSection().update_ver(sec_id)
                commit_list.append(log_dict)
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return sec_id, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def add2(self, data_dict):
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        update_time = self.get_current_time()
        micro_ver = data_dict.get('micro_ver')
        doc_id = data_dict.get('doc_id')
        commit_user = data_dict.get('commit_user')
        content = data_dict.get('content')
        if not doc_id:
            return False, '未指定文档ID!'
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        old_micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        flag, error = self.diff_ver(micro_ver, old_micro_ver)
        if not flag:
            return 0, error
        data_list = []
        new_gid_list = []
        old_data_list = self.get_old_data(DSRelTag, DSRelTag.doc_id, doc_id)
        old_gid_list = []
        commit_list = []
        for old_data in old_data_list:
            old_gid_list.append(old_data.get('gid'))
        for data in content:
            tag_id = data.get('tag_id')
            changes = data.get('changes')
            for change in changes:
                if change.get('gid'):
                    new_gid_list.append(change.get('gid'))
                change_info = dict()
                change_info['gid'] = change.get('gid')
                change_info['doc_id'] = doc_id
                change_info['tag_id'] = tag_id
                change_info['before_change'] = change.get('before_change')
                change_info['change'] = change.get('change')
                change_info['before_influence'] = change.get('before_influence')
                change_info['influence'] = change.get('influence')
                change_info['order_id'] = changes.index(change)+1
                data_list.append(change_info)
        try:
            for old_gid in old_gid_list:
                if old_gid not in new_gid_list:
                    commit_list += self.del_scene_considers(old_gid)
            commit_list += self.add_list(DSRelTag, data_list, old_data_list, DSRelTag.gid,
                                         [DSRelTag.before_change.name, DSRelTag.change.name,
                                          DSRelTag.before_influence.name, DSRelTag.influence.name,
                                          DSRelTag.order_id.name])
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return doc_id, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def add_scene(self, data_json):
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        update_time = self.get_current_time()
        micro_ver = data_json.get('micro_ver')
        doc_id = data_json.get('doc_id')
        commit_user = data_json.get('commit_user')
        content = data_json.get('content')
        if not doc_id:
            return False, '未指定文档ID!'
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        old_micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        flag, error = self.diff_ver(micro_ver, old_micro_ver)
        if not flag:
            return 0, error
        commit_list = []
        old_data_list = self.get_old_data(DSRelTag, DSRelTag.doc_id, doc_id)
        old_tag_list = []
        del_data_list = []
        for old_data in old_data_list:
            tag_id = old_data.get('tag_id')
            if tag_id not in old_tag_list:
                old_tag_list.append(tag_id)
            if tag_id not in content:
                del_data_list.append(old_data)
                commit_list += self.del_scene_considers(old_data.get('gid'))  # 刪除已刪除場景下的考慮點
        add_data_list = []
        for tag_id in content:
            new_data = {'doc_id': doc_id, 'tag_id': tag_id, 'before_change': None,
                        'change': None, 'before_influence': None, 'influence': None,
                        'order_id': 1}
            if tag_id not in old_tag_list:
                add_data_list.append(new_data)
        try:
            commit_list += self.add_list(DSRelTag, [], del_data_list, DSRelTag.gid, [])
            commit_list += self.add_list(DSRelTag, add_data_list, [], DSRelTag.gid, [])
            if commit_list:
                log_doc = CtrlDsDoc().update_ver(doc_id, commit_user)
                commit_list.append(log_doc)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return doc_id, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return 0, "服务异常！请联系管理员！"

    def del_scene_considers(self, change_id):
        old_data_list = self.get_old_data(DSRelModel, DSRelModel.change_id, change_id)
        commit_list = self.add_list(DSRelModel, [], old_data_list, DSRelModel.gid, [])
        return commit_list

    def del_rel_tag(self, doc_id):
        commit_list = []
        old_data_list = self.get_old_data(DSRelTag, DSRelTag.doc_id, doc_id)
        for old_data in old_data_list:
            commit_list += self.del_scene_considers(old_data.get('gid'))
        commit_list += self.add_list(DSRelTag, [], old_data_list, DSRelTag.gid, [])
        return commit_list

    def get_new_scene_list(self, scenes, doc_id, sec_id):
        scene_list = []
        for scene in scenes:
            if type(scene) == dict:
                scene_dict = dict()
                old_data = self.get_scene_gid(doc_id, sec_id, scene.get('scene_id'))
                scene_dict[DSRelScene.gid.name] = scene.get('gid')
                if old_data:
                    scene_dict[DSRelScene.gid.name] = old_data.get('gid')
                scene_dict[DSRelScene.sec_id.name] = sec_id
                scene_dict[DSRelScene.doc_id.name] = doc_id
                scene_dict[DSRelScene.scene_id.name] = scene.get('scene_id')
                scene_dict[DSRelScene.change.name] = scene.get('change')
                scene_dict[DSRelScene.alter.name] = scene.get('alter')
                scene_list.append(scene_dict)
            else:
                scene_dict = {'gid': None, 'sec_id': sec_id, 'doc_id': doc_id,
                              'scene_id': scene, 'change': None, 'alter': None}
                old_data = self.get_scene_gid(doc_id, sec_id, scene)
                if old_data:
                    scene_dict['gid'] = old_data.get('gid')
                    scene_dict['change'] = old_data.get('change')
                    scene_dict['alter'] = old_data.get('alter')
                scene_list.append(scene_dict)
        return scene_list

    def get_scene_gid(self, doc_id, sec_id, scene_id):
        q = (db.session.query(DSRelScene)
             .filter(and_(DSRelScene.doc_id == doc_id,
                          DSRelScene.sec_id == sec_id,
                          DSRelScene.scene_id == scene_id)).first())
        if q:
            return q.to_dict()
        else:
            return None

    def delete_scene_drbfm(self, sec_id, new_scene_list, old_scene_list):
        """
        删除已删除场景的drbfm
        :param sec_id:
        :param new_scene_list:
        :param old_scene_list:
        :return: drbfm的log
        """
        from app.db.ds_drbfm import DSDrbfm
        new_scene_id = []
        log_list = []
        for new_scene in new_scene_list:
            if type(new_scene) == dict:
                new_scene_id.append(new_scene.get("scene_id"))
            else:
                new_scene_id.append(new_scene)
        for old_scene in old_scene_list:
            scene_id = old_scene.get('scene_id')
            if scene_id not in new_scene_id:
                q = (db.session.query(DSDrbfm).filter(and_(DSDrbfm.sec_id == sec_id,
                     DSDrbfm.scene_id == scene_id)))
                old_data = []
                for drbfm in q:
                    old_data.append(drbfm.to_dict())
                log_list += self.add_list(DSDrbfm, [], old_data, DSDrbfm.gid, [DSDrbfm.drbfm_content.name])
        return log_list

    def delete_by_sec_id(self, sec_id):
        scene_q = db.session.query(DSRelScene).filter(DSRelScene.sec_id == sec_id)
        old_data_list = []
        new_data_list = []
        for scene in scene_q:
            old_data_list.append(scene.to_dict())
        commit_list = self.add_list(self.db_object, new_data_list, old_data_list,
                                    self.key_col, self.col_list)
        return commit_list

    def get(self, sec_id, sec_type=None, condition=None):
        return self.get_scene_by_doc(sec_id), None

    def get_scene2(self):
        scene_dict = {}
        q = db.session.query(DSScene)
        for scene in q:
            scene_dict[scene.scene_id] = scene.to_dict()
        return scene_dict

    def get_scene3(self):
        """新场景直接使用 技术专题 下的子TAG
        :return:
        """
        return CtrlDocTag().get_tag_for_scense()

    def get_scene_df(self):
        q = db.session.query(DSScene)
        sqlcmd = q.statement
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        return df

    def get_scene_tag(self, sec_id):
        """
        根据sec_id获取场景关联的tag
        :param sec_id:
        :return:
        """
        q = (db.session.query(DSSceneTag.tag_id)
             .outerjoin(DSScene, DSSceneTag.scene_id == DSScene.scene_id)
             .outerjoin(DSRelScene, DSScene.scene_id == DSRelScene.scene_id)
             .filter(DSRelScene.sec_id == sec_id))
        tag_id_list = []
        for tag in q:
            tag_id_list.append(tag[0])
        return tag_id_list

    def get_tags_by_doc_id(self, doc_id):
        sqlcmd = """
        SELECT a.tag_id, tag,
               a.gid as change_id, before_change, change,
               before_influence, influence, order_id,
               change_type, b.model_id, title as model_name,
               checked, failure_id_list, result
          FROM ds.ds_rel_tag as a
          left join ds.ds_rel_model as  b
          on a.gid = b.change_id
          left join ds.model as c
          on b.model_id = c.model_id
          left join public.doc_tag_category as d
          on a.tag_id = d.tag_id
          where a.doc_id = {doc_id}
          order by tag_id, order_id
        """.format(doc_id=doc_id)
        df = pd.read_sql(sqlcmd, db.session.bind)
        tag_ids = df["tag_id"].unique()
        tag_list = []
        for tag_id in tag_ids:
            sub_df = df[df["tag_id"] == tag_id]
            s = sub_df.iloc[0]
            tag_info = dict()
            tag_info["tag_id"] = int(tag_id)
            tag_info["tag"] = s["tag"]
            change_list = self._convert_change(sub_df, doc_id)
            tag_info["change_list"] = change_list
            tag_info["work_status"], tag_info["completion"] = self.get_work_status(change_list)
            tag_list.append(tag_info)
        return tag_list

    def get_work_status(self, change_list):
        """判断场景确认状态"""
        work_status = True
        length = len(change_list)
        completion = 0
        for change in change_list:
            model_list = change.get('model_list')
            if not model_list:
                work_status = False
            for model in model_list:
                if not model.get('checked'):
                    work_status = False
                else:
                    completion += (1/len(model_list))*(1/length)
        completion = "%.0f%%" % (completion * 100)
        return work_status, completion

    def _convert_change(self, df, doc_id):
        change_list = []
        change_ids = df["change_id"].unique()
        for change_id in change_ids:
            sub_df = df[df["change_id"] == change_id]
            s = sub_df.iloc[0]
            # ## 修改点
            before_change, change = s["before_change"], s["change"]
            if before_change == u"同上" and change == "同上":
                pass
            else:
                change_info = dict()
                change_info["change_id"] = int(change_id)
                change_info["before_change"] = before_change
                change_info["change"] = change
                change_info["change_type"] = 'change'
                change_df = sub_df[sub_df["change_type"] == 'change']  # 修改
                # 本模块
                curr_model = self._get_curr_model(doc_id, change_df)
                change_info["model_info"] = curr_model
                # ## 关联模块信息
                # curr_model_id = curr_model.get("model_id")
                # change_df = change_df[~change_df["model_id"].isin([curr_model_id])]  # 去掉本模块
                model_list = self._convert_models_for_change(change_df)
                change_info["model_list"] = model_list
                change_list.append(change_info)
            # 影响点
            before_influence, influence = s["before_influence"], s["influence"]
            if before_influence == u"同上" and influence == "同上":
                pass
            else:
                # 影响
                influence_info = dict()
                influence_info["change_id"] = int(change_id)
                influence_info["before_change"] = before_influence
                influence_info["change"] = influence
                influence_info["change_type"] = 'influence'
                influence_df = sub_df[sub_df["change_type"] == 'influence']
                # print(sub_df)
                # print(influence_df)
                # 本模块
                curr_model = self._get_curr_model(doc_id, influence_df)
                influence_info["model_info"] = curr_model
                # curr_model_id = curr_model.get("model_id")
                # ## 关联模块信息
                # influence_df = influence_df[~influence_df["model_id"].isin([curr_model_id])]  # 去掉本模块
                model_list = self._convert_models_for_change(influence_df)
                influence_info["model_list"] = model_list
                change_list.append(influence_info)
        return change_list

    def _get_curr_model(self, doc_id, df):
        model_info = self._get_model(doc_id)
        curr_model_id = model_info.get("model_id")
        curr_df = df[df["model_id"] == curr_model_id]
        if curr_df.empty:
            return model_info
        else:
            model_list = self._convert_models_for_change(curr_df)
            return model_list[0]

    def _get_model(self, doc_id):
        from app.db.ds_doc import Ds_Doc
        from app.db.model import Model
        q = (db.session.query(Model)
             .outerjoin(Ds_Doc, Model.model_id == Ds_Doc.model_id)
             .filter(Ds_Doc.doc_id == doc_id))
        model = q.first()
        model_info = {"model_id": model.model_id,
                      "model_name": model.title,
                      "checked": False,
                      "failure_id_list": []}
        return model_info

    def _convert_models_for_change(self, df):
        df = df.dropna(subset=["model_id"])
        df = df[["model_id", "model_name", "checked", "failure_id_list", "result"]]
        model_list = []
        for model_info in df.to_dict(orient='records'):
            failure_id_list = model_info["failure_id_list"]
            if failure_id_list:
                # model_info["failure_id_list"] = [int(s) for s in failure_id_list.split('|')]
                model_info["failure_id_list"] = json.loads(failure_id_list)
            else:
                model_info["failure_id_list"] = {'havething_list': [], 'nothing_list': []}
            model_list.append(model_info)
        return model_list

    def add_tag_considers(self, data_json):
        """
        给场景选择影响模块
        :param data_json:
        :return:
        """
        from app.ctrl.ctrl_ds_doc import CtrlDsDoc
        update_time = self.get_current_time()
        micro_ver = data_json.get('micro_ver')
        doc_id = data_json.get('doc_id')
        commit_user = data_json.get('commit_user')
        content = data_json.get('consider')
        if not doc_id:
            return False, '未指定文档ID!'
        doc_data, error = CtrlDsDoc().ds_doc_exist(doc_id)
        if error:
            return False, error
        old_micro_ver = CtrlDsDoc().get_doc_ver(doc_id)
        flag, error = self.diff_ver(micro_ver, old_micro_ver)
        if not flag:
            return 0, error
        new_data_list = []
        old_data_list = []
        for data in content:
            if not data:
                continue
            change_list = data[0].get('change_list')
            new_data, old_data = self.get_new_tag_consider(change_list)
            new_data_list += new_data
            old_data_list += old_data
        for new_data in new_data_list:
            for old_data in old_data_list:
                if (new_data.get('change_id') == old_data.get('change_id')
                    and new_data.get('change_type') == old_data.get('change_type')
                        and new_data.get('model_id') == old_data.get('model_id')):
                    new_data['gid'] = old_data.get('gid')
                    break
        commit_list = self.add_list(DSRelModel, new_data_list, old_data_list, DSRelModel.gid,
                                    [DSRelModel.checked.name, DSRelModel.failure_id_list.name,
                                     DSRelModel.result.name])
        self.commit_log(commit_list, commit_user, update_time)
        db.session.commit()
        return doc_id, None

    def get_new_tag_consider(self, change_list):
        new_data_list = []
        old_data_list = []
        for change in change_list:
            change_id = change.get('change_id')
            change_type = change.get('change_type')
            old_data_list += self.get_old_data(DSRelModel, [DSRelModel.change_id, DSRelModel.change_type],
                                               {'change_id': change_id, 'change_type': change_type})
            # model_info = change.get('model_info')
            # failure_id_list = model_info.get('failure_id_list')
            # failure_id_list = '|'.join(map(str, failure_id_list))
            # model_id = model_info.get('model_id')
            # my_modle = {'change_id': change_id, 'change_type': change_type,
            #             'model_id': model_info.get('model_id'), 'checked': model_info.get('checked'),
            #             'failure_id_list': failure_id_list}
            model_list = change.get('model_list')
            if model_list:
                for model in model_list:
                    failure_id_list = model.get('failure_id_list')
                    failure_id_list = json.dumps(failure_id_list, ensure_ascii=False)
                    # failure_id_list = '|'.join(map(str, failure_id_list))
                    new_data = {'change_id': change_id, 'change_type': change_type,
                                'model_id': model.get('model_id'), 'checked': model.get('checked'),
                                'failure_id_list': failure_id_list, 'result': model.get('result')}
                    new_data_list.append(new_data)
        return new_data_list, old_data_list

    def get_db_for_journal(self, doc_id):
        """
        #根据doc_id获取drbfm的相关信息
        :param doc_id:
        :return:
        """
        q = (db.session.query(DSRelTag).filter(DSRelTag.doc_id == doc_id)
             .order_by(DSRelTag.gid))
        scene_list = q.all()
        consider_list = []
        for scene in scene_list:
            change_id = scene.gid
            query = db.session.query(DSRelModel).filter(DSRelModel.change_id == change_id)
            consider_list += query.all()
        return scene_list+consider_list


