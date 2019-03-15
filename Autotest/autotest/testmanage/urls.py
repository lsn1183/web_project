# -*- coding: UTF-8 -*-
from django.conf.urls import url
from django.urls import path
from testmanage import views

app_name = 'testmanage'
urlpatterns = [
    path('CountryList', views.CountryList),
    path('CountrySearch', views.CountrySearch),
    path('ImportExcle', views.ImportExcle),
    path('ExportExcle', views.ExportExcle),
    path('BatchDeleteCountry', views.BatchDeleteCountry),
    path('CountryInfo/<int:country_id>', views.ChangeCountry),

    path('DestList', views.DestList),
    path('DestInfo/<int:Dest_id>', views.ChangeDest),
    path('DestSearch', views.DestSearch),
    path('BatchDeleteDest', views.BatchDeleteDest),

    path('KeywordList', views.KeywordList),
    path('KeywordInfo/<int:Keyword_id>', views.ChangeKeyword),
    path('KeywordSearch', views.KeywordSearch),
    path('BatchDeleteKeyword', views.BatchDeleteKeyword),

    path('FieldList', views.FieldList),
    path('FieldInfo/<int:Field_id>', views.ChangeField),
    path('BatchDeleteField', views.BatchDeleteField),
    path('FieldSearch', views.FieldSearch),

    path('ProjList', views.ProjList),
    path('Projects', views.projects),
    path('ProjTree/<int:Proj_id>', views.ProjListTree),
    path('ProjInfo/<int:Proj_id>', views.ChangeProj),
    path('BatchDeleteProj', views.BatchDeleteProj),
    path('ProjSearch', views.ProjSearch),
    path('ImportYaml', views.ImportYaml),
    path('ExportYaml/<int:Proj_id>', views.ExportYaml),

    path('ModuleList/<int:Proj_id>', views.ModuleList),
    path('ModuleAdd', views.ModuleAdd),
    path('ModuleInfo/<int:id>', views.ChangeModule),
    path('ChangeModuleInfo/<int:id>', views.ChangeModuleInfo),
    path('GetFieldsByProj/<int:id>', views.GetFieldsByProj),
    path('ModuleSearch', views.ModuleSearch),
    path('BatchDeleteModule', views.BatchDeleteModule),

    path('CaseTree/<int:id>', views.GetCaseTree),
    path('ModuleTree/<int:id>', views.GetModuleTree),
    path('GetCactusProj', views.GetCactusProj)
]
