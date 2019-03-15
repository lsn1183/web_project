# -*- coding: UTF-8 -*-
from app.db import db


class DSDocIf(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_if'

    if_id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_doc.doc_id'))
    if_name = db.Column(db.String(512))
    parameter = db.Column(db.String(1024))
    return_val = db.Column(db.String(512))
    description = db.Column(db.String(512))
    micro_ver = db.Column(db.Integer)  # 微版本

    def __repr__(self):
        return '<CheckItem %r>' % self.content

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
