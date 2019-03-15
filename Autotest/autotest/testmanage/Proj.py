# -*- coding: UTF-8 -*-
from testmanage.models import *
from django.db import transaction
# from requests import get, put, post, delete
from django.http import FileResponse
from jinja2 import Environment, FileSystemLoader, Template
from testmanage.Country import Country
from testmanage.Dest import Dest
from testmanage.Field import Field
from testmanage.Keyword import Keyword
from userManage.api_cactus import ApiCactus
from diffTool.ctrl_base import CtrlBase
import datetime
import json
import yaml
import os


class Proj(CtrlBase):
    def __init__(self):
        CtrlBase.__init__(self)
        self.db_obj = ProjInfo
        self.key_col = 'id'
        self.diff_col_list = ['proj_name', 'proj_intro', 'user_name', 'charger',
                              'finish_datetime']

    def get_proj_list(self):
        Proj = ProjInfo.objects.all().order_by("id")
        result = []
        for i_cat in Proj:
            dest_lis = []
            field_lis = []
            keyword_list = []
            if i_cat.dest_list.all():
                dests = i_cat.dest_list.all()
                for ct in dests:
                    ct_lis = []
                    if ct.country_list.all():
                        countrys = ct.country_list.all()
                        for c_data in countrys:
                            ct_lis.append({
                                "id": c_data.id,
                                "code": c_data.iso_code,
                                "en_name":c_data.eng_name,
                                "cn_name":c_data.cn_name,
                            })
                    dest_lis.append({
                        "id": ct.id,
                        "name": ct.dest_showname,
                        "provider": ct.data_provider,
                        "introduce": ct.dest_introduce,
                        "country_list": ct_lis,
                    })
            if i_cat.option_field_list.all():
                fields = i_cat.option_field_list.all()
                for fd in fields:
                    fd_lis = []
                    if fd.field_option_list.all():
                        options = fd.field_option_list.all()
                        for o_data in options:
                            fd_lis.append({
                                "id": o_data.id,
                                "value": o_data.option_value,
                            })
                    field_lis.append({
                        "id": fd.id,
                        "name": fd.field_name,
                        "type": fd.field_type,
                        "is_show": fd.field_show_when_execute,
                        "option_list": fd_lis,
                    })
            if i_cat.keyword_list.all():
                keywords = i_cat.keyword_list.all()
                for kd in keywords:
                    keyword_list.append({
                        "id": kd.id,
                        "name": kd.keyword,
                    })
            result.append({
                "id": i_cat.id,
                "name": i_cat.proj_name,
                "intro": i_cat.proj_intro,
                "user_name": i_cat.user_name,
                "charger": i_cat.charger,
                "is_catus": i_cat.is_catus,
                "create_time": i_cat.create_datetime,
                "update_time": i_cat.update_datetime,
                "finish_time": i_cat.finish_datetime,
                "dest_list": dest_lis,
                "field_list": field_lis,
                "keyword_list": keyword_list,
            })
        return result

    def get_projects(self):
        proj_objs = ProjInfo.objects.all().order_by("id")
        result = []
        for proj_obj in proj_objs:
            result.append({"id": proj_obj.id, "name": proj_obj.proj_name,
                           # "intro": proj_obj.proj_intro,
                           })
        return result

    def get_proj_tree(self, _id):
        Proj = ProjInfo.objects.filter(pk=_id).order_by("proj_name")
        result = []
        if Proj:
            for i_cat in Proj:
                leafs = True
                md = ModelInfo.objects.filter(parent_proj=i_cat)
                if md:
                    leafs = False
                result.append({
                    "id": i_cat.id,
                    "name": i_cat.proj_name,
                    "leaf": leafs,
                })

        return result


    def add_proj(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if not ProjInfo.objects.filter(proj_name=json["name"]):
                now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                ChangeData = ProjInfo(proj_name=json["name"], proj_intro=json["intro"],
                                      charger=json["charger"],user_name=json["user_name"],
                                      create_datetime=now_time, finish_datetime=json["finish_time"],
                                      update_datetime=now_time,
                                      is_catus=False,)
                ChangeData.save()
                for i_dest in json["dest_list"]:
                    ChangeData.dest_list.add(DestInfo.objects.get(pk=i_dest.get("id")))
                for i_field in json["field_list"]:
                    ChangeData.option_field_list.add(FieldInfo.objects.get(pk=i_field.get("id")))
                for i_kd in json["keyword_list"]:
                    ChangeData.keyword_list.add(KeywordInfo.objects.get(pk=i_kd.get("id")))
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "此项目名称已存在"
        return data

    # def add_test(self, json):
    #     """
    #     测试比较后更新数据并记下log信息
    #     :param json:
    #     :return:
    #     """
    #     id = 3
    #     # json["is_catus"] = False
    #     old_data = None
    #     if id:
    #         old_data_list = self.get_old_data(self.db_obj, id)
    #         if old_data_list:
    #             old_data = old_data_list[0]
    #     log_dict = self.common_add(self.db_obj, json, old_data, self.diff_col_list, self.key_col)

    def add_import_proj(self, json, dest_list, field_list, keyword_list):
        data = ""
        with transaction.atomic():
            ChangeData = ProjInfo(proj_name=json["name"], proj_intro=json["intro"], user_name=json["user_name"],
                                  create_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  update_datetime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                  is_catus=False, finish_datetime=json["finish_time"],)
            ChangeData.save()
            for i_dest in dest_list:
                ChangeData.dest_list.add(DestInfo.objects.get(pk=i_dest))
            for i_field in field_list:
                ChangeData.option_field_list.add(FieldInfo.objects.get(pk=i_field))
            for i_kd in keyword_list:
                ChangeData.keyword_list.add(KeywordInfo.objects.get(pk=i_kd))
            ChangeData.save()
            data = ChangeData.id
        return data

    def change_proj(self, json, _id):
        data ={"result": '', "error": ''}
        with transaction.atomic():
            if ProjInfo.objects.filter(pk=_id):
                ChangeData = ProjInfo.objects.get(pk=_id)
                if ChangeData.option_field_list.all():
                    ChangeData.option_field_list.clear()
                if ChangeData.dest_list.all():
                    ChangeData.dest_list.clear()
                if ChangeData.keyword_list.all():
                    ChangeData.keyword_list.clear()
                ChangeData.proj_name = json["name"]
                ChangeData.proj_intro = json["intro"]
                ChangeData.charger = json["charger"]
                ChangeData.finish_datetime = json["finish_time"]
                ChangeData.update_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if json["field_list"]:
                    for i_field in json["field_list"]:
                        ChangeData.option_field_list.add(FieldInfo.objects.get(pk=i_field.get("id")))
                if json["dest_list"]:
                    for i_dest in json["dest_list"]:
                        ChangeData.dest_list.add(DestInfo.objects.get(pk=i_dest.get("id")))
                if json["keyword_list"]:
                    for i_kd in json["keyword_list"]:
                        ChangeData.keyword_list.add(KeywordInfo.objects.get(pk=i_kd.get("id")))
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "未找到数据"
        return data

    def change_import_proj(self, json, _id, dest_list, field_list, keyword_list):
        data = ""
        with transaction.atomic():
            ChangeData = ProjInfo.objects.get(pk=_id)
            if ChangeData:
                if ChangeData.option_field_list.all():
                    ChangeData.option_field_list.clear()
                if ChangeData.dest_list.all():
                    ChangeData.dest_list.clear()
                if ChangeData.keyword_list.all():
                    ChangeData.keyword_list.clear()
                ChangeData.proj_name = json["name"]
                ChangeData.proj_intro = json["intro"]
                ChangeData.user_name = json["user_name"]
                ChangeData.finish_datetime = json["finish_time"]
                ChangeData.update_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                if field_list:
                    for i_field in field_list:
                        ChangeData.dest_list.add(FieldInfo.objects.get(pk=i_field))
                if dest_list:
                    for i_dest in dest_list:
                        ChangeData.dest_list.add(DestInfo.objects.get(pk=i_dest))
                if keyword_list:
                    for i_kd in keyword_list:
                        ChangeData.keyword_list.add(KeywordInfo.objects.get(pk=i_kd))
                ChangeData.save()
                data = ChangeData.id
        return data

    def delete_proj(self, _id):
        data = {"result": '', "error":''}
        if ProjInfo.objects.filter(pk=_id):
            ChangeData = ProjInfo.objects.get(pk=_id)
            ChangeData.delete()
            data["result"] = "DELETE OK"
        else:
            data["error"] = "未找到此数据"
        return data

    def export_yaml(self, _id):
        if ProjInfo.objects.get(pk=_id):
            proj = self.get_one_proj(_id)
            if proj:
                env = Environment(loader=FileSystemLoader('./template','utf-8'))
                template = env.get_template("test2.yaml")
                file = template.render(proj)
                # print(file)
                resp = FileResponse(file)
                resp['Content-Type'] = 'application/octet-stream'
                resp['Content-Disposition'] = 'attachment;filename="proj{0}.yaml"'.format(_id)
            else:
                resp = ""
        else:
            resp = ""
        return resp

    def import_yaml(self, file):
        data = ""
        error =""
        file_name = file.name
        path = os.path.join('import')
        if not os.path.exists(path):
            os.makedirs(path)
        with open(os.path.join(path, file_name), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        json = yaml.load("import/" + file_name)
        Data = ProjInfo.objects.get(proj_name= json.get("name"))
        res = ""
        with transaction.atomic():
            if Data:
                dest_id_list,dest_error = self.search_yaml_data(DestInfo, json.get("dest_list"), "code")
                field_id_list,field_error = self.search_yaml_data(FieldInfo, json.get("field_list"), "option")
                keyword_id_list,keyword_error = self.search_yaml_data(KeywordInfo, json.get("keyword_list"), "key")
                if dest_error or field_error or keyword_error:
                    res = ""
                    error = dest_error+field_error+keyword_error
                else:
                    res = self.change_import_proj(json, Data.id, dest_id_list, field_id_list, keyword_id_list)
            else:
                dest_id_list,dest_error = self.search_yaml_data(DestInfo, json.get("dest_list"), "code")
                field_id_list,field_error = self.search_yaml_data(FieldInfo, json.get("field_list"), "option")
                keyword_id_list,keyword_error = self.search_yaml_data(KeywordInfo, json.get("keyword_list"), "key")
                # res = self.add_import_proj(json, dest_id_list, field_id_list, keyword_id_list)
                if dest_error or field_error or keyword_error:
                    res = ""
                    error = dest_error+field_error+keyword_error
                else:
                    res = self.add_import_proj(json, dest_id_list, field_id_list, keyword_id_list)
            if res:
                data = "OK"
        return data, error

    # def import_yaml(self, file):
    #     data = ""
    #     file_name = file.name
    #     path = os.path.join('import')
    #     if not os.path.exists(path):
    #         os.makedirs(path)
    #     with open(os.path.join(path, file_name), 'wb+') as destination:
    #         for chunk in file.chunks():
    #             destination.write(chunk)
    #     json = yaml.load("import/" + file_name)
    #     Data = ProjInfo.objects.get(proj_name= json.get("name"))
    #     res = ""
    #     with transaction.atomic():
    #         if Data:
    #             dest_id_list = self.search_yaml_data(DestInfo, json.get("dest_list"), CountryInfo, "code")
    #             field_id_list = self.search_yaml_data(FieldInfo, json.get("field_list"), FieldOptionInfo, "option")
    #             keyword_id_list = self.search_yaml_data(KeywordInfo, json.get("keyword_list"), KeywordInfo, "key")
    #             res = self.change_import_proj(json, Data.id, dest_id_list, field_id_list, keyword_id_list)
    #         else:
    #             dest_id_list = self.search_yaml_data(DestInfo, json.get("dest_list"), CountryInfo, "code")
    #             field_id_list = self.search_yaml_data(FieldInfo, json.get("field_list"), FieldOptionInfo, "option")
    #             keyword_id_list = self.search_yaml_data(KeywordInfo, json.get("keyword_list"), KeywordInfo, "key")
    #             res = self.add_import_proj(json, dest_id_list, field_id_list, keyword_id_list)
    #         if res:
    #             data = "OK"
    #     return data

    def search_yaml_data(self, Info, json, type):
        id_list = []
        error = ""
        for FD in json:
            if FD.get("name"):
                if type == "code":
                    Data = Info.objects.get(dest_showname=FD.get("name"))
                    if Data:
                        id_list.append(Data.id)
                    else:
                        error = "未找到名字为 '{0}' 的仕向地".format(FD.get("name"))
                elif type =="option":
                    Data = Info.objects.get(field_name=FD.get("name"))
                    if Data:
                        id_list.append(Data.id)
                    else:
                        error = "未找到名字为 '{0}' 的自定义字段".format(FD.get("name"))
                else:
                    Data = Info.objects.get(keyword=FD.get("name"))
                    if Data:
                        id_list.append(Data.id)
                    else:
                        error = "未找到名字为 '{0}' 的关键字".format(FD.get("name"))
        return id_list,error

    # def search_yaml_data(self, Info, json, deepInfo , type):
    #     id_list = []
    #     for FD in json:
    #         if FD.get("name"):
    #             if type == "code":
    #                 Data = Info.objects.get(dest_showname=FD.get("name"))
    #                 if Data:
    #                     ct_id_list = self.search_deep_data(deepInfo, FD.get("Country_list"))
    #                     res = self.change_import_dest(FD,Data.id,ct_id_list)
    #                     if res:
    #                         id_list.append(Data.id)
    #                 else:
    #                     ct_id_list = self.search_deep_data(deepInfo, FD.get("Country_list"))
    #                     res = self.add_import_dest(FD, ct_id_list)
    #                     if res:
    #                         id_list.append(Data.id)
    #             elif type =="option":
    #                 Data = Info.objects.get(field_name=FD.get("name"))
    #                 if Data:
    #                     fp_id_list = self.search_deep_data(deepInfo, FD.get("option_list"))
    #                     res = self.change_import_field(FD, Data.id, fp_id_list)
    #                     if res:
    #                         id_list.append(Data.id)
    #                 else:
    #                     fp_id_list = self.search_deep_data(deepInfo, FD.get("option_list"))
    #                     res = self.add_import_field(FD, fp_id_list)
    #                     if res:
    #                         id_list.append(Data.id)
    #             else:
    #                 Data = Info.objects.get(keyword=FD.get("name"))
    #                 if Data:
    #                     res = self.change_import_keyword(FD, Data.id)
    #                     if res:
    #                         id_list.append(Data.id)
    #                 else:
    #                     res = self.add_import_keyword(FD)
    #                     if res:
    #                         id_list.append(Data.id)
    #     return id_list

    def add_import_dest(self, json, list):
        data = ""
        with transaction.atomic():
            ChangeData = DestInfo(dest_showname=json["name"], data_provider=json["provider"],
                                  dest_introduce=json["introduce"])
            ChangeData.save()
            for i_dest in list:
                ChangeData.country_list.add(CountryInfo.objects.get(pk=i_dest))
            ChangeData.save()
            data = ChangeData.id
        return data

    def add_import_field(self, json, list):
        data = ""
        with transaction.atomic():
            ChangeData = FieldInfo(field_name=json["name"], field_type=json["type"],
                                   field_show_when_execute=json["is_show"])
            ChangeData.save()
            for i_field in list:
                option = FieldOptionInfo.objects.get(pk=i_field)
                ChangeData.field_option_list.add(option)
            ChangeData.save()
            data = ChangeData.id
        return data

    def change_import_dest(self, json, _id, list):
        data = ""
        with transaction.atomic():
            ChangeData = DestInfo.objects.get(pk=_id)
            if ChangeData:
                if ChangeData.country_list.all():
                    ChangeData.country_list.clear()
                ChangeData.dest_showname = json["name"]
                ChangeData.data_provider = json["data_provider"]
                ChangeData.dest_introduce = json["introduce"]
                for i_dest in list:
                    dest_country = CountryInfo.objects.get(pk=i_dest)
                    ChangeData.country_list.add(dest_country)
                ChangeData.save()
                data = ChangeData.id
        return data

    def change_import_keyword(self, json, _id):
        data = ""
        with transaction.atomic():
            ChangeData = KeywordInfo.objects.get(pk=_id)
            if ChangeData:
                ChangeData.keyword = json["name"]
                ChangeData.save()
                data = ChangeData.id
        return data

    def add_import_keyword(self, json):
        data = ""
        with transaction.atomic():
            ChangeData = KeywordInfo(keyword=json["name"])
            ChangeData.save()
            data = ChangeData.id
        return data

    def change_import_field(self, json, _id, list):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if FieldInfo.objects.filter(pk=_id):
                ChangeData = FieldInfo.objects.get(pk=_id)
                if ChangeData.field_option_list.all():
                    ChangeData.field_option_list.clear()
                ChangeData.field_name = json["name"]
                ChangeData.field_type = json["type"]
                ChangeData.field_show_when_execute = json["is_show"]
                for i_field in list:
                    option = FieldOptionInfo.objects.get(pk=i_field)
                    ChangeData.field_option_list.add(option)
                ChangeData.save()
                data["result"] = ChangeData.id
            else:
                data["error"] = "未找到此数据"
        return data

    # def search_deep_data(self, Info, json):
    #     id_list = []
    #     if json:
    #         for CF in json:
    #             if CF.get("code"):
    #                 Data = Info.object.get(iso_code= CF.get("code"))
    #                 if Data:
    #                     res = Country().change_country(CF,Data.id)
    #                     if res:
    #                         id_list.append(Data.id)
    #                 else:
    #                     res = Country().add_country(CF)
    #                     if res["result"]:
    #                         id_list.append(res["result"])
    #             elif CF.get("value"):
    #                 Data = Info.object.get(value= CF.get("value"))
    #                 if Data:
    #                     Data.value = CF["value"]
    #                     Data.save()
    #                     id_list.append(Data.id)
    #                 else:
    #                     addData = Info(value= CF.get("value"))
    #                     addData.save()
    #                     id_list.append(addData.id)
    #     return id_list

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
                    dest_lis.append({
                        "name": ct.dest_showname,
                    })
            if Proj.option_field_list.all():
                fields = Proj.option_field_list.all()
                for fd in fields:
                    field_lis.append({
                        "name": fd.field_name,
                    })
            if Proj.keyword_list.all():
                keywords = Proj.keyword_list.all()
                for kd in keywords:
                    keyword_lis.append({
                        "name": kd.keyword,
                    })
            result = {
                "name": Proj.proj_name,
                "intro": Proj.proj_intro,
                "user_name": Proj.user_name,
                "is_catus":Proj.is_catus,
                "create_time":Proj.create_datetime,
                "update_time":Proj.update_datetime,
                "finish_time": Proj.finish_datetime,
                "dest_list": dest_lis,
                "field_list": field_lis,
                "keyword_list": keyword_lis,
            }
        return result

    # def get_one_proj(self, _id):
    #     Proj = ProjInfo.objects.get(pk=_id)
    #     result = {}
    #     if Proj:
    #         dest_lis = []
    #         field_lis = []
    #         keyword_lis = []
    #         if Proj.dest_list.all():
    #             dests = Proj.dest_list.all()
    #             for ct in dests:
    #                 ct_lis = []
    #                 if ct.country_list.all():
    #                     countrys = ct.country_list.all()
    #                     for c_data in countrys:
    #                         ct_lis.append({
    #                             "code": c_data.iso_code,
    #                             "en_name":c_data.eng_name,
    #                             "cn_name":c_data.cn_name,
    #                         })
    #                 dest_lis.append({
    #                     "name": ct.dest_showname,
    #                     "provider": ct.data_provider,
    #                     "introduce": ct.dest_introduce,
    #                     "country_list": ct_lis,
    #                 })
    #         if Proj.option_field_list.all():
    #             fields = Proj.option_field_list.all()
    #             for fd in fields:
    #                 fd_lis = []
    #                 if fd.field_option_list.all():
    #                     options = fd.field_option_list.all()
    #                     for o_data in options:
    #                         fd_lis.append({
    #                             "value": o_data.option_value,
    #                         })
    #                 field_lis.append({
    #                     "name": fd.field_name,
    #                     "type": fd.field_type,
    #                     "is_show": fd.field_show_when_execute,
    #                     "option_list": fd_lis,
    #                 })
    #         if Proj.keyword_list.all():
    #             keywords = Proj.keyword_list.all()
    #             for kd in keywords:
    #                 keyword_lis.append({
    #                     "id": kd.id,
    #                     "name": kd.keyword,
    #                 })
    #         result = {
    #             "name": Proj.proj_name,
    #             "intro": Proj.proj_intro,
    #             "user_name": Proj.user_name,
    #             "is_catus":Proj.is_catus,
    #             "create_time":Proj.create_datetime,
    #             "update_time":Proj.update_datetime,
    #             "finish_time": Proj.finish_datetime,
    #             "dest_list": dest_lis,
    #             "field_list": field_lis,
    #             "keyword_list": keyword_lis,
    #         }
    #     return result

    def search_proj(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = ProjInfo.objects.all().order_by("proj_name")
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
            list = self.get_proj_list()
        return list

    def data_to_json(self,data):
        search_list = []
        for i_data in data:
            dest_lis = []
            field_lis = []
            keyword_lis = []
            if i_data.dest_list.all():
                dests = i_data.dest_list.all()
                for ct in dests:
                    ct_lis = []
                    if ct.country_list.all():
                        countrys = ct.country_list.all()
                        for c_data in countrys:
                            ct_lis.append({
                                "id": c_data.id,
                                "code": c_data.iso_code,
                                "en_name": c_data.eng_name,
                                "cn_name": c_data.cn_name,
                            })
                    dest_lis.append({
                        "id": ct.id,
                        "name": ct.dest_showname,
                        "provider": ct.data_provider,
                        "introduce": ct.dest_introduce,
                        "country_list": ct_lis,
                    })
            if i_data.option_field_list.all():
                fields = i_data.option_field_list.all()
                for fd in fields:
                    fd_lis = []
                    if fd.field_option_list.all():
                        options = fd.field_option_list.all()
                        for o_data in options:
                            fd_lis.append({
                                "id": o_data.id,
                                "value": o_data.option_value,
                            })
                    field_lis.append({
                        "id": fd.id,
                        "name": fd.field_name,
                        "type": fd.field_type,
                        "is_show": fd.field_show_when_execute,
                        "option_list": fd_lis,
                    })
            if i_data.keyword_list.all():
                keywords = i_data.keyword_list.all()
                for kd in keywords:
                    keyword_lis.append({
                        "id": kd.id,
                        "name": kd.keyword,
                    })
            search_list.append({
                "id": i_data.id,
                "name": i_data.proj_name,
                "intro": i_data.proj_intro,
                "user_name": i_data.user_name,
                "is_catus": i_data.is_catus,
                "create_time": i_data.create_datetime,
                "update_time": i_data.update_datetime,
                "finish_time": i_data.finish_datetime,
                "dest_list": dest_lis,
                "field_list": field_lis,
                "keyword_list":keyword_lis,
            })
        return search_list

    def link_option_type(self, data):
        name = "proj_name"
        user = "user_name"
        contains = "__icontains"
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
            elif i_da.get("type") == "user_name":
                con = "{}".format(user)
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

    def batch_delete(self, json):
        data = {"error": '', "result": ''}
        with transaction.atomic():
            if json["dellist"]:
                for i_data in json["dellist"]:
                    ChangeData = ProjInfo.objects.get(pk=i_data)
                    ChangeData.delete()
                    data["result"] = "OK"
            else:
                data["error"] = "请不要传空数据"
        return data

    def get_proj_for_cactus(self, data_json):
        """
        从cactus上拿项目信息
        :param data_json:
        :return:
        """
        manager = data_json.get('manager')
        accessToken = data_json.get('accessToken')
        proj_ids = self.get_ids_by_manager(manager)
        result_list = []
        cactus_project_list = ApiCactus().get_project_from_cactus(accessToken)
        for cactus_project in cactus_project_list:
            project_list = cactus_project.get('project_list')
            for project in project_list:
                if manager == project.get('manager'):
                    proj_id = project.get('proj_id')
                    if proj_id not in proj_ids:
                        project_json = {
                            'proj_id': proj_id,
                            'proj_name': project.get('proj_name'),
                            'charger': project.get('manager'),
                            'intro': project.get('proj_intro')
                        }
                        result_list.append(project_json)
        return result_list

    def get_ids_by_manager(self, manager):
        proj_id_list = []
        q = ProjInfo.objects.filter(charger=manager)
        for proj in q:
            proj_id_list.append(proj.pk)
        return proj_id_list