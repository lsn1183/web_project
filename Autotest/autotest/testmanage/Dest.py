# -*- coding: UTF-8 -*-
from testmanage.models import *
from django.db import transaction


class Dest():
    def get_dest_list(self):
        Dests = DestInfo.objects.all().order_by("dest_showname")
        result = []
        for i_cat in Dests:
            ct_lis = []
            en_name_list = []
            cn_name_list = []
            if i_cat.country_list.all():
                cct = i_cat.country_list.all()
                for ct in cct:
                    ct_lis.append(ct.id)
                    CountryData = CountryInfo.objects.get(pk=ct.id)
                result.append({
                    "id": i_cat.id,
                    "name": i_cat.dest_showname,
                    "provider": i_cat.data_provider,
                    "introduce": i_cat.dest_introduce,
                    "country_list": ct_lis,
                })
            else:
                result.append({
                    "id": i_cat.id,
                    "name": i_cat.dest_showname,
                    "provider": i_cat.data_provider,
                    "introduce": i_cat.dest_introduce,
                    "country_list": ct_lis,
                })
        return result

    def add_dest(self, json):
        data = {"result": '', "error": ''}
        with transaction.atomic():
            if not DestInfo.objects.filter(dest_showname=json["name"]):
                ChangeData = DestInfo(dest_showname=json["name"], data_provider=json["provider"],
                                      dest_introduce=json["introduce"])
                ChangeData.save()
                for i_dest in json["country_list"]:
                    ChangeData.country_list.add(CountryInfo.objects.get(pk=i_dest))
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "该名称已存在"
        return data

    def change_dest(self, json, _id):
        data = {"result": '', "error": ''}
        with transaction.atomic():

            if DestInfo.objects.filter(pk=_id):
                ChangeData = DestInfo.objects.get(pk=_id)
                if ChangeData.country_list.all():
                    ChangeData.country_list.clear()
                ChangeData.dest_showname = json["name"]
                ChangeData.data_provider = json["provider"]
                ChangeData.dest_introduce = json["introduce"]
                for i_dest in json["country_list"]:
                    dest_country = CountryInfo.objects.get(pk=i_dest)
                    ChangeData.country_list.add(dest_country)
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "无数据"

        return data

    def delete_dest(self, _id):
        data = {"error": ''}
        if DestInfo.objects.filter(pk=_id):
            ChangeData = DestInfo.objects.get(pk=_id)
            ChangeData.delete()
            if not ChangeData.id:
                data["result"] = "DELETE OK"
        else:
            data["error"] = "未找到此数据"
        return data

    def batch_delete(self, json):
        data = {"error": ''}
        with transaction.atomic():
            if json["dellist"]:
                for i_data in json["dellist"]:
                    ChangeData = DestInfo.objects.get(pk=i_data)
                    if ChangeData:
                        ChangeData.delete()
                    if not ChangeData.id:
                        data["result"] = "DELETE OK"
            else:
                data["error"] = "未找到此数据"
        return data


    def search_dest(self, json):
        list = []
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = DestInfo.objects.all().order_by("dest_showname")
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
            list = self.get_dest_list()
        return list


    def data_to_json(self,data):
        search_list = []

        for i_data in data:
            search_list.append({
                "id": i_data.id,
                "name": i_data.dest_showname,
                "provider": i_data.data_provider,
                "introduce": i_data.dest_introduce,
            })
        return search_list


    def link_option_type(self, data):
        name = "dest_showname"
        provider = "data_provider"
        introduce = "dest_introduce"
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
            elif i_da.get("type") == "provider":
                con = "{}".format(provider)
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
            elif i_da.get("type") == "introduce":
                con = "{}".format(introduce)
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
