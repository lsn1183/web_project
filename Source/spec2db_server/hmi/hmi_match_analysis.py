# -*- coding: UTF-8 -*-
import re
from Source.spec2db_server.hmi.hmi_base import HMIBase
import psycopg2
BASE_DB = "host='192.168.0.56' dbname='spec2db_1120' port='5432' user='postgres' password='pset123456'"


class HmiMatchAna(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def copy_analysis_from_base_db(self):
        self._pg.connect()
        sqlcmd = """
        DELETE FROM public.it_analysis;
        """
        self._pg.execute(sqlcmd)
        sqlcmd = """
        INSERT INTO public.it_analysis(
                    definition_id, unique_id, seq_diagram, asta_filename, application, new_date, exception)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        for row in self._get_analysi_from_base_db():
            self._pg.execute(sqlcmd, row)
        self._pg.commit()

    def update_analysis_info(self):
        sqlcmd = """
        update hmi.req as t1 set seq_diagram_file = asta_filenames, seq_diagram_no = seq_diagrams,
                                 definition_id = t2.definition_id, ana_unique_id = t2.unique_id, 
                                 application = t2.application, new_date = t2.new_date,
                                 exception = t2.exception
          from (
            select hu_id,
                   (array_agg(definition_id))[1] as definition_id,
                   (array_agg(unique_id))[1] as unique_id, 
                   array_to_string(array_agg(seq_diagram), chr(10)) seq_diagrams,
                   array_to_string(array_agg(asta_filename), chr(10)) as asta_filenames,
                   (array_agg(application))[1] application,
                   (array_agg(new_date))[1] new_date,
                   (array_agg(exception))[1] exception
              from (
                 SELECT hu_id, definition_id, unique_id,
                        seq_diagram, asta_filename, application, new_date, exception
                   from (
                    SELECT array_to_string(id_array[1:array_upper(id_array, 1) -1], '.') hu_id, 
                           definition_id, unique_id, seq_diagram, asta_filename, application, new_date,
                           exception
                    from (
                        SELECT definition_id, unique_id, seq_diagram, asta_filename, 
                               application, new_date, exception,
                               regexp_split_to_array(definition_id, E'\\.+') as id_array
                          FROM public.it_analysis
                      ) as a
                  ) as b
                  order by definition_id, unique_id
              ) as c
              group by hu_id
          ) as t2
          where (t1.definition_id = '' or t1.definition_id is null) and (t1.hu_id = t2.hu_id)
        """
        self._pg.connect()
        self._pg.execute(sqlcmd)
        self._pg.commit()

    def _get_analysi_from_base_db(self):
        conn = psycopg2.connect(BASE_DB)
        pgcur = conn.cursor()
        sqlcmd = """
                SELECT definition_id, unique_id,
                       seq_diagram, asta_filename,
                       val as aplication, new_date,
                       exception
                  FROM spec.analysis as a
                  left join spec.analysis_model_rel as b
                  on a.analysis_rc_id = b.analysis_rc_id and model_id = 1
                  order by definition_id, unique_id;
                """
        pgcur.execute(sqlcmd)
        rows = pgcur.fetchall()
        conn.close()
        return rows


def main():
    obj = HmiMatchAna()
    obj.copy_analysis_from_base_db()
    obj.update_analysis_info()


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()