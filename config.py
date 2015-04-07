import os
WTF_CSRF_ENABLED = True
SECRET_KEY = '#!$~`you-will-never-guess@%^&'

basedir = os.path.abspath(os.path.dirname(__file__))
#basedir = os.path.join(ldir,'pmp')
SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost/moengage'
