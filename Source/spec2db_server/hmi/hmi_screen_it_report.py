# -*- coding: UTF-8 -*-
import platform
import os
import time
from Source.spec2db_server.hmi.hmi_base import HMIBase
from openpyxl import Workbook
from openpyxl import load_workbook
from Source.spec2db_server.hmi.hmi_report import HmiReport
HMI_DEV_STATUS_FINISH = u'完成'  # 完成
HMI_DEV_STATUS_QA = u'QA'  # "需要QA"
HMI_DEV_STATUS_UNFINISH = u'未完成'  # 空格
HMI_DEV_STATUS_NO_CASE = u'未测试'
DEV_STATUS_FINISH_LIST = [HMI_DEV_STATUS_FINISH]
DEV_STATUS_UNFINISH_LIST = [HMI_DEV_STATUS_UNFINISH]
DEV_STATUS_QA_LIST = [HMI_DEV_STATUS_QA]
DEV_STATUS_UNDELAY_LIST = DEV_STATUS_FINISH_LIST + DEV_STATUS_QA_LIST
DEV_STATUS_ALL = [HMI_DEV_STATUS_FINISH, HMI_DEV_STATUS_QA, HMI_DEV_STATUS_UNFINISH]
if platform.system() == 'Windows':
    ISSUSE_ROOT = r'Z:\user\maotianyuan\hmi_daily_report'
else:
    ISSUSE_ROOT = r'ftp/user/maotianyuan/hmi_daily_report'


class HmiScreenItReport(HMIBase):
    def __init__(self):
        HMIBase.__init__(self)

    def get_daily_report(self, classify, today):
        new_date = self.get_current_date()
        if today < new_date:
            is_today = False
        elif today == new_date:
            is_today = True
        else:
            return []
        daily_report = None
        try:
            if classify == 'user':
                daily_report = self.get_daily_report_by_user(today, is_today)
            # elif classify == 'category':
            #     daily_report = self.get_daily_report_by_category(today, step, is_today)
        except Exception as e:
            print e
        finally:
            self._pg.close()
        if daily_report:
            return daily_report
        return []

    def get_yesterday_finish(self, pg, today, condition, parms):
        sqlcmd = """
            SELECT a.represent_req
            FROM (
            SELECT *
            FROM hmi.req_history
            WHERE backup_date = %s and 
            dev_status in (
            SELECT dev_status_id
            FROM hmi.dev_status
            where dev_major_category = '完成'
            )
            ) AS A
            LEFT JOIN (
            SELECT hu_id, dev_status
            FROM hmi.req_history
            WHERE backup_date = %s and
            dev_status in (
            SELECT dev_status_id
            FROM hmi.dev_status
            where dev_major_category = '完成'
            )
            ) AS B
            on A.hu_id = B.hu_id
            where (A.dev_status <> B.dev_status or B.dev_status is null)
            {condition}
            ORDER BY a.hu_id
        """.format(condition=condition)
        yesterday = self.get_yesterday(pg, today)
        sum_rep = 0
        sum_not_rep = 0
        if yesterday:
            pg.execute(sqlcmd, (today, yesterday)+tuple(parms))
            rows = pg.fetchall()
            if rows:
                for row in rows:
                    if row[0] == '○':
                        sum_rep += 1
                    else:
                        sum_not_rep += 1
        return sum_rep, sum_not_rep

    def get_yesterday(self, pg, today):
        sqlcmd = """SELECT
                    backup_date
                    from hmi.req_history where
                    backup_date < %s
                    limit 1"""
        pg.execute(sqlcmd, (today,))
        row = pg.fetchone()
        yesterday = None
        if row:
            yesterday = row[0]
        return yesterday

    def get_daily_report_by_user(self, today, is_today):
        condition = ''
        if is_today:
            table_name = 'hmi.hmi_screen_it'
        # else:
        #     table_name = 'hmi.hmi_screen_it'
        #     condition = 'WHERE backup_date = %s'
        sqlcmd = """
        SELECT charger, 
               count(screen_id),
               array_agg(screen_id) screen_id_list,
               array_agg(c1) in_migration_id_list, -- 第一状态
               array_agg(in_migration_date) in_migration_date_list, -- 迁入预定日
               array_agg(c2) followup_migration_id_list, -- 第二状态
               array_agg(followup_migration_date) followup_migration_date_list, -- 迁入后预定日
               array_agg(first_layer) first_layer_list, -- 一层画面
               array_agg(second_layer) second_layer_list, -- 二层画面
               array_agg(third_layer) third_layer_list, -- 三层画面
               array_agg(layer4) layer4_list, -- 四层画面
               array_agg(layer5) layer5_list, -- 五层画面
               array_agg(status) status_list -- 状态
          FROM (
                SELECT t1.screen_id, 
                       (case when charger is null or charger = '' then '未分配'
                        else charger end) charger,
                        in_migration_date, t2.category as c1, t1.in_migration_id, t3.category as c2,
                        t1.followup_migration_id, first_layer, second_layer, third_layer, layer4, layer5,
                        followup_migration_date, t2.status 
                  FROM {table_name} as t1
                  left join hmi.hmi_screen_it_status as t2
                  on t1.in_migration_id = t2.dev_status_id
                  left join hmi.hmi_screen_it_followup_status as t3
                  on t1.followup_migration_id = t3.dev_status_id
                    {condition}
          ) as t1
          --where new_status in (1, 13) -- 完成
          group by charger
          order by charger = '未分配', charger
        """.format(table_name=table_name, condition=condition)
        self._pg.connect()
        if condition:
            self._pg.execute(sqlcmd, (today,))
        else:
            self._pg.execute(sqlcmd,)
        rows = self._pg.fetchall()
        daily_report = []
        sum_data = {"all_num": 0, "all_no_case": 0, "all_finished": 0, "all_unfinished": 0,
                    "all_qa": 0, "all_delay": 0,  "all_num_First": 0, "all_no_case_First": 0,
                    "all_unfinished_First": 0, "all_finished_First": 0, "all_delay_First": 0,
                    "all_qa_First": 0, "all_num_Second": 0,  "all_no_case_Second": 0,
                    "all_finished_Second": 0, "all_unfinished_Second": 0,
                    "all_qa_Second": 0, "all_delay_Second": 0,
                    "all_num_Third": 0, "all_no_case_Third": 0,
                    "all_unfinished_Third": 0, "all_finished_Third": 0, "all_delay_Third": 0,
                    "all_qa_Third": 0, "all_num_layer4": 0, "all_no_case_layer4": 0,
                    "all_unfinished_layer4": 0, "all_finished_layer4": 0, "all_delay_layer4": 0,
                    "all_qa_layer4": 0, "all_num_layer5": 0, "all_no_case_layer5": 0,
                    "all_unfinished_layer5": 0, "all_finished_layer5": 0, "all_delay_layer5": 0,
                    "all_qa_layer5": 0,
                    }
        for row in rows:
            data = dict()
            charger = row[0]  #
            in_migration_id_list = row[3]
            in_migration_date_list = row[4]
            first_layer_list = row[7]
            second_layer_list = row[8]
            third_layer_list = row[9]
            layer4_list = row[10]
            layer5_list = row[11]
            status_list = row[12]
            ####################################################################################################
            # 所有总数
            data["all_num"] = row[1]
            # 所有已完了
            all_finished = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,)
            data["all_finished"] = all_finished
            # 所有未测试
            all_no_case = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                               reserve=False)
            data["all_no_case"] = all_no_case
            # 所有未完了
            all_unfinished = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                               reserve=False)
            data["all_unfinished"] = all_unfinished - all_no_case
            # 所有QA
            all_qa = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST)
            data["all_qa"] = all_qa
            # 所有delay
            all_delay = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                          schedule_list=in_migration_date_list, today=today,
                                          cls='before', reserve=True, include_today=False
                                          )
            data["all_delay"] = all_delay
            ####################################################################################################
            # 画面一
            data["all_num_First"] = self.count_status(in_migration_id_list, [],
                                                      reserve=False,
                                                      represent_req_list=first_layer_list,
                                                      represent_next_list=second_layer_list, represent='First')
            # 所有未测试:画面一
            all_no_case_represent = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                            reserve=False,
                                            represent_req_list=first_layer_list,
                                            represent_next_list=second_layer_list, represent='First')
            data["all_no_case_First"] = all_no_case_represent
            # 所有未完了: 画面一
            all_unfinished_represent = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                                         reserve=False,
                                                         represent_req_list=first_layer_list,
                                                         represent_next_list=second_layer_list, represent='First')
            data["all_unfinished_First"] = all_unfinished_represent - all_no_case_represent
            # 所有已完了: 画面一
            all_finished_represent = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,
                                                       represent_req_list=first_layer_list,
                                                       represent_next_list=second_layer_list, represent='First')
            data["all_finished_First"] = all_finished_represent
            # 所有delay: 画面一
            all_delay_represent = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                                    schedule_list=in_migration_date_list, today=today,
                                                    cls='before', reserve=True,
                                                    represent_req_list=first_layer_list,
                                                    represent_next_list=second_layer_list, represent='First',
                                                    include_today=False)
            data["all_delay_First"] = all_delay_represent
            # 所有QA: 画面一
            all_qa_represent = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST,
                                                 represent_req_list=first_layer_list,
                                                 represent_next_list=second_layer_list, represent='First')
            data["all_qa_First"] = all_qa_represent
            ####################################################################################################
            # 画面二
            data["all_num_Second"] = self.count_status(in_migration_id_list, [],
                                                       reserve=False,
                                                       represent_req_list=second_layer_list,
                                                       represent_next_list=third_layer_list, represent='Second')
            # 所有已完了: 画面二
            all_finished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,
                                                     represent_req_list=second_layer_list,
                                                     represent_next_list=third_layer_list, represent='Second')
            data["all_finished_Second"] = all_finished_not_rep
            # 所有未测试:画面二
            all_no_case_represent = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                                      reserve=False,
                                                      represent_req_list=second_layer_list,
                                                      represent_next_list=third_layer_list, represent='Second')
            data["all_no_case_Second"] = all_no_case_represent
            # 所有未完了: 画面二
            all_unfinished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                                       reserve=False,
                                                       represent_req_list=second_layer_list,
                                                       represent_next_list=third_layer_list, represent='Second')
            data["all_unfinished_Second"] = all_unfinished_not_rep - all_no_case_represent
            # 所有QA: 画面二
            all_qa_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST,
                                               represent_req_list=second_layer_list,
                                               represent_next_list=third_layer_list, represent='Second')
            data["all_qa_Second"] = all_qa_not_rep
            # 所有delay: 画面二
            all_delay_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                                  schedule_list=in_migration_date_list, today=today,
                                                  cls='before', reserve=True,
                                                  represent_req_list=second_layer_list,
                                                  represent_next_list=third_layer_list, represent='Second',
                                                  include_today=False)

            data["all_delay_Second"] = all_delay_not_rep
            ####################################################################################################
            # 画面三
            data["all_num_Third"] = self.count_status(in_migration_id_list, [],
                                                      reserve=False,
                                                      represent_req_list=third_layer_list,
                                                      represent_next_list=layer4_list, represent='Third')

            # 所有已完了: 画面三
            all_finished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,
                                                     represent_req_list=third_layer_list,
                                                     represent_next_list=layer4_list, represent='Third')
            data["all_finished_Third"] = all_finished_not_rep
            # 所有未测试:画面二
            all_no_case_represent = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                                      reserve=False,
                                                      represent_req_list=third_layer_list,
                                                      represent_next_list=layer4_list, represent='Third')
            data["all_no_case_Third"] = all_no_case_represent
            # 所有未完了: 画面三
            all_unfinished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                                       reserve=False,
                                                       represent_req_list=third_layer_list,
                                                       represent_next_list=layer4_list, represent='Third')
            data["all_unfinished_Third"] = all_unfinished_not_rep - all_no_case_represent
            # 所有QA: 画面三
            all_qa_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST,
                                               represent_req_list=third_layer_list,
                                               represent_next_list=layer4_list, represent='Third')
            data["all_qa_Third"] = all_qa_not_rep
            # 所有delay: 画面三
            all_delay_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                                  schedule_list=in_migration_date_list, today=today,
                                                  cls='before', reserve=True,
                                                  represent_req_list=third_layer_list,
                                                  represent_next_list=layer4_list, represent='Third',
                                                  include_today=False)

            data["all_delay_Third"] = all_delay_not_rep
            ####################################################################################################
            # 画面四
            data["all_num_layer4"] = self.count_status(in_migration_id_list, [],
                                                       reserve=False,
                                                       represent_req_list=layer4_list,
                                                       represent_next_list=layer5_list, represent='Four')
            # 所有已完了: 画面四
            all_finished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,
                                                     represent_req_list=layer4_list,
                                                     represent_next_list=layer5_list, represent='Four')
            data["all_finished_layer4"] = all_finished_not_rep
            # 所有未测试:画面四
            all_no_case_represent = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                                      reserve=False,
                                                      represent_req_list=layer4_list,
                                                      represent_next_list=layer5_list, represent='Four')
            data["all_no_case_layer4"] = all_no_case_represent
            # 所有未完了: 画面四
            all_unfinished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                                       reserve=False,
                                                       represent_req_list=layer4_list,
                                                       represent_next_list=layer5_list, represent='Four')
            data["all_unfinished_layer4"] = all_unfinished_not_rep - all_no_case_represent
            # 所有QA: 画面四
            all_qa_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST,
                                               represent_req_list=layer4_list,
                                               represent_next_list=layer5_list, represent='Four')
            data["all_qa_layer4"] = all_qa_not_rep
            # 所有delay: 画面四
            all_delay_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                                  schedule_list=in_migration_date_list, today=today,
                                                  cls='before', reserve=True,
                                                  represent_req_list=layer4_list,
                                                  represent_next_list=layer5_list, represent='Four',
                                                  include_today=False)

            data["all_delay_layer4"] = all_delay_not_rep
            ####################################################################################################
            # 画面五
            data["all_num_layer5"] = self.count_status(in_migration_id_list, [],
                                                       reserve=False,
                                                       represent_req_list=layer5_list, represent='Five')
            # 所有已完了: 画面五
            all_finished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_FINISH_LIST,
                                                     represent_req_list=layer5_list, represent='Five')
            data["all_finished_layer5"] = all_finished_not_rep
            # 所有未测试:画面四
            all_no_case_represent = self.count_status(status_list, HMI_DEV_STATUS_NO_CASE,
                                                      reserve=False,
                                                      represent_req_list=layer5_list, represent='Five')
            data["all_no_case_layer5"] = all_no_case_represent
            # 所有未完了: 画面五
            all_unfinished_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNFINISH_LIST,
                                                       reserve=False,
                                                       represent_req_list=layer5_list, represent='Five')
            data["all_unfinished_layer5"] = all_unfinished_not_rep - all_no_case_represent
            # 所有QA: 画面五
            all_qa_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_QA_LIST,
                                               represent_req_list=layer5_list, represent='Five')
            data["all_qa_layer5"] = all_qa_not_rep
            # 所有delay: 画面五
            all_delay_not_rep = self.count_status(in_migration_id_list, DEV_STATUS_UNDELAY_LIST,
                                                  schedule_list=in_migration_date_list, today=today,
                                                  cls='before', reserve=True,
                                                  represent_req_list=layer5_list, represent='Five',
                                                  include_today=False)

            data["all_delay_layer5"] = all_delay_not_rep
            ####################################################################################################
            self.count_sum(sum_data, data, sum_data.keys())
            if not daily_report or charger != daily_report[-1].get("charger"):
                # user_list = [data]
                daily_report.append({"charger": charger,
                                     "user_list": [data]})
            else:
                user_list = daily_report[-1].get("user_list")
                user_list.append(data)
        sum_data["charger"] = u'总计'
        daily_report.append(sum_data)
        return daily_report

    def count_status(self, status_list, filter_status_list,
                     schedule_list=None, today=None,
                     cls='equal', reserve=False, represent_req_list=None, represent_next_list=None, represent=None,
                     include_today=True):
        """
        :param status_list:  状态
        :param filter_status_list: 过滤条件
        :param schedule_list:
        :param today:
        :param cls:
        :param reserve:
        :param represent_req_list: 当前画面List
        :param represent_next_list: 下个画面List
        :param represent: First--画面一, Second--画面二，Third--画面三 None--所有要件
        :return:
        """
        count = 0
        if not schedule_list:
            schedule_list = [None] * len(status_list)
        if not represent_req_list:
            represent_req_list = [None] * len(status_list)
        if not represent_next_list:
            represent_next_list = [None] * len(status_list)
        for status, schedule, represent_req, represent_next in zip(status_list, schedule_list,
                                                                   represent_req_list, represent_next_list):
            if not status:  # 空认为未完成
                status = HMI_DEV_STATUS_UNFINISH
            if represent == 'First':  # 选择画面一
                if not represent_req:
                    continue
                else:
                    if represent_next:
                        continue
            elif represent == 'Second':  # 选择画面二
                if not represent_req:
                    continue
                else:
                    if represent_next:
                        continue
            elif represent == 'Third':  # 选择画面三
                if not represent_req:
                    continue
                else:
                    if represent_next:
                        continue
            elif represent == 'Four':  # 选择画面四
                if not represent_req:
                    continue
                else:
                    if represent_next:
                        continue
            elif represent == 'Five':  # 选择画面五
                if not represent_req:
                    continue
            else:
                pass
            if(not reserve and (status in filter_status_list or not filter_status_list) or
               (reserve and status not in filter_status_list)):
                if cls == 'equal':  # 当天
                    if schedule == today:
                        count += 1
                elif cls == 'before':  # 当天及之前
                    if include_today:
                        if schedule <= today:
                            count += 1
                    else:
                        if schedule < today:
                            count += 1
                else:
                    count += 1
        return count

    # def get_daily_report_by_category(self, today, step, is_today):
    #     condition = ''
    #     if is_today:
    #         table_name = 'hmi.req'
    #     else:
    #         table_name = 'hmi.req_history'
    #         condition = 'AND backup_date = %s'
    #     sqlcmd = """
    #     SELECT major_category, medium_category, small_category,
    #            array_agg(hu_id) hu_id_list,
    #            array_agg(dev_major_category) dev_major_category_list,
    #            array_agg(apl_schedule) apl_schedule_list, -- APL日程
    #            array_agg(it_schedule) it_schedule_list,     -- 结合日程
    #            array_agg(represent_req) represent_req_list,  -- 代表要件
    #            array_agg(it_progress) it_progress_list      --结合测试进度
    #       FROM (
    #             SELECT major_category, medium_category, small_category,
    #                    t1.hu_id,
    #                    apl_schedule, it_schedule,
    #                    t2.dev_major_category, t1.dev_status,
    #                    it_progress, represent_req
    #               FROM {table_name} as t1
    #               left join hmi.dev_status as t2
    #               on t1.dev_status = t2.dev_status_id
    #               where step = %s {condition}
    #       ) as t1
    #       group by major_category, medium_category, small_category
    #       order by major_category, medium_category, small_category
    #     """.format(table_name=table_name, condition=condition)
    #     self._pg.connect()
    #     if condition:
    #         self._pg.execute(sqlcmd, (step, today))
    #     else:
    #         self._pg.execute(sqlcmd, (step,))
    #     rows = self._pg.fetchall()
    #     daily_report = []
    #     sum_data = {"all_num": 0, "all_exclude": 0, "all_finished": 0, "all_unfinished": 0,
    #                 "all_qa": 0, "all_delay": 0, "all_num_represent": 0, "all_exclude_represent": 0,
    #                 "all_unfinished_represent": 0, "all_finished_represent": 0, "all_delay_represent": 0,
    #                 "all_qa_represent": 0, "all_num_not_rep": 0, "all_exclude_not_rep": 0,
    #                 "all_finished_not_rep": 0, "all_unfinished_not_rep": 0, "it_progress_success": 0,
    #                 "all_qa_not_rep": 0, "all_delay_not_rep": 0,
    #                 "today_plan": 0, "today_plan_reprent": 0, "today_plan_not_rep": 0,
    #                 "yesterday_finished_reprent": 0, "yesterday_finished_not_rep": 0
    #                 }
    #     for row in rows:
    #         data = dict()
    #         major_category = row[0]
    #         medium_category = row[1]
    #         data["small_category"] = row[2]
    #         dev_major_category_list, apl_schedule_list, it_schedule_list, represent_req_list, it_progress_list = row[4:]
    #         ####################################################################################################
    #         # 所有总数
    #         data["all_num"] = len(row[3])
    #         # 对象外
    #         all_exclude = self.count_status(dev_major_category_list, DEV_STATUS_EXCLUDE_LIST)
    #         data["all_exclude"] = all_exclude
    #         # 所有已完了
    #         all_finished = self.count_status(dev_major_category_list, DEV_STATUS_FINISH_LIST,
    #                                          represent_req_list=represent_req_list, represent=None)
    #         data["all_finished"] = all_finished
    #         # 所有未完了
    #         all_unfinished = self.count_status(dev_major_category_list, DEV_STATUS_UNFINISH_LIST,
    #                                            reserve=False,
    #                                            represent_req_list=represent_req_list, represent=None)
    #         data["all_unfinished"] = all_unfinished
    #         # 所有QA
    #         all_qa = self.count_status(dev_major_category_list, DEV_STATUS_QA_LIST)
    #         data["all_qa"] = all_qa
    #         # 所有delay
    #         all_delay_represent = self.count_status(dev_major_category_list, DEV_STATUS_UNDELAY_LIST,
    #                                                 schedule_list=it_schedule_list, today=today,
    #                                                 cls='before', reserve=True,
    #                                                 represent_req_list=represent_req_list, represent='Yes',
    #                                                 include_today=False)
    #         # 非代表Delay
    #         all_delay_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_UNDELAY_LIST,
    #                                               schedule_list=apl_schedule_list, today=today,
    #                                               cls='before', reserve=True,
    #                                               represent_req_list=represent_req_list, represent='No',
    #                                               include_today=False)
    #         data["all_delay"] = all_delay_represent + all_delay_not_rep
    #         ####################################################################################################
    #         # 代表（结合日程）
    #         data["all_num_represent"] = self.count_status(dev_major_category_list, [],
    #                                                       reserve=False,
    #                                                       represent_req_list=represent_req_list, represent='Yes')
    #         # 对象外: 代表
    #         all_exclude_represent = self.count_status(dev_major_category_list, DEV_STATUS_EXCLUDE_LIST,
    #                                                   represent_req_list=represent_req_list, represent='Yes')
    #         data["all_exclude_represent"] = all_exclude_represent
    #         # 所有未完了: 代表
    #         all_unfinished_represent = self.count_status(dev_major_category_list, DEV_STATUS_UNFINISH_LIST,
    #                                                      reserve=False,
    #                                                      represent_req_list=represent_req_list, represent='Yes')
    #         data["all_unfinished_represent"] = all_unfinished_represent
    #         # 所有已完了: 代表
    #         all_finished_represent = self.count_status(dev_major_category_list, DEV_STATUS_FINISH_LIST,
    #                                                    represent_req_list=represent_req_list, represent='Yes')
    #         data["all_finished_represent"] = all_finished_represent
    #         # 所有delay: 代表
    #         all_delay_represent = self.count_status(dev_major_category_list, DEV_STATUS_UNDELAY_LIST,
    #                                                 schedule_list=it_schedule_list, today=today,
    #                                                 cls='before', reserve=True,
    #                                                 represent_req_list=represent_req_list, represent='Yes',
    #                                                 include_today=False)
    #         data["all_delay_represent"] = all_delay_represent
    #         # 所有QA: 代表
    #         all_qa_represent = self.count_status(dev_major_category_list, DEV_STATUS_QA_LIST,
    #                                              represent_req_list=represent_req_list, represent='Yes')
    #         data["all_qa_represent"] = all_qa_represent
    #         ####################################################################################################
    #         # 非代表（APL日程）
    #         data["all_num_not_rep"] = self.count_status(dev_major_category_list, [],
    #                                                     reserve=False,
    #                                                     represent_req_list=represent_req_list, represent='No')
    #         # 对象外: 非代表
    #         all_exclude_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_EXCLUDE_LIST,
    #                                                 represent_req_list=represent_req_list, represent='No')
    #         data["all_exclude_not_rep"] = all_exclude_not_rep
    #         # 所有已完了: 非代表
    #         all_finished_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_FINISH_LIST,
    #                                                  represent_req_list=represent_req_list, represent='No')
    #         data["all_finished_not_rep"] = all_finished_not_rep
    #         # 所有未完了: 非代表
    #         all_unfinished_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_UNFINISH_LIST,
    #                                                    reserve=False,
    #                                                    represent_req_list=represent_req_list, represent='No')
    #         data["all_unfinished_not_rep"] = all_unfinished_not_rep
    #         # 结合测试完成: 非代表
    #         it_progress_success = self.count_status(it_progress_list, DEV_STATUS_FINISH_LIST,
    #                                                 represent_req_list=represent_req_list, represent='No')
    #         data["it_progress_success"] = it_progress_success
    #         # 所有QA: 非代表
    #         all_qa_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_QA_LIST,
    #                                            represent_req_list=represent_req_list, represent='No')
    #         data["all_qa_not_rep"] = all_qa_not_rep
    #         # 所有delay: 非代表
    #         all_delay_not_rep = self.count_status(dev_major_category_list, DEV_STATUS_UNDELAY_LIST,
    #                                               schedule_list=apl_schedule_list, today=today,
    #                                               cls='before', reserve=True,
    #                                               represent_req_list=represent_req_list, represent='No',
    #                                               include_today=False)
    #         data["all_delay_not_rep"] = all_delay_not_rep
    #         ####################################################################################################
    #         # 今日
    #         # 今日计划完成总数: 代表
    #         today_plan_reprent = self.count_status(dev_major_category_list, [],
    #                                                schedule_list=it_schedule_list, today=today,
    #                                                represent_req_list=represent_req_list, represent='Yes')
    #         # 今日计划完成总数: 非代表
    #         today_plan_not_rep = self.count_status(dev_major_category_list, [],
    #                                                schedule_list=apl_schedule_list, today=today,
    #                                                represent_req_list=represent_req_list, represent='No')
    #         data["today_plan"] = today_plan_reprent + today_plan_not_rep  # 今日计划完成总数
    #         # 今日代表要件数
    #         today_plan_reprent = self.count_status(dev_major_category_list, [],
    #                                                schedule_list=it_schedule_list, today=today,
    #                                                represent_req_list=represent_req_list, represent='Yes')
    #         data["today_plan_reprent"] = today_plan_reprent
    #         # 今日非代表要件数
    #         today_plan_not_rep = self.count_status(dev_major_category_list, [],
    #                                                schedule_list=apl_schedule_list, today=today,
    #                                                represent_req_list=represent_req_list, represent='No')
    #         data["today_plan_not_rep"] = today_plan_not_rep
    #         # 昨日代表要件完成件数
    #         condition = "AND major_category = %s AND medium_category = %s AND small_category = %s"
    #         parms = [major_category, medium_category, data["small_category"]]
    #         sum_rep, sum_not_rep = self.get_yesterday_finish(self._pg, today, condition, parms)
    #         data["yesterday_finished_reprent"] = sum_rep
    #         # 昨日非代表要件完成件数
    #         data["yesterday_finished_not_rep"] = sum_not_rep
    #         self.count_sum(sum_data, data, sum_data.keys())
    #         if not daily_report or major_category != daily_report[-1].get("category_name"):
    #             small_list = [data]
    #             medium_list = [{"category_name": medium_category, "sub_list": small_list}]
    #             daily_report.append({"category_name": major_category,
    #                                  "sub_list": medium_list})
    #         else:
    #             medium_list = daily_report[-1].get("sub_list")
    #             if medium_category != medium_list[-1].get("category_name"):
    #                 small_list = [data]
    #                 medium_list.append({"category_name": medium_category, "sub_list": small_list})
    #             else:
    #                 small_list = medium_list[-1].get("sub_list")
    #                 small_list.append(data)
    #     sum_data["category_name"] = u'总计'
    #     daily_report.append(sum_data)
    #     return daily_report

    def count_sum(self, sum_data, curr_data, keys):
        for key in keys:
            sum_val = sum_data.get(key)
            if not sum_val:
                sum_val = 0
            curr_val = curr_data.get(key)
            if not curr_val:
                curr_val = 0
            sum_val = sum_val + curr_val
            sum_data[key] = sum_val

    def export_report(self, today, template_name, file_url):
        self._pg.connect()
        wb = load_workbook(template_name)
        ws = wb.get_sheet_by_name('Sheet')
        sum_data = ["all_num", "all_finished", "all_no_case", "all_unfinished",
                    "all_qa", "all_delay",  "all_num_First",
                    "all_finished_First", "all_no_case_First", "all_unfinished_First", "all_qa_First",
                    "all_delay_First", "all_num_Second",
                    "all_finished_Second", "all_no_case_Second", "all_unfinished_Second",
                    "all_qa_Second", "all_delay_Second",
                    "all_num_Third",
                    "all_finished_Third", "all_no_case_Third", "all_unfinished_Third", "all_qa_Third",
                    "all_delay_Third", "all_num_layer4", "all_finished_layer4", "all_no_case_layer4",
                    "all_unfinished_layer4", "all_qa_layer4", "all_delay_layer4",
                    "all_num_layer5", "all_finished_layer5", "all_no_case_layer5",
                    "all_unfinished_layer5", "all_qa_layer5", "all_delay_layer5",

                    ]
        report_data = self.get_daily_report('user', today)
        row_i = 3
        for report in report_data:
            user_row = []
            charger = report.get('charger')
            user_list = report.get('user_list')
            if not user_list:
                continue
            user_row.append(charger)
            for user in user_list:
                user_row += self.get_params(user, sum_data)
                ws.append(user_row)
            row_i = row_i+len(user_list)
        info_data = report_data[-1]
        row = ['总计', info_data['all_num'], info_data['all_finished'], info_data['all_no_case'],
               info_data['all_unfinished'], info_data['all_qa'], info_data['all_delay'], info_data['all_num_First'],
               info_data['all_finished_First'], info_data['all_no_case_First'], info_data['all_unfinished_First'],
               info_data['all_qa_First'], info_data['all_delay_First'], info_data['all_num_Second'],
               info_data['all_finished_Second'], info_data['all_no_case_Second'], info_data['all_unfinished_Second'],
               info_data['all_qa_Second'],
               info_data['all_delay_Second'],
               info_data['all_num_Third'], info_data['all_finished_Third'], info_data['all_no_case_Third'],
               info_data['all_unfinished_Third'], info_data['all_qa_Third'],
               info_data['all_delay_Third'],
               info_data['all_num_layer4'], info_data['all_finished_layer4'], info_data['all_no_case_layer4'],
               info_data['all_unfinished_layer4'], info_data['all_qa_layer4'],
               info_data['all_delay_layer4'],
               info_data['all_num_layer5'], info_data['all_finished_layer5'], info_data['all_no_case_layer5'],
               info_data['all_unfinished_layer5'], info_data['all_qa_layer5'],
               info_data['all_delay_layer5']
               ]
        ws.append(row)
        self._pg.close()
        wb.save(file_url)

    def get_steps(self):
        sqlcmd = """
        SELECT distinct step
          FROM hmi.req
          order by step
        """
        steps = []
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        for row in rows:
            steps.append(row[0])
        self._pg.close()
        return steps

    def issue_report(self):
        template_name = r'./template/report_template.xlsx'
        obj = HmiReport()
        date = obj.get_current_date()
        issue_path = os.path.join('issue', 'hmi')
        if os.path.exists(issue_path):
            try:
                # 清空
                cmd = 'rm -rf %s' % issue_path
                os.system(cmd)
                os.makedirs(issue_path)
            except Exception as e:
                print e
                return None
        else:
            os.makedirs(issue_path)
        for step in self.get_steps():
            file_name = 'TAGL_HMI_DailyReport_%s_%s.xlsx' % (step, date)
            file_url = os.path.join(issue_path, file_name)
            obj.export_report(date, step, template_name, file_url)
        # 导出昨日完成要件明细
        from Source.spec2db_server.hmi.req_export import ReqExport
        export = ReqExport()
        export.do_export_daily_finished_detail('./template/HMI_Detail_template_v005.xlsx', issue_path, date)
        self.copy_release_2_ftp(issue_path, date)

    def copy_release_2_ftp(self, release_path, rls_date):
        # rls_date = self.conver_date_format(rls_date)
        if platform.system() == 'Windows':
            dest = ISSUSE_ROOT
        else:
            dest = os.path.join(os.path.expanduser('~'), ISSUSE_ROOT)
        if not os.path.isdir(dest):
            os.mkdir(dest)
        file_name = self.get_release_dest_file(rls_date, dest)
        dest = os.path.join(dest, file_name)
        cmd = 'cp -rf {src} {dest}'.format(src=release_path, dest=dest)
        print cmd
        print 'Copy Result to %s' % dest
        if not os.system(cmd):
            return True
        return False

    def get_release_dest_file(self, release_path, dest):
        base_name = os.path.basename(release_path)
        file_name, ext_name = os.path.splitext(base_name)
        i = 1
        while True:
            if not os.path.exists(os.path.join(dest, base_name)):
                break
            else:
                base_name = '_'.join([file_name, str(i)])
                if ext_name:
                    base_name = '.'.join([base_name, ext_name])
            i += 1
        return base_name


def main():
    obj = HmiScreenItReport()
    # obj.issue_report()
    # obj.get_daily_report('user', '2018-03-06', 'SP30')
    # obj.get_daily_report('category', '2018-03-06', 'SP30')
    # result = obj.get_daily_report_by_user(today='2018-03-07', is_today=True)
    # result = obj.get_daily_report_by_category(today='2018-03-01', step='SP30')
    # print result
    template_name = './template/screen_report_template.xlsx'
    file_url = './test.xlsx'
    obj.export_report(today='2018-03-12', template_name=template_name, file_url=file_url)


if __name__ == '__main__':
    import sys, os
    os.chdir('../')
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
