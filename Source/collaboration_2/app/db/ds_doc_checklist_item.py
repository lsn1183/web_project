# -*- coding: UTF-8 -*-
from app.db import db


class DSChecklistItem(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_doc_checklist_item'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)
    sec_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    content = db.Column(db.String(1024))

    def __repr__(self):
        return '<CheckItem %r>' % self.content

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
