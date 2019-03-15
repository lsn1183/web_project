# -*- coding: UTF-8 -*-
import os
import re
from app.db import db
import pandas as pd
import datetime
from search.es_manager import EsManager
from app.db.spec.specification import ProjectMember


class CtrlAnyplance(object):
    def __init__(self):
        es_manager = EsManager.instance()
        self.es_anyplace = es_manager.get_curr_anyplace_index()

    def search_one_field(self, value):
        """查询索引"""
        result = self.es_anyplace.search(query_string=value)
        return result

    def search_one_anyplace(self, value):
        """查询某一条索引的详细"""
        result = self.es_anyplace.search(query_string=value, size=40)
        res = {"key_list": [], "value_list": []}
        for hit in result["hits"]["hits"]:
            for key in hit.get("_source").keys():
                res["key_list"].append(key)
                res["value_list"].append(hit.get("_source").get(key))
        return res

    def search_field_by_user(self, value, user, size, page):
        """查询user相关的项目下的索引"""
        proj_list = self.find_project_by_user(user)
        result = []
        if proj_list:
            number = (page - 1) * size
            new_value = self.filter_field(value)
            member_projects = self.inster_project_to_value(proj_list)
            query_string = "({}) AND ({})" .format(new_value, member_projects)
            result = self.es_anyplace.search(query_string=query_string, from_=number, size=size)
        return result

    # def search_field_by_user(self, value, user):
    #     """查询user相关的项目下的索引"""
    #     pro_list = self.find_project_by_user(user)
    #     result = []
    #     if pro_list:
    #         new_value = self.filter_field(value)
    #         member_projects = self.inster_project_to_value(pro_list)
    #         query_string = "(%r) AND (%r)" % (new_value, member_projects)
    #         result = self.es_anyplace.search(query_string=query_string, size=40)
    #     return result

    # def inster_project_to_value(self, pro_list, value):
    #     """将pro_list中的项目拼入value"""
    #     string = "project:\("
    #     for pro in pro_list:
    #         string = "%r %r" % (string, pro)
    #     string = "%r %r" % (string, '\)')
    #     new_value = "%r %r" % (value, string)
    #     return new_value

    def inster_project_to_value(self, proj_list):
        """将pro_list中的项目拼入value"""
        strings = []
        for proj in proj_list:
            strings.append("project:{}".format(proj))
        value = " OR ".join(strings)
        return value

    def filter_field(self, value):
        """过滤字符串中（）"""
        value = value.replace('(', '\(').replace(')', '\)')
        return value

    # def splice_project(self, value):
    #     """提取value中project的值"""
    #     new_pro = re.search(r'(project:("+[^"]*"+))|(project:[^"\s]+)', value, flags=0).group()
    #     new_pro = new_pro.replace('project:', '').strip('"')
    #     new_pro = new_pro.lstrip('(').rstrip(')')
    #     new_pro = new_pro.split(' ')
    #     print(new_pro)
    #     return new_pro

    def find_project_by_user(self, user):
        """查询此人的所有相关项目"""
        q = db.session.query(ProjectMember).filter(ProjectMember.user_name == user).all()
        res = []
        if q:
            for i in q:
                res.append(i.project_name)
        return res

    def find_key_name(self):
        """查询索引里所有P,R,S的值作为字段返回"""
        result = []
        for value in ["project", "rank", "status"]:
            result.append("%s:" % value)
            key_data = self.es_anyplace.search_unique(field_name=value)
            for i_key in key_data["aggregations"]["uniq_gender"]["buckets"]:
                result.append("%s:%s" % (value, i_key.get("key")))
        return result

    def find_key_name_by_user(self, user):
        """查询某人的项目在索引里所有R,S的值作为字段返回"""
        result = []
        pro_list = self.find_project_by_user(user)
        for pro in pro_list:
            result.append("project:%s" % pro)
        for value in ["rank", "status"]:
            result.append("%s:" % value)
            key_data = self.es_anyplace.search_unique(field_name=value)
            for i_key in key_data["aggregations"]["uniq_gender"]["buckets"]:
                result.append("%s:%s" % (value, i_key.get("key")))
        return result
