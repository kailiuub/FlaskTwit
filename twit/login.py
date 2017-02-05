#import twit for posting
from twit import *


#***Initialize userdb for user login***
class Userdb(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(20), nullable=False, unique=True)
	email=db.Column(db.String(20),nullable=False, unique=True)
	password=db.Column(db.String(20),nullable=False)
	
	def __init__(self, username, email, password):
		self.username=username
		self.email=email
		self.password=password
	
	def __repr__(self):
		return "User: {}".format(self.logname)


#***CREATE view for signup***
@app.route('/')
def index():
	return render_template('register.html')

#***CREATE view for signup/register processing***
@app.route('/adduser', methods=['POST','GET'])
def adduser():
	addusername=request.form['username']
	addemail=request.form['email']
	addpassword=request.form['password']
	# no empty entry	
	if addusername and addemail and addpassword:
		# check db for duplicate username and email
		usernamedb=Userdb.query.filter_by(username=addusername).first()
		emaildb=Userdb.query.filter_by(email=addemail).first()
		if usernamedb or emaildb:
			flash("username or email already existed")
		# if no dupblicate, add record to db		
		else:
			newuser=Userdb(addusername, addemail, addpassword)
			db.session.add(newuser)
			db.session.commit()
			flash("You are been registered successfully.")	
	else:
		flash("Empty username or password")
	return redirect(url_for('index'))
	

#***CREATE view for login*** (view)
@app.route('/login')
def login():
	return render_template('login.html')

#***PROCESS login view*** (processing)
@app.route('/compare',methods=['GET','POST'])
def compare():
	logemail=request.form['email']
	logpassword=request.form['password']
	if logemail and logpassword:
		logdb=Userdb.query.filter_by(email=logemail).first()
		if logdb: # if user email is found in db then compare password		
			if logpassword == logdb.password:
				session['logged_in']=True
				return redirect(url_for('posting', user=logdb.username))	
		else: 
			flash('invalid email or password')
	else:
		flash('empty email or password')
	return redirect(url_for('login'))

#***CREATE view for logout***
@app.route('/logout')
def logout():
	session.pop('logged_in', None)
	flash('you were logged out')
	return redirect(url_for('login'))


#main
if __name__=="__main__":
	app.run()


