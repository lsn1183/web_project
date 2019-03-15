# -*- coding: UTF-8 -*-
from Source.spec2db_server.arl.arl_base import ServiceBase


class AnalysisInfo(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.create_table()
        self.basic_req_dict = {}
        self.def_basic_req = {}
        self.create_basic_dict()

    def create_table(self):
        createsql = '''
            drop table if exists public.basic_req_call;
            CREATE TABLE public.basic_req_call
            (
              definition_id character varying(240),
              basic_req_name_chain character varying(4196),
              chain_result character varying(16)
            )
            WITH (
              OIDS=FALSE
            );
            ALTER TABLE public.basic_req_call
              OWNER TO postgres;
        '''
        self._pg.connect()
        self._pg.execute(createsql)
        self._pg.commit()
        self._pg.close()

    def create_basic_dict(self):
        self._pg.connect()
        sql_cmd = '''
            (select basic_req,rel_requirement from spec.analysis
            union
            select basic_req,rel_requirement from spec.basic_req_analysis)
            order by basic_req
        '''
        self._pg.execute(sql_cmd)
        for db_data in self._pg.fetchall():
            if not db_data[0]:
                continue

            if db_data[0] not in self.basic_req_dict:
                self.basic_req_dict[db_data[0]] = []

            if db_data[1]:
                for split_data in db_data[1].split("\n"):
                    self.basic_req_dict[db_data[0]].append(split_data)


        sql_cmd = '''
            select definition_id,rel_requirement from spec.analysis order by definition_id
        '''
        self._pg.execute(sql_cmd)
        for db_data in self._pg.fetchall():
            if not db_data[1]:
                continue

            if db_data[0] not in self.def_basic_req:
                self.def_basic_req[db_data[0]] = []

            for split_data in db_data[1].split("\n"):
                self.def_basic_req[db_data[0]].append(split_data)

        self._pg.close()


    def get_all_deflist(self):
        self._pg.connect()
        sqlcmd = '''
            select definition_id from public.price_ana
        '''
        self._pg.execute(sqlcmd)
        result = [db_data[0] for db_data in self._pg.fetchall()]

        self._pg.close()

        return result


    def get_ref_basic_list(self, def_id, basic_name):
        result = []
        if def_id:
            if def_id in self.def_basic_req:
                for ref_data in self.def_basic_req[def_id]:
                    if ref_data in self.basic_req_dict:
                        result.append(ref_data)

        if basic_name:
            if basic_name in self.basic_req_dict:
                for ref_data in self.basic_req_dict[basic_name]:
                    if ref_data in self.basic_req_dict:
                        result.append(ref_data)

        return set(result)


    def write_chainlist_to_db(self, _pg, def_id, chain_list, result_info):
        sql_cmd = '''
        INSERT INTO public.basic_req_call(definition_id, basic_req_name_chain, chain_result)
        values (%s, %s, %s)
        '''
        _pg.execute(sql_cmd, (def_id, '->'.join(chain_list), result_info))


    def do_call_chain(self,_pg, def_id, call_list):
        if len(call_list) == 0:
            ref_basic_list = self.get_ref_basic_list(def_id, None)
        else:
            ref_basic_list = self.get_ref_basic_list(None, call_list[-1])

        if len(ref_basic_list) == 0:
            if len(call_list) > 0:
                self.write_chainlist_to_db(_pg, def_id, call_list, 'OK')
                call_list.pop(-1)
            return

        for ref_name in ref_basic_list:
            if ref_name in call_list:
                tmp_w_list = [_data for _data in call_list]
                tmp_w_list.append(ref_name)
                self.write_chainlist_to_db(_pg, def_id, tmp_w_list, 'NG')
                continue

            call_list.append(ref_name)
            self.do_call_chain(_pg, def_id, call_list)

        if len(call_list)>0:
            call_list.pop(-1)


    def create_call_chain(self):
        def_id_list = self.get_all_deflist()

        self._pg.connect()

        w=0
        for i,def_id in enumerate(def_id_list,0):
            print i, def_id
            self.do_call_chain(self._pg, def_id, [])

            w+=1
            if w == 256:
                self._pg.commit()
                w=0

        if w>0:
            self._pg.commit()

        self._pg.close()


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')

    AnalysisInfo().create_call_chain()

