from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from user.success import user
from flask_mail import Mail, Message
import sys
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=sys.argv[1],
  database="miniamazon"
)
mycursor = mydb.cursor()

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'stationeryhub123@gmail.com'
app.config['MAIL_PASSWORD'] = 'snydbmsshub'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

app.register_blueprint(user,url_prefix='/user')
app.secret_key = "alsdkjfoinmxsfcdklahfoaasdfkajsdfsdvksdjhfahgudsgkjhuoagh"


#table -> registration

@app.errorhandler(404)
def defaultpg(anything):
	app.logger.info(f"Page not found :{request.url}")
	return render_template('notfound.html')

@app.errorhandler(405) #its basically method not found...but we are doing 403 forbidden
def forbidden(anything):
	app.logger.info(f"Page Restricted: {request.url}")
	return render_template("forbidden.html")

@app.route('/login',methods=["GET","POST"])
def login():

	if "name" not in session:
		
		if request.method == "POST":
			
			email = request.form["username"]
			password = request.form["user_pass"]
			
			sql = f"""select password,year,branch from registration where email = '{email}';"""
			
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
				session["year"] = db_pass[1]
				session["branch"] = db_pass[2].upper()
				print(session["year"])
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
	try:
		search_item = request.form["search_item"]
		sql = "select * from items where item_name LIKE %s and sold = %s;"
		print(search_item,type(search_item))
		mycursor.execute(sql, ("%" + search_item + "%", 0))
		db_search = mycursor.fetchall()
		print (db_search)
		return render_template('table.html', db_search = db_search)
	except Exception as e:
		print(e)
		app.logger.info(f"Exception occured while encountering search :{request.url,e}")

		return redirect('/somethingwentwrong')

@app.route('/table')
def table():
	return render_template('table.html')

@app.route('/register',methods=['GET','POST'])
def register():
	
	if request.method == "POST":
	
		email = request.form["email"]
		branch = request.form["branch"].upper()
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


@app.route('/rent',methods=['POST'])
def lend():
	return render_template("rent.html")

@app.route('/rentitems',methods=['POST'])
def lenditems():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	try:
		price = int(request.form["price"])
	except:
		flash("Price must be a number!!")
		return redirect('/rent')
		
	item_type = "lend"
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,price,item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return render_template("user.html")

@app.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@app.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	try:
		price = int(request.form["price"])
	except:
		flash("Price must be a number!!")
		return redirect('/sell')
	item_type = "sell"
	print(email,price,item_type,item_name)
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,price,item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return render_template("user.html")

@app.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
def order(seller_email, item_name, item_type):
	sql1 = "select * from items where email = %s and item_name = %s and item_type = %s;"
	try:
		mycursor.execute(sql1, (seller_email, item_name, item_type))
		db_val = mycursor.fetchone()


		# img = img
		sql2 = "insert into orders(email, item_name, price, seller) values (%s, %s, %s, %s);"
		val = (session["name"] + "@gmail.com", item_name, db_val[3], seller_email)
		mycursor.execute(sql2, val)
		mydb.commit()

		sql3 = "update items set sold = 1 where email = %s and item_name = %s and item_type = %s;"
		mycursor.execute(sql3, (seller_email, item_name, item_type))
		mydb.commit()

		seller_msg = Message(
			'Hello',
			sender='stationeryhub123@gmail.com',
			recipients=[seller_email]
		)
		seller_msg.body = 'Hello! the user ' + session["name"] + '@gmail.com needs ' + item_name + '. They\'ll contact you soon. Thank you!'
		mail.send(seller_msg)
		buyer_msg = Message(
			'Hello',
			sender='stationeryhub123@gmail.com',
			recipients=[session["name"] + '@gmail.com']
		)
		buyer_msg.body = 'Hello! the user ' + seller_email + '@gmail.com has been notified about your stationery needs. You may contact them on the above email id. Thank you!'
		mail.send(buyer_msg)
		return('Ordered! Please check your mail')
	except Exception as e:
		#print("Exception:",e)
		app.logger.info(f"Exception occured while ORDER :{request.url,e}")
		flash('Login to Place the Order')
		return redirect('/login')

@app.route('/')
def home():

	if "name" not in session:
		return render_template("index.html")

	else:
		return redirect("user")

@app.route('/home')
def red_to_home():
	return redirect('/')


if __name__ == "__main__":
	TEMPLATES_AUTO_RELOAD = True
	app.debug = True
	app.run()