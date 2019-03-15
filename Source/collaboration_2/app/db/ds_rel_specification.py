# -*- coding: UTF-8 -*-
from app.db import db


class DSRelSpec(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_rel_specification'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_doc.doc_id'))
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))
    # spec_type = db.Column(db.String(30))
    # spec_name = db.Column(db.String(1024))  # 式样书名称
    spec_id = db.Column(db.Integer, db.ForeignKey('spec.spec_specification.spec_id'))
    func_id = db.Column(db.String(100))  # 机能点

    def __repr__(self):
        return '<Spec %r %r>' % (self.spec_id, self.func_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSRelFun(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_rel_fun'

    gid = db.Column(db.Integer, primary_key=True)
    sec_id = db.Column(db.Integer, db.ForeignKey('ds.ds_section.sec_id'))  # usecase_id
    ver_id = db.Column(db.Integer, db.ForeignKey('spec.spec_specVersion.ver_id'))
    func_name = db.Column(db.String(100))  # 章节名
    func_id = db.Column(db.String(100))  # 机能点

    def __repr__(self):
        return '<Spec %r %r>' % (self.sec_id, self.func_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

