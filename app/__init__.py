import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
db.create_all()
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'moengage'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '1641190706108950',
        'secret': '01d66a77371e95ede317cdb7f473b89c'
    }
}
from app import views
