# -*- coding: UTF-8 -*-
"""
Created on 2017-12-13

@author: hcz
"""
import time
import os
import platform
import shutil
import zipfile
from openpyxl import Workbook
from Source.spec2db_server.arl.arl_base import ServiceBase, JOB_STATUS_ASSURED
from Source.spec2db_server.arl.commit_log import COMMIT_ACTION
from Source.spec2db_server.arl.arl_srv_status import ArlSrvStatus
from Source.spec2db_server.arl.arl_func import ArlFunc
from Source.spec2db_server.astafile_server.astafile_service import AstaFileRecord
LOCAL_RELEASE_ROOT = r'local_release'
if platform.system() == 'Windows':
    RELEASE_ROOT_DIR = r'C:\proj\Release'
else:
    RELEASE_ROOT_DIR = os.path.join(os.path.expanduser('~'), 'Release')
FTP_BOOT = r"\\192.168.0.3\ftpboot"
HU_TEMPLATE = os.path.join('./template', 'HU_RequirementDefinition.Ver0.17_haspoint_template.xlsx')
DEF_TEMPLATE = os.path.join('./template', 'TAGL_RequirementDefinitionVer0.12_haspoint_template.xlsx')
ANA_TEMPLATE = os.path.join('./template', 'TAGL_RequirementAnalysis.ver1.00_haspoint_template.xlsx')
SPIDER_HOST = r'192.168.0.56'
SCP_HOST = r'pset@192.168.0.56:/home/pset/Spec2DB/Source/spec2db_server/astafile'


class ArlRelease(ServiceBase):
    def __init__(self):
        ServiceBase.__init__(self)
        self.table_name = "release_info"
        self.key_col = "release_id"
        self.id_col = "rls_version"
        self.attr_list = ["release_id", "rls_version", "rls_date",
                          "rls_time", "pre_version", "user_id", "path",
                          "commit_log_info_id"
                          ]

    def start(self, version, rls_date,  pre_rls_date, user_id,
              tmc_issue_url, suntec_confirm_url, blocklist_url):
        print 'Start Release(%s) by User_id: %s' % (version, user_id)
        print 'release_date:%s, prev_release_date:%s' % (rls_date,  pre_rls_date)
        print 'tmc_issue_url:%s' % tmc_issue_url
        print 'suntec_confirm_url: %s' % suntec_confirm_url
        print 'blocklist_url: %s' % blocklist_url
        srv = ArlSrvStatus()
        srv.set_srv_status(status=True)  # 锁
        result, attach_file = '', ''
        try:
            self._pg.connect()
            print self._pg.srv_path
            if self.wait_db_write(self._pg):
                self.collect_post_error(self._pg)
                self.sync_release_table(self._pg)  # 把记录同步到Release表
                arl_list = self.get_not_exist_arl_id(self._pg)
                if arl_list:
                    result = 'HU关联的arl_id(%s)不存在！' % ','.join(arl_list)
                    srv.set_srv_status(status=False)  # 解锁
                    print result
                    self._pg.conn.rollback()
                    self._pg.close()
                    return result, attach_file
                if not self.check_post(self._pg):
                    result = '基本要件转记不一致 ！'
                    srv.set_srv_status(status=False)  # 解锁
                    print result
                    self._pg.conn.rollback()
                    self._pg.close()
                    return result, attach_file
                else:
                    # 写入Release表
                    self._pg.commit()
                # 同步git上的Release
                self.sync_release(RELEASE_ROOT_DIR)
                old_release = self.get_release_path(self.conver_date_format(pre_rls_date))
                if not old_release:
                    result = '不存在Release文件: %s' % os.path.join('Release', self.conver_date_format(pre_rls_date))
                    srv.set_srv_status(status=False)  # 解锁
                    print result
                    self._pg.close()
                    return result, attach_file
                # 清空目录
                self.mk_local_release_path(user_id, root=r'local_release')
                if tmc_issue_url:
                    print 'Copy file... %s' % tmc_issue_url
                    if platform.system() == 'Windows':
                        try:
                            tmc_issue_url = tmc_issue_url.encode('gbk')
                        except:
                            pass
                    tmc_root_dir = self.mk_local_release_path(user_id, rls_date, suffix='tmc',
                                                              root=LOCAL_RELEASE_ROOT)
                    tmc_dir = self.download_file(tmc_issue_url, tmc_root_dir)
                    if not tmc_dir:
                        srv.set_srv_status(status=False)  # 解锁
                        result = 'copy %s 失败！' % tmc_issue_url
                        return result, attach_file
                else:
                    tmc_dir = ''
                # ## SUNTEC CONFIRM
                print 'Copy file... %s' % suntec_confirm_url
                if platform.system() == 'Windows':
                    try:
                        suntec_confirm_url = suntec_confirm_url.encode('gbk')
                    except:
                        pass
                suntec_root_dir = self.mk_local_release_path(user_id, rls_date, suffix='suntec',
                                                             root=LOCAL_RELEASE_ROOT)
                suntec_dir = self.download_file(suntec_confirm_url, suntec_root_dir)
                if not suntec_dir:
                    srv.set_srv_status(status=False)  # 解锁
                    result = 'copy %s 失败！' % suntec_confirm_url
                    self._pg.close()
                    return result, attach_file
                # ## BLOCK LIST
                print 'Copy file... %s' % blocklist_url
                if platform.system() == 'Windows':
                    try:
                        blocklist_url = blocklist_url.encode('gbk')
                    except:
                        pass
                block_root_dir = self.mk_local_release_path(user_id, rls_date, suffix='block',
                                                            root=LOCAL_RELEASE_ROOT)
                block_dir = self.download_file(blocklist_url, block_root_dir)
                if not block_dir:
                    srv.set_srv_status(status=False)  # 解锁
                    result = 'copy %s 失败！' % block_root_dir
                    self._pg.close()
                    return result, attach_file
                rls_time = self.get_current_time()
                release_id = self._insert_release_info(self._pg, version, rls_date,
                                                       pre_rls_date, user_id, rls_time)
                if release_id:
                    last_log_info_id = self.get_last_log_info_id(self._pg, pre_rls_date)
                    # self._update_new_date(self._pg, last_log_info_id, rls_date)  # 更新日付时间
                    # 数据库导到excel
                    rls_path = self.mk_local_release_path(user_id, rls_date, root=LOCAL_RELEASE_ROOT)
                    if not self.write_unsync_2_release_record(self._pg, rls_path):
                        srv.set_srv_status(status=False)  # 解锁
                        result = '记录同步到Release有误！'
                        self._pg.close()
                        return result, attach_file
                    self._db_2_excel(rls_path, version, rls_time)
                    self.copy_release_2_ftp(rls_path, rls_date)
                    # Set Last Log Info ID
                    self.set_last_log_info_id(self._pg, release_id)
                    self._pg.commit()
                    style_out_dir = self.mk_local_release_path(user_id, rls_date, suffix='style')
                    print '下载Astah文件...'
                    if not self.astah_file(style_out_dir):
                        result = 'Astah下载失败！'
                        srv.set_srv_status(status=False)  # 解锁
                        self._pg.close()
                        return result, attach_file
                    srv.set_srv_status(status=False)  # 解锁
                    # 切割文件, 合并指摘，刷新Excel Style
                    result, attach_file = self.lgat(user_id, rls_path, rls_date, pre_rls_date,
                                                    tmc_dir, suntec_dir, block_dir, style_out_dir)
                    if result == 'OK':
                        self._pg.commit()
                    else:
                        self._pg.conn.rollback()
            else:
                result = "TimeOut"
        except Exception as e:
            print e
            result = str(e)
            srv.set_srv_status(status=False)  # 解锁
            if self._pg.connected:
                self._pg.conn.rollback()
        finally:
            self._pg.close()
        print 'Release Finished!'
        return result, attach_file

    def download_file(self, url, dist_dir):
        if platform.system() == 'Windows':
            url = url.replace(FTP_BOOT, r'Z:')
        else:
            url = url.replace(FTP_BOOT, '')
            url = os.path.join(r'~/ftp', url[1:])
            url = url.replace('\\', os.sep)
        cmd = 'cp -rf {src} {dest}'.format(src=url, dest=dist_dir)
        print cmd
        e = os.system(cmd)
        if not e:
            astah_name = os.path.basename(url)
            if not astah_name:
                astah_name = os.path.basename(url[:-1])
            try:
                astah_name = astah_name.decode("utf8")
            except:
                astah_name = astah_name.decode("gbk")

            tmc_dir = os.path.join(dist_dir, astah_name)
            return tmc_dir
        return None

    def _db_2_excel(self, rls_path, version, rls_time):
        print 'Export HU/DEF/ANA to excel.'
        # ## 导到excel
        func_obj = ArlFunc()
        # HU
        hu_file_name = self.get_file_name("HU_DEF", version, rls_time)
        hu_template = os.path.join('./template', 'HU_RequirementDefinition.Ver0.17_template.xlsx')
        func_obj.export_for_release(self._pg, "HU_DEF", rls_path, hu_file_name, hu_template)
        # DEF
        def_file_name = self.get_file_name("TAGL_DEF", version, rls_time)
        def_template = os.path.join('./template', 'TAGL_RequirementDefinitionVer0.12_template.xlsx')
        func_obj.export_for_release(self._pg, "TAGL_DEF", rls_path, def_file_name, def_template)
        # Analysis
        ana_file_name = self.get_file_name("TAGL_ANA", version, rls_time)
        ana_template = os.path.join('./template', 'TAGL_RequirementAnalysis.ver1.00_template.xlsx')
        func_obj.export_for_release(self._pg, "TAGL_ANA", rls_path, ana_file_name, ana_template)
    
    def _insert_release_info(self, pg, version, rls_date, pre_version, user_name, rls_time, path=''):
        sqlcmd = self.list_2_insert_sql(self.table_name, self.attr_list[1:-1], self.key_col)
        pg.execute(sqlcmd, (version, rls_date, rls_time, pre_version, user_name, path))
        release_id = self.fetch_id()
        return release_id

    def wait_db_write(self, pg):
        print '等待数据库服务器空闲...'
        count = 0
        while count < 15:
            if not self.check_table_status(pg):
                return True
            else:
                time.sleep(60)  # 60 second
            count += 1
        return False

    def sync_release_table(self, pg):
        print '同步Release表'
        sqlcmd = """
        ------------------------------------------------------------------------------
        -- hu, 11.7 secs 
        DELETE FROM release.hu_model_rel
          WHERE hu_record_id IN (
            SELECT r.hu_record_id
              FROM release.hu as r
              left join spec.hu as s
              on r.hu_id = s.hu_id 
              WHERE s.job_status = 3
          );
          
        DELETE FROM release.hu
          WHERE hu_id IN (
            SELECT hu_id
              from spec.hu as s
              WHERE s.job_status = 3
          );
        
        insert into release.hu
        (
           SELECT *
            FROM spec.hu
            where job_status = 3
        );
        
        insert into release.hu_model_rel
        (
           SELECT m.*
             FROM spec.hu_model_rel as m
             left join spec.hu as s
             on m.hu_record_id = s.hu_record_id
             where s.job_status = 3
        );
        
        ------------------------------------------------------------------------------
        -- definition, 8.7 secs
        DELETE FROM release.definition_model_rel
          WHERE def_rc_id IN (
            SELECT r.def_rc_id
              FROM release.definition as r
              left join spec.definition as s
              on r.definition_id = s.definition_id 
              WHERE s.job_status = 3
          );
          
        DELETE FROM release.definition
          WHERE definition_id IN (
            SELECT definition_id
              from spec.definition as s
              WHERE s.job_status = 3
          );
        
        insert into release.definition
        (
           SELECT *
            FROM spec.definition
            where job_status = 3
        );
        
        insert into release.definition_model_rel
        (
           SELECT m.*
             FROM spec.definition_model_rel as m
             left join spec.definition as s
             on m.def_rc_id = s.def_rc_id
             where s.job_status = 3
        );
        
        -----------------------------------------------------
        -- analysis, 11.7 secs
        DELETE FROM release.analysis_model_rel
          WHERE analysis_rc_id IN (
            SELECT r.analysis_rc_id
              FROM release.analysis as r
              left join spec.analysis as s
              on r.analysis_id = s.analysis_id 
              WHERE s.job_status = 3
          );
          
        DELETE FROM release.analysis
          WHERE analysis_id IN (
            SELECT analysis_id
              from spec.analysis as s
              WHERE s.job_status = 3
          );
        
        insert into release.analysis
        (
           SELECT *
            FROM spec.analysis
            where job_status = 3
        );
        
        insert into release.analysis_model_rel
        (SELECT m.*
             FROM spec.analysis_model_rel as m
             left join spec.analysis as s
             on m.analysis_rc_id = s.analysis_rc_id
             where s.job_status = 3
        );
        
        ------------------------------------------------------------------------------
        -- Basic hu, 11.7 secs 
        DELETE FROM release.basic_req_hu_model_rel
          WHERE hu_record_id IN (
            SELECT r.hu_record_id
              FROM release.basic_req_hu as r
              left join spec.basic_req_hu as s
              on r.hu_id = s.hu_id 
              WHERE s.job_status = 3 and s.hu_id not in (
                select hu_id
                  from spec.post_error_hu
              )
          );
          
        DELETE FROM release.basic_req_hu
          WHERE hu_id IN (
            SELECT hu_id
              from spec.basic_req_hu as s
              WHERE s.job_status = 3 and s.hu_id not in (
                select hu_id
                  from spec.post_error_hu
              )
          );
        
        insert into release.basic_req_hu
        (
           SELECT *
            FROM spec.basic_req_hu as s
            where job_status = 3 and s.hu_id not in (
                select hu_id
                  from spec.post_error_hu
              )
        );
        
        insert into release.basic_req_hu_model_rel
        (
           SELECT m.*
             FROM spec.basic_req_hu_model_rel as m
             left join spec.basic_req_hu as s
             on m.hu_record_id = s.hu_record_id
             where s.job_status = 3 and s.hu_id not in (
                select hu_id
                  from spec.post_error_hu
              )
        );
        
        ------------------------------------------------------------------------------
        -- Basic definition, 8.7 secs
        DELETE FROM release.basic_req_definition_model_rel
          WHERE def_rc_id IN (
            SELECT r.def_rc_id
              FROM release.basic_req_definition as r
              left join spec.basic_req_definition as s
              on r.definition_id = s.definition_id 
              WHERE s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
          );
          
        DELETE FROM release.basic_req_definition
          WHERE definition_id IN (
            SELECT definition_id
              from spec.basic_req_definition as s
              WHERE s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
          );
        
        insert into release.basic_req_definition
        (
           SELECT *
            FROM spec.basic_req_definition as s
            where job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
        );
        
        insert into release.basic_req_definition_model_rel
        (
           SELECT m.*
             FROM spec.basic_req_definition_model_rel as m
             left join spec.basic_req_definition as s
             on m.def_rc_id = s.def_rc_id
             where s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
        );
        
        -----------------------------------------------------
        -- analysis, 11.7 secs
        
        DELETE FROM release.basic_req_analysis_model_rel
          WHERE analysis_rc_id IN (
            SELECT r.analysis_rc_id
              FROM release.basic_req_analysis as r
              left join spec.basic_req_analysis as s
              on r.analysis_id = s.analysis_id 
              WHERE s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
          );
          
        DELETE FROM release.basic_req_analysis
          WHERE analysis_id IN (
            SELECT analysis_id
              from spec.basic_req_analysis as s
              WHERE s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
          );
        
        insert into release.basic_req_analysis
        (
           SELECT *
            FROM spec.basic_req_analysis as s
            where job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
        );
        
        insert into release.basic_req_analysis_model_rel
        (
           SELECT m.*
             FROM spec.basic_req_analysis_model_rel as m
             left join spec.basic_req_analysis as s
             on m.analysis_rc_id = s.analysis_rc_id
             where s.job_status = 3 and s.definition_id not in (
                select definition_id
                  from spec.post_error_def
              )
        );
        """
        pg.execute(sqlcmd)

    def write_unsync_2_release_record(self, pg, path):
        wb = Workbook()
        ws = wb.active
        result, data_list = self.get_unsync_2_release_record(pg)
        tiles = (u"类别", u"当前库ID", u"当前库状态", u"Release库ID",  u"Release库状态", u"未同步理由")
        data_list.insert(0, tiles)
        for i, row in enumerate(data_list, 1):
            ws.append(row)
        wb.save(os.path.join(path, "unsync_record.xlsx"))
        return result

    def get_unsync_2_release_record(self, pg):
        """取得未同步到Release的记录"""
        sqlcmd = """
        SELECT classify, id, release_id, job_status, release_status, other_id
        FROM (
        ---------------------------------------------------------
        -- HU
        SELECT 'HU' classify, t1.hu_id as id, t2.hu_id as release_id, 
                t1.job_status, t2.job_status as release_status, t3.hu_id as other_id
          FROM spec.hu as t1
          full JOiN release.hu as t2
          on t1.hu_id = t2.hu_id
          LEFT JOIN spec.post_error_hu as t3
          ON t1.hu_id = t3.hu_id
          
        union
        
        SELECT 'HU' classify, t1.hu_id, t2.hu_id,
               t1.job_status, t2.job_status, t3.hu_id
          FROM spec.basic_req_hu as t1
          full JOiN release.basic_req_hu as t2
          on t1.hu_id = t2.hu_id
          LEFT JOIN spec.post_error_hu as t3
          ON t1.hu_id = t3.hu_id
        union
        ---------------------------------------------------------
        -- DEF
        SELECT 'DEF' classify, t1.definition_id, t2.definition_id,
               t1.job_status, t2.job_status, t3.definition_id
          FROM spec.definition as t1
          full JOiN release.definition as t2
          on t1.definition_id = t2.definition_id
          LEFT JOIN spec.post_error_def as t3
          ON t1.definition_id = t3.definition_id
          
        union
        
        SELECT 'DEF' classify, t1.definition_id, t2.definition_id,
               t1.job_status, t2.job_status, t3.definition_id
          FROM spec.basic_req_definition as t1
          full JOiN release.basic_req_definition as t2
          on t1.definition_id = t2.definition_id
          LEFT JOIN spec.post_error_def as t3
          ON t1.definition_id = t3.definition_id
        
        union
        ---------------------------------------------------------
        -- ANA
        SELECT 'ANA' classify, t1.definition_id, t2.definition_id,
               t1.job_status, t2.job_status, t3.definition_id
          FROM spec.analysis as t1
          full JOiN release.analysis as t2
          on t1.definition_id = t2.definition_id
          LEFT JOIN spec.post_error_def as t3
          ON t1.definition_id = t3.definition_id
        
        union
        
        SELECT 'ANA' classify, t1.definition_id, t2.definition_id,
              t1.job_status, t2.job_status, t3.definition_id
          FROM spec.basic_req_analysis as t1
          full JOiN release.basic_req_analysis as t2
          on t1.definition_id = t2.definition_id
          LEFT JOIN spec.post_error_def as t3
          ON t1.definition_id = t3.definition_id
        ) AS a
        order by classify DESC, length(id), id; 
        """
        JOB_STATUS = {1: "初始状态",
                      2: "待确认",
                      3: "确认完了",
                      }
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        data_list = []
        result = True
        for row in rows:
            classify, _id, release_id, job_status, release_status, other_id = row
            if not _id:
                reason = u'删除漏同步！'
                result = False
            else:
                if job_status != JOB_STATUS_ASSURED:
                    reason = u'未确认!'
                elif other_id:
                    reason = u'关联要件(父/子)未确认'
                else:
                    reason = u'正常'
            data_list.append((classify, _id, JOB_STATUS.get(job_status),
                              release_id, JOB_STATUS.get(release_status), reason))
        return result, data_list

    def check_table_status(self, pg):
        """检查表的读写状态是否完成
        :return:
        """
        table_list = ["arl",
                      "hu",
                      "definition",
                      "analysis",
                      "basic_req_hu",
                      "basic_req_definition",
                      "basic_req_analysis",
                      "hu_model_rel",
                      "definition_model_rel",
                      "analysis_model_rel",
                      "basic_req_hu_model_rel",
                      "basic_req_definition_model_rel",
                      "basic_req_analysis_model_rel",
                      "point_out",
                      "commit_log",
                      "commit_log_info",
                      "commit_log_ref",
                      "arl_file"
                      ]
        sqlcmd = """
        select relname
               --, , datname as db_name, mode
          from pg_locks as pl
          left join pg_class as pc
          on pl.relation = pc.oid
          left join pg_database as pdb
          on pl.database = pdb.oid
          where datname = %s and "mode" ilike '%%Exclusive%%'
        """
        db_name = pg.get_curr_db()
        if not db_name:
            return False
        exclusive_flag = False
        pg.execute(sqlcmd, (db_name,))
        rows = pg.fetchall()
        for row in rows:
            relname = row[0]
            if relname in table_list:
                exclusive_flag = True
                break
        return exclusive_flag

    def _update_new_date(self, pg, last_log_info_id, rls_date):
        """更新日付时间：如果变更还未反映到上一版里，那么日付时间设成当前日期
        :return:
        """
        if not last_log_info_id:
            return
        table_list = [("hu", "hu_record_id"),
                      ("definition", "def_rc_id"),
                      ("analysis", "analysis_rc_id"),
                      ("basic_req_hu", "hu_record_id"),
                      ("basic_req_definition", "def_rc_id"),
                      ("basic_req_analysis", "analysis_rc_id"),
                      ]
        action_condition = ','.join([str(COMMIT_ACTION.get("add")), str(COMMIT_ACTION.get("change"))])
        for table_name, key_col in table_list:
            sqlcmd = """
            UPDATE spec.{table_name} as t1 set new_date = %s
              from (
                SELECT record_id, reason
                  FROM spec.commit_log_info
                  where commit_log_info_id > %s
                        and action_type in ({action_condition})
                        and table_name = %s
              ) as t2
              where t1.{key_col} = t2.record_id and t1.new_date < %s;
            """.format(table_name=table_name, action_condition=action_condition, key_col=key_col)
            pg.execute(sqlcmd, [rls_date, last_log_info_id, table_name, rls_date])

    def get_last_log_info_id(self, pg, rls_version):
        data = self.get_by_id(pg, rls_version, self.attr_list)
        if data:
            return data.get("commit_log_info_id")
        return None

    def set_last_log_info_id(self, pg, release_id):
        sqlcmd = """
        UPDATE spec.release_info SET commit_log_info_id = (SELECT max(commit_log_info_id) FROM spec.commit_log_info)
        WHERE release_id = %s;
        """
        pg.execute(sqlcmd, (release_id,))

    def get_by_date(self, pg, rls_date, col_list):
        sqlcmd = self.list_2_select_sql(self.table_name, col_list, ["rls_date"])
        sqlcmd += """ order by release_id desc limit 1 """
        pg.execute(sqlcmd, [rls_date])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
        return attr_dict

    def get_by_id(self, pg, _id, col_list):
        sqlcmd = self.list_2_select_sql(self.table_name, col_list, [self.id_col])
        pg.execute(sqlcmd, [_id])
        row = pg.fetchone()
        attr_dict = dict()
        if row:
            i = 0
            while i < len(col_list):
                attr_dict[col_list[i]] = row[i]
                i += 1
        return attr_dict

    def get_file_name(self, export_type, version, update_time):
        update_time = time.strptime(update_time, "%Y-%m-%d %H:%M:%S")
        update_time = time.strftime('%Y-%m-%d_%H-%M-%S', update_time)
        if export_type == 'HU_DEF':
            export_file_name = "HU_RequirementDefinition.Ver%s_%s.xlsx" % (version, update_time)
        elif export_type == 'TAGL_DEF':
            export_file_name = "TAGL_RequirementDefinition.Ver%s_%s.xlsx" % (version, update_time)
        else:
            export_file_name = "TAGL_RequirementAnalysis.Ver%s_%s.xlsx" % (version, update_time)
        return export_file_name

    def mk_local_release_path(self, user_id, rls_date='', suffix='', root=r'local_release'):
        """Release:内部临时文件"""
        if not rls_date:
            path = os.path.join(root, str(user_id))
        else:
            if not suffix:
                path = os.path.join(root, str(user_id), rls_date)
            else:
                path = os.path.join(root, str(user_id), '-'.join([rls_date, suffix]))
        if os.path.exists(path):
            try:
                # 清空
                # shutil.rmtree(path)
                cmd = 'rm -rf %s' % path
                os.system(cmd)
                os.makedirs(path)
            except Exception as e:
                print e
                return None
        else:
            os.makedirs(path)
        return path

    def get_release_path(self, rls_date, create=False):
        path = os.path.join(RELEASE_ROOT_DIR, rls_date)
        if not create:
            if os.path.exists(path):
                return path
            else:
                return None
        else:
            if os.path.exists(path):
                try:
                    # 清空
                    shutil.rmtree(path)
                    os.makedirs(path)
                except Exception as e:
                    print e
                    return None
            else:
                os.makedirs(path)
            return path

    def get_releases_date(self):
        sqlcmd = """
        SELECT distinct rls_date
          FROM spec.release_info
          ORDER BY rls_date DESC
        """
        ver_list = []
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        for row in rows:
            ver_list.append(row[0])
        return ver_list

    def get_releases(self):
        sqlcmd = """
        SELECT rls_version
          FROM spec.release_info
          ORDER BY rls_version DESC
        """
        ver_list = []
        self._pg.connect()
        self._pg.execute(sqlcmd)
        rows = self._pg.fetchall()
        for row in rows:
            ver_list.append(row[0])
        return ver_list

    def lgat(self, user_id, input_dir, rls_date, pre_rls_date,
             tmc_issue_dir, suntec_confirm_dir, blocklist_dir, style_out_dir):
        print input_dir
        attach_file = ''
        cut_output_dir = self.mk_local_release_path(user_id, rls_date, suffix='cut')
        # ## 切割文件
        if not self.lgat_cut_files(input_dir, cut_output_dir):
            attach_file = self.zip_file([input_dir, cut_output_dir], cut_output_dir, 'check.zip')
            print '切割文件出错！'
            return '切割文件出错！', attach_file
        else:
            # 删除多余的文件
            del_list = [u"HU要件定義書.xlsx", u"TAGL要件定義.xlsx", u"TAGL要件分析.xlsx"]
            for _file in del_list:
                path = os.path.join(cut_output_dir, _file)
                os.remove(path)
        merger_output_dir = self.mk_local_release_path(user_id, rls_date, suffix='merger')
        if not merger_output_dir:
            error = '创建文件失败: %s' % os.path.join(RELEASE_ROOT_DIR, rls_date)
            print error
            return error, attach_file
        rls_date = self.conver_date_format(rls_date)
        pre_rls_date = self.conver_date_format(pre_rls_date)
        old_release = self.get_release_path(pre_rls_date)
        if not old_release:
            error = '不存在Release文件: %s' % os.path.join(RELEASE_ROOT_DIR, pre_rls_date)
            print error
            return error, attach_file
        new_release = cut_output_dir
        # ## 合并指摘
        print 'blocklist_dir:', blocklist_dir
        if self.merger_point_out(old_release, new_release,
                                 tmc_issue_dir, suntec_confirm_dir,
                                 merger_output_dir, blocklist_dir):
            pass
        else:
            zip_file = '%s_merger.zip' % rls_date
            attach_file = self.zip_file([input_dir, cut_output_dir, merger_output_dir], merger_output_dir, zip_file)
            print '合并指摘出错!'
            return '合并指摘出错!', attach_file
        # ## 刷新格式
        merger_output_dir = os.path.join(merger_output_dir, 'release')
        self.update_excel_style(merger_output_dir, style_out_dir)
        # ## diff脚本
        # self.release_diff(old_release, release_output_dir)
        # # ## astah 下载
        # astah_obj = AstaFileRecord()
        # astah_dir = astah_obj.get_file_to_git()
        # if astah_dir:
        #     astah_name = os.path.basename(astah_dir)
        #     # ana_dir = os.path.join(style_out_dir, u'全体要件', u'03.TAGL要件分析書')
        #     astah_path = os.path.join(style_out_dir, astah_name)
        #     if os.path.exists(astah_path):
        #         shutil.rmtree(astah_path)
        #     shutil.move(astah_dir, style_out_dir)
        # else:
        #     error = 'Astah下载失败！'
        #     return error, attach_file
        # ## 打包上传Release
        zip_file = '%s.zip' % rls_date
        release_dir = os.path.join(LOCAL_RELEASE_ROOT, str(user_id))
        attach_file = self.zip_file([style_out_dir], release_dir, zip_file)
        print 'attach_file: %s' % attach_file
        return 'OK', attach_file

    def astah_file(self, output_dir):
        if platform.system() == 'Windows' or not check_local_ip(SPIDER_HOST):
            try:
                cmd = "scp -r {SCP_HOST} ./".format(SCP_HOST=SCP_HOST)
                print cmd
                if os.system(cmd):
                    return False
            except:
                return False
        # ## astah 下载
        astah_obj = AstaFileRecord()
        astah_dir = astah_obj.get_file_to_git()
        if astah_dir:
            astah_name = os.path.basename(astah_dir)
            # ana_dir = os.path.join(style_out_dir, u'全体要件', u'03.TAGL要件分析書')
            astah_path = os.path.join(output_dir, astah_name)
            if os.path.exists(astah_path):
                shutil.rmtree(astah_path)
            shutil.move(astah_dir, output_dir)
        else:
            return False
        return True

    def zip_file(self, in_dir_list, out_dir, zip_name='zipfile'):
        try:
            import zlib
            compression = zipfile.ZIPZIP_DEFLATED
        except:
            compression = zipfile.ZIP_STORED
        path = os.path.join(out_dir, zip_name)
        if os.path.exists(path):
            os.remove(path)

        z = zipfile.ZipFile(zip_name, mode="w", compression=compression)
        try:
            for in_dir in in_dir_list:
                start = len(in_dir)
                for dirpath, dirs, files in os.walk(in_dir):
                    for file in files:
                        # if file.split('.')[-1] != "xls":
                        #     continue
                        z_path = os.path.join(dirpath, file)
                        z.write(z_path, z_path[start:])
            z.close()
            shutil.move(zip_name, out_dir)
            return path
        except Exception as e:
            print e
            if z:
                z.close()
        return None

    def get_tmc_issue(self, rls_date):
        return r'C:\doc\13_TMC指摘\20171219'

    def get_suntec_comfirm(self, rls_date):
        return r'C:\doc\18.指摘确认会\20171215'

    def sync_release(self, release_root_dir):
        cmd = "cd {GIT_DIR} && git pull".format(GIT_DIR=release_root_dir)
        os.system(cmd)

    def update_excel_style(self, in_dir, out_dir):
        for root, dirs, files in os.walk(in_dir):
            if files:
                for file in files:
                    if file.split('.')[-1] != 'xlsx':
                        continue
                    if platform.system() != 'Windows':
                        try:
                            dest_file_name = file.decode("utf8").encode("utf8")
                        except:
                            dest_file_name = file.decode("gbk").encode("utf8")
                    else:
                        dest_file_name = file
                    dest_file_name = dest_file_name.replace(' ', '\ ')
                    in_file = os.path.join(root, file)
                    in_file = in_file.replace(' ', '\ ')
                    dest_file = os.path.join(out_dir, dest_file_name)
                    style_tool_cmd = '''java -Xms4g -Xmx16g -jar tools/export/jar/UpdateStyle.jar {in_file} {hu_template} {def_template} {ana_template} {out_file}
                     '''.format(in_file=in_file, hu_template=HU_TEMPLATE,
                                def_template=DEF_TEMPLATE, ana_template=ANA_TEMPLATE,
                                out_file=dest_file)
                    print style_tool_cmd
                    os.system(style_tool_cmd)
        return True

    def commit_release(self, release_root_dir):
        pass

    def conver_date_format(self, date):
        date = time.strptime(date, "%Y-%m-%d")
        date = time.strftime('%Y%m%d', date)
        return date

    def lgat_cut_files(self, input_dir, output_dir):
        """切割execle文件
        :param input_dir:
        :param output_dir:
        :return:
        """
        "python lgat_check.py --env combine -id input_directory -od output_directory"
        if platform.system() == 'Windows':
            env_path = self._get_env_path_for_python3()
            check = r"""C:\Python36\python.exe C:\proj\CI_Script\lgat_check\lgat_check.py --env combine -id {input_directory} -od {output_directory}
                   """.format(input_directory=input_dir, output_directory=output_dir)
            cmd = " && ".join([env_path, check])
        else:
            python_path = os.path.join(os.path.expanduser('~'), '/virtualenv/python3/bin/python')
            if not os.path.exists(python_path):
                python_path = '/usr/bin/python3.5'
            cmd = r"""{python_path} ~/CI_Script/lgat_check/lgat_check.py --env combine -id {input_directory} -od {output_directory}
                   """.format(python_path=python_path, input_directory=input_dir, output_directory=output_dir)
        print cmd
        os_ret = os.system(cmd)
        if os_ret != 0:
            return False
        return True

    def merger_point_out(self, old_release, new_release, tmc_issue, suntec_comfirm, output_dir, blocklist_dir):
        if tmc_issue:
            tmc_issue = ' '.join(['-ti', tmc_issue])
        else:
            tmc_issue = ''
        if platform.system() == 'Windows':
            env_path = self._get_env_path_for_python3()
            diff = r"""C:\Python36\python.exe C:\proj\CI_Script\lgat_check\release_with_review.py -or {OLD_RELEASE} -nr {NEW_RELEASE} {TMC_ISSUE} -sc {SUNTEC_CONFIRM} -od {OUTPUT_DIR} -bl {blocklist}
                    """.format(OLD_RELEASE=old_release, NEW_RELEASE=new_release,
                               TMC_ISSUE=tmc_issue, SUNTEC_CONFIRM=suntec_comfirm,
                               OUTPUT_DIR=output_dir, blocklist=blocklist_dir)
            cmd = " && ".join([env_path, diff])
        else:
            python_path = os.path.join(os.path.expanduser('~'), '/virtualenv/python3/bin/python')
            if not os.path.exists(python_path):
                python_path = '/usr/bin/python3.5'
            cmd = r"""{python_path} ~/CI_Script/lgat_check/release_with_review.py -or {OLD_RELEASE} -nr {NEW_RELEASE} {TMC_ISSUE} -sc {SUNTEC_CONFIRM} -od {OUTPUT_DIR} -bl {blocklist}
                   """.format(python_path=python_path,
                              OLD_RELEASE=old_release, NEW_RELEASE=new_release,
                              TMC_ISSUE=tmc_issue, SUNTEC_CONFIRM=suntec_comfirm,
                              OUTPUT_DIR=output_dir, blocklist=blocklist_dir)
        print cmd
        os_ret = os.system(cmd)
        if os_ret != 0:
            return False
        return True

    def release_diff(self, old_release, new_release):
        if platform.system() == 'Windows':
            env_path = self._get_env_path_for_python3()
            diff = "C:\Python36\python.exe C:\proj\CI_Script\lgat_check\daily_diff_report.py"
            cmd = " && ".join([env_path, diff])
        else:
            pass
        os_ret = os.system(cmd)
        if os_ret != 0:
            return False
        return True

    def _get_env_path_for_python3(self):
        path = os.getenv('PATH')
        path_list = path.split(';')
        temp_path_list = []
        for path in path_list:
            if path.find("Python27") >= 0:
                pass
            else:
                if path:
                    temp_path_list.append(path)
        path = ';'.join(temp_path_list)
        path = "Path=%s" % path
        return path

    def collect_post_error(self, pg):
        self.collect_post_error_hu(pg)
        self.collect_post_error_def(pg)

    def collect_post_error_hu(self, pg):
        sqlcmd = """
        DROP TABLE IF EXISTS spec.post_error_hu;
        -------------------------------------------------
        create table spec.post_error_hu
        as 
            SELECT hu_id
            FROM spec.basic_req_hu AS t1
            inner JOIN spec.basic_req_definition as t2
            on t1.hu_id = t2.hu_def_id
            where (t1.dcu_status <> t2.dcu_status) or 
                  (t1.dcu_status is null and t2.dcu_status is not null) or 
                  (t1.dcu_status is not null and t2.dcu_status is null) or 
                  (t1.dcu_trigger <> t2.dcu_trigger) or
                  (t1.dcu_trigger is null and t2.dcu_trigger is not null) or
                  (t1.dcu_trigger is not null and t2.dcu_trigger is null) or 
                  (t1.dcu_action <> t2.dcu_action ) or
                  (t1.dcu_action is null and t2.dcu_action is not null) or 
                  (t1.dcu_action is not null and t2.dcu_action is null) or 
                  (t1.meu_status <> t2.meu_status ) or 
                  (t1.meu_status is null and t2.meu_status is not null) or 
                  (t1.meu_status is not null and t2.meu_status is null) or 
                  (t1.meu_trigger <> t2.meu_trigger) or 
                  (t1.meu_trigger is null and t2.meu_trigger is not null) or 
                  (t1.meu_trigger is not null and t2.meu_trigger is null) or 
                  (t1.meu_action <> t2.meu_action) or 
                  (t1.meu_action is null and t2.meu_action is not null) or 
                  (t1.meu_action is not null and t2.meu_action is null) or 
                  (t1.remark <> t2.hu_remark ) or 
                  (t1.remark is null and t2.hu_remark is not null) or 
                  (t1.remark is not null and t2.hu_remark is null)
             ORDER BY hu_id
        """
        pg.execute(sqlcmd)
        # HU作业状态完成了，DEF/ANA状态未完成
        sqlcmd = """
        INSERT INTO spec.post_error_hu(hu_id)
        (
        SELECT hu_id
          FROM (
            SELECT hu_id, t1.dcu_status, t1.dcu_trigger, t1.dcu_action,
                   t1.meu_status, t1.meu_trigger, t1.meu_action, t1.remark,
                   t2.definition_id, t2.pf_status, t2.pf_trigger, t2.pf_action
            FROM spec.basic_req_hu AS t1
            left JOIN spec.basic_req_definition as t2
            on t1.hu_id = t2.hu_def_id
            left join spec.basic_req_analysis as t3
            on t2.definition_id = t3.definition_id
            where t1.job_status = 3 and (t2.job_status <> 3 or t3.job_status <> 3)
          ) AS tt1
        )
        """
        pg.execute(sqlcmd)
        pg.commit()

    def collect_post_error_def(self, pg):
        sqlcmd = """
        DROP TABLE IF EXISTS spec.post_error_def;
        ------------------------------------------------
        create table spec.post_error_def
        as
        SELECT definition_id
        FROM spec.basic_req_hu AS t1
        INNER JOIN spec.basic_req_definition as t2
        on t1.hu_id = t2.hu_def_id
        where (t1.dcu_status <> t2.dcu_status) or 
              (t1.dcu_status is null and t2.dcu_status is not null) or 
              (t1.dcu_status is not null and t2.dcu_status is null) or 
              (t1.dcu_trigger <> t2.dcu_trigger) or
              (t1.dcu_trigger is null and t2.dcu_trigger is not null) or
              (t1.dcu_trigger is not null and t2.dcu_trigger is null) or 
              (t1.dcu_action <> t2.dcu_action ) or
              (t1.dcu_action is null and t2.dcu_action is not null) or 
              (t1.dcu_action is not null and t2.dcu_action is null) or 
              (t1.meu_status <> t2.meu_status ) or 
              (t1.meu_status is null and t2.meu_status is not null) or 
              (t1.meu_status is not null and t2.meu_status is null) or 
              (t1.meu_trigger <> t2.meu_trigger) or 
              (t1.meu_trigger is null and t2.meu_trigger is not null) or 
              (t1.meu_trigger is not null and t2.meu_trigger is null) or 
              (t1.meu_action <> t2.meu_action) or 
              (t1.meu_action is null and t2.meu_action is not null) or 
              (t1.meu_action is not null and t2.meu_action is null) or 
              (t1.remark <> t2.hu_remark ) or 
              (t1.remark is null and t2.hu_remark is not null) or 
              (t1.remark is not null and t2.hu_remark is null)
        
        union
        
        SELECT t1.definition_id
          FROM spec.basic_req_definition AS t1
          inner JOIN spec.basic_req_analysis as t2
          on t1.definition_id = t2.definition_id
          where (t1.pf_status <> t2.pf_status) or 
            (t1.pf_status is null and t2.pf_status is not null) or 
            (t1.pf_status is not null and t2.pf_status is null) or 
            (t1.pf_trigger <> t2.pf_trigger) or
            (t1.pf_trigger is null and t2.pf_trigger is not null) or
            (t1.pf_trigger is not null and t2.pf_trigger is null) or 
            (t1.pf_action <> t2.pf_action ) or
            (t1.pf_action is null and t2.pf_action is not null) or 
            (t1.pf_action is not null and t2.pf_action is null)
        """
        pg.execute(sqlcmd)
        # DEF作业状态完成了，HU/ANA作业状态未完成
        sqlcmd = """
        INSERT INTO spec.post_error_def(definition_id)
        (
        SELECT tt1.definition_id
          FROM (
            SELECT t1.hu_def_id, t1.dcu_status, t1.dcu_trigger, t1.dcu_action,
                   t1.meu_status, t1.meu_trigger, t1.meu_action, t1.remark,
                   t1.definition_id, t1.pf_status, t1.pf_trigger, t1.pf_action
            FROM spec.basic_req_definition as t1
            left JOIN spec.basic_req_hu AS t2
            on t1.hu_def_id = t2.hu_id
            left join spec.basic_req_analysis as t3
            on t1.definition_id = t3.definition_id
            where t1.job_status = 3 and (t2.job_status <> 3 or t3.job_status <> 3)
          ) AS tt1
        );
        """
        pg.execute(sqlcmd)
        # ANA作业状态完成了，DEF作业状态未完成
        sqlcmd = """
        INSERT INTO spec.post_error_def(definition_id)
        (
        SELECT tt1.definition_id
          FROM (
            SELECT t1.definition_id, t1.pf_status, t1.pf_trigger, t1.pf_action
            FROM spec.basic_req_analysis as t1
            left JOIN spec.basic_req_definition AS t2
            on t1.definition_id = t2.definition_id
            where t1.job_status = 3 and (t2.job_status <> 3)
          ) AS tt1
        );
        """
        pg.execute(sqlcmd)
        pg.commit()

    def get_not_exist_arl_id(self, pg):
        sqlcmd = """
        SELECT a.arl_id
          FROM release.hu as a
          left join spec.arl as b
          on a.arl_id = b.arl_id
          where b.arl_id is null
        """
        pg.execute(sqlcmd)
        rows = pg.fetchall()
        arl_list = []
        for row in rows:
            arl_list.append(row[0])
        return arl_list

    def check_post(self, pg):
        print 'Check Post'
        if not self.check_hu_def_post(pg):
            return False
        if not self.check_def_ana_post(pg):
            return False
        return True

    def check_hu_def_post(self, pg):
        sqlcmd = """
        SELECT hu_id,
               t1.dcu_status, t1.dcu_trigger, t1.dcu_action, t1.meu_status, t1.meu_trigger, 
               t1.meu_action, t1.remark, 
               t2.dcu_status, t2.dcu_trigger, t2.dcu_action, t2.meu_status, t2.meu_trigger, 
               t2.meu_action, t2.hu_remark,
               t1.dcu_status = t2.dcu_status, t1.dcu_trigger = t2.dcu_trigger,
               t1.dcu_action = t2.dcu_action, t1.meu_status = t2.meu_status,
               t1.meu_trigger = t2.meu_trigger, t1.meu_action =t2.meu_action,
               t1.remark = t2.remark
        FROM release.basic_req_hu AS t1
        inner JOIN release.basic_req_definition as t2
        on t1.hu_id = t2.hu_def_id
        where (t1.dcu_status <> t2.dcu_status) or 
              (t1.dcu_status is null and t2.dcu_status is not null) or 
              (t1.dcu_status is not null and t2.dcu_status is null) or 
              (t1.dcu_trigger <> t2.dcu_trigger) or
              (t1.dcu_trigger is null and t2.dcu_trigger is not null) or
              (t1.dcu_trigger is not null and t2.dcu_trigger is null) or 
              (t1.dcu_action <> t2.dcu_action ) or
              (t1.dcu_action is null and t2.dcu_action is not null) or 
              (t1.dcu_action is not null and t2.dcu_action is null) or 
              (t1.meu_status <> t2.meu_status ) or 
              (t1.meu_status is null and t2.meu_status is not null) or 
              (t1.meu_status is not null and t2.meu_status is null) or 
              (t1.meu_trigger <> t2.meu_trigger) or 
              (t1.meu_trigger is null and t2.meu_trigger is not null) or 
              (t1.meu_trigger is not null and t2.meu_trigger is null) or 
              (t1.meu_action <> t2.meu_action) or 
              (t1.meu_action is null and t2.meu_action is not null) or 
              (t1.meu_action is not null and t2.meu_action is null) or 
              (t1.remark <> t2.hu_remark ) or 
              (t1.remark is null and t2.hu_remark is not null) or 
              (t1.remark is not null and t2.hu_remark is null)
        ---------------------------------------------------------------------------------
        union
        SELECT hu_id,
               t1.dcu_status, t1.dcu_trigger, t1.dcu_action, t1.meu_status, t1.meu_trigger, 
               t1.meu_action, t1.hu_remark, 
               t2.dcu_status, t2.dcu_trigger, t2.dcu_action, t2.meu_status, t2.meu_trigger, 
               t2.meu_action, t2.remark,
               t1.dcu_status = t2.dcu_status, t1.dcu_trigger = t2.dcu_trigger,
               t1.dcu_action = t2.dcu_action, t1.meu_status = t2.meu_status,
               t1.meu_trigger = t2.meu_trigger, t1.meu_action =t2.meu_action,
               t1.remark = t2.remark
        FROM release.basic_req_definition AS t1
        left JOIN release.basic_req_hu as t2
        on t1.hu_def_id = t2.hu_id
        where ((t1.dcu_status <> t2.dcu_status) or 
               (t1.dcu_status is null and t2.dcu_status is not null) or 
               (t1.dcu_status is not null and t2.dcu_status is null) or 
               (t1.dcu_trigger <> t2.dcu_trigger) or
               (t1.dcu_trigger is null and t2.dcu_trigger is not null) or
               (t1.dcu_trigger is not null and t2.dcu_trigger is null) or 
               (t1.dcu_action <> t2.dcu_action ) or
               (t1.dcu_action is null and t2.dcu_action is not null) or 
               (t1.dcu_action is not null and t2.dcu_action is null) or 
               (t1.meu_status <> t2.meu_status ) or 
               (t1.meu_status is null and t2.meu_status is not null) or 
               (t1.meu_status is not null and t2.meu_status is null) or 
               (t1.meu_trigger <> t2.meu_trigger) or 
               (t1.meu_trigger is null and t2.meu_trigger is not null) or 
               (t1.meu_trigger is not null and t2.meu_trigger is null) or 
               (t1.meu_action <> t2.meu_action) or 
               (t1.meu_action is null and t2.meu_action is not null) or 
               (t1.meu_action is not null and t2.meu_action is null) or 
               (t1.hu_remark <> t2.remark ) or 
               (t1.hu_remark is null and t2.remark is not null) or 
               (t1.hu_remark is not null and t2.remark is null)
              ) and (t2.hu_id is not null)
              or
              (t2.hu_id is null and substr(t1.definition_id, 1, 1) = 'B')
        """
        pg.execute(sqlcmd)
        row = pg.fetchone()
        if row:
            return False
        return True

    def check_def_ana_post(self, pg):
        sqlcmd = """
        SELECT t1.definition_id,
               t1.pf_status, t1.pf_trigger, t1.pf_action,
               t2.pf_status, t2.pf_trigger, t2.pf_action 
          FROM release.basic_req_definition AS t1
          inner JOIN release.basic_req_analysis as t2
          on t1.definition_id = t2.definition_id
          where (t1.pf_status <> t2.pf_status) or 
                (t1.pf_status is null and t2.pf_status is not null) or 
                (t1.pf_status is not null and t2.pf_status is null) or 
                (t1.pf_trigger <> t2.pf_trigger) or
                (t1.pf_trigger is null and t2.pf_trigger is not null) or
                (t1.pf_trigger is not null and t2.pf_trigger is null) or 
                (t1.pf_action <> t2.pf_action ) or
                (t1.pf_action is null and t2.pf_action is not null) or 
                (t1.pf_action is not null and t2.pf_action is null)
        ---------------------------------------------------------------------------------
        union
        SELECT t1.definition_id,
               t1.pf_status, t1.pf_trigger, t1.pf_action,
               t2.pf_status, t2.pf_trigger, t2.pf_action
          FROM release.basic_req_analysis AS t1
          left JOIN release.basic_req_definition as t2
          on t1.definition_id = t2.definition_id
          where ((t1.pf_status <> t2.pf_status) or 
                 (t1.pf_status is null and t2.pf_status is not null) or 
                 (t1.pf_status is not null and t2.pf_status is null) or 
                 (t1.pf_trigger <> t2.pf_trigger) or
                 (t1.pf_trigger is null and t2.pf_trigger is not null) or
                 (t1.pf_trigger is not null and t2.pf_trigger is null) or 
                 (t1.pf_action <> t2.pf_action ) or
                 (t1.pf_action is null and t2.pf_action is not null) or 
                 (t1.pf_action is not null and t2.pf_action is null)
                 ) and (t2.definition_id is not null)
                 or
                (t2.definition_id is null and substr(t1.definition_id, 1, 1) in ('B', 'C'))
        """
        pg.execute(sqlcmd)
        row = pg.fetchone()
        if row:
            return False
        return True

    def copy_release_2_ftp(self, release_path, rls_date):
        rls_date = self.conver_date_format(rls_date)
        if platform.system() == 'Windows':
            dest = os.path.join(r'Z:\LGAT\99.Output\SpiderOutput', rls_date)
        else:
            dest = os.path.join(os.path.expanduser('~'), 'ftp/LGAT/99.Output/SpiderOutput', rls_date)
        if not os.path.isdir(dest):
            os.mkdir(dest)
        file_name = self.get_release_dest_file(release_path, dest)
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


def check_local_ip(ip=SPIDER_HOST):
    local_ips = get_local_ips()
    for local_ip in local_ips:
        if local_ip == ip:
            return True
    return False


def get_local_ips():
    ips = []
    import netifaces
    interfaces = netifaces.interfaces()  # ['lo', 'eno1']
    for interface in interfaces:
        addrs = netifaces.ifaddresses(interface)
        for addr in addrs[netifaces.AF_INET]:
            ips.append(addr['addr'])
    return ips


def play(start=True):
    if platform.system() == 'Windows':
        import winsound
        if start:
            sound = 'SystemQuestion'
        else:
            sound = 'SystemExit'
        play_count = 0
        while play_count < 3:
            winsound.PlaySound(sound, winsound.SND_PURGE)
            time.sleep(0.2)
            play_count += 1
    else:
        # sudo apt install sox
        if start:
            cmd = 'spd-say "Release Starting!"'
        else:
            cmd = 'spd-say "Release Finished!"'
        for i in range(0, 2):
            os.system(cmd)
            time.sleep(2.0)


def main():
    os.chdir('../')
    print os.getcwd()
    # check_local_ip()
    rls_ojb = ArlRelease()
    rls_ojb._pg.connect()
    path = r'local_release/349/2018-01-26'
    rls_ojb.write_unsync_2_release_record(rls_ojb._pg, path)
    rls_ojb._pg.close()
    print rls_ojb.get_current_time()
    return 0
    # in_dir'local_release\450\2017-12-21-cut'
    # print rls_ojb.zip_file(in_dir, out_dir=r'local_release\450', zip_name='release.zip')
    # return 0
    # update_time = rls_ojb.get_current_time()
    version, rls_date, pre_rls_date, user_id = '0.016', '2018-01-09', '2018-01-03', 450
    rls_ojb.copy_release_2_ftp(r'local_release/450/2018-01-09', rls_date)
    return 0
    tmc_issue_url = r'\\192.168.0.3\ftpboot\LGAT\99.Output\SpiderOutput\SuntecReply_TMCComments_Sample'.encode('gbk')
    suntec_confirm_url = r'\\192.168.0.3\ftpboot\LGAT\99.Output\SpiderOutput\SuntecReply_TMCComments_Sample'.encode('gbk')
    blocklist_url = r'\\192.168.0.3\ftpboot\LGAT\13_TMC指摘\20180105'
    if platform.system() == 'Windows':
        blocklist_url = blocklist_url.encode('gbk')
    result = rls_ojb.start(version, rls_date,  pre_rls_date, user_id,
                           tmc_issue_url, suntec_confirm_url, blocklist_url)
    path = result[1]
    if path:
        rls_ojb.copy_release_2_ftp(path, rls_date)
    print result
    # rls_ojb.sync_release(RELEASE_ROOT_DIR)
    # # return 0
    # rls_path = os.path.join('local_release', '450', rls_date)
    # pre_rls_date = '2017-12-20'
    # rls_ojb.lgat(user_id, rls_path, rls_date, pre_rls_date)
    # new_release = rls_ojb.mk_local_release_path(user_id, rls_date, suffix='style')
    # merger_out_dir = r'C:\proj\Spec2DB\Source\spec2db_server\local_release\450\2017-12-21-merger\release'
    # rls_ojb.update_excel_style(merger_out_dir, new_release)
    print rls_ojb.get_current_time()


if __name__ == '__main__':
    import sys
    reload(sys)
    sys.setdefaultencoding('UTF-8')
    main()
