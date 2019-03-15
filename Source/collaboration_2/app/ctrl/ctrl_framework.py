# -*- coding: UTF-8 -*-
import json
from flask import current_app
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_base import CtrlBase
from app.db.framework import Framework
from app.db.framework import FrameworkModel
from app.db.framework import FrameworkModelRel
from app.db.project import ProjectFW
from app.db.model import Model
from app.ctrl.ctrl_project import CtrlProject


class CtrlFramework(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Framework.fw_id
        self.db_object = Framework
        self.col_list = [Framework.manager.name, Framework.summary.name,
                         Framework.content.name, Framework.fw_name.name]

    def get(self, fw_id):
        q = db.session.query(Framework)
        if fw_id:
            q = q.filter(Framework.fw_id == fw_id)
        q = q.order_by(Framework.fw_id)
        framework_list = []
        for fw in q:
            framework_list.append(fw.to_dict())
        return framework_list

    def get_fw_project(self, fw_id):
        project_list = CtrlProject().get_proj_by_fw(fw_id)
        return project_list

    def add(self, data_json):
        if 'type' in data_json:
            data_json.pop('type')
        try:
            fw_id = data_json.get('fw_id')
            update_time = self.get_current_time()
            commit_list = []
            log_dict = self.add_framework(data_json)
            if log_dict:
                commit_list.append(log_dict)
            self.commit_log(commit_list, data_json.get('manager'), update_time)
            db.session.commit()
            return fw_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def add_framework(self, new_framework):
        old_framework = None
        fw_id = new_framework.get('fw_id')
        old_data = self.get_old_data(self.db_object, self.key_col, fw_id)
        if old_data:
            old_framework = old_data[0]
        log_dict = self.common_add(self.db_object, new_framework, old_framework,
                                   self.col_list, self.key_col)
        return log_dict

    def delete(self, fw_id, commit_user):
        try:
            commit_list = []
            update_time = self.get_current_time()
            q = db.session.query(ProjectFW).filter(ProjectFW.fw_id == fw_id).all()
            if q:
                return False, "该平台下还有项目无法删除！"
            fm_rel_q = db.session.query(FrameworkModelRel).filter(FrameworkModelRel.fw_id == fw_id)
            fm_rel_list = self.db_query_to_list(fm_rel_q)
            commit_list += self.add_list(FrameworkModelRel, [], fm_rel_list, FrameworkModelRel.gid, [])
            fm_q = db.session.query(FrameworkModel).filter(FrameworkModel.fw_id == fw_id)
            fm_list = self.db_query_to_list(fm_q)
            commit_list += self.add_list(FrameworkModel, [], fm_list, FrameworkModel.gid, [])
            fw_q = db.session.query(Framework).filter(Framework.fw_id == fw_id)
            fw_list = self.db_query_to_list(fw_q)
            commit_list += self.add_list(Framework, [], fw_list, Framework.fw_id, [])
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            from app.db import cache
            cache.delete('get_model_tree')  # 删除缓存
            return True, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_fw_byname(self, fw_name):
        q = db.session.query(Framework)
        fw_list = []
        if fw_name:
            q = q.filter(Framework.fw_name.ilike(fw_name))
            for fw in q:
                fw_info = fw.to_dict()
                fw_list.append(fw_info)
        return fw_list

    def get_cactus_fw(self, accessToken, manager):
        from app.ctrl.ctrl_project import CtrlProject
        cactus_fw_list = []
        fw_list = self.get_fw_by_manager(manager)
        fw_ids = []
        for fw in fw_list:
            fw_ids.append(fw.get('fw_id'))
        cactus_list = CtrlProject().get_project_from_cactus(accessToken)
        for cactus in cactus_list:
            if manager == cactus.get('manager'):
                fw_id = cactus.get('fw_id')
                if fw_id not in fw_ids:
                    framework_json = {'fw_id': fw_id,
                                      'fw_name': cactus.get('fw_name'),
                                      'manager': manager
                                      }
                    cactus_fw_list.append(framework_json)
        return cactus_fw_list

    def get_fw_by_manager(self, manager):
        q = db.session.query(Framework).filter(Framework.manager == manager)
        fw_list = []
        for fw in q:
            fw_list.append(fw.to_dict())
        return fw_list


class CtrlFwModel(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)

    def add(self, data_json):
        fw_id = data_json.get(Framework.fw_id.name)
        user_name = data_json.get('user_name')
        update_time = self.get_current_time()
        model_tree = data_json.get('model_tree')
        try:
            model_rel_q = db.session.query(FrameworkModelRel).filter(FrameworkModelRel.fw_id == fw_id)
            model_q = db.session.query(FrameworkModel).filter(FrameworkModel.fw_id == fw_id)
            old_model, old_modle_rel = [], []
            for model in model_q:
                old_model.append(model.to_dict())
            for model_rel in model_rel_q:
                old_modle_rel.append(model_rel.to_dict())
            parent_model_id = 0  # 树的顶端设为0
            model_sub = model_tree[0].get('model_sub')
            model_list, model_rel_list = [], []
            self.add_fw_model(fw_id, model_sub, parent_model_id,
                              model_list, model_rel_list)
            commit_list = self.add_list(FrameworkModel, model_list, old_model, FrameworkModel.gid, [])
            commit_list += self.add_list(FrameworkModelRel, model_rel_list, old_modle_rel,
                                         FrameworkModelRel.gid, [])
            self.commit_log(commit_list, user_name, update_time)
            db.session.commit()
            return fw_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def add_fw_model(self, fw_id, model_sub, parent_model_id,
                     model_list, model_rel_list):
        for model in model_sub:
            model_id = model.get(FrameworkModel.model_id.name)
            fm = {FrameworkModel.fw_id.name: fw_id, FrameworkModel.model_id.name: model_id}
            q = db.session.query(FrameworkModel).filter(and_(FrameworkModel.fw_id == fw_id,
                                                        FrameworkModel.model_id == model_id)).first()
            if q:  # 检查是否已存在该模块
                fm['gid'] = q.gid
            if fm not in model_list:
                model_list.append(fm)
            if parent_model_id:
                fm_rel = {FrameworkModelRel.model_id.name: model_id,
                          FrameworkModelRel.fw_id.name: fw_id,
                          FrameworkModelRel.parent_model_id.name: parent_model_id}
                q = (db.session.query(FrameworkModelRel)
                     .filter(and_(FrameworkModelRel.fw_id == fw_id,
                             FrameworkModelRel.model_id == model_id,
                             FrameworkModelRel.parent_model_id == parent_model_id)).first())
                if q:
                    fm_rel['gid'] = q.gid
                if fm_rel not in model_rel_list:
                    model_rel_list.append(fm_rel)
            if model.get('model_sub'):
                self.add_fw_model(fw_id, model.get('model_sub'), model_id,
                                  model_list, model_rel_list)

    def get(self, fw_id):
        fw = db.session.query(Framework).filter(Framework.fw_id == fw_id).first()
        fw_name = fw.fw_name
        fm_q = (db.session.query(Model)
                .outerjoin(FrameworkModel, Model.model_id == FrameworkModel.model_id)
                .filter(FrameworkModel.fw_id == fw_id).order_by(Model.model_id).all())
        fm_rel_q = (db.session.query(Model)
                    .outerjoin(FrameworkModelRel, Model.model_id == FrameworkModelRel.model_id)
                    .filter(FrameworkModelRel.fw_id == fw_id).order_by(Model.model_id).all())
        fm_model_ids = []
        for fm_rel in fm_rel_q:
            fm_model_ids.append(fm_rel.model_id)
        model_tree = []
        tree_top = {"model_id": fw_id, "title": fw_name, "key": False, "model_sub": []}
        for fm in fm_q:
            if fm.model_id not in fm_model_ids:
                model = fm.to_dict()
                # model[Framework.fw_id.name] = fw_id
                # model[Framework.fw_name.name] = fw_name
                model["key"] = False
                model["model_sub"] = []
                self.get_model_sub(model, fw_id, fw_name)
                model_tree.append(model)
        tree_top['model_sub'] = model_tree
        model_dict = {'fw_id': fw_id, 'fw_name': fw_name, 'model_tree': []}
        model_dict['model_tree'].append(tree_top)
        return model_dict

    def get_model_sub(self, model, fw_id, fw_name):
        """
        通过父模块找子模块
        :param model:
        :param fw_id:
        :param fw_name:
        :return:
        """
        model_id = model.get("model_id")
        model_sub_q = (db.session.query(Model)
                       .outerjoin(FrameworkModelRel, Model.model_id == FrameworkModelRel.model_id)
                       .filter(and_(FrameworkModelRel.fw_id == fw_id,
                                    FrameworkModelRel.parent_model_id == model_id)).all())
        if len(model_sub_q):
            for sub in model_sub_q:
                model_sub = sub.to_dict()
                # model_sub[Framework.fw_id.name] = fw_id
                # model_sub[Framework.fw_name.name] = fw_name
                model_sub["key"] = False
                model_sub["model_sub"] = []
                self.get_model_sub(model_sub, fw_id, fw_name)
                model["model_sub"].append(model_sub)

    def get_fw_model(self, fw_id):
        """
        获取平台下的模块以及模块的父子关系
        :param fw_id:
        :return:
        """
        model_list = []
        model_rel_list = []
        model_q = db.session.query(FrameworkModel).filter(FrameworkModel.fw_id == fw_id)
        model_rel_q = db.session.query(FrameworkModelRel).filter(FrameworkModelRel.fw_id == fw_id)
        for model in model_q:
            model_dict = model.to_dict()
            model_dict.pop(FrameworkModel.gid.name)
            model_list.append(model_dict)
        for model_rel in model_rel_q:
            model_rel_dict = model_rel.to_dict()
            model_rel_dict.pop(FrameworkModelRel.gid.name)
            model_rel_list.append(model_rel_dict)
        return model_list, model_rel_list

    def delete(self, fw_id):
        db.session.query(FrameworkModelRel).filter(
            FrameworkModelRel.fw_id == fw_id).delete()
        db.session.query(FrameworkModel).filter(
            FrameworkModel.fw_id == fw_id).delete()










