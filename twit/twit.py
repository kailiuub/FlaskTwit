#import packages
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack
import os
from datetime import datetime

app=Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://ee:123@localhost/mydb'
#config environments
app.config.update(dict(
SECRET_KEY=os.urandom(24),
DEBUG=True,
SQLALCHEMY_DATABASE_URI='postgresql://ee:123@localhost/mydb'
))

db=SQLAlchemy(app)


#***Initialize blogdb for storing posting***
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


#***ADD and LIST posting***  (view and processing)
@app.route('/posting/<user>', methods=['POST','GET'])
def posting(user):
	if request.method == 'POST':
		if not session.get('logged_in'):
			abort(401)
		username=request.form['username']
		user=username	
		title=request.form['title']
		posting=request.form['posting']
		timenow=datetime.now()
		time=timenow.strftime('%Y/%m/%d-%H:%M:%S')	
		if title and posting:
			bdb=Blogdb(username,title,posting,time)
			#automatically select blogdb to add and commit
			db.session.add(bdb)
			db.session.commit()	

	#show blog posting in a REVERSE order	
	dblist=Blogdb.query.filter_by(username=user).order_by(desc(Blogdb.id))
	#show the profile specified by url <user>	
	return render_template('blog.html', dblist=dblist, user=user)


#main
if __name__=="__main__":
	app.run()


