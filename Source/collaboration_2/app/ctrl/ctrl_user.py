# -*- coding: UTF-8 -*-
from flask import current_app
from app.db.user import User
from app.db import db
from sqlalchemy import or_, and_
from app.ctrl.ctrl_role import CtrlRole
from app.db.user_roles import UserRoles


class CtrlUser(object):
    def __init__(self):
        pass

    def register(self, username='', work_id=''):
        if username:
            user = db.session.query(User).filter(User.username == username).first()
            if user:  # 用户已经存在
                user_id = user.user_id
                roles = CtrlRole().get_roles_by_user(user_id)
                user_dict = user.to_dict()
                user_dict['role_list'] = roles
                return user_dict
            else:  # 新用户
                user = self.add(username, work_id)
                if user:
                    user_dict = user.to_dict()
                    user_dict['role_list'] = []
                    return user_dict
        return {}

    def add(self, username='', work_id=''):
        if username:
            user = User(username=username, user_type='NORMAL', work_id=work_id)
            db.session.add(user)
            db.session.commit()
            return user
        return None

    def get_user(self, user_id=None, page=None, size=None, condition=None):
        count = 0
        q = db.session.query(User)
        if user_id:
            q = q.filter(User.user_id == user_id)
        elif condition:
            q = q.filter(User.username.ilike('%'+condition+'%'))
        q.order_by(User.user_id)
        if page and size:
            count = q.count()
            q = q.limit(size).offset(size * (page - 1))
        role_list = []
        for user in q:
            role_list.append(user.to_dict())
        return count, role_list

    def get_user_role(self, page, size, user_id, cls, condition):
        role_obj = CtrlRole()
        count, user_list = self.get_user(user_id, page, size, condition)
        role_list = role_obj.get_roles(None, cls)
        user_role_list = self._get_user_role(user_id)
        result_list = []
        for user in user_list:
            role_list = self._rescript_role_list(role_list)
            result_dict = dict()
            result_dict['user_name'] = user.get('username')
            user_id = user.get('user_id')
            result_dict['user_id'] = user_id
            for role in role_list:
                user_role = dict()
                user_role['user_id'] = user_id
                user_role['role_id'] = role.get('role_id')
                if user_role in user_role_list:
                    role['have_role'] = True
            result_dict['role_list'] = role_list
            result_list.append(result_dict)
        return count, result_list

    def get_user_permission(self, user_id):
        """获取用户的所有权限
        :param user_id:
        :return: permission list
        """
        sqlcmd = """
        SELECT distinct b.perm_id, perm_name
          FROM public.user_roles as a
          inner join role_permissions as b
          on a.role_id = b.role_id
          left join permission as c
          on b.perm_id = c.perm_id
          where a.user_id = :user_id
          order by b.perm_id
        """
        perm_infos = db.session.execute(sqlcmd, {'user_id': user_id}).fetchall()
        permission_list = []
        for perm in perm_infos:
            permission_list.append(perm[1])
        return permission_list

    def _rescript_role_list(self, role_list):
        new_list = []
        for role in role_list:
            new_role = {}
            new_role['role_id'] = role.get('role_id')
            new_role['have_role'] = False
            new_list.append(new_role)
        return new_list

    def _get_user_role(self, user_id=None):
        q = db.session.query(UserRoles.user_id, UserRoles.role_id)
        if user_id:
            q = q.filter(UserRoles.user_id == user_id)
        user_roles = q.order_by(UserRoles.user_id, UserRoles.role_id)
        user_role_list = []
        for user_role in user_roles:
            user_role_dict = dict()
            user_role_dict['user_id'] = user_role[0]
            user_role_dict['role_id'] = user_role[1]
            user_role_list.append(user_role_dict)
        return user_role_list

    def update_user_role(self, user_role_list):
        result = {"result": "NG"}
        try:
            for user_role in user_role_list:
                user_id = user_role.get('user_id')
                role_list = user_role.get('role_list')
                self.delete_user_role(user_id)
                for role in role_list:
                    if role.get('have_role'):
                        user_role_dict = {'user_id': user_id, 'role_id': role.get('role_id')}
                        self.insert_user_role(user_role_dict)
            db.session.commit()
            result['result'] = "OK"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            result["error"] = "服务异常！请联系管理员！"
        return result

    def delete_user_role(self, user_id):
        db.session.query(UserRoles).filter(UserRoles.user_id == user_id).delete()

    def insert_user_role(self, user_role):
        userRole = UserRoles(**user_role)
        db.session.add(userRole)

    def get_user_by_name(self, username):
        q = db.session.query(User)
        user = q.filter(User.username == username).first()
        if user:
            return user
        return None

    def get_role_by_cactus(self, data_json):
        """
        从cactus项目体制中获取用户角色
        :param proj_id:
        :param accessToken:
        :param model_id:
        :return:
        """
        try:
            role_list = []
            proj_id = data_json.get('proj_id')
            accessToken = data_json.get('accessToken')
            model_id = data_json.get('model_id')
            username = data_json.get('username')
            user = self.get_user_by_name(username)
            roles = CtrlRole().get_roles_by_user(user.user_id)
            if user.user_type == "TEST" or "Admin" in roles:
                perm_list = self.get_user_permission(user.user_id)
                return perm_list, None
            group_list = []
            if model_id:
                group_list = self.get_group_by_model(proj_id, model_id)
                if not group_list:
                    return role_list, "该模块还没分配组！"
            from app.ctrl.ctrl_group import CtrlGroup
            project_root = CtrlGroup().get_project_root(accessToken, proj_id)
            if not project_root:
                return [], None
            if project_root:
                pmo = project_root.get('pmo')
                if username == pmo.get('userName'):
                    role_list.append('PMO')
                pl_username = project_root.get('username')
                if pl_username == username:
                    role_list.append(project_root.get('user_role'))
                group_members = project_root.get('group_members')
                if group_members:
                    for group in group_members:
                        if username == group.get('username'):
                            if group.get('group_name') in group_list:
                                role_list.append(group.get('user_role'))
            if role_list:
                from app.ctrl.ctrl_permission import CtrlPermission
                perm_list = CtrlPermission().get_perm_by_role(role_list)
            else:
                if model_id:
                    perm_list = self.user_in_model_rel(proj_id, model_id, username, project_root)
                else:
                    perm_list = []
            return perm_list, None
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            error = "服务异常！请联系管理员！"
            return None, error

    def user_in_model_rel(self, proj_id, model_id, username, project_root):
        """
        判断用户是否在关联模块的组内,
        关联模块的组成员有查看权限
        :return:
        """
        perm_list = []
        group_list = self.get_group_by_model_ref(proj_id, model_id)
        group_members = project_root.get('group_members')
        if group_members:
            for group in group_members:
                if username == group.get('username'):
                    if group.get('group_name') in group_list:
                        perm_list.append('设计书_查看')
                        break
        return perm_list

    def get_group_by_model(self, proj_id, model_id):
        from app.db.group import GroupModel
        q = db.session.query(GroupModel).filter(and_(GroupModel.proj_id == proj_id,
                                                GroupModel.model_id == model_id))
        group_list = []
        for group in q:
            group_list.append(group.group_name)
        return group_list

    def get_group_by_model_ref(self, proj_id, model_id):
        from app.db.group import GroupModel
        from app.db.project import ProjectModelRef
        q = (db.session.query(GroupModel)
             .outerjoin(ProjectModelRef, ProjectModelRef.ref_model_id == GroupModel.model_id)
             .filter(ProjectModelRef.model_id == model_id)
             .filter(GroupModel.proj_id == proj_id))
        group_list = []
        for group in q:
            group_list.append(group.group_name)
        return group_list







