# -*- coding: UTF-8 -*-
import copy
import pandas as pd
import os
from flask import current_app
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_base import CtrlBase
from app.ctrl.ctrl_user import CtrlUser
from app.ctrl.ctrl_user_group import CtrlUserGroup
from app.import_file.import_manager import ImportManager
from app.db.projects import *
from app.db.users import Group, Users
from app.ctrl.utility import Utillity
from app.db.users import UserRole
from app.data_server.ds_pieces import refresh_group_df


class CtrlProject(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Projects.proj_id
        self.db_object = Projects
        self.col_list = [Projects.inside_name.name, Projects.outside_name.name, Projects.proj_id.name]
        self.del_manday = """
            delete from func.func_man_day where task_id in (
                select task_id from func.task as t1 left join 
                func.functions as t2 on t1.func_id = t2.func_id
                left join func.quotations as t3 
                on t2.quotation_id = t3.quotation_id
                where t3.proj_id = {}
            )
            """
        self.del_task = """
            delete from func.task where func_id in(
                select func_id from func.functions as t1
                left join func.quotations as t2
                on t1.quotation_id = t2.quotation_id
                where t2.proj_id = {}
            )
            """
        self.del_function_one = """
            delete from func.func_group where func_id in(
                select func_id from func.functions as t1
                left join func.quotations as t2
                on t1.quotation_id = t2.quotation_id
                where t2.proj_id = {}
            )
            """
        self.del_function_two = """
            delete from func.functions where quotation_id in(
                select quotation_id from func.quotations 
                where proj_id = {}
            )
            """
        self.del_option_combination = """
            delete from func.option_combination where quotation_id in (
                select quotation_id from func.quotations
                where proj_id = {}
            )
            """
        self.del_option_value = """
            delete from func.option_value where option_id in (
                select option_id from func.options as t1 left join
                func.quotations as t2 on t1.quotation_id = t2.quotation_id 
                where proj_id = {}
            )
            """
        self.del_options = """
            delete from func.options where quotation_id in (
                select quotation_id from func.quotations
                where proj_id = {}
            )
            """
        self.del_preconditions = """
            delete from func.preconditions where proj_id = {}
            """
        self.del_quotations = """
            delete from func.quotations where proj_id = {}
            """
        self.del_user_role = """
            delete from user_role where proj_id = {}
            """
        self.del_projects = """
            delete from func.projects proj_id = {}
            """





    def add_project(self, data):
        try:
            if not data.get('other_proj_type'):
                if not data.get('proj_type'):
                    return False, "项目系列不能为空"
                else:
                    proj_type_id = data.get('proj_type')
            else:
                proj_type_id = self.add_proj_type(data.get('other_proj_type'))
            if not data.get('other_inside_name'):
                if not data.get('inside_name'):
                    return False, "项目内部名称不能为空"
                else:
                    inside_id = data.get('inside_name')
                    q = db.session.query(Projects).filter(Projects.inside_name == inside_id).first()
                    if q:
                        return False, "此内部名称已被使用"
            else:
                inside_id = self.add_proj_inside_name(data.get('other_inside_name'))
                if not inside_id:
                    return False, "此内部名称已被使用"
            if not data.get('file_url'):
                if not data.get('manage_id'):
                    return False, "体制表不能为空"
                else:
                    manage_id = data.get('manage_id')
                    file_url = None
            else:
                file_url = data.get("file_url")
                manage_id = None
            if not data.get('describe'):
                return False, "项目详细不能为空"
            if not data.get('outside_name'):
                return False, "项目外部名称不能为空"
            if not data.get('commit_user'):
                return False, "提交人不能为空"
            role_name = CtrlUser().get_user_role(data.get('commit_user'))
            if role_name != "SALES":
                return False, "该用户无法创建项目！"
            commit_user = data.get('commit_user')
            describe = data.get('describe')
            outside_name = data.get('outside_name')
            proj_id = self.add_proj_to_table(inside_id, outside_name, proj_type_id, describe, commit_user)
            if file_url:
                res, msg = self.import_project_manager(file_url, proj_id)
                if not res:
                    return False, msg
            else:
                CtrlUser().extend_user_roles_to_table(manage_id, proj_id, commit_user)
            db.session.commit()
            refresh_group_df()
            return proj_id, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def add_proj_inside_name(self, value):
        q = db.session.query(ProjectInsideName).filter(ProjectInsideName.inside_name == value).first()
        if q:
            return False
        name_info = {
            ProjectInsideName.inside_name.name: value,
        }
        name = ProjectInsideName(**name_info)
        db.session.add(name)
        db.session.flush()
        return name.inside_id

    def add_proj_type(self, value):
        q = db.session.query(ProjectType).filter(ProjectType.project_type == value).first()
        if q:
            return q.id
        type_info = {
            ProjectType.project_type.name: value,
        }
        proj_type = ProjectType(**type_info)
        db.session.add(proj_type)
        db.session.flush()
        return proj_type.id

    def add_proj_to_table(self, inside_id, outside_name, proj_type_id, describe, commit_user):
        pro_info = {
            Projects.inside_name.name: inside_id,
            Projects.outside_name.name: outside_name,
            Projects.proj_type.name: proj_type_id,
            Projects.describe.name: describe,
            Projects.commit_time.name: self.get_current_time(),
            Projects.update_time.name: self.get_current_time(),
            Projects.proj_state.name: 1,                 # 新建
            Projects.commit_user.name: commit_user,
        }
        pro = Projects(**pro_info)
        db.session.add(pro)
        db.session.flush()
        return pro.proj_id

    def get_inside_name_list(self):
        name_list = []
        q = db.session.query(ProjectInsideName).order_by(ProjectInsideName.inside_id).all()
        for name in q:

            name_list.append({"inside_id": name.inside_id, "inside_name": name.inside_name})
        return name_list

    def get_proj_type_list(self):
        type_list = []
        q = db.session.query(ProjectType).order_by(ProjectType.id).all()
        for name in q:
            type_list.append({"type_id": name.id, "proj_type": name.project_type})
        return type_list

    def check_proj_name(self):
        """
        将已经存在引用的InsideName返回给前端
        :return:
        """
        type_list = []
        q = (db.session.query(Projects.inside_name, ProjectInsideName.inside_name)
             .outerjoin(ProjectInsideName, Projects.inside_name == ProjectInsideName.inside_id)
             .order_by(Projects.inside_name).all())
        for name in q:
            type_list.append({"inside_id": name[0], "inside_name": name[1]})
        return type_list

    def get_proj_state_options(self):
        name_list = []
        q = db.session.query(ProjectState).order_by(ProjectState.state_id).all()
        for name in q:
            name_list.append({"state_id": name.state_id, "state_name": name.state_name})
        return name_list

    def get_proj_list(self):
        """
        获取所有的项目
        :param project_type:
        :return:
        """
        project_list = []
        q = (db.session.query(Projects)
             .filter(Projects.proj_state != 3)
             .order_by(Projects.proj_id)
             .all())
        for q_obj in q:
            project = dict()
            project[Projects.proj_id.name] = q_obj.proj_id
            project[Projects.outside_name.name] = q_obj.outside_name
            project[Projects.describe.name] = q_obj.describe
            project[Projects.commit_time.name] = self.time_to_str(q_obj.commit_time)
            project[Projects.update_time.name] = self.time_to_str(q_obj.update_time)
            project[Projects.inside_name.name] = q_obj.insideName.inside_name
            project[Projects.proj_type.name] = q_obj.projectType.project_type
            project[Projects.proj_state.name] = q_obj.projectState.state_name
            project_list.append(project)
        return project_list

    def get_proj_list_by_user_id(self, user_id):
        """
        获取我的项目
        :param project_type:
        :return:
        """
        project_list = []

        # my_groups = CtrlUserGroup().get_my_group(user_id)
        # group_ids = [group.get("group_id") for group in my_groups]
        # q = (db.session.query(Projects)
        #      .outerjoin(Group, Projects.commit_user == Group.owner_user)
        #      .filter(Group.group_id.in_(group_ids)))
        q1 = (db.session.query(Projects)
              .outerjoin(UserRole, UserRole.proj_id == Projects.proj_id)
              .filter(UserRole.user_id == user_id)
              .filter(Projects.proj_state != 3)
              .order_by(Projects.proj_id.desc())
              )
        q2 = (db.session.query(Projects)
              .filter(Projects.commit_user == user_id)
              .filter(Projects.proj_state != 3)
              .order_by(Projects.proj_id.desc()))
        q3 = q1.union(q2)
        for proj in q3:
            project_list.append(self.proj_to_dict(proj))
            # if proj.commit_user == user_id:
            #     project_list.append(self.proj_to_dict(proj))
            # else:
            #     for quo in proj.quotations:
            #         from app.ctrl.ctrl_cost import CtrlCost
            #         from app.ctrl.ctrl_quotations import CtrlQuotations
            #         groups, group_id_list, p_group_id_list = CtrlCost().get_group_list(user_id, quo.quotation_id)
            #         check_feature = CtrlQuotations().check_feature_group(quo.quotation_id, p_group_id_list)
            #         check_task = CtrlQuotations().check_task_group(quo.quotation_id, p_group_id_list)
            #         if check_feature:
            #             project_list.append(self.proj_to_dict(proj))
            #             break
            #         if check_task:
            #             project_list.append(self.proj_to_dict(proj))
            #             break
        return project_list

    def proj_to_dict(self, info):
        project = dict()
        project[Projects.proj_id.name] = info.proj_id
        project[Projects.outside_name.name] = info.outside_name
        project[Projects.describe.name] = info.describe
        project[Projects.commit_time.name] = self.time_to_str(info.commit_time)
        project[Projects.update_time.name] = self.time_to_str(info.update_time)
        project[Projects.inside_name.name] = info.insideName.inside_name
        project[Projects.proj_type.name] = info.projectType.project_type
        project[Projects.proj_state.name] = info.projectState.state_name
        return project

    # def get_proj_list_by_user_id2(self, user_id):
    #     """
    #     获取某人参与的项目
    #     :param user_id:
    #     :return:
    #     """
    #     try:
    #         from app.ctrl.ctrl_quotations import CtrlQuotations
    #         proj_list = CtrlQuotations().get_proj_by_user(user_id)
    #         project_list = []
    #         q = db.session.query(Projects).order_by(Projects.proj_id).filter(Projects.commit_user == user_id).all()
    #         for proj in proj_list:
    #             if proj.commit_user == user_id:
    #                 project_list.append(self.get_projects_by_id(proj))
    #             else:
    #                 for quo in proj.quotations:
    #                     from app.ctrl.ctrl_cost import CtrlCost
    #                     groups, group_id_list = CtrlCost().get_group_list(user_id, quo.quotation_id)
    #                     check_feature = CtrlQuotations().check_feature_group(quo.quotation_id, group_id_list)
    #                     check_task = CtrlQuotations().check_feature_group(quo.quotation_id, group_id_list)
    #                     if check_feature:
    #                         project_list = self.get_projects_by_id(list(quo)) + project_list
    #                     if check_task:
    #                         project_list = self.get_projects_by_id(list(quo)) + project_list
    #         return True, project_list
    #     except Exception as e:
    #         db.session.rollback()
    #         current_app.logger.error('%s' % str(e))
    #         return False, str(e)

    def get_projects_by_id(self, proj_info):
        return

    def get_one_proj_by_id(self, pro_id):
        try:
            proj_info = db.session.query(Projects).filter(Projects.proj_id == pro_id).first()
            if proj_info:
                project = proj_info.to_dict()
                # project[Projects.proj_id.name] = proj_info.proj_id
                # project[Projects.outside_name.name] = proj_info.outside_name
                # project[Projects.describe.name] = proj_info.describe
                # project[Projects.commit_time.name] = self.time_to_str(proj_info.commit_time)
                # project[Projects.update_time.name] = self.time_to_str(proj_info.update_time)
                # project[Projects.inside_name.name] = proj_info.inside_name
                project["inside_i_name"] = proj_info.insideName.inside_name
                # project[Projects.proj_type.name] = proj_info.proj_type
                project["proj_i_type"] = proj_info.projectType.project_type
                # project[Projects.proj_state.name] = proj_info.proj_state
                project["proj_i_state"] = proj_info.projectState.state_name
                project["quotations"] = []
                quotations = proj_info.quotations
                for iq in quotations:
                    quotation = iq.to_dict()
                    from app.ctrl.ctrl_quotations import CtrlQuotations
                    quotation[Quotations.create_user.name] = CtrlQuotations().get_user_name_by_id(iq.create_user)
                    quotation[Quotations.update_user.name] = CtrlQuotations().get_user_name_by_id(iq.create_user)
                    project["quotations"].append(quotation)
                return True, project
            else:
                return False, "沒有此項目信息"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def change_proj_by_id(self, pro_id, data):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == pro_id).first())
            if proj:
                inside_name = (db.session.query(ProjectInsideName)
                               .filter(ProjectInsideName.inside_name == data.get("inside_name"))
                               .first())
                if inside_name:
                    proj.inside_name = inside_name.inside_id
                proj.insideName.inside_name = data.get("inside_name")
                proj.outside_name = data.get("outside_name")
                proj.proj_type = data.get("proj_type")
                proj.describe = data.get("describe")
                proj.update_time = self.get_current_time()
                db.session.commit()
                return proj.proj_id, ""
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def delete_proj_by_id(self, data):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == data.get("proj_id")).first())
            if proj:
                db.session.excute(self.del_manday.format(data.get("proj_id")))
                db.session.excute(self.del_task.format(data.get("proj_id")))
                db.session.excute(self.del_function_one.format(data.get("proj_id")))
                db.session.excute(self.del_function_two.format(data.get("proj_id")))
                db.session.excute(self.del_option_combination.format(data.get("proj_id")))
                db.session.excute(self.del_option_value.format(data.get("proj_id")))
                db.session.excute(self.del_options.format(data.get("proj_id")))
                db.session.excute(self.del_preconditions.format(data.get("proj_id")))
                db.session.excute(self.del_quotations.format(data.get("proj_id")))
                db.session.excute(self.del_user_role.format(data.get("proj_id")))
                db.session.excute(self.del_projects.format(data.get("proj_id")))
                db.session.commit()
                return True, ""
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def project_basic_messige(self, proj_id):
        """取项目基本信息"""
        project = dict()
        q = db.session.query(Projects).filter(Projects.proj_id == proj_id).first()
        if q:
            project[Projects.proj_id.name] = proj_id
            project[Projects.inside_name.name] = q.insideName.inside_name
            project[Projects.outside_name.name] = q.outside_name
            project[Projects.commit_user.name] = q.users.to_dict()
        return project

    def get_manager_list(self):
        q = db.session.query(Projects).all()
        manage_list = []
        try:
            for proj in q:
                manage = dict()
                manage["manage_id"] = proj.proj_id
                manage["manage_name"] = "-".join([proj.insideName.inside_name, '体制表'])
                manage_list.append(manage)
            return manage_list, ""
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def import_manager(self, request_data):
        result = dict()
        try:
            file_upload = request_data.files['file']
            uti = Utillity()
            only_id = uti.get_nextval("file_seq_file_id_seq")
            file_path = "manager_import"
            file_path = os.path.join(file_path, str(only_id))
            file_path = os.path.abspath(os.path.join(os.getcwd(), file_path))
            file_name = file_upload.filename
            if not os.path.exists(file_path):
                os.makedirs(file_path)
            file_url = os.path.join(file_path, file_name)
            file_upload.save(file_url)
            result["file"] = {
                "file_name": file_name,
                "file_url": file_url,
            }
            return result, ''
        except Exception as e:
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_project_manager(self, proj_id, user_id):
        """
        取项目的体制信息
        :param proj_id:
        :return:
        """
        from app.ctrl.ctrl_user_group import CtrlUserGroup
        ctrl_group = CtrlUserGroup()
        try:
            project_data = self.project_basic_messige(proj_id)
            proj_id = project_data.get("proj_id")
            proj_name = project_data.get("inside_name")
            owner_user = project_data.get("commit_user")
            proj_manager = {"proj_id": proj_id, "proj_name": proj_name,
                            "owner_user": owner_user, "permissions": []}
            leader = 0
            if owner_user.get("user_id") == user_id:
                leader = 1
            if leader:
                proj_manager["permissions"] = ["PERM-PROJECTGROUP-LIST"]
            # 取pl组
            pl_group = ctrl_group.get_my_group(owner_user.get("user_id"), proj_id)
            if not pl_group:
                pl_group = ctrl_group.get_my_group(owner_user.get("user_id"))
                proj_manager["group_id"] = pl_group.get("group_id")
                proj_manager["group_name"] = pl_group.get("group_name")
                proj_manager["sub"] = []
                return proj_manager, ""
            proj_manager["group_id"] = pl_group.get("group_id")
            proj_manager["group_name"] = pl_group.get("group_name")
            # proj_manager["members"] = ctrl_group.group_members(pl_group.get("group_id"), owner_user.get("user_id"))
            # 取SGL，GL
            parent_group_id = pl_group.get("group_id")
            proj_manager["sub"] = []
            self.get_sub_group(parent_group_id, ctrl_group, proj_id, proj_manager["sub"], leader, user_id)
            return proj_manager, ""
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def get_sub_group(self, parent_group_id, ctrl_group, proj_id, group_list, leader, user_id):
        from app.ctrl.ctrl_user import CtrlUser
        ctrl_user = CtrlUser()
        sub_q = (db.session.query(Group)
                 .outerjoin(UserRole, Group.group_id == UserRole.group_id)
                 .filter(Group.parent_group_id == parent_group_id)
                 .filter(UserRole.proj_id == proj_id)
                 .order_by(Group.group_name).all())
        if sub_q:
            for sub in sub_q:
                sub_group = dict()
                sub_group['group_id'] = sub.group_id
                sub_group['group_name'] = sub.group_name
                sub_group['owner_user'] = ctrl_user.get_one_user(sub.owner_user)
                if leader:
                    sub_leader = True
                    sub_group['members'] = ctrl_group.group_members(sub.group_id, sub.owner_user)
                    sub_group["permissions"] = ["PERM-PROJECTGROUP-LIST"]
                else:
                    if user_id == sub.owner_user:
                        sub_leader = True
                        sub_group['members'] = ctrl_group.group_members(sub.group_id, sub.owner_user)
                        sub_group["permissions"] = ["PERM-PROJECTGROUP-LIST"]
                    else:
                        sub_leader = False
                        sub_group['members'] = []
                        sub_group["permissions"] = []
                sub_group['sub'] = []
                self.get_sub_group(sub.group_id, ctrl_group, proj_id, sub_group['sub'], sub_leader, user_id)
                group_list.append(sub_group)
        else:
            return

    def import_project_manager(self, file_url, proj_id):
        curr_app = current_app._get_current_object()
        from app.ctrl.ctrl_user_group import CtrlUserGroup
        ctrl_group = CtrlUserGroup()
        from app.ctrl.ctrl_user import CtrlUser
        ctrl_user = CtrlUser()
        project_data = self.project_basic_messige(proj_id)
        proj_owner_user = project_data.get("commit_user")
        pl_group = ctrl_group.get_my_group(proj_owner_user.get("user_id"))
        pl_group_id = pl_group.get("group_id")
        ctrl_import = ImportManager()
        success, manager_df = ctrl_import.import_excel(file_url)
        if not success:
            return False, manager_df
        manager_group = manager_df.to_dict(orient='records')
        manager_list = [{"role_id": curr_app.config.get("SALES_ROLE_ID"), "user_id": proj_owner_user.get("user_id"),
                         "proj_id": proj_id, "group_id": pl_group_id}]
        group_tree = self.get_group_tree(manager_group)
        for group in group_tree:
            group_name = group.get("group_name")
            owner_user = group.get("owner_user")
            sub_group = group.get("sub")
            sgl_obj, error = ctrl_user.add_user(owner_user)
            if error:
                return False, error
            sgl_user_id = sgl_obj.user_id
            sgl_group = {"group_name": group_name, "describe": "",
                         "parent_group_id": pl_group_id, "owner_user": sgl_user_id}
            res, msg = ctrl_group.add_group(sgl_group)
            if res:
                sgl_group_id = msg
            else:
                db.session.rollback()
                return False, msg
            manager_list.append({"role_id": curr_app.config.get("SGL_ROLE_ID"), "user_id": sgl_user_id,
                                 "proj_id": proj_id, "group_id": sgl_group_id})
            for sub in sub_group:
                gl_obj, error = ctrl_user.add_user(sub.get("owner_user"))
                if error:
                    return False, error
                gl_user_id = gl_obj.user_id
                gl_group = {"group_name": sub.get("group_name"), "describe": "",
                            "parent_group_id": sgl_group_id, "owner_user": gl_user_id}
                res, msg = ctrl_group.add_group(gl_group)
                if res:
                    gl_group_id = msg
                else:
                    db.session.rollback()
                    return False, msg
                manager_list.append({"role_id": curr_app.config.get("GL_ROLE_ID"), "user_id": gl_user_id,
                                     "proj_id": proj_id, "group_id": gl_group_id})
        ctrl_group.update_project_manager(proj_id, manager_list)
        return True, ""

    def get_group_tree(self, manager_group):
        group_tree = []
        group_index = dict()
        for group in manager_group:
            group_name = group.get("Group")
            owner_user = group.get("Leader")
            sub_group_name = group.get("SubGroup")
            sub_owner_user = group.get("SubLeader")
            if group_name:
                if group_index.get(group_name):
                    group_dict = group_tree[group_index.get(group_name)]
                    group_dict["sub"].append({"group_name": sub_group_name,
                                              "owner_user": sub_owner_user})
                else:
                    group_dict = dict()
                    group_dict["group_name"] = group_name
                    group_dict["owner_user"] = owner_user
                    group_dict["sub"] = []
                    if sub_group_name:
                        group_dict["sub"].append({"group_name": sub_group_name,
                                                  "owner_user": sub_owner_user})
                    group_tree.append(group_dict)
                    group_index[group_name] = len(group_tree) - 1
        return group_tree














