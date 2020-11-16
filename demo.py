from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from user.success import user
from flask_login import logout_user


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="miniamazon"
)
mycursor = mydb.cursor()

app = Flask(__name__)
app.register_blueprint(user,url_prefix='/user')
app.secret_key = "alsdkjfoinmxsfcdklahfoaasdfkajsdfsdvksdjhfahgudsgkjhuoagh"


#table -> registration

@app.route('/<anything>')
def defaultpg(anything):
	return f"<h1>This the bad url</h1>"


@app.route('/login',methods=["GET","POST"])
def login():

	if "name" not in session:
		
		if request.method == "POST":
			
			email = request.form["username"]
			password = request.form["user_pass"]
			
			sql = "select password from registration where email= '" + email + "';"
			
			mycursor.execute(sql)
			
			db_pass = mycursor.fetchone()
			if db_pass == None or db_pass[0] != password:
				flash("User Name or Password INCORRECT!!")
				return redirect('/login')
			elif db_pass[0] == password:
				session["name"] = email[:email.find('@')]
				return redirect("/user")

		else:
			return render_template('sign_in.html')
	else:
		return redirect('/user')

@app.route('/logout')
def logout():
	session.pop('name', None)
	return redirect('/home')


@app.route('/search', methods=['POST'])
def search():
	search_item = request.form["search_item"]
	sql = "select * from items where item_name = '" + search_item + "';"
	mycursor.execute(sql)
	db_search = mycursor.fetchall()
	# for i in db_search:
	# 	for j in len(i):
	# 		email, item_name, price, item_type = db_search[j]
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
		sql = "select * from registration where email ='" + email + "';" 
		#print(sql)
		mycursor.execute(sql)
		# mydb.commit()
		if ((mycursor.fetchone())== None) and (request.form["psw"] == request.form["psw-repeat"]):
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


@app.route('/lend',methods=['POST'])
def lend():
	return render_template("lend.html")

@app.route('/lenditems',methods=['POST'])
def lenditems():
	email = session["name"]
	item_name = request.form["item"]
	price = 0.00
	item_type = "lend"
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,price,item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return ('/success')

@app.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@app.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"]
	item_name = request.form["item"]
	price = request.form["price"]
	item_type = "sell"
	print('hora ruko')
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,price,item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return ('/success')


@app.route('/')
@app.route('/home')
def home():
	return render_template("index.html")
	

if __name__ == "__main__":
	TEMPLATES_AUTO_RELOAD = True
	app.debug = True
	app.run()