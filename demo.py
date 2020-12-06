from flask import Flask, redirect, url_for, render_template, request, session, flash
import mysql.connector
from user.success import user,path_finder
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
app.config['MAIL_USERNAME'] = os.environ.get("USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("PASSWORD")
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app) 

app.register_blueprint(user,url_prefix='/user')
app.secret_key = "alsdkjfoinmxsfcdklahfoaasdfkajsdfsdvksdjhfahgudsgkjhuoagh"


#table -> registration

def search(page,search_item):

		scan = {

		"user": "items",
		"wishlist" :"wishlist",
		"cart" :"cart"

		}

		if page == "user":
			
			if "name" not in session:
				sql = f"""select * from {scan[page]} where item_name LIKE %s;"""   #LIKE USED
				mycursor.execute(sql, ("%" + search_item + "%",))
				name = "LOGIN"
			else:
				sql = f"""select * from {scan[page]} where email not in ('{session["email"]}') and item_name like '%{search_item}%';"""
				mycursor.execute(sql)
				name = session["name"]
		else:

			sql = f"""select {scan[page]}.product_email,{scan[page]}.item_name,items.price,{scan[page]}.img,items.item_type from {scan[page]} join items on {scan[page]}.item_name = items.item_name and cart_holder='{session["email"]}' and {scan[page]}.item_name like '%t%' order by {scan[page]}.img;"""
			mycursor.execute(sql)
			name = session["name"]
			#print(search_item,type(search_item))
		
		db_search = mycursor.fetchall()
		print (db_search)
		value = {
		0:"IN STOCK",
		1:"NOT IN STOCK"
		}

		link,file_name = path_finder()
		list_ = []


		link = sorted(link, key = lambda x: file_name[link.index(x)])
		file_name.sort()
		# DO NOT TOUCH
		total = 0
		# fname = []
		for index,val in enumerate(file_name):
			for row in (db_search):
				if val in row[-2]:
					list_.append(link[index])
					# print("list--->",link[index])
					# fname.append(val)
					# print("Fname-->",val)
		return db_search,value,list_,name,file_name






# def order(seller_email, item_name, item_type):
# 	sql1 = "select * from items where email = %s and item_name = %s;"
# 	try:
# 		mycursor.execute(sql1, (seller_email, item_name))
# 		db_val = mycursor.fetchone()


# 		# for for emails
# 		sql2 = "insert into orders(email, item_name, price, seller) values (%s, %s, %s, %s);"
# 		val = (session["name"] + "@gmail.com", item_name, db_val[3], seller_email)
# 		mycursor.execute(sql2, val)
# 		mydb.commit()

# 		#change stat to 1 fro all 
# 		sql3 = "update items set sold = 1 where email = %s and item_name = %s;"
# 		mycursor.execute(sql3, (seller_email, item_name))
# 		mydb.commit()

# 		#for emails
# 		seller_msg = Message(
# 			'Hello',
# 			sender=os.environ.get("USERNAME"),
# 			recipients=[seller_email]
# 		)
# 		seller_msg.body = 'Hello! the user ' + session["name"] + '@gmail.com needs ' + item_name + '. They\'ll contact you soon. Thank you!'
# 		mail.send(seller_msg)
# 		buyer_msg = Message(
# 			'Hello',
# 			sender=os.environ.get("USERNAME"),
# 			recipients=[session["name"] + '@gmail.com']
# 		)
# 		buyer_msg.body = 'Hello! the user ' + seller_email + '@gmail.com has been notified about your stationery needs. You may contact them on the above email id. Thank you!'
# 		mail.send(buyer_msg)
# 	except :
# 		flash("Somthing Went Wrong")
# 		return redirect('/')







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
				#print("EMAIL ---->",email)
				session["email"] = email
				session["name"] = email[:email.find('@')]
				session["year"] = db_pass[1]
				session["branch"] = db_pass[2].upper()
				#print(session["year"])
				#print("EMAIL ---->",session["email"])
				return redirect("/user")

		else:
			
			return render_template('login_pg.html')

	else:
		return redirect('/user')

@app.route('/logout')
def logout():
	session.pop('name', None)
	return redirect('/home')

@app.route('/search/<string:page>',methods=["POST"])
def page_search(page):
	search_item = request.form["search_item"]
	db_search,value,list_,name,filename = search(page,search_item)
	return render_template(f'{page}.html', db_search = enumerate(db_search),value=value,list_=list_,name=name,filename=filename)
	


@app.route('/search', methods=['POST'])
def user_search():
	#try:
		search_item = request.form["search_item"]
		db_search,value,list_,name,filename = search("user",search_item)

		return render_template('user2.html', db_search = enumerate(db_search),value=value,list_=list_,name=name,filename=filename)
	# except Exception as e:
	# 	print(e)
	# 	app.logger.info(f"Exception occured while encountering search :{request.url,e}")

	# 	return redirect('/somethingwentwrong')

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
		#print(sql)
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
			flash("You have successfully registered, Login to countine!") #It shoild be in green color
			return redirect("/login")

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
	#print(email,price,item_type,item_name)
	sql = "insert into items(email,item_name,price,item_type) values(%s, %s, %s, %s);"
	val = (email,item_name,price,item_type)
	mycursor.execute(sql, val)
	mydb.commit()
	return render_template("user.html")

# @app.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
# def ord(seller_email,item_name,item_type):
# 	try:

# 		return('Ordered! Please check your mail')
# 	except Exception as e:
# 		#print("Exception:",e)
# 		app.logger.info(f"Exception occured while ORDER :{request.url,e}")
# 		flash('Login to Place the Order')
# 		return redirect('/login')

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