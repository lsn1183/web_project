# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
#
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:pset123456@192.168.37.143/test_hcz'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#
# db = SQLAlchemy(app)
# # db.create_all()
# migrate = Migrate(app, db)
#
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)
#
#
# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#
#
# class Test1(db.Model):
#     __table_args__ = {"schema": "ds"}
#     __table_name__ = 'test1'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(128))
#
#
# if __name__ == '__main__':
#     manager.run()
#
from flask import Flask
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from config import config
from app.db import db

app = Flask(__name__)
app.config.from_object(config['default'])
# cache.init_app(app)
db.app = app
db.init_app(app)
# from app.db import *
# import app.db
# db.create_all(app=app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# from app.db.doc import *
# from app.db.doc_tag_cat import *
# from app.db.doc_tags import *
# from app.db.ds_attach import *
# from app.db.ds_doc import *
# from app.db.ds_doc_checklist_item import *
# from app.db.ds_doc_if import *
# from app.db.ds_doc_template import *
# from app.db.ds_drbfm import *
# from app.db.ds_failure import *
# from app.db.ds_model_tag_rel import *
# from app.db.ds_rel_specification import *
# from app.db.ds_resource import *
# from app.db.ds_scene import *
# from app.db.ds_section import *
# from app.db.framework import *
# from app.db.group import *
# from app.db.journal import *
# from app.db.knowledge import *
# from app.db.model import *
# from app.db.permission import *
# from app.db.project import *
# from app.db.role import *
# from app.db.role_permissions import *
# from app.db.user import *
# from app.db.user_roles import *


if __name__ == '__main__':
    manager.run()
