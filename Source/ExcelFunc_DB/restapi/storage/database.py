"""
Created on JUE 18, 2016
@author: xieyi

"""
import random
import json
import ConfigParser
import os
import sys

import time

import binascii 


import socket


CONFIG_FILE = 'db.cfg'
CONFIG_PATH = os.path.split(os.path.realpath(__file__))[0] + '/' + CONFIG_FILE


class PostgresDataBase(object):
    def __init__(self):
        self._config = ConfigParser.ConfigParser()
	self._config.read(CONFIG_PATH)
	
    def _get_config(self, section, option):
        return self._config.get(section, option)

    def get_index(self, _id):
    	 """
    	 DB process!
         test
         """

