from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from user.success import user
from flask_mail import Mail, Message


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
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
	email = session["name"] + "@gmail.com"
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
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	item_type = "sell"
	print(email,price,item_type,item_name)
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,int(price),item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return ('/success')

@app.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
def order(seller_email, item_name, item_type):
	sql1 = "select * from items where email = %s and item_name = %s and item_type = %s;"
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

@app.route('/')
@app.route('/home')
def home():
	return render_template("index.html")
	
	
	

if __name__ == "__main__":
	TEMPLATES_AUTO_RELOAD = True
	app.debug = True
	app.run()