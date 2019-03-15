# -*- coding: UTF-8 -*-
from app.db import db


class DSDrbfm(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_drbfm'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))
    item_id = db.Column(db.Integer, db.ForeignKey('ds.ds_failure.item_id'))
    scene_id = db.Column(db.Integer, db.ForeignKey('ds.ds_scene.scene_id'))
    drbfm_content = db.Column(db.String(2048))

    def __repr__(self):
        return '<CheckItem %r>' % self.content

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d