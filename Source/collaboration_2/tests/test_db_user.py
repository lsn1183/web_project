from flask import Flask
from app.db import db

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:pset123456@192.168.0.182/spec2db_0105'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


if __name__ == '__main__':
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    app.run()

    db.session.connection()

    #User.query.all()
