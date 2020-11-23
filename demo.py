from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from user.success import user
from flask_mail import Mail, Message
import sys


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=sys.argv[1],
  database="miniamazon"
)

mycursor = mydb.cursor()

app = Flask(__name__)

app.register_blueprint(user,url_prefix='/user')
app.secret_key = "alsdkjfoinmxsfcdklahfoaasdfkajsdfsdvksdjhfahgudsgkjhuoagh"


#table -> registration

@app.errorhandler(404)
def defaultpg(anything):
	app.logger.info(f"Page not found :{request.url}")
	return render_template('notfound.html')


@app.route('/login',methods=["GET","POST"])
def login():

	if "name" not in session:
		
		if request.method == "POST":
			
			email = request.form["username"]
			password = request.form["user_pass"]
			
			sql = f"""select password from registration where email = '{email}';"""
			
			try:
				mycursor.execute(sql)
			except:
				redirect('/somethingwentwrong')
			db_pass = mycursor.fetchone()
			if db_pass == None or db_pass[0] != password:
				flash("User Name or Password INCORRECT!!")
				return redirect('/login')
			elif db_pass[0] == password:
				session["name"] = email[:email.find('@')]
				return redirect("/user")

		else:
			
			return render_template('login_pg.html')

	else:
		return redirect('/user')

@app.route('/logout')
def logout():
	session.pop('name', None)
	return redirect('/home')


@app.route('/search', methods=['POST'])
def search():
	search_item = request.form["search_item"]
	sql = "select * from items where item_name = %s and sold = %s;"
	mycursor.execute(sql, (search_item, False))
	db_search = mycursor.fetchall()
	return render_template('table.html', db_search = db_search)

@app.route('/table')
def table():
	return render_template('table.html')

@app.route('/register',methods=['GET','POST'])
def register():
	
	if request.method == "POST":
	
		email = request.form["email"]
		branch = request.form["branch"]
		year = request.form["year"]
		password = request.form["psw"]
		sql = f"""select * from registration where email = '{email}' """
		print(sql)
		try:
			mycursor.execute(sql)
		except:
			redirect('/notfound')
			
		# mydb.commit()
		flag = 1
		if (request.form["psw"] != request.form["psw-repeat"]) or (len(password)< 8):
			flag = 0
			flash("Password should be atleast 8 characters long and both should match")
			return redirect('/register')
			
		if ((mycursor.fetchone())== None) and (request.form["psw"] == request.form["psw-repeat"] and flag):
			sql = "insert into registration(email,branch,year,password) values(%s, %s, %s, %s);"
			val = (email,branch,year,password)
			#print(sql)
			mycursor.execute(sql,val)
			mydb.commit()
			return f"<h1>You have successfully entered the right data</h1>"
		else:
			flash("Username already exists please Login")
			return redirect("login")
	else:
		return render_template('register.html')



@app.route('/')
@app.route('/home')
def home():
	if "name" not in session:
		return render_template("index.html")

	else:
		return redirect("user")
	

if __name__ == "__main__":
	TEMPLATES_AUTO_RELOAD = True
	app.debug = True
	app.run()