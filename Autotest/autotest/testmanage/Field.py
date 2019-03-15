# -*- coding: UTF-8 -*-
from testmanage.models import *
from django.db import transaction


class Field():
    def get_field_list(self):
        Field = FieldInfo.objects.all().order_by("sort_num")
        result = []
        for i_cat in Field:
            ct_lis = []
            if i_cat.field_option_list.all():
                cct = i_cat.field_option_list.all()
                for ct in cct:
                    ct_lis.append({'id': ct.id, 'value': ct.option_value})
            result.append({
                "id": i_cat.id,
                "name": i_cat.field_name,
                "en_name": i_cat.field_en_name,
                "type": i_cat.field_type,
                "is_show": i_cat.field_show_when_execute,
                "option_list": ct_lis,
                "sort_num": i_cat.sort_num,
                "field_open_use": i_cat.field_open_use
            })
        return result

    def add_field(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if not FieldInfo.objects.filter(field_name=json["name"]):
                ChangeData = FieldInfo(field_name=json["name"], field_type=json["type"],
                                       field_show_when_execute=json["is_show"],
                                       sort_num=json['sort_num'],
                                       field_open_use=json['field_open_use']
                                       )
                ChangeData.save()
                ChangeData.field_en_name = json["en_name"]
                for i_field in json["option_list"]:
                    option = FieldOptionInfo(option_value=i_field.get("value"))
                    option.save()
                    ChangeData.field_option_list.add(option)
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "该自定义字段已存在"
        return data

    def change_field(self, json, _id):
        data = {"result": '', "error": ''}

        with transaction.atomic():
            if FieldInfo.objects.filter(pk=_id):
                ChangeData = FieldInfo.objects.get(pk=_id)
                if ChangeData:
                    if ChangeData.field_option_list.all():
                        ChangeData.field_option_list.clear()
                    ChangeData.field_name = json["name"]
                    ChangeData.field_en_name = json["en_name"]
                    ChangeData.field_type = json["type"]
                    ChangeData.field_show_when_execute = json["is_show"]
                    ChangeData.sort_num = json["sort_num"]
                    ChangeData.field_open_use = json["field_open_use"]
                    for i_field in json["option_list"]:
                        option = FieldOptionInfo(option_value=i_field.get("value"))
                        option.save()
                        ChangeData.field_option_list.add(option)
                    ChangeData.save()
                    data["result"] = "OK"
            else:
                data["error"] = "未找到此数据"
        return data

    def delete_field(self, _id):
        data = {"result": '', "error": ''}
        if FieldInfo.objects.filter(pk=_id):
            ChangeData = FieldInfo.objects.get(pk=_id)
            ChangeData.delete()
            if not ChangeData.id:
                data["result"] = "DELETE OK"
        else:
            data["error"] = "未找到此数据"

        return data

    def batch_delete(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            for i_data in json["dellist"]:
                if FieldInfo.objects.filter(pk=i_data):
                    ChangeData = FieldInfo.objects.get(pk=i_data)
                    ChangeData.delete()
                    if not ChangeData.id:
                        data["result"] = "DELETE OK"
                else:
                    data["error"] = "未找到此数据"
        return data

    def search_field(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = FieldInfo.objects.all().order_by("sort_num")
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
            list = self.get_field_list()
        return list


    def data_to_json(self,data):
        search_list = []
        for i_data in data:
            ct_lis = []
            if i_data.field_option_list.all():
                cct = i_data.field_option_list.all()
                for ct in cct:
                    ct_lis.append({'id': ct.id, 'value': ct.option_value})
            search_list.append({
                "id": i_data.id,
                "name": i_data.field_name,
                "type": i_data.field_type,
                "is_show": i_data.field_show_when_execute,
                "option_list": ct_lis,
            })
        return search_list

    def link_option_type(self, data):
        field_name = "field_name"
        field_type = "field_type"
        field_show_when_execute = "field_show_when_execute"
        contains = "__icontains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "name":
                con = "{}".format(field_name)
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
            elif i_da.get("type") == "type":
                con = "{}".format(field_type)
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
            elif i_da.get("type") == "is_show":
                con = "{}".format(field_show_when_execute)
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
