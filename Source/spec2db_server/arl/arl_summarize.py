# -*- coding: UTF-8 -*-
"""
Created on 2017-10-15

@author: hcz
"""
from Source.spec2db_server.arl.arl_server import ServiceBase


class ArlSummarize(ServiceBase):
    """
    """
    def __init__(self):
        ServiceBase.__init__(self)

    def summarize_by_user(self, date):
        result = {"result": "NG"}
        if date:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-' and to_date(hu_date, 'YYYY/MM/DD') <= %s"
            def_condition_str = "where exclude_flag = False and def_date <> '-' and to_date(def_date, 'YYYY/MM/DD') <= %s"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-' and to_date(analysis_date, 'YYYY/MM/DD') <= %s"
            params = [date, date, date]
        else:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-'"
            def_condition_str = "where exclude_flag = False and def_date <> '-'"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-'"
            params = []
        sqlcmd = """
        SELECT group_name,
               ARRAY_AGG(user_name) user_names,
               array_agg(all_arl_num) all_arl_nums,
               array_agg(hu_arl_num) hu_arl_nums,
               array_agg(all_hu_num) all_hu_nums,
               array_agg(definition_arl_num) definition_arl_nums,
               array_agg(all_definition_num) all_definition_nums,
               array_agg(analysis_arl_num) analysis_arl_num,
               array_agg(analysis_num) analysis_nums,
               array_agg(hu_plan_num) hu_plan_nums,
               array_agg(def_plan_num) def_plan_nums,
               array_agg(analysis_plan_num) analysis_plan_nums
         from (
                SELECT group_name,          -- 组
                       user_name,           -- 担当
                       all_arl_num,         -- ARL总数
                       hu_arl_num,          -- HU==>ARL
                       all_hu_num,          -- 已有HU总数
                       definition_arl_num,   -- [TAGL要件定义]==>ARL
                       all_definition_num,  -- 已有[TAGL要件定义]总数
                       analysis_arl_num,    -- Ana对应的ARL
                       analysis_num,       -- 已经[TAGL要件分析]
                       hu_plan_num,         -- 计划HU
                       def_plan_num,        -- 计划DEF
                       analysis_plan_num    -- analysis   
                  FROM (
                    -- 组员ARL总数
                    SELECT group_name, group_id, user_name, user_id, count(arl_id) all_arl_num
                      FROM (
                        SELECT group_name, t1.group_id, t3.user_name, t1.user_id, arl_id
                          FROM spec.arl as t1
                          LEFT JOIN spec.arl_group as t2
                          on t1.group_id = t2.group_id
                          LEFT JOIN spec.arl_user as t3
                          on t1.user_id = t3.user_id
                          where exclude_flag = False
                                and t2.group_id is not null 
                    ) AS a
                    group by group_name, group_id, user_name, user_id
                  ) AS tt1
                  LEFT JOIN (
                        -- 已经有相应HU的ARL数目
                    SELECT t1.group_id, t1.user_id, count(arl_id) hu_arl_num
                      FROM spec.arl as t1
                      where arl_id in (
                        select arl_id
                        from spec.hu
                     ) and exclude_flag = False
                     group by t1.group_id, t1.user_id
                  ) as tt2
                  ON tt1.group_id = tt2.group_id and tt1.user_id = tt2.user_id
                  LEFT JOIN (
                        -- 组员已经有相应HU总数, 注：基本要件，会被过滤掉
                    SELECT t1.group_id, t1.user_id, count(hu_id) all_hu_num
                      FROM spec.arl as t1
                      inner join spec.hu as t2
                      on t1.arl_id = t2.arl_id
                      where exclude_flag = False
                      group by t1.group_id, t1.user_id
                  ) as tt3
                  ON tt1.group_id = tt3.group_id and tt1.user_id = tt3.user_id
                  LEFT JOIN (
                    -- 已经有相应DEFiNITION的ARL数目,
                    SELECT group_id, user_id, count(arl_id) as definition_arl_num
                      FROM (
                        SELECT DISTINCT t1.group_id, t1.user_id, t1.arl_id
                          FROM spec.arl as t1
                          inner join spec.hu as t2
                          on t1.arl_id = t2.arl_id
                          INNER join spec.definition as t3
                          on t2.hu_id = t3.hu_def_id
                          where exclude_flag = False
                      ) as a
                      group by group_id, user_id
                  ) as tt4
                  ON tt1.group_id = tt4.group_id and tt1.user_id = tt4.user_id
                  ----TAGL 要件定义--------------------------
                  LEFT JOIN (
                    -- 组员已经有相应DEFINITION总数
                    SELECT t1.group_id, t1.user_id, count(definition_id) all_definition_num
                      FROM spec.arl as t1
                      inner join spec.hu as t2
                      on t1.arl_id = t2.arl_id
                      LEFT JOIN spec.definition as t3
                      on t2.hu_id = t3.hu_def_id
                      where exclude_flag = False
                      group by t1.group_id, t1.user_id
                  ) as tt5
                  ON tt1.group_id = tt5.group_id and tt1.user_id = tt5.user_id
                  ------TAGL 要件分析
                  LEFT JOIN (
                    -- 已经有相应DEFiNITION的ARL数目,
                    SELECT group_id, user_id, count(arl_id) as analysis_arl_num
                      FROM (
                        SELECT DISTINCT t1.group_id, t1.user_id, t1.arl_id
                          FROM spec.arl as t1
                          inner join spec.hu as t2
                          on t1.arl_id = t2.arl_id
                          INNER join spec.definition as t3
                          on t2.hu_id = t3.hu_def_id
                          INNER JOIN spec.analysis as t4
                          on t3.definition_id = t4.definition_id
                          where exclude_flag = False
                      ) as a
                      group by group_id, user_id
                  ) as tt10
                  ON tt1.group_id = tt10.group_id and tt1.user_id = tt10.user_id
                  LEFT JOIN (
                    SELECT t1.group_id, t1.user_id, count(definition_id) analysis_num
                      FROM spec.arl as t1
                      inner join spec.hu as t2
                      on t1.arl_id = t2.arl_id
                      LEFT JOIN spec.definition as t3
                      on t2.hu_id = t3.hu_def_id
                      where definition_id in (
                        select definition_id
                          from spec.analysis
                      ) and exclude_flag = False
                      group by t1.group_id, t1.user_id
                  ) as tt6
                  ON tt1.group_id = tt6.group_id and tt1.user_id = tt6.user_id
                  LEFT JOIN (
                    SELECT group_id, user_id, count(t2.arl_id) hu_plan_num 
                        from spec.arl as t1 left join spec.arl_schedule as t2
                        on t1.arl_id = t2.arl_id 
                        {hu_condition_str}
                        group by group_id, user_id
                    ) as tt7
                    on tt1.group_id = tt7.group_id and tt1.user_id = tt7.user_id
                  LEFT JOIN (
                    SELECT group_id, user_id, count(t2.arl_id) def_plan_num 
                        from spec.arl as t1 left join spec.arl_schedule as t2
                        on t1.arl_id = t2.arl_id 
                        {def_condition_str}
                        group by group_id, user_id   
                    ) as tt8
                  on tt1.group_id = tt8.group_id and tt1.user_id = tt8.user_id
                  LEFT JOIN (
                    SELECT group_id, user_id, count(t2.arl_id) analysis_plan_num 
                      from spec.arl as t1 left join spec.arl_schedule as t2
                      on t1.arl_id = t2.arl_id 
                      {ana_condition_str}
                      group by group_id, user_id      
                    ) as tt9
                    ON tt1.group_id = tt9.group_id and tt1.user_id = tt9.user_id
                    ORDER BY group_name, user_name
                    ) as ttt1
                    group by group_name
                 """.format(hu_condition_str=hu_condition_str,
                            def_condition_str=def_condition_str,
                            ana_condition_str=ana_condition_str)
        rows, content = [], []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, params)
            rows = self._pg.fetchall()
        except Exception as e:
            print
        finally:
            self._pg.close()
        # sum_data = {"major_category": "总计"}
        # key_list = ["all_arl_num", "hu_arl_num", "all_hu_num", "definition_hu_num",
        #             "all_definition_num", "analysis_def_num", "analysis_num", "hu_plan_num",
        #             "def_plan_num", "analysis_plan_num"]
        # self.mysum(sum_data, key_list, [0] * len(key_list))
        for row in rows:
            group_dict = dict()
            group_dict["group_name"] = row[0]  # 组名
            user_list = []
            for (user_name, all_arl_num, hu_arl_num, all_hu_num,
                 definition_arl_num, all_definition_num, analysis_arl_num, analysis_num,
                 hu_plan_num, def_plan_num, analysis_plan_num)in zip(*row[1:]):
                user_dict = dict()
                user_dict["user_name"] = user_name  # 担当
                user_dict["all_arl_num"] = all_arl_num  # ARL总数
                user_dict["hu_arl_num"] = hu_arl_num  # HU里的ARL
                user_dict["all_hu_num"] = all_hu_num  # 已有HU总数
                user_dict["definition_hu_num"] = definition_arl_num  # [TAGL要件定义]里的ARL
                user_dict["all_definition_num"] = all_definition_num  # 已有[TAGL要件定义]总数
                user_dict["analysis_def_num"] = analysis_arl_num  # [TAGL要件分析]里的[ARL]
                user_dict["analysis_num"] = analysis_num  # 已经[TAGL要件分析]
                user_dict["hu_plan_num"] = hu_plan_num
                user_dict["def_plan_num"] = def_plan_num
                user_dict["analysis_plan_num"] = analysis_plan_num
                user_list.append(user_dict)
                # self.mysum(sum_data, key_list, row[2:])
            group_dict["user_list"] = user_list
            content.append(group_dict)
        if content:
            # content.append(sum_data)
            result["content"] = content
            result["result"] = "OK"
        return result

    def summarize_by_category2(self, date):
        """大分类: 不包含小组和担当"""
        result = {"result": "NG"}
        if date:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-' and to_date(hu_date, 'YYYY/MM/DD') <= %s"
            def_condition_str = "where exclude_flag = False and def_date <> '-' and to_date(def_date, 'YYYY/MM/DD') <= %s"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-' and to_date(analysis_date, 'YYYY/MM/DD') <= %s"
            params = [date, date, date]
        else:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-'"
            def_condition_str = "where exclude_flag = False and def_date <> '-'"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-'"
            params = []
        sqlcmd = """
        SELECT major_category,      -- 大分類
               --group_name,          -- 组
               --user_name,           -- 担当
               all_arl_num,         -- ARL总数
               hu_arl_num,          -- HU==>ARL
               all_hu_num,          -- 已有HU总数
               definition_arl_num,   -- [TAGL要件定义]==>ARL
               all_definition_num,  -- 已有[TAGL要件定义]总数
               analysis_arl_num,    -- [TAGL要件分析]==>ARL
               analysis_num,        -- 已经[TAGL要件分析]
               hu_plan_num,         -- 计划HU
               def_plan_num,        -- 计划DEF
               analysis_plan_num    -- analysis
          FROM (
            -- 组员ARL总数
            SELECT cat_id1, major_category, count(arl_id) all_arl_num
              FROM (
                SELECT cat_id1, major_category, group_name,
                       t1.group_id, t3.user_name, t1.user_id, arl_id
                  FROM spec.arl as t1
                  LEFT JOIN spec.arl_group as t2
                  on t1.group_id = t2.group_id
                  LEFT JOIN spec.arl_user as t3
                  on t1.user_id = t3.user_id
                  where exclude_flag = False
                        and t2.group_id is not null 
            ) AS a
            group by cat_id1, major_category
          ) AS tt1
          LEFT JOIN (
                -- 已经有相应HU的ARL数目
            SELECT cat_id1, count(arl_id) hu_arl_num
              FROM spec.arl as t1
              where arl_id in (
                select arl_id
                from spec.hu
             ) and exclude_flag = False
             group by cat_id1
          ) as tt2
          ON tt1.cat_id1 = tt2.cat_id1
          LEFT JOIN (
            -- 组员已经有相应HU总数, 注：基本要件，会被过滤掉
            SELECT t1.cat_id1, count(hu_id) all_hu_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              where exclude_flag = False
              group by t1.cat_id1
          ) as tt3
          ON tt1.cat_id1 = tt3.cat_id1
          LEFT JOIN (
            -- 已经有相应DEFiNITION的ARL数目, 
            SELECT cat_id1, count(arl_id) as definition_arl_num
              FROM (
                SELECT DISTINCT t1.cat_id1, t1.arl_id
                  FROM spec.arl as t1
                  inner join spec.hu as t2
                  on t1.arl_id = t2.arl_id
                  INNER join spec.definition as t3
                  on t2.hu_id = t3.hu_def_id
                  where exclude_flag = False
              ) as a
              group by cat_id1
          ) as tt4
          ON tt1.cat_id1 = tt4.cat_id1
          ----TAGL 要件定义--------------------------
          LEFT JOIN (
                -- 组员已经有相应DEFINITION总数
            SELECT t1.cat_id1, count(definition_id) all_definition_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              LEFT JOIN spec.definition as t3
              on t2.hu_id = t3.hu_def_id
              where exclude_flag = False
              group by t1.cat_id1
          ) as tt5
          ON tt1.cat_id1 = tt5.cat_id1
          ------TAGL 要件分析
          -- 已经有相应Analysis的ARL数目
          LEFT JOIN (
            SELECT cat_id1, count(arl_id) as analysis_arl_num
              FROM (
                SELECT DISTINCT t1.cat_id1,t1.arl_id
                  FROM spec.arl as t1
                  inner join spec.hu as t2
                  on t1.arl_id = t2.arl_id
                  INNER join spec.definition as t3
                  on t2.hu_id = t3.hu_def_id
                  inner join spec.analysis as t4
                  on t3.definition_id = t4.definition_id
                  where exclude_flag = False
              ) as a
              group by cat_id1
          ) as tt10
          ON tt1.cat_id1 = tt10.cat_id1
          LEFT JOIN (
            SELECT t1.cat_id1, count(definition_id) analysis_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              LEFT JOIN spec.definition as t3
              on t2.hu_id = t3.hu_def_id
              where definition_id in (
                select definition_id
                  from spec.analysis
              ) and exclude_flag = False
              group by t1.cat_id1
          ) as tt6
          ON tt1.cat_id1 = tt6.cat_id1
          left join (
            SELECT cat_id1, count(t1.arl_id) as hu_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {hu_condition_str}
              group by cat_id1
          ) as tt7
          ON tt1.cat_id1 = tt7.cat_id1
          LEFT JOIN (
            SELECT cat_id1, count(t1.arl_id) as def_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {def_condition_str}
              group by cat_id1
          ) as tt8
          ON tt1.cat_id1 = tt8.cat_id1
          LEFT JOIN (
            SELECT cat_id1, count(t1.arl_id) as analysis_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {ana_condition_str}
              group by cat_id1
          ) as tt9
          ON tt1.cat_id1 = tt9.cat_id1
          ORDER BY major_category
        """.format(hu_condition_str=hu_condition_str,
                   def_condition_str=def_condition_str,
                   ana_condition_str=ana_condition_str)
        rows = []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, params)
            rows = self._pg.fetchall()
        except Exception as e:
            print
        finally:
            self._pg.close()
        content = []
        sum_data = {"major_category": "总计"}
        key_list = ["all_arl_num", "hu_arl_num", "all_hu_num", "definition_hu_num",
                    "all_definition_num", "analysis_def_num", "analysis_num", "hu_plan_num",
                    "def_plan_num", "analysis_plan_num"]
        # key_list = ["all_arl_num"]
        self.mysum(sum_data, key_list, [0] * len(key_list))
        for row in rows:
            user_dict = dict()
            user_dict["major_category"] = row[0]  # 大分類
            # group_name = row[1]  # 组
            # user_dict["user_name"] = row[2]  # 担当
            user_dict["all_arl_num"] = row[1]  # ARL总数
            user_dict["hu_arl_num"] = row[2]  # HU里的ARL
            user_dict["all_hu_num"] = row[3]  # 已有HU总数
            user_dict["definition_hu_num"] = row[4]  # [TAGL要件定义]里的ARL
            user_dict["all_definition_num"] = row[5]  # 已有[TAGL要件定义]总数
            user_dict["analysis_def_num"] = row[6]  # [TAGL要件分析]里的ARL
            user_dict["analysis_num"] = row[7]  # 已经[TAGL要件分析]
            user_dict["hu_plan_num"] = row[8]  # 计划HU
            user_dict["def_plan_num"] = row[9]  # 计划DEF
            user_dict["analysis_plan_num"] = row[10]  # 计划analysis
            content.append(user_dict)
            # self.mysum(sum_data, key_list, row[1:])
        if content:
            # content.append(sum_data)
            result["content"] = content
            result["result"] = "OK"
        return result

    # def summarize_by_category3(self, date):
    #     """大分类: 包含小组和担当"""
    #     result = {"result": "NG"}
    #     if date:
    #         hu_condition_str = "where exclude_flag = False and hu_date <> '-' and to_date(hu_date, 'YYYY/MM/DD') <= %s"
    #         def_condition_str = "where exclude_flag = False and def_date <> '-' and to_date(def_date, 'YYYY/MM/DD') <= %s"
    #         ana_condition_str = "where exclude_flag = False and analysis_date <> '-' and to_date(analysis_date, 'YYYY/MM/DD') <= %s"
    #         params = [date, date, date]
    #     else:
    #         hu_condition_str = "where exclude_flag = False and hu_date <> '-'"
    #         def_condition_str = "where exclude_flag = False and def_date <> '-'"
    #         ana_condition_str = "where exclude_flag = False and analysis_date <> '-'"
    #         params = []
    #     sqlcmd = """
    #      SELECT major_category,      -- 大分類
    #             group_name,          -- 组
    #             user_name,           -- 担当
    #             all_arl_num,         -- ARL总数
    #             hu_arl_num,          -- HU==>ARL
    #             all_hu_num,          -- 已有HU总数
    #             definition_arl_num,   -- [TAGL要件定义]==>ARL
    #             all_definition_num,  -- 已有[TAGL要件定义]总数
    #             analysis_arl_num,    -- [TAGL要件分析]==>ARL
    #             analysis_num,        -- 已经[TAGL要件分析]
    #             hu_plan_num,         -- 计划HU
    #             def_plan_num,        -- 计划DEF
    #             analysis_plan_num    -- analysis
    #        FROM (
    #          -- 组员ARL总数
    #          SELECT cat_id1, major_category, group_name, group_id,
    #                 user_name, user_id, count(arl_id) all_arl_num
    #            FROM (
    #              SELECT cat_id1, major_category, group_name,
    #                     t1.group_id, t3.user_name, t1.user_id, arl_id
    #                FROM spec.arl as t1
    #                LEFT JOIN spec.arl_group as t2
    #                on t1.group_id = t2.group_id
    #                LEFT JOIN spec.arl_user as t3
    #                on t1.user_id = t3.user_id
    #                where exclude_flag = False
    #                      and t2.group_id is not null
    #          ) AS a
    #          group by cat_id1, major_category, group_name, group_id, user_name, user_id
    #        ) AS tt1
    #        LEFT JOIN (
    #              -- 已经有相应HU的ARL数目
    #          SELECT cat_id1, t1.group_id, t1.user_id, count(arl_id) hu_arl_num
    #            FROM spec.arl as t1
    #            where arl_id in (
    #              select arl_id
    #              from spec.hu
    #           ) and exclude_flag = False
    #           group by cat_id1, t1.group_id, t1.user_id
    #        ) as tt2
    #        ON tt1.cat_id1 = tt2.cat_id1 and
    #           tt1.group_id = tt2.group_id and
    #           tt1.user_id = tt2.user_id
    #        LEFT JOIN (
    #              -- 组员已经有相应HU总数, 注：基本要件，会被过滤掉
    #          SELECT t1.cat_id1, t1.group_id, t1.user_id, count(hu_id) all_hu_num
    #            FROM spec.arl as t1
    #            inner join spec.hu as t2
    #            on t1.arl_id = t2.arl_id
    #            where exclude_flag = False
    #            group by t1.cat_id1, t1.group_id, t1.user_id
    #        ) as tt3
    #        ON tt1.cat_id1 = tt3.cat_id1 and
    #           tt1.group_id = tt3.group_id and
    #           tt1.user_id = tt3.user_id
    #        LEFT JOIN (
    #          -- 已经有相应DEFiNITION的ARL数目,
    #          SELECT cat_id1, group_id, user_id, count(arl_id) as definition_arl_num
    #            FROM (
    #              SELECT DISTINCT t1.cat_id1, t1.group_id, t1.user_id, t1.arl_id
    #                FROM spec.arl as t1
    #                inner join spec.hu as t2
    #                on t1.arl_id = t2.arl_id
    #                INNER join spec.definition as t3
    #                on t2.hu_id = t3.hu_def_id
    #                where exclude_flag = False
    #            ) as a
    #            group by cat_id1, group_id, user_id
    #        ) as tt4
    #        ON tt1.cat_id1 = tt4.cat_id1 and
    #           tt1.group_id = tt4.group_id and
    #           tt1.user_id = tt4.user_id
    #        ----TAGL 要件定义--------------------------
    #        LEFT JOIN (
    #              -- 组员已经有相应DEFINITION总数
    #          SELECT t1.cat_id1, t1.group_id, t1.user_id, count(definition_id) all_definition_num
    #            FROM spec.arl as t1
    #            inner join spec.hu as t2
    #            on t1.arl_id = t2.arl_id
    #            LEFT JOIN spec.definition as t3
    #            on t2.hu_id = t3.hu_def_id
    #            where exclude_flag = False
    #            group by t1.cat_id1, t1.group_id, t1.user_id
    #        ) as tt5
    #        ON tt1.cat_id1 = tt5.cat_id1 and
    #           tt1.group_id = tt5.group_id and
    #           tt1.user_id = tt5.user_id
    #        ------TAGL 要件分析
    #        -- 已经有相应Analysis的ARL数目
    #        LEFT JOIN (
    #          SELECT cat_id1, group_id, user_id, count(arl_id) as analysis_arl_num
    #            FROM (
    #              SELECT DISTINCT t1.cat_id1, t1.group_id, t1.user_id, t1.arl_id
    #                FROM spec.arl as t1
    #                inner join spec.hu as t2
    #                on t1.arl_id = t2.arl_id
    #                INNER join spec.definition as t3
    #                on t2.hu_id = t3.hu_def_id
    #                inner join spec.analysis as t4
    #                on t3.definition_id = t4.definition_id
    #                where exclude_flag = False
    #            ) as a
    #            group by cat_id1, group_id, user_id
    #        ) as tt10
    #        ON tt1.cat_id1 = tt10.cat_id1 and
    #           tt1.group_id = tt10.group_id and
    #           tt1.user_id = tt10.user_id
    #        LEFT JOIN (
    #          SELECT t1.cat_id1, t1.group_id, t1.user_id, count(definition_id) analysis_num
    #            FROM spec.arl as t1
    #            inner join spec.hu as t2
    #            on t1.arl_id = t2.arl_id
    #            LEFT JOIN spec.definition as t3
    #            on t2.hu_id = t3.hu_def_id
    #            where definition_id in (
    #              select definition_id
    #                from spec.analysis
    #            ) and exclude_flag = False
    #            group by t1.cat_id1, t1.group_id, t1.user_id
    #        ) as tt6
    #        ON tt1.cat_id1 = tt6.cat_id1 and
    #           tt1.group_id = tt6.group_id and
    #           tt1.user_id = tt6.user_id
    #        left join (
    #          SELECT cat_id1, group_id, user_id, count(t1.arl_id) as hu_plan_num
    #            FROM spec.arl_schedule as t1
    #            inner JOIN spec.arl as t2
    #            ON t1.arl_id = t2.arl_id
    #            {hu_condition_str}
    #            group by cat_id1, group_id, user_id
    #        ) as tt7
    #        ON tt1.cat_id1 = tt7.cat_id1 and
    #           tt1.group_id = tt7.group_id and
    #           tt1.user_id = tt7.user_id
    #        LEFT JOIN (
    #          SELECT cat_id1, group_id, user_id, count(t1.arl_id) as def_plan_num
    #            FROM spec.arl_schedule as t1
    #            inner JOIN spec.arl as t2
    #            ON t1.arl_id = t2.arl_id
    #            {def_condition_str}
    #            group by cat_id1, group_id, user_id
    #        ) as tt8
    #        ON tt1.cat_id1 = tt8.cat_id1 and
    #           tt1.group_id = tt8.group_id and
    #           tt1.user_id = tt8.user_id
    #        LEFT JOIN (
    #          SELECT cat_id1, group_id, user_id, count(t1.arl_id) as analysis_plan_num
    #            FROM spec.arl_schedule as t1
    #            inner JOIN spec.arl as t2
    #            ON t1.arl_id = t2.arl_id
    #            {ana_condition_str}
    #            group by cat_id1, group_id, user_id
    #        ) as tt9
    #        ON tt1.cat_id1 = tt9.cat_id1 and
    #           tt1.group_id = tt9.group_id and
    #           tt1.user_id = tt9.user_id
    #        ORDER BY major_category, group_name, user_name
    #      """.format(hu_condition_str=hu_condition_str,
    #                 def_condition_str=def_condition_str,
    #                 ana_condition_str=ana_condition_str)
    #     rows = []
    #     try:
    #         self._pg.connect()
    #         self._pg.execute(sqlcmd, params)
    #         rows = self._pg.fetchall()
    #     except Exception as e:
    #         print
    #     finally:
    #         self._pg.close()
    #     content = []
    #     for row in rows:
    #         major_category = row[0]  # 大分類
    #         group_name = row[1]  # 组
    #         user_dict = dict()
    #         user_dict["user_name"] = row[2]  # 担当
    #         user_dict["all_arl_num"] = row[3]  # ARL总数
    #         user_dict["hu_arl_num"] = row[4]  # HU里的ARL
    #         user_dict["all_hu_num"] = row[5]  # 已有HU总数
    #         user_dict["definition_hu_num"] = row[6]  # [TAGL要件定义]里的ARL
    #         user_dict["all_definition_num"] = row[7]  # 已有[TAGL要件定义]总数
    #         user_dict["analysis_def_num"] = row[8]  # [TAGL要件分析]里的ARL
    #         user_dict["analysis_num"] = row[9]  # 已经[TAGL要件分析]
    #         user_dict["hu_plan_num"] = row[10]  # 计划HU
    #         user_dict["def_plan_num"] = row[11]  # 计划DEF
    #         user_dict["analysis_plan_num"] = row[12]  # 计划analysis
    #         if not content or major_category != content[-1].get("major_category"):
    #             group_list = [{"group_name": group_name,
    #                            "user_list": [user_dict]}]
    #             content.append({"major_category": major_category,
    #                             "group_list": group_list})
    #         else:
    #             group_list = content[-1].get("group_list")
    #             if group_name == group_list[-1].get("group_name"):
    #                 user_list = group_list[-1].get("user_list")
    #             else:
    #                 user_list = []
    #                 group_list.append({"group_name": group_name,
    #                                    "user_list": user_list})
    #             user_list.append(user_dict)
    #     if content:
    #         result["content"] = content
    #         result["result"] = "OK"
    #     return result

    def summarize_by_category(self, date):
        """大分类、小分類
        """
        result = {"result": "NG"}
        if date:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-' and to_date(hu_date, 'YYYY/MM/DD') <= %s"
            def_condition_str = "where exclude_flag = False and def_date <> '-' and to_date(def_date, 'YYYY/MM/DD') <= %s"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-' and to_date(analysis_date, 'YYYY/MM/DD') <= %s"
            params = [date, date, date]
        else:
            hu_condition_str = "where exclude_flag = False and hu_date <> '-'"
            def_condition_str = "where exclude_flag = False and def_date <> '-'"
            ana_condition_str = "where exclude_flag = False and analysis_date <> '-'"
            params = []
        sqlcmd = """
        SELECT major_category,      -- 大分類
               small_category,       -- 小分類
               all_arl_num,         -- ARL总数
               hu_arl_num,          -- HU==>ARL
               all_hu_num,          -- 已有HU总数
               definition_arl_num,   -- [TAGL要件定义]==>ARL
               all_definition_num,  -- 已有[TAGL要件定义]总数
               analysis_arl_num,    -- [TAGL要件分析]==>ARL
               analysis_num,        -- 已经[TAGL要件分析]
               hu_plan_num,         -- 计划HU
               def_plan_num,        -- 计划DEF
               analysis_plan_num    -- analysis
          FROM (
            -- 组员ARL总数
            SELECT cat_id1, major_category, cat_id3, small_category,
                   count(arl_id) all_arl_num
              FROM spec.arl as t1
              where exclude_flag = False and group_id is not null 
              group by cat_id1, major_category, cat_id3, small_category
          ) AS tt1
          LEFT JOIN (
                -- 已经有相应HU的ARL数目
            SELECT cat_id1, cat_id3, count(arl_id) hu_arl_num
              FROM spec.arl as t1
              where arl_id in (
                select arl_id
                from spec.hu
             ) and exclude_flag = False
             group by cat_id1, cat_id3
          ) as tt2
          ON tt1.cat_id1 = tt2.cat_id1 and
             tt1.cat_id3 = tt2.cat_id3 
          LEFT JOIN (
                -- 组员已经有相应HU总数, 注：基本要件，会被过滤掉
            SELECT t1.cat_id1, cat_id3, count(hu_id) all_hu_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              where exclude_flag = False
              group by t1.cat_id1, t1.cat_id3
          ) as tt3
          ON tt1.cat_id1 = tt3.cat_id1 and
             tt1.cat_id3 = tt3.cat_id3
          LEFT JOIN (
            -- 已经有相应DEFiNITION的ARL数目, 
            SELECT cat_id1, cat_id3, count(arl_id) as definition_arl_num
              FROM (
                SELECT DISTINCT t1.cat_id1, t1.cat_id3, t1.arl_id
                  FROM spec.arl as t1
                  inner join spec.hu as t2
                  on t1.arl_id = t2.arl_id
                  INNER join spec.definition as t3
                  on t2.hu_id = t3.hu_def_id
                  where exclude_flag = False
              ) as a
              group by cat_id1, cat_id3
          ) as tt4
          ON tt1.cat_id1 = tt4.cat_id1 and
             tt1.cat_id3 = tt4.cat_id3 
          ----TAGL 要件定义--------------------------
          LEFT JOIN (
            -- 组员已经有相应DEFINITION总数
            SELECT t1.cat_id1, t1.cat_id3, count(definition_id) all_definition_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              LEFT JOIN spec.definition as t3
              on t2.hu_id = t3.hu_def_id
              where exclude_flag = False
              group by t1.cat_id1, t1.cat_id3
          ) as tt5
          ON tt1.cat_id1 = tt5.cat_id1 and
             tt1.cat_id3 = tt5.cat_id3 
          ------TAGL 要件分析
          left join (
            -- 已经有相应DEFiNITION的ARL数目, 
            SELECT cat_id1, cat_id3, count(arl_id) as analysis_arl_num
              FROM (
                SELECT DISTINCT t1.cat_id1, t1.cat_id3, t1.arl_id
                  FROM spec.arl as t1
                  inner join spec.hu as t2
                  on t1.arl_id = t2.arl_id
                  INNER join spec.definition as t3
                  on t2.hu_id = t3.hu_def_id
                  inner join spec.analysis as t4
                  on t3.definition_id = t4.definition_id
                  where exclude_flag = False
              ) as a
              group by cat_id1, cat_id3
          ) as tt10
          ON tt1.cat_id1 = tt10.cat_id1 and
             tt1.cat_id3 = tt10.cat_id3
          LEFT JOIN (
            SELECT t1.cat_id1, t1.cat_id3, count(definition_id) analysis_num
              FROM spec.arl as t1
              inner join spec.hu as t2
              on t1.arl_id = t2.arl_id
              LEFT JOIN spec.definition as t3
              on t2.hu_id = t3.hu_def_id
              where definition_id in (
                select definition_id
                  from spec.analysis
              ) and exclude_flag = False
              group by t1.cat_id1, t1.cat_id3
          ) as tt6
          ON tt1.cat_id1 = tt6.cat_id1 and
             tt1.cat_id3 = tt6.cat_id3
          left join (
            SELECT cat_id1, cat_id3, count(t1.arl_id) as hu_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {hu_condition_str}
              group by cat_id1, cat_id3
          ) as tt7
          ON tt1.cat_id1 = tt7.cat_id1 and
             tt1.cat_id3 = tt7.cat_id3
          LEFT JOIN (
            SELECT cat_id1, cat_id3, count(t1.arl_id) as def_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {def_condition_str}
              group by cat_id1, cat_id3
          ) as tt8
          ON tt1.cat_id1 = tt8.cat_id1 and
             tt1.cat_id3 = tt8.cat_id3
          LEFT JOIN (
            SELECT cat_id1, cat_id3, count(t1.arl_id) as analysis_plan_num
              FROM spec.arl_schedule as t1
              inner JOIN spec.arl as t2
              ON t1.arl_id = t2.arl_id
              {ana_condition_str}
              group by cat_id1, cat_id3
          ) as tt9
          ON tt1.cat_id1 = tt9.cat_id1 and
             tt1.cat_id3 = tt9.cat_id3
          ORDER BY major_category, small_category
        """.format(hu_condition_str=hu_condition_str,
                   def_condition_str=def_condition_str,
                   ana_condition_str=ana_condition_str)
        rows, content = [], []
        try:
            self._pg.connect()
            self._pg.execute(sqlcmd, params)
            rows = self._pg.fetchall()
        except Exception as e:
            print
        finally:
            self._pg.close()
        # sum_data = {"major_category": "总计"}
        # key_list = ["all_arl_num", "hu_arl_num", "all_hu_num", "definition_hu_num",
        #             "all_definition_num", "analysis_def_num", "analysis_num", "hu_plan_num",
        #             "def_plan_num", "analysis_plan_num"]
        # self.mysum(sum_data, key_list, [0]*len(key_list))
        for row in rows:
            major_category = row[0]  # 大分類
            user_dict = dict()
            user_dict["small_category"] = row[1]  # 担当
            user_dict["all_arl_num"] = row[2]  # ARL总数
            user_dict["hu_arl_num"] = row[3]  # HU里的ARL
            user_dict["all_hu_num"] = row[4]  # 已有HU总数
            user_dict["definition_hu_num"] = row[5]  # [TAGL要件定义]里的ARL
            user_dict["all_definition_num"] = row[6]  # 已有[TAGL要件定义]总数
            user_dict["analysis_def_num"] = row[7]  # [TAGL要件分析]里的[TAGL要件定义]
            user_dict["analysis_num"] = row[8]  # 已经[TAGL要件分析]
            user_dict["hu_plan_num"] = row[9]  # 计划HU
            user_dict["def_plan_num"] = row[10]  # 计划DEF
            user_dict["analysis_plan_num"] = row[11]  # 计划analysis
            if not content or major_category != content[-1].get("major_category"):
                group_list = [user_dict]
                content.append({"major_category": major_category,
                                "group_list": group_list})
            else:
                group_list = content[-1].get("group_list")
                group_list.append(user_dict)
            # self.mysum(sum_data, key_list, row[2:])
        if content:
            # content.append(sum_data)
            result["content"] = content
            result["result"] = "OK"
        return result

    def mysum(self, sum_data, key_list, row):
        for key, num in zip(key_list, row):
            curr_val = sum_data.get(key)
            if num:
                # print num
                if curr_val:
                    sum_data[key] = curr_val + num
                else:
                    sum_data[key] = num
