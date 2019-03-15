# -*- coding: cp936 -*-
'''
Created on 2011-9-29

@author: hongchenzai
'''

import logging
import os
import sys
import time

from Source.xls2db import common

_logger_dict = {}
def get_logger(name='STDLOG'):
    global _logger_dict
    _logger = _logger_dict.get(name)
    if not _logger:
        import sys
        import logging
        _logger = logging.Logger(name)
        #import multiprocessing
        #_logger = multiprocessing.get_logger()
        #_logger.name = name
        _logger.setLevel(logging.INFO)
        objFormatter = logging.Formatter("%(asctime)s - %(levelname)s: %(name)s----%(message)s")
        objHandler = logging.StreamHandler(sys.stdout)
        objHandler.setFormatter(objFormatter)
        _logger.addHandler(objHandler)
        _logger_dict[name] = _logger
    return _logger


class common_log:
    __instance = None
    @staticmethod
    def instance():
        if common_log.__instance is None:
            common_log.__instance = common_log()
        return common_log.__instance
        
    def __init__(self):
        self.dictLogger = {}
        
        log_folder = os.path.join(os.getcwd(), 'log')
        try:
            os.stat(log_folder)            # �����ļ�·���治����
        except:
            os.makedirs(log_folder)        # �����ļ�·��
        #log_filename = 'log' + time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time())) + '.txt'
        #self.logfile = os.path.join(log_folder, log_filename)
        self.logfile = common.rdb_log.get_logfile()
        if not self.logfile:
            logfile = 'log' + time.strftime('%Y-%m-%d %H_%M_%S',time.localtime(time.time())) + '.txt'
            self.logfile = os.path.join(os.getcwd(), 'log', logfile)
    
    def init(self):
        # handler
        self.objSysHandler = common_sysout_handler()
        self.objLogHandler = common_file_handler(self.logfile)
        
        # formatter
        self.objFormatter = logging.Formatter("%(asctime)s - %(levelname)s: %(name)s----%(message)s")
        self.objSysHandler.setFormatter(self.objFormatter)
        self.objLogHandler.setFormatter(self.objFormatter)
        
    def logger(self, name):
        if not self.dictLogger.has_key(name):
            objLogger = common_logger(name)
            objLogger.addHandler(self.objSysHandler)
            objLogger.addHandler(self.objLogHandler)
            self.dictLogger[name] = objLogger
        return self.dictLogger[name]
    
    def end(self):
        for logger in self.dictLogger.values():
            logger.removeHandler(self.objLogHandler)
            logger.removeHandler(self.objSysHandler)
        self.objLogHandler.close()
    
    def get_logfile(self):
        return self.logfile
        
class common_logger(logging.Logger):
    def __init__(self, name):
        logging.Logger.__init__(self, name)

class common_sysout_handler(logging.StreamHandler):
    def __init__(self):
        logging.StreamHandler.__init__(self, sys.stdout)

class common_file_handler(logging.FileHandler):
    def __init__(self, filename):
        logging.FileHandler.__init__(self, filename)
