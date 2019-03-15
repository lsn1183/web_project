#-*- coding:utf-8 –*-
'''
Created on JUE 18, 2016

@author: xieyi
'''

import traceback
import logging

import flask
import sys
default_encoding = 'utf-8'
#print sys.getdefaultencoding()
reload(sys) 
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()
from ..storage.interface import StorageIF
import xml2dict;
import json;
import os
import types,subprocess,time,threading

class RestApi(object):
    def __init__(self, app):
        pass

    def connect_engine(self):
        pass

    def index(self):
         print 'view'
         return "Hello World!" 
	#test_plan_inte = TestPlanInte()
         #res = test_plan_inte.get_caseslist_for_point()
         #print res
         #return res
