# -*- coding: UTF-8 -*-
import datetime
import json
import pandas as pd
import numpy as np
import platform
import datetime
import copy
from collections import Iterable
from flask import current_app
from app.db import db
from app.db.journal import Journal, JournalBrief, JournalDetail
from sqlalchemy_utils.functions import get_primary_keys



JOURNALIZED_TYPE_BACKUP = 'BACKUP'
JOURNALIZED_TYPE_JOURNAL = 'JOURNAL'


class CtrlJournal(object):
    def __init__(self):
        pass

    def write(self, db_objs, **kwargs):
        """
        :param db_objs: declarative_base(db.Model) object.
        :param journalized_id: (optional)
        :param username: (optional).
        :param journalized_type: (optional).
        :param notes: (Optional).
        :param update_time: (Optional).
        :return: success return True.
        """
        # journalized_id = kwargs.get("journalized_id")
        # if not journalized_id:
        #     current_app.logger.warning('Dose not indicate journalized id[%s].'
        #                                % journalized_id)
        username = kwargs.get("username")
        journalized_type = kwargs.get("journalized_type")
        if not journalized_type:
            journalized_type = JOURNALIZED_TYPE_BACKUP
        notes = kwargs.get("notes")
        create_time = kwargs.get("update_time")
        if not create_time:
            create_time = kwargs.get("create_time")
        journalized_id = self.write_journal(journalized_type, username,
                                            notes, create_time)
        if not journalized_id:
            current_app.logger.error('Write journal failed.')
            return False
        if isinstance(db_objs, Iterable):
            for db_obj in db_objs:
                journal_brief_id = self._write_journal_brief(db_obj,
                                                             journalized_id)
                if not self._write_journal_detail(db_obj,
                                                  journal_brief_id):
                    return False
        else:
            journal_brief_id = self._write_journal_brief(db_objs,
                                                         journalized_id)
            if not journal_brief_id:
                return False
            if not self._write_journal_detail(db_objs, journal_brief_id):
                return False
        return True

    def write_journal(self, journalized_type, username, notes, create_time):
        if not username:
            current_app.logger.error('Dose not indicate user')
            return 0
        from app.ctrl.ctrl_user import CtrlUser
        if not username:
            current_app.logger.error("Dose not indicate user.")
            return 0
        user = CtrlUser().get_user_by_name(username)
        if not user:
            current_app.logger.error("Dose not exist user[%s]." % username)
            return 0
        if not create_time:
            create_time = datetime.datetime.now()
            pass
        journal_info = {Journal.journalized_type.name: journalized_type,
                        Journal.user_id.name: user.user_id,
                        Journal.notes.name: notes,
                        Journal.create_time.name: create_time,
                        }
        journal = Journal(**journal_info)
        db.session.add(journal)
        db.session.flush()
        return journal.journalized_id

    def _write_journal_brief(self, db_obj, journalized_id):
        if not journalized_id:
            return 0
        if db_obj and isinstance(db_obj, db.Model):
            table_name = db_obj.__tablename__
            data = {JournalBrief.table_name.name: table_name,
                    JournalBrief.journalized_id.name: journalized_id,
                    JournalBrief.key_id.name: self.get_key_id(db_obj),
                    JournalBrief.action.name: 'backup',
                    }
            journal_brief = JournalBrief(**data)
            db.session.add(journal_brief)
            db.session.flush()
            return journal_brief.j_brief_id
        else:
            current_app.logger.error("Type is not db.Model. current type[%s]."
                                     % type(db_obj))
            return 0

    def _write_journal_detail(self, db_obj, journal_brief_id):
        if not journal_brief_id:
            return False
        if db_obj and isinstance(db_obj, db.Model):
            # table_name = db_obj.__tablename__
            detail = {JournalDetail.j_brief_id.name: journal_brief_id,
                      # JournalDetail.table_name.name: table_name,
                      # JournalDetail.key_id.name: self.get_key_id(db_obj)
                      }
            for column in db_obj.__table__.columns:
                val = getattr(db_obj, column.name)
                detail[JournalDetail.column_name.name] = column.name
                detail[JournalDetail.val.name] = val
                db.session.add(JournalDetail(**detail))
            return True
        else:
            current_app.logger.error("Type is not db.Model. current type[%s]."
                                     % type(db_obj))
            return False

    def get_key_id(self, db_obj):
        # primary_keys = inspect(db_obj).primary_key
        # primary_keys = get_primary_keys(db_obj)
        # print(db_obj)
        primary_keys = list(get_primary_keys(db_obj).keys())
        if primary_keys:
            key_name = primary_keys[0]
            return getattr(db_obj, key_name)
        else:
            column = db_obj.__table__.columns[0]
            return getattr(db_obj, column.name)

    def get_journal_detail(self, journalized_id):
        sqlcmd = """
        SELECT key_id, table_name, column_name, val
          FROM public.journals as a
          left join public.journal_briefs as b
          on a.journalized_id = b.journalized_id
          left join public.journal_details as c
          on b.j_brief_id = c.j_brief_id
          where a.journalized_id = {journalized_id}
          order by b.j_brief_id, c.j_detail_id
        """.format(journalized_id=journalized_id)
        df = pd.read_sql(sqlcmd, db.session.bind)
        return df

    def get_detatils_by_journalized_id(self, journalized_id):
        q = (db.session.query(JournalDetail)
             .filter(JournalDetail.journalized_id == journalized_id)
             .order_by(JournalDetail.journal_id)
             )
        sqlcmd = q.statement
        df = pd.read_sql(sqlcmd, db.session.bind)
        return df

    def add_journals(self, log, journalized_type=JOURNALIZED_TYPE_JOURNAL):
        journalized_id = self._add_journal(log, journalized_type)
        if not journalized_id:
            return False
        for commit in log.get('commit_list'):
            table_name = commit.get("table_name")
            action = commit.get("action")
            key_id = commit.get("key_id")
            journal_brief_id = self._add_journal_brief(journalized_id, key_id,
                                                       table_name, action)
            data = commit.get("data")
            self._add_journal_detial(journal_brief_id, key_id, data)
        return True

    def _add_journal(self, log, journalized_type):
        # from app.ctrl.ctrl_user import CtrlUser
        user_id = log.get("commit_user")
        if not user_id:
            current_app.logger.error("Dose not indicate user.")
            return 0
        # user = CtrlUser().get_user_by_name(user_name)
        # if not user:
        #     current_app.logger.error("Dose not exist user[%s]." % user_name)
        #     return 0
        # user_id = user.user_id
        data = {Journal.journalized_type.name: journalized_type,
                Journal.create_time.name: log.get("update_time"),
                Journal.user_id.name: user_id,
                }
        journal = Journal(**data)
        db.session.add(journal)
        db.session.flush()
        return journal.journalized_id

    def _add_journal_brief(self, journalized_id, key_id, table_name, action):
        data = {JournalBrief.journalized_id.name: journalized_id,
                JournalBrief.key_id.name: key_id,
                JournalBrief.action.name: action,
                JournalBrief.table_name.name: table_name,
                }
        journal_brief = JournalBrief(**data)
        db.session.add(journal_brief)
        db.session.flush()
        return journal_brief.j_brief_id

    def _add_journal_detial(self, journal_brief_id, key_id, log_data):
        for col in log_data:
            data = {JournalDetail.j_brief_id.name: journal_brief_id,
                    # JournalDetail.key_id.name: key_id,
                    JournalDetail.column_name.name: col,
                    JournalDetail.val.name: log_data[col],
                    }
            journal_detail = JournalDetail(**data)
            db.session.add(journal_detail)


################################################################################
#
################################################################################


