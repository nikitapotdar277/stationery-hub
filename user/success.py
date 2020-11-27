from flask import Blueprint, render_template, Flask, session, flash, redirect

user = Blueprint("success",__name__,static_folder="static", template_folder="template")

@user.route('/')
def success():
	if "name" not in session:
		flash("Please Login to continue","info")
		return redirect('/login')
	else:
		return render_template('user.html', name = session['name'].lower())

@user.route('/rent',methods=['POST'])
def rent():
	return render_template("rent.html")

@user.route('/rentitems',methods=['POST'])
def rentitems():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	item_type = "rent"
	file = request.files['rentitem']
	
	if file and allowed_file(file.filename):
		image = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

	else: 
		flash('Allowed image types are -> png, jpg, jpeg, gif')


	sql = "insert into items(email,item_name,price,item_type,img,sold) values(%s, %s, %s, %s,%s,%s);"
	val = (email,item_name,price,item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	return render_template("index.html")


@user.route('/sell',methods=['POST'])
def sell():
	return render_template("sell.html")

@user.route('/sell1',methods=['POST'])
def sell1():
	email = session["name"] + "@gmail.com"
	item_name = request.form["item"]
	price = request.form["price"]
	file = request.files['sellitem']
	
	if file and allowed_file(file.filename):
		image = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], image))

	else: 
		flash('Allowed image types are -> png, jpg, jpeg, gif')
	
	item_type = "sell"
	sql = "insert into items(email,item_name,price,item_type,img, sold) values(%s, %s, %s, %s, %s, %s);"
	val = (email,item_name,int(price),item_type,image,0)
	mycursor.execute(sql, val)
	mydb.commit()
	return ('success')

@user.route('/order/<string:seller_email>/<string:item_name>/<string:item_type>')
def order(seller_email, item_name, item_type):
	sql1 = "select * from items where email = %s and item_name = %s and item_type = %s;"
	mycursor.execute(sql1, (seller_email, item_name, item_type))
	db_val = mycursor.fetchone()

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