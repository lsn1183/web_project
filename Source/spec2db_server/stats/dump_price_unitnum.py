# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.arl_base import ServiceBase
from openpyxl import Workbook
import re
import json

class UnitNumInfo(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.wb = Workbook()
        self.check_result_dict = {}
        self.use_case_dict = {}
        self.create_basic_dict()

    def create_basic_dict(self):
        self._pg.connect()
        sql_cmd = '''select definition_id, module_name, seq_content, check_result, reason
                    from temp_seq_checkresult order by definition_id'''
        self._pg.execute(sql_cmd)
        for db_data in self._pg.fetchall():
            if db_data[0] not in self.check_result_dict:
                self.check_result_dict[db_data[0]] = []

            self.check_result_dict[db_data[0]].append(list(db_data))

        use_case_sqlcmd = '''select distinct user_case, file_name from analysis_usercase_matched'''
        self._pg.execute(use_case_sqlcmd)
        for db_data in self._pg.fetchall():
            if db_data[1]:
                self.use_case_dict[db_data[0]] = db_data[1]

        self._pg.close()

    def get_seq_dia(self, s):
        if s:
            p = '[\w_]+_0\d+'
            m = re.search(p, s)
            if m:
                return m.group(0)

        return None

    def get_usecase_info(self, db_line_data):
        if db_line_data[9] in [1,2]:
            return '无USECASE'

        seq_info = db_line_data[8]
        if seq_info.find("_0")>=0:
            return self.get_seq_dia(seq_info)

        if db_line_data[8].find("※") >= 0 or db_line_data[8].find("参照") >= 0:
            return '基本要件'

        model_name_list = json.loads(db_line_data[10])
        model_name_list = [_data for _data in model_name_list if _data]
        b_found_cannot_fix = False
        if db_line_data[4] in self.check_result_dict:
            for db_data in self.check_result_dict[db_line_data[4]]:
                if db_data[1] == model_name_list[-1] and db_data[2].find("(%d)" % db_line_data[7]) >= 0:
                    b_found_cannot_fix = True
                    break

        if b_found_cannot_fix == True:
            return '不要修正'
        else:
            if db_line_data[-1] == 0:
                return '要修正[无锁]'
            else:
                return '要修正[锁]'

    def get_dest_ana_info(self):
        sql_cmd = '''
            select arl.major_category, arl.medium_catetory, arl.small_category, arl.detail,
                dest.definition_id, grp.group_name, usr.user_name, 
                ana_seq.seq_id, ana_seq.seq, model_info.model_id, model_info.model, 
                ana.rel_requirement, ana.lock_status
            from public.price_ana as dest
            left join analysis_split_sequence as ana_seq on dest.definition_id = ana_seq.definition_id
            left join spec.analysis_model_type as model_info on ana_seq.model_id=model_info.model_id
            left join spec.analysis as ana on dest.definition_id = ana.definition_id
            left join spec.arl as arl on arl.arl_id = ana_seq.arl_id
            left join spec.arl_group as grp on grp.group_id=arl.group_id
            left join spec.arl_user as usr on usr.user_id=arl.user_id
            where ana_seq.seq_id > 0
            order by dest.definition_id, ana_seq.seq_id
        '''
        self._pg.connect()
        self._pg.execute(sql_cmd)

        dest_ana_info_list = [list(db_data) for db_data in self._pg.fetchall()]

        self._pg.close()

        return dest_ana_info_list


    def get_dest_basicreq_info(self):
        self._pg.connect()
        sql_cmd = '''
            select basic_req_name_chain from basic_req_call
        '''
        basic_req_name_list = []
        self._pg.execute(sql_cmd)
        for db_data in self._pg.fetchall():
            basic_req_name_list.extend(db_data[0].split("->"))
        basic_req_name_list = set(basic_req_name_list)

        sql_cmd = '''
            select arl.major_category, arl.medium_catetory, arl.small_category, arl.detail,
                ana.definition_id, grp.group_name, usr.user_name, 
                ana_seq.seq_id, ana_seq.seq, model_info.model_id, model_info.model, 
                ana.rel_requirement, ana.basic_req, ana.lock_status
            from spec.analysis as ana
            left join analysis_split_sequence as ana_seq on ana.definition_id = ana_seq.definition_id
            left join spec.analysis_model_type as model_info on ana_seq.model_id=model_info.model_id
            left join spec.arl as arl on arl.arl_id = ana_seq.arl_id
            left join spec.arl_group as grp on grp.group_id=arl.group_id
            left join spec.arl_user as usr on usr.user_id=arl.user_id
            where ana_seq.seq_id > 0 and ana.basic_req in (%s)
            order by ana.basic_req, ana.definition_id, ana_seq.seq_id
        ''' % ','.join(["'" + n + "'" for n in basic_req_name_list])
        self._pg.execute(sql_cmd)
        dest_ana_info_list = [list(db_data) for db_data in self._pg.fetchall()]

        sql_cmd = '''
                    select '' as major_category, '' as medium_catetory, '基本要件' as small_category, ana.basic_req,
                        ana.definition_id, grp.group_name, usr.user_name, 
                        ana_seq.seq_id, ana_seq.seq, model_info.model_id, model_info.model, 
                        ana.rel_requirement, ana.lock_status
                    from spec.basic_req_analysis as ana
                    left join basic_seq_analysis_split_sequence as ana_seq on ana.definition_id = ana_seq.definition_id
                    left join spec.analysis_model_type as model_info on ana_seq.model_id=model_info.model_id
                    left join spec.arl_group as grp on grp.group_id=ana.group_id
                    left join spec.arl_user as usr on usr.user_id=ana.user_id
                    where ana_seq.seq_id > 0 and ana.basic_req in (%s)
                    order by ana.basic_req, ana.definition_id, ana_seq.seq_id
                ''' % ','.join(["'" + n + "'" for n in basic_req_name_list])
        self._pg.execute(sql_cmd)
        for db_data in self._pg.fetchall():
            dest_ana_info_list.append(list(db_data))

        self._pg.close()

        return dest_ana_info_list


    def out_stat_info(self):
        dest_ana_info_list = self.get_dest_ana_info()
        basic_req_info_list = self.get_dest_basicreq_info()
        ws = self.wb.active
        ws.title = "Summary"
        out_info_dict = {}
        for db_data in (dest_ana_info_list+basic_req_info_list):
            if not db_data[10] in out_info_dict:
                out_info_dict[db_data[10]] = [[],[],[],[]]

            usecase_info = self.get_usecase_info(db_data)
            if not usecase_info:
                out_info_dict[db_data[10]][0].append(db_data[8][db_data[8].find(")")+1:])
                continue

            if usecase_info in ('无USECASE','基本要件'):
                out_info_dict[db_data[10]][0].append(db_data[8][db_data[8].find(")") + 1:])
                continue

            if usecase_info.find('_0') >= 0:
                if usecase_info in self.use_case_dict:
                    out_info_dict[db_data[10]][0].append(usecase_info)
                else:
                    out_info_dict[db_data[10]][1].append(usecase_info)
                continue

            if usecase_info in ('不要修正',):
                out_info_dict[db_data[10]][3].append(db_data[8][db_data[8].find(")")+1:])
                continue

            out_info_dict[db_data[10]][2].append(db_data[8][db_data[8].find(")")+1:])


        for _k,_v in out_info_dict.iteritems():
            module_info = json.loads(_k)
            module_info = [_d for _d in module_info if _d]
            ws.append([
                module_info[0],"->".join(module_info[1:-1]),module_info[-1],
                len(set(_v[0])),len(set(_v[1])),
                len(set(_v[2])),len(set(_v[3]))
            ])

        self.wb.save('/mnt/sharedoc/temp/unitcnt.xlsx')




if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')

    UnitNumInfo().out_stat_info()