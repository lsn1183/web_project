# -*- coding: utf-8 -*-
from testmanage.models import *
from django.db import transaction
from testmanage.Proj import Proj
import datetime


class Module():

    def get_module_list(self, Proj_id):
        result = []
        Key = ModelInfo.objects.filter(parent_proj_id=Proj_id).order_by("model_name")
        result = []
        for i_cat in Key:
            parent_proj_list = {}
            parent_model_list = {}
            field_list = []
            if i_cat.parent_proj:
                data = ProjInfo.objects.get(pk=i_cat.parent_proj.id)
                if data:
                    parent_proj_list = self.get_one_proj(i_cat.parent_proj.id)
            fields = i_cat.field_list.all()
            for fd in fields:
                fd_lis = []
                if fd.field_option_list.all():
                    options = fd.field_option_list.all()
                    for o_data in options:
                        fd_lis.append({
                            "value": o_data.option_value,
                        })
                field_list.append({
                    "id": fd.id,
                    "name": fd.field_name,
                    "type": fd.field_type,
                    "is_show": fd.field_show_when_execute,
                    "option_list": fd_lis,
                })

            if i_cat.parent_model:
                data = ModelInfo.objects.get(pk=i_cat.parent_model.id)
                if data.parent_model:
                    parent_model_list = {
                        "model_name": data.model_name,
                        "model_intro": data.model_intro,
                        "user_name": data.user_name,
                        "charger": data.charger,
                        "create_datetime": data.create_datetime,
                        "update_datetime": data.update_datetime,
                        "parent_proj": data.parent_proj.id,
                        "parent_model": data.parent_model.id,
                    }
                else:
                    parent_model_list = {
                        "model_name": data.model_name,
                        "model_intro": data.model_intro,
                        "user_name": data.user_name,
                        "charger": data.charger,
                        "create_datetime": data.create_datetime,
                        "update_datetime": data.update_datetime,
                        "parent_proj": data.parent_proj.id,
                        "parent_model": "",
                    }
            result.append({
                "model_name": i_cat.model_name,
                "model_intro": i_cat.model_intro,
                "user_name": i_cat.user_name,
                "charger": i_cat.charger,
                "create_datetime": i_cat.create_datetime,
                "update_datetime": i_cat.update_datetime,
                "parent_proj": parent_proj_list,
                "parent_model": parent_model_list,
                "id": i_cat.id,
                "proj_id": i_cat.parent_proj.id,
                "field_list": field_list,
            })
        return result

    def get_module_field_list(self, id):
        module_field_list = {}
        field_list = []
        check_field_list = []
        data = ModelInfo.objects.get(pk=id)
        if ModelInfo.objects.filter(parent_model=None):
            data_p = ProjInfo.objects.get(pk=data.parent_proj_id)
            fields = data_p.option_field_list.all()
        else:
            data_p = ModelInfo.objects.get(pk=data.parent_model_id)
            fields = data_p.field_list.all()
        cfuelds = data.field_list.all()
        for fd in fields:
            fd_lis = []
            if fd.field_option_list.all():
                options = fd.field_option_list.all()
                for o_data in options:
                    fd_lis.append({
                        "value": o_data.option_value,
                    })
            field_list.append({
                "id": fd.id,
                "name": fd.field_name,
                "type": fd.field_type,
                "is_show": fd.field_show_when_execute,
                "option_list": fd_lis,
            })
        for cfd in cfuelds:
            check_field_list.append(cfd.id)
        module_field_list["field_list"] = field_list
        module_field_list["check_field_list"] = check_field_list
        return module_field_list

    def get_module_field_list_by_proj(self, _id):
        module_field_list = {}
        field_list = []
        data = ProjInfo.objects.get(pk=_id)
        fields = data.option_field_list.all()
        for fd in fields:
            fd_lis = []
            if fd.field_option_list.all():
                options = fd.field_option_list.all()
                for o_data in options:
                    fd_lis.append({
                        "value": o_data.option_value,
                    })
            field_list.append({
                "id": fd.id,
                "name": fd.field_name,
                "type": fd.field_type,
                "is_show": fd.field_show_when_execute,
                "option_list": fd_lis,
            })
        module_field_list["field_list"] = field_list
        return module_field_list

    def find_parent_model(self, data, pm_id, pp_id):
        parent_proj_list = []
        parent_model_list = []
        if data.parent_model:
            data_p = ProjInfo.objects.get(pk=data.parent_model)
            if data.parent_model:
                parent_model_list.append({
                    "model_name": data.model_name,
                    "model_intro": data.model_intro,
                    "user_name": data.user_name,
                    "charger": data.charger,
                    "create_datetime": data.create_datetime,
                    "update_datetime": data.update_datetime,
                    "parent_proj": parent_proj_list,
                    "parent_model": parent_model_list,
                })
            elif not data.parent_model and data.parent_proj:
                pass
            return

    def add_module(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if not ModelInfo.objects.filter(model_name=json["model_name"]):
                if json["parent_proj_id"]:
                    ChangeData = ModelInfo(model_name=json["model_name"], model_intro=json["model_intro"],
                                           user_name=json["user_name"],
                                           create_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                           charger=json["charger"], parent_proj_id=json["parent_proj_id"],
                                           update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                           parent_model_id=json["parent_model_id"]
                                           )
                    ChangeData.save()
                    for i_field in json["field_option_list"]:
                        ChangeData.field_list.add(FieldInfo.objects.get(pk=i_field))
                    ChangeData.save()
                    data["result"] = "OK"
            else:
                data["error"] = "此模块名已存在"
        return data

    def get_module_tree(self, id):
        data = ModelInfo.objects.filter(pk=id)
        list = []
        p_m = ModelInfo.objects.filter(parent_model_id=id)
        for i_pm in p_m:
            child_m = ModelInfo.objects.filter(parent_model_id=i_pm)
            leaf = True
            if child_m:
                leaf = False
            list.append({
                'name': i_pm.model_name,
                'id': i_pm.id,
                'sub': [],
                'leaf': leaf
            })
        return list


    def get_proj_module_tree(self, id):
        # data = ModelInfo.objects.filter(id=id)
        list = []
        p_m = ModelInfo.objects.filter(parent_proj=id)
        R_m = p_m.filter(parent_model=None)
        for two in R_m :
            flag = False
            leaf = True
            m_m = p_m.filter(parent_model=two.id)
            if m_m:
                leaf = False
            for one in list:
                flag = flag or two.model_name == one.get("name")
            if not flag:
                list.append({
                    'name': two.model_name,
                    'id': two.id,
                    'sub': [],
                    'leaf': leaf
                })
        return list


    def change_module(self, json, _id):
        data = {"error": '', "result": ''}
        with transaction.atomic():
            if ModelInfo.objects.filter(pk=_id):
                ChangeData = ModelInfo.objects.get(pk=_id)
                if ChangeData.field_list.all():
                    ChangeData.field_list.clear()
                ChangeData.model_name = json["model_name"]
                ChangeData.model_intro = json["model_intro"]
                ChangeData.user_name = json["user_name"]
                ChangeData.charger = json["charger"]
                ChangeData.update_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if json.get("field_option_list"):
                    for i_field in json["field_option_list"]:
                        ChangeData.field_list.add(FieldInfo.objects.get(pk=i_field))
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "未找到此数据"
        return data

    def delete_module(self, id):
        data = {"error": '',"result" :''}
        if ModelInfo.objects.filter(pk=id):
            ChangeData = ModelInfo.objects.get(pk=id)
            ChangeData.delete()
            if not ChangeData.id:
                data["result"] = "DELETE OK"
        else:
            data["error"] = "未找到此数据"
        return data

    def search_model(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = ModelInfo.objects.all().order_by("model_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                list = self.data_to_json(SearchData)
        else:
            list = self.get_module_list()
        return list

    def get_one_proj(self, _id):
        Proj = ProjInfo.objects.get(pk=_id)
        result = {}
        if Proj:
            dest_lis = []
            field_lis = []
            keyword_lis = []
            if Proj.dest_list.all():
                dests = Proj.dest_list.all()
                for ct in dests:
                    ct_lis = []
                    if ct.country_list.all():
                        countrys = ct.country_list.all()
                        for c_data in countrys:
                            ct_lis.append({
                                "code": c_data.iso_code,
                                "en_name":c_data.eng_name,
                                "cn_name":c_data.cn_name,
                            })
                    dest_lis.append({
                        "name": ct.dest_showname,
                        "provider": ct.data_provider,
                        "introduce": ct.dest_introduce,
                        "country_list": ct_lis,
                    })
            if Proj.option_field_list.all():
                fields = Proj.option_field_list.all()
                for fd in fields:
                    fd_lis = []
                    if fd.field_option_list.all():
                        options = fd.field_option_list.all()
                        for o_data in options:
                            fd_lis.append({
                                "value": o_data.option_value,
                            })
                    field_lis.append({
                        "name": fd.field_name,
                        "type": fd.field_type,
                        "is_show": fd.field_show_when_execute,
                        "option_list": fd_lis,
                    })
            if Proj.keyword_list.all():
                keywords = Proj.keyword_list.all()
                for kd in keywords:
                    keyword_lis.append({
                        "id": kd.id,
                        "name": kd.keyword,
                    })
            result = {
                "name": Proj.proj_name,
                "intro": Proj.proj_intro,
                "user_name": Proj.user_name,
                "is_catus": Proj.is_catus,
                "create_time": Proj.create_datetime,
                "update_time": Proj.update_datetime,
                "finish_time": Proj.finish_datetime,
                "dest_list": dest_lis,
                "field_list": field_lis,
                "keyword_list": keyword_lis,
                "proj_id": Proj.id
            }
        return result

    def batch_delete(self, json):
        data = {"error": '',"result": ''}
        with transaction.atomic():
            if json["dellist"]:
                for i_data in json["dellist"]:
                    ChangeData=ModelInfo.objects.get(pk=i_data)
                    ChangeData.delete()
                    data["result"] = "OK"
            else:
                data["error"] = "未找到此数据"
        return data

    def link_option_type(self, data):
        name = "model_name"
        contains = "__contains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "name":
                con = "{}".format(name)
                if i_da.get("option") == "不等于":
                    reback = False
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "等于":
                    reback = True
                    con = '{}'.format(con)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "包含":
                    reback = True
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
                elif i_da.get("option") == "不包含":
                    reback = False
                    con = '{}{}'.format(con, contains)
                    se_list.append({"name": con, "is_equal": reback, "val": i_da.get("content")})
            else:
                se_list = ""
        return se_list

    def data_to_json(self, Key):
        search_list = []
        for i_cat in Key:
            parent_proj_list = {}
            parent_model_list = {}
            field_list = []

            if i_cat.parent_proj:
                data = ProjInfo.objects.get(pk=i_cat.parent_proj.id)
                if data:
                    parent_proj_list = self.get_one_proj(i_cat.parent_proj.id)

            fields = i_cat.field_list.all()
            for fd in fields:
                fd_lis = []
                if fd.field_option_list.all():
                    options = fd.field_option_list.all()
                    for o_data in options:
                        fd_lis.append({
                            "value": o_data.option_value,
                        })
                field_list.append({
                    "name": fd.field_name,
                    "type": fd.field_type,
                    "is_show": fd.field_show_when_execute,
                    "option_list": fd_lis,
                })

            if i_cat.parent_model:
                data = ModelInfo.objects.get(pk=i_cat.parent_model.id)
                parent_model_list = {
                    "model_name": data.model_name,
                    "model_intro": data.model_intro,
                    "user_name": data.user_name,
                    "charger": data.charger,
                    "create_datetime": data.create_datetime,
                    "update_datetime": data.update_datetime,
                    "parent_proj": data.parent_proj.id,
                    "parent_model": data.parent_model,
                }

            search_list.append({
                "model_name": i_cat.model_name,
                "model_intro": i_cat.model_intro,
                "user_name": i_cat.user_name,
                "charger": i_cat.charger,
                "create_datetime": i_cat.create_datetime,
                "update_datetime": i_cat.update_datetime,
                "parent_proj": parent_proj_list,
                "parent_model": parent_model_list,
                "id": i_cat.id,
                "field_list": field_list
            })
        return search_list
