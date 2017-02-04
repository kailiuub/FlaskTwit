#import packages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
import os

app=Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://ee:123@localhost/mydb'
#config environments
app.config.update(dict(
SECURITY_KEY=os.urandom(24),
DEBUG=True,
SQLALCHEMY_DATABASE_URI='postgresql://ee:123@localhost/mydb'
)
)

db=SQLAlchemy(app)

#initialize userdb
class Userdb(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20),nullable=False)
	password=db.Column(db.String(20),nullable=False)
	
	def __init__(self, username, password):
		self.username=username
		self.password=password
	
	def __repr__(self):
		return "User: {}".format(self.username)



#initialize blogdb
class Blogdb(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), nullable=False)	
	title=db.Column(db.String(50),nullable=False)	
	posting=db.Column(db.String(500),nullable=False)
	time=db.Column(db.String(20), nullable=False)	

	def __init__(self,username, title, posting, time):
		self.username=username		
		self.title=title
		self.posting=posting
		self.time=time
	
	def __repr__(self):
		return "Title: {}".format(self.title)



#create view for signup




#create view for login




#create view to add posting
@app.route('/add', methods=['POST'])
def add():
	username=request.form['username']	
	title=request.form['title']
	posting=request.form['posting']
	time=request.form['time']	
	if title and posting:
		bdb=Blogdb(username,title,posting,time)
		db.session.add(bdb)
		db.session.commit()
	return redirect(url_for('posting',user='kai'))

#create view for list posting
@app.route('/posting/<user>', methods=['GET','POST'])
def posting(user):
	dblist=Blogdb.query.filter_by(username=user)
	#show blog posting in a reverse order
	
	#only show current user's profile
	return render_template('blog.html', dblist=dblist, user=user)
	



#create view for logout 






#main
if __name__=="__main__":
	app.run()


