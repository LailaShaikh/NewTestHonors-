import os,random, string

from flask import Flask, render_template, send_file, request, redirect, url_for
# from flaskext.mysql import MySQL
from flask_mail import Mail, Message

# changed the import for MySQLdb to this. works with python3 now.
# pandas works much better with python3. To use python2 we would have
# to install all these other packages and virtual enviornments.
import pymysql


# import pdfkit
import pandas as pd
from flask import Flask, render_template, send_file, request, redirect, url_for, session
from flaskext.mysql import MySQL
from sqlalchemy import create_engine
from datetime import datetime


app = Flask(__name__)

mysql = MySQL()
mysql.init_app(app)
app.config.from_object(__name__)

mail = Mail(app)
mail.init_app(app)

app.secret_key = os.urandom(24)


app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'honors'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'automaticmessage05@gmail.com'
app.config['MAIL_PASSWORD'] = 'automaticmessage05gmail.com'
app.config['USER_MAIL'] = 'automaticmessage05@gmail.com'


mail = Mail(app)

# connection = pymysql.connect(host='localhost', user='mikaela', password='peyton15', db='honors', charset='uft8mb4', cursorclass=pymysql.cursors.DictCursor)


@app.route('/admin-dash', methods=['GET', 'POST'])
def mainIndex():
	# adding annoucment
	# if request.method == 'POST':
		# code to add to DB Here
	return render_template("admin-dash.html")

@app.route('/forgotPassword', methods=['GET', 'POST'])
def passwordChange():
	return render_template("forgotPassword.html")

# @app.route('/emailRecovery', methods=['GET', 'POST'])
# def EmailRecovery():
# 		if request.method == 'POST':
# 			#generating a random password
# 			length = 7
# 			chars = string.ascii_letters + string.digits + '!@#$%^&*()'
# 			random.seed = (os.urandom(1024))
# 			temporaryPassword =''.join(random.choice(chars) for i in range(length))
#
# 			#sending an email with a random password
# 			emailRecovery = request.form['email']
# 			print(emailRecovery)
# 			#sending email
# 			msg = Message("Hello",sender=app.config['USER_MAIL'], recipients=[emailRecovery])
# 			msg.body = temporaryPassword
# 			mail.send(msg)
# 			return render_template('Login.html')



@app.route('/announcements')
def manage():
	return render_template("manage-announcements.html")

@app.route('/students')
def newstudent():
	return render_template("newstudent.html")

@app.route('/import')
def newChecksheetData():
	# __tablename__ = "h_prices"
	# id = db.Column(db.Integer, primary_key=True)
	# pcode = db.Column(db.String(15))
	# price_1995 = db.Column(db.Integer)
	# price_2015 = db.Column(db.Integer)
	# change = db.Column(db.Numeric)



	# this code inserts into the DB we have setup. I created the checksheet-test.csv
	# and added it to the github. I created an account with the username 'mikaela'
	# and password 'peyton15', you can change those to match you local DB and it
	# will work.
	engine = create_engine('mysql+pymysql://mikaela:peyton15@localhost/honors', echo='debug')

	df = pd.read_csv('static/checksheet-alldata.csv', parse_dates=['Initial essay', 'Date 1', 'Date 2',
	'Date 3', 'Date 4', 'Date 5', 'Date 6', 'Date 7', 'Date 8'])



	users_df = df[['ID','Last Name', 'First Name', 'email', 'Admitted', 'duPont Code']]
	users_df = users_df.set_index('ID')
	users_df.columns = ['last_name', 'first_name', 'username', 'admitted', 'code']

	users_df.to_sql('users', engine, if_exists='replace', index='ID')

	checksheet_df = df.iloc[:, 6:]

	checksheet_df.columns = ['status', 'comments', 'term', 'major','Advisor',
	'initial_essay', 'co_curricular1', 'co_curricular1_date', 'co_curricular2',
	'co_curricular2_date', 'co_curricular3', 'co_curricular3_date',
	'co_curricular4', 'co_curricular4_date', 'co_curricular5', 'co_curricular5_date',
	'co_curricular6', 'co_curricular6_date',  'co_curricular7', 'co_curricular7_date',
	'co_curricular8', 'co_curricular8_date','fsem', 'fsem_date', 'hn_course1',
	'hn_course1_date', 'hn_course2', 'hn_course2_date', 'hn_course3', 'hn_course3_date',
	'research_course', 'research_course_date', 'capstone', 'capstone_date', 'honr201',
	'honr201_date', 'leadership', 'mentoring', 'honr_port1', 'honr_port2', 'honr_port3',
	'honr_port4', 'exit_interview']



	checksheet_df.insert(0, 'ID', df['ID'])
	checksheet_df = checksheet_df.set_index('ID')

	print(checksheet_df['initial_essay'])
	print(checksheet_df['co_curricular1_date'])


	checksheet_df.to_sql('checksheet', engine, if_exists='replace', index='ID')
	print("PAST TO_SQL")

	return render_template("import.html")

@app.route('/student-dash', methods=['Get', 'POST'])
def mainstudent():
	students = {'username': 'test', 'password' : 'test'}
	return render_template("student-dash.html", student=student)

@app.route('/')
def HomePage():
	return render_template('Login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = ""
	print("have we reached over here ")
	if request.method =='POST':
		cursor = mysql.get_db().cursor()
		username = request.form['Username']
		Password = request.form['Password']
		query = "select * from users where username= '%s' and Password='%s';"% (username, Password)
		cursor.execute(query)

		UsersQueryFetch=[]
		UsersQueryFetch.append(cursor.fetchone())

		if UsersQueryFetch[0] is None:
			form = "Authentication failed! Try again"
			return render_template('Login.html',form=form )
		else:
			query = "select status from users;"
			cursor.execute(query)
			status = cursor.fetchone()
			if(status == 'student'):
				#adding student dashboard method name and take off the below method name'MainIndex'
				return redirect(url_for('mainIndex'))
			else:
				return redirect(url_for('mainIndex'))
	return render_template('Login.html')



# start the server
if __name__ == '__main__':
	app.run(host=os.getenv('IP', '0.0.0.0'), port =int(os.getenv('PORT', 8080)), debug=True)
