# -*- coding: UTF-8 -*-
from app.db import db


class Model(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'model'

    model_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))  # 标题
    summary = db.Column(db.String())  # 概述
    code = db.Column(db.String(10))  # 编号
    path = db.Column(db.String(255))  # 路径

    def __repr__(self):
        return '<Model %r:%r>' % (self.model_id, self.title)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class ModelCode(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'model_code'

    gid = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10))  # 模块编号
    model_name = db.Column(db.String())  # 模块名称
    match1 = db.Column(db.String())
    match2 = db.Column(db.String())
    match3 = db.Column(db.String())
    remark = db.Column(db.String())

    def __repr__(self):
        return '<ModelCode %r:%r>' % (self.code, self.model_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSRelModel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_rel_model'

    gid = db.Column(db.Integer, primary_key=True)
    change_id = db.Column(db.Integer)  # ds.ds_rel_tag->gid
    change_type = db.Column(db.String(10))  # change:修改点, influence: 影响点
    model_id = db.Column(db.Integer)
    checked = db.Column(db.BOOLEAN)  # 是否确认过 failuremode。
    failure_id_list = db.Column(db.String())  # failure_id1 | failure_id2 | failure_id3
    result = db.Column(db.String())  # 完成结果

    def __repr__(self):
        return '<DSRelModel change_id=%r,model_id=%r>' % (self.change_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
