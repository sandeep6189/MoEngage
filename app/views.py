from app import app,lm,db
from models import User,User_friends,Graph_friends,Posts,Tags
from flask import request, redirect, url_for, send_from_directory ,flash ,render_template ,g ,session
from flask_debugtoolbar import DebugToolbarExtension
from flaskext.mysql import MySQL
from flask.ext.login import LoginManager , login_user, logout_user, current_user, login_required , UserMixin
import json,datetime,time,MySQLdb,urllib2
from user_agents import parse
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
from flask.ext.security import Security , SQLAlchemyUserDatastore
from oauth import OAuthSignIn
#-------------------Log imports-----------------------#
#import logging
#from logging.handlers import RotatingFileHandler
#from logging import Formatter
#from logging.handlers import SMTPHandler
#-----------------------------------------------------#

#set file handlers-------------------------------------
'''
file_handler = RotatingFileHandler('error.log',maxBytes=1024 * 1024 * 100, backupCount=2)
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
))
app.logger.addHandler(file_handler)
'''
#------------------------------------------------------
# initializing required modules
mysql = MySQL()
mysql.init_app(app)
ADMINS = ['sandeep6189@gmail.com']

app.debug = True

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    return render_template('login.html',
                           title='Sign In')


@app.route("/index", methods=['GET'])
@login_required
def index():
	ua = request.headers.get('User-Agent')
	user_agent = parse(ua)
	user = g.user.nickname
	image = g.user.image
	user_id = g.user.id
	return render_template('index.html',title='home',user=user,image=image,id=user_id)

def dump(obj):
  for attr in dir(obj):
    print "obj.%s = %s" % (attr, getattr(obj, attr))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email,fullname,gender,timezone,image,locale,app_using_friends = oauth.callback()
    #print image
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
 
    if not user:
        user = User(social_id=social_id, nickname=username,username=fullname,email=email,gender=gender,timezone=timezone,image=image,country=locale)
        db.session.add(user)
        db.session.commit()
    # add friends in graph node
    for friend in app_using_friends:
    	friend_social_id = "facebook$"+friend['id']
    	friend_obj = User.query.filter_by(social_id=friend_social_id).first()
    	friend_id = friend_obj.id
    	is_friend = Graph_friends.query.filter_by(source_user_id=user.id,end_user_id=friend_id).first()
    	if not is_friend:
    		#add into the graph
    		add_node = Graph_friends(source_user_id=user.id,end_user_id=friend_id)
    		db.session.add(add_node)
        	db.session.commit()
    login_user(user, True)

    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/make_posts',methods=['POST','GET'])
@login_required
def make_posts():
	if request.method=="GET":
		user = g.user.nickname
		email = g.user.email
		image = g.user.image
		user_id = g.user.id
		return render_template('make_posts.html',user=user,email=email,image=image,id=user_id)
	elif request.method=="POST":
		content = request.form["post_content"]
		user_id = request.form['id']
		list_of_tags = json.loads(request.form['tags'])
		list_of_tags.append(user_id) # little hacky way, doing because of shortage of time
		# first insert the post, get the post id and then insert in the tag table 
		post_obj = Posts(post_content=content,source_user=user_id,created_at=datetime.datetime.now())
		db.session.add(post_obj)
        db.session.commit()

        post_id = post_obj.id
        # now make tags
        for tag in list_of_tags:
        	tag_obj = Tags(source_user=user_id,end_user=tag,post_id=post_id)
        	db.session.add(tag_obj)
        	db.session.commit()        	
	return "Success"			

@app.route('/get_posts',methods=['POST'])
@login_required
def get_posts():
	if request.method=="POST":
		user_id = int(request.form['id'])
		all_posts = Tags.query.filter_by(end_user=user_id)
		list_of_posts = []
		for post in all_posts:
			dic_row = {}
			#get post id, from post id i.e the primary key
			post_id = post.post_id
			post_obj = Posts.query.get(post_id)
			source_user_obj = User.query.get(post.source_user)
			dic_row['content'] = post_obj.post_content
			dic_row['posted_by'] = source_user_obj.username
			dic_row['pic'] = source_user_obj.image
			dic_row['created_at'] = post_obj.created_at.strftime("%A, %d. %B %Y %I:%M%p")
			list_of_posts.append(dic_row)
		return	json.dumps(list_of_posts)

def get_friends_data(data):
	lis = []
	count = 0
	distinct_bundle = {}
	for row in data:
		row_data = {}
		row_data['name'] = row[0]
		row_data['id'] = row[1]
		row_data['pic'] = row[2]
		lis.append(row_data)
	return json.dumps(lis)

@app.route("/find_friends",methods=['POST'])
def friends():
	if request.method == "POST":
		query = request.form['query']
		user_id = int(request.form['id'])
		all_user_friends = Graph_friends.query.filter_by(source_user_id=user_id)
		print "query", all_user_friends
		all_data = []
		for i in all_user_friends:
			cursor = mysql.connect().cursor()
			cursor.execute("SELECT user.username, user.id,user.image FROM user \
			WHERE user.id = %s AND user.username LIKE '%%%s%%'" % (i.end_user_id,query))
			data = cursor.fetchone()
			cursor.close()
			print data
			if data:
				all_data.append(data)
		print all_data
		return get_friends_data(all_data)