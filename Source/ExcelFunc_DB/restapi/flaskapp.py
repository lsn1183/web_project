#-*- coding:utf-8 –*-
# This Python file uses the following encoding: utf-8
# encoding: utf-8

'''
Created on JUE 18, 2016

@author: xieyi
'''

import sys
default_encoding = 'utf-8'
#print sys.getdefaultencoding()
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
print sys.getdefaultencoding()


from flask import Flask, redirect, request, session

from .view.view import RestApi
import json,threading
from storage.interface import StorageIF
import urllib

class RestApp(Flask):
    def __init__(self,
                 import_name=__package__,
                 settings='setting.py',
                 **kwargs):
        super(RestApp, self).__init__(import_name,
                                      instance_relative_config=True,
                                      **kwargs)
        self.init_views()
        self.init_api()

    def init_views(self):

	@self.route('/index/', methods=['GET', 'POST'])
        def index() :
            if request.method == 'GET':
                print "test get"
            
            elif request.method == 'POST':
                print "test post"

            return self.api.index()

    def init_api(self):
        self.api = RestApi(self)
