import os
import pdfkit
from flask import Flask, render_template, send_file, request, redirect, url_for
from flaskext.mysql import MySQL
from flask_mail import Mail, Message

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)
app.config.from_object(__name__)
mail = Mail(app)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'honors'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'smart26jn@gmail.com'
app.config['MAIL_PASSWORD'] = 'smartijn26'

mail = Mail(app)

@app.route('/admin-dash', methods=['GET', 'POST'])
def mainIndex():
	# adding annoucment
	# if request.method == 'POST':
		# code to add to DB Here

	return render_template("admin-dash.html")
	
@app.route('/forgotPassword', methods=['GET', 'POST'])
def passwordChange():
    print 'password Change ...'
    msg = Message("Hello", sender="smart26jn@gmail.com", recipients=["shaikhlaila26@gmail.com"])
    msg.body = "This is the email body"              
    print 'msg is sfsdfs'
    mail.send(msg)
    print 'after mail send msg'
    return render_template("forgotPassword.html")

@app.route('/announcements')
def manage():
	return render_template("manage-announcements.html")
	
@app.route('/students')
def newstudent():
	return render_template("newstudent.html")
	
@app.route('/import')
def newChecksheetData():
	return render_template("import.html")

@app.route('/')
def HomePage():
	return render_template('Login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print 'have we reached over here '
    if request.method =='POST':
        cursor = mysql.get_db().cursor()
    
        username = request.form['Username']
        Password = request.form['Password']
        query = "select * from users where username= '%s' and Password='%s';"% (username, Password)
        
        cursor.execute(query)
        
        UsersQueryFetch=[]
        UsersQueryFetch.append(cursor.fetchone())
        
        if UsersQueryFetch[0] is None:
            print 'unsuccessful'
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
