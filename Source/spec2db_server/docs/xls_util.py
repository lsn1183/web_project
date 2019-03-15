# -*- coding: UTF-8 -*-
import datetime

class XlsUtil():
    def __init__(self, id_col):
        self.id_col = id_col

    def check_format(self, xls_sheet, doc_format):
        ret_format_check = True

        for format_info in doc_format.itervalues():
            if format_info['needcheck'] == False:
                continue
            f_col, f_row = format_info['xlspos'][0]
            xls_val = xls_sheet.cell(row=f_row, column=f_col).value
            if type(xls_val) in [long, int, float]:
                xls_val = str(xls_val)
            val = format_info['xlsname'].decode('utf8')
            ret_format_check = ret_format_check & (xls_val.strip() in format_info['xlsname'].decode('utf8').split('->'))
            if not ret_format_check:
                print xls_val.strip(), format_info['xlsname'].decode('utf8')
                break

        return ret_format_check

    def get_xls_data(self, xls_sheet, doc_format, start_data_row):
        ret_data_list = []
        for i_row in range(start_data_row, xls_sheet.max_row + 1):
            val_dict = {}
            for format_key, format_info in doc_format.iteritems():
                f_col, _ = format_info['xlspos'][0]
                xls_val = xls_sheet.cell(row=i_row, column=f_col).value
                xls_val_dict = dict()
                xls_val_dict.update(format_info)
                xls_val_dict['xlscol'] = f_col

                if xls_val == None or xls_val == "":
                    xls_val_dict['datatype'] = 'STR'
                    xls_val_dict['datavalue'] = ""
                elif format_info['datatype'] == 'DATETIME':
                    xls_val_dict['datavalue'] = self.convert_time(xls_val)
                elif format_info['datatype'] == 'FORMULAR_HUID':
                    if xls_sheet.cell(row=i_row, column=2):
                        xls_val_dict['datavalue'] = xls_sheet.cell(row=i_row, column=2).value + \
                                        '.'+str(int(xls_sheet.cell(row=i_row, column=14).value))
                    else:
                        xls_val_dict['datavalue'] = None
                elif format_info['datatype'] == 'FORMULAR_DEFID':
                    if xls_sheet.cell(row=i_row, column=2).value:
                        xls_val_dict['datavalue'] = xls_sheet.cell(row=i_row, column=2).value + \
                                        '.'+str(int(xls_sheet.cell(row=i_row, column=4).value))
                    else:
                        xls_val_dict['datavalue'] = None
                else:
                    if type(xls_val) == str:
                        xls_val_dict['datatype'] = 'STR'
                        xls_val_dict['datavalue'] = xls_val
                    elif type(xls_val) == unicode:
                        xls_val_dict['datatype'] = 'STR'
                        xls_val_dict['datavalue'] = xls_val.encode("utf8")
                    elif type(xls_val) in (float, int, long):
                        try:
                            int_xls_val = int(xls_val)
                            xls_val_dict['datatype'] = 'INT'
                            xls_val_dict['datavalue'] = int_xls_val
                        except:
                            xls_val_dict['datatype'] = 'FLOAT'
                            xls_val_dict['datavalue'] = xls_val

                val_dict[format_key] = xls_val_dict

            if not val_dict[self.id_col]['datavalue']:
                continue

            ret_data_list.append(val_dict)

        return ret_data_list


    def convert_time(self, long_time):
        if type(long_time) in (int, long):
            # excel中，用浮点数1表示1899年12月31日
            base = datetime.date(1899, 12, 31).toordinal()
            new_date = datetime.date.fromordinal(base + long_time - 1)
            return new_date.strftime("%Y-%m-%d")
        elif type(long_time) == datetime.datetime:
            return long_time.strftime("%Y-%m-%d")

        return long_time
