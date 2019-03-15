'''
Created on JUE 18, 2016

@author: xieyi
'''

import os

from flaskapp import RestApp

instance_path = "/opt/ExcelFunc_DB/instance"

app = RestApp(settings='settings.py', instance_path=instance_path)


