# -*- coding: UTF-8 -*-
from app.db import db
from app.db.comment import Comment
import datetime
from app.ctrl.ctrl_base import CtrlBase


class CtrlComment(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)

    def add(self, data):
        if not data.get(Comment.sec_id.name):
            return False, '未指定章节ID'
        data[Comment.cm_time.name] = datetime.datetime.now()
        comment = Comment(**data)
        db.session.add(comment)
        # db.session.flush()
        db.session.commit()
        return True, 'OK'

    def get(self, sec_id):
        comment_list = []
        q = (db.session.query(Comment)
             .filter(Comment.sec_id == sec_id)
             .order_by(Comment.gid)
             )
        for cm in q:
            cm_dict = cm.to_dict()
            if cm.cm_time:
                cm_dict[Comment.cm_time.name] = cm.cm_time.strftime('%Y-%m-%d %H:%M:%S%Z')
            comment_list.append(cm_dict)
        return comment_list
