from flask import Flask, render_template, redirect, url_for, request, g
import sqlite3

app = Flask(__name__)
app.database = "empmgt.db"

@app.route('/')
def home():
	g.db=connect_db()
	cur = g.db.execute('select fname,lname,jobrole from emp_login')
	employee_login = [dict(fname=row[0], lname=row[1], jobrole=row[2])for row in cur.fetchall()]
	g.db.close()
	return render_template('home.html', employee_login=employee_login)

@app.route('/contact')
def contact():
	return render_template('contact.html')
	
@app.route('/gallery')
def gallery():
	return render_template('gallery.html')

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
			return redirect(url_for('home'))
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
			return redirect(url_for('home'))
		else:
			error = "Invalid Credentials. Please try again."

	g.db.close()
	return render_template('login.html', error=error)

def connect_db():
	return sqlite3.connect(app.database)

if __name__ == '__main__':
	app.run(debug=True)