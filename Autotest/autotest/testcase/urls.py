# -*- coding: UTF-8 -*-
# from django.conf.urls import url
from django.urls import path
from django.urls import re_path
from testcase import views
from django.conf.urls.static import static, serve
from django.conf import settings

urlpatterns = [
    path('AllTestcaseList/<int:page>/<int:size>', views.AllTestcaseList),
    path('TestcaseListAll/<int:Proj_id>/', views.TestcaseListAll),
    path('TestcaseModelList/<int:Model_id>/<int:page>/<int:size>', views.TestcaseModelList),
    path('TestcaseProjList/<int:Proj_id>/<int:page>/<int:size>', views.TestcaseProjList),
    path('TestcaseOne/<int:Testcase_id>', views.TestcaseOne),
    path('Showthreelist/<int:Model_id>', views.Getthreelist),

    path('TestcaseAdd/<int:Model_id>', views.TestcaseAdd),
    path('TestcaseVerUp/<int:Testcase_id>', views.TestcaseVerUp),
    path('TestcaseInfo/<int:Testcase_id>', views.ChangeTestcase),
    path('BatchDeleteTestcase', views.BatchDeleteTestcase),

    path('TestcaseSearch/<int:page>/<int:size>', views.search_tsetcase),
    path('TestcaseSearch', views.search_tsetcase_no_page),
    path('ProjTestcaseSearch/<int:p_id>/<int:page>/<int:size>', views.search_tsetcase_by_proj),
    path('ModelTestcaseSearch/<int:m_id>/<int:page>/<int:size>', views.search_tsetcase_by_model),

    path('TestplanList/<int:Proj_id>/<int:page>/<int:size>', views.TestplanList),
    path('TestplanAdd', views.TestplanAdd),
    path('TestplanHistoryAdd', views.TestplanHistoryAdd),
    path('TestplanHistoryList/<int:plan_id>', views.TestplanHistoryList),
    path('TestplanInfo/<int:Testplan_id>', views.ChangePlan),
    path('TestplanSearch/<int:page>/<int:size>', views.Search_Tsetplan),
    path('BatchDeleteTestplan', views.BatchDeletePlan),
    path('BatchDeleteTestplanHistory', views.BatchDeleteTestplanHistory),

    path('SettingOption/<int:Testplan_id>', views.SettingOption),
    path('TestplanSettingInfo/<int:plan_id>', views.ChangePlanSetting),
    # 创建jenkins_job
    path('CreateJenkinsJob', views.CreateJenkinsJob),
    #  获取所有节点
    path('GetJenkinsNode', views.GetJenkinsNode),

    path('TestresultHistory/<int:result_plan_id>/<int:case_id>', views.TestresultHistory),
    path('TestresultHistoryOne/<int:result_case_id>', views.TestresultHistoryOne),
    path('TestresultList/<int:result_plan_id>', views.TestresultList),
    path('TestresultOne/<int:plan_id>/<int:case_id>', views.TestresultOne),
    path('TestresultAdd/<int:result_plan_id>/<int:case_id>', views.TestresultAdd),
    # path('TestresultInfo/<int:Testresult_id>', views.ChangeTestresult),
    path('BatchDeleteTestresult', views.BatchDeleteTestresult),

    path('UploadImg', views.UploadImg),
    path('LineChart', views.LineChart),
    path('LineChart/<username>', views.LineChart),
    path('StackChart', views.StackChart),
    path('StackChart/<username>', views.StackChart),
    path('PieChart', views.PieChart),
    path('PieChart/<username>', views.PieChart),
    path('TcHistoryVer/<int:source_case_id>', views.TcHistoryVer),
    path('TcVerDiff/<int:case_id>', views.TcVerDiff),
    path('TcVerDiff/<int:case_id>/<int:lefet_ver>/<int:right_ver>', views.TcVerDiff),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]