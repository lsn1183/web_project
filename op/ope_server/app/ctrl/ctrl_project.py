import os
from flask import current_app
from app.db.models import *
from app.ctrl.ctrl_base import CtrlBase


class CtrlProject(CtrlBase):

    def __init__(self):
        CtrlBase.__init__(self)
        self.key_col = Projects.proj_id
        self.db_object = Projects

    def add_project(self, data):
        try:
            proj_name = data.get('proj_name')
            describe = data.get('describe')
            proj_id = self.add_proj_to_table(proj_name, describe)
            db.session.commit()
            return True, proj_id
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def add_proj_to_table(self, proj_name, describe):
        pro_info = {
            Projects.proj_name.name: proj_name,
            Projects.describe.name: describe,
            Projects.create_time.name: self.get_current_time(),
            Projects.update_time.name: self.get_current_time(),
        }
        pro = Projects(**pro_info)
        db.session.add(pro)
        db.session.flush()
        return pro.proj_id

    def get_proj_list(self):
        """
        获取所有的项目
        :param project_type:
        :return:
        """
        project_list = []
        q = db.session.query(Projects).all()
        for q_obj in q:
            project = dict()
            project[Projects.proj_id.name] = q_obj.proj_id
            project[Projects.proj_name.name] = q_obj.proj_name
            project[Projects.create_time.name] = self.time_to_str(q_obj.create_time)
            project[Projects.update_time.name] = self.time_to_str(q_obj.update_time)
            project[Projects.describe.name] = q_obj.describe
            project_list.append(project)
        return project_list

    def get_one_proj_by_id(self, pro_id):
        try:
            proj_info = db.session.query(Projects).filter(Projects.proj_id == pro_id).first()
            if proj_info:
                project = dict()
                project["proj_name"] = proj_info.proj_name
                project["proj_id"] = proj_info.proj_id
                project["describe"] = proj_info.describe
                project["update_time"] = self.time_to_str(proj_info.update_time)
                project["create_time"] = self.time_to_str(proj_info.create_time)
                return True, project
            else:
                return False, "沒有此項目信息"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def change_proj_by_id(self, data):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == data.get("proj_id")).first())
            if proj:
                proj.proj_name = data.get("proj_name")
                proj.describe = data.get("describe")
                proj.update_time = self.get_current_time()
                db.session.commit()
                return True, proj.proj_id
            else:
                return False, "沒有此項目"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"

    def delete_proj_by_id(self, proj_id):
        try:
            proj = (db.session.query(Projects).filter(Projects.proj_id == proj_id))
            if proj:
                proj.delete()
                db.session.commit()
                return True, ""
            else:
                return False, "沒有此項目或此项目已被删除"
        except Exception as e:
            db.session.rollback()
            current_app.logger.error('%s' % str(e))
            return False, "服务异常！请联系管理员！"