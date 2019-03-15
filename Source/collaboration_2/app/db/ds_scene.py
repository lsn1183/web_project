# -*- coding: UTF-8 -*-
from app.db import db


class DSScene(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_scene'

    scene_id = db.Column(db.Integer, primary_key=True)
    scene = db.Column(db.String(100))  # 场景
    # scene_type = db.Column(db.String(100))  # 场景分类
    order_no = db.Column(db.Integer)  # 排序编号
    explain = db.Column(db.String(100))  # 翻译解释
    scene_org = db.Column(db.String(100))
    scene_type_id = db.Column(db.Integer, db.ForeignKey('ds.ds_scene_type.scene_type_id'))

    def __repr__(self):
        return '<Scene %r>' % self.scene

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSceneType(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_scene_type'

    scene_type_id = db.Column(db.Integer, primary_key=True)
    scene_type = db.Column(db.String(100))  # 场景分类
    scene_type_org = db.Column(db.String(100))  # 场景分类

    def __repr__(self):
        return '<SceneType %r>' % self.scene_type

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSRelScene(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_rel_scene'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)  # 场景
    sec_id = db.Column(db.Integer)
    scene_id = db.Column(db.Integer)
    change = db.Column(db.String(500))  # 变更点
    alter = db.Column(db.String(500))  # 变化点

    def __repr__(self):
        return '<Scene %r>' % self.scene_id

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSSceneTag(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_scene_tag_rel'

    gid = db.Column(db.Integer, primary_key=True)
    scene_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)

    def __repr__(self):
        return '<Scene %r:%r>' % (self.scene_id, self.tag_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class DSRelTag(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'ds_rel_tag'

    gid = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer)  # 场景
    # sec_id = db.Column(db.Integer)
    tag_id = db.Column(db.Integer)
    before_change = db.Column(db.String(500))  # 修改前
    change = db.Column(db.String(500))  # 修改后
    before_influence = db.Column(db.String(500))  # 影响前
    influence = db.Column(db.String(500))  # 影响后
    order_id = db.Column(db.Integer)  # 排序用ID

    def __repr__(self):
        return '<RelTag doc_id=%r, tag_id=%r, gid=%r>' % (self.doc_id, self.tag_id, self.gid)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
