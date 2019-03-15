from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$',views.index, name='index'),
    # url(r'^signin.html',views.signin, name='signin'),
    # url(r'^signout.html',views.signout, name='signout'),
    url(r'^catalogTreeData.html',views.catalogTreeData, name='catalogTreeData'),
    url(r'^contentData.html',views.contentData, name='contentData'),
    url(r'^translation.html',views.translation, name='translation'),
    url(r'^img.html',views.img, name='img'),
    url(r'^model.html',views.model, name='model'),
    url(r'^relateDef.html',views.relateDef, name='relateDef'),
    url(r'^relateAnalysis.html',views.relateAnalysis, name='relateAnalysis'),
    url(r'^relateReq.html',views.relateReq, name='relateReq'),
    url(r'^search.html',views.search, name='search'),
    # url(r'^detail.html',views.detail, name='detail'),
    url(r'^dataView.html',views.dataView, name='dataView'),
]
