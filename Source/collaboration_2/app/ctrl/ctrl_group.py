# -*- coding: UTF-8 -*-
from app.db import db
from sqlalchemy import or_, and_
from flask import current_app
from app.db.group import Group, GroupModel, Member
from app.db.user import User
from app.ctrl.ctrl_role import CtrlRole
LEADER_ID = 1  # 组长
MEMBER_ID = 0  # 组员


class CtrlGroup(object):
    def __init__(self):
        pass

    def get_groups(self, group_name):
        q = db.session.query(Group)
        if group_name:
            q = q.filter(Group.group_name.ilike("%"+group_name+"%"))
        q = q.order_by(Group.group_id)
        group_list = []
        for group in q:
            group_list.append(group.to_dict())
        for group in group_list:
            group_id = group.get(Group.group_id.name)
            count = self.count_member(group_id)
            group['count'] = count
        return group_list

    def get_project_group(self, accessToken, proj_id):
        project_root = self.get_project_root(accessToken, proj_id)
        group_list = []
        if project_root:
            group_members = project_root.get('group_members')
            for group in group_members:
                group_name = group.get('group_name')
                if group_name not in group_list:
                    group_list.append(group_name)
        return group_list

    def get_project_root(self, accessToken, proj_id):
        """
        从cactus上拿项目的体制信息
        :param accessToken:
        :param proj_id:
        :return:
        """
        from app.api_1_0.api_cactus import ApiCactus
        result = ApiCactus().cactus_project_group(accessToken, proj_id)
        project_root = dict()
        if result.get('code') == 0:
            majorProject = result.get('majorProject')
            pmo_user = majorProject.get('ownerUser')
            if pmo_user:
                project_root['pmo'] = pmo_user
            work_root = result.get('root')
            if work_root:
                project_root['username'] = work_root.get('user').get('userName')
                project_root['user_role'] = 'PL'
                group_list = work_root.get('nodes')
                group_members = []
                self._get_cactus_group(group_list, group_members)
                project_root['group_members'] = group_members
        return project_root

    def _get_cactus_group(self, group_list, group_members, group_name=None):
        for group in group_list:
            member = dict()
            if group.get('nodeType') == 1:  # 1:组信息；2：成员信息
                group_name = group.get('name')
                member['group_name'] = group_name
                member['username'] = group.get('user').get('userName')
                member['user_role'] = 'GL'
            elif group.get('nodeType') == 2:
                member['group_name'] = group_name
                member['username'] = group.get('user').get('userName')
                member['user_role'] = 'Developer'
            group_members.append(member)
            if group.get('nodes'):
                self._get_cactus_group(group.get('nodes'), group_members, group_name)

    def get_cactus_group_mesage(self, proj_id, model_id, accessToken):
        """
        获取模块关联组的信息
        :param proj_id:
        :param model_id:
        :param accessToken:
        :return:
        """
        from app.ctrl.ctrl_user import CtrlUser
        from app.ctrl.ctrl_model import CtrlModel
        group_list = CtrlUser().get_group_by_model(proj_id, model_id)
        model_name = CtrlModel().get_name_by_model_id(model_id)
        project_root = self.get_project_root(accessToken, proj_id)
        group_message = []
        group_members = project_root.get('group_members')
        if not group_members:
            return group_message, model_name
        for group in group_members:
            group_name = group.get('group_name')
            if group_name in group_list:
                group_message.append(group)
        return group_message, model_name

    def add_group(self, group_data):
        group = Group(**group_data)
        db.session.add(group)
        db.session.commit()

    def update_group(self, group_date):
        group_id = group_date.get('group_id')
        db.session.query(Group).filter(Group.group_id == group_id).update(group_date)
        db.session.commit()

    def delete_group(self, group_id):
        db.session.query(GroupModel).filter(GroupModel.group_id == group_id).delete()
        db.session.query(Member).filter(Member.group_id == group_id).delete()
        db.session.query(Group).filter(Group.group_id == group_id).delete()
        db.session.commit()

    def count_member(self, group_id):
        count = db.session.query(Member).filter(Member.group_id == group_id).count()
        return count

    def get_group_members(self, group_id):
        q = (db.session.query(Member.group_id, Group.group_name,
                              Member.user_id, User.username, )
             .filter(Member.group_id == Group.group_id)
             .filter(Member.user_id == User.user_id)
             )
        if group_id:
            q = q.filter(Member.group_id == group_id)
        q = q.order_by(Group.group_name)
        group_members = []
        for group in q:
            group_member = dict()
            group_member[Member.group_id.name] = group[0]
            group_member[Group.group_name.name] = group[1]
            group_member[Member.user_id.name] = group[2]
            group_member[User.username.name] = group[3]
            role_list = CtrlRole().get_roles_by_user(group[2])
            group_member['role_list'] = role_list
            group_members.append(group_member)
        return group_members

    def add_group_members(self, member_data):
        for member in member_data:
            user_id = member.get('user_id')
            group_id = member.get('group_id')
            user = (db.session.query(Member)
                    .filter(and_(Member.user_id == user_id, Member.group_id == group_id)).all())
            if len(user):
                continue
            db.session.add(Member(**member))
        db.session.commit()

    def update_member_role(self, member):
        user_id = member.get("user_id")
        group_id = member.get("group_id")
        db.session.query(Member).filter(and_(Member.user_id == user_id, Member.group_id == group_id)).update(Member)
        db.session.commit()

    def delete_member(self, group_id, user_id):
        db.session.query(Member).filter(and_(Member.user_id == user_id, Member.group_id == group_id)).delete()
        db.session.commit()

    def get_model_by_group(self, group_name):
        """
        根据组名获取模块
        :param group_name:
        :return:
        """
        from app.db.model import Model
        q = (db.session.query(Model)
             .outerjoin(GroupModel, Model.model_id == GroupModel.model_id)
             .filter(GroupModel.group_name == group_name)
             .order_by(Model.code, Model.model_id))
        model_list = []
        for model in q:
            model_dict = dict()
            model_dict['model_id'] = model.model_id
            model_dict['title'] = model.title
            model_list.append(model_dict)
        return model_list

