# -*- coding: UTF-8 -*-
"""
Created on 2017-10-23

@author:yuyin
"""
import re
from import_base import ImportBase


class HUImportBase(ImportBase):
    def __init__(self):
        ImportBase.__init__(self)

    def get_row(self, sheet, row=1, from_col=1, to_col=1):
        values = []
        j = from_col
        while j <= to_col:
            val = sheet.cell(row=row, column=j).value
            if type(val) == unicode:
                val = val.replace(u'_x000D_', u'')
                val = val.replace(u'_x0000_', u'')
            values.append(val)
            j += 1
        return values


class HUImportCheck(HUImportBase):
    def __init__(self):
        HUImportBase.__init__(self)

    def hu_check_row(self, pg, sheet, start_row, max_row ):
        error_list = {}
        sqlcmd1 = '''
         select major_category, medium_catetory, small_category, detail,
         req_post, status, trigger, action, remark from spec.arl where
         arl_id = %s 
         '''
        row_list = []
        for row in range(start_row, max_row + 1):
            value = self.get_row(sheet, row, from_col=1, to_col=13)
            row_list.append(value[12])
        for row in range(start_row, max_row + 1):
            col_list = {}
            values = self.get_row(sheet, row, from_col=1, to_col=79)
            pg.execute(sqlcmd1, (values[1],))
            count = pg.fetchone()
            if count is None:
                col_list[u'B'] = 1
            else:
                if values[2] != count[0]:
                    col_list[u'C'] = 1
                if values[3] != count[1]:
                    col_list[u'D'] = 1
                if values[4] != count[2]:
                    col_list[u'E'] = 1
                if values[5] != count[3]:
                    col_list[u'F'] = 1
                if values[7] != count[4]:
                    col_list[u'H'] = 1
                if values[8] != count[5]:
                    col_list[u'I'] = 1
                if values[9] != count[6]:
                    col_list[u'J'] = 1
                if values[10] != count[7]:
                    col_list[u'K'] = 1
                if values[11] != count[8]:
                    col_list[u'L'] = 1
            for i in range(row - start_row + 1, len(row_list)):
                if values[12] == row_list[i]:
                    col_list[u'M'] = 1
            if not str(values[13]).isdigit():
                col_list[u'N'] = 1

            o = re.search('^[0-3]*$', str(values[14]))
            if o is None:
                col_list[u'O'] = 1
            p = re.search('^[0-3]*$', str(values[15]))
            if p is None:
                col_list[u'P'] = 1
            q = re.search('^[0-3]*$', str(values[16]))
            if q is None:
                col_list[u'Q'] = 1
            r = re.search('^[0-3]*$', str(values[17]))
            if r is None:
                col_list[u'R'] = 1
            s = re.search('^[0-3]*$', str(values[18]))
            if s is None:
                col_list[u'S'] = 1
            t = re.search('^[0-3]*$', str(values[19]))
            if t is None:
                col_list[u'T'] = 1

            if not values[22] is None:
                col_list[u'W'] = 1
            if str(values[23]).strip() == '':
                col_list[u'X'] = 1
            else:
                if len(str(values[23])) == 1:
                    if values[23] != '-':
                        col_list[u'X'] = 1
            if str(values[24]).strip() == '':
                col_list[u'Y'] = 1
            else:
                if len(str(values[24])) == 1:
                    if values[24] != '-':
                        col_list[u'Y'] = 1
                else:
                    m = re.search('^\(\d+\).*', str(values[24]))
                    if m is None:
                        col_list[u'Y'] = 1
            if str(values[25]).strip() == '':
                col_list[u'Z'] = 1
            else:
                if len(str(values[25])) == 1:
                    if values[25] != '-':
                        col_list[u'Z'] = 1
                else:
                    m = re.search('^\(\d+\).*', str(values[25]))
                    if m is None:
                        col_list[u'Z'] = 1
            if str(values[26]).strip() == '':
                col_list[u'AA'] = 1
            else:
                if len(str(values[26])) == 1:
                    if values[26] != '-':
                        col_list[u'AA'] = 1
            if str(values[27]).strip() == '':
                col_list[u'AB'] = 1
            else:
                if len(str(values[27])) == 1:
                    if values[27] != '-':
                        col_list[u'AB'] = 1
            if str(values[28]).strip() == '':
                col_list[u'AC'] = 1
            else:
                if len(str(values[28])) == 1:
                    if values[28] != '-':
                        col_list[u'AC'] = 1
                else:
                    m = re.search('^\(\d+\).*', str(values[28]))
                    if m is None:
                        col_list[u'AC'] = 1
            if not str(values[29]).isdigit():
                col_list[u'AD'] = 1
            if str(values[30]).strip() == '':
                col_list[u'AE'] = 1
            else:
                if len(str(values[30])) == 1:
                    if values[30] != '-':
                        col_list[u'AE'] = 1
                elif len(str(values)[30]) == 2:
                    if values[30] != '-※':
                        col_list[u'AE'] = 1
            if str(values[31]).strip() == '':
                col_list[u'AF'] = 1
            else:
                if len(str(values[31])) == 1:
                    if values[31] != '-':
                        col_list[u'AF'] = 1
                elif len(str(values[31])) == 2:
                    if values[31] != '-※':
                        col_list[u'AF'] = 1
            if str(values[32]).strip() == '':
                col_list[u'AG'] = 1
            else:
                if len(str(values[32])) == 1:
                    if values[32] != '-':
                        col_list[u'AG'] = 1
                elif len(str(values[32])) == 2:
                    if values[32] != '-※':
                        col_list[u'AG'] = 1
            if str(values[33]).strip() == '':
                col_list[u'AH'] = 1
            else:
                if len(str(values[33])) == 1:
                    if values[33] != '-':
                        col_list[u'AH'] = 1
                elif len(str(values[33])) == 2:
                    if values[33] != '-※':
                        col_list[u'AH'] = 1
            if str(values[34]).strip() == '':
                col_list[u'AI'] = 1
            else:
                if len(str(values[34])) == 1:
                    if values[34] != '-':
                        col_list[u'AI'] = 1
                elif len(str(values[34])) == 2:
                    if values[34] != '-※':
                        col_list[u'AI'] = 1
            if str(values[35]).strip() == '':
                col_list[u'AJ'] = 1
            else:
                if len(str(values[35])) == 1:
                    if values[35] != '-':
                        col_list[u'AJ'] = 1
                elif len(str(values[35])) == 2:
                    if values[35] != '-※':
                        col_list[u'AJ'] = 1
            if str(values[36]).strip() == '':
                col_list[u'AK'] = 1
            else:
                if len(str(values[36])) == 1:
                    if values[36] != '-':
                        col_list[u'AK'] = 1
                elif len(str(values[36])) == 2:
                    if values[36] != '-※':
                        col_list[u'AK'] = 1
            if str(values[37]).strip() == '':
                col_list[u'AL'] = 1
            else:
                if len(str(values[37])) == 1:
                    if values[37] != '-':
                        col_list[u'AL'] = 1
                elif len(str(values[37])) == 2:
                    if values[37] != '-※':
                        col_list[u'AL'] = 1
            if str(values[38]).strip() == '':
                col_list[u'AM'] = 1
            else:
                if len(str(values[38])) == 1:
                    if values[38] != '-':
                        col_list[u'AM'] = 1
                elif len(str(values[38])) == 2:
                    if values[38] != '-※':
                        col_list[u'AM'] = 1
            if str(values[39]).strip() == '':
                col_list[u'AN'] = 1
            else:
                if len(str(values[39])) == 1:
                    if values[39] != '-':
                        col_list[u'AN'] = 1
                elif len(str(values[39])) == 2:
                    if values[39] != '-※':
                        col_list[u'AN'] = 1
            if str(values[40]).strip() == '':
                col_list[u'AO'] = 1
            else:
                if len(str(values[40])) == 1:
                    if values[40] != '-':
                        col_list[u'AO'] = 1
                elif len(str(values[40])) == 2:
                    if values[40] != '-※':
                        col_list[u'AO'] = 1
            if str(values[41]).strip() == '':
                col_list[u'AP'] = 1
            else:
                if len(str(values[41])) == 1:
                    if values[41] != '-':
                        col_list[u'AP'] = 1
                elif len(str(values[41])) == 2:
                    if values[41] != '-※':
                        col_list[u'AP'] = 1
            if str(values[42]).strip() == '':
                col_list[u'AQ'] = 1
            else:
                if len(str(values[42])) == 1:
                    if values[42] != '-':
                        col_list[u'AQ'] = 1
                elif len(str(values[42])) == 2:
                    if values[42] != '-※':
                        col_list[u'AQ'] = 1
            if str(values[43]).strip() == '':
                col_list[u'AR'] = 1
            else:
                if len(str(values[43])) == 1:
                    if values[43] != '-':
                        col_list[u'AR'] = 1
                elif len(str(values[43])) == 2:
                    if values[43] != '-※':
                        col_list[u'AR'] = 1
            if str(values[44]).strip() == '':
                col_list[u'AS'] = 1
            else:
                if len(str(values[44])) == 1:
                    if values[44] != '-':
                        col_list[u'AS'] = 1
                elif len(str(values[44])) == 2:
                    if values[44] != '-※':
                        col_list[u'AS'] = 1
            if str(values[45]).strip() == '':
                col_list[u'AT'] = 1
            else:
                if len(str(values[45])) == 1:
                    if values[45] != '-':
                        col_list[u'AT'] = 1
                elif len(str(values[45])) == 2:
                    if values[45] != '-※':
                        col_list[u'AT'] = 1
            if str(values[46]).strip() == '':
                col_list[u'AU'] = 1
            else:
                if len(str(values[46])) == 1:
                    if values[46] != '-':
                        col_list[u'AU'] = 1
                elif len(str(values[46])) == 2:
                    if values[46] != '-※':
                        col_list[u'AU'] = 1
            if str(values[47]).strip() == '':
                col_list[u'AV'] = 1
            else:
                if len(str(values[47])) == 1:
                    if values[47] != '-':
                        col_list[u'AV'] = 1
                elif len(str(values[47])) == 2:
                    if values[47] != '-※':
                        col_list[u'AV'] = 1
            if str(values[48]).strip() == '':
                col_list[u'AW'] = 1
            else:
                if len(str(values[48])) == 1:
                    if values[48] != '-':
                        col_list[u'AW'] = 1
                elif len(str(values[48])) == 2:
                    if values[48] != '-※':
                        col_list[u'AW'] = 1
            if str(values[49]).strip() == '':
                col_list[u'AX'] = 1
            else:
                if len(str(values[49])) == 1:
                    if values[49] != '-':
                        col_list[u'AX'] = 1
                elif len(str(values[49])) == 2:
                    if values[49] != '-※':
                        col_list[u'AX'] = 1
            if str(values[50]).strip() == '':
                col_list[u'AY'] = 1
            else:
                if len(str(values[50])) == 1:
                    if values[50] != '-':
                        col_list[u'AY'] = 1
                elif len(str(values[50])) == 2:
                    if values[50] != '-※':
                        col_list[u'AY'] = 1
            if str(values[51]).strip() == '':
                col_list[u'AZ'] = 1
            else:
                if len(str(values[51])) == 1:
                    if values[51] != '-':
                        col_list[u'AZ'] = 1
                elif len(str(values[51])) == 2:
                    if values[51] != '-※':
                        col_list[u'AZ'] = 1
            if str(values[52]).strip() == '':
                col_list[u'BA'] = 1
            else:
                if len(str(values[52])) == 1:
                    if values[52] != '-':
                        col_list[u'BA'] = 1
                elif len(str(values[52])) == 2:
                    if values[52] != '-※':
                        col_list[u'BA'] = 1
            if str(values[53]).strip() == '':
                col_list[u'BB'] = 1
            else:
                if len(str(values[53])) == 1:
                    if values[53] != '-':
                        col_list[u'BB'] = 1
                elif len(str(values[53])) == 2:
                    if values[53] != '-※':
                        col_list[u'BB'] = 1
            if str(values[54]).strip() == '':
                col_list[u'BC'] = 1
            else:
                if len(str(values[54])) == 1:
                    if values[54] != '-':
                        col_list[u'BC'] = 1
                elif len(str(values[54])) == 2:
                    if values[54] != '-※':
                        col_list[u'BC'] = 1
            if str(values[55]).strip() == '':
                col_list[u'BD'] = 1
            else:
                if len(str(values[55])) == 1:
                    if values[55] != '-':
                        col_list[u'BD'] = 1
                elif len(str(values[55])) == 2:
                    if values[55] != '-※':
                        col_list[u'BD'] = 1
            if str(values[56]).strip() == '':
                col_list[u'BE'] = 1
            else:
                if len(str(values[56])) == 1:
                    if values[56] != '-':
                        col_list[u'BE'] = 1
                elif len(str(values[56])) == 2:
                    if values[56] != '-※':
                        col_list[u'BE'] = 1
            if str(values[57]).strip() == '':
                col_list[u'BF'] = 1
            else:
                if len(str(values[57])) == 1:
                    if values[57] != '-':
                        col_list[u'BF'] = 1
                elif len(str(values[57])) == 2:
                    if values[57] != '-※':
                        col_list[u'BF'] = 1
            if str(values[58]).strip() == '':
                col_list[u'BG'] = 1
            else:
                if len(str(values[58])) == 1:
                    if values[58] != '-':
                        col_list[u'BG'] = 1
                elif len(str(values[58])) == 2:
                    if values[58] != '-※':
                        col_list[u'BG'] = 1
            if str(values[59]).strip() == '':
                col_list[u'BH'] = 1
            else:
                if len(str(values[59])) == 1:
                    if values[59] != '-':
                        col_list[u'BH'] = 1
                elif len(str(values[59])) == 2:
                    if values[59] != '-※':
                        col_list[u'BH'] = 1
            if str(values[61]).strip() == '':
                col_list[u'BJ'] = 1
            else:
                bj = re.search('^\d+\.*$', str(values[61]))
                if bj is None:
                    col_list[u'BJ'] = 1
            if str(values[62]).strip() == '':
                col_list[u'BK'] = 1
            if str(values[63]).strip() == '':
                col_list[u'BL'] = 1
            if str(values[64]).strip() == '':
                col_list[u'BM'] = 1
            if str(values[65]).strip() == '':
                col_list[u'BN'] = 1
            if str(values[66]).strip() == '':
                col_list[u'BO'] = 1
            if str(values[67]).strip() == '':
                col_list[u'BP'] = 1
            if str(values[68]).strip() == '':
                col_list[u'BQ'] = 1
            if str(values[69]).strip() == '':
                col_list[u'BR'] = 1
            if str(values[70]).strip() == '':
                col_list[u'BS'] = 1
            if values[72] != u'○':
                col_list[u'BU'] = 1
            if not values[77]:
                col_list[u'BZ'] = 1
            if str(values[78]).strip() == '':
                col_list[u'CA'] = 1
            if len(col_list) != 0:
                error_list[row] = col_list
        return error_list


class DEFImportCheck(ImportBase):
    def __init__(self):
        ImportBase.__init__(self)

    def get_row(self, sheet, row=1, from_col=1, to_col=1):
        values = []
        j = from_col
        while j <= to_col:
            val = sheet.cell(row=row, column=j).value
            if type(val) == unicode:
                val = val.replace(u'_x000D_', u'')
                val = val.replace(u'_x0000_', u'')
            values.append(val)
            j += 1
        return values

    def def_check_row(self, pg, sheet, start_row, max_row):
        error_list = {}

        tagl_id_list = self._tagl_id_list(sheet, start_row, max_row)
        for row in range(start_row, max_row + 1):
            col_list = {}
            values = self.get_row(sheet, row, from_col=1, to_col=60)
            hu_id = values[1]
            for i in range(row - start_row + 1, len(tagl_id_list)):
                if values[2] == tagl_id_list[i]:
                    col_list[u'C'] = 1
            if not str(values[3]).isdigit():
                col_list[u'N'] = 1
            compare_list = self._get_hu(pg, hu_id)
            if compare_list is None:
                col_list[u'B'] = 1
            else:
                if values[4] != compare_list[0]:
                    col_list[u'E'] = 1
                if values[5] != compare_list[1]:
                    col_list[u'F'] = 1
                if values[6] != compare_list[2]:
                    col_list[u'G'] = 1
                if values[7] != compare_list[3]:
                    col_list[u'H'] = 1
                if values[9] != compare_list[4]:
                    col_list[u'J'] = 1
                if values[11] != compare_list[5]:
                    col_list[u'L'] = 1
                if values[12] != compare_list[6]:
                    col_list[u'M'] = 1
                if values[13] != compare_list[7]:
                    col_list[u'N'] = 1
                if values[14] != compare_list[8]:
                    col_list[u'O'] = 1
                if values[15] != compare_list[9]:
                    col_list[u'P'] = 1
                if values[16] != compare_list[10]:
                    col_list[u'Q'] = 1
                if values[17] != compare_list[11]:
                    col_list[u'R'] = 1
            if not values[10] is None:
                col_list[u'K'] = 1
            if values[18] != u'MEU' and values[18] != u'DCU' and values[18] != u'DCU/MEU':
                col_list[u'S'] = 1
            if str(values[19]) == '':
                col_list[u'T'] = 1
            else:
                if len(str(values[19])) == 1:
                    if values[19] != '-':
                        col_list[u'T'] = 1
            # 不能为空, 必须以(数字)开始, 必须为半角"("，和半角数字如果只有一个字符, 必须为"-"
            if str(values[20]) == '':
                col_list[u'U'] = 1
            else:
                if len(str(values[20])) == 1:
                    if values[20] != '-':
                        col_list[u'U'] = 1
                    else:
                        m = re.search('^\(\d+\).*', str(values[20]))
                        if m is None:
                            col_list[u'U'] = 1
            if str(values[21]) == '':
                col_list[u'V'] = 1
            else:
                if len(str(values[21])) == 1:
                    if values[21] != '-':
                        col_list[u'V'] = 1
                    else:
                        m = re.search('^\(\d+\).*', str(values[21]))
                        if m is None:
                            col_list[u'V'] = 1
            # 不能为空, 如果只有一个字符, 必须为"-", 如果只有两个字符, 必须为"-※"
            if not self._is_error(str(values[22])):
                col_list[u'W'] = 1
            if not self._is_error(str(values[23])):
                col_list[u'X'] = 1
            if not self._is_error(str(values[24])):
                col_list[u'Y'] = 1
            if not self._is_error(str(values[25])):
                col_list[u'Z'] = 1
            if not self._is_error(str(values[26])):
                col_list[u'AA'] = 1
            if not self._is_error(str(values[27])):
                col_list[u'AB'] = 1
            if not self._is_error(str(values[28])):
                col_list[u'AC'] = 1
            if not self._is_error(str(values[29])):
                col_list[u'AD'] = 1
            if not self._is_error(str(values[30])):
                col_list[u'AE'] = 1
            if not self._is_error(str(values[31])):
                col_list[u'AF'] = 1
            if not self._is_error(str(values[32])):
                col_list[u'AG'] = 1
            if not self._is_error(str(values[33])):
                col_list[u'AH'] = 1
            if not self._is_error(str(values[34])):
                col_list[u'AI'] = 1
            if not self._is_error(str(values[35])):
                col_list[u'AJ'] = 1
            if not self._is_error(str(values[36])):
                col_list[u'AK'] = 1
            if not self._is_error(str(values[37])):
                col_list[u'AL'] = 1
            if not self._is_error(str(values[38])):
                col_list[u'AM'] = 1
            if not self._is_error(str(values[39])):
                col_list[u'AN'] = 1
            if not self._is_error(str(values[40])):
                col_list[u'AO'] = 1
            if not self._is_error(str(values[41])):
                col_list[u'AP'] = 1
            if not self._is_error(str(values[42])):
                col_list[u'AQ'] = 1
            if not self._is_error(str(values[43])):
                col_list[u'AR'] = 1
            if not self._is_error(str(values[44])):
                col_list[u'AS'] = 1
            if not self._is_error(str(values[45])):
                col_list[u'AT'] = 1
            if not self._is_error(str(values[46])):
                col_list[u'AU'] = 1
            if not self._is_error(str(values[47])):
                col_list[u'AV'] = 1
            if not self._is_error(str(values[48])):
                col_list[u'AW'] = 1
            if not self._is_error(str(values[49])):
                col_list[u'AX'] = 1
            if str(values[50]) == '':
                col_list[u'AY'] = 1
            else:
                if len(str(values[50])) == 1:
                    if values[50] != '-':
                        col_list[u'AY'] = 1
            if str(values[51]) == '':
                col_list[u'AZ'] = 1
            else:
                if len(str(values[51])) == 1:
                    if values[51] != '-':
                        col_list[u'AZ'] = 1
            if str(values[52]) == '':
                col_list[u'BA'] = 1
            else:
                if len(str(values[52])) == 1:
                    if values[52] != '-':
                        col_list[u'BA'] = 1
            if str(values[53]) == '':
                col_list[u'BB'] = 1
            else:
                if len(str(values[53])) == 1:
                    if values[53] != '-':
                        col_list[u'BB'] = 1
            if str(values[54]) == '':
                col_list[u'BC'] = 1
            else:
                if len(str(values[54])) == 1:
                    if values[54] != '-':
                        col_list[u'BC'] = 1
            if not values[55] == u'〇' or values[55] == u'△' or values[55] == u'×' or values[55] == u'未確認':
                col_list[u'BD'] = 1
            if values[56] != u'×':
                col_list[u'BE'] = 1
            if values[57] != u'〇':
                col_list[u'BF'] = 1
            if str(values[58]).strip() == '':
                col_list[u'BG'] = 1
            if str(values[59]) == '':
                col_list[u'BH'] = 1
            if len(col_list) != 0:
                error_list[row] = col_list
        return error_list

    def _is_error(self, str):
        if str == '':
            return False
        else:
            if len(str) == 1:
                if str != '-':
                    return False
            elif len(str) == 2:
                if str != '-※':
                    return False
        return True

    def _tagl_id_list(self, sheet, start_row, max_row):
        tagl_id_list = []
        for row in range(start_row, max_row + 1):
            value = self.get_row(sheet, row, from_col=1, to_col=2)
            tagl_id_list.append(value[1])
        return tagl_id_list

    def _get_hu(self, pg, hu_id):
        """从H / U表中查询ID，获取信息后进行对比"""
        sqlcmd = """
            select a.major_category, a.medium_catetory, a.small_category, a.detail,
            h.rel_requirement, h.dcu_status, h.dcu_trigger, h.dcu_action, h.meu_status,
            h.meu_trigger, h.meu_action, h.remark from spec.arl as a left join spec.hu as h
            on a.arl_id = h.arl_id left join spec.definition as d on d.hu_def_id = h.hu_id where d.hu_def_id = %s
        """
        pg.execute(sqlcmd, (hu_id,))
        row = pg.fetchone()
        return row












