from app import db
from flask.ext.login import LoginManager, UserMixin
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    social_id = db.Column(db.String(120),index=True,unique=True)
    gender = db.Column(db.String(10))
    country = db.Column(db.String(100))
    phone = db.Column(db.String(10))
    timezone = db.Column(db.String(40))
    image = db.Column(db.String(300),index=True)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Graph_friends(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    source_user_id = db.Column(db.Integer)
    end_user_id = db.Column(db.Integer)

class User_friends(db.Model,UserMixin):
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


        