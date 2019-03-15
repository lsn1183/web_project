# -*- coding: UTF-8 -*-
from app.db.permission import Permission
from app.db import db


class CtrlPermission(object):
    def __init__(self):
        pass

    def get_perms(self, category=True):
        query = db.session.query(Permission).order_by(Permission.perm_id)
        perm_dict = {}
        if category:
            sort_list = []
            for perm in query:
                perm = perm.to_dict()
                module_name = perm.pop("module_name")
                if module_name in perm_dict:
                    perm_dict[module_name].append(perm)
                else:
                    perm_dict[module_name] = [perm]
                    sort_list.append(module_name)
            perm_sorted = []
            for module_name in sort_list:
                perm_sorted.append({"model_name": module_name,
                                    "permissions": perm_dict.get(module_name)})
            return perm_sorted
        else:
            perm_list = []
            for perm in query:
                perm = perm.to_dict()
                perm_list.append(perm)
            return perm_list

    def get_perm_by_role(self, role_list):
        from app.db.role import Role
        from app.db.role_permissions import RolePermission
        q = (db.session.query(Permission.perm_name)
             .outerjoin(RolePermission, Permission.perm_id == RolePermission.perm_id)
             .outerjoin(Role, RolePermission.role_id == Role.role_id)
             .filter(Role.role_name.in_(role_list)).distinct())
        perm_list = []
        for perm in  q:
            perm_list.append(perm[0])
        return perm_list





