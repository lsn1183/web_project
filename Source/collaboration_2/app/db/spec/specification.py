# -*- coding: UTF-8 -*-
from app.db import db


class Specification(db.Model):
    __table_args__ = {"schema": "spec"}
    __tablename__ = 'spec_specification'

    spec_id = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer)
    spec_name = db.Column(db.String(100))  # 文档名称
    spec_file_name = db.Column(db.String(100))  # 章节ID
    spec_type = db.Column(db.String(30))  # 评论内容
    search_str = db.Column(db.String(1024))
    spec_num = db.Column(db.String(64))  # 章节号

    def __repr__(self):
        return ('<Spec spec_type:%r, spec_name:%r, spec_id:%r>' %
                (self.spec_type, self.spec_name, self.spec_id))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


db.Index('spec_specification_proj_id_spec_type_spec_num_idx',
         Specification.proj_id, Specification.spec_type, Specification.spec_num,
         # unique=True
         )


class SpecVersion(db.Model):
    __table_args__ = {"schema": "spec"}
    __tablename__ = 'spec_specVersion'

    ver_id = db.Column(db.Integer, primary_key=True)
    spec_id = db.Column(db.Integer, db.ForeignKey('spec.spec_specification.spec_id'))
    spec_ver = db.Column(db.String(64))  # 版本号
    excel_url = db.Column(db.String(2048))
    html_url = db.Column(db.String(2048))
    create_time = db.Column(db.Date)  # 创建时间

    def __repr__(self):
        return ('<SpecVer ver_id:%r, spec_id:%r, spec_ver:%r>' %
                (self.ver_id, self.spec_id, self.spec_ver))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


db.Index('spec_specVersion_spec_id_spec_ver_idx',
         SpecVersion.spec_id, SpecVersion.spec_ver,
         unique=True
         )


class ProjectMember(db.Model):
    __table_args__ = {"schema": "spec"}
    __tablename__ = 'spec_projectmember'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(32))
    project_name = db.Column(db.String(2048))
    # create_time = db.Column(db.Date)  # 创建时间

    def __repr__(self):
        return ('<ProMember id:%r project_name:%r, user_id:%r>' %
                (self.id, self.project_name, self.user_id))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class HeaderFile(db.Model):
    __table_args__ = {"schema": "spec"}
    __tablename__ = 'spec_headerfile'

    h_id = db.Column(db.Integer, primary_key=True)
    doc_id = db.Column(db.Integer, db.ForeignKey('ds.ds_doc.doc_id'))
    html_url = db.Column(db.String(2048))
    status = db.Column(db.String(10))  # 删除和新增
    create_time = db.Column(db.Date)  # 创建时间

    def __repr__(self):
        return ('<SpecHF h_id:%r, doc_id:%r>' %
                (self.h_id, self.doc_id))

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d
