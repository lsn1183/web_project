# -*- coding: UTF-8 -*-
import datetime
from testmanage.models import *
from testcase.models import *
from django.db import transaction
from django.http import FileResponse
import xml.etree.ElementTree as et
from jenkinsapi.jenkins import Jenkins


class Testplan():
    def __init__(self):
        self.jenkins = Jenkins('http://192.168.37.112:8080', username='huangyp', password='111111Aa')

    def get_testplan_list(self, Proj_id, page, size):
        data = {"error":""}
        start = (page-1)*size
        data["count"] = TestplanInfo.objects.filter(proj_id=Proj_id).count()
        end = min((page-1)*size+size, data["count"])
        cases = TestplanInfo.objects.filter(proj_id=Proj_id).order_by("plan_name")[start:end]
        data["result"] = []
        for i_case in cases:
            case_lis = []
            if i_case.plan_case_list.all():
                i_ca = i_case.plan_case_list.all()
                for c_data in i_ca:
                    case_lis.append(c_data.id)
            data["result"].append({
                "id":i_case.id,
                "title": i_case.plan_name,
                "charger": i_case.charger,
                "user_name": i_case.user_name,
                "case_list": case_lis,
            })
        return data

    def get_historyplan_list_by_id(self, plan_id):
        data = {"error":""}
        cases = TestplanhistoryInfo.objects.filter(h_testplan_id=plan_id).order_by("-h_datatime")
        data["result"] = []
        for i_case in cases:
            case_lis = []
            if i_case.h_plan_case_list.all():
                i_ca = i_case.h_plan_case_list.all()
                for c_data in i_ca:
                    case_lis.append(c_data.id)
            data["result"].append({
                "id": i_case.id,
                "plan_id": i_case.h_testplan_id,
                "time": i_case.h_datatime,
                "title": i_case.h_plan_name,
                "charger": i_case.h_charger,
                "user_name": i_case.h_user_name,
                "version": i_case.h_version,
                "case_list": case_lis,
            })
        return data

    def get_one_testplan(self, _id):
        data = {"error": ""}
        case_lis = []
        data["result"] = []
        if TestplanInfo.objects.filter(pk=_id):
            plan = TestplanInfo.objects.get(pk=_id)
            if plan.plan_case_list.all():
                i_ca = plan.plan_case_list.all()
                for c_data in i_ca:
                    case_lis.append({
                        "id": c_data.id,
                        "source_id": c_data.source_case_id,
                        "version": c_data.case_version,
                    })
            data["result"].append({
                "id": plan.id,
                "title": plan.plan_name,
                "charger": plan.charger,
                "user_name": plan.user_name,
                "case_list": case_lis,
            })
        else:
            data["error"] = "NG"
        return data

    def get_allcase_on_testplan(self, result_plan_id):
        data = {"error": ""}
        case_lis = []
        name_list = []
        data["result"] = []
        if TestplanhistoryInfo.objects.filter(pk=result_plan_id):
            plan = TestplanhistoryInfo.objects.get(pk=result_plan_id)

            if plan.h_plan_case_list.all():
                i_ca = plan.h_plan_case_list.all()
                if PlanFieldSetting.objects.filter(plan=plan.h_testplan):
                    setting = PlanFieldSetting.objects.get(plan=plan.h_testplan)
                    for c_data in i_ca:
                        lol = []
                        fs = {}
                        if TestresultInfo.objects.filter(case_id=c_data.id, result_plan=plan):
                            statue = TestresultInfo.objects.filter(case_id=c_data.id, result_plan=plan).order_by("-update_datetime")[0]
                            fields = ResultfieldInfo.objects.filter(result_case=statue)
                            for i_set in setting.field_list.all():
                                fs.setdefault(i_set.field_en_name, "")
                                lol.append({"en_name": i_set.field_en_name,"name": i_set.field_name,"value": ""})
                            for i_fd in fields:
                                fs[i_fd.field.field_en_name] = i_fd.field_value
                                for i_f in lol:
                                    if i_f["name"] == i_fd.field.field_name:
                                        i_f["value"] = i_fd.field_value
                            case_lis.append({
                                "id": c_data.id,
                                "title": c_data.case_name,
                                "charger": c_data.charger,
                                "case_version": c_data.case_version,
                                "importance": c_data.case_importance,
                                "test_mode": c_data.case_test_mode,
                                "state": statue.result_value,
                                "update_time": statue.update_datetime,
                                "field_list": lol,
                                "field_list_two": fs,
                            })
                        else:
                            for i_set in setting.field_list.all():
                                fs.setdefault(i_set.field_en_name, "")
                                lol.append({"en_name": i_set.field_en_name,"name": i_set.field_name,"value": ""})
                            case_lis.append({
                                "id": c_data.id,
                                "title": c_data.case_name,
                                "charger": c_data.charger,
                                "case_version": c_data.case_version,
                                "importance": c_data.case_importance,
                                "test_mode": c_data.case_test_mode,
                                "state": "",
                                "update_time": "",
                                "field_list": lol,
                                "field_list_two": fs,
                            })
                    for i_set in setting.field_list.all():
                        name_list.append({"en_name": i_set.field_en_name, "name": i_set.field_name, })
                else:
                    for c_data in i_ca:
                        lol = []
                        fs = {}
                        if TestresultInfo.objects.filter(case_id=c_data.id, result_plan=plan):
                            statue = TestresultInfo.objects.filter(case_id=c_data.id, result_plan=plan).order_by("-update_datetime")[0]
                            case_lis.append({
                                "id": c_data.id,
                                "title": c_data.case_name,
                                "charger": c_data.charger,
                                "case_version": c_data.case_version,
                                "importance": c_data.case_importance,
                                "test_mode": c_data.case_test_mode,
                                "state": statue.result_value,
                                "update_time": statue.update_datetime,
                                "field_list": lol,
                                "field_list_two": fs,
                            })
                        else:
                            case_lis.append({
                                "id": c_data.id,
                                "title": c_data.case_name,
                                "charger": c_data.charger,
                                "case_version": c_data.case_version,
                                "importance": c_data.case_importance,
                                "test_mode": c_data.case_test_mode,
                                "state": "",
                                "update_time": "",
                                "field_list": lol,
                                "field_list_two": fs,
                            })
            data["result"].append({
                "id": plan.id,
                "title": plan.h_plan_name,
                "charger": plan.h_charger,
                "creattime":plan.h_datatime,
                "user_name": plan.h_user_name,
                "case_list": case_lis,
                "name_list": name_list,
            })
        else:
            data["error"] = "NG"
        return data

    def get_one_case_on_testplan(self, plan_id, case_id):
        data = {"error": ""}
        step_list = []
        data["result"] = []
        if TestplanInfo.objects.filter(pk=plan_id):
            plan = TestplanInfo.objects.get(pk=plan_id)
            if plan.plan_case_list.filter(id=case_id):
                i_ca = plan.plan_case_list.filter(id=case_id)
                for c_data in i_ca:
                    field_list = []
                    fileds = c_data.case_model.field_list.filter(field_show_when_execute=True)
                    for i_fid in fileds:
                        ct_lis = []
                        if i_fid.field_option_list.all():
                            cct = i_fid.field_option_list.all()
                            for ct in cct:
                                ct_lis.append({'id': str(ct.id), 'label': ct.option_value})
                        if i_fid.field_type == "multiSelect":
                            field_list.append({
                                "id": i_fid.id,
                                "name": i_fid.field_name,
                                "type": i_fid.field_type,
                                "is_show": i_fid.field_show_when_execute,
                                "option_list": ct_lis,
                                "sort_num": i_fid.sort_num,
                                "field_open_use": i_fid.field_open_use,
                                "field_value": [],
                            })
                        else:
                            field_list.append({
                                "id": i_fid.id,
                                "name": i_fid.field_name,
                                "type": i_fid.field_type,
                                "is_show": i_fid.field_show_when_execute,
                                "option_list": ct_lis,
                                "sort_num": i_fid.sort_num,
                                "field_open_use": i_fid.field_open_use,
                                "field_value": '',
                            })
                    if c_data.case_step_list.all():
                        cct = c_data.case_step_list.all()
                        for ct in cct:
                            step_list.append({
                                "id": ct.id,
                                "order": ct.order,
                                "operate": ct.operate,
                                "expected_value": ct.expected_value,
                                "is_automatically": ct.is_automatically,
                                "step_remark":ct.step_remark,
                                "step_state":ct.step_state,
                            })
                    data["result"].append({
                        "id": c_data.id,
                        "title": c_data.case_name,
                        "abstract": c_data.case_abstract,
                        "premise": c_data.case_premise,
                        "case_version": c_data.case_version,
                        "importance": c_data.case_importance,
                        "test_mode": c_data.case_test_mode,
                        "case_model": c_data.case_model.id,
                        "step_list": step_list,
                        "field_list": field_list,
                        "result_value":"",
                        "result_commiter":"",
                        "result_remarks":"",
                    })
        else:
            data["error"] = "NG"
        return data

    def get_PlanSetting_options(self, _id):
        data = {"error": ""}
        if TestplanInfo.objects.filter(pk=_id):
            PlanData = TestplanInfo.objects.get(pk=_id)
            if PlanData.plan_case_list.all():
                mod_list = []
                fi_list = []
                fields = []
                for i_case in PlanData.plan_case_list.all():
                    mod_list.append(i_case.case_model.id)
                for i_mod in list(set(mod_list)):
                    Mdata = ModelInfo.objects.get(pk=i_mod)
                    for i_f in Mdata.field_list.all():
                        fi_list.append(i_f.id)
                for i in list(set(fi_list)):
                    field = FieldInfo.objects.get(pk=i)
                    fields.append({
                        "id": field.id,
                        "field_name": field.field_name,
                        "field_en_name": field.field_en_name,
                    })
                data["result"] = fields
        else:
            data["error"] = "此计划无配置"
        return data


    def get_PlanSetting_by_id(self, _id):
        data = {"error": ""}
        checked_list = []
        if PlanFieldSetting.objects.filter(plan=TestplanInfo.objects.get(pk=_id)):
            ChangeData = PlanFieldSetting.objects.get(plan=TestplanInfo.objects.get(pk=_id))
            for i_fd in ChangeData.field_list.all():
                checked_list.append({
                    "id": i_fd.id,
                    "field_name": i_fd.field_name,
                    "field_en_name": i_fd.field_en_name,
                })
        data["result"] = checked_list
        return data


    def add_or_change_PlanSetting(self, json, _id):
        data = {"error": ""}
        with transaction.atomic():
            if not PlanFieldSetting.objects.filter(plan=TestplanInfo.objects.get(pk=_id)):
                ChangeData = PlanFieldSetting(plan=TestplanInfo.objects.get(pk=_id))
                ChangeData.save()
                for i_fd in json:
                    ChangeData.field_list.add(FieldInfo.objects.get(pk=i_fd.get("id")))
                ChangeData.save()
                data["result"] = "OK"
            else:
                ChangeData = PlanFieldSetting.objects.get(plan=TestplanInfo.objects.get(pk=_id))
                if ChangeData.field_list.all():
                    ChangeData.field_list.clear()
                for i_fd in json:
                    ChangeData.field_list.add(FieldInfo.objects.get(pk=i_fd.get("id")))
                ChangeData.save()
                data["result"] = "OK"
        return data


    def add_testplan(self, json):
        data = {"error": ""}
        with transaction.atomic():
            if not TestplanInfo.objects.filter(plan_name=json["title"], proj=ProjInfo.objects.get(pk=json["proj_id"])):
                ChangeData = TestplanInfo(plan_name=json["title"], charger=json["charger"],
                                          user_name=json["user_name"],
                                          proj=ProjInfo.objects.get(pk=json["proj_id"]))
                ChangeData.save()
                for i_plan in json["case_list"]:
                    ChangeData.plan_case_list.add(TestcaseInfo.objects.get(pk=i_plan.get("id")))
                ChangeData.save()
                if json.get("jenkins"):
                    self.create_jenkins_job(json["jenkins"], ChangeData.id)
                data["result"] = "OK"
            else:
                data["error"] = "此计划已存在"
        return data

    def add_plan_history(self, data_json):
        data = {"error": ""}
        with transaction.atomic():
            if TestplanInfo.objects.filter(pk=data_json.get("plan_id")):
                planData = TestplanInfo.objects.get(pk=data_json.get("plan_id"))
                ChangeData = TestplanhistoryInfo(h_plan_name=planData.plan_name, h_charger=planData.charger,
                                          h_user_name=data_json.get("user_name"), h_testplan=planData, h_version=0,
                                          h_datatime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                          h_proj=planData.proj)
                ChangeData.save()
                if TestplanhistoryInfo.objects.filter(h_testplan=planData):
                    ver_list = TestplanhistoryInfo.objects.filter(h_testplan=planData).order_by("-h_version")[0]
                    ChangeData.h_version = ver_list.h_version+1
                for i_plan in planData.plan_case_list.all():
                    ChangeData.h_plan_case_list.add(i_plan)
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "未找到此计划"
        return data

    def change_testplan(self, json, _id):
        data = {"error": ""}
        with transaction.atomic():
            if TestplanInfo.objects.filter(pk=_id):
                ChangeData = TestplanInfo.objects.get(pk=_id)
                if ChangeData.plan_case_list.all():
                    ChangeData.plan_case_list.clear()
                # ChangeData.plan_name = json["title"]
                ChangeData.charger = json["charger"]
                ChangeData.user_name = json["user_name"]
                if json["case_list"]:
                    for i_plan in json["case_list"]:
                        ChangeData.plan_case_list.add(TestcaseInfo.objects.get(pk=i_plan.get("id")))
                ChangeData.save()
                data["result"] = "OK"
            else:
                data["error"] = "未找到此计划"
        return data


    def batch_delete(self, json):
        data = {"error":""}
        with transaction.atomic():
            for i_data in json["dellist"]:
                ChangeData = TestplanInfo.objects.get(pk=i_data)
                if ChangeData:
                    ChangeData.delete()
            data["count"] = TestplanInfo.objects.count()
            data["result"] = "DELETE OK"
        return data


    def batch_delete_history(self, json):
        data = {"error":"","count":0}
        with transaction.atomic():
            for i_data in json["dellist"]:
                ChangeData = TestplanhistoryInfo.objects.get(pk=i_data)
                if ChangeData:
                    ChangeData.delete()
            data["count"] = TestplanhistoryInfo.objects.count()
            data["result"] = "DELETE OK"
        return data


    def search_tsetplan(self, json, page, size):
        data = {"error": ""}
        if json:
            search_list = self.link_option_type(json)
            if search_list:
                SearchData = TestplanInfo.objects.all().order_by("plan_name")
                for ida in search_list:
                    app = {}
                    if ida.get("is_equal"):
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.filter(**app)
                    else:
                        app[ida.get("name")] = ida.get("val")
                        SearchData = SearchData.exclude(**app)
                start = (page - 1) * size
                data["count"] = SearchData.count()
                end = min((page - 1) * size + size, data["count"])
                cases = SearchData.order_by("plan_name")[start:end]
                data["result"] = self.data_to_json(cases)
        else:
            data["error"] = "请不要传空数据"
        return data

    def link_option_type(self, data):
        title = "plan_name"
        charger = "charger"
        user_name = "user_name"
        contains = "__icontains"
        se_list = []

        for i_da in data:
            con = ""
            reback = ""
            if i_da.get("type") == "title":
                con = "{}".format(title)
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
            elif i_da.get("type") == "charger":
                con = "{}".format(charger)
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
                con = "{}".format(user_name)
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

    def data_to_json(self, data):
        search_list = []
        for i_data in data:
            case_list = []
            if i_data.plan_case_list.all():
                cas = i_data.plan_case_list.all()
                for i_ca in cas:
                    case_list.append(i_ca.id)
            search_list.append({
                "id":i_data.id,
                "title": i_data.plan_name,
                "charger": i_data.charger,
                "user_name": i_data.user_name,
                "case_list": case_list,
            })
        return search_list

    # create_jenkins_job
    def create_jenkins_job(self, data, _id):
        J = self.jenkins
        job_name = data.get('job_name')
        # 获取模板
        sample_job = J.get_job('sample_job')
        xml = sample_job.get_config()
        root = et.fromstring(xml.strip())
        # 下面的修改:节点(执行机)
        node = root.find('assignedNode')
        #  换成自己的节点
        node.text = data.get('node')
        #  创建新的job
        new_conf = et.tostring(root, encoding='unicode')
        new_job = J.create_job(job_name, new_conf)
        print(new_job)
        with transaction.atomic():
            ChangeData = JenkinsCreateJob(job_name=data.get('job_name'), node=data.get('node'),
                                      plan=TestplanInfo.objects.get(pk=_id))
            ChangeData.save()


    def get_jenkins_node(self):
        J = self.jenkins
        # 获取节点
        list = []
        for node_id, node in J.get_nodes().iteritems():
            list.append({
                'node': node_id
            })
        return list