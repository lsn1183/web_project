# -*- coding: UTF-8 -*-
import datetime
from app.db import db


class DSAttach(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_attach'

    attach_id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(512))
    file_url = db.Column(db.String(2014))
    file_type = db.Column(db.String(2014))
    ver = db.Column(db.String(30))
    committer = db.Column(db.String(30))
    update_time = db.Column(db.Date)
    commit_time = db.Column(db.Date)
    micro_ver = db.Column(db.Integer)  # 微版本

    def __repr__(self):
        return '<Attach %r>' % self.file_name

    def to_dict(self, auto_convert_time=True):
        d = {}
        for column in self.__table__.columns:
            attr = getattr(self, column.name)
            if auto_convert_time and type(attr) in (datetime.datetime,
                                                    datetime.time):
                d[column.name] = attr.strftime("%Y-%m-%d %H:%M:%S")
            else:
                d[column.name] = attr
        return d
