# -*- coding: UTF-8 -*-
import copy
import pandas as pd
from flask import current_app
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_base import CtrlBase
from app.db.model import Model
from app.db.project import Project, ProjectTag, ProjectFW
from app.db.project import ProjectModel, ProjectModelRel, ProjectModelRef
from app.db.framework import Framework
from app.db.doc_tag_cat import DBDocTagCat
from app.db.ds_model_tag_rel import DsModelTagRel
from app.db.group import GroupModel
from app.db.group import Group
from app.db.ds_doc import Ds_Doc


class CtrlProject(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Project.proj_id
        self.db_object = Project
        self.col_list = [Project.proj_name.name, Project.summary.name, Project.proj_tag_id.name]

    def add(self, data):
        proj_id = data.get('proj_id')
        update_time = self.get_current_time()
        fw_id = data.get('fw_id')
        try:
            commit_list = []
            project_json = {'proj_id': proj_id,
                            'proj_name': data.get('proj_name'),
                            'manager': data.get('proj_manager'),
                            'summary': data.get('summary'),
                            'ver': data.get('ver'),
                            'proj_tag_id': data.get('proj_tag_id'),
                            'update_time': update_time
                            }
            projects = self.get_old_data(self.db_object, self.key_col, proj_id)
            if not projects:
                project_json['create_time'] = update_time
            log_dict = self.add_project(project_json)
            if log_dict:
                commit_list.append(log_dict)
            from app.ctrl.ctrl_framework import CtrlFramework
            frameworks = self.get_old_data(Framework, Framework.fw_id, fw_id)
            if not frameworks:
                return False, "请先创建平台“%s”" % data.get('fw_name')
                # framework_json = {'fw_id': fw_id,
                #                   'fw_name': data.get('fw_name'),
                #                   'manager': data.get('fw_manager'),
                #                   'content': None,
                #                   'summary': None
                #                   }
                # log_dict = CtrlFramework().add_framework(framework_json)
                # if log_dict:
                #     commit_list.append(log_dict)
            if fw_id:
                log_dict = self.add_fw_project(fw_id, proj_id)
                if log_dict:
                    commit_list.append(log_dict)
                    pro_fw = {'fw_id': fw_id, 'proj_id': proj_id}
                    commit_list += self.copy_fw_model(pro_fw)
            self.commit_log(commit_list, data.get('proj_manager'), update_time)
            db.session.commit()
            return proj_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def add_project(self, new_project):
        proj_id = new_project.get('proj_id')
        old_project = None
        old_data = self.get_old_data(self.db_object, self.key_col, proj_id)
        if old_data:
            old_project = old_data[0]
        log_dict = self.common_add(self.db_object, new_project, old_project, self.col_list,
                                   self.key_col)
        return log_dict

    def add_fw_project(self, fw_id, proj_id):
        new_data = {'gid': None, 'proj_id': proj_id, 'fw_id': fw_id}
        old_data = None
        q = db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id).first()
        if q:
            old_data = q.to_dict()
            new_data['gid'] = old_data.get('gid')
        log_dict = self.common_add(ProjectFW, new_data, old_data, [ProjectFW.fw_id], ProjectFW.gid)
        return log_dict

    def update(self, proj_id, data):
        proj_name = data.get("proj_name")
        if proj_name:
            try:
                db.session.query(Project).filter(Project.proj_id == proj_id).update(data)
                db.session.commit()
                return proj_id, 'OK'
            except Exception as e:
                db.session.rollback()
                current_app.logger.error('%s' % str(e))
                return False, str(e)
        else:
            return False, u'未指定项目名称'

    def update_editor(self, username, proj_id):
        """
        更新编辑时间
        :param username:
        :param proj_id:
        :return:
        """
        if username:
            proj = db.session.query(Project).filter(Project.proj_id == proj_id).first()
            update_time = self.get_current_time()
            if proj:
                # proj.editor = username
                proj.update_time = update_time

    def get_project_from_cactus(self, accessToken):
        """
        从cactus上拿项目信息
        :param accessToken:
        :return:
        """
        cactus_project_list = []
        from app.api_1_0.api_cactus import ApiCactus
        result = ApiCactus().cactus_project(accessToken)
        if result.get('code') == 0:
            pro_list = result.get('list')
            for pro in pro_list:
                project_dict = dict()
                project_dict['project_list'] = []
                minor_projects = pro.get('minorProjects')
                project_dict['fw_id'] = pro.get('majorProjectId')
                project_dict['fw_name'] = pro.get('name')
                project_dict['manager'] = pro.get('ownerName')
                for minor_project in minor_projects:
                    minor_project_dict = dict()
                    minor_project_dict['proj_id'] = minor_project.get('minorProjectId')
                    minor_project_dict['proj_name'] = minor_project.get('name')
                    minor_project_dict['manager'] = minor_project['owner'].get('userName')
                    minor_project_dict['create_time'] = minor_project['startDate']
                    project_dict['project_list'].append(minor_project_dict)
                cactus_project_list.append(project_dict)
        return cactus_project_list

    def get_project_by_manager(self, manager):
        q = db.session.query(Project).filter(Project.manager == manager)
        project_list = []
        for proj in q:
            project_list.append(proj.to_dict())
        return project_list

    def get_cactus_project(self, accessToken, manager):
        """
        获取cactus上的项目
        :param accessToken:
        :return:
        """
        project_list = self.get_project_by_manager(manager)
        proj_ids = []
        for proj in project_list:
            proj_ids.append(proj.get('proj_id'))
        result_list = []
        cactus_project_list = self.get_project_from_cactus(accessToken)
        for cactus_project in cactus_project_list:
            framework_json = {'fw_id': cactus_project.get('fw_id'),
                              'fw_name': cactus_project.get('fw_name'),
                              'fw_manager': cactus_project.get('manager')
                              }
            project_list = cactus_project.get('project_list')
            for project in project_list:
                if manager == project.get('manager'):
                    proj_id = project.get('proj_id')
                    if proj_id not in proj_ids:
                        project_json = {
                            'proj_id': proj_id,
                            'proj_name': project.get('proj_name'),
                            'proj_manager': project.get('manager'),
                        }
                        project_json.update(framework_json)
                        result_list.append(project_json)
        return result_list

    def synchronize_project(self, accessToken):
        """
        同步cactus与idsign的项目信息
        :param cactus_project_list:
        :return:
        """
        try:
            from app.ctrl.ctrl_framework import CtrlFramework
            cactus_project_list = self.get_project_from_cactus(accessToken)
            for cactus_project in cactus_project_list:
                framework_json = {'fw_id': cactus_project.get('fw_id'),
                                  'fw_name': cactus_project.get('fw_name'),
                                  'manager': cactus_project.get('manager')
                                  }
                project_list = cactus_project.get('project_list')
                fw_id = framework_json['fw_id']
                frameworks = self.get_old_data(Framework, Framework.fw_id, fw_id)
                if frameworks:
                    old_framework = frameworks[0]
                    new_framework = copy.deepcopy(old_framework)
                    new_framework.update(framework_json)
                else:
                    old_framework = None
                    new_framework = framework_json
                self.common_add(Framework, new_framework, old_framework,
                                CtrlFramework().col_list, CtrlFramework().key_col)
                for project in project_list:
                    project_json = {
                                    'proj_id': project.get('proj_id'),
                                    'proj_name': project.get('proj_name'),
                                    # 'summary': project.get('summary'),
                                    'manager': project.get('manager'),
                                    'create_time': project.get('create_time')
                                    }
                    proj_id = project_json.get('proj_id')
                    projects = self.get_old_data(self.db_object, self.key_col, proj_id)
                    if projects:
                        old_project = projects[0]
                        new_project = copy.deepcopy(project_json)
                        new_project.update(project_json)
                    else:
                        old_project = None
                        new_project = project_json
                    self.common_add(self.db_object, new_project, old_project, self.col_list,
                                    self.key_col)
                    pf_q = db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id).first()
                    if pf_q:
                        pf_q.fw_id = fw_id
                    else:
                        project_fw = {'proj_id': proj_id, 'fw_id': fw_id}
                        db.session.add(ProjectFW(**project_fw))
            db.session.commit()
            return None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return "服务异常！请联系管理员！"

    def get(self, proj_id, page=None, size=None, condition=None, manager=None,):
        q = (db.session.query(Project.proj_id, Project.proj_name, Project.summary,
             Project.manager, Project.ver, Framework.fw_id, Framework.fw_name, Project.proj_tag_id)
             .outerjoin(ProjectFW, Project.proj_id == ProjectFW.proj_id)
             .outerjoin(Framework, ProjectFW.fw_id == Framework.fw_id))
        if manager:
            q = q.filter(Project.manager == manager)
        if proj_id:
            q = q.filter(Project.proj_id == proj_id)
        elif condition:
            q = q.filter(Project.proj_name.like('%'+condition+'%'))
        q = q.order_by(Project.proj_id)
        count = None
        if page and size:
            count = q.count()
            q = q.limit(size).offset(size * (page - 1))
        proj_list = []
        for proj in q:
            project = dict()
            project[Project.proj_id.name] = proj[0]
            project[Project.proj_name.name] = proj[1]
            project[Project.summary.name] = proj[2]
            project[Project.manager.name] = proj[3]
            project[Project.ver.name] = proj[4]
            project[Framework.fw_id.name] = proj[5]
            project[Framework.fw_name.name] = proj[6]
            project[Project.proj_tag_id.name] = proj[7]
            proj_list.append(project)
        return count, proj_list

    def delete(self, proj_id, commit_user):
        try:
            update_time = self.get_current_time()
            commit_list = []
            from app.ctrl.ctrl_ds_doc import CtrlDsDoc
            ctrl_obj = CtrlDsDoc()
            querys = db.session.query(Ds_Doc).filter(Ds_Doc.proj_id == proj_id).all()
            for q in querys:
                doc_id = q.doc_id
                commit_list += ctrl_obj.delete(doc_id, commit_user, commit=False)
            gm_q = db.session.query(GroupModel).filter(GroupModel.proj_id == proj_id)
            gm_list = self.db_query_to_list(gm_q)
            commit_list += self.add_list(GroupModel, [], gm_list, GroupModel.gid, [])
            pm_q = db.session.query(ProjectModel).filter(ProjectModel.proj_id == proj_id)
            pm_list = self.db_query_to_list(pm_q)
            commit_list += self.add_list(ProjectModel, [], pm_list, ProjectModel.gid, [])
            pm_rel_q = db.session.query(ProjectModelRel).filter(ProjectModelRel.proj_id == proj_id)
            pm_rel_list = self.db_query_to_list(pm_rel_q)
            commit_list += self.add_list(ProjectModelRel, [], pm_rel_list, ProjectModelRel.gid, [])
            pm_ref_q = db.session.query(ProjectModelRef).filter(ProjectModelRef.proj_id == proj_id)
            pm_ref_list = self.db_query_to_list(pm_ref_q)
            commit_list += self.add_list(ProjectModelRef, [], pm_ref_list, ProjectModelRef.gid, [])
            mt_q = db.session.query(DsModelTagRel).filter(DsModelTagRel.proj_id == proj_id)
            mt_list = self.db_query_to_list(mt_q)
            commit_list += self.add_list(DsModelTagRel, [], mt_list, DsModelTagRel.gid, [])
            pt_q = db.session.query(ProjectTag).filter(ProjectTag.proj_id == proj_id)
            pt_list = self.db_query_to_list(pt_q)
            commit_list += self.add_list(ProjectTag, [], pt_list, ProjectTag.gid, [])
            pf_q = db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id)
            pf_list = self.db_query_to_list(pf_q)
            commit_list += self.add_list(ProjectFW, [], pf_list, ProjectFW.gid, [])
            pj_q = db.session.query(Project).filter(Project.proj_id == proj_id)
            pj_list = self.db_query_to_list(pj_q)
            commit_list += self.add_list(self.db_object, [], pj_list, self.key_col, self.col_list)
            self.commit_log(commit_list, commit_user, update_time)
            db.session.commit()
            return True, 'OK'
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, str(e)

    def add_proj_fw(self, data):
        """
        由于给平台项目从cactus拿,IDESIGN就
        没有给项目选平台的操作了:2018/7/30
        :param data:
        :return:
        """
        proj_id = int(data.get("proj_id"))
        try:
            user_name = None
            if "user_name" in data:
                user_name = data.get("user_name")
                data.pop("user_name")
            pro_fw_q = db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id).first()
            if pro_fw_q:
                if pro_fw_q.fw_id == data.get('fw_id'):
                    return proj_id, 'OK'
                else:
                    db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id).update(data)
            else:
                projfw = ProjectFW(**data)
                db.session.add(projfw)
            self.update_editor(user_name, proj_id)
            self.copy_fw_model(data)
            db.session.commit()
            return proj_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def copy_fw_model(self, projfw):
        """
        复制平台模块
        :param projfw:
        :return:
        """
        commit_list = []
        from app.ctrl.ctrl_framework import CtrlFwModel
        fw_id = projfw.get("fw_id")
        proj_id = projfw.get("proj_id")
        model_list, model_rel_list = CtrlFwModel().get_fw_model(fw_id)
        for model in model_list:
            model_id = model.get("model_id")
            model.pop(ProjectFW.fw_id.name)
            model[ProjectModel.proj_id.name] = proj_id
            pro_model_q = (db.session.query(ProjectModel)
                           .filter(and_(ProjectModel.proj_id == proj_id,
                                   ProjectModel.model_id == model_id)).first())
            if not pro_model_q:
                log_dict = self.common_add(ProjectModel, model, None, [], ProjectModel.gid)
                if log_dict:
                    commit_list.append(log_dict)
        for model_rel in model_rel_list:
            model_id = model_rel.get("model_id")
            parent_model_id = model_rel.get('parent_model_id')
            model_rel.pop(ProjectFW.fw_id.name)
            model_rel[ProjectModelRel.proj_id.name] = proj_id
            pro_model_rel_q = (db.session.query(ProjectModelRel)
                               .filter(and_(ProjectModelRel.proj_id == proj_id,
                                            ProjectModelRel.model_id == model_id,
                                            ProjectModelRel.parent_model_id == parent_model_id)).first())
            if not pro_model_rel_q:
                log_dict = self.common_add(ProjectModelRel, model_rel, None, [], ProjectModelRel.gid)
                if log_dict:
                    commit_list.append(log_dict)
        return commit_list

    def get_proj_fw(self, proj_id):
        q = (db.session.query(Framework)
             .outerjoin(ProjectFW, Framework.fw_id == ProjectFW.fw_id)
             .filter(ProjectFW.proj_id == proj_id).first())
        fw_dict = dict()
        if q:
            fw_dict[Framework.fw_id.name] = q.fw_id
            fw_dict[Framework.fw_name.name] = q.fw_name
        return fw_dict

    def add_proj_tag(self, data):
        proj_id = data.get("proj_id")
        tag_list = data.get("tag_list")
        user_name = data.get("user_name")
        update_time = self.get_current_time()
        try:
            old_data_list = []
            q = db.session.query(ProjectTag).filter(ProjectTag.proj_id == proj_id)
            for pt in q:
                old_data_list.append(pt.to_dict())
            new_data_list = []
            for tag in tag_list:
                pro_tag = {"proj_id": proj_id, "tag_id": tag}
                for old_data in old_data_list:
                    if tag == old_data.get('tag_id'):
                        pro_tag['gid'] = old_data.get('gid')
                new_data_list.append(pro_tag)
            commit_list = self.add_list(ProjectTag, new_data_list, old_data_list, ProjectTag.gid, [])
            self.commit_log(commit_list, user_name, update_time)
            db.session.commit()
            return proj_id, False
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_proj_tag(self, proj_id):
        querys = db.session.query(DBDocTagCat).\
            outerjoin(ProjectTag, DBDocTagCat.tag_id == ProjectTag.tag_id)\
            .filter(ProjectTag.proj_id == proj_id)
        pro_tags = []
        for query in querys:
            # pro_tag = dict()
            # pro_tag['tag_id'] = query.tag_id
            # pro_tag['tag'] = query.tag
            pro_tags.append(query.tag_id)
        return pro_tags

    # def add_proj_model(self, data):
    #     proj_id = data.get("proj_id")
    #     model_list = data.get("model_list")
    #     user_name = data.get("user_name")
    #     try:
    #         db.session.query(ProjectModel).filter(ProjectModel.proj_id == proj_id).delete()
    #         for model in model_list:
    #             pro_tag = {"proj_id": proj_id, "model_id": model}
    #             db.session.add(ProjectModel(**pro_tag))
    #         self.update_editor(user_name, proj_id)
    #         db.session.commit()
    #         return proj_id, False
    #     except Exception as e:
    #         db.session.rollback()
    #         current_app.logger.error('%s' % str(e))
    #         return False, str(e)

    def add_proj_model(self, data_json):
        proj_id = int(data_json.get(Project.proj_id.name))
        user_name = data_json.get('user_name')
        update_time = self.get_current_time()
        model_tree = data_json.get('model_tree')
        try:
            model_rel_q = db.session.query(ProjectModelRel).filter(ProjectModelRel.proj_id == proj_id)
            model_q = db.session.query(ProjectModel).filter(ProjectModel.proj_id == proj_id)
            old_model, old_modle_rel = [], []
            for model in model_q:
                old_model.append(model.to_dict())
            for model_rel in model_rel_q:
                old_modle_rel.append(model_rel.to_dict())
            parent_model_id = 0  # 树的顶端设为0
            model_sub = model_tree[0].get('model_sub')
            model_list, model_rel_list = [], []
            self._add_proj_model_sub(proj_id, model_sub, parent_model_id,
                                     model_list, model_rel_list)
            commit_list = self.add_list(ProjectModel, model_list, old_model, ProjectModel.gid, [])
            commit_list += self.add_list(ProjectModelRel, model_rel_list, old_modle_rel,
                                         ProjectModelRel.gid, [])
            self.commit_log(commit_list, user_name, update_time)
            db.session.commit()
            return proj_id, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            return False, "服务异常！请联系管理员！"

    def _add_proj_model_sub(self, proj_id, model_sub, parent_model_id, model_list, model_rel_list):
        for model in model_sub:
            model_id = model.get(ProjectModel.model_id.name)
            pm = {ProjectModel.proj_id.name: proj_id, ProjectModel.model_id.name: model_id}
            q = db.session.query(ProjectModel).filter(and_(ProjectModel.proj_id == proj_id,
                                                           ProjectModel.model_id == model_id)).first()
            if q:
                pm['gid'] = q.gid
            if pm not in model_list:
                model_list.append(pm)
            if parent_model_id:
                pm_rel = {ProjectModelRel.model_id.name: model_id,
                          ProjectModelRel.proj_id.name: proj_id,
                          ProjectModelRel.parent_model_id.name: parent_model_id}
                q = (db.session.query(ProjectModelRel)
                     .filter(and_(ProjectModelRel.proj_id == proj_id,
                                  ProjectModelRel.model_id == model_id,
                                  ProjectModelRel.parent_model_id == parent_model_id)).first())
                if q:
                    pm_rel['gid'] = q.gid
                if pm_rel not in model_rel_list:
                    model_rel_list.append(pm_rel)
            if model.get('model_sub'):
                self._add_proj_model_sub(proj_id, model.get('model_sub'), model_id, model_list, model_rel_list)

    def get_proj_model(self, proj_id):
        pro = db.session.query(Project).filter(Project.proj_id == proj_id).first()
        proj_name = pro.proj_name
        q = db.session.query(ProjectFW).filter(ProjectFW.proj_id == proj_id).first()
        # self.copy_fw_model({'proj_id': proj_id, 'fw_id': q.fw_id})
        pro_q = (db.session.query(Model)
                 .outerjoin(ProjectModel, Model.model_id == ProjectModel.model_id)
                 .filter(ProjectModel.proj_id == proj_id).order_by(Model.model_id).all())
        pro_rel_q = (db.session.query(Model)
                     .outerjoin(ProjectModelRel, Model.model_id == ProjectModelRel.model_id)
                     .filter(ProjectModelRel.proj_id == proj_id).order_by(Model.model_id).all())
        pro_model_ids = []
        for pro_rel in pro_rel_q:
            pro_model_ids.append(pro_rel.model_id)
        model_tree = []
        tree_top = {"model_id": proj_id, "title": proj_name, "key": False, "model_sub": []}
        for pro in pro_q:
            if pro.model_id not in pro_model_ids:
                model = pro.to_dict()
                # model[Project.proj_id.name] = proj_id
                # model[Project.proj_name.name] = proj_name
                model["key"] = False
                model["model_sub"] = []
                self.get_model_sub(model, proj_id, proj_name)
                model_tree.append(model)
        tree_top['model_sub'] = model_tree
        model_dict = {'fw_id': proj_id, 'fw_name': proj_name, 'model_tree': []}
        model_dict['model_tree'].append(tree_top)
        return model_dict

    def get_model_sub(self, model, proj_id, proj_name):
        """
        通过父模块找子模块
        :param model:
        :param fw_id:
        :param fw_name:
        :return:
        """
        model_id = model.get("model_id")
        model_sub_q = (db.session.query(Model)
                       .outerjoin(ProjectModelRel, Model.model_id == ProjectModelRel.model_id)
                       .filter(and_(ProjectModelRel.proj_id == proj_id,
                                    ProjectModelRel.parent_model_id == model_id)).all())
        if len(model_sub_q):
            for sub in model_sub_q:
                model_sub = sub.to_dict()
                # model_sub[Project.proj_id.name] = proj_id
                # model_sub[Project.proj_name.name] = proj_name
                model_sub["key"] = False
                model_sub["model_sub"] = []
                self.get_model_sub(model_sub, proj_id, proj_name)
                model["model_sub"].append(model_sub)

    # def get_proj_model(self, proj_id):
    #     querys = db.session.query(ProjectModel).filter(ProjectModel.proj_id == proj_id)
    #     modle_ids = []
    #     for query in querys:
    #         # model = dict()
    #         # model['model_id'] = query.model_id
    #         modle_ids.append(query.model_id)
    #     return modle_ids

    def add_proj_group(self, data):
        user_name = data.get('user_name')
        proj_id = int(data.get('proj_id'))
        model_list = data.get('model_list')
        update_time = self.get_current_time()
        try:
            q = db.session.query(GroupModel).filter(GroupModel.proj_id == proj_id)
            old_gm_list = []
            for gm in q:
                old_gm_list.append(gm.to_dict())
            new_gm_list = []
            for model in model_list:
                model_id = model.get('model_id')
                group_list = model.get('group_list')
                for group_name in group_list:
                    # group_id = group.get('group_id')
                    group_model = {'proj_id': proj_id, 'model_id': model_id, 'group_name': group_name}
                    for old_gm in old_gm_list:
                        if model_id == old_gm.get('model_id') and group_name == old_gm.get('group_name'):
                            group_model['gid'] = old_gm.get('gid')
                    new_gm_list.append(group_model)
            commit_list = self.add_list(GroupModel, new_gm_list, old_gm_list, GroupModel.gid, [])
            self.commit_log(commit_list, user_name, update_time)
            db.session.commit()
            return proj_id, False
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_proj_group(self, proj_id):
        model_list = self.get_models(proj_id)
        id_index = dict()
        data_list = []
        for model in model_list:
            model_id = model.get('model_id')
            index = id_index.get(model_id)
            if index:
                data_list[index]['parent_title'] = data_list[index]['parent_title']+';'+model['parent_title']
                continue
            group_list = []
            groups = (db.session.query(GroupModel)
                      .filter(and_(GroupModel.proj_id == proj_id, GroupModel.model_id == model_id)))
            for group in groups:
                group_list.append(group.group_name)
            model["group_list"] = group_list
            data_list.append(model)
            id_index[model_id] = data_list.index(model)
        group_data = {"proj_id": proj_id, "model_list": data_list}
        return group_data

    def get_leaf_model(self, proj_id):
        """
        获取项目叶子模块
        :param proj_id:
        :return:
        """
        sqlcmd = """
        SELECT distinct t1.model_id, title from ds.model t1 
        left join ds.project_models t2 on t1.model_id = t2.model_id 
        WHERE t2.proj_id = {proj_id} and t2.model_id not in 
        (SELECT parent_model_id FROM ds.project_models_rel
        order by t1.model_id)
        """.format(proj_id=proj_id)
        df = pd.read_sql(sqlcmd, con=db.session.bind)
        data_list = df[['model_id', 'title']].to_dict(orient='records')
        return data_list

    def get_models(self, proj_id):
        """
        获取子模块的层级关系
        :param proj_id:
        :return:
        """
        model_list = []
        pro_q = (db.session.query(Model)
                 .outerjoin(ProjectModel, Model.model_id == ProjectModel.model_id)
                 .filter(ProjectModel.proj_id == proj_id).order_by(Model.code, Model.model_id).all())
        pro_rel_q = (db.session.query(Model)
                     .outerjoin(ProjectModelRel, Model.model_id == ProjectModelRel.model_id)
                     .filter(ProjectModelRel.proj_id == proj_id).order_by(Model.model_id).all())
        pro_model_ids = []
        for pro_rel in pro_rel_q:
            pro_model_ids.append(pro_rel.model_id)
        for pro in pro_q:
            if pro.model_id not in pro_model_ids:
                model_dict = {"model_id": pro.model_id, "title": pro.title, "parent_title": None}
                self._sub_model(model_dict, proj_id, model_list)
        return model_list

    def _sub_model(self, model_dict, proj_id, model_list):
        model_id = model_dict.get('model_id')
        parent_title = model_dict.get('parent_title')
        title = model_dict.get('title')
        model_sub_q = (db.session.query(Model)
                       .outerjoin(ProjectModelRel, Model.model_id == ProjectModelRel.model_id)
                       .filter(and_(ProjectModelRel.proj_id == proj_id,
                                    ProjectModelRel.parent_model_id == model_id)).all())
        if len(model_sub_q):
            for sub in model_sub_q:
                model_dict['model_id'] = sub.model_id
                if parent_title:
                    model_dict['parent_title'] = '%s/%s' % (parent_title, title)
                else:
                    model_dict['parent_title'] = title
                model_dict['title'] = sub.title
                self._sub_model(model_dict, proj_id, model_list)
        else:
            if not model_dict.get('parent_title'):
                model_dict['parent_title'] = '无'
            model = dict()
            model = copy.deepcopy(model_dict)
            model_list.append(model)

    def get_proj_by_fw(self, fw_id):
        q = (db.session.query(Project)
             .outerjoin(ProjectFW, Project.proj_id == ProjectFW.proj_id)
             .filter(ProjectFW.fw_id == fw_id).order_by(Project.proj_id))
        project_list = []
        for pro in q:
            project = pro.to_dict()
            project['create_time'] = self.time_to_str(project.get('create_time'))
            project['update_time'] = self.time_to_str(project.get('update_time'))
            project_list.append(project)
        return project_list

    def get_proj_tags(self, sec_id):
        """
        根据sec_id获取项目关联的Tag
        :param sec_id:
        :return:
        """
        from app.db.ds_section import DSSection
        q = (db.session.query(Ds_Doc)
             .outerjoin(DSSection, Ds_Doc.doc_id == DSSection.doc_id)
             .filter(DSSection.sec_id == sec_id)
             .first())
        proj_id = q.proj_id
        tag_id_list = self.get_proj_tag(proj_id)
        return tag_id_list

    def get_project_byname(self, proj_name):
        q = db.session.query(Project)
        project_list = []
        if proj_name:
            q = q.filter(Project.proj_name.ilike(proj_name))
            for fw in q:
                project_info = fw.to_dict()
                project_list.append(project_info)
        return project_list
