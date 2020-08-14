from flask import Flask, session, render_template, redirect, url_for, request, g
import sqlite3

app = Flask(__name__)
app.database = "empmgt.db"
app.secret_key = "delrockz"


@app.route('/')
def home():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('home.html', username=username)


@app.route('/contact',methods=['GET','POST'])
def contact():
	error = None
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.cursor()
	if request.method == 'POST':
		cur.execute("insert into feedback values(?,?,?,?)", (request.form['name'],request.form['email'],request.form['subject'],request.form['message'],))
		g.db.commit();
		cur.execute("select * from feedback where email=?",(request.form['email'],))
		rows=cur.fetchall()
		counter=1
		for row in rows:
			counter+=1
		if(counter==2):
			error = "Feedback sent successfully"
		else:
			error = "Please check your details"
	g.db.close()
	return render_template('contact.html' ,error=error ,username=username)


@app.route('/viewfeedback')
def viewfeedback():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.execute("select * from feedback")
	feedback = [dict(name=row[0], email=row[1], subject=row[2], message=row[3])for row in cur.fetchall()]
	g.db.close()
	return render_template('admin.html',feedback=feedback,username=username,showfeedback='true')


@app.route('/register', methods=['GET', 'POST'])
def register():
	error = None
	g.db=connect_db()
	cur = g.db.cursor()
	if request.method == 'POST':
		cur.execute("insert into emp_login values(?,?,?,?,?,?,?,?,?)", (request.form['user_fname'],request.form['user_lname'],request.form['user_email'],request.form['contact_number'],request.form['user_name'],request.form['user_password'],request.form['birthday'],request.form['user_bio'],request.form['user_job'],))
		g.db.commit();
		cur.execute("select * from emp_login where username=?",(request.form['user_name'],))
		rows=cur.fetchall()
		counter=1
		for row in rows:
			counter+=1
		if(counter==2):
			return redirect(url_for('login'))
		else:
			error = 'Please check your details'
	g.db.close()
	return render_template('reg.html',error=error)
	

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	g.db=connect_db()
	cur = g.db.cursor()
	if request.method == 'POST':
		cur.execute("select * from emp_login where username=? and pw=?", (request.form['username'],request.form['password'],))
		counter=1
		rows=cur.fetchall()
		for row in rows:
			counter+=1
		if(counter==2):
			session['username'] = request.form['username']
			if session['username'] == 'admin':
				return redirect(url_for('admin'))
			else:
				return redirect(url_for('home'))
		else:
			error = "Invalid Credentials. Please try again."
	g.db.close()
	return render_template('login.html', error=error)


@app.route('/admin')
def admin():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	
	return render_template('admin.html', username=username)


def connect_db():
	return sqlite3.connect(app.database)


@app.route('/showemp')
def showemp():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.execute('select fname,lname,email,dob,bio,jobrole from emp_login')
	employee_login = [dict(fname=row[0], lname=row[1], email=row[2],dob=row[3], bio=row[4], jobrole=row[5])for row in cur.fetchall()]
	g.db.close()
	return render_template('admin.html',employee_login=employee_login, username=username, showemployees='true')


@app.route('/leaverequest', methods=['GET', 'POST'])
def leave():
	error=None
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.cursor()
	if request.method == 'POST':
		cur.execute("insert into leave_request values(?,?,?,?,?,?,?,?,?)", (username,request.form['fname'],request.form['lname'],request.form['dept'],request.form['pos'],request.form['phno'],request.form['date'],request.form['reason'],"Waiting",))
		g.db.commit();
		cur.execute("select * from leave_request where fname=?",(request.form['fname'],))
		rows=cur.fetchall()
		counter=1
		for row in rows:
			counter+=1
		if(counter==2):
			error = "Leave request sent successfully!"
		else:
			error = "Please check your details"
	g.db.close()
	return render_template('leave_request.html',username=username,error=error)


@app.route('/password',methods=['GET','POST'])
def password():
	error = None
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.cursor()
	if request.method == 'POST':
		cur.execute("update emp_login set pw=? where username=?",(request.form['pw'],username,))
		g.db.commit();
		cur.execute("select pw from emp_login where pw=?",(request.form['pw'],))
		rows=cur.fetchall()
		counter=1
		for row in rows:
			counter+=1
		if(counter==2):
			error = "Password changed successfully"
			session.pop('username', None)
	g.db.close()
	return render_template('home.html',error=error, passwordchange='true', username=username)


@app.route('/viewleaves', methods=['GET','POST'])
def viewleave():
	error = None
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.execute('select fname,lname,dept,pos,leavedate,reason,status from leave_request')
	leave_request = [dict(fname=row[0], lname=row[1], dept=row[2],pos=row[3],leavedate=row[4],reason=row[5],status=row[6])for row in cur.fetchall()]
	cur = g.db.cursor()
	if request.method == 'POST':
		option = request.form['status']
		cur.execute("update leave_request set status=?  where fname=?",(option,request.form['fname']))
		g.db.commit();
		cur.execute("select * from leave_request where status=? AND fname=?",(option,request.form['fname']))
		rows=cur.fetchall()
		counter=1
		for row in rows:
			counter+=1
		if(counter==2):
			error = "Updated Successfully!"
			return redirect(url_for('viewleave'))
		else:
			error = "Update Failed"
	g.db.close()
	return render_template('admin.html',error=error ,leave_request=leave_request, username=username, show = 'true')


@app.route('/leavestatus')
def leavestatus():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.execute("select fname,dept,pos,leavedate,reason,status from leave_request where username=?",(username,))
	status_request = [dict(fname=row[0], dept=row[1],pos=row[2],leavedate=row[3], reason=row[4],status=row[5])for row in cur.fetchall()]
	g.db.close()
	return render_template('home.html', status_request=status_request, username=username, show = 'true')


@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('home'))


@app.route('/gallery')
def gallery():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('gallery.html',username=username)


@app.route('/notices')
def notices():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	g.db=connect_db()
	cur = g.db.execute('select fname,lname,jobrole from emp_login where rowid=(select max(rowid) from emp_login)')
	employee_login = [dict(fname=row[0], lname=row[1], jobrole=row[2])for row in cur.fetchall()]
	g.db.close()
	return render_template('notices.html',employee_login=employee_login,username=username)


@app.route('/birthday')
def birthday():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('birthday.html',username=username)


@app.route('/holiday')
def holiday():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('holiday.html',username=username)


@app.route('/policy')
def policy():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('policy.html',username=username)


@app.route('/about')
def about():
	if 'username' in session:
		username = session['username']
	else:
		username = None
	return render_template('about.html',username=username)


if __name__ == '__main__':
	app.run(debug=True)