from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.db import connections
from django.db import transaction
from django.http import HttpResponse
import json
import re
# Create your views here.
# @login_required
def index(request):
    return render(request, 'index.html')
# def detail(request):
#     return render(request, 'detail.html')
def dataView(request):
    return render(request, 'dataView.html')

# def signin(request):
#     if request.method == 'GET':
#         return render(request, 'signin.html')
#         # username = "admin"  # request.POST['username']
#         # password = "admin"  # request.POST['password']
#         # user = authenticate(request, username=username, password=password)
#         # return redirect('/doctree/')
#     elif request.method == 'POST':
#         username = "admin"#request.POST['username']
#         password = "admin"#request.POST['password']
#         user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/doctree/')
#         # return render(request, 'signin.html')
#
#     else:
#         # return redirect('/doctree/')
#         return render(request, 'signin.html')
# def signout(request):
#     logout(request)
#     return redirect('/doctree/signin.html')

def catalogTreeData(request):
    if request.method == 'GET':
        docType = request.GET.get('t')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record=[]
        try:
            if docType=="1":
                sql_1="SELECT ope_spec_id, ope_name FROM ope_spec ORDER BY ope_spec_id"
                c.execute(sql_1)
                for i in c.fetchall():
                    if i:
                        record.append({ "id" : str(i[0])+"_0", "parent" : "#", "text" : str(i[1])})
                        sql_1="SELECT t1.ope_spec_id,t2.ope_screen_id, t2.screen_no, t2.screen_name FROM ope_spec_screen_rel AS t1 LEFT JOIN ope_screen AS t2 ON t1.ope_screen_id = t2.ope_screen_id WHERE t1.ope_spec_id = %s ORDER BY t1.order_no"%(str(i[0]))
                        c.execute(sql_1)
                        for i in c.fetchall():
                            if i:
                                record.append({ "id" : str(i[0])+"_"+str(i[1]), "parent" : str(i[0])+"_0", "text" : str(i[2])+":"+str(i[3])})
            else:
                sql_1="SELECT spec_id, spec_num, spec_name FROM spec_specification order by array_to_string(regexp_matches(spec_num , '\d+'),'')::int, substring(spec_num,'\d+$')::int"
                c.execute(sql_1)
                tmpList1=[]
                for i in c.fetchall():
                    if i:
                        record.append({ "id" : str(i[0])+"_0", "parent" : "#", "text" : str(i[1])+":"+str(i[2]) })
                        tmpList1.append(str(i[0]))
                sql_1="SELECT t1.spec_id, t1.chapter_id, t2.chapter_number, t2.title FROM spec_spec_chapter_rel AS t1 LEFT JOIN spec_chapter AS t2 ON t1.chapter_id = t2.chapter_id WHERE t1.spec_id IN (%s) ORDER BY t1.order_no" % ",".join(tmpList1)
                c.execute(sql_1)
                tmpDict1={}
                for i in c.fetchall():
                    if i:
                        record.append({ "id" : str(i[0])+"_"+str(i[1]), "parent" : str(i[0])+"_0", "text" : str(i[2])+":"+str(i[3])})
                        tmpDict1[str(i[1])]=str(i[0])
                while True:
                    sql_1="SELECT t1.parent_chapter_id, t2.chapter_id, t2.chapter_number, t2.title FROM spec_chapter_chapter_rel AS t1 LEFT JOIN spec_chapter AS t2 ON t1.child_chapter_id = t2.chapter_id WHERE t1.parent_chapter_id IN (%s) ORDER BY t1.order_no"%",".join(tmpDict1.keys())
                    c.execute(sql_1)
                    if c.rowcount > 0 :
                        tmpDict2={}
                        for i in c.fetchall():
                            record.append({ "id" : tmpDict1[str(i[0])]+"_"+str(i[1]), "parent" : tmpDict1[str(i[0])]+"_"+str(i[0]), "text" : str(i[2])+":"+str(i[3])})
                            tmpDict2[str(i[1])]=tmpDict1[str(i[0])]
                        tmpDict1=tmpDict2
                    else:
                        break
        finally:
            c.close()

        return HttpResponse(json.dumps(record))

def contentData(request):
    if request.method == 'GET':
        docType = request.GET.get('t')
        catalogTreeID = request.GET.get('id')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record={}
        try:
            if docType=="1":
                chapter_id = catalogTreeID.split('_')
                if chapter_id[1]=='0':
                    sql_1="SELECT file_name FROM ope_spec WHERE ope_spec_id = %s"%(str(chapter_id[0]))
                    c.execute(sql_1)
                    i=c.fetchone()
                    record['type']=0
                    record['data']={"file_name":i[0]}
                else:
                    sql_1="SELECT t2.operation_id ,t2.title ,t2.view_img_id ,t2.action_img_id ,t2.ref_img_id FROM ope_screen_operation_rel AS t1 LEFT JOIN ope_operation AS t2 ON t1.ope_operation_id = t2.operation_id WHERE t1.ope_screen_id = %s ORDER BY t1.order_no"%(str(chapter_id[1]))
                    c.execute(sql_1)
                    record['type']=1
                    record['data']=[]
                    tmpList1=[]
                    for i in c.fetchall():
                        record['data'].append({"id":i[0],"parent":"#","title":i[1],"view_img_id":i[2],"action_img_id":i[3],"ref_img_id":i[4]})
                        tmpList1.append(str(i[0]))
                    while True:
                        sql_1="SELECT t1.parent_operation_id,t2.operation_id, t2.title, t2.view_img_id, t2.action_img_id, t2.ref_img_id FROM ope_operation_rel AS t1 LEFT JOIN ope_operation AS t2 ON t1.child_operation_id = t2.operation_id WHERE t1.parent_operation_id IN (%s) ORDER BY t1.order_no"%(",".join(tmpList1))
                        c.execute(sql_1)
                        tmpList1=[]
                        if c.rowcount > 0 :
                            for i in c.fetchall():
                                record['data'].append({"id":i[1],"parent":i[0],"title":i[2],"view_img_id":i[3],"action_img_id":i[4],"ref_img_id":i[5]})
                                tmpList1.append(str(i[1]))
                        else:
                            break
            else:
                spec_id,chapter_id = catalogTreeID.split('_')
                if chapter_id=='0':
                    record['type']=0
                    sql_1="SELECT version, spec_file_name, language FROM spec_specification WHERE spec_id ="+spec_id
                    c.execute(sql_1)
                    i=c.fetchone()
                    record['data']={'version':i[0],'spec_file_name':i[1],'language':i[2]}
                else:
                    sql_1="SELECT chapter_type FROM spec_chapter WHERE chapter_id ="+chapter_id
                    c.execute(sql_1)
                    i=c.fetchone()
                    if i[0]=='terminology':
                        record['type']=1
                        record['data']=[]
                        sql_1="SELECT name, definition FROM spec_terminology_name WHERE chapter_id = %s ORDER BY order_no"%chapter_id
                        c.execute(sql_1)
                        for j in c.fetchall():
                            record['data'].append({'name':eval(j[0]) if j[0] else '','definition':eval(j[1]) if j[1] else ''})
                    elif i[0]=='chapter':
                        record['type']=2
                        record['data']=[]
                        sql_1="SELECT '#' AS parent_function_id,t1.func_id, t2.func_type, t2.func_content,t2.test_type,t2.id FROM spec_chapter_func_rel AS t1 LEFT JOIN spec_functions AS t2 ON t1.func_id = t2.func_id WHERE t1.chapter_id = %s ORDER BY t1.order_no"%chapter_id
                        c.execute(sql_1)
                        if c.rowcount > 0 :
                            tmpList1=[]
                            for j in c.fetchall():
                                record['data'].append({'parent_function_id':j[0],'func_id':j[1],'func_type':j[2],'func_content':eval(j[3]) if j[3] else '','test_type':j[4],'id':j[5] if j[5] else None,'spec_def_count':0,'spec_analysis_count':0,'spec_req_title':[],'has_model':False})
                                tmpList1.append(str(j[1]))
                            while True:
                                sql_1="SELECT t1.parent_func_id, t2.func_id, t2.func_type, t2.func_content,t2.test_type,t2.id,t2.parent_chapter_num FROM spec_func_func_rel AS t1 LEFT JOIN spec_functions AS t2 ON t1.child_func_id = t2.func_id WHERE t1.parent_func_id IN (%s) ORDER BY order_no"%",".join(tmpList1)
                                c.execute(sql_1)
                                tmpList1=[]
                                if c.rowcount > 0 :
                                    for j in c.fetchall():
                                        tmpDict1={'parent_function_id':j[0],'func_id':j[1],'func_type':j[2],'func_content':eval(j[3]) if j[3] else '','test_type':j[4],'id':j[5] if j[5] else None,'spec_def_count':0,'spec_analysis_count':0,'spec_req_title':[],'has_model':False}
                                        if j[5] and j[6]:
                                            sql_1="SELECT DISTINCT(detail) FROM requirement_def_record WHERE id ='%s' AND spec_chapter_num ='%s'"%(str(j[5]),str(j[6]))
                                            c.execute(sql_1)
                                            if c.rowcount > 0 :
                                                tmpDict1['spec_def_count']=c.rowcount
                                            sql_1="SELECT DISTINCT(detail) FROM analysis_spec_record WHERE id ='%s' AND spec_chapter_num ='%s'"%(str(j[5]),str(j[6]))
                                            c.execute(sql_1)
                                            if c.rowcount > 0 :
                                                tmpDict1['spec_analysis_count']=c.rowcount
                                            sql_1 = "SELECT req_chapter_title, url FROM seq_spec_record WHERE ID = '%s' AND spec_chapter_num = '%s'" % (str(j[5]), str(j[6]))
                                            c.execute(sql_1)
                                            if c.rowcount > 0 :
                                                for k in c.fetchall():
                                                    tmpDict1['spec_req_title'].append([str(k[0]),str(k[1])])
                                        sql_1="SELECT * FROM spec_func_model_rel WHERE func_id =%s"%str(j[1])
                                        c.execute(sql_1)
                                        if c.rowcount > 0:
                                            tmpDict1['has_model']=True
                                        record['data'].append(tmpDict1)
                                        tmpList1.append(str(j[1]))
                                else:
                                    break
        finally:
            c.close()
            print (c,"1111")
        return HttpResponse(json.dumps(record))
def translation(request):
    c = connections['spec'].cursor()
    c.execute('SET search_path TO spec')
    try:
        sql_1="SELECT key, val FROM spec_key_table"
        c.execute(sql_1)
        record={}
        for i in c.fetchall():
            if i:
                record[i[0]]=i[1]
    finally:
        c.close()
    return HttpResponse(json.dumps(record))
def img(request):
    if request.method == 'GET':
        docType = request.GET.get('t')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        try:
            if docType=="1":
                imgID= request.GET.get('id')
                sql_1="SELECT image_blob,image_type FROM spec_image WHERE image_id = %s"%(imgID)
                c.execute(sql_1)
                i=c.fetchone()
                imgType=i[1]
                imgDT=i[0]
            else:
                tmpList1= request.GET.get('img').split('.')
                imgName='.'.join(tmpList1[:-1])
                imgType='.'+tmpList1[-1]
                sql_1="SELECT image_blob FROM spec_image WHERE image_name = '%s' AND image_type = '%s'"%(imgName,imgType)
                c.execute(sql_1)
                imgDT=c.fetchone()[0]
        finally:
            c.close()
        return HttpResponse(imgDT,content_type="image/"+imgType.strip('.'))
def model(request):
    if request.method == 'GET':
        func_id= request.GET.get('func_id')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record={}
        try:
            sql_1="SELECT t2.model, t1.val FROM spec_func_model_rel AS t1 LEFT JOIN spec_model AS t2 ON t1.model_id = t2.model_id WHERE t1.func_id = %s ORDER BY order_no" %func_id
            c.execute(sql_1)
            if c.rowcount != 0 :
                tmpList1=[]
                record['searchList']=[]
                for i in c.fetchall():
                    tmpList2=i[0].split('-')
                    if i[1] not in record['searchList']:
                        record['searchList'].append(i[1])
                    for k,v in enumerate(tmpList2):
                        if v not in record['searchList']:
                            record['searchList'].append(v)
                        if k==0:
                            v = v if v else '-'
                            tmpDict1={"parent": "#","id":'-'.join(tmpList2[:k+1]),"text":v}
                            if tmpDict1 not in tmpList1:
                                tmpList1.append(tmpDict1)
                        elif k==len(tmpList2)-1:
                            tmpDict1={"parent": '-'.join(tmpList2[:k]),"id":'-'.join(tmpList2[:k+1]),"text":'%s<div id="leafNode">%s</div>'%(v,i[1])}
                            if tmpDict1 not in tmpList1:
                                tmpList1.append(tmpDict1)
                        else:
                            tmpDict1={"parent": '-'.join(tmpList2[:k]),"id":'-'.join(tmpList2[:k+1]),"text":v}
                            if tmpDict1 not in tmpList1:
                                tmpList1.append(tmpDict1)
                record['data']=tmpList1
        finally:
            c.close()

        return HttpResponse(json.dumps(record))

@csrf_exempt
def relateDef(request):
    if request.method == 'GET':
        func_id = request.GET.get('func_id')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record=[]
        try:
            sql_1="SELECT author_name, hu_def_id, requirement_id, unique_id, major_category, medium_catetory, small_category, detail, base, rel_requiremant, dcu_status, dcu_trigger, dcu_action, meu_status, meu_trigger, meu_action, hu_req_remark, dcu_meu, pf_status, pf_trigger, pf_action, device_types, vals, remark, notice, rel_flow_diagram, rel_hal_design, other_spec, implementation, analysis, unrequire,t1.req_def_id FROM requirement_def_record AS t1 LEFT JOIN ( SELECT req_def_id, ARRAY_AGG(device_type) AS device_types, ARRAY_AGG(val) AS vals FROM ( SELECT order_no, req_def_id, device_type, val FROM requirement_def_device ORDER BY req_def_id, order_no ) AS t2 GROUP BY req_def_id ) AS t3 ON t1.req_def_id = t3.req_def_id WHERE (t1.id, t1.spec_chapter_num) IN ( SELECT id, parent_chapter_num FROM spec_functions WHERE func_id = % s )"%(func_id)
            c.execute(sql_1)
            if c.rowcount > 0 :
                for i in c.fetchall():
                    tmpDict1={}
                    tmpDict1["author_name"]=i[0]
                    tmpDict1["hu_def_id"]=i[1]
                    tmpDict1["requirement_id"]=i[2]
                    tmpDict1["unique_id"]=i[3]
                    tmpDict1["major_category"]=i[4]
                    tmpDict1["medium_catetory"]=i[5]
                    tmpDict1["small_category"]=i[6]
                    tmpDict1["detail"]=i[7]
                    tmpDict1["base"]=i[8]
                    tmpDict1["rel_requiremant"]=i[9]
                    tmpDict1["dcu_status"]=i[10]
                    tmpDict1["dcu_trigger"]=i[11]
                    tmpDict1["dcu_action"]=i[12]
                    tmpDict1["meu_status"]=i[13]
                    tmpDict1["meu_trigger"]=i[14]
                    tmpDict1["meu_action"]=i[15]
                    tmpDict1["hu_req_remark"]=i[16]
                    tmpDict1["dcu_meu"]=i[17]
                    tmpDict1["pf_status"]=i[18]
                    tmpDict1["pf_trigger"]=i[19]
                    tmpDict1["pf_action"]=i[20]
                    tmpDict1["device_types"]=i[21]
                    tmpDict1["vals"]=i[22]
                    tmpDict1["remark"]=i[23]
                    tmpDict1["notice"]=i[24]
                    tmpDict1["rel_flow_diagram"]=i[25]
                    tmpDict1["rel_hal_design"]=i[26]
                    tmpDict1["other_spec"]=i[27]
                    tmpDict1["implementation"]=i[28]
                    tmpDict1["analysis"]=i[29]
                    tmpDict1["unrequire"]=i[30]
                    tmpDict1["req_def_id"]=i[31]
                    record.append(tmpDict1)
        finally:
            c.close()
        return HttpResponse(json.dumps(record))
    elif request.method == 'POST':
        savedFlag=False
        record=json.loads(request.body)
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        try:
            with transaction.atomic():
                sql_1="UPDATE requirement_def_record SET (author_name ,hu_def_id ,requirement_id ,major_category ,medium_catetory ,small_category ,detail ,base ,rel_requiremant ,dcu_status ,dcu_trigger ,dcu_action ,meu_status ,meu_trigger ,meu_action ,hu_req_remark ,dcu_meu ,pf_status ,pf_trigger ,pf_action ,remark ,notice ,rel_flow_diagram ,rel_hal_design ,other_spec ,implementation ,analysis ,unrequire ,unique_id) = ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s) WHERE req_def_id =%s"%(record["author_name"], record["hu_def_id"], record["requirement_id"], record["major_category"], record["medium_catetory"], record["small_category"], record["detail"], record["base"], record["rel_requiremant"], record["dcu_status"], record["dcu_trigger"], record["dcu_action"], record["meu_status"], record["meu_trigger"], record["meu_action"], record["hu_req_remark"], record["dcu_meu"], record["pf_status"], record["pf_trigger"], record["pf_action"], record["remark"], record["notice"], record["rel_flow_diagram"], record["rel_hal_design"], record["other_spec"], record["implementation"], record["analysis"], record["unrequire"], record["unique_id"], record["req_def_id"])
                c.execute(sql_1)
                for i in range(len(record["device_types"])):
                    sql_1="UPDATE requirement_def_device SET (val)=('%s') WHERE device_type='%s' AND req_def_id =%s"%(record["vals"][i],record["device_types"][i],record["req_def_id"])
                    c.execute(sql_1)
                savedFlag=True
        finally:
            c.close()
            return HttpResponse(json.dumps({"savedFlag":savedFlag}))

@csrf_exempt
def relateAnalysis(request):
    if request.method == 'GET':
        func_id = request.GET.get('func_id')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record=[]
        try:
            sql_1="SELECT author_name, requirement_id, unique_id, major_category, medium_catetory, small_category, detail, base, rel_requiremant, exception, dcu_meu, pf_status, fp_trigger, pf_action, seq_diagram, supple_spec, uncheck, remark, application, kernel, systemd, models, vals,tt1.analysis_id FROM analysis_spec_record AS tt1 LEFT JOIN ( SELECT analysis_id, ARRAY_AGG(model) models, ARRAY_AGG(val) vals FROM ( SELECT order_no, analysis_id, model, val FROM analysis_rc_model_rel AS t1 LEFT JOIN analysis_model AS t2 ON t1.model_id = t2.model_id ORDER BY analysis_id, order_no ) AS tt2 GROUP BY analysis_id ) AS tt3 ON tt1.analysis_id = tt3.analysis_id WHERE ( tt1.id, tt1.spec_chapter_num ) IN ( SELECT id, parent_chapter_num FROM spec_functions WHERE func_id = % s )"%(func_id)
            c.execute(sql_1)
            if c.rowcount > 0 :
                for i in c.fetchall():
                    tmpDict1={}
                    tmpDict1["author_name"]=i[0]
                    tmpDict1["requirement_id"]=i[1]
                    tmpDict1["unique_id"]=i[2]
                    tmpDict1["major_category"]=i[3]
                    tmpDict1["medium_catetory"]=i[4]
                    tmpDict1["small_category"]=i[5]
                    tmpDict1["detail"]=i[6]
                    tmpDict1["base"]=i[7]
                    tmpDict1["rel_requiremant"]=i[8]
                    tmpDict1["exception"]=i[9]
                    tmpDict1["dcu_meu"]=i[10]
                    tmpDict1["pf_status"]=i[11]
                    tmpDict1["fp_trigger"]=i[12]
                    tmpDict1["pf_action"]=i[13]
                    tmpDict1["seq_diagram"]=i[14]
                    tmpDict1["supple_spec"]=i[15]
                    tmpDict1["uncheck"]=i[16]
                    tmpDict1["remark"]=i[17]
                    tmpDict1["application"]=i[18]
                    tmpDict1["kernel"]=i[19]
                    tmpDict1["systemd"]=i[20]
                    tmpDict1["models"]=i[21]
                    tmpDict1["vals"]=i[22]
                    tmpDict1["analysis_id"]=i[23]
                    record.append(tmpDict1)
        finally:
            c.close()
        return HttpResponse(json.dumps(record))
    elif request.method == 'POST':
        savedFlag=False
        record=json.loads(request.body)
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        try:
            with transaction.atomic():
                sql_1="UPDATE analysis_spec_record SET (author_name, requirement_id, major_category, medium_catetory, small_category, detail, base, rel_requiremant, exception, dcu_meu, pf_status, fp_trigger, pf_action, seq_diagram, supple_spec, uncheck, remark, application, kernel, systemd, unique_id) = ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s',%s) WHERE analysis_id =%s"%(record["author_name"], record["requirement_id"], record["major_category"], record["medium_catetory"], record["small_category"], record["detail"], record["base"], record["rel_requiremant"], record["exception"], record["dcu_meu"], record["pf_status"], record["fp_trigger"], record["pf_action"], record["seq_diagram"], record["supple_spec"], record["uncheck"], record["remark"], record["application"], record["kernel"], record["systemd"], record["unique_id"], record["analysis_id"])
                c.execute(sql_1)
                for i in range(len(record["models"])):
                    sql_1="UPDATE analysis_rc_model_rel SET (val) = ('%s') WHERE model_id IN ( SELECT model_id FROM analysis_model WHERE model = '%s' ) AND analysis_id =%s"%(record["vals"][i],record["models"][i],record["analysis_id"])
                    c.execute(sql_1)
                savedFlag=True
        finally:
            c.close()
            return HttpResponse(json.dumps({"savedFlag":savedFlag}))


def relateReq(request):
    if request.method == 'GET':
        func_id = request.GET.get('func_id')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record=[]
        try:
            sql_1="SELECT id, parent_chapter_num FROM spec_functions WHERE func_id = %s "%(func_id)
            c.execute(sql_1)
            if c.rowcount > 0 :
                for i in c.fetchall():
                    sql_1="SELECT t3.req_spec, t3.req_spec_name, t3.req_spec_file_name, t1.no, t1.req_chapter_num, t1.req_chapter_title, t1.req_page, t1.update_date, t1.category, t1.spec_num, t1.spec_file_name, t1.version , t1.spec_chapter_num, t1.spec_chapter_title, t1.need, t1.reason, t1.department, t1.group_name, t1.name, t1.date, t1.remark FROM seq_spec_record AS t1 LEFT JOIN req_spec_rel AS t2 ON t1.req_rc_id = t2.req_rc_id LEFT JOIN req_spec_info AS t3 ON t2.req_spec_id = t3.req_spec_id WHERE t1.spec_chapter_title IN ( SELECT DISTINCT (detail) FROM requirement_def_record WHERE id = '%s' AND spec_chapter_num = '%s' ) AND t1.spec_chapter_num = '%s'"%(i[0],i[1],i[1])
                    c.execute(sql_1)
                    if c.rowcount > 0 :
                        for j in c.fetchall():
                            tmpDict1={}
                            tmpDict1['req_spec']=j[0]
                            tmpDict1['req_spec_name']=j[1]
                            tmpDict1['req_spec_file_name']=j[2]
                            tmpDict1['no']=j[3]
                            tmpDict1['req_chapter_num']=j[4]
                            tmpDict1['req_chapter_title']=j[5]
                            tmpDict1['req_page']=j[6]
                            tmpDict1['update_date']=j[7]
                            tmpDict1['category']=j[8]
                            tmpDict1['spec_num']=j[9]
                            tmpDict1['spec_file_name']=j[10]
                            tmpDict1['version']=j[11]
                            tmpDict1['spec_chapter_num']=j[12]
                            tmpDict1['spec_chapter_title']=j[13]
                            tmpDict1['need']=j[14]
                            tmpDict1['reason']=j[15]
                            tmpDict1['department']=j[16]
                            tmpDict1['group_name']=j[17]
                            tmpDict1['name']=j[18]
                            tmpDict1['date']=j[19]
                            tmpDict1['remark']=j[20]
                            record.append(tmpDict1)
        finally:
            c.close()
        return HttpResponse(json.dumps(record))
def search(request):
    if request.method == 'GET':
        searchKey = request.GET.get('searchKey')
        searchType = request.GET.get('searchType')
        c = connections['spec'].cursor()
        c.execute('SET search_path TO spec')
        record=[]
        try:
            #机能式样书搜索
            if searchType=="1":
                sql_1="SELECT chapter_number, title FROM spec.spec_chapter WHERE chapter_number LIKE '%s' OR title LIKE '%s' order by chapter_number"%(searchKey+"%",searchKey+"%")
                c.execute(sql_1)
                if c.rowcount > 0 :
                    for i in c.fetchall():
                        tmpList1={"spec_chapter_num":i[0], "spec_chapter_title":i[1]}
                        record.append(tmpList1)
            elif searchType=="2":
                sql_1="SELECT DISTINCT spec_chapter_title, t1.spec_chapter_num, t5.id::INT, parsed_content FROM ( SELECT req_rc_id, spec_chapter_num, spec_chapter_title FROM spec.seq_spec_record WHERE spec_chapter_title LIKE '%s' ) AS t1 LEFT JOIN spec.req_spec_rel AS t2 ON t1.req_rc_id = t2.req_rc_id LEFT JOIN spec.req_spec_info AS t3 ON t2.req_spec_id = t3.req_spec_id LEFT JOIN spec.requirement_def_record AS t4 ON t1.spec_chapter_num = t4.spec_chapter_num AND t1.spec_chapter_title = t4.detail LEFT JOIN spec.spec_functions AS t5 ON t4.spec_chapter_num = t5.parent_chapter_num AND t4.id = t5.id ORDER BY t1.spec_chapter_num, t5.id::INT"%("%"+searchKey+"%")
                c.execute(sql_1)
                if c.rowcount > 0 :
                    for i in c.fetchall():
                        tmpList1={"spec_chapter_title":i[0], "spec_chapter_num":i[1], "id":i[2],"func_content":i[3]}
                        record.append(tmpList1)
            #全局搜索
            elif searchType=="3":
                sql_1="SELECT parent_chapter_num, parsed_content FROM spec.spec_functions WHERE parsed_content ILIKE '%s' ORDER BY parent_chapter_num"%("%"+searchKey+"%")
                print ('aaa',sql_1)
                c.execute(sql_1)
                if c.rowcount > 0 :
                    for i in c.fetchall():
                        tmpList1 = {"parent_chapter_num": i[0], "parsed_content": i[1]}
                        record.append(tmpList1)
        finally:
            c.close()
        return HttpResponse(json.dumps(record))
