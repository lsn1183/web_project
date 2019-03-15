# -*- coding: UTF-8 -*-
import pandas as pd
from app.db import db
from app.db.role import Role
from flask import current_app
from app.db.role_permissions import RolePermission
from app.ctrl.ctrl_permission import CtrlPermission
from app.db.user_roles import UserRoles
ROLE_CLS_SYS = 'system'


class CtrlRole(object):
    def __init__(self):
        pass

    def get_roles(self, role_id=None, cls=ROLE_CLS_SYS):
        q = db.session.query(Role)
        if role_id:
            q = q.filter(Role.role_id == role_id)
        if cls:
            q = q.filter(Role.cls == cls)
        q = q.order_by(Role.role_id)
        # print(q.statement)
        role_list = []
        for role in q:
            role_list.append(role.to_dict())
        return role_list

    def get_role_permission(self, role_id=None, cls=ROLE_CLS_SYS):
        role_list = self.get_roles(role_id, cls)
        q = db.session.query(RolePermission)
        if role_id:
            q = q.filter(Role.role_id == role_id)
        q = q.order_by(RolePermission.role_id, RolePermission.perm_id)
        # print(q.statement)
        df = pd.read_sql(q.statement, db.session.bind)
        perm_list = CtrlPermission().get_perms(category=False)
        for role in role_list:
            role_id = role.get("role_id")
            perm_df = df[df["role_id"] == role_id]
            perm_df = perm_df[["perm_id"]]
            assigned_list = [True] * len(perm_df)
            perm_df = perm_df.assign(assigned=assigned_list)
            perm_df2 = perm_df.set_index(keys=["perm_id"])
            # perm_S = perm_df2["assigned"]
            # perms = perm_S.to_dict()
            perms_all = perm_df.to_dict(orient='records')
            for perm_info in perm_list:
                perm_id = perm_info.get("perm_id")
                if perm_id not in perm_df2.index:
                    perms_all.append({"perm_id": perm_id, "assigned": False})
            perms_all = sorted(perms_all, key = lambda x: x.get("perm_id"))
            role["permissions"] = perms_all
            # role.update(perms)
        return role_list

    def update_role_permissions(self, role_permissions_list):
        result = {"result": "NG"}
        try:
            for role_permissions in role_permissions_list:
                role_id = role_permissions.get('role_id')
                permissions = role_permissions.get('permissions')
                self.delete_role_permission(role_id)
                for permission in permissions:
                    if permission.get('assigned'):
                        role_per_dict = {'role_id': role_id, 'perm_id': permission.get('perm_id')}
                        self.insert_role_permission(role_per_dict)
            db.session.commit()
            result['result'] = "OK"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % e)
            result["error"] = "服务异常！请联系管理员！"
        return result

    def delete_role_permission(self, role_id):
        db.session.query(RolePermission).filter(RolePermission.role_id == role_id).delete()

    def insert_role_permission(self, role_permission):
        rolePerm = RolePermission(**role_permission)
        db.session.add(rolePerm)

    def get_roles_by_user(self, user_id):
        q = (db.session.query(Role)
             .outerjoin(UserRoles, Role.role_id == UserRoles.role_id)
             .filter(UserRoles.user_id == user_id))
        role_list = []
        for role in q:
            role_list.append(role.role_name)
        return role_list



