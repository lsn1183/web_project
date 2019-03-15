# -*- coding: UTF-8 -*-
from import_base import ImportBase


class AnaCollectSeq(ImportBase):
    def __init__(self):
        ImportBase.__init__(self)

    def collect_seq(self):
        """归集时序
        :return:
        """
        self._pg.connect()
        sqlcmd = """
        drop table if exists price_ana_collect_seq;
        
        CREATE TABLE price_ana_collect_seq
        (
          record_id      serial primary key,
          definition_id  character varying(30),
          unique_id      integer,
          collect_seq_id integer,
          model_id       integer,
          gid            integer,
          seq_id         integer,
          seq            character varying,
          user_case      character varying
        );
        """
        self._pg.execute(sqlcmd)
        self._pg.commit()
        for row in self._get_seq(self._pg):
            all_conllect_list = []
            one_conllect_list = []
            definition_id, unique_id, seq_id_list, model_id_list, gid_list, seq_list = row
            for i, model_id in enumerate(model_id_list):
                if model_id in (1, 2):  # 1: Application, 2: kernel
                    if one_conllect_list:
                        all_conllect_list.append(one_conllect_list)
                        one_conllect_list = []
                else:
                    one_conllect_list.append((seq_id_list[i], model_id_list[i], gid_list[i], seq_list[i]))
            if one_conllect_list:
                all_conllect_list.append(one_conllect_list)
            # store
            for collect_seq_id, one_conllect_list in enumerate(all_conllect_list):
                for (seq_id, model_id, gid, seq) in one_conllect_list:
                    params = (definition_id, unique_id, collect_seq_id, model_id, gid, seq_id, seq)
                    self._insert(self._pg, params)
        self.update_user_case(self._pg)
        self._pg.commit()

    def update_user_case(self, pg):
        sqlcmd = """
        update price_ana_collect_seq as a set user_case = b.user_case
          from (
            SELECT record_id,
                   (regexp_matches(seq, '[\w|\d|_]+<?\w?>?\_0[\w|\d]+', 'g'))[1] as user_case
            from price_ana_collect_seq
          ) as b
          where a.record_id = b.record_id
        """
        pg.execute(sqlcmd)

    def _insert(self, pg, params):
        sqlcmd = """
        INSERT INTO public.price_ana_collect_seq(
                    definition_id, unique_id, collect_seq_id, model_id, 
                    gid, seq_id, seq)
            VALUES (%s, %s, %s, %s, 
                    %s, %s, %s);
        """
        pg.execute(sqlcmd, params)

    def _get_seq(self, pg):
        sqlcmd = """
        SELECT definition_id, unique_id,
               array_agg(seq_id) seq_id_list, 
               array_agg(model_id) model_id_list,
               array_agg(gid) gid_list,
               array_agg(seq) seq_list
          FROM (
            select b.definition_id, unique_id, model_id, gid, seq_id, seq
              from price_ana as a
              LEFT JOIN analysis_split_sequence as b
              ON a.definition_id = b.definition_id
              where seq_id <> 0
              order by b.definition_id, unique_id, seq_id, model_id, gid
          ) as a
          group by definition_id, unique_id
        """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        return rows


if __name__ == '__main__':
    import sys, os
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    os.chdir('../')
    obj = AnaCollectSeq()
    obj.collect_seq()
