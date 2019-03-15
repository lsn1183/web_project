# -*- coding: UTF-8 -*-
from ..db import db


class DsModelTagRel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_model_tag_rel'

    gid = db.Column(db.Integer, primary_key=True)
    model_id = db.Column(db.Integer, db.ForeignKey('ds.model.model_id'))  # 模块
    tag_id = db.Column(db.Integer, db.ForeignKey('public.doc_tag_category.tag_id'))  # Tag ID
    proj_id = db.Column(db.Integer, db.ForeignKey('ds.project.proj_id'))  # 项目id

    def __repr__(self):
        return '<DsModelTagRel %r:%r>' % (self.model_id, self.tag_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d