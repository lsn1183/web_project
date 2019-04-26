from app.db import db
from app.db.models import Users
class CtrlUser(object):
    def __init__(self):
        pass

    def get_user_by_name(self, username):
        q = db.session.query(Users)
        user = q.filter(Users.user_name == username).first()
        if user:
            return user
        return None

    def register(self, username='', work_id=''):
        if username:
            user = db.session.query(Users).filter(Users.user_name == username).first()
            if user:  # 用户已经存在
                user_id = user.user_id
                user_dict = user.to_dict()
                return user_dict
            else:  # 新用户
                user = self.add(username, work_id)
                if user:
                    user_dict = user.to_dict()
                    return user_dict
        return {}

    def add(self, username='', work_id=''):
        if username:
            user = Users(user_name=username, user_emp_id=work_id)
            db.session.add(user)
            db.session.commit()
            return user
        return None