from userManage.api_cactus import ApiCactus
from userManage.models import *
from django.db import transaction

class UserRole(object):
    def __init__(self):
        pass

    def get_role_by_cactus(self, data_json):
        """
        从cactus项目体制中获取用户角色
        :param proj_id:
        :param accessToken:
        :param model_id:
        :return:
        """
        #TODO@yuyin

    def get_user_by_name(self, username):
        user = Users.objects.get(user_name=username)
        return user

    def get_all_perm(self):
        perm_list = []
        perm = Permission.objects.all()
        type_list = []
        for i_perm in perm:
            if i_perm.perm_type not in type_list:
                type_list.append(i_perm.perm_type)
        for type_i in type_list:
            sub_list = []
            q = Permission.objects.filter(perm_type=type_i)
            for per in q:
                sub_list.append({'id': per.pk, 'perm_name': per.perm_name})
            perm_list.append({
                'perm_type': type_i,
                'perm_list': sub_list
            })
        return perm_list

    def get_username_role(self, username):
        if username:
            role = Role.objects.get(role_name=username)
            role.perm_list.all()
        data = {
            "role": role.role_name,
            "role_list": [],
        }
        for i_r in role.perm_list.all():
            data["role_list"].append({
                "role": i_r.id,
                "role_list": i_r.perm_name,
            })
        return role.perm_list.all()

    def check_permission(self, data_json):
        data = {"error": ""}
        personnel = Users.objects.get(user_name=data_json.get('personnel_name'))
        if personnel.role_list.all():
            role = personnel.role_list.first()
            role_data = Role.objects.get(role_name=role.role_name)
            with transaction.atomic():
                for item in data_json.get('role_list'):
                    role_data.perm_list.add(Permission.objects.get(pk=item))
                role_data.save()
        else:
            data["error"] = "人员无角色"
        return data

    def save_personne_role(self, data_json):
        data = {"error": ""}
        for data_item in data_json:
            if Users.objects.filter(pk=data_item.get('user_id')):
                personnel = Users.objects.get(pk=data_item.get('user_id'))
                with transaction.atomic():
                    if personnel.role_list.all():
                        personnel.role_list.clear()
                    for item in data_item.get("role_list"):
                        personnel.role_list.add(Role.objects.get(pk=item))
                    personnel.save()
                    data["result"] = "OK"
            else:
                data["error"] = "查无此人"
        return data

    def change_permission(self, data_json):
        data = {"error": ""}
        with transaction.atomic():
            if Role.objects.filter(pk=data_json.get('role_name')):
                role = Role.objects.get(pk=data_json.get('role_name'))
                if role.perm_list.all():
                    role.perm_list.clear()
                for i_dest in data_json["perm_list"]:
                    dest_country = Permission.objects.get(pk=i_dest)
                    role.perm_list.add(dest_country)
                role.save()
            else:
                data["error"] = "无此角色"
            return data

    def get_role_by_promission(self, permission):
        data = {"error": ""}
        with transaction.atomic():
            if Role.objects.filter(pk=permission):
                role = Role.objects.get(pk=permission)
                role_list = []
                if role.perm_list.all():
                    for i_role in role.perm_list.all():
                        role_list.append(i_role.id)
                data["result"] = role_list
            else:
                data["error"] = "没有此角色"
            return data

    def get_role(self):
        role_data = Role.objects.all().order_by('role_name')
        data_list = {"error": ""}
        if role_data:
            role_list = []
            for role_i in role_data:
                role_list.append({
                    'role_name': role_i.role_name,
                    'id': role_i.id
                })
            data_list["result"] = role_list
        else:
            data_list["error"] = "没有此角色"
        return data_list

    def get_role_user(self, user_name):  # 获取某人角色
        data_list = {"error": ""}
        if Users.objects.filter(user_name=user_name):
            users_data = Users.objects.get(user_name=user_name)
            role_list = []
            if users_data.role_list.all():
                for item in users_data.role_list.all():
                    role_list.append({
                        'role_name': item.role_name,
                        'id': item.id
                    })
            data_list['role_list'] = role_list
        else:
            data_list["error"] = "查无此人"
        return data_list

    def get_user_permission(self, user_name, per_name):  # 获取某人的权限
        data_list = {"error": ""}
        if Users.objects.filter(user_name=user_name):
            users_data = Users.objects.get(user_name=user_name)
            perm_list = []
            if users_data.role_list.all():
                for item in users_data.role_list.all():
                    for perm_i in item.perm_list.all():
                        perm_list.append(perm_i.perm_name)
            if per_name in perm_list:
                data_list['flag'] = True
            else:
                data_list['flag'] = False
        else:
            data_list["error"] = "查无此人"
        return data_list