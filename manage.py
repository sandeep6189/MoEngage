from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.login import LoginManager, UserMixin
from app import models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:admin@localhost/moengage'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    image = db.Column(db.String(300),index=True)
    social_id = db.Column(db.String(120),index=True,unique=True)
    gender = db.Column(db.String(10))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    timezone = db.Column(db.String(40))

class User_friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_user = db.Column(db.Integer)
    end_user = db.Column(db.String(64))
    end_user_id = db.Column(db.String(300))
    end_user_pic_url = db.Column(db.String(300))

class Posts(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    post_content = db.Column(db.Text)
    source_user = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

class Tags(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    source_user = db.Column(db.Integer)
    end_user = db.Column(db.Integer)
    post_id = db.Column(db.Integer,db.ForeignKey('posts.id'))

class Graph_friends(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    source_user_id = db.Column(db.Integer)
    end_user_id = db.Column(db.Integer)

if __name__ == '__main__':
    manager.run()