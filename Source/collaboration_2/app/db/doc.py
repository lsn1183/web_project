# -*- coding: UTF-8 -*-
from ..db import db
from sqlalchemy.orm import relationship


class Doc(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'docs'

    doc_id = db.Column(db.Integer, primary_key=True)
    doc_type = db.Column(db.String(10))  # file:本地方件，url：url地址，text:  文本
    doc_title = db.Column(db.String(256))  # 文档Title
    content = db.Column(db.String(1024))  # 文档路径or Url地址 or 正文
    ver = db.Column(db.String(30))  # 版本号
    summary = db.Column(db.String(2048))  # 摘要
    author = db.Column(db.String(30))  # 作者
    committer = db.Column(db.String(30))  # 提交者
    create_time = db.Column(db.String(30))  # 创建时间
    update_time = db.Column(db.String(30))  # 更新时间
    keywords = db.Column(db.String(2014))  # 关键词
    sub_cat = db.Column(db.String(255))

    def __repr__(self):
        return '<Title %r>' % self.doc_title

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Consider(db.Model):
    """考虑点
    """
    __table_args__ = {"schema": "public"}
    __tablename__ = 'consider'

    consider_id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('public.docs.doc_id'))  # 设计文档ID
    consider_name = db.Column(db.String(1024))  # 考虑内容

    def __repr__(self):
        return '<Consider %r>' % self.consider_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class FailureMode(db.Model):
    """故障模式
    """
    __table_args__ = {"schema": "public"}
    __tablename__ = 'failure_mode'

    failure_id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('public.docs.doc_id'))  # 设计文档ID
    failure_mode_name = db.Column(db.String(1024))  # 故障模式

    def __repr__(self):
        return '<failure_mode %r>' % self.failure_mode_name

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


