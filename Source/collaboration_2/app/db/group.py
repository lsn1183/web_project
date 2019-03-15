from app.db import db


class Group(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'groups'

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))  # 模块名

    def __repr__(self):
        return '<Group %r:%r>' % (self.group_id, self.group_name)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class Member(db.Model):
    __table_args__ = {"schema": "public"}
    __tablename__ = 'members'

    gid = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer)  # 组ID
    user_id = db.Column(db.Integer)  # 用户ID

    def __repr__(self):
        return '<Group %r:%r>' % (self.group_id, self.user_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d


class GroupModel(db.Model):
    __table_args__ = {"schema": "ds"}
    __tablename__ = 'group_model_rel'

    gid = db.Column(db.Integer, primary_key=True)
    proj_id = db.Column(db.Integer)  # 项目ID
    model_id = db.Column(db.Integer)  # 模块名
    group_name = db.Column(db.String(500))  # 小组名

    def __repr__(self):
        return '<GroupModel %r:%r>' % (self.group_id, self.model_id)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:
            d[column.name] = getattr(self, column.name)
        return d

