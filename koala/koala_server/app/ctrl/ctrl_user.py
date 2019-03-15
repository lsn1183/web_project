# -*- coding: UTF-8 -*-
from flask import current_app
from app.db.users import *
from app.db import db
from sqlalchemy import or_, and_


class CtrlUser(object):
    def __init__(self):
        pass

    def register(self, username='', work_id=''):
        if username:
            user = db.session.query(Users).filter(Users.user_name == username).first()
            if user:  # 用户已经存在
                user_id = user.user_id
                user_dict = user.to_dict()
                user_dict['role_list'] = self.get_user_roles(user_id)
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
            user = Users(user_name=username, user_type='NORMAL', work_id=work_id)
            db.session.add(user)
            db.session.commit()
            return user
        return None

    def get_user_by_name(self, username):
        q = db.session.query(Users)
        user = q.filter(Users.user_name == username).first()
        if user:
            return user
        return None

    def get_user_by_work(self, work_id):
        q = db.session.query(Users)
        user = q.filter(Users.work_id == work_id).first()
        if user:
            return user
        return None

    def get_one_user(self, user_id):
        q = db.session.query(Users).filter(Users.user_id == user_id).first()
        if q:
            return q.to_dict()
        return None

    def add_user(self, username):
        user = self.get_user_by_name(username)
        if user:
            return user, ""
        else:
            error = "该用户还没登录过系统！"
            # user = Users(user_name=username, user_type='NORMAL', work_id="")  # 测试先加进去
            # db.session.add(user)
            return user, error

    def get_all_user(self):
        user_list = []
        q = db.session.query(Users).order_by(Users.work_id)
        for user in q:
            user_list.append(user.to_dict())
        return user_list

    def get_user_role(self, user_id):
        """取不带项目的角色"""
        q = (db.session.query(Roles)
             .outerjoin(UserRole, Roles.role_id == UserRole.role_id)
             .filter(UserRole.user_id == user_id)
             .first())
        if q:
            return q.role_name
        return None

    def get_user_roles(self, user_id):
        role_list = []
        q = (db.session.query(Roles)
             .outerjoin(UserRole, Roles.role_id == UserRole.role_id)
             .filter(UserRole.user_id == user_id).distinct())
        for role in q:
            role_list.append(role.role_name)
        return role_list

    def extend_user_roles_to_table(self, old_proj_id, proj_id, user_id):
        q = (db.session.query(UserRole)
             .filter(UserRole.proj_id == old_proj_id)
             .all())
        for i in q:
            if i.role_id == 1:
                info = {
                    UserRole.proj_id.name: proj_id,
                    UserRole.group_id.name: i.group_id,
                    UserRole.role_id.name: i.role_id,
                    UserRole.user_id.name: user_id,
                }
            else:
                info = {
                    UserRole.proj_id.name: proj_id,
                    UserRole.group_id.name: i.group_id,
                    UserRole.role_id.name: i.role_id,
                    UserRole.user_id.name: i.user_id,
                }
            pro = UserRole(**info)
            db.session.add(pro)
