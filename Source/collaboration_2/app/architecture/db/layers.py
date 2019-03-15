# -*- coding: UTF-8 -*-
from app.db import db


class Layer(db.Model):
    __table_args__ = {"schema": "architecture"}
    __tablename__ = 'layers'

    gid = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.String(30))
    layer_id1 = db.Column(db.String(30))
    layer1 = db.Column(db.String(30))


    def __repr__(self):
        return '<Title %r>' % self.doc_title

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d