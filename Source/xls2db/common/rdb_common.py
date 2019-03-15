# -*- coding: cp936 -*-
'''
Created on 2011-10-12
ת����ά�����õ���һЩ���ú���
@author: hongchenzai
'''
import types

from xlrd import open_workbook

import rdb_log
from Source.xls2db import common


class Stratify(object):
    ''' �������ֵַ������
    '''
    
    def Open(self, path = '.\docs\��������ע��Code�ֲ��_iPC�ձ�.xls'):
        self.book = open_workbook(path)
       
    def GetStratify(self, kind, arrt):
        """ȡ�÷ֲ���Ϣ
           Kind: Ҫת�����ֱ�  1: link,          2: link���֣�            3: ������          4�� �����֣�             5��  POI����,  6:������        7:������      8: ˮϵ
           arrt: �������            1: link�ȼ�������    2: link�ȼ�������  3: ��������, 4:  �����ִ���      5:  POI����       6:�����ֱ�   7:�����ֱ� 8: ˮϵ�ֱ�
           return(����ֵ):
           code:  �ֱ�
           nametype: ���  0:RESERVED��1: �������֣�2: ��״���ƣ�3���Ǻ�+������
           prior: ���ȼ�
           low_level: ��ֵԽ��,level�ȼ�Խ��; 19---0
           high_level:ͬ��
        """
        module_name = ''
        if kind == 2:    # ��link���ֲַ�
            module_name = 'Link Name'        
        elif kind == 5:    # POI����
            module_name = 'POI Name'
        elif kind == 6:    # ������
            module_name = 'Line'
        elif kind == 7:    # ������
            module_name = 'Polygon'
        elif kind == 8:    # ˮϵ
            module_name = 'water'
        else:
            rdb_log.log('Stratify', "error kind" + repr(kind), 'warning')
            return None, None, None, None, None 
        
        i           = 0
        sheet       = self.book.sheet_by_index(0)
        ni_code_col = ord('O') - ord('A')
        for ni_code in sheet.col(ni_code_col):
            if ni_code.value.lower().find(arrt.lower()) != -1 :
                rdb_code_col = ord('D') - ord('A')              # �ֱ�Code�к�
                rdb_prio_col = ord('E') - ord('A')              # ���Ʊ�ʾ���ȶ��к�
                rdb_type_col = ord('F') - ord('A')              # ������Type�к�
                rdb_low_col  = ord('V') - ord('A')              # ��Ͳ��к�
                rdb_high_col = ord('W') - ord('A')              # ��߲��к�
                rdb_code, name_prio,name_type, low_col, high_col = None, None, None, None, None
                if sheet.cell_value(i, rdb_code_col) != '':
                    rdb_code  = int(sheet.cell_value(i, rdb_code_col)[0:6], 16)   # ��ʮ�����Ƶ��ִ�תΪʮ��������
                else:
                    rdb_log.log(module_name, "can't find rdb code for NI_Code " + arrt, 'warning')
                if sheet.cell_value(i, rdb_prio_col) != '':
                    name_prio = sheet.cell_value(i, rdb_prio_col)
                else :
                    if module_name != 'Line' and module_name != 'Polygon' and module_name != 'water':
                        rdb_log.log(module_name, "can't find Priority code for NI_Code: " + arrt, 'warning')
                if sheet.cell_value(i, rdb_type_col) != '':
                    name_type = sheet.cell_value(i, rdb_type_col)
                else :
                    if module_name != 'Line' and module_name != 'Polygon' and module_name != 'water':
                        rdb_log.log(module_name, " can't find type code for NI_Code: " + arrt, 'warning')
                if sheet.cell_value(i, rdb_low_col) != '':
                    low_col   = sheet.cell_value(i, rdb_low_col)
                else:
                    if module_name != 'Line' and module_name != 'Polygon' and module_name != 'water':
                        rdb_log.log(module_name, "can't find low level code for NI_Code: " + arrt, 'warning')
                if sheet.cell_value(i, rdb_high_col) != '':
                    high_col  = sheet.cell_value(i, rdb_high_col)
                else:
                    if module_name != 'Line' and module_name != 'Polygon' and module_name != 'water':
                        rdb_log.log(module_name, "can't find high level code for NI_Code: " + arrt, 'warning')
                
                return rdb_code, name_type, name_prio, low_col, high_col
            i += 1
    
        rdb_log.log(module_name, "can't find the information for NI_Code: " + arrt, 'warning')
        
        return None, None, None, None, None 
    
    def GetRoadDisplayClass(self, road_kind):
        module_name = 'Road'
        i           = 0
        sheet       = self.book.sheet_by_index(0)
        ni_code_col = ord('O') - ord('A')
        for ni_code in sheet.col(ni_code_col):
            if ni_code.value.lower().find(road_kind.lower()) != -1 :
                rdb_road_dc_col = ord('X') - ord('A')              # Road Display Class
                rdb_dc = None
                if sheet.cell_value(i, rdb_road_dc_col) != '':
                    rdb_dc  = int(sheet.cell_value(i, rdb_road_dc_col))   # ��ʮ�����Ƶ��ִ�תΪʮ��������
                else:
                    rdb_log.log(module_name, "can't find rdb code for NI_Code: " + road_kind, 'warning')
              
                return rdb_dc
            i += 1
            
        return None
    
    def GetAllStratify(self):

        '''���ֲ���Ϣ�������ݿ��'''
        kind_code_list = []
        sheet          = self.book.sheet_by_index(0)
        
        kind_code_col  = ord('D') - ord('A')
        kiwi_name_col  = ord('G') - ord('A')              # Kiwi�ֱ�����
        emg_code_col   = ord('H') - ord('A')              # EMG-Code
        ni_code_col    = ord('O') - ord('A')              # NI-Code
        
        rdb_code_col   = ord('D') - ord('A')              # �ֱ�Code�к�
        rdb_prio_col   = ord('E') - ord('A')              # ���Ʊ�ʾ���ȶ��к�
        rdb_type_col   = ord('F') - ord('A')              # ������Type�к�
        rdb_low_col    = ord('V') - ord('A')              # ��Ͳ��к�
        rdb_high_col   = ord('W') - ord('A')              # ��߲��к�
        disp_class_col = ord('X') - ord('A')              # Display Class
        emg_codes_num  = 0
        ni_codes_num   = 0
        emg_code_list  = []
        ni_code_list   = []
        
        i = 6
        while i < sheet.nrows:
            kind_code = sheet.cell_value(i, kind_code_col)
            if kind_code == None or kind_code == '':
                i += 1
                continue
            else:
                kind_code = int(kind_code, 16)
                
            if sheet.cell_value(i, emg_code_col) != '':
                emg_code_list = str(sheet.cell_value(i, emg_code_col)).split('\n')
                emg_codes_num = len(emg_code_list)
            else:
                emg_code_list = []
                emg_codes_num = 0
                
            if sheet.cell_value(i, ni_code_col) != '':
                cell_value = sheet.cell_value(i, ni_code_col)
                if type(cell_value) in [types.StringType, types.UnicodeType]:
                    ni_code_list = cell_value.split('\n')
                else:
                    ni_code_list = [str(int(cell_value))]
                ni_codes_num = len(ni_code_list)
            else:
                ni_code_list = []
                ni_codes_num = 0
            
            if sheet.cell_value(i, rdb_prio_col) != '':
                priority  = int(sheet.cell_value(i, rdb_prio_col))
            else:
                priority  = None
            if sheet.cell_value(i, rdb_type_col) != '':    
                name_type  = int(sheet.cell_value(i, rdb_type_col))
            else:
                name_type  = None
            
            kiwi_name = sheet.cell_value(i, kiwi_name_col)
            emg_name  = sheet.cell_value(i, emg_code_col + 1)
            ni_name   = sheet.cell_value(i, ni_code_col + 1)
            
            if sheet.cell_value(i, rdb_low_col) != '':
                low_level = int(sheet.cell_value(i, rdb_low_col))
            else :
                low_level = None
            
            if sheet.cell_value(i, rdb_high_col) != '':
                high_level = int(sheet.cell_value(i, rdb_high_col))
            else:
                high_level = None
            
            if sheet.cell_value(i, disp_class_col) != '':    
                disp_class = int(sheet.cell_value(i, disp_class_col))
            else:
                disp_class = None   
         
            if emg_codes_num == 0 and  ni_codes_num == 0:
                kind_code_list.append((kind_code, priority, name_type, kiwi_name, None, emg_name, None, ni_name, low_level, high_level, disp_class))
                #print kind_code, priority, name_type, kiwi_name, None, emg_name, None, ni_name, low_level, high_level
                i += 1
                continue
            
            if emg_codes_num >= ni_codes_num:
                j = 0 
                while j < ni_codes_num: 
                    dot_idx = emg_code_list[j].find('.')
                    kind_code_list.append((kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, 
                                           ni_code_list[j], ni_name, low_level, high_level, disp_class))
                    #print kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, ni_code_list[j][2:], ni_name, low_level, high_level, disp_class
                    j += 1
                while j < emg_codes_num:
                    dot_idx = emg_code_list[j].find('.')
                    kind_code_list.append((kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, 
                                           None, ni_name, low_level, high_level, disp_class))
                    #print kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, None, ni_name, low_level, high_level, disp_class
                    j += 1
            else:
                j = 0 
                while j < emg_codes_num: 
                    dot_idx = emg_code_list[j].find('.')
                    kind_code_list.append((kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, 
                                           ni_code_list[j], ni_name, low_level, high_level, disp_class))
                    #print kind_code, priority, name_type, kiwi_name, emg_code_list[j][0:dot_idx], emg_name, ni_code_list[j][2:], ni_name, low_level, high_level, disp_class
                    j += 1
                
                while j < ni_codes_num:
                    kind_code_list.append((kind_code, priority, name_type, kiwi_name, None, emg_name, 
                                           ni_code_list[j], ni_name, low_level, high_level, disp_class))
                    #print kind_code, priority, name_type, kiwi_name, None, emg_name, ni_code_list[j][2:], ni_name, low_level, high_level, disp_class
                    j += 1
            i += 1
        return kind_code_list

def GetPara(name):
    return common.config.CConfig.instance().getPara(name)

def GetPath(name):
    return common.config.CConfig.instance().getPara(name)

def getProjName():
    return GetPara('proj_name')

def getProjCountry():
    return GetPara('proj_country')

def getItem(proj_mapping):
    proj_name = common.config.CConfig.instance().getPara('proj_name').lower()
    proj_country = common.config.CConfig.instance().getPara('proj_country').lower()
    if proj_mapping.has_key((proj_name, proj_country)):
        return proj_mapping[(proj_name, proj_country)]
    elif proj_mapping.has_key(proj_name):
        return proj_mapping[proj_name]
    else:
        return proj_mapping['default']

def readlines(path):
    lines = []
    file_object = open(path, 'r')
    
    try:
        lines = file_object.readlines()
    except:
        file_object.close()
        exit(1)
    finally:
        file_object.close()
 
    return lines   
    
def CountPassLink(PassLid, PassLid2 = None):
    count = 0;
    if PassLid != None and PassLid != '':
        count = PassLid.count('|') + 1
    if PassLid2 != None and PassLid2 != '':
        count += PassLid2.count('|') + 1
    return count

def rdb_exit(param):
    import time
    time.sleep(1.0) # avoid same log file name to autocheck
    exit(param)
    
def GetAllLanguages(path):
    book = open_workbook(path)
    Lang_list = []
    sheet             = book.sheet_by_index(0)
    language_id_col   = ord('A') - ord('A')              # 
    l_full_name_col   = ord('B') - ord('A')              # ��������
    l_talbe_col       = ord('C') - ord('A')              # ���Ա���
    pronunciation_col = ord('D') - ord('A')             # ������ȫ��    
    p_talbe_col       = ord('E') - ord('A')             # ��������
    i         = 3
    while i < sheet.nrows:
        language_id = sheet.cell_value(i, language_id_col)
        if language_id == None:
            break;
            
        Lang_list.append( (language_id
                          , sheet.cell_value(i, l_full_name_col)
                          , sheet.cell_value(i, l_talbe_col)
                          , sheet.cell_value(i, pronunciation_col)
                          , sheet.cell_value(i, p_talbe_col))
                         )
        i += 1
    
    return Lang_list
            
    

    